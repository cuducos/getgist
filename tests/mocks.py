import json
import os


class MockResponse(object):

    def __init__(self, content, status_code):
        self.content = content
        self.code = status_code

    def __repr__(self):
        return self.content

    def json(self):
        return json.loads(self.content)

    @property
    def status_code(self):
        return self.code


def request_mock(uri, **kwargs):
    """
    Returns an object similar to requests response, containins the contents of
    a json file. The file to be read is placed at tests/fixtures. The file name
    is composed by the equivalent of the request URI replacing slashes by
    underscores (eg: users/janedoe/gists is converted to users_janedoe_gists),
    and to it it's appended the case (success if True, or fail if False) and
    the .json extention.
    :param request: (str) Example: users/janedoe/gists
    :param kwargs: case (bool) True/success or False/fail; status_code (int)
    :return: contents of the JSON file (eg: contents of
    tests/fixtures/users_janedoe_gists.success.json)
    """
    case = kwargs.get('case', True)
    status_code = kwargs.get('status_code', 200)

    path = os.path.dirname(__file__)
    parts = dict(name=uri.replace('/', '_'),
                 path=os.path.join(path, 'fixtures'),
                 case='success' if case else 'fail')
    with open('{path}/{name}.{case}.json'.format(**parts)) as handler:
        return MockResponse(handler.read(), status_code)


def parse_mock(**kwargs):
    """
    Accepts as kwargs the following arguments to build a dictionary with
    expected gist (dict) values: id (int), filename (str or list),
    description (str) and user (str)
    """

    # filter the arguments
    id_num = kwargs.get('id', 1)
    id = 'id_gist_' + str(id_num)
    hash = 'hash_gist_' + str(id_num)
    filename = kwargs.get('filename', '.gist')
    if not isinstance(filename, list):
        filename = [filename]
    filename = sorted(filename)
    user = kwargs.get('user', 'janedoe')
    description = kwargs.get('description')
    if not description:
        description = filename[0]

    # build the file list
    files = list()
    struct = '{base}{user}/{id}/raw/{hash}/{filename}'
    base = 'https://gist.githubusercontent.com/'
    for f in filename:
        url = struct.format(base=base, user=user, id=id, hash=hash, filename=f)
        files.append(dict(filename=f, raw_url=url))

    return dict(description=description, id=id, files=files)
