import requests
import scrape_helpers as sh
from bs4 import BeautifulSoup

def scrape_site(site_name, query_text, location):
    url = sh.generate_request_url(site_name, query_text, location)
    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')
    print(soup)
    resp1 = soup.find(id='ResultsContainer')
    print(resp1)
    print(resp1.findall('section', class_='card-content'))
    return response
