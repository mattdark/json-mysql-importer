from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

engine = create_engine("mysql+pymysql://user:pass@localhost/movienet")
Session = sessionmaker(bind=engine)

Base = declarative_base()
