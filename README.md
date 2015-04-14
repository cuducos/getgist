# GetGist

This is a simple script I wrote to easily download any file from a public [GitHub Gist](http://gist.github.com) account.

For some reason I do not have a `dotfile` repository because I prefer to store my `.vimrc`, `.gitconfig`, `.bash_whatever` etc. as gists. I wrote this script so I can update my `.vimrc` with one single command.

## Installing

Just copy the `getgist.py` to the directory where you want to have your files downloaded.

## Usage

Just run `python getgist.py <user> <file>`. For example:

```
vagrant@vagrant ~ $ python getgist.py cuducos .vimrc
  Fetching https://api.github.com/users/cuducos/gists …
  Fetching https://gist.githubusercontent.com/cuducos/409fac6ac23bf515f495/raw/f8acc26f0422b02fc282c5b4e97b70710044dbb3/.vimrc …
  Replace existing .vimrc ? (y/n) y
  Deleting existing .vimrc …
  Saving new .vimrc …
  Done!
vagrant@vagrant ~ $
```

If you decide **not to delete** your copy of the local file, the **local file is renamed** with an extension such as `.bkp`, `.bkp.1`, `.bkp.2` etc.

## To do list

* Distribute it as standard PyPI package
* Make it a CLI command (e.g. `$ getgist cuducos .vimrc`)
* Store default user (e.g. `$ getgist .vimrc` to download my `.vimrc` but `$ getgist johndoe .vimrc` to download John's one)

## License

So far I consider this script just public domain.
