import os
import sqlite3

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

def getData(scriptname, *args):
    """Execute a single select SQL query and return the result.
    
    Arguments:
        scriptname {String} -- Name of the file to run.
        args {Varies} -- Params to substute in the query.
    """
    db = sqlite3.connect(databaseFile)
    cursor = db.cursor()
    script = open(sqlpath + scriptname, "r").read()
    res = cursor.execute(script, args).fetchall()
    db.commit()
    db.close()
    return res