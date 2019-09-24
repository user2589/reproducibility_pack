
Prerequisites
-------------
Install required Python packages:
```
pip install -r requirements.txt
```

Configure strudel.scraper with Github tokens as described in 
[package documentation](https://github.com/cmustrudel/strudel.scraper):

`export GITHUB_API_TOKENS='comma-separated list of tokens'`


Sample projects
---------------
Create a list of projects to sample issues from.
Each line should contain github slug of the project, e.g.:
```
project,namespace
numpy/numpy,numpy
PyMySQL/mysqlclient-python,MySQLdb
benjaminp/six,six
...
```
The rest of this file assumes the file name is `projects.csv`.
Project column is expected to contain GitHub slug of the project, 
i.e. a string of the form '<user_name>/<repo_name>'.
Namespace should contain the name under which the project is imported in Python code.
In most cases, it is identical to the project name but there are few exceptions.
This field will be used to mine project usage. 


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



Automatic data collection
--------------------
`mine_data.py -i issues.csv -o scraped_data.csv`

The resulting file `scraped_data.csv` will contain columns:

- project
- issue
    - time it was reported
    - issue title
    - issue text
    - issue status
- reporter
    - Github ID
    - role in the project (one of: NONE, MEMBER, CONTRIBUTOR, COLLABORATOR, OWNER)
    - days since the first issue by the same reporter in this project
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
- public usage
    - first date project publicly used in any of reporter's commits 
    - last date project publicly used in any of reporter's commits 
    
At this step, you can remove issues not falling into the desired date range.
 
Manual data collection
----------------------
Although we tried to do our best at the previous step, the automatically
mined data from the previous step might be incomplete or inaccurate.
Fill in the gaps and by researching reporters' profiles.

Fill in the following columns:

- Reporter's job profile is aligned with the project scope
- Reporter's activity in the last year is mostly academia-related
    
(optional) Anonymize data
-------------------------
 `anonymize.py -i scraped_data.csv -o scraped_data.csv`


Evaluate signals
--------------
Use jupyter notebooks (requires R)
