.. image:: https://img.shields.io/travis/cuducos/getgist.svg?style=flat
   :target: https://travis-ci.org/cuducos/getgist
.. image:: https://img.shields.io/coveralls/cuducos/getgist.svg?style=flat
   :target: https://coveralls.io/github/cuducos/getgist
.. image:: https://img.shields.io/codeclimate/maintainability-percentage/cuducos/getgist.svg
   :target: https://codeclimate.com/github/cuducos/getgist
.. image:: https://img.shields.io/pypi/v/getgist.svg?style=flat
   :target: https://pypi.python.org/pypi/getgist
.. image:: https://img.shields.io/pypi/pyversions/getgist.svg?style=flat
   :target: https://pypi.python.org/pypi/getgist

GetGist
=======

Easily download any file from a `GitHub
Gist <http://gist.github.com>`__, with *one single command*.

Why?
----

Because of reasons I do not have a *dotfiles* repository. I prefer to
store my ``.vimrc``, ``.gitconfig``, ``.bash_profile`` etc. as
`Gists <http://gist.github.com/>`__.

I wrote this script so I could update my *dotfiles* with one single
command: ``getmy .vimrc``, for example — and it's done.

Install
-------

::

    $ pip install getgist

*GetGist* works with Python 2.7+ or 3.4+.

To **update** just run ``$ pip install -U getgist``.

Usage
-----

Getting Gists from GitHub
~~~~~~~~~~~~~~~~~~~~~~~~~

Just run ``getgist <username> <filename>``. For example:

.. code:: console

    $ getgist cuducos .vimrc
      Fetching https://api.github.com/users/cuducos/gists
      Reading https://gist.githubusercontent.com/cuducos/409fac6ac23bf515f495/raw/666d7d01a0058e4fd898ff752db66160f10a60bb/.vimrc
      Saving .vimrc
      Done!

*GetGist* asks you what to do when a local file (with the same name)
exists. If you decide not to delete your local copy of the file, it will
be renamed with extensions such as ``.bkp``, ``.bkp1``, ``.bkp2`` etc.

Updating Gists at GitHub
~~~~~~~~~~~~~~~~~~~~~~~~

Just run ``putgist <username> <filename>`` to upate the remote Gist with
the contents of the local file. It requires an OAuth token (see *Using
OAuth authentication* below). For example:

.. code:: console

    $ putgist cuducos .vimrc
      User cuducos authenticated
      Fetching https://api.github.com/gists
      Sending contents of .vimrc to https://api.github.com/gists/409fac6ac23bf515f495
      Done!
      The URL to this Gist is: https://gist.github.com/cuducos/409fac6ac23bf515f495

*GetGist* asks you what to do when it finds the different files with the
same name in different Gists.

Using OAuth authentication
--------------------------

Why?
~~~~

Add your `personal access token <https://github.com/settings/tokens>`__
as as enviroment variable to allow:

1. the download of private Gists
2. the update of existing Gists

How?
~~~~

1. Get a personal access token with permission to manage your *gists*
   from `GitHub settings <https://github.com/settings/tokens>`__
2. Set an environment variable called ``GETGIST_TOKEN`` with your personal access token

This `article <https://www.serverlab.ca/tutorials/linux/administration-linux/how-to-set-environment-variables-in-linux/>`__ might help you create an environment >variable in a Unix-based operational system with Bash, but feel free to search alternatives for other systems and shells.

Example
~~~~~~~

.. code:: console

    $ export GETGIST_TOKEN=whatever1234
    $ getgist cuducos .vimrc
      User cuducos authenticated
      Fetching https://api.github.com/gists
      Reading https://gist.githubusercontent.com/cuducos/409fac6ac23bf515f495/raw/666d7d01a0058e4fd898ff752db66160f10a60bb/.vimrc
      Saving .vimrc
      Done!
      The URL to this Gist is: https://gist.github.com/cuducos/409fac6ac23bf515f495

This will work even if the file you are trying to download is a private
gist (surely the user name has to macth the ``GETGIST_TOKEN`` account).

Setting a default user
----------------------

Why?
~~~~

Set a default user to avoid typing your GitHub user name all the time

How?
~~~~

1. Set an environment variable called ``GETGIST_USER`` with your GitHub
   username
2. Use the shortcut ``getmy <filename>`` or ``putmy <filename>``

Example
~~~~~~~

.. code:: console

    $ export GETGIST_USER=cuducos
    $ getmy .vimrc
      Fetching https://api.github.com/users/cuducos/gists
      Reading https://gist.githubusercontent.com/cuducos/409fac6ac23bf515f495/raw/666d7d01a0058e4fd898ff752db66160f10a60bb/.vimrc
      Saving .vimrc
      Done!
      The URL to this Gist is: https://gist.github.com/cuducos/409fac6ac23bf515f495

Contributing
------------

Feel free to `report an
issue <http://github.com/cuducos/getgist/issues>`__, `open a pull
request <http://github.com/cuducos/getgist/pulls>`__, or `drop a
line <http://twitter.com/cuducos>`__.

Thank you very much `@ddboline <http://github.com/ddboline>`_ and
`/u/Sean1708 <http://reddit.com/user/Sean1708>`_ for the contributions!

Don't forget to format your code with `Black <https://github.com/ambv/black>`_, and to write and run tests:

.. code:: console

    $ pip install tox
    $ tox
