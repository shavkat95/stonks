# nohup python3 main.py > output.log &
# ps -ef | grep python
# pkill -9 -f main.py





from datetime import time
import datetime
from time import sleep
import pandas as pd
import csv
from scrape_for_btc import scrape_reddit_btc
import sqlite3

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
                return action()
            sleep(60)
        return action()
    
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
            return action()
        sleep(60)
    return action()



def run_sql_statements(statements):
    try:
        with sqlite3.connect("my.db") as conn:
            cursor = conn.cursor()
            for statement in statements:
                cursor.execute(statement)
            conn.commit()
    except sqlite3.Error as e:
        print(e)
        
        

def get_row(nh):
    print('getting row')
    if nh == '00:00':
        date = datetime.datetime.today() + datetime.timedelta(days=1)
    else:
        date = datetime.datetime.today()
    id = str(date)+' - '+str(nh)
    btc_reddit_headlines = scrape_reddit_btc()
    sql_statements = [ 
        f"""INSERT INTO the_do (id, BTC_R)
            VALUES ({id},{btc_reddit_headlines});""",
        ]
    run_sql_statements(sql_statements)
    return [id, btc_reddit_headlines]

def wait_next_full_hour(nh = None, action=None):
    if nh==None:
        nh = get_next_full_hour()
    if nh == '00:00':
        date = datetime.datetime.today() + datetime.timedelta(days=1)
    else:
        date = datetime.datetime.today()
    id = str(date)[:10]+'-'+str(nh)
    print(id)
    return wait_until(nh, action)




while True:
    nh = get_next_full_hour()
    wait_next_full_hour(nh = nh, action=get_row)
    
    

# open the file in the write mode
f = open('csv_file.csv', 'w')

# create the csv writer
writer = csv.writer(f)

# write a row to the csv file
writer.writerow(['eins', 'zwo'])

# close the file
f.close()