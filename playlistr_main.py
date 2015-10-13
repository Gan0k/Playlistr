#!/usr/bin/python
# -*- coding: utf-8 -*-

import httplib2
import os
import sys

import keys

from apiclient.discovery import build
from apiclient.errors import HttpError
from oauth2client.client import flow_from_clientsecrets
from oauth2client.file import Storage
from oauth2client.tools import argparser, run_flow

YOUTUBE_API_SERVICE_NAME = "youtube"
YOUTUBE_API_VERSION = "v3"
CLIENT_SECRETS_FILE = "client_secrets.json"
MISSING_CLIENT_SECRETS_MESSAGE = "WARNING: Please configure OAuth 2.0".format(os.path.abspath(os.path.join(os.path.dirname(__file__), CLIENT_SECRETS_FILE)))
YOUTUBE_READ_WRITE_SCOPE = "https://www.googleapis.com/auth/youtube"
YOUTUBE_API_SERVICE_NAME = "youtube"
YOUTUBE_API_VERSION = "v3"

def youtube_search(yt, query, max_results):
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

	return videos[0]

def create_playlist(ids):
	flow = flow_from_clientsecrets(CLIENT_SECRETS_FILE,
		message=MISSING_CLIENT_SECRETS_MESSAGE,
		scope=YOUTUBE_READ_WRITE_SCOPE)

	storage = Storage("%s-oauth2.json" % sys.argv[0])
	credentials = storage.get()

	if credentials is None or credentials.invalid:
		flags = argparser.parse_args()
		credentials = run_flow(flow, storage, flags)

	yt = build(YOUTUBE_API_SERVICE_NAME, YOUTUBE_API_VERSION,
		http=credentials.authorize(httplib2.Http()))

	# This code creates a new, private playlist in the authorized user's channel.
	playlists_response = yt.playlists().insert(
			part="snippet,status",
			body=dict(
				snippet=dict(
						title="Playlistr",
						description="Playlist Created by Playlisr!"
				),
				status=dict(
					privacyStatus="public"
				)
			)
		).execute()

	playlistid = playlists_response["id"]
	for idvideo in ids:
		response = yt.playlistItems().insert(
				part="snippet,status",
				body=dict(
					snippet=dict(
							playlistId=playlistid,
							resourceId=dict(
								kind='youtube#video',
								videoId=idvideo
							)
					),
					status=dict(
						privacyStatus="public"
					)
				)
			).execute()

	return playlistid 

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
			videos.append(youtube_search(youtube,line[i:], 1))
		except(HttpError, e):
			print("An HTTP error %d occurred:\n%s" % (e.resp.status, e.content))
	return "https://www.youtube.com/embed/" + videos[0] + '?list=' + create_playlist(videos)

