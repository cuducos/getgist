import os

from . import GetGistCommons


class LocalTools(GetGistCommons):

    def __init__(self, filename):
        self.cwd = os.getcwd()
        self.filename = filename
        self.path = os.path.join(self.cwd, filename)

    def save(self, content):

        # backup existing file if needed
        if os.path.exists(self.path):
            message = 'Overwrite existing {}? (y/n) '
            confirm = self.ask(message.format(self.filename))
            if confirm.lower() != 'y':
                self.backup()

        # write file
        self.output('Saving ' + self.filename)
        with open(self.path, 'w') as handler:
            handler.write(content)
        self.output('Done!')

    def backup(self):
        count = 0
        name = '{}.bkp'.format(self.filename)
        backup = os.path.join(self.cwd, name)
        while os.path.exists(backup):
            count += 1
            name = '{}.bkp{}'.format(self.filename, count)
            backup = os.path.join(self.cwd, name)
        self.output('Moving existing {} to {}'.format(self.filename, name))
        os.rename(os.path.join(self.cwd, self.filename), backup)

    def read(self, filename=None):
        if not filename:
            filename = self.path
        with open(filename) as handler:
            return handler.read()
