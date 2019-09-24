#!/usr/bin/env python
"""
Get list of issues
------------------
`get_issues.py -i projects.csv -o issues.csv -n 20`

The resulting file `issues.csv` will contain columns:

- project (str): github repository slug of the project
- namespace (str): name of the project module when imported
- reporter
    - reporter (str): Github ID
    - tenure (int): days since the first issue by the same reporter
    - role (str): reporter's role in the project
        (one of: 'NONE', 'MEMBER', 'CONTRIBUTOR', 'COLLABORATOR', 'OWNER')
- issue
    - issue_no (int): number of the issue in the project
    - title (str): issue title
    - created_at (str): time it was reported, YYY-MM-DDTHH:MM:SS
    - body (str): issue text
    - state (str): issue status, 'open' or 'closed'
"""

from __future__ import print_function

import argparse
import logging

import stscraper as scraper
import pandas as pd

api = scraper.GitHubAPI()


def json_imap(mapping, iterable):
    """Extract json mappings from an iterable.

    Typically it is applied to an iterator returned by an API

    Args:
        mapping (dict): mapping, same as used by `json_map`
        iterable (Iterable): any kind of a directly iterable object.
    Returns:
        Generator: a generator of mapped items
    """
    for item in iterable:
        yield scraper.json_map(mapping, item)


def get_project_issues(repo_slug, max_issues_per_project=None, max_date=None):
    # type: (str, int, str) -> pd.DataFrame
    """Get issues for a single project"""
    logging.info("Processing %s", repo_slug)
    all_issues = pd.DataFrame(
            json_imap({
                'reporter': 'user__login',
                'role': 'author_association',
                'number': 'number',
                'title': 'title',
                'created_at': 'created_at',
                'body': 'body',
                'state': 'state',
            },
            api.repo_issues(repo_slug)),
        ).sort_values('created_at')
    if max_date:
        all_issues = all_issues[all_issues['created_at'] < max_date]
    last_reported = all_issues.groupby(
        'reporter').last().iloc[:max_issues_per_project]
    first_reported = all_issues.groupby('reporter').first()['created_at']
    # int(timedelta) is ns, times 86400 seconds in a day
    last_reported['tenure'] = (
        pd.to_datetime(last_reported['created_at'])
        - pd.to_datetime(last_reported.index.map(first_reported))
    ).astype(int) // 86400000000000
    last_reported['project'] = repo_slug
    return last_reported.reset_index().sort_values('number')


def main(projects_df, max_issues_per_project=None, max_date=None):
    # type: (pd.DataFrame, int, str) -> pd.DataFrame
    df = pd.concat(
        (get_project_issues(row['project'], max_issues_per_project)
         for _, row in projects_df.iterrows())
    )
    df['namespace'] = df['project'].map(
        projects_df.set_index('project')['namespace'])
    return df.set_index(['project', 'namespace'])


if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        description="Mine data to reproduce ")
    parser.add_argument("-i", "--input", default="-",
                        type=argparse.FileType('r'),
                        help="Input filename, '-' or skip for stdin")
    parser.add_argument("-o", "--output", default="-",
                        type=argparse.FileType('w'),
                        help="Output filename, '-' or skip for stdout")
    parser.add_argument("-n", "--max-issues", default=None,
                        type=int, help="Max number of issues per project,"
                                       "not limited by default")
    parser.add_argument("--max-date", default=None,
                        type=str, help="Max date the issue was reported")
    parser.add_argument("-v", "--verbose", action="store_true",
                        help="Log progress to stderr")
    args = parser.parse_args()
    if args.max_issues is not None and args.max_issues < 1:
        parser.exit(1, "max number of issues must be non-negative\n")

    expected_columns = {"project", "namespace"}
    input_df = pd.read_csv(args.input)
    missing_columns = expected_columns - set(input_df.columns)
    if missing_columns:
        parser.exit(1, "The input file doesn't contain required columns:\n"
                       "%s" % ','.join(missing_columns))

    logging.basicConfig(format="%(asctime)s %(message)s",
                        level=logging.INFO if args.verbose else logging.WARNING)

    output_df = main(input_df, args.max_issues, args.max_date)
    output_df.to_csv(args.output, encoding='utf8')
