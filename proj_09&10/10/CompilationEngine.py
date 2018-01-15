#
#CompilationEngine.py
#
# CS2002   Project 10 Jack Compiler (part 1)
#
# Summer 2013
# last updated 25 Oct 2016
#

from JTConstants import *

TT_TOKEN = 0
TT_XML = 1

class CompilationEngine(object):

############################################
# Constructor
    def __init__(self, tokenList):
        self.tokens = tokenList   #the list of tagged tokens to process (a copy was previously output as ____T.xml )

        #add and delete from this to reack left padding for XML file readability
        self.indentation = 0


############################################
# instance methods

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
            result.append( (self.indentation * ' ') + tokenTuple[TT_XML]) #classname identifier

            tokenTuple = self.__getNextEntry__()
            result.append( (self.indentation * ' ') + tokenTuple[TT_XML]) #opening brace

            # below needs to be peak next entry
            tokenTuple = self.__peekAtNextEntry__()

            #compile class vardecs until there are no more:
            while ((tokenTuple[TT_TOKEN] == "static") | (tokenTuple[TT_TOKEN] == "field")):
                result.extend(self.__compileClassVarDec__())
                # below needs to be peak next entry
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



    def __compileClassVarDec__(self):
        ''' compiles a class variable declaration statement.
            returning a list of VM commands. '''

        #create opening <classVarDec> tag
        classVardecs = []
        classVardecs.append( (self.indentation * ' ') + "<classVarDec>")

        #indent
        self.indentation += 2

        #append 'static' or 'int' token   (from nextToken)
        tokenTuple = self.__getNextEntry__()

        if ((tokenTuple[TT_TOKEN] == "static") | (tokenTuple[TT_TOKEN] == "field")):
            classVardecs.append( (self.indentation * ' ') + tokenTuple[TT_XML])
        else:
            raise RuntimeError("Error, __compileClassVarDec__ expected a 'static' or 'field' token and got: :", tokenTuple[TT_TOKEN])

        #get next entry
        tokenTuple = self.__getNextEntry__()
        #append (what should be) a type token
        classVardecs.append( (self.indentation * ' ') + tokenTuple[TT_XML])

        tokenTuple = self.__peekAtNextEntry__()

        #untill next token == ";"
            # for every variable name,
                #add identifier, comma (if more than 1 identifier)
        while(tokenTuple[TT_TOKEN] != ";"):

            tokenTuple = self.__getNextEntry__()
            classVardecs.append( (self.indentation * ' ') + tokenTuple[TT_XML])
            tokenTuple = self.__peekAtNextEntry__()

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

        #append keyword 'constructor', 'function', or 'method' token    (from nextToken)
            #check for one of those 3 words ^
        subroutineDecList.append((self.indentation * ' ') + tokenTuple[TT_XML])

        #append keyword/identifier of:  ('void' | int | char | boolean | className) token
        tokenTuple = self.__getNextEntry__()
        subroutineDecList.append((self.indentation * ' ') + tokenTuple[TT_XML])

        #append identifier of: subroutineName      (from nextToken)
        tokenTuple = self.__getNextEntry__()
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

        # append self.__compileSubroutineBody__()
        subroutineDecList.extend(self.__compileSubroutineBody__())

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



    def __compileParameterList__(self):
        ''' compiles a parameter list from a function/method.
            returning a list of VM commands.
            '''
        parameterList = []

        #untill next token == ")"
        tokenTuple = self.__peekAtNextEntry__()
        while(tokenTuple[TT_TOKEN] != ")"):
           tokenTuple = self.__getNextEntry__()
           parameterList.append((self.indentation * ' ') + tokenTuple[TT_XML])
           tokenTuple = self.__peekAtNextEntry__()

        return parameterList



    def __compileSubroutineBody__(self):

        subRoutineBodyList = []

        tokenTuple = self.__peekAtNextEntry__()

        # while next token = var
        while(tokenTuple[TT_TOKEN] == "var"):

            #append <varDec>
            subRoutineBodyList.append((self.indentation * ' ') + '<varDec>')
            #indent
            self.indentation += 2

            #result.append(self.__compileVarDec__())
            subRoutineBodyList.extend(self.__compileVarDec__())

            #unindent
            self.indentation -= 2

            #append </varDec>
            subRoutineBodyList.append((self.indentation * ' ') + '</varDec>')
            tokenTuple = self.__peekAtNextEntry__()

        subRoutineBodyList.extend(self.__compileStatements__())

        return subRoutineBodyList



    def __compileVarDec__(self):
        ''' compiles a single variable declaration line.
            returning a list of VM commands. '''
        varDecList = []

        tokenTuple = self.__peekAtNextEntry__()

        #"untill next token = ;' append next token"
        while (tokenTuple[TT_TOKEN] != ";"):

            tokenTuple = self.__getNextEntry__()
            varDecList.append((self.indentation * ' ') + tokenTuple[TT_XML])
            tokenTuple = self.__peekAtNextEntry__()

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

        tokenTuple = self.__getNextEntry__()
        #append "do" keyword
        doStatements.append((self.indentation * ' ') + tokenTuple[TT_XML])

        doStatements.extend(self.__compileSubroutineCall__())

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

        # append <letStatement>
        letStatement.append((self.indentation * ' ') + '<letStatement>')

        # indent
        self.indentation += 2

        # append "let" keyword from nextToken
        tokenTuple = self.__getNextEntry__()
        letStatement.append((self.indentation * ' ') + tokenTuple[TT_XML])

        # append varName identifier
        tokenTuple = self.__getNextEntry__()
        letStatement.append((self.indentation * ' ') + tokenTuple[TT_XML])


        # if nextKey = "["
        # then we know we need to compile an expression
        tokenTuple = self.__peekAtNextEntry__()
        if(tokenTuple[TT_TOKEN] == "["):
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
        # append "{"     (from nextToken)
        tokenTuple = self.__getNextEntry__()
        whileList.append((self.indentation * ' ') + tokenTuple[TT_XML])
        # append self.__compileStatements__()
        whileList.extend(self.__compileStatements__())
        # append "}"      (from nextToken)
        tokenTuple = self.__getNextEntry__()
        whileList.append((self.indentation * ' ') + tokenTuple[TT_XML])

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
            # append self.__compileExpression__()
            returnList.extend(self.__compileExpression__())

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
        if(tokenTuple[TT_TOKEN] == "else"):
            # append "else"     (from nextToken)
            tokenTuple = self.__getNextEntry__()
            ifList.append((self.indentation * ' ') + tokenTuple[TT_XML])
            # append "{"  (from nextToken)
            tokenTuple = self.__getNextEntry__()
            ifList.append((self.indentation * ' ') + tokenTuple[TT_XML])
            # append self.__compileStatements__()
            ifList.extend(self.__compileStatements__())
            # append "}"     (from nextToken)
            tokenTuple = self.__getNextEntry__()
            ifList.append((self.indentation * ' ') + tokenTuple[TT_XML])

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
        elif(nextToken[TT_TOKEN] in UNARY_OPS):
            #append the unary opp
            tokenTuple = self.__getNextEntry__()
            termList.append((self.indentation * ' ') + tokenTuple[TT_XML])
            #compile the term
            termList.extend(self.__compileTerm__())

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
                # elif nextToken tag = <stringConstant>
                elif(nextToken[TT_XML].startswith("<stringConstant>")):
                    #append nextToken (which is a stringConstant)
                    tokenTuple = self.__getNextEntry__()
                    termList.append((self.indentation * ' ') + tokenTuple[TT_XML])
                # elif nextToken tag = <keyword>
                elif(nextToken[TT_XML].startswith("<keyword>")):
                    #append nextToken tag
                    tokenTuple = self.__getNextEntry__()
                    termList.append((self.indentation * ' ') + tokenTuple[TT_XML])
                else:
                    #append the var name
                    tokenTuple = self.__getNextEntry__()
                    termList.append((self.indentation * ' ') + tokenTuple[TT_XML])

                    nextToken = self.__peekAtNextEntry__()
                    if(nextToken[TT_TOKEN] == "["):
                        #append the "["
                        tokenTuple = self.__getNextEntry__()
                        termList.append((self.indentation * ' ') + tokenTuple[TT_XML])
                        #compile the expression...kinda crazy recursive here
                        termList.extend(self.__compileExpression__())
                        #append the "]"
                        tokenTuple = self.__getNextEntry__()
                        termList.append((self.indentation * ' ') + tokenTuple[TT_XML])

        # unindent
        self.indentation -= 2

        # append </term> tag
        termList.append((self.indentation * ' ') + '</term>')


        return termList




    def __compileExpressionList__(self):
        ''' compiles a list of expressions.
            returning a list of VM commands. '''

        result = []

        result.append((self.indentation * ' ') + "<expressionList>")
        self.indentation += 2

        tokenTuple = self.__peekAtNextEntry__()

        # if token is not ")", there are expressions to compile:
        while(tokenTuple[TT_TOKEN] != ")"):
            result.extend(self.__compileExpression__())
            tokenTuple = self.__peekAtNextEntry__()
            #if the next token is a ",", append it, and
            #   there will be another expression that will be handled by while loop
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
        tokenTuple = self.__getNextEntry__()
        subRoutineCallList.append((self.indentation * ' ') + tokenTuple[TT_XML])

        #get second token, it be a "." or a "(" which will determine wich type of subRoutine call to build
        tokenTuple = self.__getNextEntry__()

        # if next_next_char is "("
        if(tokenTuple[TT_TOKEN] == "("):
            # append "(" from nextToken
            subRoutineCallList.append((self.indentation * ' ') + tokenTuple[TT_XML])

            #attempt to compile any expressionLists
            subRoutineCallList.extend(self.__compileExpressionList__())

            #close the bracket ")"
            tokenTuple = self.__getNextEntry__()
            subRoutineCallList.append((self.indentation * ' ') + tokenTuple[TT_XML])

        #else (next_next is ".")
        else:
            if(tokenTuple[TT_TOKEN] != "."):
                raise RuntimeError("Error, subroutineCall expected a '.' or '(' and got a :" + tokenTuple[TT_TOKEN])
            # append "." from nextToken
            subRoutineCallList.append((self.indentation * ' ') + tokenTuple[TT_XML])
            # append subroutineName identifier
            tokenTuple = self.__getNextEntry__()
            subRoutineCallList.append((self.indentation * ' ') + tokenTuple[TT_XML])
            # append "(" from nextToken
            tokenTuple = self.__getNextEntry__()
            subRoutineCallList.append((self.indentation * ' ') + tokenTuple[TT_XML])
            # append self.__compileExpressionList__()
            subRoutineCallList.extend(self.__compileExpressionList__())
            # append ")"
            tokenTuple = self.__getNextEntry__()
            subRoutineCallList.append((self.indentation * ' ') + tokenTuple[TT_XML])

        return subRoutineCallList
