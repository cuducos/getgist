from setuptools import setup

url = 'http://github.com/cuducos/getgist'

setup(author='Eduardo Cuducos',
      author_email='cuducos@gmail.com',
      classifiers=['Development Status :: 3 - Alpha',
                   'Programming Language :: Python :: 2.7',
                   'Programming Language :: Python :: 3.4',
                   'Intended Audience :: Developers',
                   'Topic :: Utilities',
                   'License :: Public Domain'],
      description='Command-line to update local files from GitHub gists',
      include_package_data=True,
      keywords='gist, command-line, github, dotfiles',
      license='Public Domain',
      long_description='Check `GetGist at GitHub <{}>`_.'.format(url),
      name='getgist',
      scripts=['bin/getgist'],
      packages=['getgist'],
      package_dir={'getgist': 'getgist'},
      url=url,
      version='0.0.1',
      zip_safe=False)
