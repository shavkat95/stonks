# pip install playwright
# then: python -m playwright install
from playwright.sync_api import sync_playwright

# Display browser window for debugging?
debug = True

# This does not catch all tweets yet, maybe some have a different xpath
# This needs more checking
extract_tweet_javascript = """
try
{
    var xpathExpression = "/html/body/div[1]/div/div/div[2]/main/div/div/div/div[1]/div/div[3]/div/div/section/div/div/div[%tweet_id%]/div/div/article/div/div/div[2]/div[2]/div[2]/div/span/text()";
    var element = document.evaluate (xpathExpression, document, null, XPathResult.FIRST_ORDERED_NODE_TYPE, null).singleNodeValue;
    element = element.textContent;
 }
catch (error)
{
    element = false;
}
"""

with sync_playwright() as p:
    # Headless mode = Browser is invisible
    browser = p.chromium.launch (headless = not debug)
    page = browser.new_page()
    page.goto ('https://twitter.com/TheEconomist')
    page.wait_for_load_state ("networkidle")
    
    tweet_id = 1
    tweets = []
    while True:
        # Get tweet with a given ID (1 = first)
        tweet = page.evaluate (extract_tweet_javascript.replace ("%tweet_id%", str (tweet_id))) 
        if not tweet:
            break
        tweets.append (tweet)
        tweet_id += 1
    if debug:
        input ("Debug: Showing Browser until [Enter]")
    browser.close()

# Print found tweets
for tweet in tweets:
    print("Result: " + tweet)