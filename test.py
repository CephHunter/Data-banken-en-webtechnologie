from utils import *
from passlib.hash import pbkdf2_sha256
from datetime import datetime


# test([{'a':i} for i in range(0, 5)])
# print(getNextID('actors', 'actor_id'))
# nextactorID = getNextID('actors', 'actor_id')
# actorIDs = ['', 10, 20, '']
# actorIDs = [(id or (nextactorID + i)) for i, id in enumerate(actorIDs)]
# print(actorIDs)

insertData(
    'updateFriendRequest.sql',
    {
        'sender': 1,
        'receiver': 3,
        'send_date': None,
        'date_accepted': None,
        'date_canceled': None
    }
)
