from unittest import TestCase
from unittest.mock import patch

from getgist.github import GitHubTools
from tests.mocks import request_mock

GETGIST_USER = 'janedoe'
GETGIST_TOKEN = "Jane's token"


class TestAuthentication(TestCase):

    @patch('getgist.github.GitHubTools._get_token')
    def test_no_token_results_in_no_authentication(self, mock_token):
        mock_token.return_value = False
        oops = GitHubTools(GETGIST_USER)
        self.assertNotIn('Authorization', oops.headers)
        self.assertFalse(oops.is_authenticated)

    @patch('getgist.requests.GetGistRequests.get')
    @patch('getgist.github.GitHubTools._get_token')
    def test_invalid_token(self, mock_token, mock_get):
        mock_token.return_value = GETGIST_TOKEN
        mock_get.return_value = request_mock('user', case=False)
        oops = GitHubTools(GETGIST_USER)
        self.assertNotIn('Authorization', oops.headers)
        self.assertFalse(oops.is_authenticated)

    @patch('getgist.requests.GetGistRequests.get')
    @patch('getgist.github.GitHubTools._get_token')
    def test_valid_token(self, mock_token, mock_get):
        mock_token.return_value = GETGIST_TOKEN
        mock_get.return_value = request_mock('user')
        yeah = GitHubTools(GETGIST_USER)
        self.assertIn('Authorization', yeah.headers)
        self.assertTrue(yeah.is_authenticated)


class GitHubToolsTestCase(TestCase):

    def setUp(self):
        self.github = GitHubTools(GETGIST_USER)


class TestMainHeaders(GitHubToolsTestCase):

    def test_main_headers(self):
        user_agent = self.github.headers.get('User-Agent')
        user_agent_re = r'^(GetGist v)([\d]+).([\d]+)(.[\d]+)?$'
        with self.subTest():
            self.assertIn('Accept', self.github.headers)
            self.assertIn('User-Agent', self.github.headers)
            self.assertRegex(user_agent, user_agent_re)


class TestApiUrl(GitHubToolsTestCase):

    def test_api_url(self):
        url = self.github._api_url('janedoe', 'gists')
        expected = 'https://api.github.com/{}/gists'.format(GETGIST_USER)
        self.assertEqual(url, expected)


class TestGetGists(GitHubToolsTestCase):

    @patch('getgist.requests.GetGistRequests.get')
    def test_get_gists(self, mock_get):
        mock_get.return_value = request_mock('users/janedoe/gists')
        self.github.headers.pop('Authorization', None)
        gists = list(self.github.get_gists())
        with self.subTest():
            self.assertIn({'name': '.gist',
                           'files': ['.gist']}, gists)
            self.assertIn({'name': 'Description of Gist 2',
                           'files': ['.gist']}, gists)
            self.assertNotIn({'name': '.gist.prod',
                              'files': ['gist.prod']}, gists)

    @patch('getgist.requests.GetGistRequests.get')
    def test_no_gists_with_wrong_username(self, mock_get):
        mock_get.return_value = request_mock('users/janedoe/gists',
                                             case=False, status_code=404)
        self.assertFalse(list(self.github.get_gists()))

    @patch('getgist.requests.GetGistRequests.get')
    def test_authenticated_get_gists(self, mock_get):
        mock_get.return_value = request_mock('gists')
        gists = list(self.github.get_gists())
        self.assertIn({'name': '.gist.prod', 'files': ['.gist.prod']}, gists)
