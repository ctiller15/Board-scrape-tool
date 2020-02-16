def generate_request_url(site, query, location):
    if 'monster' in site:
        return f'https://www.monster.com/jobs/search/?q={query}&where={location}'
