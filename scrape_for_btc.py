import sqlite3
db_filename = "my.db"
import time
import os
# pip install playwright
# then: python -m playwright install
from playwright.sync_api import sync_playwright
import config
# Display browser window for debugging?
debug = False
# debug = bool(config.dic['debug'])
# os.environ['PATH'] += "/home/banksy/.local/bin"
SCROLL_PAUSE_TIME = 5

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
            
            
def evaluate_one(url, xpath):
    with sync_playwright() as p:
        browser = p.chromium.launch(headless = not debug)    
        page = browser.new_page()
        page.goto (url)
        page.wait_for_load_state("networkidle")
        extract_tweet_javascript = """
            try
            {
                var xpathExpression = "$PATH";
                var element = document.evaluate (xpathExpression, document, null, XPathResult.FIRST_ORDERED_NODE_TYPE, null).singleNodeValue;
                element = element.textContent;
            }
            catch (error)
            {
                element = false;
            }
            """
        result = page.evaluate(extract_tweet_javascript.replace("$PATH", str(xpath))) 
    return result

def evaluate_in_page(page, xpath):
    # with sync_playwright() as p:
    # browser = p.chromium.launch(headless = not debug)    
    # page = browser.new_page()
    # page.goto (url)
    # page.wait_for_load_state("networkidle")
    extract_tweet_javascript = """
            try
            {
                var xpathExpression = "$PATH";
                var element = document.evaluate (xpathExpression, document, null, XPathResult.FIRST_ORDERED_NODE_TYPE, null).singleNodeValue;
                element = element.textContent;
            }
            catch (error)
            {
                element = false;
            }
            """
    result = page.evaluate(extract_tweet_javascript.replace("$PATH", str(xpath))) 
    return result

def get_search_data(kw):
    # return list with data to keyword search
    # posts sentiment info last 2 hours (headline, text, votes, comments, comment count, comment votes, word count) -> mean + activity info (posts count, comments count, votes count)
    # active posts sentiment info last 12 hours (headline, text, votes, comments, comment count, comment votes, word count) -> mean + activity info (posts count, comments count, votes count)
    
    
    output = []
    # browser = p.chromium.launch (headless = not debug)
    # driver = webdriver.Firefox()
    # driver.get(f'https://www.reddit.com/search/?q={kw}&sort=new')
    # time.sleep(SCROLL_PAUSE_TIME) # Sleep for 3 seconds
    
    return output

