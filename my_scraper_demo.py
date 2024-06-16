import sys
import time
import my_scraper as ms
import sqlite3
from datetime import datetime

# Show debug messages? Enable this if you have problems!
ms.DEBUG = False

URL = "http://www.reuters.com/markets"
BASE_URL = ms.extract_base_url(URL)

# Reuters demo
response = ms.goto_url (URL)

data = []

# Database setup
conn = sqlite3.connect('reuters.db')
cursor = conn.cursor()

# Create table if not present
cursor.execute('''
CREATE TABLE IF NOT EXISTS news (
    news_id INTEGER PRIMARY KEY AUTOINCREMENT,
    headline TEXT UNIQUE,
    text TEXT UNIQUE,
    link TEXT UNIQUE,
    timestamp TIMESTAMP
)
''')
conn.commit()

# Extract headlines and links
for i in range (1, 1000):
    # Finds span tags with attribute "Heading" that are links
    headline = ms.wait_for (f'(//a/span[@data-testid="Heading"])[{i}]')
    link = ms.wait_for (f'(//a/span[@data-testid="Heading"])[{i}]/parent::a/@href')
    if not headline or not link:
        break
    link = BASE_URL + link
    print("Headline: " + headline)
    print("Link: " + link)
    print("----------")
    timestamp = datetime.now().strftime ('%Y-%m-%d %H:%M:%S')  # ISO 8601 format
    data.append({"headline": headline, "link": link, "news": "", "timestamp": timestamp})

# Open links to extract news text
for item in data:
    print("----------")
    # Check if the headline already exists in the database
    cursor.execute('SELECT 1 FROM news WHERE headline = ?', (item["headline"],))
    if cursor.fetchone():
        print(f"Skipping duplicate headline: {item['headline']}")
        continue
    ms.goto_url(item["link"])
    # More intuitive but sometimes contains junk
    # text = ms.wait_for ("//div[@class='article-body__content__17Yit']")    
    text = ms.run_js ('Array.from(document.querySelectorAll(\'div[data-testid^="paragraph-"]\')).map(div => div.textContent).join(\' \').replace(/  /g, \' \');')
    if text:
        # Junk, sometimes contained in article
        text = text.replace ("New Tab, opens new tab", "")
        item["news"] = text
        print ("Text: " + text[:50] + "...")
    else:
        print ("Error extracting news for: " + item["link"])
        continue

    required_keys = ["headline", "news", "link", "timestamp"]
    if not all (item.get (key, '').strip() for key in required_keys):
        print ("Skipping insertion of incomplete entry for: " + item["link"])
        continue
    try:
        cursor.execute('''
        INSERT INTO news (headline, text, link, timestamp) VALUES (?, ?, ?, ?)
        ''', (item["headline"], item["news"], item["link"], item["timestamp"]))
        conn.commit()
    except sqlite3.IntegrityError:
        print(f"Duplicate entry found for link: {item['link']}")
    except Exception as e:
        print(f"An SQLite error occurred: {e}")
    link = item["link"]
    print (f"Inserted data for: {link}")
    time.sleep (3)

# Close the database connection
conn.close()

sys.exit(0)

# Other demo
response = ms.goto_url("http://www.ariva.de")
print("Got: " + response)

response = ms.run_js('alert ("Let\'s have some fun!")')
print("Got: " + response)

response = ms.wait_for("/html/body/div[1]/div[3]/div[6]/div/div[2]/div[1]/div[4]/table/tbody/tr[1]/td[1]/div/div[2]/div/span")
print("Got: " + response)

response = ms.set_text("main-search", "GameStop")
print("Got: " + response)

response = ms.click("main-search-search-icon")
print("Got: " + response)
