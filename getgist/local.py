import os

from click import confirm

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
        self.file_path = os.path.expanduser(filename)
        self.filename = os.path.basename(filename)
        self.assume_yes = assume_yes

    def save(self, content):
        """
        Save any given content to the instance file.
        :param content: (str or bytes)
        :return: (None)
        """
        # backup existing file if needed
        if os.path.exists(self.file_path) and not self.assume_yes:
            message = "Overwrite existing {}? (y/n) "
            if not confirm(message.format(self.filename)):
                self.backup()

        # write file
        self.output("Saving " + self.filename)
        with open(self.file_path, "wb") as handler:
            if not isinstance(content, bytes):
                content = bytes(content, "utf-8")
            handler.write(content)
        self.yeah("Done!")

    def backup(self):
        """Backups files with the same name of the instance filename"""
        count = 0
        name = "{}.bkp".format(self.filename)
        backup = os.path.join(self.cwd, name)
        while os.path.exists(backup):
            count += 1
            name = "{}.bkp{}".format(self.filename, count)
            backup = os.path.join(self.cwd, name)
        self.hey("Moving existing {} to {}".format(self.filename, name))
        os.rename(os.path.join(self.cwd, self.filename), backup)

    def read(self, file_path=None):
        """
        Read the contents of a file.
        :param filename: (str) path to a file in the local file system
        :return: (str) contents of the file, or (False) if not found/not file
        """
        if not file_path:
            file_path = self.file_path

        # abort if the file path does not exist
        if not os.path.exists(file_path):
            self.oops("Sorry, but {} does not exist".format(file_path))
            return False

        # abort if the file path is not a file
        if not os.path.isfile(file_path):
            self.oops("Sorry, but {} is not a file".format(file_path))
            return False

        with open(file_path) as handler:
            return handler.read()
