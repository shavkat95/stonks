import sqlite3

db_filename = "my.db"


import time

from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
import selenium
from selenium.webdriver.common.by import By
from selenium.webdriver import ChromeOptions
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager


options = ChromeOptions()
options.binary_location = "path/to/chromedriver_linux64/chromedriver"    #chrome binary location specified here
options.add_argument("--start-maximized") #open Browser in maximized mode
options.add_argument("--no-sandbox") #bypass OS security model
options.add_argument("--disable-dev-shm-usage") #overcome limited resource problems
options.add_argument("--disable-extensions")

# options.add_experimental_option("excludeSwitches", ["enable-automation"])
# options.add_experimental_option('useAutomationExtension', False)



SCROLL_PAUSE_TIME = 2





def init_db():
    create_tables()
    return



    

def create_tables():
    # also deletes 'the_do'-table
    sql_statements = [ 
        """DROP TABLE IF EXISTS the_do;""",
        """CREATE TABLE the_do (
                id TEXT PRIMARY KEY, 
                BTC_R VARCHAR(65535), 
                some_numeric smallint, 
                some_bigger_numeric int
        );""",
        # """CREATE TABLE IF NOT EXISTS tasks (
        #         id INTEGER PRIMARY KEY, 
        #         name TEXT NOT NULL, 
        #         priority INT, 
        #         project_id INT NOT NULL, 
        #         status_id INT NOT NULL, 
        #         begin_date TEXT NOT NULL, 
        #         end_date TEXT NOT NULL, 
        #         FOREIGN KEY (project_id) REFERENCES projects (id)
        # );"""
        ]

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


def get_search_data(kw):
    # return list with data to keyword search
    # posts sentiment info last 2 hours (headline, text, votes, comments, comment count, comment votes, word count) -> mean + activity info (posts count, comments count, votes count)
    # active posts sentiment info last 12 hours (headline, text, votes, comments, comment count, comment votes, word count) -> mean + activity info (posts count, comments count, votes count)
    output = []
    driver = webdriver.Firefox()
    driver.get(f'https://www.reddit.com/search/?q={kw}&sort=new')
    time.sleep(SCROLL_PAUSE_TIME) # Sleep for 3 seconds
    
    return output



