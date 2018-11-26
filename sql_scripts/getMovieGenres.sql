SELECT genre_name
FROM genres
WHERE genre_id IN (
    SELECT genre_id
    FROM movie_genre
    WHERE movie_id IN (
        SELECT movie_id
        FROM movies
        WHERE title = ?
    )
)