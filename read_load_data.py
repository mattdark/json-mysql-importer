from modules.countries import Country_Dict
from modules.genres import Genre_Dict

from modules.schema import Country, Genre, Movie, Director, Actor, Writer
from modules.base import Session, engine, Base

import pandas as pd
from tqdm import tqdm
import os
import json
from glob import glob

# 2 - generate database schema
Base.metadata.create_all(engine)

# 3 - create a new session
session = Session()

def create_dataframe(filepath):
    json_pattern = os.path.join(filepath, '*.json')
    file_list = glob(json_pattern)

    json_list = []
    #for file in tqdm(file_list, desc='Creating DataFrame'):
    for i in tqdm(range(499), desc='Creating DataFrame'):
        #with open (file) as f:
        with open(file_list[i]) as f:
            exp = json.load(f)
            json_list.append(exp)

    df = pd.DataFrame(json_list)
    return df

def create_catalog():
    for key, value in Country_Dict.items():
        country = Country(value, key)
        session.add(country)

    for key, value in Genre_Dict.items():
        genre = Genre(value, key)
        session.add(genre)
    
    session.commit()

def load_data(df):
    for row in tqdm (df.itertuples(), desc='Loading Data'):
        country = None
        if row.country in Country_Dict:
            country = Country_Dict[row.country]
        movie = Movie(row.imdb_id, row.title, country)

        if row.genres is not None:
            for val in row.genres:
                if val in Genre_Dict:
                    genre = Genre(Genre_Dict[val], val)
                    movie.genres.append(genre)

        if row.director != [None] and row.director != None:
            done = set()
            w = []
            for d in row.director:
                if d['id'] not in done:
                    done.add(d['id'])
                    w.append(d)
            for data in w or []:
                director = Director(data['id'], data['name'])
                session.merge(director)
                session.flush()
                movie.directors.append(director)

        if row.cast:
            for data in row.cast:
                actor = Actor(data['id'], data['name'])
                session.merge(actor)
                session.flush()
                movie.actors.append(actor)

        if row.writer:
            done = set()
            w = []
            for d in row.writer:
                if d['id'] not in done:
                    done.add(d['id'])
                    w.append(d)
            for data in w:
                writer = Writer(data['id'], data['name'])
                session.merge(writer)
                session.flush()
                movie.writers.append(writer)
        
        session.merge(movie)
        session.flush()
    session.commit()

df = create_dataframe('./datasets/')
create_catalog()
load_data(df)
session.close()
