#
#JackTokenizer.py
#
# CS2002   Project 10 Jack Compiler (part 1)
#
# Summer 2013
# last updated 25 Oct 2016
#


from JTConstants import *


############################################
# Class
class JackTokenizer(object):

############################################
#static class variables
    BLOCK_COMMENT_INDICATOR = False
    #ALEX: can you make ^ an instance variable????

############################################
# Constructor

    def __init__(self, filePath):
        loadedList = self.__loadFile__(str(filePath))

        cleanLines = self.__filterFile__(loadedList)

        #1. split up strings
        stringsSeperated = self.__seperateStrings__(cleanLines)
        #2. split by symbol
        symbolsSeperated = self.__seperateSymbols__(stringsSeperated)
        #3. split by space
        self.whiteSpaceRemoved = self.__filterWhitespace__(symbolsSeperated)



# ############################################
# instance methods

    def advance(self):
        '''reads and returns the next token, returns None if there are no more tokens.'''


        if self.whiteSpaceRemoved:
            return self.whiteSpaceRemoved.pop(0)
        else:
            return False



#############################################
# private


    def __parseInt__(self, line):
        ''' returns an integerConstant off of the start of the line.
            assumes there are no leading spaces
            does not modify the line itself. '''

        #TODO make it work

        '''
        his method from lecture:

        index = 0
        whileline[index].isDigit():
            index += 1

        return line[:index]

        then helper method

        def __parseIntBreak__(self, line):
            result = ''
            for char in line:
                if char.isDigit():
                    result += char
                else:
                    break

            return result

        '''


    def __parseCharacters__(self, line):
        ''' returns a token off of the start of the line which could be an identifier or a keyword.
            assumes there are no leading spaces
            does not modify the line itself. '''

        #TODO make it work



    def __parseString__(self, line):
        ''' returns a stringConstant off of the start of the line, quotes left in place.
            assumes there are no leading spaces and that the leading double quote has not been stripped.
            does not modify the line itself. '''

        #TODO make it work





################   file loading stuff below   ############

    def __loadFile__(self, fileName):
        '''Loads the file into memory.

           -fileName is a String representation of a file name,
           returns contents as a simple List'''

        fileList = []
        file = open(fileName,"r")

        for line in file:
            fileList.append(line)

        file.close()

        return fileList



    def __filterFile__(self, fileList):
        '''Comments, blank lines and unnecessary leading/trailing whitespace are removed from the list.

           -fileList is a List representation of a file, one line per element
           returns the fully filtered List'''

        #start with your project 8 __filterFile__
        #handle single line block commentsmuch like you did EOL comments
        #multi-line block coments are the only things on their lines, **different than single line block comments**

        #TODO make it work
        listOfLines = []
        for line in fileList:

            kinda_clean_line =  self.__filterOutEOLComments__(line)
            cleaner_line = self.__filterOutComments__(kinda_clean_line)
            listOfLines += [cleaner_line]

        # filter out empty strings
        listOfLines = list(filter(None, listOfLines))

        return listOfLines



    def __filterOutEOLComments__(self, line):
        '''Removes end-of-line comments and and resulting whitespace.

           -line is a string representing single line, line endings already stripped
           returns the filtered line, which may be empty '''

        index = line.find('//')
        if index >= 0:
            line = line[0:index]

        line = line.strip()

        return line



    def __filterOutComments__(self, line):
        '''Removes single line block comments and resulting whitespace.
           There may valid code following a single line block comment so entire lines are not deleted.

           -line is a string representing single line, line endings already stripped
           returns the filtered line, which may be empty. '''

        # find indexes of begining and end comment
        beginIndex = line.find("/*")
        endIndex = line.find("*/")

        #check for potential begining of block comment, if triggered, set indicator, return begining of string
        if ((beginIndex != -1) & (endIndex == -1)):
            JackTokenizer.BLOCK_COMMENT_INDICATOR = True
            outString = line[0:beginIndex]

        #check if we are inside of block comment, and not at the end of it
        elif((JackTokenizer.BLOCK_COMMENT_INDICATOR == True) & (endIndex == -1)):
            outString = ""

        #check if we are inside of block comment, but at the end of it, return rest of line after block comment, revert indicator
        elif((JackTokenizer.BLOCK_COMMENT_INDICATOR == True) & (endIndex != -1)):
            outString = line[endIndex+2:]
            JackTokenizer.BLOCK_COMMENT_INDICATOR = False

        #otherwise we are not in block comment and we do the regular line parsing:
        else:
            #there is no block comment, and no comment, just return the line
            if ((beginIndex == -1) & (endIndex == -1)):
                outString = line

            #parse a single line block comment
            else:
                outString = line[0:beginIndex] + line[endIndex+2:]

        return outString


    def __findCharOccurances__(self, string, char):
        #return a list of indexes where every 'char' occurs
        return [i for i, ltr in enumerate(string) if ltr == char]


    def __seperateStrings__(self, cleanLines):

        ''' Finds one or many strings in a line. works by finding the first string and making that a seperate element until there are no more strings in the line
        '''

        seperateStrings = []

        for line in cleanLines:
            if '"' in line:
                #find every occurance of '"' in a line
                indexes = self.__findCharOccurances__(line, '"')

                # if len(indexes > 2), that means more than 1 string is present in line
                while (len(indexes)>2):
                    firstIndex = indexes.pop(0)
                    secondIndex = indexes.pop(0)

                    #add the begining of the string up to the first '"' and the string
                    seperateStrings += [line[0:firstIndex], line[firstIndex:secondIndex+1]]

                    #update indexes + line
                    line = line[secondIndex+1:]
                    indexes = self.__findCharOccurances__(line, '"')

                #exit while loop, now we have last two indexes where '"' occurs
                firstIndex = indexes.pop(0)
                secondIndex = indexes.pop(0)

                #use last two indexes to chop up remainder of line at '"' delimiters
                seperateStrings += [line[0:firstIndex], line[firstIndex:secondIndex+1], line[secondIndex+1:]]

            else:
                #no '"' in string, just return the line
                seperateStrings += [line]

        #return either the seperate strings, or a single line
        return seperateStrings



    def __findSymbolOccurances__(self, string):
        #return a list of indexes for every place a symbol occurs
        return [i for i, ltr in enumerate(string) if ltr in SYMBOLS]


    def __seperateSymbols__(self, listOfStrings):

        symbolsSeperated = []

        for line in listOfStrings:

            #find index of every symbol on line
            occurances = self.__findSymbolOccurances__(line)

            ## if line contains a symbol:
            if(occurances):
                ##for every occurance, split string
                while(occurances):
                    index = occurances.pop(0)
                    symbolsSeperated += [line[0:index], line[index:index+1]]
                    line = line[index+1:]
                    #find remaining symbols on the line
                    occurances = self.__findSymbolOccurances__(line)
            ##else line does not contain a symbol
            else:
                symbolsSeperated += [line]

        # filter out empty strings
        symbolsSeperated = list(filter(None, symbolsSeperated))

        return symbolsSeperated



    def __filterWhitespace__(self, listOfStrings):
        cleanedList = []

        for line in listOfStrings:
            if '"' in line:
                cleanedList += [line]
            else:
                cleanedList += line.split(" ")

        cleanedList = list(filter(None, cleanedList))

        return cleanedList