#
#VMCodeGenerator.py
#
# CS2002   Project 7 Virtual Machine (part 1)
#
#  Hardt
#
# Summer 2013
# last updated 18 Oct 2017
#

from VMParser import *

#constants only used in this file
T_STATIC = 'static'
T_CONSTANT = 'constant'
T_POINTER = 'pointer'
T_TEMP = 'temp'

SEGMENT_MAP = {  'argument' : 'ARG',
                    'local' : 'LCL',
                     'this' : 'THIS',
                     'that' : 'THAT',
                  T_POINTER : 3,
                     T_TEMP : 5  }

OPERAND_MAP = { 'add' : 'M+D',
                'sub' : 'M-D',
                'neg' : '-M',
                'and' : 'D&M',    #for example: A=1...
                 'or' : 'D|M',
                'not' : '!M'   }

class VMCodeGenerator(object): #variable belongs to class, not thing in class

############################################
#static class variables
#   these will be shared across multiple instances

    labelID = 0  # "use this to create unique labels across program"
                 #ClassName.lableId <- doesn't refer to the isntance of the object
############################################
# Constructor
    def __init__(self, filePath):                  #self.... refers to the instance of the object

        self.fileName = filePath.stem

        self.tokenToCommandDict = {

                'add' : self.__arithmetic__,
                'sub' : self.__arithmetic__,
                'neg' : self.__arithmetic__,
                'and' : self.__arithmetic__,
                 'or' : self.__arithmetic__,
                'not' : self.__arithmetic__,

                 'eq' : self.__conditional__,
                 'gt' : self.__conditional__,
                 'lt' : self.__conditional__,

               'push' : self.__push__,
                'pop' : self.__pop__,
        }

############################################
# static class methods
#    these methods are owned by the Class not one instance
#    note they do not have self as the first argument and they have the @staticmethod tag

    @staticmethod
    def generateTermination():
        ''' I am paranoid about running off the edge of the earth and into arbirtary malicious code.
            put a jump to the termination loop at the very bottom of the program
            to prevent any possibility of leaking off the bottom (the edge)'''
        lines = []

        lines.append('(TERMINAL_LOOP)')
        lines.append('@TERMINAL_LOOP')
        lines.append('0;JMP')

        return lines



    @staticmethod
    def __getSimpleLabel__():
        ''' a static utility method to access the class variable '''

        #do work here
        #uniqueifier
        result = VMCodeGenerator.labelID

        #increment labelID *after* setting result
        VMCodeGenerator.labelID += 1

        return result



############################################
# instance methods

    def translateLine(self, line):
        ''' this is how we prevent VMtoMnemonics from having to twiddle,
            we do the translation task here and return the result'''

        result = self.tokenToCommandDict[VMParser.command(line)](line)
        return result




############################################
# private/utility methods


    def __arithmetic__(self, line):
        ''' Handle generation of Hack assembler code for the basic arithmetic commands
            -line will only contain the arithmetic operation
            returns a list of assembler instructions'''

        lines = []
        vmLLetters = str(line)
        valid_commands = ["add", "sub", "neg", "or", "not", "and"]
        unaray_operators = ["neg", "not"]

        #do work here
        if(vmLLetters in valid_commands):
            if (vmLLetters in unaray_operators):
                lines += ["@SP","A=M-1", "M=" + OPERAND_MAP[vmLLetters]]
            else:
                lines += self.__popStacktoD__()
                lines += ["@SP","A=M-1","M=" + OPERAND_MAP[vmLLetters]]
        else:
            raise RuntimeError('Error! called VMCodeGenerator.arithmetic() with this bad command: '+line)
            lines = None
        return lines




    def __conditional__(self, line):
        ''' Translate basic conditional (lt, gt, eq) commands.
            -command is the boolean comparison operator, Hack VM lang provides it in lowercase,
            returns a list of assembler instructions'''
        labelCount = str(self.__getSimpleLabel__())
        vmLLetters = str(line).upper()
        lines = []
        lines += self.__popStacktoD__()
        lines += ["A=A-1", "D=M-D", "@IF_TRUE" + labelCount, "D;J"+ vmLLetters, "D=0", "@END" + labelCount, "0;JMP", "(IF_TRUE"+labelCount+")", "D=-1", "(END"+labelCount+")","@SP", "A=M-1", "M=D"]
        return lines




    def __push__(self, line):
        ''' Translate a push command.
            -line is the whole command, arg1 of the line is the segment, arg 2 is the index,
            returns a list of assembler instructions'''
        lines = []
        #do work here
        command = VMParser.command(line)
        arg1 = VMParser.arg1(line)
        arg2 = VMParser.arg2(line)

        if(arg1 == T_CONSTANT):
            lines += ["@"+arg2, "D=A"]
            lines += self.__pushDtoStack__()
        #working on: static
        elif(arg1 == T_STATIC):
            # @self.fileName.index
            lines += ["@" + self.fileName + "." + arg2, "D=M"]
            lines += self.__pushDtoStack__()
        # pointer/temp
        elif((arg1 == T_POINTER) or (arg1 == T_TEMP)):
            lines += ["@" + str(SEGMENT_MAP[arg1] + int(arg2)), "D=M"]
            lines += self.__pushDtoStack__()
        #arg,local, this, that
        elif((arg1 == "argument") or (arg1 == "local") or(arg1 == "this") or (arg1 == "that")):
            lines += ["@"+arg2, "D=A","@" + SEGMENT_MAP[arg1], "D=M+D", "A=D", "D=M"]
            lines += self.__pushDtoStack__()
        else:
            raise RuntimeError('Error! Illegal segment for pushing:', segment)
        return lines


    def __pop__(self, line):
        ''' Translate a pop command.
            -line is the whole command, arg1 of the line is the segment, arg 2 is the index,
            returns a list of assembler instructions'''

        lines = []
        command = VMParser.command(line)
        arg1    = VMParser.arg1(line)
        arg2    = VMParser.arg2(line)

        # static
        if(arg1 == T_STATIC):
            lines += self.__popStacktoD__()
            lines += ["@" + self.fileName + "." + arg2, "M=D"]
        #pointer/temp
        elif((arg1 == T_POINTER) or (arg1 == T_TEMP)):
            lines += self.__popStacktoD__()
            lines += ["@" + str(SEGMENT_MAP[arg1] + int(arg2)), "M=D"]
        #'altt..'
        elif((arg1 == "argument") or (arg1 == "local") or (arg1 == "this") or (arg1 == "that")):
            lines += ["@" + SEGMENT_MAP[arg1], "D=M","@"+arg2, "D=D+A","@R15", "M=D"]
            lines += self.__popStacktoD__()
            lines += ["@R15", "A=M", "M=D"]
        else:
            raise RuntimeError('Error! Illegal segment for popping')
        return lines


    def __pushDtoStack__(self):
        #do work here
        lines = ["@SP", "A=M", "M=D", "@SP", "M=M+1"]
        return lines


    def __popStacktoD__(self):
        #do work here
        lines = ["@SP", "AM=M-1", "D=M"]
        return lines






