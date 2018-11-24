import sqlite3
import os

if __name__ == "__main__":
    from sys import argv

    db = sqlite3.connect('movies.db')
    cursor = db.cursor()
    cursor.execute('pragma foreign_keys=ON')
    script = open("create_tables.sql", "r").read()
    cursor.executescript(script)
    db.commit()
    db.close()