import os
from configparser import ConfigParser

path_current_directory = os.path.dirname(__file__)
path_config_file = os.path.join(path_current_directory, 'config.ini')

config = ConfigParser()

config.read(path_config_file)

from_email = config.get('email', 'from_email')

from_email_password = config.get('email', 'from_email_password')

to_email = config.get('email', 'to_email')

query_params = {}

query_params['sitelist'] = config.get('query_params', 'target_sites').split(',')
query_params['query_text'] = config.get('query_params', 'query_text')
query_params['location'] = config.get('query_params', 'location')

print(query_params)
