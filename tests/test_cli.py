import pytest
from click.testing import CliRunner
from getgist.__main__ import (
    run_getgist,
    run_getmy,
    run_putgist,
    run_putmy,
    run_lsgists,
    run_mygists,
)

runner = CliRunner()


@pytest.mark.parametrize(
    "command, to_patch, args",
    [
        (run_getmy, None, []),
        (run_putmy, "getgist.__main__.GetGist.put", []),
        (run_putgist, None, ["cuducos"]),
        (run_getgist, None, ["cuducos"]),
    ],
)
def test_run_command_with_error_in_filename(
    command, to_patch, args, mocker, monkeypatch
):
    monkeypatch.setenv("GETGIST_USER", "cuducos")

    if to_patch:
        mocker.patch(to_patch)

    result = runner.invoke(command, args)
    assert result.exit_code == 2
    assert "Error: Missing argument 'FILENAME'." in result.output


@pytest.mark.parametrize(
    "command, to_patch, args",
    [
        (run_putgist, "getgist.__main__.GetGist.put", []),
        (run_getgist, None, []),
        (run_lsgists, "getgist.__main__.GetGist.put", []),
    ],
)
def test_run_command_with_error_in_username(
    command, to_patch, args, mocker, monkeypatch
):
    monkeypatch.setenv("GETGIST_USER", "cuducos")

    if to_patch:
        mocker.patch(to_patch)

    result = runner.invoke(command, args)
    assert result.exit_code == 2
    assert "Error: Missing argument 'USER'." in result.output


@pytest.mark.parametrize(
    "command, to_patch, args",
    [
        (run_getgist, "getgist.__main__.GetGist.get", ["cuducos", ".gitignore_global"]),
        (run_getmy, "getgist.__main__.GetGist.get", [".gitignore_global"]),
        (run_putmy, "getgist.__main__.GetGist.put", ["~/.vimrc"]),
        (run_mygists, "getgist.__main__.GetGist.put", []),
        (run_lsgists, "getgist.__main__.GetGist.put", ["cuducos"]),
        (run_putgist, "getgist.__main__.GetGist.put", ["cuducos", "~/.vimrc"]),
        (run_mygists, "getgist.__main__.GetGist.get", []),
    ],
)
def test_run_command_with_success(command, to_patch, args, mocker, monkeypatch):
    monkeypatch.setenv("GETGIST_USER", "cuducos")

    if to_patch:
        mocker.patch(to_patch)

    result = runner.invoke(command, args)
    assert result.exit_code == 0
