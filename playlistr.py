#!/usr/bin/python
# -*- coding: utf-8 -*-

import os
import logging
import re

from apiclient.discovery import build
from apiclient.errors import HttpError

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

YOUTUBE_API_SERVICE_NAME = "youtube"
YOUTUBE_API_VERSION = "v3"
YOUTUBE_PLAYLIST_LINK = 'http://www.youtube.com/watch_videos?video_ids='
DEVELOPER_KEY = os.environ.get('YOUTUBE_API_KEY')
NOT_FOUND_MSG = 'No videos were found :('

def youtube_search(yt, query, max_results=1):

	logger.debug('Will search for: %s', query)

	# Call the search.list method to retrieve results matching the specified
	# query term.
	search_response = yt.search().list(
		q=query,
		part="id,snippet",
		maxResults=max_results
		).execute()

	videos = []
	for search_result in search_response.get("items", []):
		if search_result["id"]["kind"] == "youtube#video":
			videos.append(search_result["id"]["videoId"])

	logger.debug('Video(s) found: %d', len(videos))

	return videos

def make_playlist(tracklist):
	videos = []
	youtube = build(YOUTUBE_API_SERVICE_NAME, YOUTUBE_API_VERSION,
		developerKey=DEVELOPER_KEY)

	for line in tracklist.splitlines():

		logger.debug('Will parse: %s', line)

		# delete unnesesarry chars start string
		line = re.sub(r'^(\d|[.]|-|\s|\t)*', "", line)

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

	if not videos:
		return NOT_FOUND_MSG
	else:
		return YOUTUBE_PLAYLIST_LINK + ','.join(videos)

