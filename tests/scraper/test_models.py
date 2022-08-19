from django.test import TestCase

from app.src.twitter_scraper.scraper.models import Tweet


class TweetModelTest(TestCase):
    """
    Tests for the Tweet model
    """

    @classmethod
    def setUpTestData(cls):
        cls.tweet = Tweet.objects.create(
            tweet_id=1534851183571083264,
            tweet_text='This is a Test Tweet',
            tweet_rts=5,
            tweet_likes=14,
            tweet_replies=24,
            liked=False
        )

    def test_model_instance(self):
        self.assertIsInstance(self.tweet.tweet_id, int)
        self.assertIsInstance(self.tweet.tweet_text, str)
        self.assertIsInstance(self.tweet.tweet_rts, int)
        self.assertIsInstance(self.tweet.tweet_likes, int)
        self.assertIsInstance(self.tweet.tweet_replies, int)
        self.assertIsInstance(self.tweet.liked, bool)

    def test_string_representation(self):
        tweet = f"{self.tweet.tweet_text}"

        self.assertEqual(str(self.tweet), tweet)
