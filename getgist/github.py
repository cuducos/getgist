import os
from json import dumps
from pkg_resources import get_distribution

from click import prompt

from getgist import GetGistCommons
from getgist.request import GetGistRequests


class FileFromGist:
    def __init__(self, name, gist, url, public):
        self.name = name
        self.gist = gist
        self.url = url
        self.public = public

    def __str__(self):
        if self.public:
            return self.name
        return "{} [Secret Gist]".format(self.name)

    def __repr__(self):
        return str(
            {
                "name": self.name,
                "gist": self.gist,
                "url": self.url,
                "public": self.public,
            }
        )

    def __eq__(self, other):
        if self.name != other.name:
            return False
        if self.gist != other.gist:
            return False
        if self.url != other.url:
            return False
        if self.public != other.public:
            return False
        return True


def oauth_only(function):
    """Decorator to restrict some GitHubTools methods to run only with OAuth"""

    def check_for_oauth(self, *args, **kwargs):
        """
        Returns False if GitHubTools instance is not authenticated, or return
        the decorated function if it is.
        """
        if not self.is_authenticated:
            self.oops("To use putgist you have to set your GETGIST_TOKEN")
            self.oops("(see `putgist --help` for details)")
            return False
        return function(self, *args, **kwargs)

    return check_for_oauth


def with_filename_only(function):
    """Decorator to restrict some GitHubTools methods to run only if the
    instance has an attribute `filename` set (which is optional)."""

    def check_for_filename_attribute(self, *args, **kwargs):
        """
        Returns False if GitHubTools instance has no filename attribute, or
        return the decorated function if it has.
        """
        if not hasattr(self, "filename") or not self.filename:
            msg = "To use {} method you need a filename, which was not set."
            self.oops(msg.format(function.__name__))
            return False
        return function(self, *args, **kwargs)

    return check_for_filename_attribute


