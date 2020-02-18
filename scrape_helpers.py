import models
from bs4 import BeautifulSoup

def generate_request_url(site, query, location):
    if 'monster' in site:
        return f'https://www.monster.com/jobs/search/?q={query}&where={location}'

def parse_relevant_job_data(html, site, query, location):
    print(html)
    print(html[0:50])
    soup = BeautifulSoup(html, 'html.parser')
    #print(soup.find('h2', class_='title'))
    title = soup.find('h2', class_='title').text.strip().lower()
    location = soup.find('div', class_ = 'location').text.strip().lower()
    link = soup.find('a')['href']
    return models.JobDataModel(title, location, link)

def parse_job_list(html_list, site, query, location):
    print(html_list)
    job_data_list = [parse_relevant_job_data(html, site, query, location) for html in html_list]
    return job_data_list
