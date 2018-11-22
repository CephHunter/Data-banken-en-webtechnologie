import sqlite3
import os

rootpath = os.path.dirname(__file__) + "\\"
sqlpath = rootpath + "sql_scripts\\"
templatepath = rootpath + "templates\\"

if __name__ == "__main__":
    db = sqlite3.connect(rootpath + 'filmdata.db')
    cursor = db.cursor()
    # cursor.execute('pragma foreign_keys=ON')
    script = open(sqlpath + "create_tables.sql", "r").read()
    cursor.executescript(script)
    db.commit()
    db.close()