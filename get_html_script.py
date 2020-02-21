import requests
import scrape_helpers as sh

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

