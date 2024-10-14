import sqlite3

def chk_conn(conn):
    try:
        conn.cursor()
        return True
    except Exception as ex:
        return False

conn = sqlite3.connect("my.db")
print(chk_conn(conn))

cur = conn.cursor()
cur.execute("SELECT name FROM sqlite_master WHERE type='table';")
print(cur.fetchall())

cur.execute("SELECT * FROM cmc_data LIMIT 10")
data = cur.fetchall()

for row in data:
    print(row)

conn.close()
