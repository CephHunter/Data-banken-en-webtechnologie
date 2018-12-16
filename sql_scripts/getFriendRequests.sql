SELECT
    u1.user_id,
    u1.alias,
    u2.user_id,
    u2.alias,
    friendships.date_send,
    friendships.date_accepted,
    friendships.date_canceled
FROM friendships
LEFT JOIN users AS u1
    ON u1.user_id = friendships.sender_user_id
    AND u1.user_id <> :user_id
LEFT JOIN users AS u2
    ON u2.user_id = friendships.receiver_user_id
    AND u2.user_id <> :user_id
WHERE 
    friendships.sender_user_id = :user_id
    OR friendships.receiver_user_id = :user_id
