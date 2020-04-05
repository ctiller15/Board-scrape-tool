from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
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

email_jobs_to_user(session)