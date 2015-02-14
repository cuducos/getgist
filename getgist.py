# coding: utf-8

import argparse
import os
import re
import urllib2


class file_name(object):

    def __init__(self, user=None, file_name=None):

        # load arguments
        parser = argparse.ArgumentParser()
        parser.add_argument('-y', '--yes-to-all',
                            help='Assume `yes` to all prompts',
                            action="store_true")
        parser.add_argument('user', help='Gist username')
        parser.add_argument('file_name', help='Gist file name')
        args = parser.parse_args()

        # set http request variables
        self.user = args.user
        self.file_name = args.file_name
        self.domain = 'https://gist.github.com'
        self.assume_yes = args.yes_to_all

        # current directory
        self.current = os.path.dirname(os.path.realpath(__file__))

        # regex to find a link tag – use .format(…) to include tag contents
        self.link_tag = r'<a[\w\s=:.,-?i\'"</>]+{}[</>\w]*<\/a>'

        # regexp to find a href attribute
        self.href_attribute = r'href=[\'"][\w/\/.:=?]+[\'"]'

    def run(self):
        gist_url = self.__get_url(self.user, self.file_name)
        if gist_url:
            gist_raw_url = self.__get_url(gist_url, 'Raw')
            if gist_raw_url:
                contents = self.__get_contents(gist_raw_url)
                self.__save(contents)
            else:
                print "  Couldn't fetch gist raw URL"
        else:
            print "  Couldn't fetch gist URL"

    def __get_url(self, location, name):
        data = self.__get_contents(location)
        if data:
            tag = self.__match(self.link_tag.format(name), data)
            if tag:
                gist_url = self.__match(self.href_attribute, tag)
                if gist_url:
                    return gist_url[6:-1]
        return False

    def __match(self, regex, data):
        data = data.replace('href="/{0}">{0}</a>'.format(self.user), '')
        search = re.search(regex, data)
        if search:
            return search.group(0)
        else:
            print "  Couldn't match regular expression"
            print "  regexp: ", regex
            print "  data: ", data[0:140], '…'
            return search

    def __get_contents(self, location):
        if location[0:1] != '/':
            location = '/{}'.format(location)
        url = '{}{}'.format(self.domain, location)
        print "  Fetching {} ...".format(url)
        request = urllib2.urlopen(url)
        status = request.getcode()
        if status == 200:
            return request.read()
        else:
            print status
            print request.info()
            return False

    def __save(self, contents):

        # currentd ir and file path
        file_path = os.path.join(self.current, self.file_name)

        # check if file exists
        if os.path.exists(file_path):

            # delete or backup existing file?
            confirm = 'y'
            if not self.assume_yes:
                message = '  Replace existing {} ? (y/n) '
                confirm = raw_input(message.format(self.file_name))

            # delete exitsing file
            if confirm.lower() == 'y':
                print "  Deleting existing {} …".format(self.file_name)
                os.remove(file_path)

            # backup existing file
            else:
                self.__backup()

        # save new file
        with open(file_path, 'w') as file_handler:
            print "  Saving new {} …".format(self.file_name)
            file_handler.write(contents)
        print "  Done!"

    def __backup(self):
        count = 0
        name = '{}.bkp'.format(self.file_name)
        backup = os.path.join(self.current, name)
        while os.path.exists(backup):
            count += 1
            name = '{}.bkp.{}'.format(self.file_name, count)
            backup = os.path.join(self.current, name)
        print "  Saving existing {} as {}".format(self.file_name, name)
        os.rename(os.path.join(self.current, self.file_name), backup)

run_forrest = file_name()
run_forrest.run()
