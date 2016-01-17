import requests


class GetGistRequests(object):
    """Encapsulate requests lib to always send self.headers as headers"""

    def __init__(self, headers=None):
        """
        Get a header object to use it in all requests
        :param headers: (dict)
        :return: (None)
        """
        if not headers:
            headers = dict()
        self.headers = headers

    def add_headers(self, kwargs):
        """
        Add any extra header to the existng header object.
        :param kwargs: (dict)
        :return: (dict) containing an item with `headers` as key
        """
        kwargs['headers'] = kwargs.get('headers', {})
        kwargs['headers'].update(self.headers)
        return kwargs

    def get(self, url, params=None, **kwargs):
        """Encapsulte requests.get to use this class instance header"""
        return requests.get(url, params=params, **self.add_headers(kwargs))

    def patch(self, url, data=None, **kwargs):
        """Encapsulte requests.patch to use this class instance header"""
        return requests.patch(url, data=data, **self.add_headers(kwargs))

    def post(self, url, data=None, **kwargs):
        """Encapsulte requests.post to use this class instance header"""
        return requests.post(url, data=data, **self.add_headers(kwargs))
