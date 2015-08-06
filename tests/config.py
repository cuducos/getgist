import json

config = {'user': 'cuducos',
          'file': '.vimrc',
          'json': open('tests/gists.sample.json').read()}


class MockAPI(object):

    description = 'Gist #{}'
    url = 'URL #{}'

    def __init__(self, name='xpto', number=1):
        self.name = name
        self.number = number

    def get_json(self):
        return json.dumps([self.factory(i + 1) for i in range(self.number)])

    def get_results(self):
        for i in range(self.number):
            yield {'id': str(i + 1),
                   'description': self.description.format(i + 1),
                   'raw_url': self.url.format(i + 1)}

    def factory(self, id):
        return {'id': str(id),
                'description': self.description.format(id),
                'files': {self.name: {'filename': self.name,
                                      'raw_url': self.url.format(id)}}}
