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

        # intantiate GetGistRequests
        self.requests = GetGistRequests(self.headers)

        # OAuth via token
        self.token = config('GETGIST_TOKEN', default=None)
        self.auth = self.validate_token()

    def api_url(self, *args):
        """Construct API entrypoints adding args separated by slashes"""
        return self.api_root_url + '/'.join(args)

    def get_gists(self):

        # fetch all gists
        url = self.api_url('users', self.user, 'gists')
        self.output('Fetching ' + url)
        resp = self.requests.get(url)

        # parse response
        gists = list()
        for gist in resp.json():
            files = list(gist['files'].keys())
            name = gist['description'] if gist['description'] else files[0]
            gists.append(dict(files=files, name=name))

        return gists

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

        # validate
        if resp.get('login', None) != self.user:
            self.output('Invalid token for user ' + self.user)
            self.headers.pop('Authorization')
            return False
        return True
