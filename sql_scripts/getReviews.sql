SELECT reviews.score, reviews.review, reviews.create_date, reviews.edit_date, 
    users.user_id, users.alias, users.email
FROM reviews
INNER JOIN users ON reviews.user_id = users.user_id
WHERE movie_id IN (
    SELECT movie_id FROM movies WHERE title = ?
)