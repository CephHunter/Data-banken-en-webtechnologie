from utils import *
from passlib.hash import pbkdf2_sha256
from datetime import datetime

# def test(*args, t=None):
#     for a in args:
#         print(a)
#     if t:
#         print(t)
    

# insertData('updateActors.sql', 
#             {
#                 'actor_id': '16' or None,
#                 'name': 'test',
#                 'gender': 'Male',
#                 'country': 'BE',
#                 'year_of_birth': 1000,
#                 'year_of_decease': 4
#             }
#         )

# test([{'a':i} for i in range(0, 5)])
# print(getNextID('actors', 'actor_id'))
# nextactorID = getNextID('actors', 'actor_id')
# actorIDs = ['', 10, 20, '']
# actorIDs = [(id or (nextactorID + i)) for i, id in enumerate(actorIDs)]
# print(actorIDs)
