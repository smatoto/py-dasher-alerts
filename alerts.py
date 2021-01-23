#!/usr/bin/env python
import re, sys
from os import path
import requests
import feedparser
import logging
from pathlib import Path

logfile = 'logs/status.log'
previousState = 'logs/previous-state.xml'
rssfeed = "https://www.google.com/appsstatus/rss/en"
# rssfeed = "https://storage.googleapis.com/test-gsuite-alerts/2020-11-17T16-17-00Z.xml"
# rssfeed = "https://storage.googleapis.com/test-gsuite-alerts/2020-11-17T16-19-00Z.xml"
# rssfeed = "https://storage.googleapis.com/test-gsuite-alerts/2020-11-17T17-20-00Z.xml"

def checkState(currentState,previousState):
    # Parse the current status
    new_feed = feedparser.parse(currentState)
    new_items = new_feed.entries
    new_items.reverse()
    alerts = []
    if path.exists(previousState):
        old_feed = feedparser.parse(previousState)
        old_items = old_feed.entries
        if not old_items:
            alerts = new_items
        else:
            while new_items:
                matches = False
                new_item = new_items.pop()
                for count, old_item in enumerate(old_items):
                    if ((new_item.published == old_item.published) and (new_item.title == old_item.title) and (new_item.updated == old_item.updated)):
                        matches = True
                        del old_items[count]
                        break
                    else:
                        continue
                if not matches:
                    alerts.append(new_item) 
                    
    else:
        print('No previous state')
        alerts = new_feed.entries

    return alerts

def get_alert_code(alerts):
    for alert in alerts:
        print(f'{alert.title} : {alert.published} - {alert.updated}')

def main():
    # Set up logger.
    logging.basicConfig(filename=logfile,format="%(asctime)s: [%(levelname)s] : %(message)s", level=logging.INFO)
    logger = logging.getLogger('workspace_status')

    try:
        # Grab the current status.
        logger.info('Fetching Google Workspace Status RSS Feed over HTTP(S).')
        currentState = requests.get(rssfeed).text

        # Generate alerts
        logger.info('Listing alerts...')
        alerts = checkState(currentState, previousState)
        get_alert_code(alerts)

        # Save out the current status for the next invocation.
        logger.info('Saving the current Google Workspace Status for future invocation.')
        with open(previousState,"w") as f:
            f.write(currentState)
        logger.info('Script runtime complete. Exiting now.')
        sys.exit(0)

    except Exception as e:
        # Log error
        logger.error(f'Error has occurred: {str(e)}')
        sys.exit(1)

if __name__ == "__main__":
    main()
