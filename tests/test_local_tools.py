import os

from getgist import GetGistCommons
from tests.conftest import TEST_FILE_CONTENTS


def test_read_file_without_argument(local):
    assert local.read() == TEST_FILE_CONTENTS


def test_read_file_with_argument(local):
    assert local.read(local.file_path) == TEST_FILE_CONTENTS


def test_read_non_existet_file(mocker, local):
    error_message = mocker.patch.object(GetGistCommons, "error_message")
    assert not local.read(".no_gist")
    error_message.assert_called_once_with("Sorry, but .no_gist does not exist")


def test_read_directory(mocker, local):
    error_message = mocker.patch.object(GetGistCommons, "error_message")
    cwd = os.getcwd()
    assert not local.read(cwd)
    error_message.assert_called_once_with("Sorry, but {} is not a file".format(cwd))


def test_read_file_inside_directory(temporary_file):
    assert temporary_file.read() == TEST_FILE_CONTENTS


def test_simple_backup(local):
    backup = "{}.bkp".format(local.file_path)

    local.backup()
    assert os.path.exists(backup)
    assert local.read(backup) == TEST_FILE_CONTENTS


def test_two_backups(local):
    backup = "{}.bkp".format(local.file_path)
    with open(backup, "w") as fobj:
        fobj.write("first backup")

    new_backup = "{}1".format(backup)
    local.backup()
    assert os.path.exists(new_backup)
    assert local.read(new_backup) == TEST_FILE_CONTENTS


def test_multi_backups(local):
    for ext in ("", ".bkp", ".bkp1", ".bkp2", ".bkp3"):
        backup = "{}{}".format(local.file_path, ext)
        with open(backup, "w") as fobj:
            fobj.write(ext or TEST_FILE_CONTENTS)

    new_backup = "{}.bkp4".format(local.file_path)
    local.backup()
    assert os.path.exists(new_backup)
    assert local.read(new_backup) == TEST_FILE_CONTENTS


def test_write_file(local):
    os.remove(local.file_path)
    assert not os.path.exists(local.file_path)

    local.save(TEST_FILE_CONTENTS)
    assert os.path.exists(local.file_path)
    assert local.read() == TEST_FILE_CONTENTS


def test_write_file_overwrite(local, mocker):
    confirm = mocker.patch("getgist.local.confirm")
    confirm.return_value = True

    with open(local.file_path, "w") as fobj:
        fobj.write("nope")

    assert os.path.exists(local.file_path)
    assert local.read() == "nope"

    local.save(TEST_FILE_CONTENTS)
    assert os.path.exists(local.file_path)
    assert local.read() == TEST_FILE_CONTENTS
    assert not os.path.exists("{}.bkp1".format(local.file_path))


def test_write_file_with_backup(local, mocker):
    confirm = mocker.patch("getgist.local.confirm")
    confirm.return_value = False
    local.save(TEST_FILE_CONTENTS)

    assert os.path.exists(local.file_path)
    assert local.read() == TEST_FILE_CONTENTS

    backup = "{}.bkp1".format(local.file_path)
    local.save("new contents")
    assert os.path.exists(local.file_path)
    assert os.path.exists(backup)
    assert local.read() == "new contents"
    assert local.read(backup) == TEST_FILE_CONTENTS


def test_write_file_with_multiple_backup(local, mocker):
    for ext in ("", ".bkp", ".bkp1", ".bkp2", ".bkp3"):
        backup = "{}{}".format(local.file_path, ext)
        with open(backup, "w") as fobj:
            fobj.write(ext)

    confirm = mocker.patch("getgist.local.confirm")
    confirm.return_value = False

    local.save(TEST_FILE_CONTENTS)
    assert local.read() == TEST_FILE_CONTENTS
    for ext in ("", ".bkp", ".bkp1", ".bkp2", ".bkp3", ".bkp4"):
        backup = "{}{}".format(local.file_path, ext)
        assert os.path.exists(backup)
