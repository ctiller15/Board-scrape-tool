from models import database_models as dm

def map_job_data_model_to_db(job_data_model):
    new_model = dm.JobDataDbModel()
    new_model.link = job_data_model.link
    new_model.location = job_data_model.location
    new_model.title = job_data_model.title
    new_model.has_been_emailed = False

    return new_model

def map_job_data_models_to_db_models(job_data_models):
    return [map_job_data_model_to_db(model) for model in job_data_models]
