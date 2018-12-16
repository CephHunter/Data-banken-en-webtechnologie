SELECT movie_id, title, [description], [image]
FROM movies
WHERE title LIKE ? AND movie_id IN (
    SELECT DISTINCT movie_id
    FROM movie_genre
    WHERE genre_id IN (
        SELECT genre_id FROM genres WHERE genre_name IN (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    )
)
LIMIT 50
