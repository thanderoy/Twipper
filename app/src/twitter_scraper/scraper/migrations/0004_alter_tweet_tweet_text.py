# Generated by Django 4.0.5 on 2022-06-19 12:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('scraper', '0003_alter_tweet_tweet_text'),
    ]

    operations = [
        migrations.AlterField(
            model_name='tweet',
            name='tweet_text',
            field=models.TextField(max_length=280),
        ),
    ]
