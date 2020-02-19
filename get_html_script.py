import requests
import scrape_helpers as sh
from bs4 import BeautifulSoup

def scrape_site(site_name, query_text, location):
    url = sh.generate_request_url(site_name, query_text, location)
    response = requests.get(url)
    parsed_lists = sh.parse_html_to_lists(response.content)
    parsed_data = sh.parse_job_list(parsed_lists, site_name, query_text, location)
    return parsed_data
