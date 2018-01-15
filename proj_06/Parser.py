#
#Parser.py
#
# CS2001   Project 6 Assembler
# 31 July 2013
# last updated 26 Aug 2016
#
# start code version
#



'''Manages the mechanical work of breaking the input into tokens, and later further breaking
   down presented tokens into component chunks.  The Parser does not know what the chunks mean
   or what to do with them, it just knows how to slice-and-dice. '''

class Parser(object):

    A_COMMAND = 1
    C_COMMAND = 2
    L_COMMAND = 3

##########################################
#Constructor

    def __init__(self, fileName):
        loadedList = self.__loadFile__(fileName)

        self.toParse = self.__filterFile__(loadedList)
        self.__toTestDotTxt__()
        self.lineNumber = 0


##########################################
#public Methods


    def advance(self):
        '''reads and returns the next command in the input,
           returns false if there are no more commands.  '''

        if self.lineNumber < len(self.toParse):            # while there are items in list, return items
            noParen = self.toParse[self.lineNumber]
            self.lineNumber += 1
            return noParen
        else:
            return False                                   # if there are no more items in list, return False


    def commandType(self, command):
        ''' returns type of the command
            A_COMMAND   @xxx
         or C_COMMAND   c-commands
         or L_COMMAND   a label e.g. (LABEL)
        '''
        result = 0                                         # initialized to a tattle-tail value

        if ("@" in command):                               # this method returns what type of command is being parse
            result = self.A_COMMAND
        elif ("=" in command) or (";" in command):
            result = self.C_COMMAND
        elif("(" in command):
            result = self.L_COMMAND
        else:
            result

        return result


    def symbol(self, command):
        ''' returns
             symbol or decimal of an A-command
          or symbol of a label'''

        if (self.commandType(command) == self.A_COMMAND):   # return the first half of an A command
            return command[1:]
        elif (self.commandType(command) == self.L_COMMAND): # return the label without "(...)" characters
            return command[1:-1]
        else:
            raise RuntimeError("Error!!! parse.symbol(): We should never parse a symbol from a C_COMMAND")
            result = None

        return result


    def dest(self, command):
        ''' returns the dest mnemonic portion of the command '''

        if (";" in command):                               # if a command contains a ";" or "("
            return "null"                                  #       destination will be null (000)
        elif("(" in command):
            return "null"
        else:
            return command.split("=")[0]                   # otherwise return the first part of the command


    def comp(self, command):
        ''' returns the comp mnemonic portion of the command '''

        if ("=" in command):
            return command.split("=")[1]                   # if the command has a "=", the comp portion is the 2nd half
        else:
            return command.split(";")[0]                   # if the command has a ";", the comp portion is the 1st half



    def jump(self, command):
        ''' returns the jmp mnemonic portion of the command '''

        if ("=" in command):
            return "null"                                  # if the command has a "=", the dest portion is null
        else:
            return command.split(";")[1]                   # if the command has a ";", the dest portion is 2nd part



    def processLabels(self):
        ''' Passes over the list of commands and removes labels from the code being parsed.
            as labels are identified they are added to a dictionary of <label, romAddress>
            pairs.  After passing over the entire file the dictionary is returned. '''


        labels = {}
        lineCount = 0
        while lineCount < len(self.toParse):               # while there are items in list
            if self.toParse[lineCount].startswith("("):    # if its a L command
                noParen = self.toParse[lineCount][1:-1]    # strip it
                labels[noParen] = lineCount                # populate labels dict w/ new label
                self.toParse.pop(lineCount)                # remove symbol from list object
            lineCount += 1                                 # increment counter
        return labels



##########################################
#private/local Methods



    def __toTestDotTxt__(self):
        '''this is just for outputting our stripped file as a test
           this function will not be active in the final program'''

        file = open("test.txt","w")
        file.write("\n".join(self.toParse))
        file.close()



    def __loadFile__(self, fileName):
        '''Loads the file into memory.
           -fileName is a String representation of a file name,
           returns contents as a simple List.'''

        with open(fileName) as f:
            fileList = f.read().splitlines()
        return fileList


    def __filterFile__(self, fileList):
        '''Comments,
           blank lines and
           unnecessary leading/trailing whitespace are removed from the list.
           Removes end-of-line comments and and resulting whitespace.

           -fileList is a List representation of a file, one line per element
           returns the fully filtered List'''

        filteredList = []

        for line in fileList:
            noWhiteSpace = line.strip()
            commentSymbol = '//'
            noComments = noWhiteSpace.split(commentSymbol, 1)[0]
            filteredList.append(noComments)
            filteredList = [x for x in filteredList if x] #remove empty elements in list

        return filteredList




