'''
helper file to run PythonLexer on a file given as a sys.argv
and print the string - token pairs to check syntax highlighting
'''

import sys
from pygments import lex
from pygments.lexers.python import PythonLexer



try:
    FILE_INPUT = sys.argv[1]
except IndexError:
    print('no file given, use \'python print_tokens.py file_name\'')

FILE_TEXT = open(FILE_INPUT, 'r').read()

for token, content in lex(FILE_TEXT, PythonLexer()):
    print(content + ' - ' + str(token))
