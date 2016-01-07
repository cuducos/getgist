from decouple import config

from . import GetGistCommons
from .requests import GetGistRequests


class GitHubTools(GetGistCommons):

    def __init__(self, user):

        # GitHub API main settings and entrypoints
        self.user = user
        self.api_root_url = 'https://api.github.com/'
        self.headers = {'Accept': 'application/vnd.github.v3+json',
                        'User-Agent': 'GetGist-app'}

        # instantiate GetGistRequests
        self.requests = GetGistRequests(self.headers)

        # OAuth via token
        self.token = config('GETGIST_TOKEN', default=None)
        self.auth = self.validate_token()

    def api_url(self, *args):
        """Get entrypoints adding arguments separated by slashes"""
        return self.api_root_url + '/'.join(args)

    def get_gists(self):
        """List generator w/ dictionaries w/ Gists' `name` and `files`"""

        # fetch all gists
        url = self.api_url('users', self.user, 'gists')
        self.output('Fetching ' + url)
        resp = self.requests.get(url)

        # abort if not found
        if resp.status_code != 200:
            self.output('No gists found. Check if the username is correct.')
            raise StopIteration

        # parse response
        for gist in resp.json():
            files = list(gist['files'].keys())
            name = gist['description'] if gist['description'] else files[0]
            yield dict(files=files, name=name)

    def validate_token(self):
        """Validate the token and add the proper headers for requests"""

        # if no token, return False
        if not self.token:
            return False

        # reach api w/ the token
        self.headers['Authorization'] = 'token ' + self.token
        url = self.api_url('user')
        raw_resp = self.requests.get(url)
        resp = raw_resp.json()

        # abort if invalid
        if resp.get('login', None) != self.user:
            self.output('Invalid token for user ' + self.user)
            self.headers.pop('Authorization')
            return False

        return True
