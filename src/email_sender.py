import smtplib, ssl

def send_email_to_user(generated_email_class):
    context = ssl.create_default_context()
    with smtplib.SMTP_SSL(smpt_server, port, context=context) as server:
        server.login(sender_email, password)
        server.sendmail(sender_email, receiver_email, message)
