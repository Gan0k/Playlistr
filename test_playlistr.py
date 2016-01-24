import unittest
import sys
import os
from apiclient.discovery import build

import playlistr

class TestPlaylistr(unittest.TestCase):

	def test_youtube_search(self):
		yt = build(playlistr.YOUTUBE_API_SERVICE_NAME,
						playlistr.YOUTUBE_API_VERSION,
						developerKey=playlistr.DEVELOPER_KEY)

		videoId = playlistr.youtube_search(yt,'gangam style')
		self.assertEqual(videoId[0], '9bZkp7q19f0')

	def test_make_playlist1(self):
		tracklist = '    01. gangam style \n  \t never gonna give '
		pl = playlistr.make_playlist(tracklist)
		self.assertIn('9bZkp7q19f0', pl)

	def test_make_playlist2(self):
		script_dir = os.path.dirname(__file__)
		relative_dir = 'tests/tracklist1.txt'
		with open(os.path.join(script_dir,relative_dir),'r') as tracklist:
			pl = playlistr.make_playlist(tracklist.read())
			self.assertIn('OPf0YbXqDm0', pl)

	def test_make_playlist3(self):
		script_dir = os.path.dirname(__file__)
		relative_dir = 'tests/tracklist2.txt'
		with open(os.path.join(script_dir,relative_dir),'r') as tracklist:
			pl = playlistr.make_playlist(tracklist.read())
			self.assertIn('mxvG-_KvWlw', pl)

if __name__ == '__main__':
	unittest.main()

