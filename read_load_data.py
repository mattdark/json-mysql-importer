from modules import countries
from modules import genres
from modules import schema
import pandas as pd
from tqdm import tqdm
import os
import json
from glob import glob

def create_dataframe(filepath):
    json_pattern = os.path.join(filepath, '*.json')
    file_list = glob(json_pattern)

    json_list = []
    for file in tqdm(file_list, desc='Creating DataFrame'):
        with open (file) as f:
            exp = json.load(f)
            json_list.append(exp)

    df = pd.DataFrame(json_list)
    return df

def create_catalog():
    for key, value in countries.Country.items():
        statement = schema.countries.insert().values(country_id=value, name=key)
        schema.engine.execute(statement)

    for key, value in genres.Genre.items():
        statement = schema.genres.insert().values(genre_id=value, name=key)
        schema.engine.execute(statement)

def load_data(df):
    for row in tqdm (df.itertuples(), desc='Loading Data'):
        country = None
        if row.country in countries.Country:
            country = countries.Country[row.country]

        stm = schema.movies.insert().values(movie_id=row.imdb_id, title=row.title, country=country)
        schema.engine.execute(stm)

        if row.genres is not None:
            for val in row.genres:
                if val in genres.Genre:
                    genre = genres.Genre[val]
                    stm = schema.movie_genres.insert().values(movie_id=row.imdb_id, genre_id=genre)
                    schema.engine.execute(stm)

        if row.director != [None]:
            for data in row.director or []:
                stm = schema.director.insert().values(director_id=data['id'], name=data['name']).prefix_with('IGNORE')
                schema.engine.execute(stm)
                stm = schema.movie_director.insert().values(movie_id=row.imdb_id, director_id=data['id'])
                schema.engine.execute(stm)

        if row.cast:
            for data in row.cast:
                stm = schema.cast.insert().values(cast_id=data['id'], name=data['name']).prefix_with('IGNORE')
                schema.engine.execute(stm)
                stm = schema.movie_cast.insert().values(movie_id=row.imdb_id, cast_id=data['id'])
                schema.engine.execute(stm)

        if row.writer:
            for data in row.writer:
                stm = schema.writers.insert().values(writer_id=data['id'], name=data['name']).prefix_with('IGNORE')
                schema.engine.execute(stm)
                stm = schema.movie_writers.insert().values(movie_id=row.imdb_id, writer_id=data['id']).prefix_with('IGNORE')
                schema.engine.execute(stm)

df = create_dataframe('./datasets/')
chunks = np.array_split(df, 100)
schema.meta.create_all(schema.engine)
create_catalog()
load_data(df)