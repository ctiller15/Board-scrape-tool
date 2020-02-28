import format_helpers as fh

def generate_text_email_header(date_obj):
    return f"Jobs for {fh.format_date(date_obj)}"

def generate_text_row_from_job_data(JobDataModel):
    pass

def generate_html_row_from_job_data(JobDataModel):
    return f"""
            <tr>
                <td>
                    <h3 align="center">{JobDataModel.title}</h3>
                    <p align="center">Location:{JobDataModel.location}</p>
                    <p align="center"><span>Posting link:</span> <a href="{JobDataModel.link}">link</a></p>
                </td>
            </tr>
    """

def generate_html_rows_from_job_data_list(JobDataModels):
    return [generate_html_row_from_job_data(model) for model in JobDataModels]

def generate_full_html_email(JobDataModels, date_obj):
    html_email_markup = f"""
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
                                            <h2>{generate_text_email_header(date_obj)}</h2>
                                        </td>
                                    </tr>
                                    <tr>
                                        <td class="body_content" style="padding: 30px">
                                            <table border="1" cellpadding="0" cellspacing="0" width="100%">
                                                {"".join(generate_html_rows_from_job_data_list(JobDataModels))}
                                            </table>
                                        </td>
                                    </tr>

                                    <tr>
                                        <td class="footer_content">
                                            <table border="1" cellpadding="0" cellspacing="0" width="100%">
                                                <tr>
                                                    <td>Powered by job scraper</td>
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

    return html_email_markup
