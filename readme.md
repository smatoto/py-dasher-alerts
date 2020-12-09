# Google Workspace alerts

![GitHub](https://img.shields.io/github/license/mashape/apistatus.svg) [![Build Status](https://travis-ci.org/smatoto/python-workspace-alerts.svg?branch=master)](https://travis-ci.org/smatoto/python-workspace-alerts) ![GitHub last commit (branch)](https://img.shields.io/github/last-commit/smatoto/python-workspace-alerts/master)

This script checks for the status of Google Workspace services by parsing the [Status Dashboard](https://www.google.com/appsstatus#hl=en&v=status) RSS feed as described in the Help Center article below:

- [Check the current status of a Google Workspace service](https://support.google.com/a/answer/139569?hl=en)

### Usage:

1. #### Install Python3

   Install Python3 from [python.org](https://www.python.org/downloads/windows/)

2. #### Install dependencies

   ```
   pip3 install -r requirements.txt
   ```

3. #### Run the script

   ```
   python3 alert.py
   ```

### Next Steps:

- Schedule a cron-job to run the script on regular intervals
