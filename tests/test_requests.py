from getgist.request import GetGistRequests


def test_no_header():
    requests = GetGistRequests()
    assert isinstance(requests.headers, dict)


def test_update_header():
    requests = GetGistRequests({"foo": "bar"})
    assert requests.headers["foo"] == "bar"


def test_add_header():
    requests = GetGistRequests({"foo": "bar"})
    new_headers = requests.add_headers({"headers": {"bar": "foo"}})
    assert new_headers == {"headers": {"foo": "bar", "bar": "foo"}}
    # TODO new API for add_headers to avoid the repetitive usage of `header`
