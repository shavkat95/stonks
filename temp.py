import sqlite3














def execute_sql(sql_statements):
    # execute statements
    try:
        with sqlite3.connect("my.db") as conn:
            cursor = conn.cursor()
            for statement in sql_statements:
                cursor.execute(statement)
            conn.commit()
    except sqlite3.Error as e:
        print(e)
    
    

sql_statements = [ 
    """DROP TABLE IF EXISTS the_do;"""]


execute_sql(sql_statements)











