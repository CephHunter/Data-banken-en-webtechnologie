import os
import sys
import sqlite3
from flask import session
from flask_login import UserMixin
from datetime import datetime

# global variables
rootpath = os.path.dirname(__file__) + "\\"
sqlpath = rootpath + "sql_scripts\\"
templatepath = rootpath + "templates\\"
databaseFile = rootpath + "filmdata.db"


def runScript(scriptname):
    """Execute multiple SQL queries at once.
    
    Arguments:
        scriptname {String} -- Name of the file to run.
    """
    db = sqlite3.connect(databaseFile)
    cursor = db.cursor()
    script = open(sqlpath + scriptname, "r").read()
    cursor.executescript(script)
    db.commit()
    db.close()

def insertData(scriptname, *args):
    """Execute a single SQL query. Can write multiple lines of data in one call.
    
    Arguments:
        scriptname {String} -- Name of the file to run.
        args {Varies} -- Params to substute in the query.
    """
    db = sqlite3.connect(databaseFile)
    cursor = db.cursor()
    script = open(sqlpath + scriptname, "r").read()
    cursor.execute('pragma foreign_keys=ON')
    cursor.executemany(script, args)
    db.commit()
    db.close()

def getData(scriptname, *args, raw=None):
    """Execute a single select SQL query and return the result.
    
    Arguments:
        scriptname {String} -- Name of the file to run.
        args {Varies} -- Params to substute in the query.
    """
    db = sqlite3.connect(databaseFile)
    cursor = db.cursor()
    script = open(sqlpath + scriptname, "r").read()
    if raw:
        res = cursor.execute(script, raw).fetchall()
    else:
        res = cursor.execute(script, args).fetchall()
    db.commit()
    db.close()
    return res

def getNextID(tableName, idname):
    db = sqlite3.connect(databaseFile)
    cursor = db.cursor()
    sql = 'SELECT max({})+1 FROM {}'.format(idname, tableName)
    res = cursor.execute(sql).fetchone()[0]
    db.commit()
    db.close()
    return res

class User(UserMixin):
    def __init__(self, id, alias, email, password, birthday, gender, country, is_authenticated):
        self.id = id
        self.alias = alias
        self.email = email
        self.password = password
        self.birthday = birthday
        self.gender = gender
        self.country = country
        self.is_authenticated = is_authenticated

    def get_id(self):
        return self.email

    def __repr__(self):
        return 'id:%d, email:%s, alias:%s' % (self.id, self.email, self.alias)

    @property
    def is_authenticated(self):
        return self.__is_authenticated

    @is_authenticated.setter
    def is_authenticated(self, is_authenticated):
        self.__is_authenticated = is_authenticated

    @classmethod
    def get(cls, email):
        userData = getData('getUserData.sql', email)
        if userData:
            userData = userData[0]
            return cls(userData[0], userData[1], userData[2], userData[3],
                        userData[4], userData[5], userData[6], True)
        return None


def getLoggedInUser():
    try:
        return User.get(session['user_id'])
    except:
        return User('', '', '', '', '', '', '', False)


def currentTime():
    now = datetime.utcnow()
    return now.strftime('%Y/%m/%d %H:%M:%S')