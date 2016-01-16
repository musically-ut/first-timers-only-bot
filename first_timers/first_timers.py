# -*- coding: utf-8 -*-
from __future__ import print_function
import tweepy
import requests
import warnings

ellipse = u'…'
query = 'https://api.github.com/search/issues?q=label:first-timers-only+is:issue+is:open&sort=updated&order=desc'

def get_first_timer_issues():
    res = requests.get(query)
    if res.status_code == 403:
        warnings.warn('Rate limit reached')
        return []
    elif res.ok:
        return res.json()['items']
    else:
        raise RuntimeError('Could not handle response: ' + str(res) + ' from the API.')


def get_fresh(old_issue_list, new_issue_list):
    old_urls = set(x['url'] for x in old_issue_list)
    return [x for x in new_issue_list if x['url'] not in old_urls]


def tweet_issues(issues, creds, debug=False):
    if len(issues) == 0:
        return

    auth = tweepy.OAuthHandler(creds['Consumer Key'], creds['Consumer Secret'])
    auth.set_access_token(creds['Access Token'], creds['Access Token Secret'])
    api = tweepy.API(auth)

    # This results in an API call to /help/configuration
    conf = api.configuration()

    url_len = conf['short_url_length_https']
    hashTags = u'#github'
    # 1 space with URL and 1 space before hashtags.
    allowed_title_len = 140 - (url_len + 1) - (len(hashTags) + 1)

    tweets = [] if debug else None

    for issue in issues:
        title = issue['title']
        if len(title) > allowed_title_len:
            title = title[:allowed_title_len - 1] + ellipse

        url = issue['url']

        tweet = '{title} {url} {tags}'.format(title=title, url=url, tags=hashTags)

        if debug:
            tweets.append(tweet)
        else:
            api.update_status(tweet)

    return tweets
