INSERT OR REPLACE INTO friendships VALUES (
    :sender,
    :receiver,
    COALESCE(
        :send_date, 
        (SELECT date_send 
            FROM friendships 
            WHERE sender_user_id=:sender AND receiver_user_id=:receiver),
        ''
    ),
    COALESCE(
        :date_accepted, 
        (SELECT date_accepted 
            FROM friendships 
            WHERE sender_user_id=:sender AND receiver_user_id=:receiver),
        ''
    ),
    COALESCE(
        :date_canceled, 
        (SELECT date_canceled 
            FROM friendships 
            WHERE sender_user_id=:sender AND receiver_user_id=:receiver),
        ''
    )
)