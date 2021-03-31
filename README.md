[![Travis CI](https://img.shields.io/travis/cuducos/getgist.svg?style=flat)](https://travis-ci.org/cuducos/getgist) [![Coveralls](https://img.shields.io/coveralls/cuducos/getgist.svg?style=flat)](https://coveralls.io/github/cuducos/getgist) [![PyPI Version](https://img.shields.io/pypi/v/getgist.svg?style=flat)](https://pypi.python.org/pypi/getgist) [![Python Version](https://img.shields.io/pypi/pyversions/getgist.svg?style=flat)](https://pypi.python.org/pypi/getgist)

# GetGist

Easily download any file from a [GitHub Gist](http://gist.github.com), with _one single command_.

## Why?

Because of reasons I do not have a *dotfiles* repository. I prefer to store my `init.vim`, `.gitconfig`, `.bashrc` etc. as [Gists](http://gist.github.com/).

I wrote this CLI so I could update my *dotfiles* with one single command: `getmy vim.init`, for example — and it's done.

## Install

```console
$ pip install getgist
```

_GetGist_ works with Python 3.6+.

To **update** it just run `$ pip install --upgrade getgist`.

## Usage

### Getting Gists from GitHub

Just run `getgist <username> <filename>`. For example:

```console
$ getgist cuducos .vimrc
  Fetching https://api.github.com/users/cuducos/gists
  Reading https://gist.githubusercontent.com/cuducos/409fac6ac23bf515f495/raw/666d7d01a0058e4fd898ff752db66160f10a60bb/.vimrc
  Saving .vimrc
  Done!
```

_GetGist_ asks you what to do when a local file (with the same name) exists. If you decide not to delete your local copy of the file, it will be renamed with extensions such as `.bkp`, `.bkp1`, `.bkp2` etc.

### Updating Gists at GitHub

Just run `putgist <username> <filename>` to update the remote Gist with the contents of the local file. It requires an OAuth token (see [Using OAuth authentication](#using-oauth-authentication) below). For example:

```console
$ putgist cuducos .vimrc
  User cuducos authenticated
  Fetching https://api.github.com/gists
  Sending contents of .vimrc to https://api.github.com/gists/409fac6ac23bf515f495
  Done!
  The URL to this Gist is: https://gist.github.com/cuducos/409fac6ac23bf515f495
```

_GetGist_ asks you what to do when it finds the different files with the same name in different Gists.

### Listing Gist files from GitHub

Just run `lsgists <username>`. For example:

```console
$ lsgists cuducos
  Gist           File               URL
  -------------  ------------------ -------------------------
  First Gist     file.md            https://gist.github.com/…
  My Gist #2     another_file.md    https://gist.github.com/…
  My Gist #2     README.md          https://gist.github.com/…
```

Secret Gists (when user is authenticated) are listed with `[Secret Gist]` tag next to their names.

## Using OAuth authentication

### Why?

Add your [personal access token](https://github.com/settings/tokens) as as environment variable to allow:

1. downloading private gists
2. updating existing gists
3. listing private gists

### How?

1. Get a personal access token with permission to manage your gists from [GitHub settings](https://github.com/settings/tokens)
2. Set an environment variable called `GETGIST_TOKEN` with your personal access token

This [article](https://www.serverlab.ca/tutorials/linux/administration-linux/how-to-set-environment-variables-in-linux/) might help you create an environment variable in a Unix-based operational system with Bash, but feel free to search alternatives for other systems and shells.

### Example

```console
$ export GETGIST_TOKEN=whatever1234
$ getgist cuducos .vimrc
  User cuducos authenticated
  Fetching https://api.github.com/gists
  Reading https://gist.githubusercontent.com/cuducos/409fac6ac23bf515f495/raw/666d7d01a0058e4fd898ff752db66160f10a60bb/.vimrc
  Saving .vimrc
  Done!
  The URL to this Gist is: https://gist.github.com/cuducos/409fac6ac23bf515f495
```

This will work even if the file you are trying to download is a private gist (surely the user name has to match the `GETGIST_TOKEN` account).

## Setting a default user

### Why?

Set a default user to avoid typing your GitHub user name all the time.

### How?

1. Set an environment variable called `GETGIST_USER` with your GitHub user name
2. Use the shortcut `getmy <filename>`, `putmy <filename>` or `mygists`

### Example

```console
$ export GETGIST_USER=cuducos
$ getmy .vimrc
  Fetching https://api.github.com/users/cuducos/gists
  Reading https://gist.githubusercontent.com/cuducos/409fac6ac23bf515f495/raw/666d7d01a0058e4fd898ff752db66160f10a60bb/.vimrc
  Saving .vimrc
  Done!
  The URL to this Gist is: https://gist.github.com/cuducos/409fac6ac23bf515f495
```

## Contributing

We use [Poetry](https://python-poetry.org) to manage our development environment:

1. `poetry install` will get you a virtualenv with all the dependencies for you
1. `poetry shell` will activate this virtualenv
1. `exit` deactivates this virtualenv

Feel free to [report an issue](http://github.com/cuducos/getgist/issues), [open a pull request](http://github.com/cuducos/getgist/pulls), or [drop a line](http://twitter.com/cuducos).

Don't forget to format your code with [Black](https://github.com/ambv/black), and to write and run tests:

```console
$ tox
```
