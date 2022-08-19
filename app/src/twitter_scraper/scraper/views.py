import logging

from django.conf import settings
from django.contrib import messages
from django.core.paginator import Paginator
from django.shortcuts import HttpResponseRedirect, get_object_or_404, render
from django.urls import reverse

from .forms import InputForm
from .models import Tweet
from .tasks import fetch_tweets

logger = logging.getLogger('main')
logger.setLevel(logging.DEBUG)


def like_unlike_tweet(request, id):
    tweet = Tweet.objects.get(tweet_id=id)

    try:
        settings.CLIENT.like(tweet.tweet_id)
    except Exception:
        logger.error("Problem accessing API")

    if tweet.liked is False:
        Tweet.objects.filter(tweet_id=tweet.tweet_id).update(
            liked=1, tweet_likes=tweet.tweet_likes + 1)
        logger.info("Tweet liked. Tweet ID: %s", tweet.tweet_id)

    else:
        Tweet.objects.filter(tweet_id=tweet.tweet_id).update(
            liked=0, tweet_likes=tweet.tweet_likes - 1)
        logger.info("Tweet unliked. Tweet ID: %s", tweet.tweet_id)

    return HttpResponseRedirect(reverse('scraper:tweet', args=[tweet.id]))


def index(request):

    if request.method == 'POST':
        form = InputForm(request.POST)

        if form.is_valid():
            username = form.cleaned_data['username']
            no_of_tweets = form.cleaned_data['no_of_tweets']

            try:
                fetch_tweets.delay(username, no_of_tweets)
                logger.info("Tweets fetched")
            except Exception:
                print("Error retrieving Tweets")
                logger.error("Error retrieving Tweets")

        messages.info(
            request,
            'Reload page to view newly retrieved Tweets'
        )
        return HttpResponseRedirect('tweets')

    form = InputForm()

    context = {'form': form}
    return render(request, "scraper/index.html", context)


def tweets_list_view(request):
    tweet_list = Tweet.objects.all().order_by('-id')
    paginator = Paginator(tweet_list, 10)

    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    context = {
        'tweet_list': tweet_list,
        'page_obj': page_obj,
    }

    return render(request, "scraper/tweets_list.html", context)


def tweet_detail_view(request, id):
    tweet = get_object_or_404(Tweet, id=id)

    context = {
        'tweet': tweet,
    }

    return render(request, 'scraper/tweet_detail.html', context)
