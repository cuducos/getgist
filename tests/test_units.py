from config import config, MockAPI
from getgist.__main__ import Gist, MyGist
from hashlib import md5
from unittest import TestCase

try:
    from mock import patch
except ImportError:
    from unittest.mock import patch


class TestInit(TestCase):

    @patch('getgist.__main__.Gist.curl')
    def test_init_for_getgist(self, mocked_curl):
        mocked_curl.return_value = config['json']
        gist = Gist(config['user'], config['file'])
        hashed_url = md5(gist.raw_url.encode('utf-8')).hexdigest()
        self.assertEqual(gist.id, '409fac6ac23bf515f495')
        self.assertEqual(hashed_url, '847fe81c7fdc3b6bd7184379fcd42773')

    @patch('getgist.__main__.Gist.ask')
    @patch('getgist.__main__.Gist.curl')
    def test_init_for_mygist(self, mocked_curl, mocked_input):
        mocked_curl.return_value = config['json']
        mocked_input.return_value = config['user']
        gist = MyGist(config['file'])
        hashed_url = md5(gist.raw_url.encode('utf-8')).hexdigest()
        self.assertEqual(gist.id, '409fac6ac23bf515f495')
        self.assertEqual(hashed_url, '847fe81c7fdc3b6bd7184379fcd42773')

    @patch('getgist.__main__.Gist.curl')
    def test_init_with_no_result(self, mocked_curl):
        api = MockAPI(config['file'], 0)
        mocked_curl.return_value = api.get_json()
        gist = MyGist(config['file'])
        self.assertFalse(gist.id)
        self.assertFalse(gist.raw_url)


class TestConfig(TestCase):

    @patch('getgist.__main__.Gist.curl')
    def test_config_for_getgist(self, mocked_curl):
        mocked_curl.return_value = config['json']
        gist = Gist(config['user'], config['file'])
        self.assertEqual(gist.user, config['user'])
        self.assertEqual(gist.file_name, config['file'])
        self.assertFalse(gist.assume_yes)

    @patch('getgist.__main__.Gist.ask')
    @patch('getgist.__main__.Gist.curl')
    def test_config_for_mygist(self, mocked_curl, mocked_input):
        mocked_curl.return_value = config['json']
        mocked_input.return_value = config['user']
        gist = MyGist(config['file'])
        self.assertEqual(gist.user, config['user'])
        self.assertEqual(gist.file_name, config['file'])
        self.assertFalse(gist.assume_yes)

    @patch('getgist.__main__.Gist.curl')
    def test_config_for_getgist_assume_yes(self, mocked_curl):
        mocked_curl.return_value = config['json']
        gist = Gist(config['user'], config['file'], True)
        self.assertEqual(gist.user, config['user'])
        self.assertEqual(gist.file_name, config['file'])
        self.assertTrue(gist.assume_yes)

    @patch('getgist.__main__.Gist.ask')
    @patch('getgist.__main__.Gist.curl')
    def test_config_for_mygist_assume_yes(self, mocked_curl, mocked_input):
        mocked_curl.return_value = config['json']
        mocked_input.return_value = config['user']
        gist = MyGist(config['file'], True)
        self.assertEqual(gist.user, config['user'])
        self.assertEqual(gist.file_name, config['file'])
        self.assertTrue(gist.assume_yes)


class TestLoadGistInfo(TestCase):

    @patch('getgist.__main__.Gist.filter_gists')
    def test_select_file_with_one_option(self, mocked):
        one_option = [{'id': 12345,
                       'description': 'Gist #1',
                       'raw_url': 'URL #1'}]
        mocked.return_value = one_option
        gist = Gist(config['user'], config['file'])
        self.assertEqual(gist.load_gist_info(), one_option[0])

    @patch('getgist.__main__.Gist.ask')
    @patch('getgist.__main__.Gist.filter_gists')
    def test_select_file_with_two_options(self, mocked_filter, mocked_input):
        two_options = [{'id': 12345,
                        'description': 'Gist #1',
                        'raw_url': 'URL #1'},
                       {'id': 67890,
                        'description': 'Gist #2',
                        'raw_url': 'URL #2'}]
        mocked_filter.return_value = two_options
        mocked_input.return_value = '2'
        gist = Gist(config['user'], config['file'])
        self.assertEqual(gist.load_gist_info(), two_options[1])

    @patch('getgist.__main__.Gist.filter_gists')
    def test_select_file_with_no_option(self, mocked):
        mocked.return_value = list()
        gist = Gist(config['user'], config['file'])
        self.assertFalse(gist.load_gist_info())


