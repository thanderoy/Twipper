from django import forms


class InputForm(forms.Form):
    username = forms.CharField(
        max_length=15,
        help_text='Enter Twitter username from a public account')
    no_of_tweets = forms.IntegerField(
        min_value=0,
        max_value=900,
        help_text='Enter the number of Tweets to fetch')
