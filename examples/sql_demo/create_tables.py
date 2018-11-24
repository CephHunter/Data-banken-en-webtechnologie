sql = """
CREATE TABLE movies (
	movie_id	INTEGER NOT NULL,
	title	TEXT NOT NULL,
	PRIMARY KEY(movie_id)
);
"""

movies = """
CREATE TABLE IF NOT EXISTS movies (
	movie_id	INTEGER NOT NULL,
	titel	    TEXT NOT NULL,
    jaar        INTEGER,
    land        TEXT,
    inhoud      TEXT,
	PRIMARY KEY(movie_id)
);
"""

genres = """
CREATE TABLE IF NOT EXISTS genres (
    genre TEXT,
    PRIMARY KEY(genre)
);
"""

insert = """
INSERT INTO movies (titel, jaar, land, inhoud)
    VALUES ("test title", 1985, "USA", "hello worlds")
"""