try:
    from unittest import TestCase
    from unittest.mock import patch
except ImportError:
    from unittest2 import TestCase
    from mock import patch

from getgist.github import GitHubTools
from tests.mocks import MockResponse, parse_mock, request_mock

GETGIST_USER = 'janedoe'
GETGIST_TOKEN = "Jane's token"


class TestAuthentication(TestCase):

    @patch('getgist.github.GitHubTools._get_token')
    def test_no_token_results_in_no_authentication(self, mock_token):
        mock_token.return_value = False
        oops = GitHubTools(GETGIST_USER, '.gist')
        with self.subTest():
            self.assertNotIn('Authorization', oops.headers)
            self.assertFalse(oops.is_authenticated)

    @patch('getgist.request.GetGistRequests.get')
    @patch('getgist.github.GitHubTools._get_token')
    def test_invalid_token(self, mock_token, mock_get):
        mock_token.return_value = GETGIST_TOKEN
        mock_get.return_value = request_mock('user', case=False)
        oops = GitHubTools(GETGIST_USER, '.gist')
        with self.subTest():
            self.assertNotIn('Authorization', oops.headers)
            self.assertFalse(oops.is_authenticated)

    @patch('getgist.request.GetGistRequests.get')
    @patch('getgist.github.GitHubTools._get_token')
    def test_valid_token(self, mock_token, mock_get):
        mock_token.return_value = GETGIST_TOKEN
        mock_get.return_value = request_mock('user')
        yeah = GitHubTools(GETGIST_USER, '.gist')
        with self.subTest():
            self.assertIn('Authorization', yeah.headers)
            self.assertTrue(yeah.is_authenticated)


class GitHubToolsTestCase(TestCase):

    def setUp(self):
        self.github = GitHubTools(GETGIST_USER, '.gist')
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

    @patch('getgist.request.GetGistRequests.get')
    @patch('getgist.github.GitHubTools.add_oauth_header')
    def test_get_gists(self, mock_oauth, mock_get):
        mock_oauth.return_value = None
        mock_get.return_value = request_mock('users/janedoe/gists')
        gists = list(self.github.get_gists())
        with self.subTest():
            self.assertIn(self.gist1, gists)
            self.assertIn(self.gist2, gists)
            self.assertNotIn(self.gist4, gists)

    @patch('getgist.request.GetGistRequests.get')
    @patch('getgist.github.GitHubTools.add_oauth_header')
    def test_no_gists_with_wrong_username(self, mock_oauth, mock_get):
        mock_oauth.return_value = None
        mock_get.return_value = request_mock('users/janedoe/gists',
                                             case=False, status_code=404)
        self.assertFalse(list(self.github.get_gists()))

    @patch('getgist.request.GetGistRequests.get')
    @patch('getgist.github.GitHubTools.add_oauth_header')
    def test_user_with_no_gists(self, mock_oauth, mock_get):
        mock_oauth.return_value = None
        mock_get.return_value = request_mock('users/casper/gists')
        self.assertFalse(list(self.github.get_gists()))

    @patch('getgist.request.GetGistRequests.get')
    @patch('getgist.github.GitHubTools._get_token')
    def test_authenticated_get_gists(self, mock_token, mock_get):
        mock_token.return_value = GETGIST_TOKEN
        mock_get.side_effect = [request_mock('user'), request_mock('gists')]
        yeah = GitHubTools(GETGIST_USER, '.gist')
        gists = list(yeah.get_gists())
        with self.subTest():
            self.assertIn(self.gist3, gists)
            self.assertIn(self.gist4, gists)


class TestAskWhichGist(GitHubToolsTestCase):

    @patch('getgist.request.GetGistRequests.get')
    @patch('getgist.github.GitHubTools.add_oauth_header')
    @patch('getgist.GetGistCommons.ask')
    def test_select_gist_single_input(self, mock_ask, mock_oauth, mock_get):
        mock_ask.return_value = 2
        mock_oauth.return_value = None
        mock_get.return_value = request_mock('users/janedoe/gists')
        self.github.filename = '.gist'
        gists = list(self.github.get_gists())
        self.assertEqual(self.github._ask_which_gist(gists), self.gist2)

    @patch('getgist.request.GetGistRequests.get')
    @patch('getgist.github.GitHubTools.add_oauth_header')
    @patch('getgist.input_method')
    def test_select_gist_multi_input(self, mock_input, mock_oauth, mock_get):
        mock_input.side_effect = ['alpha', '', 2]
        mock_oauth.return_value = None
        mock_get.return_value = request_mock('users/janedoe/gists')
        self.github.filename = '.gist'
        gists = list(self.github.get_gists())
        self.assertEqual(self.github._ask_which_gist(gists), self.gist2)


