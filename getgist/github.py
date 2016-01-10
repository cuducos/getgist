from decouple import config
from pkg_resources import get_distribution

from . import GetGistCommons
from .requests import GetGistRequests


class GitHubTools(GetGistCommons):

    def __init__(self, user):

        # GitHub API main settings and entrypoints
        self.version = get_distribution('getgist').version
        self.user = user
        self.is_authenticated = False
        self.api_root_url = 'https://api.github.com/'
        self.headers = {'Accept': 'application/vnd.github.v3+json',
                        'User-Agent': 'GetGist v' + self.version}
        self.requests = GetGistRequests(self.headers)
        self.add_oauth_header()

    def add_oauth_header(self):
        """Validate token and add the proper header for further requests"""

        # abort if no token
        oauth_token = self._get_token()
        if not oauth_token:
            return

        # add oauth header & reach the api
        self.headers['Authorization'] = 'token ' + oauth_token
        url = self._api_url('user')
        raw_resp = self.requests.get(url)
        resp = raw_resp.json()

        # abort & remove header if token is invalid
        if resp.get('login', None) != self.user:
            self.output('Invalid token for user ' + self.user)
            self.headers.pop('Authorization')
            return

        self.is_authenticated = True

    def get_gists(self):
        """List generator w/ dictionaries w/ Gists' `name` and `files`"""

        # fetch all gists
        if self.is_authenticated:
            url = self._api_url('gists')
        else:
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
            yield self._parse_gist(gist)

    def _api_url(self, *args):
        """Get entrypoints adding arguments separated by slashes"""
        return self.api_root_url + '/'.join(args)

    @staticmethod
    def _parse_gist(gist):
        """Receive a gist (dict, from json.loads()) and parse it to GetGist"""

        # parse files
        files = list()
        file_names = sorted(filename for filename in gist['files'].keys())
        for name in file_names:
            files.append(dict(filename=name,
                              raw_url=gist['files'][name].get('raw_url')))

        # parse description
        description = gist['description']
        if not description:
            names = sorted(f['filename'] for f in files)
            description = names.pop(0)

        return dict(files=files, description=description)

    @staticmethod
    def _get_token():
        return config('GETGIST_TOKEN', default=None)
