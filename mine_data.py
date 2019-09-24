
import argparse
import logging

import pandas as pd

"""
- issue
    - time it was reported
    - issue title
    - issue text
    - issue status
- reporter
    - Github ID
    - role in the project (one of: NONE, MEMBER, CONTRIBUTOR, COLLABORATOR, OWNER)
    - number of
    - GitHub profile
        - profile email
        - employer
        - personal page
        - location
    - contributions up to the issue reporting date
        - number of private contributions
        - number of public contributions
        - number of contributions made Monday through Friday
        - number of public commits
        - number of reported public issues        
    - contributions in one year before reporting
        same fields as overall contributions 
    - LinkedIn profile
    - email address
- first date project publicly used in any of reporter's commits 
"""


def main(df):

    return df


if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        description="Mine data to reproduce ")
    parser.add_argument('-i', '--input', default="-",
                        type=argparse.FileType('r'),
                        help='Input filename, "-" or skip for stdin')
    parser.add_argument('-o', '--output', default="-",
                        type=argparse.FileType('w'),
                        help='Output filename, "-" or skip for stdout')
    args = parser.parse_args()

    logging.basicConfig(format='%(asctime)s %(message)s',
                        level=logging.INFO if args.verbose else logging.WARNING)

    expected_columns = ('project', 'reporter')