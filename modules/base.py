from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

engine = create_engine("mysql+pymysql://user:password@127.0.0.1:16033/movienet", pool_size=10, max_overflow=20, pool_recycle=3600, pool_pre_ping=True, echo=False)
Session = sessionmaker(bind=engine)

Base = declarative_base()
