from sqlalchemy import Column, String, Integer, Table, ForeignKey, ForeignKeyConstraint
from sqlalchemy.orm import relationship

from .base import Base

class Country(Base):
    __tablename__ = 'countries'

    country_id = Column(Integer, primary_key=True, nullable=False)
    name = Column(String(45), nullable=False)

    def __init__(self, country_id, name):
        self.country_id = country_id
        self.name = name

class Genre(Base):
    __tablename__ = 'genres'
    
    genre_id = Column(Integer, primary_key=True, nullable=False)
    name = Column(String(45), nullable=False)

    def __init__(self, genre_id, name):
        self.genre_id = genre_id
        self.name = name

movies_genres = Table (
    'movies_genres', Base.metadata,
    Column('movie_id', String(15), primary_key=True, nullable=False),
    Column('genre_id', Integer, primary_key=True, nullable=False),
    ForeignKeyConstraint(['movie_id'], ['movies.movie_id']),
    ForeignKeyConstraint(['genre_id'], ['genres.genre_id'])
)

movies_actors = Table(
    'movies_actors', Base.metadata,
    Column('movie_id', String(15), primary_key=True, nullable=False),
    Column('actor_id', String(15), primary_key=True, nullable=False),
    ForeignKeyConstraint(['movie_id'], ['movies.movie_id']),
    ForeignKeyConstraint(['actor_id'], ['actors.actor_id'])
)

movies_directors = Table (
    'movies_directors', Base.metadata,
    Column('movie_id', String(15), primary_key=True, nullable=False),
    Column('director_id', String(15), primary_key=True, nullable=False),
    ForeignKeyConstraint(['movie_id'], ['movies.movie_id']),
    ForeignKeyConstraint(['director_id'], ['directors.director_id'])
)

movies_writers = Table (
    'movies_writers', Base.metadata,
    Column('movie_id', String(15), primary_key=True, nullable=False),
    Column('writer_id', String(15), primary_key=True, nullable=False),
    ForeignKeyConstraint(['movie_id'], ['movies.movie_id']),
    ForeignKeyConstraint(['writer_id'], ['writers.writer_id'])
)

class Movie(Base):
    __tablename__ = 'movies'
    
    movie_id = Column(String(15), primary_key=True, nullable=False)
    title = Column(String(250), nullable=False)
    country = Column(Integer, ForeignKey('countries.country_id'), nullable=True)
    genres = relationship("Genre", secondary=movies_genres)
    directors = relationship("Director", secondary=movies_directors)
    actors = relationship("Actor", secondary=movies_actors)
    writers = relationship("Writer", secondary=movies_writers)

    def __init__(self, movie_id, title, country):
        self.movie_id = movie_id
        self.title = title
        self.country = country

class Director(Base):
    __tablename__ = 'directors'
    
    director_id = Column(String(15), primary_key=True, nullable=False)
    name = Column(String(45), nullable=False)
    
    def __init__(self, director_id, name):
        self.director_id = director_id
        self.name = name

class Actor(Base):
    __tablename__ = 'actors'
    
    actor_id = Column(String(15), primary_key=True, nullable=False)
    name = Column(String(100), nullable=False)
    
    def __init__(self, actor_id, name):
        self.actor_id = actor_id
        self.name = name

class Writer(Base):
    __tablename__ = 'writers'
    
    writer_id = Column(String(15), primary_key=True, nullable=False)
    name = Column(String(45), nullable=False)
    
    def __init__(self, writer_id, name):
        self.writer_id = writer_id
        self.name = name
