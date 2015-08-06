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
        self.info = self.load_gist_info()

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
                self.output('Deleting existing {} …'.format(self.file_name))
                os.remove(self.local_path)

            # backup existing file
            else:
                self.backup()

        # save new file
        with open(self.local_path, 'w') as file_handler:
            contents = self.curl(self.raw_url)
            self.output('Saving new {} …'.format(self.file_name))
            file_handler.write(contents)
        self.output('Saved as {}'.format(os.path.abspath(self.local_path)))
        self.output('Done!')

    def backup(self):
        count = 0
        name = '{}.bkp'.format(self.file_name)
        backup = os.path.join(self.local_dir, name)
        while os.path.exists(backup):
            count += 1
            name = '{}.bkp.{}'.format(self.file_name, count)
            backup = os.path.join(self.local_dir, name)
        self.output('Moving existing {} to {}…'.format(self.file_name, name))
        os.rename(os.path.join(self.local_dir, self.file_name), backup)

    def load_gist_info(self):

        # return Gist info if Gist is found
        gists = [gist for gist in self.filter_gists()]
        if gists:
            return self.select_file(gists)

        # return False if no match if found
        error = "[Error] No file named `{}` found in {}'s public Gists."
        self.output(error.format(self.file_name, self.user))
        return False

    def filter_gists(self):
        for gist in self.query_api():
            if self.file_name in gist['files']:
                yield {'id': gist['id'],
                       'description': gist['description'],
                       'raw_url': gist['files'][self.file_name]['raw_url']}

    def query_api(self):
        url = 'https://api.github.com/users/{}/gists'.format(self.user)
        contents = str(self.curl(url))
        if not contents:
            self.output('[Hint] Check if the entered user name is correct.')
            return list()
        return json.loads(contents)

    def select_file(self, files):

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
            self.output(question)
            options = '[{}] {}'
            valid_indexes = list()
            for f in files:
                index = files.index(f)
                valid_indexes.append(index)
                self.output(options.format(index + 1, f['description']))

            # get the gist index
            try:
                gist_index = int(input('Type the number: ')) - 1
            except:
                self.output('Please type a number.')
                return self.select_file(files)

            # check if entered index is valid
            if gist_index not in valid_indexes:
                self.output('Invalid number, please try again.')
                return self.select_file(files)

            # return the approproate file
            selected = files[gist_index]
            self.output('Using `{}` Gist…'.format(selected['description']))
            return selected

    def curl(self, url):

        # try to connect
        self.output('Fetching {} …'.format(url))
        try:
            request = urlopen(url)
            status = request.getcode()
        except HTTPError:
            self.output("[Error] Couldn't reach GitHub at {}.".format(url))
            return ''

        # if it works
        if status == 200:
            contents = request.read()
            return contents.decode('utf-8')

        # in case of error
        self.output('[Error] HTTP Status {}.'.format(url, status))
        return ''

    def output(self, message):
        print('  {}'.format(message))


def run():
    gist = Gist()
    if gist.info:
        gist.save()
