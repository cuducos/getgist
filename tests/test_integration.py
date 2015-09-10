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
    @patch('getgist.__main__.Gist.validate_token')
    def setUp(self, validate_token, query_api, curl):
        api = MockAPI()
        validate_token.return_value = api.fail_auth()
        query_api.return_value = config['json']
        curl.return_value = 'test'
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
    def test_download(self, mocked_curl, mocked_ask):
        mocked_ask.return_value = 'y'
        mocked_curl.return_value = 'test'
        self.gist.save()
        self.assertTrue(os.path.exists(self.gist.local_path))

    @patch('getgist.__main__.Gist.ask')
    @patch('getgist.__main__.Gist.curl')
    def test_backup(self, mocked_curl,  mocked_ask):

        # mock input value
        mocked_ask.return_value = 'n'
        mocked_curl.return_value = config['content']

        # backup filenames
        backup1 = '{}.bkp'.format(self.gist.local_path)
        backup2 = '{}.bkp.1'.format(self.gist.local_path)

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


class TestMyGist(TestCase):

    @patch('getgist.__main__.Gist.ask')
    @patch('getgist.__main__.Gist.curl')
    @patch('getgist.__main__.Gist.query_api')
    @patch('getgist.__main__.Gist.validate_token')
    def setUp(self, validate_token, query_api, curl, ask):
        api = MockAPI()
        validate_token.return_value = api.fail_auth()
        query_api.return_value = config['json']
        curl.return_value = 'test'
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
