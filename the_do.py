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
            
            "dapps", "defi", "crypto", "cryptocurrency", "blockchain", "web3", "ledger"
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
    # - - - headlines, texts, votes, comments, comment counts, comment votes
    
    for kw in keywords:
        for interval in ["_2hr_", "_12hr_", "_24hr_", "_7d_"]:
            for col in ["headlines", "texts", "votes", "comments", "comment_counts", "comment_votes"]:
                sql_statements.append(f"""ALTER TABLE the_do ADD {str(kw)+str(interval)+str(col)} VARCHAR(65535);""")
    
    # print('sql_statements: ')
    # print(sql_statements)
    execute_sql(sql_statements)
    
    sql_statements = []
    
    # - token
    # - - "volume_24h", "percent_change_1h", "percent_change_24h", "percent_change_7d", "percent_change_30d"
    
    for name_ in slugs:
        for interval in ["volume_24h", "percent_change_1h", "percent_change_24h", "percent_change_7d", "percent_change_30d"]:
            sql_statements.append(f"""ALTER TABLE the_do ADD {str(name_)+"_"+str(interval)} FLOAT;""")
            
    # print('sql_statements: ')
    # print(sql_statements)
    execute_sql(sql_statements)

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

    page.goto(f'https://www.reddit.com/search/?q={kw}')
    scroll_to_bottom(page)
    
    # - keyword
    # - - 2 hr, 12 hr, 24 hr, 7d
    # - - - headlines, texts, votes, comments, comment counts, comment votes
    
    output = []
    headlines = ""
    texts = ""
    votes = ""
    comments = ""
    comment_counts = ""
    comments_votes = ""

    result = ''
    i = 1
    while True:
        # /html/body/shreddit-app/search-dynamic-id-cache-controller/div/div/div[1]/div[2]/main/div/reddit-feed/faceplate-tracker[1]/post-consume-tracker/div/div/a
        my_element = evaluate_in_page(page, f"/html/body/shreddit-app/search-dynamic-id-cache-controller/div/div/div[1]/div[2]/main/div/reddit-feed/faceplate-tracker[{i}]/post-consume-tracker/div/div/a")
        # /html/body/shreddit-app/search-dynamic-id-cache-controller/div/div/div[1]/div[2]/main/div/reddit-feed/faceplate-tracker[1]/post-consume-tracker/div/div/div[2]/span[1]/faceplate-number
        comments_  = evaluate_in_page(page, f"/html/body/shreddit-app/search-dynamic-id-cache-controller/div/div/div[1]/div[2]/main/div/reddit-feed/faceplate-tracker[{i}]/post-consume-tracker/div/div/div[2]/span[1]/faceplate-number")
        # /html/body/shreddit-app/search-dynamic-id-cache-controller/div/div/div[1]/div[2]/main/div/reddit-feed/faceplate-tracker[1]/post-consume-tracker/div/div/div[2]/span[3]/faceplate-number
        votes_ = evaluate_in_page(page, f"/html/body/shreddit-app/search-dynamic-id-cache-controller/div/div/div[1]/div[2]/main/div/reddit-feed/faceplate-tracker[{i}]/post-consume-tracker/div/div/div[2]/span[3]/faceplate-number")
        
        # /html/body/shreddit-app/search-dynamic-id-cache-controller/div/div/div[1]/div[2]/main/div/reddit-feed/faceplate-tracker[1]/post-consume-tracker/div/div/div[1]/span/faceplate-timeago/time
        time = evaluate_in_page(page, f"/html/body/shreddit-app/search-dynamic-id-cache-controller/div/div/div[1]/div[2]/main/div/reddit-feed/faceplate-tracker[{i}]/post-consume-tracker/div/div/div[1]/span/faceplate-timeago/time")
        # time = time.datetime
        
        if time.endswith("ago"):
            # english
            time = time[:-4]
        elif time.startswith("vor"):
            # german
            time = time[4:]
            time.replace(" Std", "h")
            time.replace(" m", "m")
            time.replace(" Tagen", "d")
            time.replace(" Tag", "d")
            time.replace(" Monaten", "mo")
            time.replace(" Monat", "mo")
            time.replace(" Jahren", "y")
            time.replace(" Jahr", "y")
        print("time: "+str(time))
        if my_element == False:
            print('\n bad bad at - '+str(i))
            break
        i+=1
        result+="\n "+str(my_element)+ " -votes:"+str(votes_)+ " -comments:"+str(comments_)+" \n "
        if i%5 == 1:
            page.keyboard.press("PageDown")
            page.keyboard.press("PageDown")
            page.keyboard.press("PageDown")
            page.keyboard.press("PageDown")
            page.keyboard.press("PageDown")
            page.keyboard.press("PageDown")
    return output
        
def do_the_do():
    # for all keywords, get the lists + price-change data per token -> write to table
    with sync_playwright() as p:
        browser = p.chromium.launch(headless = headless)
        context = browser.new_context(user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/116.0.0.0 Safari/537.36 Edg/116.0.1938.81")
        page = context.new_page()
        get_search_data(page, "dogecoin")
    return












if __name__ == '__main__':
    create_table()
    do_the_do()

















