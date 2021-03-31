import json
import os
from glob import glob
from tempfile import NamedTemporaryFile
from uuid import uuid4

import pytest

from getgist.github import GitHubTools
from getgist.local import LocalTools


GETGIST_USER = "janedoe"
GETGIST_TOKEN = "Jane's token"
TEST_FILE = ".test-{}".format(uuid4())
TEST_FILE_CONTENTS = "42"


class MockResponse(object):
    def __init__(self, content, status_code):
        self.content = content
        self.status_code = status_code

    def __repr__(self):
        return self.content

    def json(self):
        return json.loads(self.content)


def response_mock(uri, **kwargs):
    """Returns an object similar to the requests's response, containing the
    contents of a JSON file. The file to be read is placed at tests/fixtures.
    The file name is composed by the equivalent of the request URI replacing
    slashes by underscores (eg: users/janedoe/gists is converted to
    users_janedoe_gists), and to it it's appended the case (success if True, or
    fail if False) and the .json extension.

    :param uri: (str) Example: users/janedoe/gists/page0
    :param kwargs: case (bool) True/success or False/fail; status_code (int)
    :return: contents of the JSON file (eg: contents of
    tests/fixtures/users_janedoe_gists.success.json)
    """
    case = kwargs.get("case", True)
    status_code = kwargs.get("status_code", 200)

    path = os.path.dirname(__file__)
    parts = dict(
        name=uri.replace("/", "_"),
        path=os.path.join(path, "fixtures"),
        case="success" if case else "fail",
    )
    with open("{path}/{name}.{case}.json".format(**parts)) as fobj:
        return MockResponse(fobj.read(), status_code)


def parse_mock(**kwargs):
    """Accepts as kwargs the following arguments to build a dictionary with an
    expected gist (dict) values: id (int), filename (str or list), description
    (str), user (str) and public (bool).
    """

    # filter the arguments
    id_num = kwargs.get("id", 1)
    id_ = "id_gist_{}".format(id_num)
    hash_ = "hash_gist_{}".format(id_num)
    gist_url = kwargs.get("url")
    user = kwargs.get("user", "janedoe")
    public = kwargs.get("public", True)

    filename = kwargs.get("filename", ".gist")
    if not isinstance(filename, list):
        filename = [filename]
    filename = sorted(filename)

    description = kwargs.get("description")
    if not description:
        description = filename[0]

    # build the file list
    files = list()
    struct = "{base}{user}/{id}/raw/{hash}/{filename}"
    base = "https://gist.githubusercontent.com/"
    for name in filename:
        url = struct.format(base=base, user=user, id=id_, hash=hash_, filename=name)
        files.append(dict(filename=name, raw_url=url))

    return dict(
        description=description, id=id_, files=files, url=gist_url, public=public
    )


@pytest.fixture
def local():
    with open(TEST_FILE, "w") as fobj:
        fobj.write(TEST_FILE_CONTENTS)

    yield LocalTools(TEST_FILE)

    for path in glob("{}*".format(TEST_FILE)):
        os.remove(path)


@pytest.fixture
def temporary_file():
    with NamedTemporaryFile(mode="w") as fobj:
        fobj.write(TEST_FILE_CONTENTS)
        fobj.seek(0)
        yield LocalTools(fobj.name)


@pytest.fixture
def parse():
    return parse_mock


@pytest.fixture
def response():
    return response_mock


@pytest.fixture
def authenticated_github(mocker):
    oauth = mocker.patch("getgist.github.GitHubTools.add_oauth_header")
    oauth.return_value = None
    return GitHubTools("janedoe", ".gist")


@pytest.fixture
def gists():
    gist1 = parse_mock(
        id=1,
        user=GETGIST_USER,
        filename=".gist",
        url="https://gist.github.com/id_gist_1",
        public=True,
    )
    gist2 = parse_mock(
        id=2,
        user=GETGIST_USER,
        filename=".gist",
        description="Description of Gist 2",
        url="https://gist.github.com/id_gist_2",
        public=True,
    )
    gist3 = parse_mock(
        id=3,
        user=GETGIST_USER,
        filename=[".gist.sample", ".gist.dev"],
        url="https://gist.github.com/id_gist_3",
        public=True,
    )
    gist4 = parse_mock(
        id=4,
        user=GETGIST_USER,
        filename=".gist.prod",
        url="https://gist.github.com/id_gist_4",
        public=False,
    )

    return gist1, gist2, gist3, gist4
