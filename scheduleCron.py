from crontab import CronTab
from datetime import time
import os

current_path = os.getcwd()
cron_command = f'cd {current_path} && /usr/bin/python3.6 -m cron_jobs.scrape_sites'
cron_comment = 'job to run the job scraper daily'

email_command = f'cd {current_path} && /usr/bin/python3.6 -m cron_jobs.email_results'
email_comment = 'job to email the stored results daily.'

def generate_new_job(generator_command=cron_command, generator_comment=cron_comment, schedule_time=time(0, 0, 0)):
    my_cron = CronTab(user=True)

    if generator_comment not in [job.comment for job in my_cron]:
        job = my_cron.new(command=generator_command, comment=generator_comment)
        job.setall(schedule_time)
        job.enable()

    my_cron.write()

if __name__ == '__main__':
    generate_new_job(cron_command, cron_comment, time(0, 0, 0))
    generate_new_job(email_command, email_comment, time(12, 0, 0))
