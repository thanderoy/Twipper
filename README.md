# Twitter Scraper

Twitter scraper utilizing the Tweepy Library and Twitter API v2 to scrap Tweets from a specified user account on Twitter

## Description

Firing up the server will bring your to a page from which the user will be required to provide a username to a public account from where Tweets will be scraped and the number of Tweets to receive

celery -A app.src.twitter_scraper.config worker -l info
