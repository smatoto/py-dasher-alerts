#!/usr/bin/env python
import re, sys
import requests, logging
from os import path
from feedparser import parse
from pathlib import Path
from bs4 import BeautifulSoup

LOG_FILE = 'logs/status.log'
BASE_URL = "https://www.google.com/appsstatus/rss/en"


def get_alert_info(alerts):
    if len(alerts):
        soup = BeautifulSoup(alerts[0].description, features="html.parser")
        description = soup.find("p").findNext("p").get_text()
        color = Path(soup.img['src']).stem
        if color == 'red':
            code = 2
        elif color == 'yellow':
            code = 1
        elif color == 'blue':
            code = 0
    else:
        code = 0
        description = 'No update'
    return { "code": code, "description": description }


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
        response = requests.get(rss).text

        # Generate alerts
        logger.info('Fetching alerts...')
        new_feed = parse(response)
        alert_info = get_alert_info(new_feed.entries)
        print(f'{alert_info["description"]}')
        # print(f'Exit code: {alert_info["code"]}')


        # Save out the current status for the next invocation.
        logger.info(f'Details: {alert_info["description"]}')
        logger.info(f'Script runtime complete. Exiting with code {alert_info["code"]}')
        sys.exit(alert_info["code"])

    except Exception as e:
        # Log error
        logger.error(f'Error has occurred: {str(e)}')
        sys.exit(1)

def main():
    list_alerts(BASE_URL)

if __name__ == "__main__":
    main()
