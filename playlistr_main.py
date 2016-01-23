#!/usr/bin/python
# -*- coding: utf-8 -*-

from keys import *

from apiclient.discovery import build
from apiclient.errors import HttpError

YOUTUBE_API_SERVICE_NAME = "youtube"
YOUTUBE_API_VERSION = "v3"
YOUTUBE_PLAYLIST_LINK = 'http://www.youtube.com/watch_videos?video_ids='

def youtube_search(yt, query, max_results=1):
	# Call the search.list method to retrieve results matching the specified
	# query term.
	search_response = yt.search().list(
		q=query,
		part="id,snippet",
		maxResults=max_results
		).execute()

	videos = []

	# Add each result to the appropriate list, and then display the lists of
	# matching videos, channels, and playlists.
	for search_result in search_response.get("items", []):
		if search_result["id"]["kind"] == "youtube#video":
			videos.append(search_result["id"]["videoId"])

	return videos

def make_playlist(tracklist):
	videos = []
	youtube = build(YOUTUBE_API_SERVICE_NAME, YOUTUBE_API_VERSION,
		developerKey=DEVELOPER_KEY)

	for line in tracklist.splitlines():
		i = 0
		while line[i].isdigit() or line[i] is "." or line[i] is " ":
			i += 1;

		print(line[i:])

		try:
			search = youtube_search(youtube,line[i:])
			if search:
				videos.append(search[0]) #get first result

		except (HttpError, e):
			print("An HTTP error %d occurred:\n%s" % (e.resp.status, e.content))

	if not videos: return 'No videos found'
	else:
		return YOUTUBE_PLAYLIST_LINK + ','.join(videos)

