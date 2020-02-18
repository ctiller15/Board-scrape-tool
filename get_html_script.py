import requests
import scrape_helpers as sh
from bs4 import BeautifulSoup

def scrape_site(site_name, query_text, location):
    url = sh.generate_request_url(site_name, query_text, location)
    response = requests.get(url)
    first_soup = BeautifulSoup(response.content, 'html.parser')
    parsed_data = sh.parse_job_list(str(first_soup.find('body')), site_name, query_text, location)
    return parsed_data
    #soup = BeautifulSoup(response.content, 'html.parser')
    #resp1 = soup.find(id='ResultsContainer')
    #return response
