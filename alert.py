import feedparser as p
url = 'https://www.google.com/appsstatus/rss/en'

# Get RSS feed contents
feed = p.parse(url)

# Get feed entries
alerts = feed.entries

# Set status response based on alerts
status = 1 if len(alerts) else 0

# Return status (0 or 1) when RSS has an alert item
print(status)