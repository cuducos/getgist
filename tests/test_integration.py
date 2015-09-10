import os
from config import config, MockAPI
from getgist.__main__ import Gist, MyGist
from re import search
from unittest import TestCase

try:
    from mock import patch
except ImportError:
    from unittest.mock import patch


class TestDownload(TestCase):

    @patch('getgist.__main__.Gist.curl')
    @patch('getgist.__main__.Gist.query_api')
    @patch('getgist.__main__.Gist.authenticated')
    def setUp(self, authenticated, query_api, curl):
        authenticated.return_value = False
        query_api.return_value = config['gists']
        curl.return_value = config['content']
        self.gist = Gist(config['user'], config['file'])

    def tearDown(self):
        for name in os.listdir(self.gist.local_dir):
            if search(r'^({})(\.bkp(.\d)?)?$'.format(config['file']), name):
                os.remove(os.path.join(self.gist.local_dir, name))

    @patch('getgist.__main__.Gist.ask')
    def test_local_dir(self, mocked_ask):
        mocked_ask.return_value = 'y'
        self.assertTrue(os.path.exists(self.gist.local_dir))
        self.assertTrue(os.path.isdir(self.gist.local_dir))

    @patch('getgist.__main__.Gist.ask')
    @patch('getgist.__main__.Gist.curl')
    def test_download(self, curl, ask):
        ask.return_value = 'y'
        curl.return_value = config['content']
        self.gist.save()
        self.assertTrue(os.path.exists(self.gist.local_path))
        self.assertEqual(open(self.gist.local_path).read(), config['content'])

    @patch('getgist.__main__.Gist.ask')
    @patch('getgist.__main__.Gist.curl')
    def test_backup(self, curl,  ask):

        # mock input value
        ask.return_value = 'n'
        curl.return_value = config['content']

        # backup filenames
        backup1 = '{}.bkp'.format(self.gist.local_path)
        backup2 = '{}.bkp1'.format(self.gist.local_path)
        backup3 = '{}.bkp2'.format(self.gist.local_path)

        # 1st download
        self.gist.save()
        self.assertTrue(os.path.exists(self.gist.local_path))
        self.assertEqual(config['content'], open(self.gist.local_path).read())

        # 2nd download
        self.gist.save()
        self.assertTrue(os.path.exists(backup1))
        self.assertEqual(config['content'], open(backup1).read())

        # 3rd download
        self.gist.save()
        self.assertTrue(os.path.exists(backup2))
        self.assertEqual(config['content'], open(backup2).read())

        # 4th download
        self.gist.save()
        self.assertTrue(os.path.exists(backup3))
        self.assertEqual(config['content'], open(backup3).read())


class TestMyGist(TestCase):

    @patch('getgist.__main__.Gist.ask')
    @patch('getgist.__main__.Gist.curl')
    @patch('getgist.__main__.Gist.query_api')
    @patch('getgist.__main__.Gist.authenticated')
    def setUp(self, authenticated, query_api, curl, ask):
        authenticated.return_value = False
        query_api.return_value = config['gists']
        curl.return_value = config['content']
        ask.return_value = config['user']
        self.gist = MyGist(config['file'], True)

    def tearDown(self):
        for name in os.listdir(self.gist.local_dir):
            if search(r'^({})(\.bkp(.\d)?)?$'.format(config['file']), name):
                os.remove(os.path.join(self.gist.local_dir, name))

    @patch('getgist.__main__.Gist.ask')
    @patch('getgist.__main__.Gist.curl')
    def test_mygist_download(self, mocked_curl, mocked_ask):
        mocked_ask.return_value = config['user']
        mocked_curl.return_value = config['content']
        self.gist.save()
        self.assertTrue(os.path.exists(self.gist.local_path))
        self.assertEqual(open(self.gist.local_path).read(), config['content'])
