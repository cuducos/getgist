from __future__ import absolute_import

import os
from getgist.__main__ import Gist
from re import search
from unittest import TestCase

try:
    from mock import patch
    from urllib2 import urlopen
    input_function = 'getgist.__main__.input'
except ImportError:
    from unittest.mock import patch
    from urllib.request import urlopen
    input_function = 'builtins.input'

test_user = 'cuducos'
test_gist = '.vimrc'


class TestAPI(TestCase):

    def setUp(self):
        self.gist = Gist(test_user, test_gist)

    def test_id(self):
        self.assertTrue(search(r'[\w\d]{16,}', self.gist.id))

    def test_raw_url(self):
        request = urlopen(self.gist.raw_url)
        self.assertEqual(request.getcode(), 200)


class TestDownload(TestCase):

    def setUp(self):
        self.gist = Gist(test_user, test_gist)

    def tearDown(self):
        for file_name in os.listdir(self.gist.local_dir):
            if search(r'^({})(\.bkp(.\d)?)?$'.format(test_gist), file_name):
                os.remove(os.path.join(self.gist.local_dir, file_name))

    @patch(input_function)
    def test_local_dir(self, mocked_input):
        mocked_input.return_value = 'y'
        self.assertTrue(os.path.exists(self.gist.local_dir))
        self.assertTrue(os.path.isdir(self.gist.local_dir))

    @patch(input_function)
    def test_download(self, mocked_input):
        mocked_input.return_value = 'y'
        self.gist.save()
        self.assertTrue(os.path.exists(self.gist.local_path))

    @patch(input_function)
    def test_backup(self, mocked_input):

        # mock input value
        mocked_input.return_value = 'n'

        # backup filenames
        backup1 = '{}.bkp'.format(self.gist.local_path)
        backup2 = '{}.bkp.1'.format(self.gist.local_path)

        # 1st download
        self.gist.save()
        self.assertTrue(os.path.exists(self.gist.local_path))

        # 2nd download
        self.gist.save()
        self.assertTrue(os.path.exists(backup1))

        # 3rd download
        self.gist.save()
        self.assertTrue(os.path.exists(backup2))

        # 4th download
        self.gist.save()
