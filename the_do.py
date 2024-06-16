import sqlite3
db_filename = "my.db"
import time
import os
# pip install playwright
# then: python -m playwright install
from playwright.sync_api import sync_playwright

# headless on linux
if os.name=="posix":
    print('os.name == posix -> headless')
    headless = True
else:
    headless = False
SCROLL_PAUSE_TIME = .5

keywords = ["bitcoin", 'ethereum', 'bnb', 'solana', 'xrp', 'dogecoin', 'toncoin', 'cardano', 'shiba_inu', 'avalanche', 'tron', 'polkadot', 'bitcoin_cash', 'chainlink', 'near_protocol',
            "btc", 
            "eth",
            "binance",
            "sol",
            
            "dapps", "defi", "crypto", "cryptocurrency", "cryptocurrencies", "blockchain",
            ]

slugs = ['bitcoin', 'ethereum', 'bnb', 'solana', 'xrp', 'dogecoin', 'toncoin', 'cardano', 'shiba_inu', 'avalanche', 'tron', 'polkadot_new', 'bitcoin_cash', 'chainlink', 'near_protocol']


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
    

def create_table():
    # also deletes 'the_do'-table
    # set up table with the columns for each keyword + per crypto volume_24h/market_cap, percent_change_1h, percent_change_24h, percent_change_7d, percent_change_30d (https://pro-api.coinmarketcap.com/v2/cryptocurrency/quotes/latest)
    sql_statements = [ 
        """DROP TABLE IF EXISTS the_do;""",
        """CREATE TABLE the_do (
                id TEXT PRIMARY KEY
        );"""]
    
    execute_sql(sql_statements)
    
    sql_statements = []
    
    # - keyword
    # - - 2 hr, 12 hr, 24 hr, 7d
    # - - - headlines, texts, votes, comments, comment counts, comment votes (added)
    
    for kw in keywords:
        for interval in ["_2hr_", "_12hr_", "_24hr_", "_7d_"]:
            for col in ["headlines", "texts", "votes", "comments", "comment_counts", "comment_votes"]:
                sql_statements.append(f"""ALTER TABLE the_do ADD {str(kw)+str(interval)+str(col)} VARCHAR(65535);""")
    
    # print('sql_statements: ')
    # print(sql_statements)
    execute_sql(sql_statements)
    
    sql_statements = []
    
    for name_ in slugs:
        for interval in ["volume_24h", "percent_change_1h", "percent_change_24h", "percent_change_7d", "percent_change_30d"]:
            sql_statements.append(f"""ALTER TABLE the_do ADD {str(name_)+"_"+str(interval)} FLOAT;""")
            
    # print('sql_statements: ')
    # print(sql_statements)
    execute_sql(sql_statements)
    
    
def evaluate_one(url, xpath):
    with sync_playwright() as p:
        browser = p.chromium.launch(headless = headless)    
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

def joan_scroll(page):
    page.keyboard.press("PageDown")
    page.keyboard.press("PageDown")
    page.keyboard.press("PageDown")
    page.keyboard.press("PageDown")
    page.keyboard.press("PageDown")
    page.keyboard.press("PageDown")
    page.keyboard.press("PageDown")
    page.keyboard.press("PageDown")
    page.keyboard.press("PageDown")
    page.keyboard.press("PageDown")
    page.keyboard.press("PageDown")
    page.keyboard.press("PageDown")
    page.keyboard.press("PageDown")
    time.sleep(SCROLL_PAUSE_TIME)
    
def scroll_to_bottom(page):
    for _ in range(25):
        joan_scroll(page)
        
        
def get_search_data(page, kw):
    # return list with data to keyword search
    # posts sentiment info last 2 hours - per post: (headline, text, votes, comments, comment count, comment votes, word count) -> mean + activity info - per keyword/request: (posts count, comments count, votes count)
    # active posts sentiment info last 12 hours - per post: (headline, text, votes, comments, comment count, comment votes, word count) -> mean + activity info - per keyword/request: (posts count, comments count, votes count)
    output = []
    page.goto(f'https://www.reddit.com/search/?q={kw}&sort=new')
    
    
    
    return output
        
        
def do_the_do():
    # for all keywords, get the lists, write to table
    with sync_playwright() as p:
        browser = p.chromium.launch(headless = headless)
        context = browser.new_context(user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/116.0.0.0 Safari/537.36 Edg/116.0.1938.81")
        page = context.new_page()
    return












if __name__ == '__main__':
    create_table()

















