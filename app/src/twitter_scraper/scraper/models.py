import pytest
from django.db import models


class Tweet(models.Model):
    """
    This is the Tweet model. It stores data related to the Tweet object

    Fields:
        tweet_id: Unique ID for each Tweet
        tweet_text: Actual Tweet text
        tweet_rts: Number of Retweets on the Tweet
        tweet_likes: Number of Likes on the Tweet
        tweet_replies: Number of Replies on the Tweet
    """
    tweet_id = models.CharField(max_length=50)
    tweet_text = models.TextField(max_length=280)
    tweet_rts = models.PositiveIntegerField()
    tweet_likes = models.PositiveIntegerField()
    tweet_replies = models.PositiveIntegerField()
    tweet_author = models.CharField(max_length=50)
    liked = models.BooleanField(default=False)

    def __str__(self):
        return self.tweet_text
