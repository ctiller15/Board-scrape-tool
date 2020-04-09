## Job board scrape tool

A tool made to aggregate the searches of multiple job boards. Written in python.

All packages can be installed via:
`pip3 install -r requirements.txt`


### Required python
Only works with `python3.6`
You can check your current python with `python --version` or `python3 --version`

### Required Packages
- Requests
- BeautifulSoup4
- sqlalchemy
- python-crontab

`pip3 install beautifulsoup4 sqlalchemy requests python-crontab`

## Running the tests
From the top level directory:

`python -m unittest tests/tests.py` for the unit tests

`python -m unittest tests/functional_tests.py` for the end-to-end/functional tests

`python -m unittest discover -s tests -p '*tests.py'` for all tests.

## Behavior
Every day at a given time, the app will scrape a single page of all of the supported sites.
At another time, the app will email all of the results from a specified email of your choice to another given email of your choice.

### How to use
After the tests all run successfully, run the following from the project directory:

`python -m scheduleCron`

And your jobs will be generated.

### Troubleshooting
Given that right now it uses cron and not anacron, the machine this is on has to _always be running_. 
There are plans to set up anacron in the future.
