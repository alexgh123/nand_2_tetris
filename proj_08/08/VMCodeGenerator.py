#
#VMCodeGenerator.py
#
#
#
#
# CS2002   Project 8 Virtual Machine (part 2)
#
# Summer 2013
# last updated 05 Nov 2017
# by Alex Hardt

from VMParser import *

#constants only used in this file, so I located them outside the class boundary
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

class VMCodeGenerator(object):

############################################
#static class variables
#   these will be shared across multiple instances

    labelID = 0
    NO_INIT_FOR_TESTS = ['BasicLoop.vm', 'FibonacciSeries.vm', 'SimpleFunction.vm']

############################################
# Constructor
    def __init__(self, filePath):       #note the change in the function-argument signature!!!

        #fileName is used for static partition name creation
        self.fileName = filePath.name

        # self.currentFunction = filePath.stem
        self.currentFunction = None

        #we will cover what this dictionary means, othere than it eliminates
        #well over 100 lines of code just to do two-stage lookups
        self.tokenToCommandDict = {

                'add'     : self.__arithmetic__,
                'sub'     : self.__arithmetic__,
                'neg'     : self.__arithmetic__,
                'and'     : self.__arithmetic__,
                 'or'     : self.__arithmetic__,
                'not'     : self.__arithmetic__,

                 'eq'     : self.__conditional__,
                 'gt'     : self.__conditional__,
                 'lt'     : self.__conditional__,

               'push'     : self.__push__,
                'pop'     : self.__pop__,

                'label'   : self.__generateLabel__,
                'if-goto' : self.__generateIf__,
                'goto'    : self.__generateGoto__,
                'function': self.__generateFunction__,
                'call'    : self.__generateCall__,
                'return'  : self.__generateReturn__


                #add entries as required for this project

        }



############################################
# static class methods
#    these methods are owned by the Class not one instance
#    note they do not have self as the first argument and they have the @staticmethod tag


    @staticmethod
    def __getSimpleLabel__():
        ''' A static utility method useful for creating arbitrary unique labels when the required label
            was not provided by the VM code. '''

        #do work here
        result = VMCodeGenerator.labelID

        #increment labelID *after* setting result
        VMCodeGenerator.labelID += 1

        return result


############################################
# instance methods

    def translateLine(self, line):
        ''' this is how we prevent VMtoMnemonics from having to twiddle,
            we do the translation task here and return the result'''
        command = VMParser.command(line)
        return self.tokenToCommandDict[command](line)


    def generateInit(self):
        ''' Generation Hack assembler code for program initialization:
                SP = 256.
                pointers = true
                Call Sys.Init()
                place Termination loop'''
        lines = []


        if self.fileName not in VMCodeGenerator.NO_INIT_FOR_TESTS:

            #SP = 256
            lines += ["@256", "D=A", "@SP", "M=D"]
            # pointers = true
            lines += self.__setPointersTrue__()
            #call Sys.init() 0
            lines += self.__generateCall__("call Sys.init 0")

            #TODO: call sys.init correctly

            #TODO: also put replacement for P7's generateTermination() here
            #  above and beyond book requirement to keep PC from going off
            #  into nowhere good
            lines += ['(TERMINAL_LOOP)']
            lines += ['@TERMINAL_LOOP']
            lines += ['0;JMP']

            ##### end not invoked for first 3 examples


        return lines



