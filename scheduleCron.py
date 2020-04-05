from crontab import CronTab
from datetime import date


my_cron = CronTab(user=True)
cron_command = 'python -m cron_jobs.scrape_sites'
cron_comment = 'job to run the job scraper daily'

if cron_comment not in [job.comment for job in my_cron]:
    job = my_cron.new(command=cron_command, comment=cron_comment)
    job.hour.on(20)
    job.minute.on(30)
    job.enable()

my_cron.write()

def generate_new_job(command=cron_command, comment=cron_comment, time=date.today()):
    pass

if __name__ == '__main__':
    generate_new_job()

