import csv
import datetime
import os


ISSUES_FILE = 'issues.csv'
ISSUES_COLUMNS = ['id', 'summary', 'type']
ISSUE_STATES_FILE =  'issue_states.csv'
ISSUE_STATES_COLUMNS = ['issue', 'state', 'from', 'to']


def load(input_dir):
    issues = {}
    with open(os.path.join(input_dir, ISSUES_FILE)) as issues_file:
        issues_csv = csv.DictReader(issues_file)
        for issue in issues_csv:
            issues[issue['id']] = issue

    with open(os.path.join(input_dir, ISSUE_STATES_FILE)) as issue_states_file:
        issue_states_csv = csv.DictReader(issue_states_file)
        for issue_state in issue_states_csv:
            issue_state['from'] = datetime.datetime.fromisoformat(issue_state['from'])
            if issue_state['to']:
                issue_state['to'] = datetime.datetime.fromisoformat(issue_state['to'])
            issue = issues[issue_state['issue']]
            issue['states'] = issue.get('states', [])
            issue['states'].append(issue_state)

    return issues
