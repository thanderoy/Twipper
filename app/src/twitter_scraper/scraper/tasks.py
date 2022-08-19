"""
Defines functions(tasks) working with Celery
    fetch_tweets -Fetches tweets will be run periodically in Celery.
    send_email - Sends a notification email after saving new record on
        DB in the background. Will be initiated by Celery from a Redis
        queue to enhance app response time.

"""

import logging

from celery import shared_task
from django.conf import settings
from django.core.mail import EmailMessage
from django.template.loader import render_to_string

from .models import Tweet

logger = logging.getLogger('main')
logger.setLevel(logging.DEBUG)


@shared_task()
def send_email(tweet_text, tweet_likes, tweet_rts, tweet_replies):
    """Sends an email notification for new Tweets saved in DB"""

    template = render_to_string('scraper/email_template.html',
                                {
                                    'tweet_text': tweet_text,
                                    'tweet_rts': tweet_rts,
                                    'tweet_likes': tweet_likes,
                                    'tweet_replies': tweet_replies,
                                }
                                )

    email = EmailMessage(
        'New Tweet Retrieved', template,
        settings.EMAIL_HOST_USER, ['roy.thande@gmail.com']
        )

    email.fail_silently = False
    email.content_subtype = 'html'
    email.send()
    logger.info("Email Sent")


@shared_task()
def fetch_tweets(username, no_of_tweets):

    if username != 'username' or no_of_tweets != 'no_of_tweets':

        # Send GET request with Twitter username and get user id in response
        try:
            user_response = settings.CLIENT.get_user(
                username=username,
                user_auth=True
                )
            user_id = user_response.data.id

        except Exception:
            logger.error("Error retrieving user ID for username %s", username)

        # Send GET request with obtained user id and get tweet data in response
        try:
            tweet_response = settings.CLIENT.get_users_tweets(
                user_id,
                max_results=no_of_tweets,
                user_auth=True,
                tweet_fields='public_metrics',
                )
        except Exception:
            logger.error("Error retriveing Tweets for username %s", username)

        for tweet in tweet_response.data:

            tweet_id = tweet.id
            tweet_text = tweet.text
            tweet_rts = tweet['public_metrics']['retweet_count']
            tweet_likes = tweet['public_metrics']['like_count']
            tweet_replies = tweet['public_metrics']['reply_count']

            obj, created = Tweet.objects.get_or_create(
                tweet_id=tweet_id, tweet_text=tweet_text,
                tweet_rts=tweet_rts, tweet_likes=tweet_likes,
                tweet_replies=tweet_replies, tweet_author=username,
                )

            if created is True:
                send_email.delay(
                    tweet_text, tweet_likes, tweet_rts, tweet_replies
                )
            logger.info("Awaiting send_email")

    else:
        # print("Failed to provide username and number of Tweets")
        logger.info("Failed to provide username and number of Tweets")
