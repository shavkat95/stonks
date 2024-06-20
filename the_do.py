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

# headless = False #debugging on mac

SCROLL_PAUSE_TIME = .001

keywords = ["bitcoin", 'ethereum', 'bnb', 'solana', 'xrp', 'dogecoin', 'toncoin', 'cardano', 'shiba_inu', 'avalanche', 'tron', 'polkadot', 'bitcoin_cash', 'chainlink', 'near_protocol',
            "btc", 
            "eth",
            "sol",
            
            "coin_exchange","crypto_exchange","binance", "coinbase", "OKX" "coinbase_exchange", "bybit", "Upbit", "Kraken", "Gate_io_Exchange", "HTX", "Bitfinex", "KuCoin", "MEXC_Exchange", "Bitget", "Crypto_com_Exchange", "Binance_TR", "BingX", 
            
            "dapps", "defi", "crypto", "cryptocurrency", "blockchain", "web3", "ledger", "satoshi", "satoshis", "meme_coin", "meme_coins", "token_dominance", "on_chain"
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
                id TEXT
        );"""]
    
    execute_sql(sql_statements)
    
    sql_statements = [ 
        """CREATE UNIQUE INDEX idx ON the_do (id)""",] # not sure about best practices here
    
    execute_sql(sql_statements)
    
    sql_statements = []
    
    # - keyword
    # - - 2 hr, 12 hr, 24 hr, 7d
    # - - - headlines, texts, votes, comments, comment counts, comment votes
    
    for kw in keywords:
        for interval in ["_2hr_", "_12hr_", "_3d_", "_7d_", "_mo_"]:
            for col in ["headlines", "texts", "votes", "comments", "comment_counts", "comment_votes"]:
                sql_statements.append(f"""ALTER TABLE the_do ADD {str(kw)+str(interval)+str(col)} TEXT;""")
    
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

def get_comment_votes(page, i, j = False, k = False, l = False, m = False):
    # document.querySelector("#comment-tree > shreddit-comment:nth-child(2) > shreddit-comment > shreddit-comment-action-row").shadowRoot.querySelector("div > div > span > span > faceplate-number")
    if not j:
        jsPath = "#comment-tree > shreddit-comment:nth-child($I) > shreddit-comment-action-row".replace("$I", str(i+1))
    elif not k:
        jsPath = "#comment-tree > shreddit-comment:nth-child($I) > shreddit-comment:nth-child($J) > shreddit-comment-action-row"
        if j == 1:
            jsPath = jsPath.replace(":nth-child($J)", "")
        jsPath = jsPath.replace("$I", str(i+1)).replace("$J", str(j))
    elif not l:
        jsPath = "#comment-tree > shreddit-comment:nth-child($I) > shreddit-comment:nth-child($J) > shreddit-comment:nth-child($K) > shreddit-comment-action-row"
        if j == 1:
            jsPath = jsPath.replace(":nth-child($J)", "")
        if k == 1:
            jsPath = jsPath.replace(":nth-child($K)", "")
        jsPath = jsPath.replace("$I", str(i+1)).replace("$J", str(j)).replace("$K", str(k))
    elif not m:
        jsPath = "#comment-tree > shreddit-comment:nth-child($I) > shreddit-comment:nth-child($J) > shreddit-comment:nth-child($K) > shreddit-comment:nth-child($L) > shreddit-comment-action-row"
        if j == 1:
            jsPath = jsPath.replace(":nth-child($J)", "")
        if k == 1:
            jsPath = jsPath.replace(":nth-child($K)", "")
        if l == 1:
            jsPath = jsPath.replace(":nth-child($L)", "")
        jsPath = jsPath.replace("$I", str(i+1)).replace("$J", str(j)).replace("$K", str(k)).replace("$L", str(l))
    elif m:
        jsPath = "#comment-tree > shreddit-comment:nth-child($I) > shreddit-comment:nth-child($J) > shreddit-comment:nth-child($K) > shreddit-comment:nth-child($L) > shreddit-comment:nth-child($M) > shreddit-comment-action-row"
        if j == 1:
            jsPath = jsPath.replace(":nth-child($J)", "")
        if k == 1:
            jsPath = jsPath.replace(":nth-child($K)", "")
        if l == 1:
            jsPath = jsPath.replace(":nth-child($L)", "")
        if m == 1:
            jsPath = jsPath.replace(":nth-child($M)", "")
        jsPath = jsPath.replace("$I", str(i+1)).replace("$J", str(j)).replace("$K", str(k)).replace("$L", str(l)).replace("$M", str(m))
    
    extract_tweet_javascript = """
        try
        {
            var jsPath = "$jsPath";
            var element = document.querySelector(jsPath).shadowRoot.querySelector("div > div > span > span > faceplate-number")
            element = element.textContent;
        }
        catch (error)
        {
            element = false;
        }
        """
    result = page.evaluate(extract_tweet_javascript.replace("$jsPath", jsPath)) 
    return result

def juan_scroll(page):
    page.keyboard.press("PageDown")
    page.keyboard.press("PageDown")
    page.keyboard.press("PageDown")
    page.keyboard.press("PageDown")
    page.keyboard.press("PageDown")
    page.keyboard.press("PageDown")
    page.keyboard.press("PageDown")
    page.keyboard.press("PageDown")
    page.wait_for_load_state('domcontentloaded')
    time.sleep(SCROLL_PAUSE_TIME)
    page.keyboard.press("PageDown")
    page.keyboard.press("PageDown")
    page.keyboard.press("PageDown")
    page.keyboard.press("PageDown")
    page.keyboard.press("PageDown")
    page.keyboard.press("PageDown")
    page.keyboard.press("PageDown")
    page.keyboard.press("PageDown")
    page.wait_for_load_state('domcontentloaded')
    time.sleep(SCROLL_PAUSE_TIME)

def scroll_to_bottom(page):
    for _ in range(5):
        juan_scroll(page)
    time.sleep(SCROLL_PAUSE_TIME)

def read_comments(page):
    comments = ""
    comments_votes = 0
    # /html/body/shreddit-app/div/div[1]/div/main/div/faceplate-batch/shreddit-comment-tree/shreddit-comment[1]/div[3]
    # /html/body/shreddit-app/div/div[1]/div/main/div/faceplate-batch/shreddit-comment-tree/shreddit-comment[2]/div[3]
    # /html/body/shreddit-app/div/div[1]/div/main/div/faceplate-batch/shreddit-comment-tree/shreddit-comment[3]/div[3]
    # /html/body/shreddit-app/div/div[1]/div/main/div/faceplate-batch/shreddit-comment-tree/shreddit-comment[3]/shreddit-comment/div[3] # nested once
    # ...
    # /html/body/shreddit-app/div/div[1]/div/main/div/faceplate-batch/shreddit-comment-tree/shreddit-comment[7]/div[3]
    # /html/body/shreddit-app/div/div[1]/div/main/div/faceplate-batch/shreddit-comment-tree/shreddit-comment[7]/shreddit-comment[1]/div[3] # nested once
    # /html/body/shreddit-app/div/div[1]/div/main/div/faceplate-batch/shreddit-comment-tree/shreddit-comment[7]/shreddit-comment[2]/div[3] # nested once
    # ...
    # /html/body/shreddit-app/div/div[1]/div/main/div/faceplate-batch/shreddit-comment-tree/shreddit-comment[17]/div[3]
    # /html/body/shreddit-app/div/div[1]/div/main/div/faceplate-batch/shreddit-comment-tree/shreddit-comment[17]/shreddit-comment[1]/div[3] # nested once
    # /html/body/shreddit-app/div/div[1]/div/main/div/faceplate-batch/shreddit-comment-tree/shreddit-comment[17]/shreddit-comment[2]/div[3] # nested once
    # /html/body/shreddit-app/div/div[1]/div/main/div/faceplate-batch/shreddit-comment-tree/shreddit-comment[17]/shreddit-comment[2]/shreddit-comment/div[3] # nested twice
    base_XPath = "/html/body/shreddit-app/div/div[1]/div/main/div/faceplate-batch/shreddit-comment-tree/shreddit-comment[$index]"
    shreddit = "/shreddit-comment[$index]"
    for i in range(1, 100):
        if i%6 == 5:
            scroll_to_bottom(page)
        current_comment = evaluate_in_page(page, base_XPath.replace('$index', str(i))+'/div[3]')
        if current_comment == False:
            break
        if i == 1 and "I am a bot, and this action was performed automatically. Please contact the moderators of this subreddit if you have any questions or concerns." in current_comment:
            continue
        current_vote = get_comment_votes(page, i=i)
        if i == 1 and current_vote == False:
            continue
        if str(current_vote).isdigit():
            current_vote = abs(int(current_vote))
            comments_votes += current_vote
        comments += '\n'+current_comment.replace("\n", "").replace("                ", "")
        for j in range(1, 50):
            current_comment = evaluate_in_page(page, base_XPath.replace('$index', str(i))+shreddit.replace('$index', str(j))+'/div[3]')
            if current_comment == False:
                break
            current_vote = get_comment_votes(page, i=i, j=j)
            if str(current_vote).isdigit():
                current_vote = abs(int(current_vote))
                comments_votes += current_vote  
            comments += '\n >'+current_comment.replace("\n", "").replace("                ", "")
            for k in range(1, 50):
                current_comment = evaluate_in_page(page, base_XPath.replace('$index', str(i))+shreddit.replace('$index', str(j))+shreddit.replace('$index', str(k))+'/div[3]')
                if current_comment == False:
                    break
                current_vote = get_comment_votes(page, i=i, j=j, k=k)
                if str(current_vote).isdigit():
                    current_vote = abs(int(current_vote))
                    comments_votes += current_vote
                comments += '\n > >'+current_comment.replace("\n", "").replace("                ", "")
                for l in range(1, 50):
                    current_comment = evaluate_in_page(page, base_XPath.replace('$index', str(i))+shreddit.replace('$index', str(j))+shreddit.replace('$index', str(k))+shreddit.replace('$index', str(l))+'/div[3]')
                    if current_comment == False:
                        break
                    current_vote = get_comment_votes(page, i=i, j=j, k=k, l=l)
                    if str(current_vote).isdigit():
                        current_vote = abs(int(current_vote))
                        comments_votes += current_vote
                    comments += '\n > > >'+current_comment.replace("\n", "").replace("                ", "")
                    for m in range(1, 50):
                        current_comment = evaluate_in_page(page, base_XPath.replace('$index', str(i))+shreddit.replace('$index', str(j))+shreddit.replace('$index', str(k))+shreddit.replace('$index', str(l))+shreddit.replace('$index', str(m))+'/div[3]')
                        if current_comment == False:
                            break
                        current_vote = get_comment_votes(page, i=i, j=j, k=k, l=l, m=m)
                        if str(current_vote).isdigit():
                            current_vote = abs(int(current_vote))
                            comments_votes += current_vote
                        comments += '\n > > > >'+current_comment.replace("\n", "").replace("                ", "")
    
    
    return [comments, comments_votes]

def scrape_post(context, url):
    # print(url)
    
    try:
        page = context.new_page()
        page.wait_for_load_state('domcontentloaded')
        page.goto(url)
        scroll_to_bottom(page)
    except:
        print('ups 1 '+url)
        return "ups_1"
            
    # see if loaded correctly
    error_div = evaluate_in_page(page, "//shreddit-forbidden")
    if error_div:
        if error_div:
            print('ups 2 | error_div appeared | '+url)
        return 'try_again'
    
    scroll_to_bottom(page)
    
    # post text
    post_text = evaluate_in_page(page, f"/html/body/shreddit-app/div/div[1]/div/main/shreddit-post/div[2]/div/div/p")
    if post_text == False: 
        post_text = ""
    post_text = post_text.strip()
        
    # post comments
    [post_comments, comments_votes] = read_comments(page)
    
    page.close()
    return [post_text, post_comments, comments_votes]

def one_search_page(context, page, PAUSE_TIME = 0):
    scroll_to_bottom(page)
    
    # - keyword
    # - - 2 hr, 12 hr, 24 hr, 7d
    # - - - headlines, texts, votes, comments, comment_counts, comment_votes
    
    hr2 = {"headlines": "", "texts": "", "votes": "", "comments": "", "comment_counts": "", "comment_votes": ""}
    hr12 = {"headlines": "", "texts": "", "votes": "", "comments": "", "comment_counts": "", "comment_votes": ""}
    hr24 = {"headlines": "", "texts": "", "votes": "", "comments": "", "comment_counts": "", "comment_votes": ""}
    d7 = {"headlines": "", "texts": "", "votes": "", "comments": "", "comment_counts": "", "comment_votes": ""}
    mo = {"headlines": "", "texts": "", "votes": "", "comments": "", "comment_counts": "", "comment_votes": ""}

    i = 1
    while True:
        # /html/body/shreddit-app/search-dynamic-id-cache-controller/div/div/div[1]/div[2]/main/div/reddit-feed/faceplate-tracker[1]/post-consume-tracker/div/div/a
        headline = evaluate_in_page(page, f"/html/body/shreddit-app/search-dynamic-id-cache-controller/div/div/div[1]/div[2]/main/div/reddit-feed/faceplate-tracker[{i}]/post-consume-tracker/div/div/a")
        if headline == False:
            # print('\n bad bad at - '+str(i))
            break
        headline = headline.strip()
        # /html/body/shreddit-app/search-dynamic-id-cache-controller/div/div/div[1]/div[2]/main/div/reddit-feed/faceplate-tracker[1]/post-consume-tracker/div/div/div[2]/span[1]/faceplate-number
        num_comments  = evaluate_in_page(page, f"/html/body/shreddit-app/search-dynamic-id-cache-controller/div/div/div[1]/div[2]/main/div/reddit-feed/faceplate-tracker[{i}]/post-consume-tracker/div/div/div[2]/span[1]/faceplate-number")
        if "K" in num_comments: #for the english
            num_comments = num_comments.replace("K", "")
            num_comments = float(num_comments)
            num_comments = num_comments * 1000
            try:
                num_comments = int(num_comments)
            except ValueError: # this makes no sense to me, maybe there's a big here?
                num_comments = num_comments.replace(".", "")
                num_comments = int(num_comments)
        else:
            num_comments = int(num_comments.replace(".", ""))
        # /html/body/shreddit-app/search-dynamic-id-cache-controller/div/div/div[1]/div[2]/main/div/reddit-feed/faceplate-tracker[1]/post-consume-tracker/div/div/div[2]/span[3]/faceplate-number
        num_votes = evaluate_in_page(page, f"/html/body/shreddit-app/search-dynamic-id-cache-controller/div/div/div[1]/div[2]/main/div/reddit-feed/faceplate-tracker[{i}]/post-consume-tracker/div/div/div[2]/span[3]/faceplate-number")
        if "K" in num_votes: #for the english
            num_votes = num_votes.replace("K", "")
            num_votes = float(num_votes)
            num_votes = num_votes * 1000
            try:
                num_votes = int(num_votes)
            except ValueError: # this makes no sense to me, maybe there's a big here?
                num_votes = num_votes.replace(".", "")
                num_votes = int(num_votes)
        else:
            num_votes = int(num_votes.replace(".", ""))
        # /html/body/shreddit-app/search-dynamic-id-cache-controller/div/div/div[1]/div[2]/main/div/reddit-feed/faceplate-tracker[1]/post-consume-tracker/div/div/div[1]/span/faceplate-timeago/time
        time_ago = evaluate_in_page(page, f"/html/body/shreddit-app/search-dynamic-id-cache-controller/div/div/div[1]/div[2]/main/div/reddit-feed/faceplate-tracker[{i}]/post-consume-tracker/div/div/div[1]/span/faceplate-timeago/time")
        
        post_link = page.locator(f'xpath=/html/body/shreddit-app/search-dynamic-id-cache-controller/div/div/div[1]/div[2]/main/div/reddit-feed/faceplate-tracker[{i}]/post-consume-tracker/div/faceplate-tracker/h2/a').get_attribute('href')
        post_link = "https://www.reddit.com"+str(post_link)
        
        
        pages = context.pages
        if len(pages) > 1:
            for k in range(1, len(pages)):
                pages[k].close()
        
        # print(str(i)+' | '+post_link)
        scrape_output =  scrape_post(context, post_link)
        
        if scrape_output == "ups_1":
            print('ups_1 ')
            ulr_1 = page.url
            close_context(context)
            page = context.new_page()
            page.goto(ulr_1)
            scroll_to_bottom(page)
            scroll_to_bottom(page)
            scroll_to_bottom(page)
            # return 'try_again'
            
        
        # for when need to slow down
        time.sleep(PAUSE_TIME)
        
        j = 0
        while scrape_output == "try_again" and j<15: # it's bugged idk
            print('j: '+str(j))
            time.sleep(j)
            scroll_to_bottom(page)
            time.sleep(j)
            scrape_output =  scrape_post(context, post_link)
            if scrape_output != "try_again":
                print('fixed ups '+post_link)
            elif j > 4:
                url_1 = page.url
                close_context(context)
                page = context.new_page()
                page.goto(url_1)
                scroll_to_bottom(page)
                scroll_to_bottom(page)
                scroll_to_bottom(page)
            j+=1
            
        
        if scrape_output == "try_again":
            print('oopsie at '+post_link)
            return 'try_again'
        
        [post_text, post_comments, comments_votes] = scrape_output
        
        # considering only active older posts 
        activity = int(float(num_comments))+int(float(num_comments))
        
        # we work with text-value instead of original datetime:
        if time_ago != False:
            time_ago = str(time_ago)
            if time_ago.endswith("ago"):
                # english
                time_ago = time_ago[:-4]
                time_ago = time_ago.replace(" ", "")
            elif time_ago.startswith("vor"):
                # german
                time_ago = time_ago[4:]
                time_ago = time_ago.replace(" Std", "h")
                time_ago = time_ago.replace(" m", "m")
                time_ago = time_ago.replace(" Tagen", "d")
                time_ago = time_ago.replace(" Tag", "d")
                time_ago = time_ago.replace(" Monaten", "mo")
                time_ago = time_ago.replace(" Monat", "mo")
                time_ago = time_ago.replace(" Jahren", "y")
                time_ago = time_ago.replace(" Jahr", "y")
                time_ago = time_ago.replace(".", "")
                time_ago = time_ago.replace(" ", "")
        
        # output logic
        if time_ago.endswith("d"):
            if activity > 5:
                d7["headlines"]+=headline + " | "
                d7["texts"]+=post_text + " | "
                d7["votes"]+=str(num_votes) + " | "
                d7["comments"]+=post_comments + " | "
                d7["comment_counts"]+=str(num_comments) + " | "
                d7["comment_votes"]+=str(comments_votes) + " | "
        elif time_ago.endswith("m"):
            hr2["headlines"]+=headline + " | "
            hr2["texts"]+=post_text + " | "
            hr2["votes"]+=str(num_votes) + " | "
            hr2["comments"]+=post_comments + " | "
            hr2["comment_counts"]+=str(num_comments) + " | "
            hr2["comment_votes"]+=str(comments_votes) + " | "                
        elif time_ago.endswith("h"):
            if int(time_ago[:-1])<=2:
                hr2["headlines"]+=headline + " | "
                hr2["texts"]+=post_text + " | "
                hr2["votes"]+=str(num_votes) + " | "
                hr2["comments"]+=post_comments + " | "
                hr2["comment_counts"]+=str(num_comments) + " | "
                hr2["comment_votes"]+=str(comments_votes) + " | "    
            elif int(time_ago[:-1])<=12:
                if activity > 5:
                    hr12["headlines"]+=headline + " | "
                    hr12["texts"]+=post_text + " | "
                    hr12["votes"]+=str(num_votes) + " | "
                    hr12["comments"]+=post_comments + " | "
                    hr12["comment_counts"]+=str(num_comments) + " | "
                    hr12["comment_votes"]+=str(comments_votes) + " | "                                
            else:
                if activity > 4:
                    hr24["headlines"]+=headline + " | "
                    hr24["texts"]+=post_text + " | "
                    hr24["votes"]+=str(num_votes) + " | "
                    hr24["comments"]+=post_comments + " | "
                    hr24["comment_counts"]+=str(num_comments) + " | "
                    hr24["comment_votes"]+=str(comments_votes) + " | "
        elif time_ago.endswith("mo"):
                mo["headlines"]+=headline + " | "
                mo["texts"]+=post_text + " | "
                mo["votes"]+=str(num_votes) + " | "
                mo["comments"]+=post_comments + " | "
                mo["comment_counts"]+=str(num_comments) + " | "
                mo["comment_votes"]+=str(comments_votes) + " | "
        i+=1
        if i%20 == 19:
            juan_scroll(page)
    return [hr2, hr12, hr24, d7, mo]


def close_context(context):
    pages = context.pages
    if len(pages) > 0:
        for k in range(0, len(pages)):
            pages[k].close()
    
    
   
def get_search_data(context, page, kw):
    # return list with data to keyword search

    page.close()
    page = context.new_page()
    page.goto(f'https://www.reddit.com/search/?q={kw}&sort=new')
    scroll_to_bottom(page)
    new = one_search_page(context, page)
    if new == 'try_again':
        time.sleep(1)
        close_context(context)
        page = context.new_page()
        page.wait_for_load_state('domcontentloaded')
        page.goto(f'https://www.reddit.com/search/?q={kw}&sort=new')
        scroll_to_bottom(page)
        time.sleep(1)
        new = one_search_page(context, page, PAUSE_TIME = .37)
        if new == 'try_again':
            print("UPS ERROR")
            exit()
    close_context(context)
    page = context.new_page()
    page.wait_for_load_state('domcontentloaded')
    page.goto(f'https://www.reddit.com/search/?q={kw}&sort=hot')
    scroll_to_bottom(page)
    hot = one_search_page(context, page)
    if hot == 'try_again':
        time.sleep(1)
        close_context(context)
        page = context.new_page()
        page.wait_for_load_state('domcontentloaded')
        page.goto(f'https://www.reddit.com/search/?q={kw}&sort=hot')
        scroll_to_bottom(page)
        time.sleep(1)
        hot = one_search_page(context, page, PAUSE_TIME = .37)
        if hot == 'try_again':
            print("UPS ERROR")
            exit()
    close_context(context)
    page = context.new_page()
    page.wait_for_load_state('domcontentloaded')
    page.goto(f'https://www.reddit.com/search/?q={kw}&sort=relevance')
    scroll_to_bottom(page)
    relevant = one_search_page(context, page)
    if relevant == 'try_again':
        time.sleep(1)
        close_context(context)
        page = context.new_page()
        page.wait_for_load_state('domcontentloaded')
        page.goto(f'https://www.reddit.com/search/?q={kw}&sort=relevance')
        scroll_to_bottom(page)
        time.sleep(1)
        relevant = one_search_page(context, page, PAUSE_TIME = .37)
        if relevant == 'try_again':
            print("UPS ERROR")
            exit()
        
    [hr2, hr12, hr24, d7, mo] =  new
    
    #output logic
    hr2["headlines"]+=hot[0]["headlines"] + relevant[0]["headlines"]
    hr2["texts"]+=hot[0]["texts"] + relevant[0]["texts"]
    hr2["votes"]+=hot[0]["votes"] + relevant[0]["votes"]
    hr2["comments"]+=hot[0]["comments"] + relevant[0]["comments"]
    hr2["comment_counts"]+=hot[0]["comment_counts"] + relevant[0]["comment_counts"]
    hr2["comment_votes"]+=hot[0]["comment_votes"] + relevant[0]["comment_votes"]  
    hr12["headlines"]+=hot[1]["headlines"] + relevant[1]["headlines"]
    hr12["texts"]+=hot[1]["texts"] + relevant[1]["texts"]
    hr12["votes"]+=hot[1]["votes"] + relevant[1]["votes"]
    hr12["comments"]+=hot[1]["comments"] + relevant[1]["comments"]
    hr12["comment_counts"]+=hot[1]["comment_counts"] + relevant[1]["comment_counts"]
    hr12["comment_votes"]+=hot[1]["comment_votes"] + relevant[1]["comment_votes"]  
    hr24["headlines"]+=hot[2]["headlines"] + relevant[2]["headlines"]
    hr24["texts"]+=hot[2]["texts"] + relevant[2]["texts"]
    hr24["votes"]+=hot[2]["votes"] + relevant[2]["votes"]
    hr24["comments"]+=hot[2]["comments"] + relevant[2]["comments"]
    hr24["comment_counts"]+=hot[2]["comment_counts"] + relevant[2]["comment_counts"]
    hr24["comment_votes"]+=hot[2]["comment_votes"] + relevant[2]["comment_votes"]  
    d7["headlines"]+=hot[3]["headlines"] + relevant[3]["headlines"]
    d7["texts"]+=hot[3]["texts"] + relevant[3]["texts"]
    d7["votes"]+=hot[3]["votes"] + relevant[3]["votes"]
    d7["comments"]+=hot[3]["comments"] + relevant[3]["comments"]
    d7["comment_counts"]+=hot[3]["comment_counts"] + relevant[3]["comment_counts"]
    d7["comment_votes"]+=hot[3]["comment_votes"] + relevant[3]["comment_votes"]  
    mo["headlines"]+=hot[4]["headlines"] + relevant[4]["headlines"]
    mo["texts"]+=hot[4]["texts"] + relevant[4]["texts"]
    mo["votes"]+=hot[4]["votes"] + relevant[4]["votes"]
    mo["comments"]+=hot[4]["comments"] + relevant[4]["comments"]
    mo["comment_counts"]+=hot[4]["comment_counts"] + relevant[4]["comment_counts"]
    mo["comment_votes"]+=hot[4]["comment_votes"] + relevant[4]["comment_votes"]  
    
    return [hr2, hr12, hr24, d7, mo]
        
def do_the_do(kw):
    # for all keywords, get the lists + price-change data per token -> write to table
    with sync_playwright() as p:
        browser = p.chromium.launch(headless = headless)
        context = browser.new_context(user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/116.0.0.0 Safari/537.36 Edg/116.0.1938.81")
        page = context.new_page()
        [hr2, hr12, hr24, d7, mo] = get_search_data(context, page, kw)
    
    return [hr2, hr12, hr24, d7, mo]






if __name__ == '__main__':
    create_table()
    # do_the_do("dogecoin")
