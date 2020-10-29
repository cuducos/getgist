from getgist import GetGistCommons
from getgist.github import FileFromGist


def test_tabulate(mocker):
    secho = mocker.patch("getgist.secho")
    tabulate = mocker.patch("getgist.tabulate")
    commons = GetGistCommons()
    commons.tabulate(
        FileFromGist("file1.txt", "My First Gist", "http://…"),
        FileFromGist("file2.txt", "My 2nd Gist", "https://…"),
    )
    tabulate.assert_called_once_with(
        (
            ("file1.txt", "My First Gist", "http://…"),
            ("file2.txt", "My 2nd Gist", "https://…"),
        ),
        headers=("Gist", "File", "URL"),
    )
    secho.assert_called_once()
