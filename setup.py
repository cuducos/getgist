from setuptools import setup

REPO_URL = 'http://github.com/cuducos/getgist'

setup(author='Eduardo Cuducos',
      author_email='cuducos@gmail.com',
      classifiers=['Development Status :: 4 - Beta',
                   'Programming Language :: Python :: 2.7',
                   'Programming Language :: Python :: 3.4',
                   'Programming Language :: Python :: 3.5',
                   'Intended Audience :: Developers',
                   'Topic :: Utilities',
                   'License :: OSI Approved :: MIT License'],
      description='Command-line to update local files from GitHub gists',
      entry_points={'console_scripts': ['getgist=getgist.__init__:run_getgist',
                                        'getmy=getgist.__init__:run_getmy',
                                        'putgist=getgist.__init__:run_putgist',
                                        'putmy=getgist.__init__:run_putmy']},
      include_package_data=True,
      install_requires=['requests==2.9.1',
                        'python-decouple==3.0'],
      keywords='gist, command-line, github, dotfiles',
      license='MIT',
      long_description='Check `GetGist at GitHub <{}>`_.'.format(REPO_URL),
      name='getgist',
      packages=['getgist'],
      url=REPO_URL,
      version='0.1.0',
      zip_safe=False)
