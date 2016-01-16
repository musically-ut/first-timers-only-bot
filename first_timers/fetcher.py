import requests
import warnings

query = 'https://api.github.com/search/issues?q=label:first-timers-only+is:issue+is:open&sort=created&order=desc'

def get_first_timer_issues():
    res = requests.get(query)
    if res.status_code == 403:
        warnings.warn('Rate limit reached')
        return []
    elif res.ok:
        return res.json()['items']
    else:
        raise RuntimeError('Could not handle response: ' + str(res) + ' from the API.')