class GitHubTools(GetGistCommons):
    """Helpers to deal with GitHub API and manipulate gists"""

    version = get_distribution("getgist").version
    api_root_url = "https://api.github.com/"
    headers = {
        "Accept": "application/vnd.github.v3+json",
        "User-Agent": "GetGist v{}".format(version),
    }
    requests = GetGistRequests(headers)
    is_authenticated = False

    def __init__(self, user, file_path, assume_yes=False):
        """
        Save basic variables to all methods, instantiate GetGistrequests and
        calls the OAuth method.
        :param user: (str) GitHub username
        :param file_path: (str or None) file_path to be saved (locally), created or updated (remotelly)
        :param assume_yes: (bool) assume yes (or first option) for all prompts
        :return: (None)
        """
        self.user = user
        self.file_path = file_path
        self.filename = os.path.basename(file_path) if file_path else None
        self.assume_yes = assume_yes
        self.add_oauth_header()

    def add_oauth_header(self):
        """
        Validate token and add the proper header for further requests.
        :return: (None)
        """
        # abort if no token
        oauth_token = self._get_token()
        if not oauth_token:
            return

        # add oauth header & reach the api
        self.headers["Authorization"] = "token " + oauth_token
        url = self._api_url("user")
        raw_resp = self.requests.get(url)
        resp = raw_resp.json()

        # abort & remove header if token is invalid
        if resp.get("login", "").lower() != self.user.lower():
            self.oops("Invalid token for user " + self.user)
            self.headers.pop("Authorization")
            return

        self.is_authenticated = True
        self.yeah("User {} authenticated".format(self.user))

    def get_gists(self, page=1):
        """
        List generator containing gist relevant information
        such as id, description, filenames and raw URL (dict).
        """
        # fetch all gists
        if self.is_authenticated:
            base_url = self._api_url("gists")
        else:
            base_url = self._api_url("users", self.user, "gists")

        url = "{}?page={}".format(base_url, page)
        self.output("Fetching " + url)
        raw_resp = self.requests.get(url)

        # abort if user not found
        if raw_resp.status_code != 200:
            self.oops("User `{}` not found".format(self.user))
            return

        # abort if there are no gists
        resp = raw_resp.json()
        if not resp:
            if page == 1:
                self.oops("No gists found for user `{}`".format(self.user))
            return

        # parse response
        yield from (self._parse_gist(gist) for gist in raw_resp.json())

        # check next page
        try:
            yield from (gist for gist in self.get_gists(page=page + 1))
        except StopIteration:
            pass

    @with_filename_only
    def select_gist(self, allow_none=False):
        """
        Given the requested filename, it selects the proper gist; if more than
        one gist is found with the given filename, user is asked to choose.
        :allow_none: (bool) for `getgist` it should raise error if no gist is
        found, but setting this argument to True avoid this error, which is
        useful when `putgist` is calling this method
        :return: (dict) selected gist
        """
        # pick up all matching gists
        matches = list()
        for gist in self.get_gists():
            for gist_file in gist.get("files"):
                if self.filename == gist_file.get("filename"):
                    matches.append(gist)

        # abort if no match is found
        if not matches:
            if allow_none:
                return None
            else:
                msg = "No file named `{}` found in {}'s gists"
                self.oops(msg.format(self.file_path, self.user))
                if not self.is_authenticated:
                    self.warn("To access private gists set the GETGIST_TOKEN")
                    self.warn("(see `getgist --help` for details)")
                return False

        # return if there's is only one match
        if len(matches) == 1 or self.assume_yes:
            return matches.pop(0)

        return self._ask_which_gist(matches)

    def list_gists(self):
        """ Prints all gists names, filenames and URLs"""
        gists = tuple(
            FileFromGist(
                gist.get("description"),
                gist_file.get("filename"),
                gist.get("url"),
                gist.get("public"),
            )
            for gist in self.get_gists()
            for gist_file in gist.get("files")
        )
        self.tabulate(*gists)

    @with_filename_only
    def read_gist_file(self, gist):
        """
        Returns the contents of file hosted inside a gist at GitHub.
        :param gist: (dict) gist parsed by GitHubTools._parse()
        :return: (bytes) content of a gist loaded from GitHub
        """
        url = False
        files = gist.get("files")
        for gist_file in files:
            if gist_file.get("filename") == self.filename:
                url = gist_file.get("raw_url")
                break
        if url:
            self.output("Reading {}".format(url))
            response = self.requests.get(url)
            return response.content

    @with_filename_only
    @oauth_only
    def update(self, gist, content):
        """
        Updates the contents of file hosted inside a gist at GitHub.
        :param gist: (dict) gist parsed by GitHubTools._parse_gist()
        :param content: (str or bytes) to be written
        :return: (bool) indicatind the success or failure of the update
        """
        # abort if content is False
        if content is False:
            return False

        # request
        url = self._api_url("gists", gist.get("id"))
        data = {"files": {self.filename: {"content": content}}}
        self.output("Sending contents of {} to {}".format(self.file_path, url))
        response = self.requests.patch(url, data=dumps(data))

        # error
        if response.status_code != 200:
            self.oops("Could not update " + gist.get("description"))
            self.oops("PATCH request returned " + str(response.status_code))
            return False

        # success
        self.yeah("Done!")
        self.hey("The URL to this Gist is: {}".format(gist["url"]))
        return True

    @with_filename_only
    @oauth_only
    def create(self, content, **kwargs):
        """
        Create a new gist.
        :param gist: (dict) gist parsed by GitHubTools._parse()
        :param content: (str or bytes) to be written
        :param public: (bool) defines if the gist is public or private
        :return: (bool) indicating the success or failure of the creation
        """
        # abort if content is False
        if content is False:
            return False

        # set new gist
        public = bool(kwargs.get("public", True))
        data = {
            "description": self.filename,
            "public": public,
            "files": {self.filename: {"content": content}},
        }

        # send request
        url = self._api_url("gists")
        self.output("Sending contents of {} to {}".format(self.file_path, url))
        response = self.requests.post(url, data=dumps(data))

        # error
        if response.status_code != 201:
            self.oops("Could not create " + self.filename)
            self.oops("POST request returned " + str(response.status_code))
            return False

        # parse created gist
        gist = self._parse_gist(response.json())

        # success
        self.yeah("Done!")
        self.hey("The URL to this Gist is: {}".format(gist["url"]))
        return True

    @with_filename_only
    def _ask_which_gist(self, matches):
        """
        Asks user which gist to use in case of more than one gist matching the
        instance filename.
        :param matches: (list) of dictionaries generated within select_gists()
        :return: (dict) of the selected gist
        """
        # ask user which gist to use
        self.hey("Use {} from which gist?".format(self.filename))
        for count, gist in enumerate(matches, 1):
            self.hey("[{}] {}".format(count, gist.get("description")))

        # get the gist index
        selected = False
        while not selected:
            gist_index = prompt("Type the number: ", type=int) - 1
            try:
                selected = matches[gist_index]
            except IndexError:
                self.oops("Invalid number, please try again.")

        self.output("Using `{}` Gist".format(selected["description"]))
        return selected

    def _api_url(self, *args):
        """Get entrypoints adding arguments separated by slashes"""
        return self.api_root_url + "/".join(args)

    @staticmethod
    def _parse_gist(gist):
        """Receive a gist (dict) and parse it to GetGist"""

        # parse files
        files = list()
        file_names = sorted(filename for filename in gist["files"].keys())
        for name in file_names:
            files.append(
                dict(filename=name, raw_url=gist["files"][name].get("raw_url"))
            )

        # parse description
        description = gist["description"]
        if not description:
            names = sorted(f.get("filename") for f in files)
            description = names.pop(0)

        return dict(
            description=description,
            id=gist.get("id"),
            files=files,
            url=gist.get("html_url"),
            public=gist.get("public"),
        )

    @staticmethod
    def _get_token():
        """Retrieve username from env var"""
        return os.getenv("GETGIST_TOKEN")
