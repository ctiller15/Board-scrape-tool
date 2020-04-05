from config.config import query_params as qp
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from src.get_html_script import scrape_sites_and_save_jobs
from models.database_models import JobDataDbModel

Base = declarative_base()

print("Check me out!")

# Initialize sql db.
engine = create_engine('sqlite:///job_records.db')
Session = sessionmaker(bind=engine)
session = Session()
Base.metadata.create_all(engine, tables=[JobDataDbModel.__table__])

# Run scrape/save script.
scrape_sites_and_save_jobs(qp['sitelist'], qp['query_text'], qp['location'], session)
