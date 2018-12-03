DELETE FROM reviews
WHERE user_id = ? AND movie_id IN (
    SELECT movie_id FROM movies WHERE title = ?
)