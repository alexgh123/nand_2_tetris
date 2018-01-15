#
#CompilationEngine.py
#
# CS2002   Project 10 Jack Compiler (part 1)
#
# Summer 2013
# last updated 25 Oct 2016
#

from JTConstants import *
from SymbolTable import *
from VMWriter import *

TT_TOKEN = 0
TT_XML = 1

# symbolTable = SymbolTable()

class CompilationEngine(object):
#static class variables
    labelNumber = 0


############################################
# Constructor
    def __init__(self, tokenList):
        self.tokens = tokenList   #the list of tagged tokens to process (a copy was previously output as ____T.xml )

        #add and delete from this to reack left padding for XML file readability
        self.indentation = 0

        self.vmInstList = []

        self.symbolTable = SymbolTable()

        self.vmWriter = VMWriter()

        self.className = ""

        self.subRoutineName = ""

        self.argCounter = 0

        self.args = 0

        self.voidMethod = False

        self.ListOfOps = []


############################################
# instance methods

    def getLabel(self):
        num = CompilationEngine.labelNumber
        CompilationEngine.labelNumber += 1
        return(num)

    def debugSatement(self, methodName):
        indent = "-" * self.indentation
        string = "----------------------" + indent + methodName
        # self.vmInstList.extend([string])

    def compileTokens(self):
        ''' primary call to do the final compilation.
            returns a list of properly identified structured XML with appropriate indentation.'''

        #the compilation recursive descent always starts with the <tokens> tag, and then calls __compileClass__(),
        #  if it does not -- fail early because something is wrong, either in the tokenizing or how the file was output.
        #  **use the fail early technique throughout the compilation, you will always know which of a small number of
        #  possibilities you are looking for, if none of them are there raise the exception so you can start debugging

        result = []

        tokenTuple = self.__getNextEntry__()

        if tokenTuple[TT_XML] == '<tokens>':
            result.extend( self.__compileClass__() )
            tokenTuple = self.__getNextEntry__()

            if tokenTuple[TT_XML] != '</tokens>':
                raise RuntimeError('Error, this file was not properly tokenized, missing </tokens>')
        else:
            raise RuntimeError('Error, this file was not properly tokenized, missing <tokens>')

        return result

############################################
# project 11 method


    def get_vmInstructions(self):
        ''' returns a fully translated list of vm instructions, one instruction per list element '''
        # self.vmInstList = []
        return self.vmInstList



