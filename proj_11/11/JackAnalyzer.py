#
#JackAnalyzer.py
#
# CS2002   Project 10 & 11 Jack Compiler
#
# Summer 2013
# last updated 25 Oct 2016
#

import sys  #for grading server
from pathlib import *

from JackTokenizer import *
from CompilationEngine import *
from JTConstants import *
# from SymbolTable import *

thingy = []

class JackAnalyzer(object):

##########################################
#Constructor

    def __init__(self, target):
        self.targetPath = Path(target)


##########################################
#public methods

    def process(self):
        ''' iterates over a directory causing each .jack file to be processed.
            returns the pathname of the directory upon successful completion. '''

        if self.targetPath.is_dir():
            for eachFile in self.targetPath.iterdir():

                if eachFile.suffix == '.jack':
                    self.__processFile__(eachFile)

        else:
            raise RuntimeError("Error, " + target.name + " is not a directory ")

        return str(self.targetPath)


##########################################
#private methods

    def __processFile__(self, filePath):
        ''' processes a single file, first feeding the file to JackTokenizer to generate a list of tokens
            (output as T.xml files for debugging use) and that token list is fed through
            CompilationEngine to generate a final result list of XML tokens which is output into an .xml file. '''

        #TODO  make it work

        # create opening token tag for tokenizing lines of .jack
        tokens = ["<tokens>"]
        tokenizer = JackTokenizer(filePath)

        line =  tokenizer.advance()

        # tokenize each line of .jack
        while line:
            tokens += [self.__wrapTokenInXML__(line)]
            line = tokenizer.advance()

        tokens += ["</tokens>"]

        # print(tokens)
        # write out the raw tokens
        xml_T_FilePath = Path(filePath.parent / (filePath.stem + 'T.xml'))
        self.__output__(xml_T_FilePath, tokens)

        # 2. create a list for compiled tokens to go into, create compEngine instance
        #     compile the tokens
        compiledTokens = []
        compEngine = CompilationEngine(tokens)
        compiledTokens += compEngine.compileTokens()

        # create the filepath names for writing the tokens and full blown xml
        finalTokenPath = Path(filePath.parent / (filePath.stem + '.xml'))

        self.__output__(finalTokenPath, compiledTokens)

        # ===============================
        # ======== project 11 stuff =====
        # ===============================
        vmPath = Path(filePath.parent / (filePath.stem + '.vm'))
        vmCommands = compEngine.get_vmInstructions()
        self.__output__(vmPath, vmCommands)



    def __output__(self, filePath, codeList):
        ''' outputs the VM code codeList into a file and returns the file path'''

        file = open(str(filePath), 'w')
        file.write("\n".join(codeList))
        file.close()



    def __wrapTokenInXML__(self, token):
        ''' returns an XML tag pair with the token properly sandwiched.
             conducts proper substitutions and quotation mark removals. '''

        flavor = 'unknown'

        if(token in SYMBOLS):
            if any(ch in token for ch in glyphSubstitutes):
                    token = glyphSubstitutes[token]
            flavor = "symbol"
        elif(token in KEYWORDS):
            flavor = "keyword"
        elif(token.isdigit()):
            flavor = "integerConstant"
        elif(token[0]== '"'):
            token = token[1:-1]
            flavor = "stringConstant"
        else:
            flavor = "identifier"

        return '<' + flavor + '> ' + token + ' </' + flavor + '>'




#################################
#################################
#################################
#this kicks off the program and assigns the argument to a variable
#
if __name__=="__main__":

    target = sys.argv[1]     # use this one for final deliverable

    #project 10 tests
##    target = 'ExpressionlessSquare'
##    target = 'ArrayTest'
##    target = 'Square'


    #project 11 tests
##    target = 'Seven'
##    target = 'ConvertToBin'
##    target = 'square'
##    target = 'Average'
##    target = 'Pong'
##    target = 'ComplexArrays'

    analyzer = JackAnalyzer(target)
    print('\n' + analyzer.process() + ' has been translated.')

