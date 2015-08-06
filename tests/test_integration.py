from __future__ import absolute_import

import os
from config import config
from getgist.__main__ import Gist, MyGist
from re import search
from unittest import TestCase

try:
    from mock import patch
    input_function = 'getgist.__main__.input'
except ImportError:
    from unittest.mock import patch
    input_function = 'builtins.input'


class TestDownload(TestCase):

    @patch('getgist.__main__.Gist.curl')
    def setUp(self, mocked_curl):
        mocked_curl.return_value = config['json']
        self.gist = Gist(config['user'], config['file'])

    def tearDown(self):
        for name in os.listdir(self.gist.local_dir):
            if search(r'^({})(\.bkp(.\d)?)?$'.format(config['file']), name):
                os.remove(os.path.join(self.gist.local_dir, name))

    @patch(input_function)
    def test_local_dir(self, mocked_input):
        mocked_input.return_value = 'y'
        self.assertTrue(os.path.exists(self.gist.local_dir))
        self.assertTrue(os.path.isdir(self.gist.local_dir))

    @patch(input_function)
    @patch('getgist.__main__.Gist.curl')
    def test_download(self, mocked_curl, mocked_input):
        mocked_input.return_value = 'y'
        mocked_curl.return_value = config['json']
        self.gist.save()
        self.assertTrue(os.path.exists(self.gist.local_path))

    @patch(input_function)
    @patch('getgist.__main__.Gist.curl')
    def test_backup(self, mocked_curl,  mocked_input):

        # mock input value
        mocked_input.return_value = 'n'
        mocked_curl.return_value = config['json']

        # backup filenames
        backup1 = '{}.bkp'.format(self.gist.local_path)
        backup2 = '{}.bkp.1'.format(self.gist.local_path)

        # 1st download
        self.gist.save()
        self.assertTrue(os.path.exists(self.gist.local_path))
        self.assertEqual(config['json'], open(self.gist.local_path).read())

        # 2nd download
        self.gist.save()
        self.assertTrue(os.path.exists(backup1))
        self.assertEqual(config['json'], open(backup1).read())

        # 3rd download
        self.gist.save()
        self.assertTrue(os.path.exists(backup2))
        self.assertEqual(config['json'], open(backup2).read())

        # 4th download
        self.gist.save()


class TestMyGist(TestCase):

    @patch('getgist.__main__.Gist.curl')
    def setUp(self, mocked_curl):
        mocked_curl.return_value = config['json']
        self.gist = MyGist(config['file'], True)

    def tearDown(self):
        for name in os.listdir(self.gist.local_dir):
            if search(r'^({})(\.bkp(.\d)?)?$'.format(config['file']), name):
                os.remove(os.path.join(self.gist.local_dir, name))

    @patch(input_function)
    @patch('getgist.__main__.Gist.curl')
    def test_mygist_download(self, mocked_curl, mocked_input):
        mocked_input.return_value = config['user']
        mocked_curl.return_value = config['json']
        self.gist.save()
        self.assertTrue(os.path.exists(self.gist.local_path))
