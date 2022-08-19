from django.urls import path

from .views import (index, like_unlike_tweet, tweet_detail_view,
                    tweets_list_view)

app_name = 'scraper'
urlpatterns = [
    path('', index, name='index'),
    path('tweets/', tweets_list_view, name='tweets'),
    path('tweet/<int:id>', tweet_detail_view, name='tweet'),
    path('tweet/<int:id>/like/', like_unlike_tweet, name='like'),
    path('tweet/<int:id>/unlike/', like_unlike_tweet, name='unlike'),
]
