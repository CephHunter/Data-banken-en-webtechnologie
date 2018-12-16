SELECT
    users.user_id,
    users.alias,
    users.email,
    users.date_of_birth,
    users.gender,
    users.country,
    f1.date_send,
    f1.date_accepted,
    f1.date_canceled,
    f2.date_send,
    f2.date_accepted,
    f2.date_canceled
FROM users
LEFT JOIN friendships AS f1
    ON users.user_id = f1.receiver_user_id
    AND f1.sender_user_id = :self_id
LEFT JOIN friendships AS f2
    ON users.user_id = f2.sender_user_id
    AND f2.receiver_user_id = :self_id
WHERE
    users.alias LIKE :search
    AND NOT users.user_id = :self_id
LIMIT 50