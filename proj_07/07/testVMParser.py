#
#testVMParser.py
#
# CS2002   Project 7 Virtual Machine (part 1)
#
# Summer 2013
# last updated 30 Aug 2016
#


import unittest
from VMParser import *


class unitTests(unittest.TestCase):
    ''' unit tests for class VMParser'''

    def test__init__(self):
        fileName = 'StackArithmetic/SimpleAdd/SimpleAdd.vm'
        parser = VMParser(fileName)

        self.assertTrue( parser.toParse )  #empty lists are false per PEP 8
        '''

        '''


    def test_advance(self):
        fileName = 'StackArithmetic/SimpleAdd/SimpleAdd.vm'
        parser = VMParser(fileName)

        self.assertTrue( parser.advance() )   #check normal behavior

        parser.toParse = []
        self.assertFalse( parser.advance() )  #check list empty behavior

        #test more focused now with some canned info
        parser.toParse=[1,2,3]
        line = parser.advance()
        self.assertTrue(line == 1)
        self.assertTrue(len(parser.toParse) == 2)


    def test_command(self):
        fileName = 'StackArithmetic/SimpleAdd/SimpleAdd.vm'
        parser = VMParser(fileName)

        line = parser.advance()
        command = parser.command(line)
        self.assertTrue(command == 'push')


    def test_arg1(self):
        fileName = 'StackArithmetic/SimpleAdd/SimpleAdd.vm'
        parser = VMParser(fileName)

        line = parser.advance()
        arg1 = VMParser.arg1(line)
        self.assertTrue(arg1 == 'constant')

        line = parser.advance()
        line = parser.advance()

        #correctly ID a bad request
        self.assertRaises(RuntimeError, VMParser.arg1, line)


    def test_arg2(self):
        fileName = 'StackArithmetic/SimpleAdd/SimpleAdd.vm'
        parser = VMParser(fileName)

        line = parser.advance()
        arg2 = VMParser.arg2(line)
        self.assertTrue(arg2 == '7')

        line = parser.advance()
        line = parser.advance()

        #correctly ID a bad request
        self.assertRaises(RuntimeError, VMParser.arg2, line)




#
#************* automated tests run below
#
if __name__ == "__main__":
    unittest.main(exit=False)


