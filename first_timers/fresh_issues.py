def get_fresh(old_issue_list, new_issue_list):
    old_urls = set(x['url'] for x in old_issue_list)
    return [x for x in new_issue_list if x['url'] not in old_urls]
