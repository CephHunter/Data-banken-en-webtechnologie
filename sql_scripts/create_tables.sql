BEGIN;
DROP TABLE IF EXISTS movies;
DROP TABLE IF EXISTS actors;
DROP TABLE IF EXISTS users;
DROP TABLE IF EXISTS genres;
DROP TABLE IF EXISTS movie_genre;
DROP TABLE IF EXISTS roles;
DROP TABLE IF EXISTS movie_reception;
DROP TABLE IF EXISTS reviews;
DROP TABLE IF EXISTS comments;
DROP TABLE IF EXISTS friendships;

CREATE TABLE IF NOT EXISTS movies (
    movie_id      INTEGER NOT NULL PRIMARY KEY,
    title         TEXT NOT NULL,
    [description] TEXT NOT NULL,
    country       TEXT NOT NULL,
    releaseyear   INTEGER NOT NULL,
    budget        INTEGER NOT NULL
);

CREATE TABLE IF NOT EXISTS actors (
    actor_id        INTEGER NOT NULL PRIMARY KEY,
    [name]          TEXT NOT NULL,
    gender          TEXT NOT NULL,
    country         TEXT NOT NULL,
    year_of_birth   INTEGER NOT NULL,
    year_of_decease INTEGER NOT NULL
);

CREATE TABLE IF NOT EXISTS users (
    user_id       INTEGER NOT NULL PRIMARY KEY,
    alias         TEXT NOT NULL,
    email         TEXT NOT NULL,
    [password]    TEXT NOT NULL,
    date_of_birth TEXT NOT NULL,
    gender        TEXT NOT NULL,
    country       TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS genres (
    genre_id      INTEGER NOT NULL PRIMARY KEY,
    genre_name    TEXT NOT NULL,
    [description] TEXT NOT NULL
);

-- Descriptions copied from imdb.com
INSERT INTO genres (genre_name, [description])
    VALUES ('Action', "Should contain numerous scenes where action is spectacular and usually destructive. Note: if a movie contains just one action scene (even if prolonged, i.e. airplane-accident) it does not qualify. Subjective."),
    ('Adventure', "Should contain numerous consecutive and inter-related scenes of characters participating in hazardous or exciting experiences for a specific goal. Not to be confused with Action, and should only sometimes be supplied with it. Subjective."),
    ('Animation', "Over 75% of the title's running time should have scenes that are wholly, or part-animated. Any form of animation is acceptable, e.g., hand-drawn, computer-generated, stop-motion, etc. Puppetry does not count as animation, unless a form of animation such as stop-motion is also applied. Incidental animated sequences should be indicated with the keywords part-animated or animated-sequence instead. Although the overwhelming majority of video games are a form of animation it's okay to forgo this genre when adding them as this is implied by the title type. Objective."),
    ('Comedy', "Virtually all scenes should contain characters participating in humorous or comedic experiences. The comedy can be exclusively for the viewer, at the expense of the characters in the title, or be shared with them. Please submit qualifying keywords to better describe the humor (i.e. spoof, parody, irony, slapstick, satire, black-comedy etc). If the title does not conform to the 'virtually all scenes' guideline then please do not add the comedy genre; instead, submit the same keyword variations described above to signify the comedic elements of the title. Subjective."),
    ('Crime', "Whether the protagonists or antagonists are criminals this should contain numerous consecutive and inter-related scenes of characters participating, aiding, abetting, and/or planning criminal behavior or experiences usually for an illicit goal. Not to be confused with Film-Noir, and only sometimes should be supplied with it. Subjective."),
    ('Drama', "Should contain numerous consecutive scenes of characters portrayed to effect a serious narrative throughout the title. This can be exaggerated upon to produce melodrama. Subjective."),
    ('Fantasy', "Should contain numerous consecutive scenes of characters portrayed to effect a magical and/or mystical narrative throughout the title. Note: not to be confused with Sci-Fi which is not usually based in magic or mysticism. Subjective."),
    ('Horror', "Should contain numerous consecutive scenes of characters effecting a terrifying and/or repugnant narrative throughout the title. Note: not to be confused with Thriller which is not usually based in fear or abhorrence. Subjective."),
    ('Mistery', "Should contain numerous inter-related scenes of one or more characters endeavoring to widen their knowledge of anything pertaining to themselves or others. Note: Usually, but not always associated with Crime. Subjective."),
    ('Romance', "Should contain numerous inter-related scenes of a character and their personal life with emphasis on emotional attachment or involvement with other characters, especially those characterized by a high level of purity and devotion. Note: Reminder, as with all genres if this does not describe the movie wholly, but only certain scenes or a subplot, then it should be submitted as a keyword instead. Subjective."),
    ('Sci-Fi', "Numerous scenes, and/or the entire background for the setting of the narrative, should be based on speculative scientific discoveries or developments, environmental changes, space travel, or life on other planets. Subjective."),
    ('Thriller', "Should contain numerous sensational scenes or a narrative that is sensational or suspenseful. Note: not to be confused with Mystery or Horror, and should only sometimes be accompanied by one (or both). Subjective.");

CREATE TABLE IF NOT EXISTS movie_genre (
    movie_id  INTEGER NOT NULL REFERENCES movies (movie_id),
    genre_id  INTEGER NOT NULL REFERENCES genres (genre_id),
    PRIMARY KEY (genre_id, movie_id)
);

CREATE TABLE IF NOT EXISTS roles (
    movie_id  INTEGER NOT NULL REFERENCES movies (movie_id),
    [role]    TEXT NOT NULL,
    actor_id  INTEGER NOT NULL REFERENCES actors (actor_id),
    PRIMARY KEY (movie_id, role)
);

CREATE TABLE IF NOT EXISTS movie_reception (
    movie_id      INTEGER NOT NULL REFERENCES movies (movie_id),
    country       TEXT NOT NULL,
    release_date  TEXT NOT NULL,
    viewers       INTEGER NOT NULL,
    profit        INTEGER NOT NULL,
    PRIMARY KEY (movie_id, country)
);

CREATE TABLE IF NOT EXISTS reviews (
    movie_id      INTEGER NOT NULL REFERENCES movies (movie_id),
    user_id       INTEGER NOT NULL REFERENCES users (user_id),
    score         INTEGER NOT NULL,
    review        TEXT NOT NULL,
    create_date   TEXT NOT NULL,
    edit_date     TEXT NOT NULL,
    PRIMARY KEY (movie_id, user_id)
);

CREATE TABLE IF NOT EXISTS comments (
    movie_id          INTEGER NOT NULL,
    review_user_id    INTEGER NOT NULL,
    user_id           INTEGER NOT NULL,
    comment           TEXT NOT NULL,
    create_date       TEXT NOT NULL,
    edit_date         TEXT NOT NULL,
    PRIMARY KEY (movie_id, review_user_id, user_id),
    FOREIGN KEY (movie_id, review_user_id) REFERENCES reviews (movie_id, user_id)
);

CREATE TABLE IF NOT EXISTS friendships (
    sender_user_id      INTEGER NOT NULL REFERENCES users (user_id),
    receiver_user_id    INTEGER NOT NULL REFERENCES users (user_id),
    date_send           TEXT NOT NULL,
    date_accepted       TEXT,
    date_canceled       TEXT,
    PRIMARY KEY (sender_user_id, receiver_user_id),
    CHECK (sender_user_id <> receiver_user_id)
);

COMMIT;

-- pragma foreign_keys=ON;
-- insert into movies values (NULL, 't', 't', 't', 1, 1), (NULL, 't', 't', 't', 1, 1), (NULL, 't', 't', 't', 1, 1);
-- insert into users values (NULL, 't', 't', 't', 't', 't', 't'), (NULL, 't', 't', 't', 't', 't', 't'), (NULL, 't', 't', 't', 't', 't', 't');
-- insert into reviews values (1, 1, 5, "", "t", "t"), (1, 3, 5, "", "t", "t");
-- insert into comments values (NULL, 1, 1), (NULL, 1, 1);
-- insert into friendships VALUES (1,3)