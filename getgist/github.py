from decouple import config
from pkg_resources import get_distribution

from . import GetGistCommons
from .requests import GetGistRequests


class GitHubTools(GetGistCommons):

    def __init__(self, user, assume_yes=False):

        # GitHub API main settings and entrypoints
        self.version = get_distribution('getgist').version
        self.user = user
        self.assume_yes = assume_yes
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
            self.oops('Invalid token for user ' + self.user)
            self.headers.pop('Authorization')
            return

        self.is_authenticated = True
        self.yeah('User {} authenticated'.format(self.user))

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
            self.oops('User `{}` not found'.format(self.user))
            return

        # abort if there are no gists
        resp = raw_resp.json()
        if not resp:
            self.oops('No gists found for user `{}`'.format(self.user))
            return

        # parse response
        for gist in raw_resp.json():
            yield self._parse_gist(gist)

    def select_gist(self, filename):
        """
        Get a list of gists (from self.get_gists) and return the one that
        contain the filename offered as an argument (str). If more than one
        gist is found with the given filename, user is asked to choose.
        Returns the dictionary of the selected gist
        """

        # pick up all macthing gists
        matches = list()
        for gist in self.get_gists():
            for gist_file in gist.get('files'):
                if filename == gist_file.get('filename'):
                    matches.append(gist)

        # abort if no match is found
        if not matches:
            msg = "No file named `{}` found in {}'s gists"
            self.oops(msg.format(filename, self.user))
            if not self.is_authenticated:
                self.warn('To access private gists set the GETGIST_TOKEN')
                self.warn('(see `getgist --help` for details)')
            return False

        # return if there's is only one match
        if len(matches) == 1 or self.assume_yes:
            return matches.pop(0)

        return self._ask_which_gist(filename, matches)

    def read_gist_file(self, gist, filename):
        """Return the contents of a gist"""
        url = False
        files = gist.get('files')
        for f in files:
            if f.get('filename') == filename:
                url = f.get('raw_url')
                break
        if url:
            self.output('Reading {}'.format(url))
            response = self.requests.get(url)
            return response.content

    def _ask_which_gist(self, filename, matches):

        # ask user which gist to use
        self.hey('Use {} from which gist?'.format(filename))
        for count, gist in enumerate(matches, 1):
            self.hey('[{}] {}'.format(count, gist.get('description')))

        # get the gist index
        selected = False
        while not selected:
            try:
                gist_index = int(self.ask('Type the number: ')) - 1
                selected = matches[gist_index]
            except (ValueError, IndexError):
                self.oops('Invalid number, please try again.')

        self.output('Using `{}` Gist'.format(selected['description']))
        return selected

    def _api_url(self, *args):
        """Get entrypoints adding arguments separated by slashes"""
        return self.api_root_url + '/'.join(args)

    @staticmethod
    def _parse_gist(gist):
        """Receive a gist (dict) and parse it to GetGist"""

        # parse files
        files = list()
        file_names = sorted(filename for filename in gist['files'].keys())
        for name in file_names:
            files.append(dict(filename=name,
                              raw_url=gist['files'][name].get('raw_url')))

        # parse description
        description = gist['description']
        if not description:
            names = sorted(f.get('filename') for f in files)
            description = names.pop(0)

        return dict(description=description, id=gist.get('id'), files=files)

    @staticmethod
    def _get_token():
        return config('GETGIST_TOKEN', default=None)
