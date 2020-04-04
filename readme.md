## Job board scrape tool

A tool made to aggregate the searches of multiple job boards. Written in python.

### Required Packages
- Requests
- BeautifulSoup4
- sqlalchemy

`pip3 install beautifulsoup4 sqlalchemy requests`


## Running the tests
From the top level directory:

`python -m unittest tests/tests.py` for the unit tests

`python -m unittest tests/functional_tests.py` for the end-to-end/functional tests

`python -m unittest discover -s tests -p '*tests.py'` for all tests.
