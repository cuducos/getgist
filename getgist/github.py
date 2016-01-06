import requests

from . import GetGistCommons


class GitHubTools(GetGistCommons):

    def __init__(self, user):

        # GitHub API main settings and entrypoints
        self.user = user
        self.api_root_url = 'https://api.github.com/'
        self.headers = {'Accept': 'application/vnd.github.v3+json',
                        'User-Agent': 'GetGist-app'}

    def api_url(self, *args):
        """Construct API entrypoints adding args separated by slashes"""
        return self.api_root_url +  '/'.join(args)

    def request(self, method, url, data=None, kwargs={}):
        """Encapsulate requests lib to always send self.headers as headers"""

        methods = dict(get=requests.get, patch=requests.patch)
        return_method = methods.get(method)

        if not return_method:
            return False

        return return_method(url, data=data, headers=self.headers, **kwargs)

    def get_gists(self):

        # fetch all gists
        url = self.api_url('users', self.user, 'gists')
        self.output('Fetching ' + url)
        resp = self.request('get', url)
        print(resp.url)

        # parse response
        gists = list()
        for gist in resp.json():
            files = list(gist['files'].keys())
            name = gist['description'] if gist['description'] else files[0]
            gists.append(dict(files=files, name=name))

        return gists
