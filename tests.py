import os
from getgist import Gist
from re import search
from unittest import TestCase
try:
    from urllib2 import urlopen
except ImportError:
    from urllib.request import urlopen

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
        self.gist = Gist(test_user, test_gist, True)

    def tearDown(self):
        for file_name in os.listdir(self.gist.local_dir):
            if search(r'^({})(\.bkp(.\d)?)?$'.format(test_gist), file_name):
                os.remove(os.path.join(self.gist.local_dir, file_name))

    def test_local_dir(self):
        self.assertTrue(os.path.exists(self.gist.local_dir))
        self.assertTrue(os.path.isdir(self.gist.local_dir))

    def test_download(self):
        self.gist.save()
        self.assertTrue(os.path.exists(self.gist.local_path))
