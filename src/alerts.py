#!/usr/bin/env python
import re, sys
from os import path
import requests
import feedparser
import logging
from pathlib import Path
from bs4 import BeautifulSoup

LOG_FILE = 'logs/status.log'
PREVIOUS_STATE = 'logs/previous-state.xml'
BASE_URL = "https://www.google.com/appsstatus/rss/en"


def get_alert_info(alerts):
    # code = 0
    # for alert in alerts:
    #     soup = BeautifulSoup(alert.description, features="html.parser")
    #     color = Path(soup.img['src']).stem
    #     print(f'{alert.title} : {alert.updated} - {color}')
    #     code = 1 if color == 'yellow' else 0
    # return code

    if len(alerts):
        # alert = alerts[0]
        soup = BeautifulSoup(alerts[0].description, features="html.parser")
        description = soup.find("p").findNext("p").get_text()
        color = Path(soup.img['src']).stem
        code = 2 if color == 'yellow' else 1
    else:
        code = 0
        description = 'No update'
    return { "code": code, "description": description }


def checkState(curr,prev):
    # Parse the current status
    new_feed = feedparser.parse(curr)
    new_items = new_feed.entries
    new_items.reverse()
    alerts = []
    if path.exists(prev):
        old_feed = feedparser.parse(prev)
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
        alerts = new_feed.entries
    return alerts

def list_alerts(rss):
    # Set default feed
    if rss is None:
        rss = BASE_URL

    # Set up logger.
    logging.basicConfig(filename=LOG_FILE,format="%(asctime)s: [%(levelname)s] : %(message)s", level=logging.INFO)
    logger = logging.getLogger('workspace_status')

    try:
        # Grab the current status.
        logger.info('Fetching Google Workspace status RSS feed.')
        currentState = requests.get(rss).text

        # Generate alerts
        logger.info('Listing alerts...')
        alerts = checkState(currentState, PREVIOUS_STATE)
        # print(f'Feed: {rss}')
        alert_info = get_alert_info(alerts)
        print(f'{alert_info["description"]}')
        # print(f'Code: {alert_info["code"]}')

        # Save out the current status for the next invocation.
        logger.info('Saving the current Google Workspace status.')
        with open(PREVIOUS_STATE,"w") as f:
            f.write(currentState)
        logger.info('Script runtime complete. Exiting now.')
        sys.exit(alert_info["code"])

    except Exception as e:
        # Log error
        logger.error(f'Error has occurred: {str(e)}')
        sys.exit(1)

def main():
    list_alerts(BASE_URL)

if __name__ == "__main__":
    main()
