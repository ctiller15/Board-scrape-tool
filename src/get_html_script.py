import requests
from src import scrape_helpers as sh
from models import database_methods as db_ops

def scrape_site(site_name, query_text, location):
    url = sh.generate_request_url(site_name, query_text, location)
    response = requests.get(url)
    return response

def parse_data(response_object):
    parsed_lists = sh.parse_html_to_lists(response_object.content)
    parsed_data = sh.parse_job_list(parsed_lists)
    return parsed_data

def scrape_full_page(site_name, query_text, location):
    scraped_data = scrape_site(site_name, query_text, location)
    parsed_data = parse_data(scraped_data)
    return parsed_data

def scrape_sites_and_save_jobs(site_list, query_text, location, session):
    # Currently there is no problem since this project only supports one
    # site. Upon extending though this operation
    # should be asynchronous.
    for site in site_list:
        parsed_page = scrape_full_page(site, query_text, location)
        db_ops.save_job_data(session, parsed_page)

