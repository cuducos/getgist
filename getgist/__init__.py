from click import secho
from sys import stderr, stdout


class GetGistCommons(object):

    indent_size = 2
    indent_char = ' '

    def indent(self, message):
        indent = self.indent_char * self.indent_size
        return indent + message

    def output(self, message, color=None):
        """A helper to indent print()"""
        output_to = stderr if color == 'red' else stdout
        secho(self.indent(message), fg=color, file=output_to)

    def ask(self, message):
        """A helper to indent input()"""
        return input(self.indent(message))

    def oops(self, message):
        return self.output(message, color='red')

    def yeah(self, message):
        return self.output(message, color='green')

    def warn(self, message):
        return self.output(message, color='yellow')

    def hey(self, message):
        return self.output(message, color='blue')
