# GetGist

Easily download any file from a public [GitHub Gist](http://gist.github.com), with a one single command.

[![Latest release](https://pypip.in/version/getgist/badge.svg?style=flat-square)](https://pypi.python.org/pypi/getgist/)
[![Downloads](https://pypip.in/download/getgist/badge.svg?style=flat-square)](https://pypi.python.org/pypi/getgist/)
[![License](https://pypip.in/license/getgist/badge.svg?style=flat-square)](https://pypi.python.org/pypi/getgist/)
[![Supported Python versions](https://pypip.in/py_versions/getgist/badge.svg?style=flat-square)](https://pypi.python.org/pypi/getgist/)

## Why?

Because of reasons I do not have a `dotfiles` repository. I prefer to store my `.vimrc`, `.gitconfig`, `.bash_whatever` etc. as [Gists](http://gist.github.com/).

Thus, to be honest, I wrote this script so I could update my `dotfiles` with one single command.

## Install

`$ pip install getgist`

*GetGist* runs with Python 2 or 3 and is written **only** with core modules (no extra dependencies but Python).

## Usage

Just run `getgist <user> <file>`. For example:

```
user@localhost ~ $ getgist cuducos .vimrc
  Fetching https://api.github.com/users/cuducos/gists …
  Fetching https://gist.githubusercontent.com/cuducos/409fac6ac23bf515f495/raw/f8acc26f0422b02fc282c5b4e97b70710044dbb3/.vimrc …
  Replace existing .vimrc ? (y/n) y
  Deleting existing .vimrc …
  Saving new .vimrc …
  Done!
user@localhost ~ $
```

If you decide not to delete your copy of the local file, it will be renamed with extensions such as `.bkp`, `.bkp.1`, `.bkp.2` etc.

## Contributing

Feel free to [report an issue](http://github.com/cuducos/getgist/issues), [open a pull request](http://github.com/cuducos/getgist/pulls), or [drop a line](http://twitter.com/cuducos).

### To do list

* Authenticate users to:
  * Have a default user (`$ getgist .vimrc` to mine, `$ getgist johndoe .vimrc` to get John's one)
  * Allow the possibility of getting private Gists
* Write tests for `Gist.__backup()`

## License

So far I consider this script just public domain.
