from re import search

from getgist.github import GitHubTools
from tests.conftest import MockResponse, GETGIST_TOKEN, GETGIST_USER


def test_no_token_results_in_no_authentication(mocker):
    token = mocker.patch("getgist.github.GitHubTools._get_token")
    token.return_value = False

    github = GitHubTools(GETGIST_USER, ".gist")
    assert "Authorization" not in github.headers
    assert not github.is_authenticated


def test_invalid_token(mocker, response):
    get = mocker.patch("getgist.request.GetGistRequests.get")
    token = mocker.patch("getgist.github.GitHubTools._get_token")
    get.return_value = response("user", case=False)
    token.return_value = GETGIST_TOKEN

    github = GitHubTools(GETGIST_USER, ".gist")
    assert "Authorization" not in github.headers
    assert not github.is_authenticated


def test_valid_token(mocker, response):
    get = mocker.patch("getgist.request.GetGistRequests.get")
    token = mocker.patch("getgist.github.GitHubTools._get_token")
    get.return_value = response("user")
    token.return_value = GETGIST_TOKEN

    github = GitHubTools(GETGIST_USER, ".gist")
    assert "Authorization" in github.headers
    assert github.is_authenticated


def test_main_headers(authenticated_github):
    assert "Accept" in authenticated_github.headers
    assert "User-Agent" in authenticated_github.headers

    user_agent = authenticated_github.headers.get("User-Agent")
    user_agent_re = r"^(GetGist v)([\d]+).([\d]+)(.[\d]+)?$"
    assert search(user_agent_re, user_agent)


def test_api_url(authenticated_github):
    url = authenticated_github._api_url(GETGIST_USER, "gists")
    expected = "https://api.github.com/{}/gists".format(GETGIST_USER)
    assert url == expected


def test_parse_gist(authenticated_github, response, gists):
    gist_raw = response("gist/id_gist_1")
    assert authenticated_github._parse_gist(gist_raw.json()) == gists[0]


def test_get_gists(mocker, response, gists, authenticated_github):
    get = mocker.patch("getgist.request.GetGistRequests.get")
    get.return_value = response("users/janedoe/gists")
    fetched_gists = tuple(authenticated_github.get_gists())
    assert gists[0] in fetched_gists
    assert gists[1] in fetched_gists
    assert gists[3] not in fetched_gists


def test_no_gists_with_wrong_username(mocker, response, authenticated_github):
    get = mocker.patch("getgist.request.GetGistRequests.get")
    get.return_value = response("users/janedoe/gists", case=False, status_code=404)
    assert not tuple(authenticated_github.get_gists())


def test_user_with_no_gists(mocker, response, authenticated_github):
    get = mocker.patch("getgist.request.GetGistRequests.get")
    get.return_value = response("users/casper/gists")
    assert not tuple(authenticated_github.get_gists())


def test_authenticated_get_gists(mocker, response, gists):
    get = mocker.patch("getgist.request.GetGistRequests.get")
    token = mocker.patch("getgist.github.GitHubTools._get_token")
    token.return_value = GETGIST_TOKEN
    get.side_effect = (response("user"), response("gists"))

    github = GitHubTools(GETGIST_USER, ".gist")
    gists = tuple(github.get_gists())
    assert gists[2] in gists
    assert gists[3] in gists


def test_select_gist_one_input(mocker, response, gists, authenticated_github):
    get = mocker.patch("getgist.request.GetGistRequests.get")
    ask = mocker.patch("getgist.GetGistCommons.ask")
    ask.return_value = 2
    get.return_value = response("users/janedoe/gists")

    authenticated_github.filename = ".gist"
    gists = tuple(authenticated_github.get_gists())
    assert authenticated_github._ask_which_gist(gists) == gists[1]


def test_select_gist_multi_input(mocker, response, gists, authenticated_github):
    get = mocker.patch("getgist.request.GetGistRequests.get")
    input_method = mocker.patch("getgist.input_method")
    get.return_value = response("users/janedoe/gists")
    input_method.side_effect = ("alpha", "", 2)

    authenticated_github.filename = ".gist"
    gists = tuple(authenticated_github.get_gists())
    assert authenticated_github._ask_which_gist(gists) == gists[1]


def test_select_gist_single_match(mocker, response, gists, authenticated_github):
    get = mocker.patch("getgist.request.GetGistRequests.get")
    get.return_value = response("users/janedoe/gists")
    authenticated_github.filename = ".gist.sample"
    assert authenticated_github.select_gist() == gists[2]


def test_select_gist_no_match_default(mocker, response, gists, authenticated_github):
    get = mocker.patch("getgist.request.GetGistRequests.get")
    get.return_value = response("users/janedoe/gists")
    authenticated_github.filename = ".no_gist"
    assert not authenticated_github.select_gist()


