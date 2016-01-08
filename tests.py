from decouple import config
from unittest import TestCase
from unittest.mock import patch

from getgist.github import GitHubTools

GETGIST_USER = config('GETGIST_USER', default='janedoe')
GETGIST_TOKEN = config('GETGIST_TOKEN', default="Jane Doe's token")


class TestAuthentication(TestCase):

    def test_valid_token(self):
        yeah = GitHubTools(GETGIST_USER)
        yeah._oauth()
        self.assertIn('Authorization', yeah.headers)

    def test_invalid_token(self):
        oops = GitHubTools('not_cuducos')
        oops._oauth()
        self.assertNotIn('Authorization', oops.headers)

    @patch('getgist.github.config')
    def test_no_token_results_in_no_authentication(self, mock_config):
        mock_config.return_value = None
        oops = GitHubTools(GETGIST_USER)
        self.assertNotIn('Authorization', oops.headers)


class GitHubToolsTests(TestCase):

    def setUp(self):
        self.github = GitHubTools(GETGIST_USER)


class TestMainHeaders(GitHubToolsTests):

    def test_main_headers(self):
        user_agent = self.github.headers.get('User-Agent')
        user_agent_re = r'^(GetGist v)([\d]+).([\d]+)(.[\d]+)?$'
        with self.subTest():
            self.assertIn('Accept', self.github.headers)
            self.assertIn('User-Agent', self.github.headers)
            self.assertRegex(user_agent, user_agent_re)


class TestApiUrl(GitHubToolsTests):

    def test_api_url(self):
        url = self.github._api_url('cuducos', 'gists')
        expected = 'https://api.github.com/{}/gists'.format(GETGIST_USER)
        self.assertEqual(url, expected)


class TestGetGists(GitHubToolsTests):

    def test_get_gists_non_authenticated(self):
        self.github.headers.pop('Authorization', None)
        gists = self.github.get_gists()
        with self.subTest():
            self.assertIn({'name': '.zshrc', 'files': ['.zshrc']}, gists)
            self.assertIn({'name': 'sVim', 'files': ['.svimrc']}, gists)
            self.assertNotIn({'name': 'PrivateGist', 'files': ['test.txt']},
                             gists)

    def test_get_gist_authenticated(self):
        gists = self.github.get_gists()
        self.assertIn({'name': 'PrivateGist', 'files': ['test.txt']}, gists)

    def test_no_gists_with_wrong_username(self):
        oops = GitHubTools('not_janedoe')
        self.assertFalse(list(oops.get_gists()))
