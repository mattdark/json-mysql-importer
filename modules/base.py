from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

engine = create_engine("mysql+pymysql://user:password@localhost/movienet?local_infile=1")
Session = sessionmaker(bind=engine)

Base = declarative_base()
