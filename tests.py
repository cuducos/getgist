from decouple import config
from unittest import TestCase

from getgist.github import GitHubTools

GETGIST_USER = config('GETGIST_USER', default='janedoe')
GETGIST_TOKEN = config('GETGIST_TOKEN', default="Jane Doe's token")


class GitHubToolsTests(TestCase):

    def setUp(self):
        self.github = GitHubTools(GETGIST_USER)


class TestApiUrl(GitHubToolsTests):

    def test_api_url(self):
        url = self.github.api_url('cuducos', 'gists')
        expected = 'https://api.github.com/{}/gists'.format(GETGIST_USER)
        self.assertEqual(url, expected)


class TestAuthentication(GitHubToolsTests):

    def test_valid_token(self):
        with self.subTest():
            self.assertTrue(self.github.validate_token())
            self.assertIn('Authorization', self.github.headers)

    def test_invalid_token(self):
        oops = GitHubTools('not_cuducos')
        with self.subTest():
            self.assertFalse(oops.validate_token())
            self.assertNotIn('Authorization', oops.headers)


class TestGetGists(GitHubToolsTests):

    def test_get_gists_non_authenticated(self):
        self.github.headers.pop('Authorization')
        gists = self.github.get_gists()
        with self.subTest():
            self.assertIn({'name': '.zshrc', 'files': ['.zshrc']}, gists)
            self.assertIn({'name': 'sVim', 'files': ['.svimrc']}, gists)
            self.assertNotIn({'name': 'PrivateGist', 'files': ['test.txt']},
                             gists)

    def test_get_gist_authenticated(self):
        gists = self.github.get_gists()
        self.assertIn({'name': 'PrivateGist', 'files': ['test.txt']}, gists)