def scrape_reddit_btc():
    driver = webdriver.Chrome(options=options)
    result = ''
    driver.get('https://www.reddit.com/search/?q=bitcoin&sort=new')

    driver.implicitly_wait(3)
    time.sleep(SCROLL_PAUSE_TIME) # Sleep for 3 seconds
    
    i = 1
    while True:
        try:
            # /html/body/shreddit-app/search-dynamic-id-cache-controller/div/div/div[1]/div[2]/main/div/reddit-feed/faceplate-tracker[1]/post-consume-tracker/div/div/a
            my_element = driver.find_element(By.XPATH, f"/html/body/shreddit-app/search-dynamic-id-cache-controller/div/div/div[1]/div[2]/main/div/reddit-feed/faceplate-tracker[{i}]/post-consume-tracker/div/div/a")
            # /html/body/shreddit-app/search-dynamic-id-cache-controller/div/div/div[1]/div[2]/main/div/reddit-feed/faceplate-tracker[1]/post-consume-tracker/div/div/div[2]/span[1]/faceplate-number
            comments = driver.find_element(By.XPATH, f"/html/body/shreddit-app/search-dynamic-id-cache-controller/div/div/div[1]/div[2]/main/div/reddit-feed/faceplate-tracker[{i}]/post-consume-tracker/div/div/div[2]/span[1]/faceplate-number")
            # /html/body/shreddit-app/search-dynamic-id-cache-controller/div/div/div[1]/div[2]/main/div/reddit-feed/faceplate-tracker[1]/post-consume-tracker/div/div/div[2]/span[3]/faceplate-number
            votes = driver.find_element(By.XPATH, f"/html/body/shreddit-app/search-dynamic-id-cache-controller/div/div/div[1]/div[2]/main/div/reddit-feed/faceplate-tracker[{i}]/post-consume-tracker/div/div/div[2]/span[3]/faceplate-number")
        except selenium.common.exceptions.NoSuchElementException as e:
            print('\n bad bad at - '+str(i))
            break
        i+=1
        result+="\n "+my_element.text + " -votes:"+str(votes.text)+ " -comments:"+str(comments.text)+" \n "
        
    # driver.implicitly_wait(1)
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    # Wait to load page
    time.sleep(SCROLL_PAUSE_TIME)

    while True:
        try:
            # /html/body/shreddit-app/search-dynamic-id-cache-controller/div/div/div[1]/div[2]/main/div/reddit-feed/faceplate-tracker[1]/post-consume-tracker/div/div/a
            my_element = driver.find_element(By.XPATH, f"/html/body/shreddit-app/search-dynamic-id-cache-controller/div/div/div[1]/div[2]/main/div/reddit-feed/faceplate-tracker[{i}]/post-consume-tracker/div/div/a")
            # /html/body/shreddit-app/search-dynamic-id-cache-controller/div/div/div[1]/div[2]/main/div/reddit-feed/faceplate-tracker[1]/post-consume-tracker/div/div/div[2]/span[1]/faceplate-number
            comments = driver.find_element(By.XPATH, f"/html/body/shreddit-app/search-dynamic-id-cache-controller/div/div/div[1]/div[2]/main/div/reddit-feed/faceplate-tracker[{i}]/post-consume-tracker/div/div/div[2]/span[1]/faceplate-number")
            # /html/body/shreddit-app/search-dynamic-id-cache-controller/div/div/div[1]/div[2]/main/div/reddit-feed/faceplate-tracker[1]/post-consume-tracker/div/div/div[2]/span[3]/faceplate-number
            votes = driver.find_element(By.XPATH, f"/html/body/shreddit-app/search-dynamic-id-cache-controller/div/div/div[1]/div[2]/main/div/reddit-feed/faceplate-tracker[{i}]/post-consume-tracker/div/div/div[2]/span[3]/faceplate-number")
        except selenium.common.exceptions.NoSuchElementException as e:
            print('\n bad bad at - '+str(i))
            break
        i+=1
        result+="\n "+my_element.text + " -votes:"+str(votes.text)+ " -comments:"+str(comments.text)+" \n "
        
    # driver.implicitly_wait(1)
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    # Wait to load page
    time.sleep(SCROLL_PAUSE_TIME)

    while True:
        try:
            # /html/body/shreddit-app/search-dynamic-id-cache-controller/div/div/div[1]/div[2]/main/div/reddit-feed/faceplate-tracker[1]/post-consume-tracker/div/div/a
            my_element = driver.find_element(By.XPATH, f"/html/body/shreddit-app/search-dynamic-id-cache-controller/div/div/div[1]/div[2]/main/div/reddit-feed/faceplate-tracker[{i}]/post-consume-tracker/div/div/a")
            # /html/body/shreddit-app/search-dynamic-id-cache-controller/div/div/div[1]/div[2]/main/div/reddit-feed/faceplate-tracker[1]/post-consume-tracker/div/div/div[2]/span[1]/faceplate-number
            comments = driver.find_element(By.XPATH, f"/html/body/shreddit-app/search-dynamic-id-cache-controller/div/div/div[1]/div[2]/main/div/reddit-feed/faceplate-tracker[{i}]/post-consume-tracker/div/div/div[2]/span[1]/faceplate-number")
            # /html/body/shreddit-app/search-dynamic-id-cache-controller/div/div/div[1]/div[2]/main/div/reddit-feed/faceplate-tracker[1]/post-consume-tracker/div/div/div[2]/span[3]/faceplate-number
            votes = driver.find_element(By.XPATH, f"/html/body/shreddit-app/search-dynamic-id-cache-controller/div/div/div[1]/div[2]/main/div/reddit-feed/faceplate-tracker[{i}]/post-consume-tracker/div/div/div[2]/span[3]/faceplate-number")
        except selenium.common.exceptions.NoSuchElementException as e:
            print('\n bad bad at - '+str(i))
            break
        i+=1
        result+="\n "+my_element.text + " -votes:"+str(votes.text)+ " -comments:"+str(comments.text)+" \n "
        
    # driver.implicitly_wait(1)
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    # Wait to load page
    time.sleep(SCROLL_PAUSE_TIME)


        
    while True:
        try:
            # /html/body/shreddit-app/search-dynamic-id-cache-controller/div/div/div[1]/div[2]/main/div/reddit-feed/faceplate-tracker[1]/post-consume-tracker/div/div/a
            my_element = driver.find_element(By.XPATH, f"/html/body/shreddit-app/search-dynamic-id-cache-controller/div/div/div[1]/div[2]/main/div/reddit-feed/faceplate-tracker[{i}]/post-consume-tracker/div/div/a")
            # /html/body/shreddit-app/search-dynamic-id-cache-controller/div/div/div[1]/div[2]/main/div/reddit-feed/faceplate-tracker[1]/post-consume-tracker/div/div/div[2]/span[1]/faceplate-number
            comments = driver.find_element(By.XPATH, f"/html/body/shreddit-app/search-dynamic-id-cache-controller/div/div/div[1]/div[2]/main/div/reddit-feed/faceplate-tracker[{i}]/post-consume-tracker/div/div/div[2]/span[1]/faceplate-number")
            # /html/body/shreddit-app/search-dynamic-id-cache-controller/div/div/div[1]/div[2]/main/div/reddit-feed/faceplate-tracker[1]/post-consume-tracker/div/div/div[2]/span[3]/faceplate-number
            votes = driver.find_element(By.XPATH, f"/html/body/shreddit-app/search-dynamic-id-cache-controller/div/div/div[1]/div[2]/main/div/reddit-feed/faceplate-tracker[{i}]/post-consume-tracker/div/div/div[2]/span[3]/faceplate-number")
        except selenium.common.exceptions.NoSuchElementException as e:
            print('\n bad bad at - '+str(i))
            break
        i+=1
        result+="\n "+my_element.text + " -votes:"+str(votes.text)+ " -comments:"+str(comments.text)+" \n "
        
    # driver.implicitly_wait(1)
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    # Wait to load page
    time.sleep(SCROLL_PAUSE_TIME)


        
    while True:
        try:
            # /html/body/shreddit-app/search-dynamic-id-cache-controller/div/div/div[1]/div[2]/main/div/reddit-feed/faceplate-tracker[1]/post-consume-tracker/div/div/a
            my_element = driver.find_element(By.XPATH, f"/html/body/shreddit-app/search-dynamic-id-cache-controller/div/div/div[1]/div[2]/main/div/reddit-feed/faceplate-tracker[{i}]/post-consume-tracker/div/div/a")
            # /html/body/shreddit-app/search-dynamic-id-cache-controller/div/div/div[1]/div[2]/main/div/reddit-feed/faceplate-tracker[1]/post-consume-tracker/div/div/div[2]/span[1]/faceplate-number
            comments = driver.find_element(By.XPATH, f"/html/body/shreddit-app/search-dynamic-id-cache-controller/div/div/div[1]/div[2]/main/div/reddit-feed/faceplate-tracker[{i}]/post-consume-tracker/div/div/div[2]/span[1]/faceplate-number")
            # /html/body/shreddit-app/search-dynamic-id-cache-controller/div/div/div[1]/div[2]/main/div/reddit-feed/faceplate-tracker[1]/post-consume-tracker/div/div/div[2]/span[3]/faceplate-number
            votes = driver.find_element(By.XPATH, f"/html/body/shreddit-app/search-dynamic-id-cache-controller/div/div/div[1]/div[2]/main/div/reddit-feed/faceplate-tracker[{i}]/post-consume-tracker/div/div/div[2]/span[3]/faceplate-number")
        except selenium.common.exceptions.NoSuchElementException as e:
            print('\n bad bad at - '+str(i))
            break
        i+=1
        result+="\n "+my_element.text + " -votes:"+str(votes.text)+ " -comments:"+str(comments.text)+" \n "
        
    # driver.implicitly_wait(1)
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    # Wait to load page
    time.sleep(SCROLL_PAUSE_TIME)


        
    while True:
        try:
            # /html/body/shreddit-app/search-dynamic-id-cache-controller/div/div/div[1]/div[2]/main/div/reddit-feed/faceplate-tracker[1]/post-consume-tracker/div/div/a
            my_element = driver.find_element(By.XPATH, f"/html/body/shreddit-app/search-dynamic-id-cache-controller/div/div/div[1]/div[2]/main/div/reddit-feed/faceplate-tracker[{i}]/post-consume-tracker/div/div/a")
            # /html/body/shreddit-app/search-dynamic-id-cache-controller/div/div/div[1]/div[2]/main/div/reddit-feed/faceplate-tracker[1]/post-consume-tracker/div/div/div[2]/span[1]/faceplate-number
            comments = driver.find_element(By.XPATH, f"/html/body/shreddit-app/search-dynamic-id-cache-controller/div/div/div[1]/div[2]/main/div/reddit-feed/faceplate-tracker[{i}]/post-consume-tracker/div/div/div[2]/span[1]/faceplate-number")
            # /html/body/shreddit-app/search-dynamic-id-cache-controller/div/div/div[1]/div[2]/main/div/reddit-feed/faceplate-tracker[1]/post-consume-tracker/div/div/div[2]/span[3]/faceplate-number
            votes = driver.find_element(By.XPATH, f"/html/body/shreddit-app/search-dynamic-id-cache-controller/div/div/div[1]/div[2]/main/div/reddit-feed/faceplate-tracker[{i}]/post-consume-tracker/div/div/div[2]/span[3]/faceplate-number")
        except selenium.common.exceptions.NoSuchElementException as e:
            print('\n bad bad at - '+str(i))
            break
        i+=1
        result+="\n "+my_element.text + " -votes:"+str(votes.text)+ " -comments:"+str(comments.text)+" \n "
        
    # driver.implicitly_wait(1)
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    # Wait to load page
    time.sleep(SCROLL_PAUSE_TIME)


        
    while True:
        try:
            # /html/body/shreddit-app/search-dynamic-id-cache-controller/div/div/div[1]/div[2]/main/div/reddit-feed/faceplate-tracker[1]/post-consume-tracker/div/div/a
            my_element = driver.find_element(By.XPATH, f"/html/body/shreddit-app/search-dynamic-id-cache-controller/div/div/div[1]/div[2]/main/div/reddit-feed/faceplate-tracker[{i}]/post-consume-tracker/div/div/a")
            # /html/body/shreddit-app/search-dynamic-id-cache-controller/div/div/div[1]/div[2]/main/div/reddit-feed/faceplate-tracker[1]/post-consume-tracker/div/div/div[2]/span[1]/faceplate-number
            comments = driver.find_element(By.XPATH, f"/html/body/shreddit-app/search-dynamic-id-cache-controller/div/div/div[1]/div[2]/main/div/reddit-feed/faceplate-tracker[{i}]/post-consume-tracker/div/div/div[2]/span[1]/faceplate-number")
            # /html/body/shreddit-app/search-dynamic-id-cache-controller/div/div/div[1]/div[2]/main/div/reddit-feed/faceplate-tracker[1]/post-consume-tracker/div/div/div[2]/span[3]/faceplate-number
            votes = driver.find_element(By.XPATH, f"/html/body/shreddit-app/search-dynamic-id-cache-controller/div/div/div[1]/div[2]/main/div/reddit-feed/faceplate-tracker[{i}]/post-consume-tracker/div/div/div[2]/span[3]/faceplate-number")
        except selenium.common.exceptions.NoSuchElementException as e:
            print('\n bad bad at - '+str(i))
            break
        i+=1
        result+="\n "+my_element.text + " -votes:"+str(votes.text)+ " -comments:"+str(comments.text)+" \n "
        
    # driver.implicitly_wait(1)
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    # Wait to load page
    time.sleep(SCROLL_PAUSE_TIME)


        
    while True:
        try:
            # /html/body/shreddit-app/search-dynamic-id-cache-controller/div/div/div[1]/div[2]/main/div/reddit-feed/faceplate-tracker[1]/post-consume-tracker/div/div/a
            my_element = driver.find_element(By.XPATH, f"/html/body/shreddit-app/search-dynamic-id-cache-controller/div/div/div[1]/div[2]/main/div/reddit-feed/faceplate-tracker[{i}]/post-consume-tracker/div/div/a")
            # /html/body/shreddit-app/search-dynamic-id-cache-controller/div/div/div[1]/div[2]/main/div/reddit-feed/faceplate-tracker[1]/post-consume-tracker/div/div/div[2]/span[1]/faceplate-number
            comments = driver.find_element(By.XPATH, f"/html/body/shreddit-app/search-dynamic-id-cache-controller/div/div/div[1]/div[2]/main/div/reddit-feed/faceplate-tracker[{i}]/post-consume-tracker/div/div/div[2]/span[1]/faceplate-number")
            # /html/body/shreddit-app/search-dynamic-id-cache-controller/div/div/div[1]/div[2]/main/div/reddit-feed/faceplate-tracker[1]/post-consume-tracker/div/div/div[2]/span[3]/faceplate-number
            votes = driver.find_element(By.XPATH, f"/html/body/shreddit-app/search-dynamic-id-cache-controller/div/div/div[1]/div[2]/main/div/reddit-feed/faceplate-tracker[{i}]/post-consume-tracker/div/div/div[2]/span[3]/faceplate-number")
        except selenium.common.exceptions.NoSuchElementException as e:
            print('\n bad bad at - '+str(i))
            break
        i+=1
        result+="\n "+my_element.text + " -votes:"+str(votes.text)+ " -comments:"+str(comments.text)+" \n "


    driver.quit()
    return result















if __name__ == '__main__':
    create_sqlite_database(db_filename)
    print(scrape_reddit_btc())