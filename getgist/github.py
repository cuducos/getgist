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

        # OAuth via token
        self.token = config('GETGIST_TOKEN', default=None)
        self.auth = self._validate_token()

    def get_gists(self):
        """List generator w/ dictionaries w/ Gists' `name` and `files`"""

        # fetch all gists
        url = self._api_url('users', self.user, 'gists')
        self.output('Fetching ' + url)
        raw_resp = self.requests.get(url)

        # abort if user not found
        if raw_resp.status_code != 200:
            self.output('User `{}` not found'.format(self.user))
            raise StopIteration

        # parse response
        for gist in raw_resp.json():
            files = list(gist['files'].keys())
            name = gist['description'] if gist['description'] else files[0]
            yield dict(files=files, name=name)

    def _api_url(self, *args):
        """Get entrypoints adding arguments separated by slashes"""
        return self.api_root_url + '/'.join(args)

    def _validate_token(self):
        """Validate the token and add the proper headers for requests"""

        # abort if no token
        if not self.token:
            return False

        # reach api w/ the token
        self.headers['Authorization'] = 'token ' + self.token
        url = self._api_url('user')
        raw_resp = self.requests.get(url)
        resp = raw_resp.json()

        # abort if invalid
        if resp.get('login', None) != self.user:
            self.output('Invalid token for user ' + self.user)
            self.headers.pop('Authorization')
            return False

        return True
