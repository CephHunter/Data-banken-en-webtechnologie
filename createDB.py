import sqlite3
import json
from utils import *


if __name__ == "__main__":
    # # Create tables
    runScript("create_tables.sql")

    # Add some data to the tables
    filmdata = open(rootpath + "FilmData.json").read()
    filmdata = json.loads(filmdata)
    for movie in filmdata:
        insertData("insertMovie.sql", (movie["title"], movie["description"],
                                       movie["country"], movie["date_of_release"], movie["budget"]))
        movie_id = getData("getMovieID.sql", movie["title"])[0][0]

        for genre in movie["genres"]:
            genre_id = getData("getGenreID.sql", genre)[0][0]
            insertData("insertMovieGenres.sql", (movie_id, genre_id))

        for role in movie["roles"]:
            actor = role["actor"]
            insertData("insertActor.sql", (actor["name"], actor["gender"],
                                           actor["country"], actor["year_of_birth"], actor["year_of_decease"]))
            actor_id = getData("getActorID.sql", actor["name"])[0][0]
            insertData("insertRole.sql", (movie_id, role["role"], actor_id))
