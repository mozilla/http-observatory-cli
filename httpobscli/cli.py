#!/usr/bin/env python


from __future__ import print_function
from operator import itemgetter
from os import environ
from sys import exit

import argparse
import datetime
import pytz
import json
import requests
import sys
import time

# import urlparse in a Python2 / Python3 compatible way
try:
    from urllib.parse import urlparse
except ImportError:
    from urlparse import urlparse

API_URL = environ.get('HTTPOBS_API_URL', 'https://http-observatory.security.mozilla.org/api/v1')


def analyze(host):
    global args

    data = {}

    if args.rescan:
        data['rescan'] = 'true'
    if args.hidden:
        data['hidden'] = 'true'

    try:
        # First, make a POST to the Observatory to start the scan
        scan = requests.post(API_URL + '/analyze?host={host}'.format(host=host), data=data).json()

        # Notify the user if the user if they attempted a rescan too soon
        if (args.rescan and scan.get('error') == 'rescan-attempt-too-soon'):
            print('Rescan attempt is sooner than the allowed cooldown period. Returning cached results instead.\n',
                  file=sys.stderr)

        # Keep polling the HTTP Observatory for the scan to finish
        if scan.get('state') != 'FINISHED':
            scan = poll(API_URL + '/analyze?host={host}'.format(host=host),
                        key='state',
                        values=['FINISHED'],
                        method='GET')
        grade = scan['grade']
        score = scan['score']
    except SystemExit:
        raise
    except:
        print('\nCannot connect to HTTP Observatory at: {url} for Host: {host}.'.format(url=API_URL, host=host))
        exit(1)

    # Get the test results
    tests = poll(API_URL + '/getScanResults?scan={scan}'.format(scan=scan['scan_id']),
                 key='x-frame-options')

    # Print out a notification on stderr that it's a cached result
    # I hate working with datetime so much
    differential = datetime.datetime.now(pytz.utc) - \
                   pytz.timezone('GMT').localize(
                       datetime.datetime.strptime(
                           scan['end_time'],
                           '%a, %d %b %Y %H:%M:%S %Z'
                        )
                    )
    differential = differential.days * 86400 + differential.seconds

    if differential > 300:
        hour = int(differential / 3600)
        minute = int((differential - 3600 * hour) / 60)
        sec = int(differential % 60)
        print('Results are cached from {hour}h{min}m{sec}s ago; use -r to rescan.\n'
              .format(hour=hour, min=minute, sec=sec),
              file=sys.stderr)

    # Print the grade and scan results
    if args.csv:
        print('{host},{grade},{score},"'.format(host=host, grade=grade, score=score), end="")
    elif args.debug:
        print(json.dumps({'scan': scan, 'host': host, 'tests': tests}, indent=4, sort_keys=True))
    else:
        print('Score: {score} [{grade}]'.format(score=score, grade=grade))

    # Print out the reasons for score modification
    if not args.debug:
        if not args.csv:
            print('Modifiers:')

        # Get all the scores that aren't 0, in descending numerical order
        if args.zero:
            scores = sorted([(tests[test]['score_modifier'], tests[test]['score_description']) for test in tests])
        else:
            scores = sorted([(tests[test]['score_modifier'], tests[test]['score_description'])
                             for test in tests if tests[test]['score_modifier'] != 0])
        scores = sorted(scores, key=itemgetter(0), reverse=True)  # [(-5, 'foo'), (-10, 'bar')]
        scores = [list(score) for score in scores]  # convert everything from tuples to lists

        for score in scores:
            if score[0] > 0:
                score[0] = '+' + str(score[0])  # display 5 as +5
            if args.csv:
                # it's not fancy but it works
                print('[{modifier:>4}] {reason}'.format(modifier=score[0], reason=score[1].replace('"','\\"')))
            else:
                print('    [{modifier:>4}] {reason}'.format(modifier=score[0], reason=score[1]))

        if args.csv:
            # Terminating " for the block of text, post-loop
            print('"')


def poll(url, key, values=None, method='GET', headers=None, timeout=300):
    if headers is None:
        headers = {}

    # Create requests session
    s = requests.Session()
    s.headers.update(headers)

    # Set the start time, since we don't want to go longer than timeout seconds
    start_time = time.time()

    if args.verbose:
        print('Retrieving: {url}'.format(url=url), end='', file=sys.stderr)
        sys.stdout.flush()

    while True:
        # Retrieve the URL
        if method == 'POST':
            r = s.post(url).json()
        else:
            r = s.get(url).json()

        # See if error is in there; if so, we just abort the whole thing
        if 'error' in r:
            print('\nUnable to get result from the HTTP Observatory. Host:{host} Error: {error}.'.format(host, error=r['error']))
            exit(1)

        # See if the key is one of the pollable values
        if values:
            if r[key] in values:
                if args.verbose:
                    print()
                return r
        else:
            if key in r:
                if args.verbose:
                    print()
                return r

        # Let's error out if it has taken too long
        if time.time() - start_time > timeout:
            raise requests.Timeout

        # If not, let's sleep and try again
        if args.verbose:
            print('.', end='', file=sys.stderr)
            sys.stdout.flush()
        time.sleep(3)


def usage(cmd):
    print('Usage: {0} <hostname>'.format(cmd))
    exit(1)


def main():
    global args

    # Parse the command line
    parser = argparse.ArgumentParser(usage='%(prog)s [options] host')
    parser.add_argument('host', help='hostname of the website to scan')
    parser.add_argument('-d', '--debug', action='store_true', help='output only raw JSON from scan and tests')
    parser.add_argument('-c', '--csv', action='store_true', help='output record in quoted csv format')
    parser.add_argument('-r', '--rescan',
                        action='store_true',
                        help='initiate a rescan instead of showing recent scan results')
    parser.add_argument('-v', '--verbose', action='store_true', help='display progress indicator')
    parser.add_argument('-x', '--hidden', action='store_true', help='don\'t list scan in the recent scan results')
    parser.add_argument('-z', '--zero', action='store_true',
                        help='show test results that don\'t affect the final score')
    args = parser.parse_args()

    # Try to parse the hostname, in case they used a URL instead
    args.host = urlparse(args.host).netloc if urlparse(args.host).netloc else args.host

    # Go out and scan!
    analyze(args.host)


if __name__ == "__main__":
    main()
