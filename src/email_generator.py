from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from src import format_helpers as fh
from datetime import date

class EmailContent(object):
    def __init__(self, job_data_model_list, date_obj):
        self.job_data_list = job_data_model_list
        self.date = date_obj
        self.header = ''
        self.body = ''
        self.footer = ''

    def generate_row_from_job_data(self):
        pass

    def generate_header(self):
        pass

    def generate_body(self):
        self.body = [self.generate_row_from_job_data(model) for model in self.job_data_list]

    def generate_footer(self):
        self.footer = 'Powered by Job Scraper'

    def to_string(self):
        pass

class TextEmailContent(EmailContent):
    def __init__(self, job_data_model_list, date_obj):
        super().__init__(job_data_model_list, date_obj)
        self.generate_header()
        self.generate_body()
        self.generate_footer()

    def generate_row_from_job_data(self, job_data_model):
        return f"""
                Title: {job_data_model.title}
                Location: {job_data_model.location}
                Link: {job_data_model.link}
        """

    def generate_header(self):
        self.header = f"Jobs for {fh.format_date(self.date)}"

    def to_string(self):
        job_rows_combined = '\n'.join(self.body)

        return f"""
            {self.header}

            {job_rows_combined}

            {self.footer}
            """

class HtmlEmailContent(EmailContent):
    def __init__(self, job_data_model_list, date_obj):
        super().__init__(job_data_model_list, date_obj)
        self.generate_header()
        self.generate_body()
        self.generate_footer()

    def generate_row_from_job_data(self, job_data_model):
        return f"""
                <tr>
                    <td>
                        <h3 align="center">{job_data_model.title}</h3>
                        <p align="center">Location:{job_data_model.location}</p>
                        <p align="center"><span>Posting link:</span> <a href="{job_data_model.link}">link</a></p>
                    </td>
                </tr>
        """

    def generate_header(self):
        self.header = f"Jobs for <span class=\"date\">{fh.format_date(self.date)}</span>"

    def to_string(self):
        return f"""
            <!DOCTYPE html PUBLIC "-//W4C//DTD XHTML 1.0 Transitional//EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-transitional.dtd">
                <html xmlns="http://www.w3.org/1999/xhtml">
                    <head>
                        <meta http-equiv="Content-Type" content="text/html; charset=UTF-8" />
                        <title>Jobs sent for today</title>
                        <meta name="viewport" content="width=device-width, initial-scale=1.0"/>
                    </head>

                    <body style="margin: 0; padding: 0;">
                        <table border="1" cellpadding="0" cellspacing="0" width="100%">
                            <tr>
                                <td>
                                    <table align="center" border="1" cellpadding="0" cellspacing="0" width="600">
                                        <tr>
                                            <td class="header_content" align="center" style="padding: 20px">
                                                <h2>{self.header}</h2>
                                            </td>
                                        </tr>
                                        <tr>
                                            <td class="body_content" style="padding: 30px">
                                                <table border="1" cellpadding="0" cellspacing="0" width="100%">
                                                    {"".join(self.body)}
                                                </table>
                                            </td>
                                        </tr>

                                        <tr>
                                            <td class="footer_content">
                                                <table border="1" cellpadding="0" cellspacing="0" width="100%">
                                                    <tr>
                                                        <td>{self.footer}</td>
                                                    </tr>
                                                </table>
                                            </td>
                                        </tr>

                                    </table>
                                </td>
                            </tr>
                        </table>
                    </body>
                </html>
        """


class FullEmailContent(object):

    def __init__(self, job_data_model_list):
        self.date = date.today()
        self.html = HtmlEmailContent(job_data_model_list, self.date)
        self.text = TextEmailContent(job_data_model_list, self.date)

    def to_email(self):
        message = MIMEMultipart("alternative")
        message["Subject"] = f"New job postings for {fh.format_date(self.date)}"
        message["From"] = config.sender_email
        message["To"] = config.receiver_email
        text_part = MIMEText(self.text, "plain")
        email_part = MIMEText(self.html, "html")
        message.attach(text_part)
        message.attach(email_part)
        return message

def generate_full_email_content(job_data_model_list):
    return FullEmailContent(job_data_model_list)


