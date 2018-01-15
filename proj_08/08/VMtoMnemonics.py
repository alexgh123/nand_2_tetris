#
#VMtoMnemonics.py
#
# (student completing)
#
# CS2002   Project 8 Virtual Machine (part 2)
#
# Summer 2013
# last updated 05 Nov 2017
# by Alex Hardt

import sys  #for grading server
from pathlib import *

from VMParser import *
from VMCodeGenerator import *


class VMtoMnemonics(object):

##########################################
#Static file tracker
    fileCount = 0

##########################################
#Constructor

    #there are no changes to the constructor
    def __init__(self, targetPath):

        self.targetPath = Path(targetPath)

        if self.targetPath.is_dir():
            self.outputFilePath = self.targetPath / (self.targetPath.name + '.asm')

        else:
            if self.targetPath.suffix == '.vm':
                self.outputFilePath = Path(self.targetPath.parent / (self.targetPath.stem + '.asm'))

            else:
                raise RuntimeError( "error, cannot use the filename: " + targetPath )



##########################################
#public methods


    def process(self):
        ''' processes a directory or a single file, returning the translated  assembly code. '''

        assemblyCode = []

        for file in self.targetPath.iterdir():
            if (file.suffix == ".vm"):
                assemblyCode += self.__processFile__(file)
                VMtoMnemonics.fileCount += 1
            #else, not a .vm file

        return self.__output__(assemblyCode)


##########################################
#private methods


    def __processFile__(self, filePath):
        ''' processes a single file, returning the translated assembler. '''

        assemblyCode = []
        parserObject = VMParser(filePath)
        line = parserObject.advance();
        codeGen = VMCodeGenerator(filePath)

        # Add generate init to first file
        #   I'm **not** creating a second VmCodeGenerator object,
        #   I'm using the one that is given
        if (VMtoMnemonics.fileCount == 0):
            assemblyCode += codeGen.generateInit()

        while line:

            #Alex: debug comment:========================
            comment = ["//"+line]
            assemblyCode += comment
            #:============================================

            translatedLine = codeGen.translateLine(line)
            assemblyCode += translatedLine
            line = parserObject.advance()

        return assemblyCode


    def __output__(self, codeList):
        ''' outpute the machine code codeList into a file and returns the filename'''

        file = open(str(self.outputFilePath),"w")
        file.write("\n".join(codeList))
        file.close()
        return str(self.outputFilePath)



# un changed version to turn in


#################################
#################################
#################################
#this kicks off the program and assigns the argument to a variable
#
if __name__=="__main__":

    target = sys.argv[1]     # use this one for final deliverable


##    target = 'ProgramFlow/BasicLoop'          # test 1  for internal IDLE testing only
##    target = 'ProgramFlow/FibonacciSeries'    # test 2  for internal IDLE testing only
##    target = 'FunctionCalls/SimpleFunction'   # test 3  for internal IDLE testing only
##    target = 'FunctionCalls/NestedCall'       # test 4  for internal IDLE testing only
##    target = 'FunctionCalls/FibonacciElement' # test 5  for internal IDLE testing only
##    target = 'FunctionCalls/StaticsTest'      # test 6  for internal IDLE testing only

    translator = VMtoMnemonics(target)
    print('\n' + str( translator.process() ) + ' has  been translated.')

'''

# ALEX: delete below before submission:

# target = 'ProgramFlow/BasicLoop'          # test 1  for internal IDLE testing only
#target = 'ProgramFlow/FibonacciSeries'    # test 2  for internal IDLE testing only
# target = 'FunctionCalls/SimpleFunction'   # test 3  for internal IDLE testing only
#target = 'FunctionCalls/NestedCall'       # test 4  for internal IDLE testing only
target = 'FunctionCalls/FibonacciElement' # test 5  for internal IDLE testing only
#target = 'FunctionCalls/StaticsTest'      # test 6  for internal IDLE testing only

translator = VMtoMnemonics(target)
translator.process()

# thing = VMCodeGenerator(Path(target))
# print(thing.generateInit())
'''