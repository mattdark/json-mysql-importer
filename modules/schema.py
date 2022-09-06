from sqlalchemy import create_engine, MetaData, Table, Column, Integer, String, ForeignKey, ForeignKeyConstraint

engine = create_engine('mysql+pymysql://root:12345@10.194.44.250/movienet', pool_recycle=3600)

meta = MetaData(bind=engine)
MetaData.reflect(meta)

countries = Table(
    'countries', meta,
    Column('country_id', Integer, primary_key=True, nullable=False),
    Column('name', String(45), nullable=False)
)

movies = Table(
    'movies', meta,
    Column('movie_id', String(15), primary_key=True, nullable=False),
    Column('title', String(250), nullable=False),
    Column('country', Integer, ForeignKey("countries.country_id"), nullable=True)
)

genres = Table (
    'genres', meta,
    Column('genre_id', Integer, primary_key=True, nullable=False),
    Column('name', String(45), nullable=False)
)

movie_genres = Table (
    'movie_genres', meta,
    Column('movie_id', String(15), primary_key=True, nullable=False),
    Column('genre_id', Integer, primary_key=True, nullable=False),
    ForeignKeyConstraint(['movie_id'], ['movies.movie_id']),
    ForeignKeyConstraint(['genre_id'], ['genres.genre_id'])
)

director = Table(
    'director', meta,
    Column('director_id', String(15), primary_key=True, nullable=False),
    Column('name', String(45), nullable=False)
)

cast = Table(
    'cast', meta,
    Column('cast_id', String(15), primary_key=True, nullable=False),
    Column('name', String(45), nullable=False)
)

writers = Table(
    'writers', meta,
    Column('writer_id', String(15), primary_key=True, nullable=False),
    Column('name', String(45), nullable=False)
)

movie_director = Table (
    'movie_director', meta,
    Column('movie_id', String(15), primary_key=True, nullable=False),
    Column('director_id', String(15), primary_key=True, nullable=False),
    ForeignKeyConstraint(['movie_id'], ['movies.movie_id']),
    ForeignKeyConstraint(['director_id'], ['director.director_id'])
)

movie_cast = Table (
    'movie_cast', meta,
    Column('movie_id', String(15), primary_key=True, nullable=False),
    Column('cast_id', String(15), primary_key=True, nullable=False),
    ForeignKeyConstraint(['movie_id'], ['movies.movie_id']),
    ForeignKeyConstraint(['cast_id'], ['cast.cast_id'])
)

movie_writers = Table (
    'movie_writers', meta,
    Column('movie_id', String(15), primary_key=True, nullable=False),
    Column('writer_id', String(15), primary_key=True, nullable=False),
    ForeignKeyConstraint(['movie_id'], ['movies.movie_id']),
    ForeignKeyConstraint(['writer_id'], ['writers.writer_id'])
)