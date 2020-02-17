import models
from bs4 import BeautifulSoup

def generate_request_url(site, query, location):
    if 'monster' in site:
        return f'https://www.monster.com/jobs/search/?q={query}&where={location}'

def parse_relevant_job_data(html, site, query, location):
    soup = BeautifulSoup(html, 'html.parser')
    title = soup.find('h2', class_='title').text.strip().lower()
    location = soup.find('div', class_ = 'location').text.strip().lower()
    link = soup.find('a')['href']
    return models.JobDataModel(title, location, link)
