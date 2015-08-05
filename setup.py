from setuptools import setup

url = 'http://github.com/cuducos/getgist'

setup(author='Eduardo Cuducos',
      author_email='cuducos@gmail.com',
      classifiers=['Development Status :: 4 - Beta',
                   'Programming Language :: Python :: 2.7',
                   'Programming Language :: Python :: 3.4',
                   'Intended Audience :: Developers',
                   'Topic :: Utilities',
                   'License :: OSI Approved :: MIT License'],
      description='Command-line to update local files from GitHub gists',
      entry_points={'console_scripts': ['getgist=getgist.__main__:run']},
      include_package_data=True,
      keywords='gist, command-line, github, dotfiles',
      license='MIT',
      long_description='Check `GetGist at GitHub <{}>`_.'.format(url),
      name='getgist',
      packages=['getgist'],
      url=url,
      version='0.0.5',
      zip_safe=False)
