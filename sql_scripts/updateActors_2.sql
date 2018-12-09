UPDATE actors SET
    name = :name,
    gender = :gender,
    country = :country,
    year_of_birth = :year_of_birth,
    year_of_decease = :year_of_decease,
    image = ''
WHERE actor_id = :actor_id