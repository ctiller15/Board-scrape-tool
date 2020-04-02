def mark_job_data_as_sent(session, JobDataList):
    session.query(JobDataDbModel)\
    .filter(JobDataDbModel.Id in [id for id in [job.Id for job in JobDataList]])\
    .update({JobDataDbModel.has_been_emailed:True})\
    .commit()
