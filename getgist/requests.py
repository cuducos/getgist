import requests


class GetGistRequests(object):
    """Encapsulate requests lib to always send self.headers as headers"""

    def __init__(self, headers=None):
        if not headers:
            headers = dict()
        self.headers = headers

    def add_headers(self, kwargs):
        kwargs['headers'] = kwargs.get('headers', {})
        kwargs['headers'].update(self.headers)
        return kwargs

    def get(self, url, params=None, **kwargs):
        return requests.get(url, params=params, **self.add_headers(kwargs))

    def patch(self, url, data=None, **kwargs):
        return requests.patch(url, data=data, **self.add_headers(kwargs))
