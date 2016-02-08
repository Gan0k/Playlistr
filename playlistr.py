#!/usr/bin/python
# -*- coding: utf-8 -*-

import os
import logging
import re
import sys, getopt

from apiclient.discovery import build
from apiclient.errors import HttpError

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

YOUTUBE_API_SERVICE_NAME = "youtube"
YOUTUBE_API_VERSION = "v3"
YOUTUBE_PLAYLIST_LINK = 'https://www.youtube.com/embed/{:s}?playlist={:s}'
DEVELOPER_KEY = os.environ.get('YOUTUBE_API_KEY')

def youtube_search(yt, query, max_results=1):

	logger.debug('Will search for: %s', query)

	# Call the search.list method to retrieve results matching the specified
	# query term.
	response = yt.search().list(
		q=query,
		part="id",
		maxResults=max_results,
		type="video",
		).execute()

	videos = [res["id"]["videoId"] for res in response.get("items", [])]

	logger.debug('Video(s) found: %d', len(videos))

	return videos

def make_playlist(tracklist):
	videos = []
	youtube = build(YOUTUBE_API_SERVICE_NAME, YOUTUBE_API_VERSION,
		developerKey=DEVELOPER_KEY)

	for line in tracklist.splitlines():

		logger.debug('Will parse: %s', line)

		# delete unnesesarry chars start string
		line = re.sub(r'^(\d|\.|-|\s|\t|:|\[|\])*', "", line)

		# delete unnesesarry chars end string
		line = re.sub(r'(\s|\t)*$', "", line)

		if not line:
			logger.debug('Empty line')
			continue

		try:
			search = youtube_search(youtube,line)
			if search:
				videos.append(search[0]) #get first result

		except HttpError as e:
			logger.error("An HTTP error %d occurred:\n%s" % (e.resp.status, e.content))

	return YOUTUBE_PLAYLIST_LINK.format(videos[0],','.join(videos[1:])) if videos else None

def usage(errcode):
    print('playlistr.py -i <inputfile>')
    sys.exit(errcode)

if __name__ == "__main__":
    logger.setLevel(logging.ERROR)

    try:
        opts, args = getopt.getopt(sys.argv[1:],"hi:",["help","ifile="])
    except getopt.GetoptError as err:
        print(err)
        usage(2)

    inputfile = None
    for opt, arg in opts:
        if opt in ('-h','--help'):
            usage(0)
        elif opt in ('-i', '--ifile'):
            inputfile = arg
        else:
            usage(2)

    if inputfile is None:
        usage(2)
    else:
        with open(os.getcwd() + '/' + inputfile,'r') as f:
            link = make_playlist(f.read())
            print()
            print()
            print('Playlist Link:')
            print(link)

