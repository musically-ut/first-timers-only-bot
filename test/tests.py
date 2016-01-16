from first_timers import fetcher
import json

example_res = json.load(open('data/example.json', 'r'))
example_issues = example_res['items']

def test_fetcher():
    issue_list = fetcher.get_first_timer_issues()
    assert len(issue_list) > 0


