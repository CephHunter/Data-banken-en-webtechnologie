UPDATE movies SET
    title = ?,
    description = ?,
    country = ?,
    releaseyear = ?,
    budget = ?,
    image = COALESCE(?, (SELECT image FROM movies WHERE movie_id=?))
WHERE movie_id = ?
