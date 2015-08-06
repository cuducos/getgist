from __future__ import absolute_import

from getgist.__main__ import Gist
from unittest import TestCase

try:
    from mock import patch
    input_function = 'getgist.__main__.input'
except ImportError:
    from unittest.mock import patch
    input_function = 'builtins.input'


class TestSelectFile(TestCase):

    @patch('getgist.__main__.Gist.filter_gists')
    def test_select_file_with_one_option(self, mocked):
        mocked.return_value = [{'id': 12345,
                                'description': 'Gist #1',
                                'raw_url': 'URL #1'}]
        g = Gist('user', 'file')
        self.assertEqual(g.id, 12345)
        self.assertEqual(g.raw_url, 'URL #1')

    @patch(input_function)
    @patch('getgist.__main__.Gist.filter_gists')
    def test_select_file_with_two_options(self, mocked_filter, mocked_input):
        mocked_filter.return_value = [{'id': 12345,
                                       'description': 'Gist #1',
                                       'raw_url': 'URL #1'},
                                      {'id': 67890,
                                       'description': 'Gist #2',
                                       'raw_url': 'URL #2'}]
        mocked_input.return_value = '2'
        g = Gist('user', 'file')
        self.assertEqual(g.id, 67890)
        self.assertEqual(g.raw_url, 'URL #2')

    @patch('getgist.__main__.Gist.filter_gists')
    def test_select_file_with_no_option(self, mocked):
        mocked.return_value = list()
        g = Gist('user', 'file')
        self.assertFalse(g.id, None)
        self.assertFalse(g.raw_url, None)
