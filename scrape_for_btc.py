import sqlite3

db_filename = "my.db"

con = sqlite3.connect("my.db")
cur = con.cursor()






def init_db():
    create_tables()
    return

def create_tables():
    sql_statements = [ 
        """CREATE TABLE IF NOT EXISTS projects (
                id INTEGER PRIMARY KEY, 
                name text NOT NULL, 
                begin_date TEXT, 
                end_date TEXT
        );""",
        """CREATE TABLE IF NOT EXISTS tasks (
                id INTEGER PRIMARY KEY, 
                name TEXT NOT NULL, 
                priority INT, 
                project_id INT NOT NULL, 
                status_id INT NOT NULL, 
                begin_date TEXT NOT NULL, 
                end_date TEXT NOT NULL, 
                FOREIGN KEY (project_id) REFERENCES projects (id)
        );"""]

    # create a database connection
    try:
        with sqlite3.connect("my.db") as conn:
            cursor = conn.cursor()
            for statement in sql_statements:
                cursor.execute(statement)
            
            conn.commit()
    except sqlite3.Error as e:
        print(e)




def do_the_do():
    return


def create_sqlite_database(filename):
    """ create a database connection to an SQLite database """
    conn = None
    try:
        conn = sqlite3.connect(filename)
        print(sqlite3.sqlite_version)
        init_db()
    except sqlite3.Error as e:
        print(e)
    finally:
        if conn:
            conn.close()


if __name__ == '__main__':
    create_sqlite_database(db_filename)