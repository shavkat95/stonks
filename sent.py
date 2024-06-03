# pip install -q transformers
from transformers import pipeline
sentiment_pipeline = pipeline(model="cardiffnlp/twitter-roberta-base-sentiment")








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
    
    var xpathExpression = "/html/body/shreddit-app/dsa-transparency-modal-provider/search-dynamic-id-cache-controller/div/div/div[1]/div[2]/main/div/reddit-feed/faceplate-tracker[%tweet_id%]/post-consume-tracker/div/faceplate-tracker/h2/a/faceplate-screen-reader-content"
    
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
    browser = p.chromium.launch(headless = not debug)
    page = browser.new_page()
    page.goto('https://www.reddit.com/search/?q=btc')
    page.wait_for_load_state("networkidle")
    
    tweet_id = 1
    tweets = []
    while True:
        # Get tweet with a given ID (1 = first)
        tweet = page.evaluate(extract_tweet_javascript.replace("%tweet_id%", str (tweet_id))) 
        if not tweet:
            break
        tweets.append(tweet)
        tweet_id += 1


print(tweets)

# data = ["This is definitely something to check out.", "I hate you"]
data = tweets
print('\n \n \n')
print(sentiment_pipeline(data))




