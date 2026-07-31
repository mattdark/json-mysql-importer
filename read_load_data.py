from modules.countries import Country_Dict
from modules.genres import Genre_Dict
from modules.schema import (
    Country, Genre, Movie, Director, Actor, Writer,
    movies_genres, movies_actors, movies_directors, movies_writers,
)
from modules.base import engine, Base
from sqlalchemy.dialects.mysql import insert as mysql_insert
from sqlalchemy import text

import pandas as pd
from tqdm import tqdm

with engine.connect() as c:
    c.execute(text("CREATE DATABASE IF NOT EXISTS movienet CHARACTER SET utf8 COLLATE utf8_general_ci"))

Base.metadata.create_all(engine)

conn = engine.connect()


def raw_insert_ignore(table_or_class, rows: list[dict]) -> None:
    if rows:
        conn.execute(mysql_insert(table_or_class).prefix_with("IGNORE"), rows)

def set_session_optimizations() -> None:
    conn.execute(text("SET SESSION foreign_key_checks = 0"))
    conn.execute(text("SET SESSION unique_checks = 0"))
    conn.execute(text("SET SESSION autocommit = 0"))
    conn.execute(text("SET SESSION bulk_insert_buffer_size = 268435456"))

def reset_session_optimizations() -> None:
    conn.execute(text("SET SESSION foreign_key_checks = 1"))
    conn.execute(text("SET SESSION unique_checks = 1"))
    conn.execute(text("SET SESSION autocommit = 1"))


def create_dataframe(filepath: str = "./data/dataset.parquet") -> pd.DataFrame:
    df = pd.read_parquet(filepath)
    for col in ("genres", "director", "cast", "writer"):
        if col in df.columns:
            df[col] = df[col].apply(
                lambda x: None if (x is None or (isinstance(x, float) and pd.isna(x)))
                          else list(x) if not isinstance(x, list) else x
            )
    return df


def create_catalog() -> None:
    raw_insert_ignore(Country, [{"country_id": v, "name": k} for k, v in Country_Dict.items()])
    raw_insert_ignore(Genre,   [{"genre_id": v,   "name": k} for k, v in Genre_Dict.items()])
    conn.commit()


def extract_all(df: pd.DataFrame) -> dict[str, list[dict]]:
    print("Extracting movies...")
    movies = df[["imdb_id", "title", "country"]].drop_duplicates(subset=["imdb_id"]).copy()
    movies["title"] = movies["title"].str.slice(0, 250)
    movies["country"] = movies["country"].map(Country_Dict)
    movies["country"] = (
        movies["country"]
        .astype("Int64")
        .astype(object)
        .where(movies["country"].notna(), other=None)
    )
    movies_rows = movies.rename(columns={"imdb_id": "movie_id"}).to_dict("records")

    print("Extracting genres...")
    genres_df = df[["imdb_id", "genres"]].dropna(subset=["genres"])
    genres_df = genres_df.explode("genres").dropna(subset=["genres"])
    genres_df["genre_id"] = genres_df["genres"].map(Genre_Dict)
    genres_df = genres_df.dropna(subset=["genre_id"])
    genres_df["genre_id"] = genres_df["genre_id"].astype(int)
    mg_rows = (genres_df.rename(columns={"imdb_id": "movie_id"})[["movie_id", "genre_id"]]
               .drop_duplicates().to_dict("records"))

    print("Extracting directors...")
    directors_rows, md_rows = _extract_people(df, "director", "director_id")

    print("Extracting actors...")
    actors_rows, ma_rows = _extract_people(df, "cast", "actor_id")

    print("Extracting writers...")
    writers_rows, mw_rows = _extract_people(df, "writer", "writer_id")

    return {
        "movies":           movies_rows,
        "movies_genres":    mg_rows,
        "directors":        directors_rows,
        "movies_directors": md_rows,
        "actors":           actors_rows,
        "movies_actors":    ma_rows,
        "writers":          writers_rows,
        "movies_writers":   mw_rows,
    }


def _extract_people(
    df: pd.DataFrame,
    col: str,
    id_col: str,
) -> tuple[list[dict], list[dict]]:
    sub = df[["imdb_id", col]].dropna(subset=[col])
    sub = sub[sub[col].map(lambda x: len(x) > 0)]
    sub = sub.explode(col).dropna(subset=[col])
    sub = sub[sub[col].map(lambda x: x is not None)]
    sub = sub.copy()
    sub[id_col]  = sub[col].map(lambda x: x.get("id"))
    sub["name"]  = sub[col].map(lambda x: x.get("name"))
    sub = sub.dropna(subset=[id_col])

    rel_rows = (sub[["imdb_id", id_col]]
                .rename(columns={"imdb_id": "movie_id"})
                .drop_duplicates()
                .to_dict("records"))

    max_len = 100 if id_col == "actor_id" else 45
    people_df = sub[[id_col, "name"]].drop_duplicates(subset=[id_col]).copy()
    people_df["name"] = people_df["name"].str.slice(0, max_len)
    people_rows = people_df.to_dict("records")

    return people_rows, rel_rows


def bulk_load(rows: list[dict], table_or_class, label: str, batch_size: int = 50000) -> None:
    for start in tqdm(range(0, len(rows), batch_size), desc=label):
        raw_insert_ignore(table_or_class, rows[start : start + batch_size])
    conn.commit()


def bulk_load_infile(rows: list[dict], table_name: str, columns: list[str], label: str) -> None:
    import tempfile, csv, os

    print(f"{label} ({len(rows):,} filas)...")
    with tempfile.NamedTemporaryFile(mode="w", suffix=".csv", delete=False, newline="") as f:
        tmp_path = f.name
        csv.DictWriter(f, fieldnames=columns, extrasaction="ignore").writerows(rows)

    try:
        cols = ", ".join(columns)
        conn.execute(text(f"ALTER TABLE {table_name} DISABLE KEYS"))
        conn.execute(text(f"""
            LOAD DATA LOCAL INFILE :path
            IGNORE INTO TABLE {table_name}
            FIELDS TERMINATED BY ','
            OPTIONALLY ENCLOSED BY '"'
            LINES TERMINATED BY '\\n'
            ({cols})
        """), {"path": tmp_path})
        print(f"  Rebuilding indexes of {table_name}...")
        conn.execute(text(f"ALTER TABLE {table_name} ENABLE KEYS"))
        conn.commit()
    finally:
        os.unlink(tmp_path)


if __name__ == "__main__":
    df = create_dataframe()
    create_catalog()

    data = extract_all(df)
    del df

    set_session_optimizations()

    bulk_load(data["movies"],           Movie,            "Inserting movies")
    bulk_load(data["directors"],        Director,         "Inserting directors")
    bulk_load(data["actors"],           Actor,            "Inserting actors")
    bulk_load(data["writers"],          Writer,           "Inserting writers")
    bulk_load(data["movies_genres"],    movies_genres,    "Inserting genres")
    bulk_load(data["movies_directors"], movies_directors, "Inserting directors relationship")
    bulk_load_infile(data["movies_actors"], "movies_actors", ["movie_id", "actor_id"], "Inserting actors relationship")
    bulk_load(data["movies_writers"],   movies_writers,   "Inserting writer relationship")

    reset_session_optimizations()
    conn.close()
