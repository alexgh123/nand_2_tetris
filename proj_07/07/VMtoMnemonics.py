#
#VMtoMnemonics.py
#
# CS2000   Project 7 Virtual Machine (part 1)
#
#  Hardt
#
# Summer 2013
# last updated 18 Oct 2017
#

import sys  #for grading server

from pathlib import *
from VMParser import *
from VMCodeGenerator import *


class VMtoMnemonics(object):

##########################################
#Constructor

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

        # check for dir
        for file in self.targetPath.iterdir():
            if (file.stem == ".vm"):
                assemblyCode = self.__processFile__(file)
                terminationList = VMCodeGenerator.generateTermination()
                assemblyCode += terminationList
            #else, not a .vm file

        return self.__output__(assemblyCode)


##########################################
#private methods


    def __processFile__(self, filePath):
        ''' processes a single file, returning the translated assembly code. '''
        assemblyCode = []
        parserObject = VMParser(filePath)
        line = parserObject.advance();
        codeGen = VMCodeGenerator(filePath)

        while line:
            translatedLine = codeGen.translateLine(line)
            assemblyCode += translatedLine
            line = parserObject.advance()

        return assemblyCode



    def __output__(self, codeList):
        ''' outputs the machine code codeList into a file and returns the filename'''

        file = open(str(self.outputFilePath),"w")
        file.write("\n".join(codeList))
        file.close()
        return str(self.outputFilePath)


#################################
#################################
#################################
#this kicks off the program and assigns the argument to a variable
#
if __name__=="__main__":

    target = sys.argv[1]     # use this one for final deliverable

##    target = 'multiFileTester'    #for testing ability to load multiple files in a directory
##                                  #do not try to translate this file
##    target = 'StackArithmetic/SimpleAdd'    # for internal IDLE testing only
##    target = 'StackArithmetic/StackTest'    # for internal IDLE testing only
##    target = 'MemoryAccess/BasicTest'    # for internal IDLE testing only
##    target = 'MemoryAccess/PointerTest'    # for internal IDLE testing only
##    target = 'MemoryAccess/StaticTest'    # for internal IDLE testing only

    translator = VMtoMnemonics(target)
    print('\n' + str( translator.process() ) + ' has  been translated.')

