from getgist.request import GetGistRequests


def test_no_header():
    requests = GetGistRequests()
    assert isinstance(requests.headers, dict)


def test_update_header():
    requests = GetGistRequests({"foo": "bar"})
    assert requests.headers["foo"] == "bar"


def test_add_header():
    requests = GetGistRequests({"foo": "bar"})
    new_headers = requests.add_headers(bar="foo")
    assert new_headers == {"foo": "bar", "bar": "foo"}


def test_get_without_params(mocker):
    get = mocker.patch("getgist.request.requests.get")
    requests = GetGistRequests({"foo": "bar"})
    requests.get("foobar", bar="foo")
    get.assert_called_once_with(
        "foobar", params=None, headers={"foo": "bar", "bar": "foo"}
    )


def test_get_with_params(mocker):
    get = mocker.patch("getgist.request.requests.get")
    requests = GetGistRequests({"foo": "bar"})
    requests.get("foobar", params=42, bar="foo")
    get.assert_called_once_with(
        "foobar", params=42, headers={"foo": "bar", "bar": "foo"}
    )


def test_post_without_data(mocker):
    post = mocker.patch("getgist.request.requests.post")
    requests = GetGistRequests({"foo": "bar"})
    requests.post("foobar", bar="foo")
    post.assert_called_once_with(
        "foobar", data=None, headers={"foo": "bar", "bar": "foo"}
    )


def test_post_with_data(mocker):
    post = mocker.patch("getgist.request.requests.post")
    requests = GetGistRequests({"foo": "bar"})
    requests.post("foobar", data=42, bar="foo")
    post.assert_called_once_with(
        "foobar", data=42, headers={"foo": "bar", "bar": "foo"}
    )


def test_patch_without_data(mocker):
    patch = mocker.patch("getgist.request.requests.patch")
    requests = GetGistRequests({"foo": "bar"})
    requests.patch("foobar", bar="foo")
    patch.assert_called_once_with(
        "foobar", data=None, headers={"foo": "bar", "bar": "foo"}
    )


def test_patch_with_data(mocker):
    patch = mocker.patch("getgist.request.requests.patch")
    requests = GetGistRequests({"foo": "bar"})
    requests.patch("foobar", data=42, bar="foo")
    patch.assert_called_once_with(
        "foobar", data=42, headers={"foo": "bar", "bar": "foo"}
    )
