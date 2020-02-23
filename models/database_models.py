from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, Boolean

Base = declarative_base()

class JobDataDbModel(Base):
    __tablename__ = 'job_postings'

    id = Column(Integer, primary_key=True)
    title = Column(String)
    location = Column(String)
    link = Column(String)
    has_been_emailed = Column(Boolean)
