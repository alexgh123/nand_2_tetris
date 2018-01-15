#
#Assembler.py
#
# CS2001   Project 6 Assembler
# 31 July 2013
# last updated 26 Aug 2016
#
# start code version
#


from Code import *
from SymbolTable import *
from Parser import *


'''Manages the assembly process,
   1. used (use?) the Parser to do the mechanical tokenizing and then

   2. determines the semantically correct thing to do with those tokens.

   3. Then uses the Parser to break tokens into appropriate components and requests the translations of those
   components from the Code module. Labels are passed to the SymbolTable to get mapped
   against addresses.'''
class Assembler(object):

##########################################
#Constructor

    def __init__(self, fileName):

        index = fileName.find('.asm')
        if ( index < 1):
            raise RuntimeError( "error, cannot use the filename: " + fileName )

        self.inputFileName = fileName
        self.outputFileName = self.inputFileName[:index] + '.hack'

        self.parser = Parser(self.inputFileName)

        self.code = Code()
        self.st = SymbolTable()


##########################################
#public methods

    def assemble(self):
        '''Does the assembly and creates the file of machine commands,
           returning the name of that file '''
        self.__firstPass__()
        return  self.__output__( self.__secondPass__() )


##########################################
#private/local methods

    def __output__(self, codeList):
        ''' outpute the machine code codeList into a file and returns the filename'''

        file = open(self.outputFileName,"w")
        file.write("\n".join(codeList))
        file.close()
        return self.outputFileName


    def __firstPass__(self):
        ''' Passes over the file contents to populate the symbol table'''

        dictOfLables = self.parser.processLabels()         #clearly name object

        for key in dictOfLables:                           # process labels
          if not self.st.contains(key):                    # if label isn't in symbol table
            self.st.addEntry(key, dictOfLables[key])       #     add it to symbol table


    def __secondPass__(self):
        ''' Manage the translation to machine code, returning a list of machine instructions'''

        machineCode = []

        command = self.parser.advance()                    # progress through each command in file
        while(command):                                    # while there is

                                                           # parse each command based on given logic
            if   (self.parser.commandType(command) == self.parser.A_COMMAND):
                bitString = self.__assembleA__(command)
            elif (self.parser.commandType(command) == self.parser.C_COMMAND):
                bitString = self.__assembleC__(command)
            else:
                symStr = self.parser.symbol(command)
                raise RuntimeError( 'There should be no labels on second pass, errant symbol is ' + symStr)

            machineCode.append(bitString)                  # add each computed bit string to list object
            command = self.parser.advance()                # increment/go to next command

        return machineCode                                 # return all of the bit strings


    def __assembleC__(self, command):
        ''' Do the mechanical work to translate a C_COMMAND, returns a string representation
            of a 16-bit binary word.'''

        jumpValue = self.code.jump(self.parser.jump(command))   #parse jump command, do jump lookup
        mRegister = self.code.dest(self.parser.dest(command))   #parse dest command, do dest lookup
        aluValue =  self.code.comp(self.parser.comp(command))   #parse comp command, do comp lookup

        return '111'+ aluValue + mRegister+ jumpValue           # put all parst of command together


    def __assembleA__(self, command):
        '''
         Do the mechanical work to translate an A_COMMAND, returns a string representation
            of a 16-bit binary word.
        '''

        command = self.parser.symbol(command)

        if self.st.contains(command):
            dictValue = self.st.getAddress(command)                      # if command is in symbol table
            return '0' + "{0:015b}".format(int(dictValue))               #    look up value, turn it to binary
        elif command.isdigit():                                          # if its a digit
            return '0' + "{0:015b}".format(int(command))                 #    convert to binary
        else:                                                            # otherwise, add the entry to symbol table
            self.st.addEntry(command, self.st.getNextVariableAddress())  #    with the next available memory address
            return '0' + "{0:015b}".format(self.st.getAddress(command))  #    format that newly generated address to binary



#################################
#################################
#################################
#this kicks off the program and assigns the argument to a variable
#
if __name__=="__main__":

    fileName = sys.argv[1]         # use this one for final deliverable

#    fileName = 'add/Add.asm'       # for internal IDLE testing only
#    fileName = 'max/MaxL.asm'      # for internal IDLE testing only
#    fileName = 'max/Max.asm'       # for internal IDLE testing only
#    fileName = 'rect/RectL.asm'    # for internal IDLE testing only
#    fileName = 'rect/Rect.asm'     # for internal IDLE testing only
#    fileName = 'pong/PongL.asm'    # for internal IDLE testing only
#    fileName = 'pong/Pong.asm'     # for internal IDLE testing only

    assembler = Assembler(fileName)
    print(assembler.__secondPass__())

    print('done parsing, assembled file is:', assembler.assemble() )
