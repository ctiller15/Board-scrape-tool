from models.database_models import JobDataDbModel
import models.domain_db_mappings as db_map

def mark_job_data_as_sent(session, JobDataList):
    ids = [id for id in [job.id for job in JobDataList]]

    session.query(JobDataDbModel).filter(JobDataDbModel.id.in_(ids)).update({JobDataDbModel.has_been_emailed:True}, synchronize_session='fetch')
    session.commit()

def save_job_data(session, JobDataList):
    converted_list = db_map.map_job_data_models_to_db_models(JobDataList) 
    for job in converted_list:
        session.add(job)

    session.commit()
