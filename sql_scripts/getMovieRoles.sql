SELECT roles.[role], actors.[name], actors.gender, actors.country,
    actors.year_of_birth, actors.year_of_decease, actors.[image], actors.actor_id
FROM roles
INNER JOIN actors ON roles.actor_id = actors.actor_id
WHERE roles.movie_id = ?