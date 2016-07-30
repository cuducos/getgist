# GetGist

Easily download any file from a [GitHub Gist](http://gist.github.com), with _one single command_.

[![Latest release](https://img.shields.io/pypi/v/getgist.svg?style=flat)](https://pypi.python.org/pypi/getgist)
[![Python Version](https://img.shields.io/pypi/pyversions/getgist.svg?style=flat)](https://pypi.python.org/pypi/getgist) 
[![Downloads](https://img.shields.io/pypi/dm/getgist.svg?style=flat)](https://pypi.python.org/pypi/getgist)
[![License](https://img.shields.io/pypi/l/getgist.svg?style=flat)](https://pypi.python.org/pypi/getgist)

[![Travis CI](https://img.shields.io/travis/cuducos/getgist.svg?style=flat)](https://travis-ci.org/cuducos/getgist)
[![Covearge](https://img.shields.io/coveralls/cuducos/getgist.svg?style=flat)](https://coveralls.io/github/cuducos/getgist)
[![Code Health](https://landscape.io/github/cuducos/getgist/master/landscape.svg?style=flat)](https://landscape.io/github/cuducos/getgist/master)

## Why?

Because of reasons I do not have a *dotfiles* repository. I prefer to store my `.vimrc`, `.gitconfig`, `.bash_profile` etc. as [Gists](http://gist.github.com/).

I wrote this script so I could update my *dotfiles* with one single command: `getmy .vimrc`, for example, and it's done.

## Install

```
$ pip install getgist
```

*GetGist* works with Python 2.7+ or 3.4+.

To **update** just run `$ pip install -U getgist`.

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

Just run `putgist <username> <filename>` to upate the remote Gist with the contents of the local file. It requires an OAuth token (see _Using OAuth authentication_ below). For example:

```console
$ putgist cuducos .vimrc
  User cuducos authenticated
  Fetching https://api.github.com/gists
  Sending contents of .vimrc to https://api.github.com/gists/409fac6ac23bf515f495
  Done!
  The URL to this Gist is: https://gist.github.com/cuducos/409fac6ac23bf515f495
```

_GetGist_ asks you what to do when it finds the different files with the same name in different Gists.

## Using OAuth authentication

### Why?

Add your [personal access token](https://github.com/settings/tokens) as as enviroment variable to allow:

1. the download of private Gists
2. the update of existing Gists

### How?

1. Get a personal access token with permission to manage your _gists_ from [GitHub settings](https://github.com/settings/tokens)
2. Set an environment variable called `GETGIST_TOKEN` with your personal access token

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

This will work even if the file you are trying to download is a private gist (surely the user name has to macth the `GETGIST_TOKEN` account).

## Setting a default user

### Why?

Set a default user to avoid typing your GitHub user name all the time

### How?

1. Set an environment variable called `GETGIST_USER` with your GitHub username
2. Use the shortcut `getmy <filename>` or `putmy <filename>`

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

Feel free to [report an issue](http://github.com/cuducos/getgist/issues), [open a pull request](http://github.com/cuducos/getgist/pulls), or [drop a line](http://twitter.com/cuducos).

Thank you very much [@ddboline](http://github.com/ddboline) and [/u/Sean1708](http://reddit.com/user/Sean1708) for the contributions!

Don't forget to write and run tests:

```console
$ python -m pip install tox
$ python setup.py test
```

## Changelog

* **0.1.0**
  * Complete re-write
  * Add personal access token (OAuth)
  * Allow the update of existing Gists at GitHub (when authenticated)
  * Allow the download of private Gists (when authenticated)  
  * Fix bug when getting gists with non standard encoding (UnicodeEncodeError)
* **0.0.6**
  * Add default user feature
* **0.0.5**
  * Ask user which Gist to use if more than one file is found
  * General code improvements
* **0.0.4**
  * Use `entry_points` instead of `scripts`
* **0.0.3**
  * Fix a bug related to the directory where the file was being saved
* **0.0.2**
  * Fix a bug related to the installation, path and import

## License

Copyright (c) 2016 Eduardo Cuducos

Licensed under the [MIT License](LICENSE).