# -*- coding: utf-8 -*-
from __future__ import print_function
import click
import os
import sys
import json
import first_timers as FT

def updateDB(all_issues, db_path):
    """Truncate and write the new list of issues in the DB."""
    with open(db_path, 'w') as dbFile:
        json.dump(FT.limit_issues(all_issues), dbFile)

@click.command()
@click.option('--only-save',
        is_flag=True,
        help='Do not post any tweets, just populate the DB.')
@click.option('--db-path',
        prompt='Database file',
        default='data/db.json',
        help='Old issues in a JSON list.')
@click.option('--create',
        is_flag=True,
        help='Pass if the DB file should be created.')
@click.option('--creds-path',
        prompt='Credentials file',
        default='',
        help='File which contains Twitter account credentials.'
             'Not needed if only saving to DB.')
@click.option('--debug',
        is_flag=True,
        help='Run in debug mode (does not tweet).')
def run(only_save, db_path, create, creds_path, debug):
    dbExists = os.path.exists(db_path)
    if not dbExists and not create:
        click.echo('DB file does not exist and argument'
                   '--create was not passed.', err=True)
        sys.exit(-1)
    elif dbExists and not create:
        with open(db_path, 'rb') as dbFile:
            old_issues = json.load(dbFile)
    elif not dbExists and create:
        old_issues = []
    else:
        click.echo('DB file exists but --create was passed.', err=True)
        sys.exit(-1)

    # Getting the latest list of issues from Github
    new_issues = FT.get_first_timer_issues()
    fresh_issues = FT.get_fresh(old_issues, new_issues)
    all_issues = fresh_issues + old_issues

    if not only_save:
        if not os.path.exists(creds_path):
            print('Credentials file does not exist.', file=sys.stdout)
            sys.exit(-1)

        with open(creds_path, 'r') as credsFile:
            creds = json.load(credsFile)

        click.echo('Tweeting {} tweets.'.format(len(fresh_issues)))
        tweets = FT.tweet_issues(fresh_issues, creds, debug)

        for tweet in tweets:
            click.echo('\t' + tweet)

    updateDB(all_issues, db_path)

    if len(fresh_issues) > 0:
        click.echo('Database updated.')


if __name__ == '__main__':
    run()

