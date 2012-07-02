#!/usr/bin/env python
from fsevents import Observer, Stream, IN_CREATE

import urllib2
import json
import os
import sys
import time
import logging

RPLAY_DOMAIN = os.getenv('RPLAY_DOMAIN', 'young-sky-3165.herokuapp.com')
RPLAY_USERNAME = os.getenv('RPLAY_USERNAME', '')
RPLAY_PASSWORD = os.getenv('RPLAY_PASSWORD', '')
RPLAY_DIR = os.getenv('RPLAY_DIR', '/Users/*/Library/Application Support/Blizzard/StarCraft II/Accounts/*/*/Replays/Multiplayer')

URL = 'http://%s' % RPLAY_DOMAIN
MATCH_ENDPOINT = "%s/api/v1/match/" % URL

logger = logging.getLogger('rplay_client')
logger.setLevel(logging.DEBUG)
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
ch = logging.StreamHandler()
ch.setLevel(logging.ERROR)
logger.addHandler(ch)


def upload_replay(paths = []):
    for path in paths:
        print "Uploading %s" % path
        # Open the File, and read it into a string
        fhandle = open(path, "rb").read().encode("base64")

        # build data that we will post
        replay = {
            "replay_file": {
                "name": os.path.basename(path),
                "file": fhandle
            }
        }

        # Setup the opener
        auth = urllib2.HTTPBasicAuthHandler()
        auth.add_password('django-tastypie', RPLAY_DOMAIN, RPLAY_USERNAME, RPLAY_PASSWORD)
        opener = urllib2.build_opener(auth)
        urllib2.install_opener(opener)

        # Build the request
        r = urllib2.Request(MATCH_ENDPOINT)
        r.add_data(json.dumps(replay))
        r.add_header("Content-Type", "application/json")

        urllib2.urlopen(r)
        time.sleep(3)


def callback(fileevent, *args, **kwargs):
    print args
    print kwargs
    print("Event %s" % fileevent)
    if fileevent.mask & IN_CREATE:
        print "uploading it"
        upload_replay([fileevent.name])



if __name__ == "__main__":
    ## Start with 0 arguments to run the dameon,
    # 1 or more to upload individual files
    if (sys.argv[1:]):
        upload_replay(sys.argv[1:])
    else:
        print("starting handler")
        observer = Observer()
        observer.start()
        stream = Stream(callback, RPLAY_DIR, file_events=True)
        observer.schedule(stream)

