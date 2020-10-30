from os import getenv
from sys import exit

from click import argument, command, option

from getgist import GetGistCommons
from getgist.github import GitHubTools
from getgist.local import LocalTools


GETGIST_DESC = """
    GetGist downloads any file from a GitHub Gist, with one single command.
    Usage: `getgist <GitHub username> <file name from any file inside a gist>`.

    If you set GETGIST_USER envvar with your GitHub username, you can use the
    shortcut `geymy <file name>` (see `getmy --help` for details).

    If you set GETGIST_TOKEN envvar with your personal access token (see
    https://github.com/settings/tokens for details) you can get get private
    gists from your account and you can upload local changes to your gist repo
    (see `putmy --help` for details).
"""


GETMY_DESC = """
    Call `getgist` assuming the user is set in an envvar called GETGIST_USER.
    See `getgist --help` for more details.
"""

PUTGIST_DESC = """
    PutGist uploads any file to a GitHub Gist, with one single command.
    Usage: `putgist <GitHub username> <file name>`.

    You have to set the GETGIST_TOKEN envvar with your personal access token
    (see https://github.com/settings/tokens for details).

    If you set GETGIST_USER envvar with your GitHub username, you can use the
    shortcut `putmy <file name>` (see `getmy --help` for details).
"""


PUTMY_DESC = """
    Call `putgist` assuming the user is set in an envvar called GETGIST_USER.
    See `putgist --help` for more details.
"""


LSGISTS_DESC = """
    Lists all files from a GitHub user's Gists, with one single command.
    Usage:  `lsgists <GitHub username>`.
"""

MYGISTS_DESC = """
    Call `lsgists` files assuming the user is set in an envvar called GETGIST_USER.
    See:  `lsgists --help` for more more details.
"""


class GetGist(object):
    """
    Main GetGist objects linking inputs from the CLI to the helpers from
    GitHubTools (to deal with the API) and LocalTools (to deal with the local
    file system.
    """

    def __init__(self, **kwargs):
        """
        Instantiate GitHubTools & LocalTools (if needed), and set the variables required
        to get, create or update gists (filename and public/private flag)
        :param user: (str) GitHub username
        :param filename: (str) name of file from any Gist or local file system
        :param allow_none: (bool) flag to use GitHubTools.select_gist
        differently with `getgist` and `putgist` commands (if no gist/filename
        is found it raises an error for `getgist`, or sets `putgist` to create
        a new gist).
        :param create_private: (bool) create a new gist as private
        :param assume_yes: (bool) assume yes (or first option) for all prompts
        :return: (None)
        """
        user = kwargs.get("user")
        allow_none = kwargs.get("allow_none", False)
        assume_yes = kwargs.get("assume_yes", False)
        filename = kwargs.get("filename")
        self.public = not kwargs.get("create_private", False)

        if not user:
            message = """
            No default user set yet. To avoid this prompt set an
            environmental variable called  `GETGIST_USER`.'
            """
            GetGistCommons().oops(message)
            exit(1)

        self.github = GitHubTools(user, filename, assume_yes)
        self.local = LocalTools(filename, assume_yes) if filename else None
        self.gist = self.github.select_gist(allow_none) if filename else None

    def get(self):
        """Reads the remote file from Gist and save it locally"""
        if self.gist:
            content = self.github.read_gist_file(self.gist)
            self.local.save(content)

    def put(self):
        """ Reads local file & update the remote gist (or create a new one)"""
        content = self.local.read()
        if self.gist:
            self.github.update(self.gist, content)
        else:
            self.github.create(content, public=self.public)

    def ls(self):
        """ Lists all gists from a github user """
        self.github.list_gists()


@command(help=GETGIST_DESC)
@option("--yes-to-all", "-y", is_flag=True, help="Assume yes to all prompts.")
@argument("user")
@argument("filename")
def run_getgist(filename, user, **kwargs):
    """Passes user inputs to GetGist() and calls get()"""
    assume_yes = kwargs.get("yes_to_all")
    getgist = GetGist(user=user, filename=filename, assume_yes=assume_yes)
    getgist.get()


@command(help=GETMY_DESC)
@option("--yes-to-all", "-y", is_flag=True, help="Assume yes to all prompts.")
@argument("filename")
def run_getmy(filename, **kwargs):
    """Shortcut for run_getgist() reading username from env var"""
    assume_yes = kwargs.get("yes_to_all")
    user = getenv("GETGIST_USER")
    getgist = GetGist(user=user, filename=filename, assume_yes=assume_yes)
    getgist.get()


@command(help=PUTGIST_DESC)
@option("--yes-to-all", "-y", is_flag=True, help="Assume yes to all prompts.")
@option("--private", "-p", is_flag=True, help="Create new gist as private")
@argument("user")
@argument("filename")
def run_putgist(filename, user, **kwargs):
    """Passes user inputs to GetGist() and calls put()"""
    assume_yes = kwargs.get("yes_to_all")
    private = kwargs.get("private")
    getgist = GetGist(
        user=user,
        filename=filename,
        assume_yes=assume_yes,
        create_private=private,
        allow_none=True,
    )
    getgist.put()


@command(help=PUTMY_DESC)
@option("--yes-to-all", "-y", is_flag=True, help="Assume yes to all prompts.")
@option("--private", "-p", is_flag=True, help="Create new gist as private")
@argument("filename")
def run_putmy(filename, **kwargs):
    """Shortcut for run_putgist() reading username from env var"""
    assume_yes = kwargs.get("yes_to_all")
    private = kwargs.get("private")
    user = getenv("GETGIST_USER")
    getgist = GetGist(
        user=user,
        filename=filename,
        assume_yes=assume_yes,
        create_private=private,
        allow_none=True,
    )
    getgist.put()


@command(help=LSGISTS_DESC)
@argument("user")
def run_lsgists(user):
    getgist = GetGist(user=user)
    getgist.ls()


@command(help=MYGISTS_DESC)
def run_mygists():
    user = getenv("GETGIST_USER")
    getgist = GetGist(user=user)
    getgist.ls()
