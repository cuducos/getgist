class GetGistCommons(object):

    indent_size = 2
    indent_char = ' '

    def indent(self, message, indent_size=False):
        """A helper to indent output/input messages"""
        if not indent_size:
            indent_size = self.indent_size
        indent = self.indent_char * indent_size
        return indent + message

    def output(self, message, indent_size=False):
        """A helper to indent print()"""
        print(self.indent(message, indent_size))

    def ask(self, message, indent_size):
        """A helper to indent input()"""
        return input(self.indent(message, indent_size))
