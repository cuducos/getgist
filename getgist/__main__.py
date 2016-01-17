from click import argument, command, option
from decouple import config

from getgist.github import GitHubTools
from getgist.local import LocalTools


GETGIST_DESC = """
    GetGist downloads any file from a GitHub Gist, with one single command.
    Usage: `getgist <GitHub username> <file name from any file inside a gist>`.

    If you set GETGIST_USER envvar with your GitHub username, you can use the
    shortcut `geymy <file name>` (see `getmy --help` for details).

    If you set GETGIST_TOKEN envvar with your personal access token (see
    https://github.com/settings/tokens for details) you can get get priavte
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


class GetGist(object):

    def __init__(self, **kwargs):

        # get arguments
        user = kwargs.get('user')
        allow_none = kwargs.get('allow_none', False)
        assume_yes = kwargs.get('assume_yes', False)
        self.filename = kwargs.get('filename')
        self.public = not kwargs.get('create_private', False)

        # instantiate local tools & check for user
        self.local = LocalTools(self.filename, assume_yes)
        if not user:
            message = """
                No default user set yet. To avoid this prompt set an
                environmental variable called  `GETGIST_USER`.'
            """
            self.local.oops(message)

        # instantiate filename, guthub tools and fetch gist
        self.github = GitHubTools(user, assume_yes)
        self.gist = self.github.select_gist(self.filename, allow_none)

    def get(self):
        if self.gist:
            content = self.github.read_gist_file(self.gist, self.filename)
            self.local.save(content)

    def put(self):
        content = self.local.read(self.filename)
        if self.gist:
            self.github.update(self.gist, self.filename, content)
        else:
            self.github.create(self.filename, content, public=self.public)


@command(help=GETGIST_DESC)
@option('--yes-to-all', '-y', is_flag=True, help='Assume yes to all prompts.')
@argument('user')
@argument('filename')
def run_getgist(filename, user, **kwargs):
    assume_yes = kwargs.get('yes_to_all')
    getgist = GetGist(user=user, filename=filename, assume_yes=assume_yes)
    getgist.get()


@command(help=GETMY_DESC)
@option('--yes-to-all', '-y', is_flag=True, help='Assume yes to all prompts.')
@argument('filename')
def run_getmy(filename, **kwargs):
    assume_yes = kwargs.get('yes_to_all')
    user = config('GETGIST_USER', default=None)
    getgist = GetGist(user=user, filename=filename, assume_yes=assume_yes)
    getgist.get()


@command(help=PUTGIST_DESC)
@option('--yes-to-all', '-y', is_flag=True, help='Assume yes to all prompts.')
@option('--private', '-p', is_flag=True, help='Crete new gist as private')
@argument('user')
@argument('filename')
def run_putgist(filename, user, **kwargs):
    assume_yes = kwargs.get('yes_to_all')
    private = kwargs.get('private')
    getgist = GetGist(user=user, filename=filename, assume_yes=assume_yes,
                      create_private=private, allow_none=True)
    getgist.put()


@command(help=PUTMY_DESC)
@option('--yes-to-all', '-y', is_flag=True, help='Assume yes to all prompts.')
@option('--private', '-p', is_flag=True, help='Crete new gist as private')
@argument('filename')
def run_putmy(filename, **kwargs):
    assume_yes = kwargs.get('yes_to_all')
    private = kwargs.get('private')
    user = config('GETGIST_USER', default=None)
    getgist = GetGist(user=user, filename=filename, assume_yes=assume_yes,
                      create_private=private, allow_none=True)
    getgist.put()
