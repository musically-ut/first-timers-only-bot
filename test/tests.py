from first_timers import fetcher
import json
from first_timers import fresh_issues

example_res = json.load(open('data/example.json', 'r'))
example_issues = example_res['items']

def test_fetcher():
    issue_list = fetcher.get_first_timer_issues()
    assert len(issue_list) > 0
test_fetcher.__setattr__('__test__', False) # Test disabled by default.

def test_get_fresh():
    new_issues = fresh_issues.get_fresh(example_issues[:-1], example_issues)
    assert new_issues[0] == example_issues[-1]
