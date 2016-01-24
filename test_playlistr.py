import unittest
import sys
from apiclient.discovery import build

import playlistr

class TestPlaylistr(unittest.TestCase):

	def test_youtube_search(self):
		yt = build(playlistr.YOUTUBE_API_SERVICE_NAME,
						playlistr.YOUTUBE_API_VERSION,
						developerKey=playlistr.DEVELOPER_KEY)

		videoId = playlistr.youtube_search(yt,'gangam style')
		self.assertEqual(videoId[0], '9bZkp7q19f0')

	def test_make_playlist(self):
		tracklist = '    01. gangam style \n  \t never gonna give '
		pl = playlistr.make_playlist(tracklist)
		self.assertIn('9bZkp7q19f0', pl)

if __name__ == '__main__':
	unittest.main()

