from decouple import config
from pkg_resources import get_distribution

from . import GetGistCommons
from .requests import GetGistRequests


class GitHubTools(GetGistCommons):

    def __init__(self, user):

        # GitHub API main settings and entrypoints
        self.version = get_distribution('getgist').version
        self.user = user
        self.api_root_url = 'https://api.github.com/'
        self.headers = {'Accept': 'application/vnd.github.v3+json',
                        'User-Agent': 'GetGist v' + self.version}

        # instantiate GetGistRequests
        self.requests = GetGistRequests(self.headers)

    def get_gists(self):
        """List generator w/ dictionaries w/ Gists' `name` and `files`"""

        # add oauth header
        self._oauth()

        # fetch all gists
        url = self._api_url('users', self.user, 'gists')
        self.output('Fetching ' + url)
        raw_resp = self.requests.get(url)

        # abort if user not found
        if raw_resp.status_code != 200:
            self.output('User `{}` not found'.format(self.user))
            return

        # abort if there are no gists
        resp = raw_resp.json()
        if not resp:
            self.output('No gists found for user `{}`'.format(self.user))
            return

        # parse response
        for gist in raw_resp.json():
            files = list(gist['files'].keys())
            name = gist['description'] if gist['description'] else files[0]
            yield dict(files=files, name=name)

    def _api_url(self, *args):
        """Get entrypoints adding arguments separated by slashes"""
        return self.api_root_url + '/'.join(args)

    def _oauth(self):
        """Validate the OAuth token and add the proper headers for requests"""

        # abort if no token
        oauth_token = self._get_token()
        if not oauth_token:
            return

        # add oauth header & try to reach the api
        self.headers['Authorization'] = 'token ' + oauth_token
        url = self._api_url('user')
        raw_resp = self.requests.get(url)
        resp = raw_resp.json()

        # remove header if token is invalid
        if resp.get('login', None) != self.user:
            self.output('Invalid token for user ' + self.user)
            self.headers.pop('Authorization')

    @staticmethod
    def _get_token():
        return config('GETGIST_TOKEN', default=None)
