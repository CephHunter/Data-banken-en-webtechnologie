CREATE TABLE IF NOT EXISTS movies (
	movie_id	INTEGER NOT NULL,
	titel	    TEXT NOT NULL,
    jaar        INTEGER,
    land        TEXT,
    inhoud      TEXT,
	PRIMARY KEY(movie_id)
);

INSERT INTO movies (titel, jaar, land, inhoud)
    VALUES ("test title", 1985, "USA", "hello worlds"),
    ("test title", 1986, "USA", "hello worlds"),
    ("test title", 1987, "USA", "aello worlds");

INSERT INTO movies (titel, jaar, inhoud)
    VALUES ("test title", 1985, "hello worlds"),
    ("test title", 1986, "hello worlds"),
    ("test title", 1987, "aello worlds");

DROP TABLE track;
DROP TABLE artist;

CREATE TABLE IF NOT EXISTS artist(
  artistid    INTEGER PRIMARY KEY, 
  artistname  TEXT
);

CREATE TABLE IF NOT EXISTS track(
  trackid     INTEGER PRIMARY KEY, 
  trackname   TEXT, 
  trackartist INTEGER,
  FOREIGN KEY(trackartist) REFERENCES artist(artistid)
);

INSERT INTO artist 
VALUES (1, "aaa"),
(2, 'bbb');

INSERT INTO track (trackname, trackartist) VALUES ('v', 10)

-- DROP TABLE track;
-- DROP TABLE artist;