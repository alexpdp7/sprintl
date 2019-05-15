import argparse
import csv
import datetime
import getpass
import os

from atlassian import jira

import sprintl


def get_issue(j, key):
    return j.get('rest/api/2/issue/{0}?expand=changelog'.format(key))


def convert_date(date):
    return datetime.datetime.strptime(date, '%Y-%m-%dT%H:%M:%S.%f%z')


def extract(url, username, password, sprint, output_dir):
    j = jira.Jira(url, username, password)
    issues_jql = j.jql('Sprint = {0}'.format(sprint))
    assert issues_jql
    os.makedirs(output_dir, exist_ok=True)
    with open(os.path.join(output_dir, sprintl.ISSUES_FILE), 'w') as issues_file:
        with open(os.path.join(output_dir, sprintl.ISSUE_STATES_FILE), 'w') as issue_states_file:
            issues_csv = csv.DictWriter(issues_file, sprintl.ISSUES_COLUMNS)
            issues_csv.writeheader()
            issue_states_csv = csv.DictWriter(issue_states_file, sprintl.ISSUE_STATES_COLUMNS)
            issue_states_csv.writeheader()
            for issue in issues_jql['issues']:
                key = issue['key']
                issues_csv.writerow({
                    'id': key,
                    'summary': issue['fields']['summary'],
                    'type': issue['fields']['issuetype']['name'],
                })
                issue_full = get_issue(j, key)
                previous_time = convert_date(issue['fields']['created'])
                histories = issue_full['changelog']['histories']
                for history in histories:
                    for item in history['items']:
                        if not item['field'] == 'status':
                            continue
                        previous_state = item['fromString']
                        last_state = item['toString']
                        last_time = convert_date(history['created'])
                        issue_states_csv.writerow({
                            'issue': key,
                            'state': previous_state,
                            'from': previous_time,
                            'to': last_time,
                        })
                        previous_time = last_time
                issue_states_csv.writerow({
                    'issue': key,
                    'state': last_state,
                    'from': last_time,
                    'to': None,
                })


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('url')
    parser.add_argument('username')
    parser.add_argument('sprint')
    parser.add_argument('output_dir')
    args = parser.parse_args()
    extract(args.url,
            args.username,
            getpass.getpass('JIRA password: '),
            args.sprint,
            args.output_dir)
