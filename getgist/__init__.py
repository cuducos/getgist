from sys import stderr, stdout

from tabulate import tabulate
from click import secho


class GetGistCommons(object):
    """Basic output methods used to print messages on users' terminal"""

    indent_size = 2
    indent_char = " "

    def indent(self, message):
        """
        Sets the indent for standardized output
        :param message: (str)
        :return: (str)
        """
        indent = self.indent_char * self.indent_size
        lines = (indent + line for line in message.split("\n"))
        return "\n".join(lines)

    def output(self, message, color=None):
        """
        A helper to be used like print() or click's secho() tunneling all the
        outputs to sys.stdout or sys.stderr
        :param message: (str)
        :param color: (str) check click.secho() documentation
        :return: (None) prints to sys.stdout or sys.stderr
        """
        output_to = stderr if color == "red" else stdout
        secho(self.indent(message), fg=color, file=output_to)

    def oops(self, message):
        """Helper to colorize error messages"""
        return self.output(message, color="red")

    def yeah(self, message):
        """Helper to colorize success messages"""
        return self.output(message, color="green")

    def warn(self, message):
        """Helper to colorize warning messages"""
        return self.output(message, color="yellow")

    def hey(self, message):
        """Helper to colorize highlighted messages"""
        return self.output(message, color="blue")

    def tabulate(self, *files):
        data = tuple((str(f), f.gist, f.url) for f in files)
        return self.output(tabulate(data, headers=("Gist", "File", "URL")))
