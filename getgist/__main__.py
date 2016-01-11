from click import argument, command, option
from decouple import config

from getgist.github import GitHubTools
from getgist.local import LocalTools


GETGIST_DESC = """
    GetGist downloads any file from a GitHub Gist, with one single command.
    Usage: `getgist <GitHub username> <file name from any file inside a gist>`.

    If you set GETGIST_USER envvar with your GitHub username, you can use the
    shortcut `geymy` (see `getmy --help` for details).

    If you set GETGIST_TOKEN envvar with your personal access token (see
    https://github.com/settings/tokens for details) you can get get priavte
    gists from your account and you can upload local changes to your gist repo
    (see `putmy --help` for details).
"""


GETMY_DESC = """
    Use `getgist` assuming the user is set in an envvar called GETGIST_USER.
    See `getgist --help` for more details.
"""


def get_gist(user, filename, assume_yes=False):

    # instantiate local tools & check for user
    local = LocalTools(filename, assume_yes)
    if not user:
        local.error('No default user set yet. To avoid this prompt set an')
        local.error('environmental variable called `GETGIST_USER`.')

    # instantiate guthub tools and fetch gist
    github = GitHubTools(user, assume_yes)
    gist = github.select_gist(filename)

    # save file
    if gist:
        content = github.read_gist_file(gist, filename)
        local.save(content)


@command(help=GETGIST_DESC)
@option('--yes-to-all', '-y', is_flag=True, help='Assume yes to all prompts.')
@argument('user')
@argument('filename')
def run_getgist(filename, user, **kwargs):
    assume_yes = kwargs.get('yes_to_all')
    get_gist(user, filename, assume_yes)


@command(help=GETMY_DESC)
@option('--yes-to-all', '-y', is_flag=True, help='Assume yes to all prompts.')
@argument('filename')
def run_getmy(filename, **kwargs):
    assume_yes = kwargs.get('yes_to_all')
    user = config('GETGIST_USER', default=None)
    get_gist(user, filename, assume_yes)
