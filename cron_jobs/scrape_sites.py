from config.config import query_params as qp
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from src.get_html_script import scrape_sites_and_save_jobs
from models.database_models import JobDataDbModel
import os

Base = declarative_base()

cur_dir = os.getcwd()

# Initialize sql db.
# It will save to the same directory as the project until I can
# find a better spot to put it.
engine = create_engine(f'sqlite:///{cur_dir}/job_records.db')
Session = sessionmaker(bind=engine)
session = Session()
Base.metadata.create_all(engine, tables=[JobDataDbModel.__table__])

# Run scrape/save jobs to db.
scrape_sites_and_save_jobs(qp['sitelist'], qp['query_text'], qp['location'], session)