class TestSelectGist(GitHubToolsTestCase):

    @patch('getgist.request.GetGistRequests.get')
    @patch('getgist.github.GitHubTools.add_oauth_header')
    def test_select_gist_single_match(self, mock_oauth, mock_get):
        mock_oauth.return_value = None
        mock_get.return_value = request_mock('users/janedoe/gists')
        self.github.filename = '.gist.sample'
        self.assertEqual(self.github.select_gist(), self.gist3)

    @patch('getgist.request.GetGistRequests.get')
    @patch('getgist.github.GitHubTools.add_oauth_header')
    def test_select_gist_no_match(self, mock_oauth, mock_get):
        mock_oauth.return_value = None
        mock_get.return_value = request_mock('users/janedoe/gists')
        self.github.filename = '.no_gist'
        self.assertFalse(self.github.select_gist())

    @patch('getgist.request.GetGistRequests.get')
    @patch('getgist.github.GitHubTools.add_oauth_header')
    def test_select_gist_no_match_allow_none(self, mock_get):
        mock_get.return_value = request_mock('users/janedoe/gists')
        self.github.filename = '.no_gist'
        self.assertIsNone(self.github.select_gist(allow_none=True))

    @patch('getgist.GetGistCommons.ask')
    def test_select_gist_multi_matches(self, mock_ask, mock_oauth, mock_get):
        mock_ask.return_value = 2
        mock_oauth.return_value = None
        mock_get.return_value = request_mock('users/janedoe/gists')
        self.github.filename = '.gist'
        self.assertEqual(self.github.select_gist(), self.gist2)


class TestReadGist(GitHubToolsTestCase):

    @patch('getgist.request.GetGistRequests.get')
    @patch('getgist.github.GitHubTools.add_oauth_header')
    def test_read_gist(self, mock_oauth, mock_get):
        mock_get.return_value = MockResponse('Hello, world!', 200)
        mock_oauth.return_value = None
        gist_raw = request_mock('gist/id_gist_1')
        gist = self.github._parse_gist(gist_raw.json())
        read = self.github.read_gist_file(gist)
        self.assertEqual(read, 'Hello, world!')


class TestUpdateGist(TestCase):

    @patch('getgist.github.GitHubTools._get_token')
    def test_update_gist_without_authorization(self, mock_token):
        mock_token.return_value = None
        gist = parse_mock(id=1, user=GETGIST_USER, filename='.gist')
        oops = GitHubTools(GETGIST_USER, '.gist.sample')
        self.assertFalse(oops.update(gist, '42'))

    @patch('getgist.request.GetGistRequests.get')
    @patch('getgist.request.GetGistRequests.patch')
    @patch('getgist.github.GitHubTools._get_token')
    def test_update_gist(self, mock_token, mock_patch, mock_get):
        mock_token.return_value = GETGIST_TOKEN
        mock_patch.return_value = request_mock('gist/id_gist_1')
        mock_get.return_value = request_mock('user')
        gist = parse_mock(id=1, user=GETGIST_USER, filename='.gist')
        yeah = GitHubTools(GETGIST_USER, '.gist')
        self.assertTrue(yeah.update(gist, '42'))

    @patch('getgist.request.GetGistRequests.get')
    @patch('getgist.request.GetGistRequests.patch')
    @patch('getgist.github.GitHubTools._get_token')
    def test_failed_update_gist(self, mock_token, mock_patch, mock_get):
        mock_token.return_value = GETGIST_TOKEN
        mock_patch.return_value = request_mock('gist/id_gist_1', case=False,
                                               status_code=404)
        mock_get.return_value = request_mock('user')
        gist = parse_mock(id=1, user=GETGIST_USER, filename='.gist')
        yeah = GitHubTools(GETGIST_USER, '.gist')
        self.assertFalse(yeah.update(gist, '42'))

    @patch('getgist.request.GetGistRequests.get')
    @patch('getgist.github.GitHubTools._get_token')
    def test_create_gist_with_no_file(self, mock_token, mock_get):
        mock_token.return_value = GETGIST_TOKEN
        mock_get.return_value = request_mock('user')
        gist = parse_mock(id=1, user=GETGIST_USER, filename='.gist')
        yeah = GitHubTools(GETGIST_USER, '.gist')
        self.assertFalse(yeah.update(gist, False))


class TestCreateGist(TestCase):

    @patch('getgist.github.GitHubTools._get_token')
    def test_create_gist_without_authorization(self, mock_token):
        mock_token.return_value = None
        oops = GitHubTools(GETGIST_USER, '.gist.sample')
        self.assertFalse(oops.create('42'))

    @patch('getgist.request.GetGistRequests.get')
    @patch('getgist.request.GetGistRequests.post')
    @patch('getgist.github.GitHubTools._get_token')
    def test_create_gist(self, mock_token, mock_post, mock_get):
        mock_token.return_value = GETGIST_TOKEN
        mock_post.return_value = request_mock('gist/id_gist_1',
                                              status_code=201)
        mock_get.return_value = request_mock('user')
        yeah = GitHubTools(GETGIST_USER, '.gist.sample')
        self.assertTrue(yeah.create('42', public=False))

    @patch('getgist.request.GetGistRequests.get')
    @patch('getgist.request.GetGistRequests.post')
    @patch('getgist.github.GitHubTools._get_token')
    def test_failed_create_gist(self, mock_token, mock_post, mock_get):
        mock_token.return_value = GETGIST_TOKEN
        mock_post.return_value = request_mock('gist/id_gist_1', case=False,
                                              status_code=404)
        mock_get.return_value = request_mock('user')
        yeah = GitHubTools(GETGIST_USER, '.gist.sample')
        self.assertFalse(yeah.create('42', public=False))

    @patch('getgist.request.GetGistRequests.get')
    @patch('getgist.github.GitHubTools._get_token')
    def test_create_gist_with_no_file(self, mock_token, mock_get):
        mock_token.return_value = GETGIST_TOKEN
        mock_get.return_value = request_mock('user')
        yeah = GitHubTools(GETGIST_USER, '.gist')
        self.assertFalse(yeah.create(False))
