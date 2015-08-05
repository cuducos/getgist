# coding: utf-8

import argparse
import json
import os

try:
    from urllib2 import HTTPError, urlopen
    input = raw_input
except ImportError:
    from urllib.request import HTTPError, urlopen


class Gist(object):

    def __init__(self, user=False, file_name=False, assume_yes=False):

        # set main variables
        self.user = user
        self.file_name = file_name
        self.assume_yes = assume_yes

        # load arguments
        if not self.user or not self.file_name:

            # set argparse
            parser = argparse.ArgumentParser()
            parser.add_argument('user', help='Gist username')
            parser.add_argument('file_name', help='Gist file name')
            parser.add_argument('-y', '--yes-to-all',
                                help='Assume `yes` to all prompts',
                                action="store_true")

            # load values from argparse
            args = parser.parse_args()
            if not user:
                self.user = args.user
            if not file_name:
                self.file_name = args.file_name
            if not assume_yes:
                self.assume_yes = args.yes_to_all

        # set support variables
        self.local_dir = os.path.realpath(os.curdir)
        self.local_path = os.path.join(self.local_dir, self.file_name)
        self.info = self.__load_info()

    @property
    def id(self):
        if self.info:
            return self.info.get('id', None)
        return False

    @property
    def raw_url(self):
        if self.info:
            return self.info.get('raw_url', None)
        return False

    def save(self):

        # check if file exists
        if os.path.exists(self.local_path):

            # delete or backup existing file?
            confirm = 'y'
            if not self.assume_yes:
                message = '  Delete existing {} ? (y/n) '
                confirm = input(message.format(self.file_name))

            # delete exitsing file
            if confirm.lower() == 'y':
                self.__output('Deleting existing {} …'.format(self.file_name))
                os.remove(self.local_path)

            # backup existing file
            else:
                self.__backup()

        # save new file
        with open(self.local_path, 'w') as file_handler:
            contents = self.load()
            self.__output('Saving new {} …'.format(self.file_name))
            file_handler.write(contents)
        self.__output('Saved as {}'.format(os.path.abspath(self.local_path)))
        self.__output('Done!')

    def __backup(self):
        count = 0
        name = '{}.bkp'.format(self.file_name)
        backup = os.path.join(self.local_dir, name)
        while os.path.exists(backup):
            count += 1
            name = '{}.bkp.{}'.format(self.file_name, count)
            backup = os.path.join(self.local_dir, name)
        self.__output('Moving existing {} to {}…'.format(self.file_name, name))
        os.rename(os.path.join(self.local_dir, self.file_name), backup)

    def __load_info(self):
        url = 'https://api.github.com/users/{}/gists'.format(self.user)
        gists = json.loads(str(self.__curl(url)))
        for gist in gists:
            if self.file_name in gist['files']:
                return {'id': gist['id'],
                        'raw_url': gist['files'][self.file_name]['raw_url']}
        return False

    def __curl(self, url):

        # try to connect
        self.__output('Fetching {} …'.format(url))
        try:
            request = urlopen(url)
            status = request.getcode()
        except HTTPError:
            self.__output("[Error] Couldn't reach GitHub at {}.".format(url))
            return ''

        # if it works
        if status == 200:
            contents = request.read()
            return contents.decode('utf-8')

        # in case of error
        self.__output('[Error] HTTP Status {}.'.format(url, status))
        return ''

    def __output(self, message):
        print('  {}'.format(message))


def run():
    gist = Gist()
    if gist.info:
        gist.save()
