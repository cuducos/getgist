try:
    from unittest import TestCase
except ImportError:
    from unittest2 import TestCase

from getgist.request import GetGistRequests


class TestGetGistRequestsInit(TestCase):

    def test_no_header(self):
        requests = GetGistRequests()
        self.assertIsInstance(requests.headers, dict)

    def test_update_header(self):
        requests = GetGistRequests({'foo': 'bar'})
        self.assertEqual(requests.headers['foo'], 'bar')


class TestGetGistRequestsAddHeader(TestCase):

    def test_add_header(self):
        requests = GetGistRequests({'foo': 'bar'})
        got = requests.add_headers({'headers': {'bar': 'foo'}})
        self.assertEqual({'headers': {'foo': 'bar', 'bar': 'foo'}}, got)
