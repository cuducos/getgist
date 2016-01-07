from decouple import config
from requests import get, patch

from . import GetGistCommons


class GitHubTools(GetGistCommons):

    def __init__(self, user):

        # GitHub API main settings and entrypoints
        self.user = user
        self.api_root_url = 'https://api.github.com/'
        self.headers = {'Accept': 'application/vnd.github.v3+json',
                        'User-Agent': 'GetGist-app'}

        # OAuth via token
        self.token = config('GETGIST_TOKEN', default=None)
        self.auth = self.validate_token()

    def api_url(self, *args):
        """Construct API entrypoints adding args separated by slashes"""
        return self.api_root_url +  '/'.join(args)

    def request(self, method, url, data=None, kwargs={}):
        """Encapsulate requests lib to always send self.headers as headers"""

        methods = dict(get=get, patch=patch)
        return_method = methods.get(method)
        if not return_method:
            return False

        return return_method(url, data=data, headers=self.headers, **kwargs)

    def get_gists(self):

        # fetch all gists
        url = self.api_url('users', self.user, 'gists')
        self.output('Fetching ' + url)
        resp = self.request('get', url)

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
        raw_resp = self.request('get', url)
        resp = raw_resp.json()

        # validate
        if resp.get('login') != self.user:
            self.output('Invalid token for user ' + self.user)
            self.headers.pop('Authorization')
            return False
        return True
