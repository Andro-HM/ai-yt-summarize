from sqlalchemy import Column, String, DateTime, create_engine
from sqlalchemy.ext.declarative import declarative_base
from datetime import datetime

Base = declarative_base()

class Summary(Base):
    __tablename__ = "summaries"

    id = Column(String, primary_key=True)
    video_id = Column(String, nullable=False)
    title = Column(String)
    content = Column(String)
    language = Column(String)
    mode = Column(String)
    source = Column(String)
    created_at = Column(DateTime, default=datetime.utcnow)
