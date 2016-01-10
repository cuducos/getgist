from unittest import TestCase
from unittest.mock import patch

from getgist.github import GitHubTools
from tests.mocks import parse_mock, request_mock

GETGIST_USER = 'janedoe'
GETGIST_TOKEN = "Jane's token"


class TestAuthentication(TestCase):

    @patch('getgist.github.GitHubTools._get_token')
    def test_no_token_results_in_no_authentication(self, mock_token):
        mock_token.return_value = False
        oops = GitHubTools(GETGIST_USER)
        with self.subTest():
            self.assertNotIn('Authorization', oops.headers)
            self.assertFalse(oops.is_authenticated)

    @patch('getgist.requests.GetGistRequests.get')
    @patch('getgist.github.GitHubTools._get_token')
    def test_invalid_token(self, mock_token, mock_get):
        mock_token.return_value = GETGIST_TOKEN
        mock_get.return_value = request_mock('user', case=False)
        oops = GitHubTools(GETGIST_USER)
        with self.subTest():
            self.assertNotIn('Authorization', oops.headers)
            self.assertFalse(oops.is_authenticated)

    @patch('getgist.requests.GetGistRequests.get')
    @patch('getgist.github.GitHubTools._get_token')
    def test_valid_token(self, mock_token, mock_get):
        mock_token.return_value = GETGIST_TOKEN
        mock_get.return_value = request_mock('user')
        yeah = GitHubTools(GETGIST_USER)
        with self.subTest():
            self.assertIn('Authorization', yeah.headers)
            self.assertTrue(yeah.is_authenticated)


class GitHubToolsTestCase(TestCase):

    def setUp(self):
        self.github = GitHubTools(GETGIST_USER)
        self.gist1 = parse_mock(id=1, user=GETGIST_USER, filename='.gist')
        self.gist2 = parse_mock(id=2, user=GETGIST_USER, filename='.gist',
                                description='Description of Gist 2')
        self.gist3 = parse_mock(id=3, user=GETGIST_USER,
                                filename=['.gist.sample', '.gist.dev'])
        self.gist4 = parse_mock(id=4, user=GETGIST_USER, filename='.gist.prod')


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


class TestParseGist(GitHubToolsTestCase):

    def test_parse_gist(self):
        gist_raw = request_mock('gist/id_gist_1')
        gist = gist_raw.json()
        self.assertEqual(self.github._parse_gist(gist), self.gist1)


class TestGetGists(GitHubToolsTestCase):

    @patch('getgist.requests.GetGistRequests.get')
    @patch('getgist.github.GitHubTools.add_oauth_header')
    def test_get_gists(self, mock_oauth, mock_get):
        mock_oauth.return_value = None
        mock_get.return_value = request_mock('users/janedoe/gists')
        gists = list(self.github.get_gists())
        with self.subTest():
            self.assertIn(self.gist1, gists)
            self.assertIn(self.gist2, gists)
            self.assertNotIn(self.gist4, gists)

    @patch('getgist.requests.GetGistRequests.get')
    @patch('getgist.github.GitHubTools.add_oauth_header')
    def test_no_gists_with_wrong_username(self, mock_oauth, mock_get):
        mock_oauth.return_value = None
        mock_get.return_value = request_mock('users/janedoe/gists',
                                             case=False, status_code=404)
        self.assertFalse(list(self.github.get_gists()))

    @patch('getgist.requests.GetGistRequests.get')
    @patch('getgist.github.GitHubTools.add_oauth_header')
    def test_user_with_no_gists(self, mock_oauth, mock_get):
        mock_oauth.return_value = None
        mock_get.return_value = request_mock('users/casper/gists')
        self.assertFalse(list(self.github.get_gists()))

    @patch('getgist.requests.GetGistRequests.get')
    @patch('getgist.github.GitHubTools._get_token')
    def test_authenticated_get_gists(self, mock_token, mock_get):
        mock_token.return_value = GETGIST_TOKEN
        mock_get.side_effect = [request_mock('user'), request_mock('gists')]
        yeah = GitHubTools(GETGIST_USER)
        gists = list(yeah.get_gists())
        with self.subTest():
            self.assertIn(self.gist3, gists)
            self.assertIn(self.gist4, gists)


class TestSelectGist(GitHubToolsTestCase):

    @patch('getgist.requests.GetGistRequests.get')
    @patch('getgist.github.GitHubTools.add_oauth_header')
    def test_select_gist_single_match(self, mock_oauth, mock_get):
        mock_oauth.return_value = None
        mock_get.return_value = request_mock('users/janedoe/gists')
        self.assertEqual(self.github.select_gist('.gist.sample'), self.gist3)

    # TODO: write test_select_gist_multiple_macthes
