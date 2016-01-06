from unittest import TestCase

from getgist.github import GitHubTools


class GitHubToolsTest(TestCase):

    def setUp(self):
        self.github = GitHubTools('cuducos')


class TestApiUrl(GitHubToolsTest):

    def test_api_url(self):
        url = self.github.api_url('cuducos', 'gists')
        self.assertEqual(url, 'https://api.github.com/cuducos/gists')


class TestGetGists(GitHubToolsTest):

    def test_get_gists_non_authenticated(self):
        gists = self.github.get_gists()
        with self.subTest():
            self.assertIn({'name': '.zshrc', 'files': ['.zshrc']}, gists)
            self.assertIn({'name': 'sVim', 'files': ['.svimrc']}, gists)
