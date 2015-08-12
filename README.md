# GetGist

Easily download any file from a public [GitHub Gist](http://gist.github.com), with a one single command.

[![Development Status: Alpha](https://img.shields.io/pypi/status/getgist.svg?style=flat)](https://pypi.python.org/pypi/getgist)
[![Latest release](https://img.shields.io/pypi/v/getgist.svg?style=flat)](https://pypi.python.org/pypi/getgist)
[![Travis CI](https://img.shields.io/travis/cuducos/getgist.svg?style=flat)](https://travis-ci.org/cuducos/getgist)
[![Downloads](https://img.shields.io/pypi/dm/getgist.svg?style=flat)](https://pypi.python.org/pypi/getgist)
[![Python Version](https://img.shields.io/pypi/pyversions/getgist.svg)](https://pypi.python.org/pypi/getgist) 
[![License](https://img.shields.io/pypi/l/getgist.svg?style=flat)](https://pypi.python.org/pypi/getgist)

## Why?

Because of reasons I do not have a *dotfiles* repository. I prefer to store my `.vimrc`, `.gitconfig`, `.bash_profile` etc. as [Gists](http://gist.github.com/).

I wrote this script so I could update my *dotfiles* with one single command: `getmy .vimrc`, for example, and it's done.

## Install

```
$ pip install getgist
```

*GetGist* works with Python 2.7+ or 3.4+ and is written only with Python core modules (no extra dependencies).

To update just run `$ pip install -U getgist`.

## Usage

Just run `getgist <user> <file>`. For example:

```
$ getgist cuducos .vimrc
  Fetching https://api.github.com/users/cuducos/gists …
  Fetching https://gist.githubusercontent.com/cuducos/1a2b3c4d5e/raw/1a2b3c4d5e1a2b3c4d5e/.vimrc …
  Replace existing .vimrc ? (y/n) y
  Deleting existing .vimrc …
  Saving new .vimrc …
  Saved as /home/cuducos/.vimrc
  Done!
```

If you decide not to delete your copy of the local file, it will be renamed with extensions such as `.bkp`, `.bkp.1`, `.bkp.2` etc.

## Setting a default user

You can set a default user to avoid typing your GitHub user name all the time.

1. Set an environment variable called `GETGIST_USER` (e.g. add something like `export GETGIST_USER='cuducos'` to your `.bash_profile`)
2. Use the shortcut `getmy <file>`

For example:

```
$ getmy .vimrc
  Fetching https://api.github.com/users/cuducos/gists …
  Fetching https://gist.githubusercontent.com/cuducos/1a2b3c4d5e/raw/1a2b3c4d5e1a2b3c4d5e/.vimrc …
  Saving new .vimrc …
  Saved as /home/cuducos/.vimrc
  Done!
```

## Contributing

Feel free to [report an issue](http://github.com/cuducos/getgist/issues), [open a pull request](http://github.com/cuducos/getgist/pulls), or [drop a line](http://twitter.com/cuducos).

Thank you very much [@ddboline](http://github.com/ddboline) and [/u/Sean1708](http://reddit.com/user/Sean1708) for the contributions!

### To do list

* Write tests for `entry_points`
* Authenticate users to allow the possibility of getting private Gists

### Tests


```
$ pip install nose
$ nosetests
```

In Python 2 you also need to install [mock](https://github.com/testing-cabal/mock) (e.g. `pip install mock`).

## Changelog

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

Copyright (c) 2015 Eduardo Cuducos

Licensed under the [MIT License](LICENSE).