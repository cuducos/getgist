class GetGistCommons(object):

    indent_size = 2
    indent_char = ' '

    def output(self, message):
        indent = self.indent_char * self.indent_size
        print(indent + message)