def test_select_gist_no_match_allow_none(mocker, response, gists, authenticated_github):
    get = mocker.patch("getgist.request.GetGistRequests.get")
    get.return_value = response("users/janedoe/gists")
    authenticated_github.filename = ".no_gist"
    assert not authenticated_github.select_gist(allow_none=True)


def test_select_gist_multi_matches(mocker, response, gists, authenticated_github):
    get = mocker.patch("getgist.request.GetGistRequests.get")
    ask = mocker.patch("getgist.GetGistCommons.ask")
    get.return_value = response("users/janedoe/gists")
    ask.return_value = 2
    authenticated_github.filename = ".gist"
    assert authenticated_github.select_gist() == gists[1]


def test_read_gist(mocker, response, gists, authenticated_github):
    get = mocker.patch("getgist.request.GetGistRequests.get")
    get.return_value = MockResponse("Hello, world!", 200)
    gist_raw = response("gist/id_gist_1")
    gist = authenticated_github._parse_gist(gist_raw.json())
    assert authenticated_github.read_gist_file(gist) == "Hello, world!"


def test_update_gist_without_authorization(mocker, parse):
    token = mocker.patch("getgist.github.GitHubTools._get_token")
    token.return_value = None
    gist = parse(id=1, user=GETGIST_USER, filename=".gist", url="")
    github = GitHubTools(GETGIST_USER, ".gist.sample")
    assert not github.update(gist, "42")


def test_update_gist(mocker, response, parse):
    get = mocker.patch("getgist.request.GetGistRequests.get")
    patch = mocker.patch("getgist.request.GetGistRequests.patch")
    token = mocker.patch("getgist.github.GitHubTools._get_token")
    get.return_value = response("user")
    patch.return_value = response("gist/id_gist_1")
    token.return_value = GETGIST_TOKEN
    gist = parse(id=1, user=GETGIST_USER, filename=".gist", url="")
    github = GitHubTools(GETGIST_USER, ".gist")
    assert github.update(gist, "42")


def test_failed_update_gist(mocker, response, parse):
    get = mocker.patch("getgist.request.GetGistRequests.get")
    token = mocker.patch("getgist.github.GitHubTools._get_token")
    patch = mocker.patch("getgist.request.GetGistRequests.patch")
    get.return_value = response("user")
    token.return_value = GETGIST_TOKEN
    patch.return_value = response("gist/id_gist_1", case=False, status_code=404)
    gist = parse(id=1, user=GETGIST_USER, filename=".gist", url="")
    github = GitHubTools(GETGIST_USER, ".gist")
    assert not github.update(gist, "42")


def test_update_gist_with_no_file(mocker, response, parse):
    get = mocker.patch("getgist.request.GetGistRequests.get")
    token = mocker.patch("getgist.github.GitHubTools._get_token")
    get.return_value = response("user")
    token.return_value = GETGIST_TOKEN
    gist = parse(id=1, user=GETGIST_USER, filename=".gist", url="")
    github = GitHubTools(GETGIST_USER, ".gist")
    assert not github.update(gist, False)


def test_create_gist_without_authorization(mocker):
    token = mocker.patch("getgist.github.GitHubTools._get_token")
    token.return_value = None
    github = GitHubTools(GETGIST_USER, ".gist.sample")
    assert not github.create("42")


def test_create_gist(mocker, response):
    get = mocker.patch("getgist.request.GetGistRequests.get")
    post = mocker.patch("getgist.request.GetGistRequests.post")
    token = mocker.patch("getgist.github.GitHubTools._get_token")
    get.return_value = response("user")
    post.return_value = response("gist/id_gist_1", status_code=201)
    token.return_value = GETGIST_TOKEN
    github = GitHubTools(GETGIST_USER, ".gist.sample")
    assert github.create("42", public=False)


def test_failed_create_gist(mocker, response):
    get = mocker.patch("getgist.request.GetGistRequests.get")
    post = mocker.patch("getgist.request.GetGistRequests.post")
    token = mocker.patch("getgist.github.GitHubTools._get_token")
    get.return_value = response("user")
    post.return_value = response("gist/id_gist_1", case=False, status_code=404)
    token.return_value = GETGIST_TOKEN
    github = GitHubTools(GETGIST_USER, ".gist.sample")
    assert not github.create("42", public=False)


def test_create_gist_with_no_file(mocker, response):
    get = mocker.patch("getgist.request.GetGistRequests.get")
    token = mocker.patch("getgist.github.GitHubTools._get_token")
    get.return_value = response("user")
    token.return_value = GETGIST_TOKEN
    github = GitHubTools(GETGIST_USER, ".gist")
    assert not github.create(False)
