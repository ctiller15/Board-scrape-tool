from models.database_models import JobDataDbModel

def mark_job_data_as_sent(session, JobDataList):
    ids = [id for id in [job.id for job in JobDataList]]

    session.query(JobDataDbModel).filter(JobDataDbModel.id.in_(ids)).update({JobDataDbModel.has_been_emailed:True}, synchronize_session='fetch')
    session.commit()
