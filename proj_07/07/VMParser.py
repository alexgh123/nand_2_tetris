#
#VMParser.py
#
# CS2002   Project 7 & 8 Virtual Machine (part 1 & 2)
#
#  Hardt
#
# Summer 2013
# last updated 18 Oct 2017
#

class VMParser(object):

    # No MAGIC Numbers!!!
    #  refer to these like this example:  VMParser.CMD
    CMD = 0
    ARG1 = 1
    ARG2 = 2

############################################
# Constructor

    def __init__(self, filePath):
        loadedList = self.__loadFile__(str(filePath)) #returns a list object, of unprocessed data

        self.toParse = self.__filterFile__(loadedList) #filters out all the bull crap


############################################
# static methods
#    these methods are owned by the Class not one instance
#    note they do not have self as the first argument and they have the @staticmethod tag

                      #this is a "decorator"
    @staticmethod     # its so you can call the method w/o instantiating the class
    def command(line):
        ''' returns the line's command as a string'''

        #do work here
        result = line.split()[VMParser.CMD]
        return result

    @staticmethod
    def arg1(line):
        ''' returns the line's first argument as a string'''
        #do work here
        words_seperated = line.split()
        if (len(words_seperated) <2):
            raise RuntimeError("This is not a valid command, too few arguments")
        else:
            result = line.split()[VMParser.ARG1]

        return result

    @staticmethod
    def arg2(line):
        ''' returns the line's second argument as a string '''
        #do work here
        words_seperated = line.split()
        if (len(words_seperated) <3):
            raise RuntimeError("This is not a valid command, too few arguments")
        else:
            result = line.split()[VMParser.ARG2]

        return result


############################################
# instance methods

    def advance(self):
        '''reads and returns the next command in the input,
           returns false if there are no more commands.  '''
        if self.toParse:
            return self.toParse.pop(0)
        else:
            return False


############################################
# private/utility methods (unchanged from project 6)

    def __toTestDotTxt__(self):
        '''this is just for outputting our stripped file as a test
           this function will not be active in the final program'''

        file = open("test.txt","w")
        file.write("\n".join(self.toParse))
        file.close()


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

        filteredList = []

        for line in fileList:
            line = line.strip()                       #leading and trailing whitespace removal
            line = self.__filterOutEOLComments__(line)

            if len(line) > 0:                          #empty line removal
                filteredList.append(line)

        return filteredList



    def __filterOutEOLComments__(self, line):
        '''Removes end-of-line comments and and resulting whitespace.

           -line is a string representing single line, line endings already stripped
           returns the filtered line, which may be empty '''

        index = line.find('//')
        if (index >= 0):
            line = line[0:index]

        line = line.strip()

        return line
