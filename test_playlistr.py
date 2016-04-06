import unittest
import sys
import os
from apiclient.discovery import build
from flaskapp import app

import playlistr

class TestPlaylistr(unittest.TestCase):

    def assert_video_in_list(self, videoId, relative_dir):
        script_dir = os.path.dirname(__file__)
        with open(os.path.join(script_dir,relative_dir),'r') as tracklist:
            pl = playlistr.make_playlist(tracklist.read())
            self.assertIn(videoId, pl)

    def test_youtube_search(self):
        yt = build(playlistr.YOUTUBE_API_SERVICE_NAME,
                                        playlistr.YOUTUBE_API_VERSION,
                                        developerKey=playlistr.DEVELOPER_KEY)

        videoId = playlistr.youtube_search('gangam style')
        self.assertEqual(videoId[0], '9bZkp7q19f0')

    def test_make_playlist1(self):
        tracklist = '    01. gangam style \n  \t never gonna give '
        pl = playlistr.make_playlist(tracklist)
        self.assertIn('9bZkp7q19f0', pl)

    def test_make_playlist2(self):
        self.assert_video_in_list('OPf0YbXqDm0','datalists/tracklist1.txt')

    def test_make_playlist3(self):
        self.assert_video_in_list('mxvG-_KvWlw','datalists/tracklist2.txt')

class TestFlask(unittest.TestCase):

    def setUp(self):
        self.app = app.test_client()
        self.app.testing = True

    def tearDown(self):
        pass

    def test_home_response(self):
        result = self.app.get('/')
        self.assertEqual(result.status_code, 200)

    def test_home_data(self):
        result = self.app.get('/')
        self.assertIn('Playlistr', str(result.data))

if __name__ == '__main__':
        unittest.main()

