import os

from getgist import GetGistCommons


class LocalTools(GetGistCommons):
    """Helpers to deal with local files and local file system"""

    def __init__(self, filename, assume_yes=False):
        """
        Sets the file name to be used by the instance.
        :param filename: (str) local file name (ro be read or written)
        :param assume_yes: (bool) assume yes (or first option) for all prompts
        return: (None)
        """
        self.cwd = os.getcwd()
        self.filename = filename
        self.assume_yes = assume_yes
        self.path = os.path.join(self.cwd, filename)

    def save(self, content):
        """
        Save any given content to the instance file.
        :param content: (str or bytes)
        :return: (None)
        """
        # backup existing file if needed
        if os.path.exists(self.path) and not self.assume_yes:
            message = 'Overwrite existing {}? (y/n) '
            confirm = self.ask(message.format(self.filename))
            if confirm.lower() != 'y':
                self.backup()

        # write file
        self.output('Saving ' + self.filename)
        with open(self.path, 'wb') as handler:
            if not isinstance(content, bytes):
                content = bytes(content, 'utf-8')
            handler.write(content)
        self.yeah('Done!')

    def backup(self):
        """Backups files with the same name of the instance filename"""
        count = 0
        name = '{}.bkp'.format(self.filename)
        backup = os.path.join(self.cwd, name)
        while os.path.exists(backup):
            count += 1
            name = '{}.bkp{}'.format(self.filename, count)
            backup = os.path.join(self.cwd, name)
        self.hey('Moving existing {} to {}'.format(self.filename, name))
        os.rename(os.path.join(self.cwd, self.filename), backup)

    def read(self, filename=None):
        """
        Read the contents of a file.
        :param filename: (str) path to a file in the local file system
        :return: (str) contents of the file, or (False) if not found/not file
        """
        if not filename:
            filename = self.path

        # abort if the file path does not exist
        if not os.path.exists(filename):
            self.oops('Sorry, but {} does not exist locally'.format(filename))
            return False

        # abort if the file path is not a file
        if not os.path.isfile(filename):
            self.oops('Sorry, but {} is not a file'.format(filename))
            return False

        with open(filename) as handler:
            return handler.read()
