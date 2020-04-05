import smtplib, ssl
from config import config as cfg
from models.database_models import JobDataDbModel

from src.email_generator import generate_full_email_content
from models.database_methods import mark_job_data_as_sent

ssl_port = 465

smtp_email_map = {
        'gmail.com': 'smtp.gmail.com',
        'hotmail.com': 'smtp.live.com',
        'msn.com': 'smtp.live.com',
        'live.com': 'smtp.live.com',
        'passport.com': 'smtp.live.com',
        'passport.net': 'smtp.live.com'}

def get_smtp_server(email):
    email_suffix = email.split('@')[-1]
    return smtp_email_map[email_suffix]

def send_email_to_user(generated_email_class):
    email_content = generated_email_class.to_email()
    smtp_server = get_smtp_server(email_content['From'])
   
    context = ssl.create_default_context()
    with smtplib.SMTP_SSL(smtp_server, ssl_port, context=context) as server:
        try:
            server.login(email_content['From'], cfg.from_email_password)
            response = server.sendmail(email_content['From'], email_content['To'], email_content.as_string())
        except smtplib.SMTPResponseException as error:
            print(f'An error occurred: {error}')

    return response

def get_data_and_send_email(db_session):
    data = db_session.query(JobDataDbModel).filter(JobDataDbModel.has_been_emailed==False).all()
    email_content = generate_full_email_content(data)
    response = send_email_to_user(email_content)
    mark_job_data_as_sent(db_session, data)

    return response