############################################
# private/utility methods


    def __getNextEntry__(self):
        ''' removes and returns the next token from the list of tokens as a tuple of the form
            (token, <tag> token </tag>).
            TT_TOKEN and TT_XML should be used for accessing the tuple components '''

        #TODO   make it work.

        if self.tokens:
            #create token literal
            tokenXML = self.tokens.pop(0)
            if ((tokenXML == "<tokens>") | (tokenXML == "</tokens>")):
                pureToken = "token"
            else:
                pureToken = tokenXML.split(" ")[1]
            tupple_token = (pureToken,tokenXML)
            return tupple_token
        else:
            return False



    def __peekAtNextEntry__(self):
        ''' copies, but does not remove the next token from the list of tokens as a tuple of the form
            (token, <tag> token </tag>).
            TT_TOKEN and TT_XML should be used for accessing the tuple components '''

        if self.tokens:
            tokenXML = self.tokens[0]
            if(tokenXML == "</tokens>"):
                pureToken = "</tokens>"
            else:
                pureToken = tokenXML.split(" ")[1]
            tupple_token = (pureToken,tokenXML)
        else:
            raise RuntimeError('Error, no tokens left in __peekAtNextEntry__ ')

        return tupple_token


    def __peekTwoAhead__(self):
        ''' copies, but does not remove the next token from the list of tokens as a tuple of the form
            (token, <tag> token </tag>).
            TT_TOKEN and TT_XML should be used for accessing the tuple components '''


        if(self.tokens):
            if (len(self.tokens) <= 2):
                tokenXML = self.tokens[0]
                pureToken = "</tokens>"
            else:
                tokenXML = self.tokens[1]
                pureToken = tokenXML.split(" ")[1]
            tupple_token = (pureToken,tokenXML)
        else:
            raise RuntimeError('Error, no tokens left in __peekTwoAhead__:')

        return tupple_token



    def __compileClass__(self):
        ''' compiles a class declaration.
            returning a list of VM commands. '''


        result = []
        result.append( '<class>' ) #structure label for class
        self.indentation += 2      #indentation level adjustment.  it will be paired at the bottom with a negative re-adjustment

        tokenTuple = self.__getNextEntry__()
        if tokenTuple[TT_TOKEN] == 'class':
            result.append( (self.indentation * ' ') + tokenTuple[TT_XML]) #keyword class

            tokenTuple = self.__getNextEntry__()
            self.className = tokenTuple[TT_TOKEN]
            # print("")
            result.append( (self.indentation * ' ') + tokenTuple[TT_XML]) #classname identifier

            tokenTuple = self.__getNextEntry__()
            result.append( (self.indentation * ' ') + tokenTuple[TT_XML]) #opening brace

            tokenTuple = self.__peekAtNextEntry__()

            #compile class vardecs until there are no more:
            while ((tokenTuple[TT_TOKEN] == "static") | (tokenTuple[TT_TOKEN] == "field")):

                result.extend(self.__compileClassVarDec__())
                tokenTuple = self.__peekAtNextEntry__()

            tokenTuple = self.__peekAtNextEntry__()


            # while tokenTuple is "constructor", "function", "method"
            while ((tokenTuple[TT_TOKEN] == "constructor") | (tokenTuple[TT_TOKEN] == "function") | (tokenTuple[TT_TOKEN] == "method")):
                result.extend(self.__compileSubroutine__())
                tokenTuple = self.__peekAtNextEntry__()


            tokenTuple = self.__getNextEntry__()

            result.append( (self.indentation * ' ') + tokenTuple[TT_XML])

        else:
            raise RuntimeError('Error, token provided:', tokenTuple[TT_TOKEN], ', is not class')

        #indentation level re-adjustment.
        self.indentation -= 2
        result.append( '</class>' )



        return result



    def __addToClassLevelSymbolTable__(self, name, typeOpt, kind):
        if (kind == "static"):
            num = CompilationEngine.CLASSLEVELSTATICCOUNT
            self.class_level_symbol_table[name] = [typeOpt, kind, num]
            CompilationEngine.CLASSLEVELSTATICCOUNT = CompilationEngine.CLASSLEVELSTATICCOUNT+1
        else:
            num = CompilationEngine.CLASSLEVELFIELDCOUNT
            self.class_level_symbol_table[name] = [typeOpt, kind, num]
            CompilationEngine.CLASSLEVELFIELDCOUNT = CompilationEngine.CLASSLEVELFIELDCOUNT+1

    def __compileClassVarDec__(self):
        ''' compiles a class variable declaration statement.
            returning a list of VM commands. '''


        #create opening <classVarDec> tag
        classVardecs = []
        classVardecs.append( (self.indentation * ' ') + "<classVarDec>")




        #indent
        self.indentation += 2

        #append 'static' or 'int' token   (from nextToken)
        tokenTuple1 = self.__getNextEntry__()

        if ((tokenTuple1[TT_TOKEN] == "static") | (tokenTuple1[TT_TOKEN] == "field")):
            classVardecs.append( (self.indentation * ' ') + tokenTuple1[TT_XML])
        else:
            raise RuntimeError("Error, __compileClassVarDec__ expected a 'static' or 'field' token and got: :", tokenTuple1[TT_TOKEN])

        #get next entry
        tokenTuple2 = self.__getNextEntry__()


        #append (what should be) a type token
        classVardecs.append( (self.indentation * ' ') + tokenTuple2[TT_XML])

        tokenTuple3 = self.__peekAtNextEntry__()

        #untill next token == ";"
        while(tokenTuple3[TT_TOKEN] != ";"):

            if (tokenTuple3[TT_TOKEN] != ","):
                #add entries to classLevelSymbolTable
                self.symbolTable.define(tokenTuple3[TT_TOKEN], tokenTuple2[TT_TOKEN], tokenTuple1[TT_TOKEN])


            tokenTuple3 = self.__getNextEntry__()
            classVardecs.append( (self.indentation * ' ') + tokenTuple3[TT_XML])

            if (tokenTuple3[TT_TOKEN] != ","):
                table = self.symbolTable.classTable()
                stringy = "<SYMBOL-Defined> class."
                stringy += tokenTuple3[TT_TOKEN]
                stringy += " ("
                stringy += table[tokenTuple3[TT_TOKEN]][1]
                stringy += " "
                stringy += table[tokenTuple3[TT_TOKEN]][0]
                stringy += ")"
                stringy += " = "
                stringy += str(table[tokenTuple3[TT_TOKEN]][2])
                stringy += " </SYMBOL-Defined>"
                classVardecs.append((self.indentation * ' ') + stringy)


            tokenTuple3 = self.__peekAtNextEntry__()

        #add ";" (from nextToken)
        tokenTuple = self.__getNextEntry__()
        classVardecs.append( (self.indentation * ' ') + tokenTuple[TT_XML])



        #un-indent
        self.indentation -= 2

        #close </classVarDec> tag
        classVardecs.append( (self.indentation * ' ') + "</classVarDec>")


        return classVardecs




    def __compileSubroutine__(self):
        ''' compiles a function/method.
            returning a list of VM commands.
            '''


        #create opening <subroutineDec> tag
        subroutineDecList = []
        subroutineDecList.append((self.indentation * ' ') + '<subroutineDec>')

        #indent
        self.indentation += 2

        tokenTuple = self.__getNextEntry__()

        #clear symbol table
        # self.method_level_symbol_table = {}
        self.symbolTable.startSubroutine()


        keyword = tokenTuple[TT_TOKEN]




        if(tokenTuple[TT_TOKEN] == "method"):
            # print("we got a method:")
            # print("putting class name keyword into class level table")
            # self.method_level_symbol_table["this"] = [self.className, "argument", "#?"]
            # def define(self, name, typeOpt, kind):
            self.symbolTable.define("this", self.className, "arg")


        #append keyword 'constructor', 'function', or 'method' token    (from nextToken)
            #check for one of those 3 words ^
        subroutineDecList.append((self.indentation * ' ') + tokenTuple[TT_XML])

        #append keyword/identifier of:  ('void' | int | char | boolean | className) token
        self.voidMethod = False
        tokenTuple = self.__getNextEntry__()
        if(tokenTuple[TT_TOKEN] == "void"):
            self.voidMethod = True

        subroutineDecList.append((self.indentation * ' ') + tokenTuple[TT_XML])

        #append identifier of: subroutineName      (from nextToken)
        tokenTuple = self.__getNextEntry__()
        self.subRoutineName = tokenTuple[TT_TOKEN]
        subroutineDecList.append((self.indentation * ' ') + tokenTuple[TT_XML])

        #append "("    (from nextToken)
        tokenTuple = self.__getNextEntry__()

        subroutineDecList.append((self.indentation * ' ') + tokenTuple[TT_XML])

        #append <parameterList>
        subroutineDecList.append((self.indentation * ' ') + '<parameterList>')
        #indent
        self.indentation += 2

        #peak at next token,
        tokenTuple = self.__peekAtNextEntry__()

        # while nextToken != ")"
        while(tokenTuple[TT_TOKEN] != ")"):
            # subroutineDecList.append((self.indentation * ' ')+ )
            subroutineDecList.extend(self.__compileParameterList__())
            tokenTuple = self.__peekAtNextEntry__()



        #unindent
        self.indentation -= 2
        #append </parameterList>
        subroutineDecList.append((self.indentation * ' ') + '</parameterList>')

        #get the ")"
        tokenTuple = self.__getNextEntry__()

        subroutineDecList.append((self.indentation * ' ') + tokenTuple[TT_XML])

        #append <subroutineBody> tag
        subroutineDecList.append((self.indentation * ' ') + '<subroutineBody>')

        #indent
        self.indentation += 2

        #append "{"   (from nextToken)
        tokenTuple = self.__getNextEntry__()
        subroutineDecList.append((self.indentation * ' ') + tokenTuple[TT_XML])




        tokenTuple = self.__peekAtNextEntry__()

        #for every subroutine body, you will rezero the vars
        CompilationEngine.METHOD_SCOPE_VAR_COUNTER = 0

        while(tokenTuple[TT_TOKEN] == "var"):

            #append <varDec>
            subroutineDecList.append((self.indentation * ' ') + '<varDec>')
            #indent
            self.indentation += 2

            #result.append(self.__compileVarDec__())
            subroutineDecList.extend(self.__compileVarDec__())

            #unindent
            self.indentation -= 2

            #append </varDec>
            subroutineDecList.append((self.indentation * ' ') + '</varDec>')
            tokenTuple = self.__peekAtNextEntry__()


        #building function name after var decs, before compile statements
        if(keyword == "function"):
            functionNameString = keyword + " " + self.className + "." + self.subRoutineName
            functionName = self.vmWriter.writeFunction(functionNameString, self.symbolTable.varCount())
            self.vmInstList.extend(functionName)
        if(keyword == "constructor"):
            functionName = "function " + self.className + "." + self.subRoutineName + " " + str(self.symbolTable.varCount())
            self.vmInstList.extend([functionName])
            self.vmInstList.extend(["push constant " + str(self.symbolTable.CLASSLEVELFIELDCOUNT)])
            self.vmInstList.extend(["call Memory.alloc 1"])
            self.vmInstList.extend(["pop pointer 0"])
        if(keyword== "method"):
            functionName = "function " + self.className + "." + self.subRoutineName + " " + str(self.symbolTable.varCount())
            self.vmInstList.extend([functionName])
            self.vmInstList.extend(["push argument 0", "pop pointer 0"])

        subroutineDecList.extend(self.__compileStatements__())


        #append "}"   (from nextToken)
        tokenTuple = self.__getNextEntry__()
        subroutineDecList.append((self.indentation * ' ') + tokenTuple[TT_XML])
        #unindent
        self.indentation -= 2
        #close </subroutineBody> tag
        subroutineDecList.append((self.indentation * ' ') + '</subroutineBody>')

        #unindent
        self.indentation -= 2
        #close </subroutineDec> tag
        subroutineDecList.append((self.indentation * ' ') + '</subroutineDec>')






        return subroutineDecList

    def __populateMethodLevelSymbolTable__(self):

        methodArgCounter = 0
        list_of_commands = []
        counter = 0
        tokenTuple = self.tokens[counter].split(" ")[1]
        while(tokenTuple != ")"):

            list_of_commands.append(tokenTuple)
            tokenTuple = self.tokens[counter].split(" ")[1]
            counter = counter + 1

        while(list_of_commands):
            methodArgCounter = methodArgCounter +1
            self.symbolTable.define(list_of_commands[2], list_of_commands[1], "arg")

            list_of_commands = list_of_commands[3:]





    def __compileParameterList__(self):
        ''' compiles a parameter list from a function/method.
            returning a list of VM commands.
            '''


        parameterList = []

        #untill next token == ")"
        tokenTuple = self.__peekAtNextEntry__()

        self.__populateMethodLevelSymbolTable__()



        while(tokenTuple[TT_TOKEN] != ")"):

           tokenTuple = self.__getNextEntry__()
           parameterList.append((self.indentation * ' ') + tokenTuple[TT_XML])


           if(tokenTuple[TT_TOKEN] in self.symbolTable.methodTable()):
                openTag = "<SYMBOL-Defined> subroutine."
                closeTag = " </SYMBOL-Defined>"
                table = self.symbolTable.methodTable()
                stringy = openTag
                stringy += tokenTuple[TT_TOKEN]
                stringy += " ("
                stringy += table[tokenTuple[TT_TOKEN]][1]
                stringy += " "
                stringy += table[tokenTuple[TT_TOKEN]][0]
                stringy += ")"
                stringy += " = "
                stringy += str(table[tokenTuple[TT_TOKEN]][2])
                stringy += closeTag
                parameterList.append((self.indentation * ' ') + stringy)

           if(tokenTuple[TT_TOKEN] in self.symbolTable.classTable()):
                openTag = "<SYMBOL-Defined> class."
                closeTag = " </SYMBOL-Defined>"
                table = self.symbolTable.classTable()

                stringy = openTag
                stringy += tokenTuple[TT_TOKEN]
                stringy += " ("
                stringy += table[tokenTuple[TT_TOKEN]][1]
                stringy += " "
                stringy += table[tokenTuple[TT_TOKEN]][0]
                stringy += ")"
                stringy += " = "
                stringy += str(table[tokenTuple[TT_TOKEN]][2])
                stringy += closeTag
                parameterList.append((self.indentation * ' ') + stringy)


           tokenTuple = self.__peekAtNextEntry__()



        return parameterList


    def __populateMethodLevelSymbolTableWithVars__(self):



        list_of_commands = []
        counter = 0

        tokenTuple = self.tokens[counter].split(" ")[1]
        while(tokenTuple != ";"):
            list_of_commands.append(tokenTuple)
            tokenTuple = self.tokens[counter].split(" ")[1]
            counter = counter + 1

        kind = list_of_commands[1]

        typ = list_of_commands[2]
        list_of_commands = list_of_commands[3:]

        # CompilationEngine.METHOD_SCOPE_VAR_COUNTER = 0
        while(list_of_commands):

            #name type kind
            self.symbolTable.define(list_of_commands[0], typ, kind)
            list_of_commands = list_of_commands[2:]




    def __compileVarDec__(self):
        ''' compiles a single variable declaration line.
            returning a list of VM commands. '''
        varDecList = []


        tokenTuple = self.__peekAtNextEntry__()

        self.__populateMethodLevelSymbolTableWithVars__()


        #"untill next token = ;' append next token"
        while (tokenTuple[TT_TOKEN] != ";"):
            self.argCounter += 1

            tokenTuple1 = self.__getNextEntry__()
            varDecList.append((self.indentation * ' ') + tokenTuple1[TT_XML])
            tokenTuple = self.__peekAtNextEntry__()



            if ((tokenTuple[TT_TOKEN] == ",") | (tokenTuple[TT_TOKEN] == ";")):
                stringy = "<SYMBOL-Defined> subroutine."
                stringy += tokenTuple1[TT_TOKEN]
                stringy += " ("
                stringy += self.symbolTable.methodTable()[tokenTuple1[TT_TOKEN]][1]
                stringy += " "
                stringy += self.symbolTable.methodTable()[tokenTuple1[TT_TOKEN]][0]
                stringy += ")"
                stringy += " = "
                stringy += str(self.symbolTable.methodTable()[tokenTuple1[TT_TOKEN]][2])
                stringy += " </SYMBOL-Defined>"
                varDecList.append((self.indentation * ' ') + stringy)


        #this is the ";"...append it before next vardec
        tokenTuple = self.__getNextEntry__()
        varDecList.append((self.indentation * ' ') + tokenTuple[TT_XML])



        return varDecList



    def __compileStatements__(self):
        ''' compiles statements.
            returning a list of VM commands.
            assumes any leading and trailing braces are be consumed by the caller'''

        statements = []


        tokenTupleTag = self.__peekAtNextEntry__()

        # <statements>
        statements.append((self.indentation * ' ') + '<statements>')

        #indent
        self.indentation += 2


        while(tokenTupleTag[TT_TOKEN] in STATEMENTS):


            if (tokenTupleTag[TT_TOKEN] == "let"):
                statements.extend(self.__compileLet__())
            elif (tokenTupleTag[TT_TOKEN] == "if"):
                statements.extend(self.__compileIf__())
            elif (tokenTupleTag[TT_TOKEN] == "while"):
                statements.extend(self.__compileWhile__())
            elif (tokenTupleTag[TT_TOKEN] == "do"):
                statements.extend(self.__compileDo__())
            elif(tokenTupleTag[TT_TOKEN] == "return"):
                statements.extend(self.__compileReturn__())
            else:
                #there must be an error!!!
                raise RuntimeError('Error, inside of __compileStatements__(). This token is not a statment: ' +     tokenTupleTag[TT_TOKEN])

            #look at next token to see if we continue to find statements or not
            tokenTupleTag = self.__peekAtNextEntry__()

        #unindent
        self.indentation -= 2

        statements.append((self.indentation * ' ') + '</statements>')


        return statements




    def __compileDo__(self):
        ''' compiles a function/method call.
            returning a list of VM commands. '''
        doStatements = []

        # append <doStatement>
        doStatements.append((self.indentation * ' ') + '<doStatement>')
        # indent
        self.indentation += 2

        #add "do"
        tokenTuple = self.__getNextEntry__()
        doStatements.append((self.indentation * ' ') + tokenTuple[TT_XML])


        doStatements.extend(self.__compileSubroutineCall__())

        self.vmInstList.extend(self.vmWriter.writePop("temp", "0"))

        #append ";"
        tokenTuple = self.__getNextEntry__()
        doStatements.append((self.indentation * ' ') + tokenTuple[TT_XML])

        # unindent
        self.indentation -= 2
        # append </doStatement>
        doStatements.append((self.indentation * ' ') + '</doStatement>')


        return doStatements



    def __compileLet__(self):
        ''' compiles a variable assignment statement.
            returning a list of VM commands. '''

        letStatement = []

        isArray = False

        # append <letStatement>
        letStatement.append((self.indentation * ' ') + '<letStatement>')

        # indent
        self.indentation += 2

        # append "let" keyword from nextToken
        #  <keyword> let </keyword>
        tokenTuple = self.__getNextEntry__()
        letStatement.append((self.indentation * ' ') + tokenTuple[TT_XML])

        # append varName identifier
        tokenTuple_ID = self.__getNextEntry__()
        #  <identifier> value </identifier>
        letStatement.append((self.indentation * ' ') + tokenTuple_ID[TT_XML])

        #symbol defined code
        if (tokenTuple_ID[TT_TOKEN] in self.symbolTable.methodTable()):

            table = self.symbolTable.methodTable()
            openTag = "<SYMBOL-Used> subroutine."
            stringy = openTag
            stringy += tokenTuple_ID[TT_TOKEN]
            stringy += " ("
            stringy += table[tokenTuple_ID[TT_TOKEN]][1]
            stringy += " "
            stringy += table[tokenTuple_ID[TT_TOKEN]][0]
            stringy += ")"
            stringy += " = "
            stringy += str(table[tokenTuple_ID[TT_TOKEN]][2])
            closeTag = " </SYMBOL-Used>"
            stringy += closeTag
            letStatement.append((self.indentation * ' ') + stringy)

        if (tokenTuple_ID[TT_TOKEN] in self.symbolTable.classTable()):
            table = self.symbolTable.classTable()
            openTag = "<SYMBOL-Used> class."
            stringy = openTag
            stringy += tokenTuple_ID[TT_TOKEN]
            stringy += " ("
            stringy += table[tokenTuple_ID[TT_TOKEN]][1]
            stringy += " "
            stringy += table[tokenTuple_ID[TT_TOKEN]][0]
            stringy += ")"
            stringy += " = "
            stringy += str(table[tokenTuple_ID[TT_TOKEN]][2])
            closeTag = " </SYMBOL-Used>"
            stringy += closeTag
            letStatement.append((self.indentation * ' ') + stringy)



        # if nextKey = "["
        # then we know we need to compile an expression
        tokenTuple = self.__peekAtNextEntry__()
        if(tokenTuple[TT_TOKEN] == "["):
            isArray = True
            # append "["
            tokenTuple = self.__getNextEntry__()
            letStatement.append((self.indentation * ' ') + tokenTuple[TT_XML])
            # self.__compileExpression__()
            letStatement.extend(self.__compileExpression__())
            # append "]"
            tokenTuple = self.__getNextEntry__()
            letStatement.append((self.indentation * ' ') + tokenTuple[TT_XML])

        # append "="
        tokenTuple = self.__getNextEntry__()
        letStatement.append((self.indentation * ' ') + tokenTuple[TT_XML])
        # append self.__compileExpression__()
        letStatement.extend(self.__compileExpression__())


        #IF ARRAY stuff
        if(isArray):
            #do array stuff
            self.vmInstList.extend(self.vmWriter.writePop("temp", "0"))
            if(self.symbolTable.kindOf(tokenTuple_ID[TT_TOKEN]) == "var"):
                self.vmInstList.extend(self.vmWriter.writePush("local", self.symbolTable.indexOf(tokenTuple_ID[TT_TOKEN])))
            elif(self.symbolTable.kindOf(tokenTuple_ID[TT_TOKEN]) == "arg"):
                self.vmInstList.extend(self.vmWriter.writePush("argument", self.symbolTable.indexOf(tokenTuple_ID[TT_TOKEN])))
            elif(self.symbolTable.kindOf(tokenTuple_ID[TT_TOKEN]) == "static"):
                self.vmInstList.extend(self.vmWriter.writePush("static", self.symbolTable.indexOf(tokenTuple_ID[TT_TOKEN])))
            elif(self.symbolTable.kindOf(tokenTuple_ID[TT_TOKEN]) == "field"):
                self.vmInstList.extend(self.vmWriter.writePush("this", self.symbolTable.indexOf(tokenTuple_ID[TT_TOKEN])))
            self.vmInstList.extend(["add"])
            self.vmInstList.extend(self.vmWriter.writePop("pointer", "1"))
            self.vmInstList.extend(self.vmWriter.writePush("temp", "0"))
            self.vmInstList.extend(self.vmWriter.writePop("that", "0"))

        else:
            if(self.symbolTable.kindOf(tokenTuple_ID[TT_TOKEN]) == "field"):
                self.vmInstList.extend(self.vmWriter.writePop("this", self.symbolTable.indexOf(tokenTuple_ID[TT_TOKEN])))
            elif(self.symbolTable.kindOf(tokenTuple_ID[TT_TOKEN]) == "static"):
                self.vmInstList.extend(self.vmWriter.writePop("static", self.symbolTable.indexOf(tokenTuple_ID[TT_TOKEN])))
            elif(tokenTuple_ID[TT_TOKEN] in self.symbolTable.methodTable()):
                if(self.symbolTable.kindOf(tokenTuple_ID[TT_TOKEN]) == "var"):
                    self.vmInstList.extend(self.vmWriter.writePop("local", self.symbolTable.indexOf(tokenTuple_ID[TT_TOKEN])))
                elif(self.symbolTable.kindOf(tokenTuple_ID[TT_TOKEN]) == "arg"):
                    self.vmInstList.extend(self.vmWriter.writePop("argument", self.symbolTable.indexOf(tokenTuple_ID[TT_TOKEN])))


        #append ";"
        tokenTuple = self.__getNextEntry__()
        letStatement.append((self.indentation * ' ') + tokenTuple[TT_XML])

        # unindent
        self.indentation -= 2
        # append </letStatement>
        letStatement.append((self.indentation * ' ') + '</letStatement>')

        return letStatement




    def __compileWhile__(self):
        ''' compiles a while loop.
            returning a list of VM commands. '''
        whileList = []

        num = self.getLabel()

        whileLabel ="WHILE_TOP_"+str(num)
        whileExitLabel = "WHILE_EXIT_"+str(num)
        whileIfLabel = self.vmWriter.WriteIf("WHILE_EXIT_"+str(num))
        self.vmInstList.extend([self.vmWriter.WriteLabel(whileLabel)])


        #append <whileStatement>
        whileList.append((self.indentation * ' ') + '<whileStatement>')
        #indent
        self.indentation += 2
        # append "while" (from nextToken)
        tokenTuple = self.__getNextEntry__()
        whileList.append((self.indentation * ' ') + tokenTuple[TT_XML])
        # append "("     (from nextToken)
        tokenTuple = self.__getNextEntry__()
        whileList.append((self.indentation * ' ') + tokenTuple[TT_XML])
        # append self.__compileExpression__()
        whileList.extend(self.__compileExpression__())
        # append ")"     (from nextToken)
        tokenTuple = self.__getNextEntry__()
        whileList.append((self.indentation * ' ') + tokenTuple[TT_XML])
        #append not
        self.vmInstList.extend(["not"])
        #append exit
        self.vmInstList.extend([self.vmWriter.WriteIf(whileExitLabel)])



        # append "{"     (from nextToken)
        tokenTuple = self.__getNextEntry__()
        whileList.append((self.indentation * ' ') + tokenTuple[TT_XML])
        # append self.__compileStatements__()
        whileList.extend(self.__compileStatements__())
        # append "}"      (from nextToken)
        tokenTuple = self.__getNextEntry__()
        whileList.append((self.indentation * ' ') + tokenTuple[TT_XML])

        self.vmInstList.extend([self.vmWriter.WriteGoto(whileLabel)])
        self.vmInstList.extend([self.vmWriter.WriteLabel(whileExitLabel)])

        # print(self.vmInstList)

        #unindent
        self.indentation -= 2
        #append </whileStatement>
        whileList.append((self.indentation * ' ') + '</whileStatement>')

        return whileList



    def __compileReturn__(self):
        ''' compiles a function return statement.
            returning a list of VM commands. '''

        returnList = []

        #TODO   make it work.

        #append <returnStatement>
        returnList.append((self.indentation * ' ') + '<returnStatement>')
        #indent
        self.indentation += 2

        # append "return" (from nextToken)
        tokenTuple = self.__getNextEntry__()
        returnList.append((self.indentation * ' ') + tokenTuple[TT_XML])

        # if nextToken is a member of one of the "terms":
        tokenTuple = self.__peekAtNextEntry__()
        if (tokenTuple[TT_TOKEN] != ";"):

            returnList.extend(self.__compileExpression__())
        else:
            self.vmInstList.extend(self.vmWriter.writePush("constant", "0"))

        self.vmInstList.extend(self.vmWriter.writeReturn())

        # append ";"      (from nextToken)
        tokenTuple = self.__getNextEntry__()
        returnList.append((self.indentation * ' ') + tokenTuple[TT_XML])

        #unindent
        self.indentation -= 2
        #append </returnStatement>
        returnList.append((self.indentation * ' ') + '</returnStatement>')

        return returnList



    def __compileIf__(self):
        ''' compiles an if(else)? statement block.
            returning a list of VM commands. '''

        #TODO   make it work.
        ifList = []

        uniqueNum = str(self.getLabel())

        doElseStatement = "DO_ELSE_" + uniqueNum
        ifThenComplete = "IF_THEN_COMPLETE_" + uniqueNum

        #append <ifStatement>
        ifList.append((self.indentation * ' ') + '<ifStatement>')
        #indent
        self.indentation += 2

        # append "if" (from nextToken)
        tokenTuple = self.__getNextEntry__()


        ifList.append((self.indentation * ' ') + tokenTuple[TT_XML])
        # append "("  (from nextToken)
        tokenTuple = self.__getNextEntry__()

        ifList.append((self.indentation * ' ') + tokenTuple[TT_XML])

        # append self.__compileExpression__()
        ifList.extend(self.__compileExpression__())
        # append ")"  (from nextToken)
        tokenTuple = self.__getNextEntry__()
        ifList.append((self.indentation * ' ') + tokenTuple[TT_XML])

        #append not
        self.vmInstList.extend(["not"])
        #write if-do else
        self.vmInstList.extend([self.vmWriter.WriteIf(doElseStatement)])

        # append "{"  (from nextToken)
        tokenTuple = self.__getNextEntry__()
        ifList.append((self.indentation * ' ') + tokenTuple[TT_XML])
        # append self.__compileStatements__()
        ifList.extend(self.__compileStatements__())
        # append "}" (from nextToken)
        tokenTuple = self.__getNextEntry__()
        # close the statements with a bracket
        ifList.append((self.indentation * ' ') + tokenTuple[TT_XML])

        # if nextToken = "("
        tokenTuple = self.__peekAtNextEntry__()
        if(tokenTuple[TT_TOKEN] != "else"):
            #write goto, if then complete
            self.vmInstList.extend([self.vmWriter.WriteGoto(ifThenComplete)])
            #write label, do else
            self.vmInstList.extend([self.vmWriter.WriteLabel(doElseStatement)])

        if(tokenTuple[TT_TOKEN] == "else"):
            # append "else"     (from nextToken)
            tokenTuple = self.__getNextEntry__()
            ifList.append((self.indentation * ' ') + tokenTuple[TT_XML])
            # append "{"  (from nextToken)
            tokenTuple = self.__getNextEntry__()
            ifList.append((self.indentation * ' ') + tokenTuple[TT_XML])

            #go to if then complete
            self.vmInstList.extend([self.vmWriter.WriteGoto(ifThenComplete)])
            #write label, do else
            self.vmInstList.extend([self.vmWriter.WriteLabel(doElseStatement)])


            # append self.__compileStatements__()
            ifList.extend(self.__compileStatements__())
            # append "}"     (from nextToken)
            tokenTuple = self.__getNextEntry__()
            ifList.append((self.indentation * ' ') + tokenTuple[TT_XML])


        #write if-then complete
        self.vmInstList.extend([self.vmWriter.WriteLabel(ifThenComplete)])

        #unindent
        self.indentation -= 2
        #append <ifStatement>
        ifList.append((self.indentation * ' ') + '</ifStatement>')

        return ifList


    def __compileExpression__(self):
        ''' compiles an expression.
            returning a list of VM commands. '''

        #TODO   make it work.
        expressionList = []


        #append <expression> tag
        expressionList.append((self.indentation * ' ') + '<expression>')

        self.indentation += 2

        #compile the first term in expression, guaranteed to be there
        expressionList.extend(self.__compileTerm__())

        #if there are more terms in expression, compile them,
        #   otherwise, we know term is done and close the expression (below)
        nextToken = self.__peekAtNextEntry__()
        while(nextToken[TT_TOKEN] in OPERATORS):

            #append the operator:
            tokenTuple = self.__getNextEntry__()
            expressionList.append((self.indentation * ' ') + tokenTuple[TT_XML])

            #compile term
            expressionList.extend(self.__compileTerm__())

            self.vmInstList.extend(self.vmWriter.writeArithmetic(tokenTuple[TT_TOKEN]))

            nextToken = self.__peekAtNextEntry__()

        self.indentation -= 2


        expressionList.append((self.indentation * ' ') + '</expression>')


        return expressionList

    def __compileTerm__(self):
        ''' compiles a term.
            returning a list of VM commands. '''

        termList = []


        # self.indentation += 2
        # append <term> tag
        termList.append((self.indentation * ' ') + '<term>')
        # indent
        self.indentation += 2

        nextToken = self.__peekAtNextEntry__()


        #if peaked token is "(" you'll compile an expression
        if (nextToken[TT_TOKEN] == "("):
            # append the "(" token
            tokenTuple = self.__getNextEntry__()
            termList.append((self.indentation * ' ') + tokenTuple[TT_XML])

            #compile expression
            termList.extend(self.__compileExpression__())

            #append the ")" token
            tokenTuple = self.__getNextEntry__()
            termList.append((self.indentation * ' ') + tokenTuple[TT_XML])

        #if peaked token is unary opp, you'll compile term
        elif(nextToken[TT_TOKEN] in UNARY_OPERATORS):
            #append the unary opp
            tokenTuple = self.__getNextEntry__()
            termList.append((self.indentation * ' ') + tokenTuple[TT_XML])

            #compile the term
            termList.extend(self.__compileTerm__())

            self.vmInstList.extend([UNARY_OPERATORS[tokenTuple[TT_TOKEN]]])



        #otherwise, its more complicated
        else:

            #we'll need to look at the next token:
            peakToken = self.__peekTwoAhead__()
            if ((peakToken[TT_TOKEN] == ".") | (peakToken[TT_TOKEN] == "(")):
                termList.extend(self.__compileSubroutineCall__())

            else:
                if(nextToken[TT_XML].startswith("<integerConstant>")):
                    #append nextToken (which is an integerConstant)
                    tokenTuple = self.__getNextEntry__()
                    termList.append((self.indentation * ' ') + tokenTuple[TT_XML])

                    pushCommand = self.vmWriter.writePush("constant", tokenTuple[TT_TOKEN])

                    self.vmInstList.extend(pushCommand)

                # elif nextToken tag = <stringConstant>
                elif(nextToken[TT_XML].startswith("<stringConstant>")):
                    #append nextToken (which is a stringConstant)
                    tokenTuple = self.__getNextEntry__()
                    termList.append((self.indentation * ' ') + tokenTuple[TT_XML])

                    #dal with strings here
                    lenOfXMLTags = 17
                    actualString = tokenTuple[TT_XML][lenOfXMLTags:-lenOfXMLTags-1]
                    lengthOfString = len(actualString)
                    self.vmInstList.extend(self.vmWriter.writePush("constant", str(lengthOfString)))
                    self.vmInstList.extend(self.vmWriter.writeCall("String.new", "1"))
                    for char in actualString:
                        num = ord(char)
                        self.vmInstList.extend(self.vmWriter.writePush("constant", str(num)))
                        self.vmInstList.extend(self.vmWriter.writeCall("String.appendChar", "2"))

                # elif nextToken tag = <keyword>
                elif(nextToken[TT_XML].startswith("<keyword>")):
                    #append nextToken tag
                    tokenTuple = self.__getNextEntry__()
                    termList.append((self.indentation * ' ') + tokenTuple[TT_XML])

                    if(nextToken[TT_TOKEN] in KEYWORD_CONSTANTS):
                        if(nextToken[TT_TOKEN] == "true"):
                            self.vmInstList.extend(self.vmWriter.writePush("constant", "0"))
                            self.vmInstList.extend(["not"])
                        elif(nextToken[TT_TOKEN] == "false"):
                            self.vmInstList.extend(self.vmWriter.writePush("constant", "0"))
                        if(nextToken[TT_TOKEN] == "this"):
                            self.vmInstList.extend(self.vmWriter.writePush("pointer", "0"))
                        if(nextToken[TT_TOKEN] == "null"):
                            self.vmInstList.extend(self.vmWriter.writePush("constant", "0"))




                else:
                    #append the var name
                    tokenTuple = self.__getNextEntry__()
                    termList.append((self.indentation * ' ') + tokenTuple[TT_XML])

                    varName = tokenTuple[TT_TOKEN]

                    if (tokenTuple[TT_TOKEN] in self.symbolTable.methodTable()):
                        table = self.symbolTable.methodTable()
                        openTag = "<SYMBOL-Used> subroutine."
                        stringy = openTag
                        stringy += tokenTuple[TT_TOKEN]
                        stringy += " ("
                        stringy += table[tokenTuple[TT_TOKEN]][1]
                        stringy += " "
                        stringy += table[tokenTuple[TT_TOKEN]][0]
                        stringy += ")"
                        stringy += " = "
                        stringy += str(table[tokenTuple[TT_TOKEN]][2])
                        closeTag = " </SYMBOL-Used>"
                        stringy += closeTag
                        termList.append((self.indentation * ' ') + stringy)

                    if(tokenTuple[TT_TOKEN] in self.symbolTable.classTable()):
                        table = self.symbolTable.classTable()
                        openTag = "<SYMBOL-Used> class."
                        stringy = openTag
                        stringy += tokenTuple[TT_TOKEN]
                        stringy += " ("
                        stringy += table[tokenTuple[TT_TOKEN]][1]
                        stringy += " "
                        stringy += table[tokenTuple[TT_TOKEN]][0]
                        stringy += ")"
                        stringy += " = "
                        stringy += str(table[tokenTuple[TT_TOKEN]][2])
                        closeTag = " </SYMBOL-Used>"
                        stringy += closeTag
                        termList.append((self.indentation * ' ') + stringy)



                    nextToken = self.__peekAtNextEntry__()
                    testToken = self.__peekTwoAhead__()


                    if(nextToken[TT_TOKEN] == "["):
                        #append the "["
                        tokenTuple = self.__getNextEntry__()
                        termList.append((self.indentation * ' ') + tokenTuple[TT_XML])
                        termList.extend(self.__compileExpression__())

                        if(self.symbolTable.kindOf(varName) == "var"):
                            self.vmInstList.extend(self.vmWriter.writePush("local", self.symbolTable.indexOf(varName)))

                        elif(self.symbolTable.kindOf(varName) == "arg"):
                            self.vmInstList.extend(self.vmWriter.writePush("argument", self.symbolTable.indexOf(varName)))

                        elif(self.symbolTable.kindOf(varName) == "field"):
                            self.vmInstList.extend(self.vmWriter.writePush("this", self.symbolTable.indexOf(varName)))

                        elif(self.symbolTable.kindOf(varName) == "static"):
                            self.vmInstList.extend(self.vmWriter.writePush("static", self.symbolTable.indexOf(varName)))

                        #append add
                        self.vmInstList.extend(["add"])
                        #append pop pointer 1
                        self.vmInstList.extend(self.vmWriter.writePop("pointer", "1"))
                        # append push that 0
                        self.vmInstList.extend(self.vmWriter.writePush("that", "0"))

                        tokenTuple = self.__getNextEntry__()
                        termList.append((self.indentation * ' ') + tokenTuple[TT_XML])


                    elif(nextToken[TT_TOKEN] != "["):


                        if(self.symbolTable.kindOf(varName) == "var"):
                            self.vmInstList.extend(self.vmWriter.writePush("local", self.symbolTable.indexOf(varName)))

                        elif(self.symbolTable.kindOf(varName) == "arg"):
                            self.vmInstList.extend(self.vmWriter.writePush("argument", self.symbolTable.indexOf(varName)))

                        elif(self.symbolTable.kindOf(varName) == "field"):
                            self.vmInstList.extend(self.vmWriter.writePush("this", self.symbolTable.indexOf(varName)))

                        elif(self.symbolTable.kindOf(varName) == "static"):
                            self.vmInstList.extend(self.vmWriter.writePush("static", self.symbolTable.indexOf(varName)))


        self.indentation -= 2

        termList.append((self.indentation * ' ') + '</term>')



        return termList




    def __compileExpressionList__(self):
        ''' compiles a list of expressions.
            returning a list of VM commands. '''

        result = []

        self.ListOfOps = []

        self.argCounter = 0

        result.append((self.indentation * ' ') + "<expressionList>")
        self.indentation += 2

        tokenTuple = self.__peekAtNextEntry__()

        while(tokenTuple[TT_TOKEN] != ")"):
            self.argCounter += 1

            result.extend(self.__compileExpression__())
            tokenTuple = self.__peekAtNextEntry__()
            if(tokenTuple[TT_TOKEN] == ","):
                tokenTuple = self.__getNextEntry__()
                result.append((self.indentation * ' ') + tokenTuple[TT_XML])



            tokenTuple = self.__peekAtNextEntry__()

        self.indentation -= 2
        result.append((self.indentation * ' ') + "</expressionList>")


        return result




    def __compileSubroutineCall__(self):
        ''' compiles a subroutine call.
            returning a list of VM commands. '''

        subRoutineCallList = []

        #get first token, it will be an identifier
            # either subRoutineName
            # or className/Varname
        tokenTuple0 = self.__getNextEntry__()
        subRoutineCallList.append((self.indentation * ' ') + tokenTuple0[TT_XML])

        varName = tokenTuple0[TT_TOKEN]
        baseName = tokenTuple0[TT_TOKEN]
        self.argCounter = 0
        otherNum = 0

        #put symbol used code here
        if (tokenTuple0[TT_TOKEN] in self.symbolTable.methodTable()):
                table = self.symbolTable.methodTable()
                openTag = "<SYMBOL-Used> subroutine."
                closeTag = " </SYMBOL-Used>"
                otherName = table[tokenTuple0[TT_TOKEN]][0]
                num = str(table[tokenTuple0[TT_TOKEN]][2])
                if(table[tokenTuple0[TT_TOKEN]][1].startswith("argument")):
                   argName = "arg"
                else:
                   argName = table[tokenTuple0[TT_TOKEN]][1]
                stringy = openTag
                stringy += tokenTuple0[TT_TOKEN]
                stringy += " ("
                stringy += argName
                stringy += " "
                stringy += otherName
                stringy += ")"
                stringy += " = "
                stringy += num
                stringy += closeTag
                subRoutineCallList.append((self.indentation * ' ') + stringy)
        if (tokenTuple0[TT_TOKEN] in self.symbolTable.classTable()):
                table = self.symbolTable.classTable()
                openTag = "<SYMBOL-Used> class."
                closeTag = " </SYMBOL-Used>"
                argName = table[tokenTuple0[TT_TOKEN]][1]
                otherName = table[tokenTuple0[TT_TOKEN]][0]
                num = str(table[tokenTuple0[TT_TOKEN]][2])
                stringy = openTag
                stringy += tokenTuple0[TT_TOKEN]
                stringy += " ("
                stringy += argName
                stringy += " "
                stringy += otherName
                stringy += ")"
                stringy += " = "
                stringy += num
                stringy += closeTag
                subRoutineCallList.append((self.indentation * ' ') + stringy)


        #get second token, it be a "." or a "(" which will determine wich type of subRoutine call to build
        tokenTuple = self.__getNextEntry__()

        #else (next_next is ".")
        if(tokenTuple[TT_TOKEN] == "."):

            if(tokenTuple0[TT_TOKEN] in self.symbolTable.methodTable()):

                if(self.symbolTable.kindOf(tokenTuple0[TT_TOKEN]) == "var"):
                    # print("$$")

                    self.vmInstList.extend(self.vmWriter.writePush("local", self.symbolTable.indexOf(tokenTuple0[TT_TOKEN])))

                    varName = self.symbolTable.typeOf(tokenTuple0[TT_TOKEN])

                #push local index
                elif(self.symbolTable.kindOf(tokenTuple0[TT_TOKEN]) == "arg"):

                    self.vmInstList.extend(self.vmWriter.writePush("argument", self.symbolTable.indexOf(tokenTuple0[TT_TOKEN])))

                self.argCounter += 1
                otherNum = self.argCounter
                varName = self.symbolTable.typeOf(tokenTuple0[TT_TOKEN])

            elif(tokenTuple0[TT_TOKEN] in self.symbolTable.classTable()):

                    if(self.symbolTable.kindOf(tokenTuple0[TT_TOKEN]) == "field"):
                        #push (this index of token)
                        self.vmInstList.extend(self.vmWriter.writePush("this", self.symbolTable.indexOf(tokenTuple0[TT_TOKEN])))

                    self.argCounter += 1
                    varName = self.symbolTable.typeOf(tokenTuple0[TT_TOKEN])
                    otherNum = self.argCounter
                    # other_num = str(self.argCounter)

            else: #not in method table or class table
                    varName = baseName

            # append "." from nextToken
            subRoutineCallList.append((self.indentation * ' ') + tokenTuple[TT_XML])
            # append subroutineName identifier
            tokenTuple_name = self.__getNextEntry__()
            subRoutineCallList.append((self.indentation * ' ') + tokenTuple_name[TT_XML])
            # append "(" from nextToken
            tokenTuple = self.__getNextEntry__()
            subRoutineCallList.append((self.indentation * ' ') + tokenTuple[TT_XML])
            # append self.__compileExpressionList__()
            subRoutineCallList.extend(self.__compileExpressionList__())
            # append ")"
            tokenTuple = self.__getNextEntry__()
            subRoutineCallList.append((self.indentation * ' ') + tokenTuple[TT_XML])

            # write call
            argName = varName + "." + tokenTuple_name[TT_TOKEN]
            self.vmInstList.extend(self.vmWriter.writeCall(argName, self.argCounter+otherNum))

        else: # next_next_char is "("

            #set up write call
            self.vmInstList.extend(self.vmWriter.writePush("pointer", "0"))
            varName = self.className + "." + tokenTuple0[TT_TOKEN]
            self.argCounter += 1
            otherNum = self.argCounter

            if(tokenTuple[TT_TOKEN] != "("):
              raise RuntimeError("Error, subroutineCall expected a '.' or '(' and got a :" + tokenTuple[TT_TOKEN])
            # append "(" from nextToken
            subRoutineCallList.append((self.indentation * ' ') + tokenTuple[TT_XML])

            #attempt to compile any expressionLists
            subRoutineCallList.extend(self.__compileExpressionList__())

            #write call
            self.vmInstList.extend(self.vmWriter.writeCall(varName, self.argCounter+otherNum))

            #close the bracket ")"
            tokenTuple = self.__getNextEntry__()
            subRoutineCallList.append((self.indentation * ' ') + tokenTuple[TT_XML])

        return subRoutineCallList
