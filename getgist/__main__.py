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
        self.info = self.__load_gist_info()

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
            contents = self.__curl(self.raw_url)
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

    def __load_gist_info(self):

        # return Gist info if Gist is found
        gists = [gist for gist in self.__filter_gists()]
        if gists:
            return self.__select_file(gists)

        # return False if no match if found
        error = "[Error] No file named `{}` found in {}'s public Gists."
        self.__output(error.format(self.file_name, self.user))
        return False

    def __filter_gists(self):
        for gist in self.__query_api():
            if self.file_name in gist['files']:
                yield {'id': gist['id'],
                       'description': gist['description'],
                       'raw_url': gist['files'][self.file_name]['raw_url']}

    def __query_api(self):
        url = 'https://api.github.com/users/{}/gists'.format(self.user)
        contents = str(self.__curl(url))
        if not contents:
            self.__output('[Hint] Check if the entered user name is correct.')
            return list()
        return json.loads(contents)

    def __select_file(self, files):

        # return false if no match
        if len(files) == 0:
            return False

        # if there is only one match (or `yes to all`), return the 1st match
        elif len(files) == 1 or self.assume_yes:
            return files[0]

        # if we have more macthes return the appropriate one
        else:

            # list and ask
            question = 'Download {} from which Gist?'.format(self.file_name)
            self.__output(question)
            options = '[{}] {}'
            valid_indexes = list()
            for f in files:
                index = files.index(f)
                valid_indexes.append(index)
                self.__output(options.format(index + 1, f['description']))

            # get the gist index
            try:
                gist_index = int(input('Type the number: ')) - 1
            except:
                self.__output('Please type a number.')
                return self.__select_file(files)

            # check if entered index is valid
            if gist_index not in valid_indexes:
                self.__output('Invalid number, please try again.')
                return self.__select_file(files)

            # return the approproate file
            selected = files[gist_index]
            self.__output('Using `{}` Gist…'.format(selected['description']))
            return selected

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
