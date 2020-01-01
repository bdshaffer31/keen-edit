import sys
from pygments import lex
from pygments import highlight
from pygments.lexers.python import PythonLexer

'''
helper file to run PythonLexer on a file given as a sys.argv 
and print the string - token pairs to check syntax highlighting
'''

try:
    file_input = sys.argv[1]
except IndexError:
    print('no file given, use \'python print_tokens.py file_name\'')

file_text = open(file_input, 'r').read()

for token, content in lex(file_text, PythonLexer()):
    print(content + ' - ' + str(token))