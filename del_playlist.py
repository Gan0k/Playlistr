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
from oauth2client.tools import run_flow, argparser

YOUTUBE_API_SERVICE_NAME = "youtube"
YOUTUBE_API_VERSION = "v3"
CLIENT_SECRETS_FILE = "client_secrets.json"
MISSING_CLIENT_SECRETS_MESSAGE = "WARNING: Please configure OAuth 2.0".format(os.path.abspath(os.path.join(os.path.dirname(__file__), CLIENT_SECRETS_FILE)))
YOUTUBE_READ_WRITE_SCOPE = "https://www.googleapis.com/auth/youtube"
YOUTUBE_API_SERVICE_NAME = "youtube"
YOUTUBE_API_VERSION = "v3"

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

list_response = yt.playlists().list(
		part="snippet,status",
		mine="true",
		maxResults=50
	).execute()

print(len(list_response['items']))
for elem in list_response['items']:
	if elem['snippet']['title'] == 'Playlistr':
		delete_response = yt.playlists().delete(
				id=elem['id']
			).execute()

