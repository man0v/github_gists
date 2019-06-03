#!/usr/bin/env python

import urllib3
import json
import pprint
import datetime
import time
import sys
import os
import re

"""Script that searches queries gists against specific user
The script counts on a last_check file to store the last time it queried for new gists
If the file doesn't exist, it's created

The script can be cofigured using Environment Variables:
LAST_CHECK_FILE: Path to the file that stores the last time query was made
GITHUB_USERNAME: a GitHub username to be used for the query

The rest of the Globals are defined bellow
"""
### Globals
# Endpoint
GITHUB_ENDPOINT = 'https://api.github.com/'
# Headers
HEADERS = {
    'Accept': 'application/vnd.github.v3+json',
    'User-Agent': 'Equal Experts Assignment Github Gists'
}
# Absolute Path to Last Check file
LAST_CHECK_FILE = os.environ.get('LAST_CHECK_FILE', os.path.dirname(os.path.realpath(__file__)) + "/last_check")
GITHUB_USERNAME = os.environ.get('GITHUB_USERNAME', 'geerlingguy')

def is_iso8601(cmp):
    """Function that validates iso8601 timestamps

    Args:
        cmp (str): a string to be validates
    Returns:
        bool: True if the string is valid, False if not
    """

    r = "^(-?(?:[1-9][0-9]*)?[0-9]{4})-(1[0-2]|0[1-9])-(3[01]|0[1-9]|[12][0-9])T(2[0-3]|[01][0-9]):([0-5][0-9]):([0-5][0-9])(\.[0-9]+)?(Z|[+-](?:2[0-3]|[01][0-9]):[0-5][0-9])?$"

    if re.match(r, cmp) is not None:
        return True
    else:
        return False


def set_time(now = True, fn = LAST_CHECK_FILE):
    """Function that creates or updates a last_check file

    Args:
        now (bool)(optional): Set the time in the last_check file. If True, sets it to now, if False sets it to Jan 1 1970
        fn (str)(optional): Absolute path to the last_check file
    Returns:
        str: ISO 8601 time on success, exits on error
    """

    if now:
        dt = datetime.datetime.now()
    else:
        dt = datetime.datetime.fromtimestamp(0)

    iso_time = dt.isoformat()

    try:
        with open(fn, 'w') as fn_open:
            fn_open.write(iso_time)
    except (IOError, TypeError) as e:
        print("cannot open ", fn, "-", e)
        sys.exit(1)

    return iso_time

def get_time(fn = LAST_CHECK_FILE):
    """Function that gets time from a local file

    Args:
        fn (str)(optional): Absolute path to the last_check file

    Returns:
        int: ISO 8601 time and date
    """

    try:
        with open(fn, 'r') as last_check:
            ret = last_check.read()

    except FileNotFoundError:
        ret = set_time(False)
    except IOError:
        print("cannot access 'last check' file, exiting...")
        sys.exit(1)

    # If not is8601 - set it to 0
    if not is_iso8601(ret):
        ret = set_time(False)

    return ret

def get_gists(tm, username = GITHUB_USERNAME):
    """Function that get gists based on time and username

    Args:
        time (str): ISO 8601 time stamp used for the query. Anything newere will be posted and time will be written down
        username (str): a username to be checked against. Defaults to geerlingguy
    Returns:
        list: list of all gists newer than time

    """

    # Initialize urllib
    http = urllib3.PoolManager()

    # Setup the GET parameters
    fields = {
        'since': tm
    }

    # Make the actual request
    r = http.request(
        'GET',
        GITHUB_ENDPOINT + 'users/' + username + '/gists',
        fields = fields,
        headers = HEADERS
    )

    # Capture result as json
    res = json.loads(r.data)

    # Setup last check time
    set_time()

    # Return number of gists
    return len(res)


def main():

    # Get the time from LAST_CHECK_FILE location
    gt = get_time()

    # Get the gists based on the time acquired
    gists = get_gists(gt)
    # Print the result
    print("{} new gists since {} for {}".format(gists, gt, GITHUB_USERNAME))

if __name__ == "__main__":
    main()
