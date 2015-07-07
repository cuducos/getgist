# GetGist

Easily download any file from a public [GitHub Gist](http://gist.github.com), with a one single command.

[![Development Status: Alpha](https://img.shields.io/pypi/status/getgist.svg?style=flat)](https://pypi.python.org/pypi/getgist)
[![Latest release](https://img.shields.io/pypi/v/getgist.svg?style=flat)](https://pypi.python.org/pypi/getgist)
[![Downloads](https://img.shields.io/pypi/dm/getgist.svg?style=flat)](https://pypi.python.org/pypi/getgist)
[![Python Version](https://img.shields.io/pypi/pyversions/getgist.svg)](https://pypi.python.org/pypi/getgist) 
[![License](https://img.shields.io/pypi/l/getgist.svg?style=flat)](https://pypi.python.org/pypi/getgist)

## Why?

Because of reasons I do not have a *dotfiles* repository. I prefer to store my `.vimrc`, `.gitconfig`, `.bash_whatever` etc. as [Gists](http://gist.github.com/).

I wrote this script so I could update my *dotfiles* with one single command.

## Install

`$ pip install getgist`

*GetGist* works with Python 2 or 3 and is written only with Python core modules (no extra dependencies).

## Usage

Just run `getgist <user> <file>`. For example, type:

```
$ getgist cuducos .vimrc
```

And follow the output:

```
  Fetching https://api.github.com/users/cuducos/gists …
  Fetching https://gist.githubusercontent.com/cuducos/409fac6ac23bf515f495/raw/f8acc26f0422b02fc282c5b4e97b70710044dbb3/.vimrc …
  Replace existing .vimrc ? (y/n) y
  Deleting existing .vimrc …
  Saving new .vimrc …
  Saved as /Users/cuducos/.vimrc
  Done!
```

If you decide not to delete your copy of the local file, it will be renamed with extensions such as `.bkp`, `.bkp.1`, `.bkp.2` etc.

## Contributing

Feel free to [report an issue](http://github.com/cuducos/getgist/issues), [open a pull request](http://github.com/cuducos/getgist/pulls), or [drop a line](http://twitter.com/cuducos).

Thank you very much [@ddboline](http://github.com/ddboline) and [/u/Sean1708](http://reddit.com/user/Sean1708) for the contributions!

### To do list

* Write tests for `entry_points`
* Authenticate users to:
  * Have a default user (e.g: `$ getgist .vimrc` to get my `.vimrc`, and `$ getgist johndoe .vimrc` to get John's one)
  * Allow the possibility of getting private Gists

### Tests

#### Python 2

```
$ pip install nose mock
$ nosetests
```

#### Python 3

```
$ pip install nose
$ nosetests
```

## Changelog

* **0.0.4**
  * Use `entry_points` instead of `scripts`
  * Implement tests for `Gist.__backup()`
* **0.0.3**
  * Fix a bug related to the directory where the file was being saved
* **0.0.2**
  * Fix a bug related to the installation, path and import

## License

Copyright (c) 2015 Eduardo Cuducos

Licensed under the [MIT License](LICENSE).