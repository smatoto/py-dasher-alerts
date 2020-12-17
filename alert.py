import feedparser as p
import re

url = 'https://www.google.com/appsstatus/rss/en'

# Get RSS feed contents
feed = p.parse(url)

# Get feed entries
alerts = feed.entries

# Get number of alerts
status = 1 if len(alerts) else 0

# Set default alert status
peak_alert = 0

# Check each alert for alert_code
if status:
    for alert in alerts:
        result = re.search('outageid:(.*)#tstamp:', alert.guid)
        alert_code = result.group(1)
        # Compare alert codes and set highest alert code
        if int(alert_code) > int(peak_alert):
            peak_alert = alert_code

# Return outage alert_id / code
print(peak_alert)
