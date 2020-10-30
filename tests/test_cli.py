import click
from click.testing import CliRunner
from getgist.__main__ import (
    GETGIST_DESC,
    GETMY_DESC,
    LSGISTS_DESC,
    MYGISTS_DESC,
    PUTGIST_DESC,
    PUTMY_DESC,
    run_getgist,
    run_getmy,
    run_lsgists,
    run_mygists,
    run_putgist,
    run_putmy,
)

import pytest

runner = CliRunner()

def test_run_getgist_cli_without_username():
    result = runner.invoke(run_getgist)
    assert "Error: Missing argument 'USER'." in result.output

def test_run_getgist_cli_without_filename():
    result = runner.invoke(run_getgist, ['cuducos'])
    assert "Error: Missing argument 'FILENAME'." in result.output

def test_run_getgist_cli_with_username_and_filename(mocker):
    mocker.patch('getgist.__main__.GetGist.get')
    result = runner.invoke(run_getgist, ['cuducos', '.gitignore_global'])
    assert result.exit_code == 0

def test_run_getmy_cli_without_filename():
    result = runner.invoke(run_getmy)
    assert "Error: Missing argument 'FILENAME'." in result.output
    assert result.exit_code == 2

def test_run_getmy_cli_with_filename(mocker, monkeypatch):
    monkeypatch.setenv("GETGIST_USER", "cuducos")
    mocker.patch('getgist.__main__.GetGist.get')
    result = runner.invoke(run_getmy, ["bootstrap.sh"])
    assert result.exit_code == 0

def test_run_putmy_cli_without_filename(mocker, monkeypatch):
    monkeypatch.setenv("GETGIST_USER", "cuducos")
    mocker.patch('getgist.__main__.GetGist.put')
    result = runner.invoke(run_putmy)
    assert result.exit_code == 2
    assert "Error: Missing argument 'FILENAME'." in result.output

def test_run_putmy_cli_with_filename(mocker, monkeypatch):
    monkeypatch.setenv("GETGIST_USER", "cuducos")
    mocker.patch('getgist.__main__.GetGist.put')
    result = runner.invoke(run_putmy, ["~/.vimrc"])
    assert result.exit_code == 0

def test_run_putgist_cli_without_username_and_filename(mocker):
    mocker.patch('getgist.__main__.GetGist.put')
    result = runner.invoke(run_putgist)
    assert result.exit_code == 2
    assert "Error: Missing argument 'USER'." in result.output

def test_run_putgist_cli_with_username(mocker):
    mocker.patch('getgist.__main__.GetGist.put')
    result = runner.invoke(run_putgist, ["cuducos"])
    assert result.exit_code == 2
    assert "Error: Missing argument 'FILENAME'." in result.output

def test_run_putgist_cli_with_username_and_filaname(mocker):
    mocker.patch('getgist.__main__.GetGist.put')
    result = runner.invoke(run_putgist, ["cuducos", "~/.vimrc"])
    assert result.exit_code == 0

def test_run_lsgist_cli_without_username(mocker):
    mocker.patch('getgist.__main__.GetGist.put')
    result = runner.invoke(run_lsgists)
    assert result.exit_code == 2
    assert "Error: Missing argument 'USER'." in result.output

def test_run_lsgist_cli_with_username(mocker):
    mocker.patch('getgist.__main__.GetGist.put')
    result = runner.invoke(run_lsgists, ["cuducos"])
    assert result.exit_code == 0

def test_run_mygists_cli_without_username(mocker):
    mocker.patch('getgist.__main__.GetGist.put')
    result = runner.invoke(run_mygists)
    assert result.exit_code == 1

def test_run_mygists_cli_with_username(mocker, monkeypatch):
    monkeypatch.setenv("GETGIST_USER", "cuducos")
    mocker.patch('getgist.__main__.GetGist.put')
    result = runner.invoke(run_mygists)
    assert result.exit_code == 0
