from utils import *
from passlib.hash import pbkdf2_sha256

hash = pbkdf2_sha256.hash("password")

print(hash)
print(pbkdf2_sha256.verify("passworz", hash))