def scrape_reddit_btc():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless = not debug)    
        page = browser.new_page()
        page.goto('https://www.reddit.com/search/?q=bitcoin&sort=new')
        result = ''
        
        i = 1
        while True:
            # /html/body/shreddit-app/search-dynamic-id-cache-controller/div/div/div[1]/div[2]/main/div/reddit-feed/faceplate-tracker[1]/post-consume-tracker/div/div/a
            my_element = evaluate_in_page(page, f"/html/body/shreddit-app/search-dynamic-id-cache-controller/div/div/div[1]/div[2]/main/div/reddit-feed/faceplate-tracker[{i}]/post-consume-tracker/div/div/a")
            # /html/body/shreddit-app/search-dynamic-id-cache-controller/div/div/div[1]/div[2]/main/div/reddit-feed/faceplate-tracker[1]/post-consume-tracker/div/div/div[2]/span[1]/faceplate-number
            comments = evaluate_in_page(page, f"/html/body/shreddit-app/search-dynamic-id-cache-controller/div/div/div[1]/div[2]/main/div/reddit-feed/faceplate-tracker[{i}]/post-consume-tracker/div/div/div[2]/span[1]/faceplate-number")
            # /html/body/shreddit-app/search-dynamic-id-cache-controller/div/div/div[1]/div[2]/main/div/reddit-feed/faceplate-tracker[1]/post-consume-tracker/div/div/div[2]/span[3]/faceplate-number
            votes = evaluate_in_page(page, f"/html/body/shreddit-app/search-dynamic-id-cache-controller/div/div/div[1]/div[2]/main/div/reddit-feed/faceplate-tracker[{i}]/post-consume-tracker/div/div/div[2]/span[3]/faceplate-number")
                       
            if my_element == False:
                print('\n bad bad at - '+str(i))
                break
            i+=1
            result+="\n "+str(my_element)+ " -votes:"+str(votes)+ " -comments:"+str(comments)+" \n "
            if i%5 == 1:
                page.keyboard.press("PageDown")
            
        page.keyboard.press("PageDown")
        page.keyboard.press("PageDown")
        page.keyboard.press("PageDown")
        page.keyboard.press("PageDown")
        page.keyboard.press("PageDown")
        page.keyboard.press("PageDown")
        time.sleep(SCROLL_PAUSE_TIME)

        while True:
            # /html/body/shreddit-app/search-dynamic-id-cache-controller/div/div/div[1]/div[2]/main/div/reddit-feed/faceplate-tracker[1]/post-consume-tracker/div/div/a
            my_element = evaluate_in_page(page, f"/html/body/shreddit-app/search-dynamic-id-cache-controller/div/div/div[1]/div[2]/main/div/reddit-feed/faceplate-tracker[{i}]/post-consume-tracker/div/div/a")
            # /html/body/shreddit-app/search-dynamic-id-cache-controller/div/div/div[1]/div[2]/main/div/reddit-feed/faceplate-tracker[1]/post-consume-tracker/div/div/div[2]/span[1]/faceplate-number
            comments = evaluate_in_page(page, f"/html/body/shreddit-app/search-dynamic-id-cache-controller/div/div/div[1]/div[2]/main/div/reddit-feed/faceplate-tracker[{i}]/post-consume-tracker/div/div/div[2]/span[1]/faceplate-number")
            # /html/body/shreddit-app/search-dynamic-id-cache-controller/div/div/div[1]/div[2]/main/div/reddit-feed/faceplate-tracker[1]/post-consume-tracker/div/div/div[2]/span[3]/faceplate-number
            votes = evaluate_in_page(page, f"/html/body/shreddit-app/search-dynamic-id-cache-controller/div/div/div[1]/div[2]/main/div/reddit-feed/faceplate-tracker[{i}]/post-consume-tracker/div/div/div[2]/span[3]/faceplate-number")
            if my_element == False:
                print('\n bad bad at - '+str(i))
                break
            i+=1
            result+="\n "+str(my_element)+ " -votes:"+str(votes)+ " -comments:"+str(comments)+" \n "
            if i%5 == 1:
                page.keyboard.press("PageDown")
            
        page.keyboard.press("PageDown")
        page.keyboard.press("PageDown")
        page.keyboard.press("PageDown")
        page.keyboard.press("PageDown")
        page.keyboard.press("PageDown")
        page.keyboard.press("PageDown")
        time.sleep(SCROLL_PAUSE_TIME)

        while True:
            # /html/body/shreddit-app/search-dynamic-id-cache-controller/div/div/div[1]/div[2]/main/div/reddit-feed/faceplate-tracker[1]/post-consume-tracker/div/div/a
            my_element = evaluate_in_page(page, f"/html/body/shreddit-app/search-dynamic-id-cache-controller/div/div/div[1]/div[2]/main/div/reddit-feed/faceplate-tracker[{i}]/post-consume-tracker/div/div/a")
            # /html/body/shreddit-app/search-dynamic-id-cache-controller/div/div/div[1]/div[2]/main/div/reddit-feed/faceplate-tracker[1]/post-consume-tracker/div/div/div[2]/span[1]/faceplate-number
            comments = evaluate_in_page(page, f"/html/body/shreddit-app/search-dynamic-id-cache-controller/div/div/div[1]/div[2]/main/div/reddit-feed/faceplate-tracker[{i}]/post-consume-tracker/div/div/div[2]/span[1]/faceplate-number")
            # /html/body/shreddit-app/search-dynamic-id-cache-controller/div/div/div[1]/div[2]/main/div/reddit-feed/faceplate-tracker[1]/post-consume-tracker/div/div/div[2]/span[3]/faceplate-number
            votes = evaluate_in_page(page, f"/html/body/shreddit-app/search-dynamic-id-cache-controller/div/div/div[1]/div[2]/main/div/reddit-feed/faceplate-tracker[{i}]/post-consume-tracker/div/div/div[2]/span[3]/faceplate-number")
                       
            if my_element == False:
                print('\n bad bad at - '+str(i))
                break
            i+=1
            result+="\n "+str(my_element)+ " -votes:"+str(votes)+ " -comments:"+str(comments)+" \n "
            if i%5 == 1:
                page.keyboard.press("PageDown")

        page.keyboard.press("PageDown")
        page.keyboard.press("PageDown")
        page.keyboard.press("PageDown")
        page.keyboard.press("PageDown")
        page.keyboard.press("PageDown")
        page.keyboard.press("PageDown")
        time.sleep(SCROLL_PAUSE_TIME)
            
        while True:
            # /html/body/shreddit-app/search-dynamic-id-cache-controller/div/div/div[1]/div[2]/main/div/reddit-feed/faceplate-tracker[1]/post-consume-tracker/div/div/a
            my_element = evaluate_in_page(page, f"/html/body/shreddit-app/search-dynamic-id-cache-controller/div/div/div[1]/div[2]/main/div/reddit-feed/faceplate-tracker[{i}]/post-consume-tracker/div/div/a")
            # /html/body/shreddit-app/search-dynamic-id-cache-controller/div/div/div[1]/div[2]/main/div/reddit-feed/faceplate-tracker[1]/post-consume-tracker/div/div/div[2]/span[1]/faceplate-number
            comments = evaluate_in_page(page, f"/html/body/shreddit-app/search-dynamic-id-cache-controller/div/div/div[1]/div[2]/main/div/reddit-feed/faceplate-tracker[{i}]/post-consume-tracker/div/div/div[2]/span[1]/faceplate-number")
            # /html/body/shreddit-app/search-dynamic-id-cache-controller/div/div/div[1]/div[2]/main/div/reddit-feed/faceplate-tracker[1]/post-consume-tracker/div/div/div[2]/span[3]/faceplate-number
            votes = evaluate_in_page(page, f"/html/body/shreddit-app/search-dynamic-id-cache-controller/div/div/div[1]/div[2]/main/div/reddit-feed/faceplate-tracker[{i}]/post-consume-tracker/div/div/div[2]/span[3]/faceplate-number")  
            if my_element == False:
                print('\n bad bad at - '+str(i))
                break
            i+=1
            result+="\n "+str(my_element)+ " -votes:"+str(votes)+ " -comments:"+str(comments)+" \n "
            if i%5 == 1:
                page.keyboard.press("PageDown")
            
        page.keyboard.press("PageDown")
        page.keyboard.press("PageDown")
        page.keyboard.press("PageDown")
        page.keyboard.press("PageDown")
        page.keyboard.press("PageDown")
        page.keyboard.press("PageDown")
        time.sleep(SCROLL_PAUSE_TIME)
            
        while True:
            # /html/body/shreddit-app/search-dynamic-id-cache-controller/div/div/div[1]/div[2]/main/div/reddit-feed/faceplate-tracker[1]/post-consume-tracker/div/div/a
            my_element = evaluate_in_page(page, f"/html/body/shreddit-app/search-dynamic-id-cache-controller/div/div/div[1]/div[2]/main/div/reddit-feed/faceplate-tracker[{i}]/post-consume-tracker/div/div/a")
            # /html/body/shreddit-app/search-dynamic-id-cache-controller/div/div/div[1]/div[2]/main/div/reddit-feed/faceplate-tracker[1]/post-consume-tracker/div/div/div[2]/span[1]/faceplate-number
            comments = evaluate_in_page(page, f"/html/body/shreddit-app/search-dynamic-id-cache-controller/div/div/div[1]/div[2]/main/div/reddit-feed/faceplate-tracker[{i}]/post-consume-tracker/div/div/div[2]/span[1]/faceplate-number")
            # /html/body/shreddit-app/search-dynamic-id-cache-controller/div/div/div[1]/div[2]/main/div/reddit-feed/faceplate-tracker[1]/post-consume-tracker/div/div/div[2]/span[3]/faceplate-number
            votes = evaluate_in_page(page, f"/html/body/shreddit-app/search-dynamic-id-cache-controller/div/div/div[1]/div[2]/main/div/reddit-feed/faceplate-tracker[{i}]/post-consume-tracker/div/div/div[2]/span[3]/faceplate-number")
            if my_element == False:
                print('\n bad bad at - '+str(i))
                break
            i+=1
            result+="\n "+str(my_element)+ " -votes:"+str(votes)+ " -comments:"+str(comments)+" \n "
            if i%5 == 1:
                page.keyboard.press("PageDown")

        page.keyboard.press("PageDown")
        page.keyboard.press("PageDown")
        page.keyboard.press("PageDown")
        page.keyboard.press("PageDown")
        page.keyboard.press("PageDown")
        page.keyboard.press("PageDown")
        time.sleep(SCROLL_PAUSE_TIME)
            
        while True:
            # /html/body/shreddit-app/search-dynamic-id-cache-controller/div/div/div[1]/div[2]/main/div/reddit-feed/faceplate-tracker[1]/post-consume-tracker/div/div/a
            my_element = evaluate_in_page(page, f"/html/body/shreddit-app/search-dynamic-id-cache-controller/div/div/div[1]/div[2]/main/div/reddit-feed/faceplate-tracker[{i}]/post-consume-tracker/div/div/a")
            # /html/body/shreddit-app/search-dynamic-id-cache-controller/div/div/div[1]/div[2]/main/div/reddit-feed/faceplate-tracker[1]/post-consume-tracker/div/div/div[2]/span[1]/faceplate-number
            comments = evaluate_in_page(page, f"/html/body/shreddit-app/search-dynamic-id-cache-controller/div/div/div[1]/div[2]/main/div/reddit-feed/faceplate-tracker[{i}]/post-consume-tracker/div/div/div[2]/span[1]/faceplate-number")
            # /html/body/shreddit-app/search-dynamic-id-cache-controller/div/div/div[1]/div[2]/main/div/reddit-feed/faceplate-tracker[1]/post-consume-tracker/div/div/div[2]/span[3]/faceplate-number
            votes = evaluate_in_page(page, f"/html/body/shreddit-app/search-dynamic-id-cache-controller/div/div/div[1]/div[2]/main/div/reddit-feed/faceplate-tracker[{i}]/post-consume-tracker/div/div/div[2]/span[3]/faceplate-number")
            
            if my_element == False:
                print('\n bad bad at - '+str(i))
                break
            i+=1
            result+="\n "+str(my_element)+ " -votes:"+str(votes)+ " -comments:"+str(comments)+" \n "
            if i%5 == 1:
                page.keyboard.press("PageDown")


        page.keyboard.press("PageDown")
        page.keyboard.press("PageDown")
        page.keyboard.press("PageDown")
        page.keyboard.press("PageDown")
        page.keyboard.press("PageDown")
        page.keyboard.press("PageDown")
        time.sleep(SCROLL_PAUSE_TIME)
            
        while True:
            # /html/body/shreddit-app/search-dynamic-id-cache-controller/div/div/div[1]/div[2]/main/div/reddit-feed/faceplate-tracker[1]/post-consume-tracker/div/div/a
            my_element = evaluate_in_page(page, f"/html/body/shreddit-app/search-dynamic-id-cache-controller/div/div/div[1]/div[2]/main/div/reddit-feed/faceplate-tracker[{i}]/post-consume-tracker/div/div/a")
            # /html/body/shreddit-app/search-dynamic-id-cache-controller/div/div/div[1]/div[2]/main/div/reddit-feed/faceplate-tracker[1]/post-consume-tracker/div/div/div[2]/span[1]/faceplate-number
            comments = evaluate_in_page(page, f"/html/body/shreddit-app/search-dynamic-id-cache-controller/div/div/div[1]/div[2]/main/div/reddit-feed/faceplate-tracker[{i}]/post-consume-tracker/div/div/div[2]/span[1]/faceplate-number")
            # /html/body/shreddit-app/search-dynamic-id-cache-controller/div/div/div[1]/div[2]/main/div/reddit-feed/faceplate-tracker[1]/post-consume-tracker/div/div/div[2]/span[3]/faceplate-number
            votes = evaluate_in_page(page, f"/html/body/shreddit-app/search-dynamic-id-cache-controller/div/div/div[1]/div[2]/main/div/reddit-feed/faceplate-tracker[{i}]/post-consume-tracker/div/div/div[2]/span[3]/faceplate-number")
            
            if my_element == False:
                print('\n bad bad at - '+str(i))
                break
            i+=1
            result+="\n "+str(my_element)+ " -votes:"+str(votes)+ " -comments:"+str(comments)+" \n "
            if i%5 == 1:
                page.keyboard.press("PageDown")

        page.keyboard.press("PageDown")
        page.keyboard.press("PageDown")
        page.keyboard.press("PageDown")
        page.keyboard.press("PageDown")
        page.keyboard.press("PageDown")
        page.keyboard.press("PageDown")
        time.sleep(SCROLL_PAUSE_TIME)
            
        while True:
            # /html/body/shreddit-app/search-dynamic-id-cache-controller/div/div/div[1]/div[2]/main/div/reddit-feed/faceplate-tracker[1]/post-consume-tracker/div/div/a
            my_element = evaluate_in_page(page, f"/html/body/shreddit-app/search-dynamic-id-cache-controller/div/div/div[1]/div[2]/main/div/reddit-feed/faceplate-tracker[{i}]/post-consume-tracker/div/div/a")
            # /html/body/shreddit-app/search-dynamic-id-cache-controller/div/div/div[1]/div[2]/main/div/reddit-feed/faceplate-tracker[1]/post-consume-tracker/div/div/div[2]/span[1]/faceplate-number
            comments = evaluate_in_page(page, f"/html/body/shreddit-app/search-dynamic-id-cache-controller/div/div/div[1]/div[2]/main/div/reddit-feed/faceplate-tracker[{i}]/post-consume-tracker/div/div/div[2]/span[1]/faceplate-number")
            # /html/body/shreddit-app/search-dynamic-id-cache-controller/div/div/div[1]/div[2]/main/div/reddit-feed/faceplate-tracker[1]/post-consume-tracker/div/div/div[2]/span[3]/faceplate-number
            votes = evaluate_in_page(page, f"/html/body/shreddit-app/search-dynamic-id-cache-controller/div/div/div[1]/div[2]/main/div/reddit-feed/faceplate-tracker[{i}]/post-consume-tracker/div/div/div[2]/span[3]/faceplate-number")
            
            if my_element == False:
                print('\n bad bad at - '+str(i))
                break
            i+=1
            result+="\n "+str(my_element)+ " -votes:"+str(votes)+ " -comments:"+str(comments)+" \n "
            if i%5 == 1:
                page.keyboard.press("PageDown")
    return result















if __name__ == '__main__':
    create_sqlite_database(db_filename)
    print(scrape_reddit_btc())