import models
from bs4 import BeautifulSoup

def generate_request_url(site, query, location):
    if 'monster' in site:
        return f'https://www.monster.com/jobs/search/?q={query}&where={location}'

def parse_relevant_job_data(html, site, query, location):
    soup = BeautifulSoup(html, 'html.parser')

    title_element = soup.find('h2', class_='title')
    location_element = soup.find('div', class_='location')
    link_element = soup.find('a')

    if(None not in (title_element, location_element, link_element)):
        title = soup.find('h2', class_='title').text.strip().lower()
        location = soup.find('div', class_='location').text.strip().lower()
        link = soup.find('a')['href']
        return models.JobDataModel(title, location, link)

def parse_job_list(html_list, site, query, location):
    job_data_list = [parse_relevant_job_data(str(html), site, query, location) for html in html_list]
    return [job_data for job_data in job_data_list if job_data is not None]

def parse_html_to_lists(html):
    soup = BeautifulSoup(html, 'html.parser')
    return soup.find(id='ResultsContainer').findAll('section', class_='card-content')
