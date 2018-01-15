#
#JTConstants.py
#
# CS2002   Project 10 Jack Compiler (part 1)
#
# Summer 2013
# last updated 02 Sept Aug 2016
#

import string

##############################################################
#Chapter 10 stuff
#
KEYWORDS = ('boolean', 'char', 'class', 'constructor', 'do', 'else',
            'false', 'field', 'function', 'if', 'int', 'let', 'method',
            'null', 'return', 'static', 'this', 'true', 'var', 'void', 'while')

SYMBOLS = '{}()[].,;+-*/&|<>=~'

DELIMITERS = ' ' + SYMBOLS

IDENTIFIER_START_CHARS = string.ascii_letters + '_'
IDENTIFIER_CHARS = IDENTIFIER_START_CHARS + string.digits

glyphSubstitutes = {'<':'&lt;', '>':'&gt;' , '&':'&amp;'}


##############################################################
#Chapter 11 stuff
#


SUBROUTINES = ('constructor', 'method', 'function')

STATEMENTS = ('let', 'if', 'while', 'do', 'return')


KEYWORD_CONSTANTS = {'true':-1, 'false':0, 'null':0, 'this':999999999}

UNARY_OPERATORS = {'-':'neg', '~':'not'}

#this (below) duplicates dict ^above, but i don't want a key error when i look up to it
UNARY_OPS = ['-', '~']

BINARY_OPERATORS = {    '+':'add',
                        '-':'sub',
                        '*':'Math.multiply',
                        '/':'Math.divide',
                    '&amp;':'and',
                        '|':'or',
                     '&lt;':'lt',
                     '&gt;':'gt',
                        '=':'eq'}

#this (below) duplicates dict ^above, but i don't want a key error when i look up to it
OPERATORS = ['+','-','*','/','&amp;', '|', '&lt;', '&gt;', '=']


TOKEN_STRINGS = ( 'unknown', 'keyword', 'symbol', 'identifier',
                  'integerConstant', 'stringConstant',
                  'IDENTIFIER-Defined', 'SCOPE-Subroutine')

TOKEN_UNKNOWN = 0
TOKEN_KEYWORD = 1
TOKEN_SYMBOL = 2
TOKEN_IDENTIFIER = 3
TOKEN_INT_CONST = 4
TOKEN_STRING_CONST = 5
IDENTIFIER_DEFINED = 6
SCOPE_SUBROUTINE = 7
