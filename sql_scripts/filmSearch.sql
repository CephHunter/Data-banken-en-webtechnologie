SELECT movie_id FROM movie_genre 
WHERE genre_id IN (
    SELECT genre_id FROM genres WHERE genre_name IN ('Horror')
)