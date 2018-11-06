import sqlite3
import create_tables as ct

# sql = """
# CREATE TABLE `movies` (
# 	`movie_id`	INTEGER NOT NULL,
# 	`title`	TEXT NOT NULL,
# 	PRIMARY KEY(`movie_id`)
# );
# """

if __name__ == "__main__":
    from sys import argv

    if len(argv) != 2:
        print("Exited with error code 1")
        exit(1)

    db_file = argv[1]
    db = sqlite3.connect(db_file)

    cursor = db.cursor()
    cursor.execute(ct.movies)
    cursor.execute(ct.insert)
    db.commit()

    db.close()