############################################
# private/utility methods

    def __arithmetic__(self, line):

        #use yours from Project 7
        ''' Handle generation of Hack assembler code for the basic arithmetic commands
        -line will only contain the arithmetic operation
        returns a list of assembler instructions'''

        lines = []
        vmLLetters = str(line)
        unaray_operators = ["neg", "not"]

        if(vmLLetters in list(OPERAND_MAP.keys())):
        #if you don't use list(__.keys)...you will get key error... instead of kicking to the else RuntimeError
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

        labelCount = str(self.__getSimpleLabel__())
        vmLLetters = str(line).upper()
        lines = []
        lines += self.__popStacktoD__()
        lines += ["A=A-1", "D=M-D", "@IF_TRUE" + labelCount, "D;J"+ vmLLetters, "D=0", "@END" + labelCount, "0;JMP", "(IF_TRUE"+labelCount+")", "D=-1", "(END"+labelCount+")","@SP", "A=M-1", "M=D"]
        return lines


    def __push__(self, line):

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

        lines = ["@SP", "A=M", "M=D", "@SP", "M=M+1"]
        return lines


    def __popStacktoD__(self):

        lines = ["@SP", "AM=M-1", "D=M"]
        return lines


    ##############################################
    # New stuff for project 8
    #
    # \/  \/  \/  \/  \/  \/
    #


    def __mangleLabelText__(self, label):
        ''' Creates globally unique label text and returns it.

            -label is a string which requires mangling to ensure uniqueness
             per fig 8.6 standard '''

        if (self.currentFunction == None):
            outLabel = self.fileName + "." + label
        else:
            outLabel = self.fileName + "." + self.currentFunction + "$" + label

        return outLabel


    def __generateLabel__(self, line):
        ''' Translate a label command.

            -line is the whole command, arg1 of the line is the label we need
            to mangle to ensure uniqueness

             returns a list of assembler instructions that contains a proper and unique label command'''

        #TODO write function body
        mangledLabel = self.__mangleLabelText__(VMParser.arg1(line))

        lines = ["(" + mangledLabel + ")"]

        return lines



    def __generateGoto__(self, line):
        ''' Translate a goto command.

            -line is the whole command, arg1 of the line is the the label of the destination
              which requires proper mangling to match its assembly (label)

            returns a list of assembler instructions '''

        #TODO write function body
        mangledLabel = self.__mangleLabelText__(VMParser.arg1(line))

        lines = ["@" + mangledLabel, "0;JMP"]

        return lines


    def __generateIf__(self, line):
        ''' Translate an if-goto command.

            -line is the whole command, arg1 of the line is the the label of the destination
              which requires proper mangling to match its assembly (label)

            returns a list of assembler instructions '''

        #TODO write function body
        mangledLabel = self.__mangleLabelText__(VMParser.arg1(line))

        lines = []
        lines += self.__popStacktoD__()
        lines += ["@"+ mangledLabel, "D;JNE"]

        return lines



    def __generateCall__(self, line):
        ''' Translate a call command.

            -line is the whole command, arg1 of the line is the name of the called function
             arg2 of the line is the number of arguments to the called function

            returns a list of assembler instructions '''

        #TODO write function body
        lines = []

        uniqueLabel = str(self.__getSimpleLabel__())

        lines += ["@RETURN_ADDRESS" + uniqueLabel, "D=A"]
        lines += self.__pushDtoStack__()

        lines += self.__callLocals__()

        # @ARG = SP - N - 5
        arg2 = VMParser.arg2(line)
        lines += ["@SP", "D=M", "@" + arg2, "D=D-A", "@5", "D=D-A", "@ARG", "M=D"]

        #LCL = SP
        lines += ["@SP", "D=M", "@LCL", "M=D"]

        #goto f
        functionName = VMParser.arg1(line)
        lines += ["@" + functionName, "0;JMP"]

        #return address
        lines += ["(RETURN_ADDRESS" + uniqueLabel + ")"]


        return lines



    def __generateFunction__(self, line):
        ''' Translate a function command.

           -line is the whole command, arg1 of the line is the name of the defined function
             arg2 of the line is the number of local variables in the defined function

            returns a list of assembler instructions '''

        self.currentFunction = VMParser.arg1(line)

        lines = []

        functionName = VMParser.arg1(line)
        lines += ["(" + functionName + ")", ]

        numberOfConstants = int(VMParser.arg2(line))
        lines += (self.__push__("push constant 0") * numberOfConstants)

        return lines



    def __generateReturn__(self, unused):
        ''' Translate a return command.

            -unused is exactly what it says, it is required only for consistency in dynamic function
             calling.

            returns a list of assembler instructions '''

        lines = ["@LCL","D=M","@R15","M=D","@5","A=D-A", "D=M","@R14","M=D"]
        lines += self.__popStacktoD__()
        lines += ["@ARG", "A=M", "M=D"]
        #resets stack pointer
        lines += ["@ARG","D=M+1","@SP","M=D"]
        lines += self.__returnLocals__()
        #return address
        lines += ["@R14", "A=M", "0;JMP"]
        return lines




    #TODO helper function(s) as required
    #
    # Don't
    # Repeat
    # Yourself
    #
    #there is at least one required

    def __returnLocals__(self):
        returnLclsList = []
        rLcls = ["@THAT","@THIS","@ARG","@LCL"]
        for lcl in rLcls:
            returnLclsList += ["@R15", "AM=M-1", "D=M", lcl, "M=D"]
        return returnLclsList

    def __callLocals__(self):
        callLclsList = []
        cLcls = ["@LCL","@ARG","@THIS","@THAT"]
        for lcl in cLcls:
            callLclsList += [lcl, "D=M"]
            callLclsList += self.__pushDtoStack__()
        return callLclsList

    def __setPointersTrue__(self):

        truePointers = ["@LCL", "M=-1",
                        "@ARG", "M=-1",
                        "@THIS", "M=-1",
                        "@THAT", "M=-1"]

        return truePointers