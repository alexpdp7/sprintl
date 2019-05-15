import argparse
import csv
import getpass
import os

from atlassian import jira


def extract(url, username, password, sprint, output_dir):
    j = jira.Jira(url, username, password)
    issues_jql = j.jql('Sprint = {0}'.format(sprint))
    assert issues_jql
    os.makedirs(output_dir, exist_ok=True)
    with open(os.path.join(output_dir, 'issues.csv'), 'w') as issues_file:
        issues_csv = csv.DictWriter(issues_file, ['id', 'summary', 'type'])
        for issue in issues_jql['issues']:
            issues_csv.writerow({
                'id': issue['key'],
                'summary': issue['fields']['summary'],
                'type': issue['fields']['issuetype']['name'],
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
