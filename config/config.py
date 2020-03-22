import os
from configparser import ConfigParser

path_current_directory = os.path.dirname(__file__)
path_config_file = os.path.join(path_current_directory, 'config.ini')

config = ConfigParser()

config.read(path_config_file)

from_email = config.get('email', 'from_email')

from_email_password = config.get('email', 'from_email_password')

to_email = config.get('email', 'to_email')
