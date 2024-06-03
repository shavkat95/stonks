import sqlite3
from datetime import datetime

# Connect to SQLite database (or create it if it doesn't exist)
conn = sqlite3.connect('news_data.db')
c = conn.cursor()

# Create table
c.execute('''
    CREATE TABLE IF NOT EXISTS news (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        timestamp TEXT,
        headline TEXT,
        full_text TEXT
    )
''')

# Function to insert data
def insert_data(headline, full_text):
    timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    c.execute('INSERT INTO news (timestamp, headline, full_text) VALUES (?, ?, ?)', (timestamp, headline, full_text))
    conn.commit()

# Example usage
insert_data('Sample Headline', 'Sample full text content of the news.')

# Close the connection
conn.close()
