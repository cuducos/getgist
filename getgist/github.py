from decouple import config
from json import dumps
from pkg_resources import get_distribution

from getgist import GetGistCommons
from getgist.requests import GetGistRequests


def oauth_only(function):
    """Decorator to restrict some GitHubTools methods to run only with OAuth"""
    def check_for_oauth(self, *args, **kwargs):
        if not self.is_authenticated:
            self.oops('To use putgist you have to set your GETGIST_TOKEN')
            self.oops('(see `putgist --help` for details)')
            return False
        return function(self, *args, **kwargs)
    return check_for_oauth


class GitHubTools(GetGistCommons):
    """Helpers to deal with GitHub API and manipulate gists"""

    def __init__(self, user, filename, assume_yes=False):
        """
        Save basic variables to all methods, instantiate GetGistrequests and
        calls the OAuth method.
        :param user: (str) GitHub username
        :param filename: (str) filename to be saved (locally), created or
        updated (remotelly)
        :param assume_yes: (bool) assume yes (or first option) for all prompts
        :return: (None)
        """
        # GitHub API main settings and entrypoints
        self.version = get_distribution('getgist').version
        self.user = user
        self.filename = filename
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

    def select_gist(self, allow_none=False):
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
                if self.filename == gist_file.get('filename'):
                    matches.append(gist)

        # abort if no match is found
        if not matches:
            if allow_none:
                return None
            else:
                msg = "No file named `{}` found in {}'s gists"
                self.oops(msg.format(self.filename, self.user))
                if not self.is_authenticated:
                    self.warn('To access private gists set the GETGIST_TOKEN')
                    self.warn('(see `getgist --help` for details)')
                return False

        # return if there's is only one match
        if len(matches) == 1 or self.assume_yes:
            return matches.pop(0)

        return self._ask_which_gist(matches)

    def read_gist_file(self, gist):
        """Return the contents of a gist"""
        url = False
        files = gist.get('files')
        for gist_file in files:
            if gist_file.get('filename') == self.filename:
                url = gist_file.get('raw_url')
                break
        if url:
            self.output('Reading {}'.format(url))
            response = self.requests.get(url)
            return response.content

    @oauth_only
    def update(self, gist, content):

        # request
        url = self._api_url('gists', gist.get('id'))
        data = {'files': {self.filename: {'content': content}}}
        self.output('Sending contents of {} to {}'.format(self.filename, url))
        response = self.requests.patch(url, data=dumps(data))

        # error
        if response.status_code != 200:
            self.oops('Could not update ' + gist.get('description'))
            self.oops('PATCH request returned ' + str(response.status_code))
            return False

        # success
        self.yeah('Done!')
        return True

    @oauth_only
    def create(self, content, **kwargs):

        # set new gist
        public = bool(kwargs.get('public', True))
        data = {'description': self.filename, 'public': public,
                'files': {self.filename: {'content': content}}}

        # send request
        url = self._api_url('gists')
        self.output('sending contents of {} to {}'.format(self.filename, url))
        response = self.requests.post(url, data=dumps(data))

        # error
        if response.status_code != 201:
            self.oops('Could not create ' + self.filename)
            self.oops('POST request returned ' + str(response.status_code))
            return False

        # success
        self.yeah('Done!')
        return True

    def _ask_which_gist(self, matches):

        # ask user which gist to use
        self.hey('Use {} from which gist?'.format(self.filename))
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
