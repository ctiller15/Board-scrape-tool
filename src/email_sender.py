import smtplib, ssl
from config import config as cfg

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
   
    print(smtp_server)

    context = ssl.create_default_context()
    with smtplib.SMTP_SSL(smtp_server, ssl_port, context=context) as server:
        server.login(email_content['From'], cfg.from_email_password)
        server.sendmail(email_content['From'], email_content['To'], email_content.as_string())