class TestFilterGists(TestCase):

    @patch('getgist.__main__.Gist.curl')
    def test_with_sample_json(self, mocked_curl):
        mocked_curl.return_value = config['json']
        gist = Gist(config['user'], config['file'])
        filtered = [g for g in gist.filter_gists()]
        hashed_url = md5(filtered[0]['raw_url'].encode('utf-8')).hexdigest()
        self.assertEqual(len(filtered), 1)
        self.assertEqual(filtered[0]['id'], '409fac6ac23bf515f495')
        self.assertEqual(filtered[0]['description'], config['file'])
        self.assertEqual(hashed_url, '847fe81c7fdc3b6bd7184379fcd42773')

    @patch('getgist.__main__.Gist.ask')
    @patch('getgist.__main__.Gist.curl')
    def test_with_two_results(self, mocked_curl, mocked_input):
        api = MockAPI(config['file'], 2)
        mocked_curl.return_value = api.get_json()
        mocked_input.return_value = 1
        gist = Gist(config['user'], config['file'])
        filtered = [g for g in gist.filter_gists()]
        self.assertEqual(len(filtered), 2, api.get_json())
        self.assertEqual(filtered[0]['id'], '1')
        self.assertEqual(filtered[0]['description'], 'Gist #1')
        self.assertEqual(filtered[0]['raw_url'], 'URL #1')
        self.assertEqual(filtered[1]['id'], '2')
        self.assertEqual(filtered[1]['description'], 'Gist #2')
        self.assertEqual(filtered[1]['raw_url'], 'URL #2')

    @patch('getgist.__main__.Gist.curl')
    def test_with_no_result(self, mocked_curl):
        api = MockAPI(config['file'], 0)
        mocked_curl.return_value = api.get_json()
        gist = Gist(config['user'], config['file'])
        filtered = [g for g in gist.filter_gists()]
        self.assertEqual(len(filtered), 0)


class TestSelectFile(TestCase):

    @patch('getgist.__main__.Gist.curl')
    def test_select_file_with_one_option(self, mocked_curl):
        api = MockAPI(config['file'])
        mocked_curl.return_value = api.get_json()
        results = [g for g in api.get_results()]
        gist = Gist(config['user'], config['file'])
        selected = gist.select_file(results)
        self.assertEqual(selected['id'], '1')
        self.assertEqual(selected['raw_url'], 'URL #1')
        self.assertEqual(selected['description'], 'Gist #1')

    @patch('getgist.__main__.Gist.ask')
    @patch('getgist.__main__.Gist.curl')
    def test_select_file_with_two_options(self, mocked_curl, mocked_input):
        api = MockAPI(config['file'], 2)
        mocked_curl.return_value = api.get_json()
        mocked_input.return_value = '2'
        gist = Gist(config['user'], config['file'])
        selected = gist.select_file([g for g in api.get_results()])
        self.assertEqual(selected['id'], '2')
        self.assertEqual(selected['raw_url'], 'URL #2')
        self.assertEqual(selected['description'], 'Gist #2')

    @patch('getgist.__main__.Gist.curl')
    def test_select_file_with_no_option(self, mocked_curl):
        api = MockAPI(config['file'], 0)
        mocked_curl.return_value = api.get_json()
        gist = Gist(config['user'], config['file'])
        selected = gist.select_file([g for g in api.get_results()])
        self.assertFalse(selected)
