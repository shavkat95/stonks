# nohup python3 main.py > output.log &
# ps -ef | grep python
# pkill -9 -f main.py





from datetime import time
import datetime
from time import sleep
import sqlite3
import the_do
import cmc

def act(x):
    return x+10

def get_next_full_hour():
    fullhour = str(datetime.datetime.today().time())[:2]
    if int(fullhour) < 23:
        return str(int(fullhour)+1)+':00'
    else:
        return '00:00'
    

def wait_until(runTime, action=None):
    if runTime == '00:00':
        runTime = '23:59:59:999999'
    startTime = time(*(map(int, runTime.split(':'))))
    # 59
    if (datetime.datetime.now() + datetime.timedelta(minutes = 59)).time() < startTime:
        sleep(3540)
        while startTime > datetime.datetime.today().time():
            if str(datetime.datetime.today().time())[3] == '0':
                return action(runTime)
            sleep(60)
        return action(runTime)
    
    # 50
    if (datetime.datetime.now() + datetime.timedelta(minutes = 50)).time() < startTime:
        sleep(3000)
    
    # 40
    if (datetime.datetime.now() + datetime.timedelta(minutes = 40)).time() < startTime:
        sleep(2400)
    
    if (datetime.datetime.now() + datetime.timedelta(minutes = 20)).time() < startTime:
        sleep(1200)
    
    if (datetime.datetime.now() + datetime.timedelta(minutes = 10)).time() < startTime:
        sleep(600)
        
    if (datetime.datetime.now() + datetime.timedelta(minutes = 5)).time() < startTime:
        sleep(300)
        
    if (datetime.datetime.now() + datetime.timedelta(minutes = 2)).time() < startTime:
        sleep(120)
    
    if (datetime.datetime.now() + datetime.timedelta(minutes = 1)).time() < startTime:
        sleep(60)
        
    while startTime > datetime.datetime.today().time():
        if str(datetime.datetime.today().time())[3] == '0':
            return action(runTime)
        sleep(60)
    return action(runTime)


def run_sql_statements(statements):
    try:
        with sqlite3.connect("my.db") as conn:
            cursor = conn.cursor()
            for statement in statements:
                cursor.execute(statement)
            conn.commit()
    except sqlite3.Error as e:
        print(e)
        

def wait_next_full_hour(nh = None, action=None):
    if nh==None:
        nh = get_next_full_hour()
    return wait_until(nh, action)


def get_row(nh):
    reddit = {}
    
    # create id
    date = datetime.datetime.today()
    id = str(date)+' - '+str(nh)
    
    # get scraping data
    for kw in the_do.keywords:
        reddit[kw] = the_do.do_the_do(kw)
    
    # get price change data
    metrics = cmc.get_metrics()
    
    # write to db
    
    # new row
    sql_statements = [ 
        f"""INSERT INTO the_do (id)
            VALUES ({id});""",
        ]
    run_sql_statements(sql_statements)
    
    sql_statements = []
    for kw, list_1 in reddit.items():
        # [hr2, hr12, hr24, d7, mo] = list_1
        i = 0
        for interval in ["_2hr_", "_12hr_", "_3d_", "_7d_", "_mo_"]:
            for col in ["headlines", "texts", "votes", "comments", "comment_counts", "comment_votes"]:
                sql_statements.append(f"""REPLACE INTO the_do (id, {str(kw)+str(interval)+str(col)}) VALUES({id}, {list_1[i][col]});""")
            i+=1
    run_sql_statements(sql_statements)
    
    sql_statements = []
    for met_ in cmc.metrics:
        if not metrics[met_]:
            print("ERROR 28")
            exit()
        sql_statements.append(f"""REPLACE INTO the_do (id, {met_}) VALUES({id}, {metrics[met_]});""")
        
    return id





while True:
    nh = get_next_full_hour()
    wait_next_full_hour(nh = nh, action=get_row)
    # get_row("12:00")
    
