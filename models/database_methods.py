from models.database_models import JobDataDbModel

def mark_job_data_as_sent(session, JobDataList):
    ids = [id for id in [job.id for job in JobDataList]]
    print(ids)
    for job_listing in session.query(JobDataDbModel).filter(JobDataDbModel.id in ids):
        job_listing.has_been_emailed = True
            
        print(job_listing)

    session.query(JobDataDbModel).filter(JobDataDbModel.id.in_(ids)).update({JobDataDbModel.has_been_emailed:True}, synchronize_session='fetch')

    print(session.query(JobDataDbModel).filter(JobDataDbModel.has_been_emailed == False).all())

    session.commit()
