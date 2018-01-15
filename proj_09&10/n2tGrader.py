#
#
#N2T grading server
# projectnum in executable portion at bottom is the directory to be graded
#
#
# on *nix flavors launch from the command line as
#     python3 n2tGrader.py --XX
#
#     where --XX is the project number being run
#
#
# on Windows launch from the command line as
#     n2tGrader.py --XX --w
#
#     where --XX is the project number being run
#     and the --w is telling the script to use the windows .bat launch style
#
#




import os
import shutil
from pathlib import Path
import subprocess


NIX = 0
WIN = 1
PLATFORM = NIX


def testResults_01_02_05(codeDirectory, whichProject):

    testList = tests[whichProject]
    for test in testList:
        print(codeDirectory + '/' + test + 'tst')
        #launch the HardwareSimulator with test as the arg
        testCommand = '../../nand2tetris/tools/HardwareSimulator.sh ' + codeDirectory + '/' + test + 'tst'

        try:
            subprocess.run(testCommand, stdin=None, stdout=None, shell=True, check=True)

        except subprocess.CalledProcessError as cpe:
            print(codeDirectory, ':', cpe)



def testResults_03(codeDirectory):

    testDict = tests['tests03']
    for sublist in ['a', 'b']:
        testList = testDict[sublist]

        for test in testList:
            #launch the HardwareSimulator with test as the arg
            print(test)
            testCommand = '../../nand2tetris/tools/HardwareSimulator.sh ' + codeDirectory + '/' + sublist[0] + '/' + test + 'tst'

            try:
                subprocess.run(testCommand, stdin=None, stdout=None, shell=True, check=True)

            except subprocess.CalledProcessError as cpe:
                print(codeDirectory, ':', cpe)



def testResults_04(codeDirectory):

        #assemble the files to .hack machine language
        command = '../../nand2tetris/tools/Assembler.sh ' + codeDirectory + '/fill/Fill.asm'
        try:
            subprocess.run(command, stdin=None, stdout=None, timeout=0.5, shell=True, check=True)

        except subprocess.CalledProcessError as cpe:
            print(codeDirectory, ':', cpe, 'while trying to assemble')

        #fill must be run manually in CPU Emulator as it is a visual inspection

        command = '../../nand2tetris/tools/Assembler.sh ' + codeDirectory + '/mult/Mult.asm'
        try:
            subprocess.run(command, stdin=None, stdout=None, timeout=0.5, shell=True, check=True)

        except subprocess.CalledProcessError as cpe:
            print(codeDirectory, ':', cpe, 'while trying to assemble')


        #launch the CPUEmulator
        command = '../../nand2tetris/tools/CPUEmulator.sh ' + codeDirectory + '/mult/Mult.tst'

        try:
            subprocess.run(command, stdin=None, stdout=None, shell=True, check=True)

        except subprocess.CalledProcessError as cpe:
            print(codeDirectory, ':', cpe, 'while trying to test')





def compareLines(expectedFilePath, resultFilePath):

    #print('\n comparelines\n   ', str(expectedFilePath), '\n   ', str(resultFilePath))
    expected = open(str(expectedFilePath), 'r')
    result = open(str(resultFilePath), 'r')

    grade = True
    expectedLine = 'k'
    lineNumber = 0
    while len(expectedLine) > 0:
        expectedLine = expected.readline().strip()
        resultLine   = result.readline().strip()

        if expectedLine != resultLine:
            grade = False
            print('bad comparison', str(expectedFilePath.stem), 'line', lineNumber, expectedLine, resultLine)
            break
        else:
            lineNumber += 1

    expected.close()
    result.close()

    if (grade):
        print('    good:' , str(expectedFilePath.stem))



def compare_06(codeDirectory, checkfilesDir):

    resultFilePath = codeDirectory / 'add/Add.hack'
    expectedFilePath  = checkfilesDir / 'Add.hack'
    try:
        compareLines(expectedFilePath, resultFilePath)
    except Exception as error:
        print(codeDirectory, ':', error, 'while trying to compare student program')


    resultFilePath = codeDirectory / 'max/Max.hack'
    expectedFilePath  = checkfilesDir / 'Max.hack'
    try:
        compareLines(expectedFilePath, resultFilePath)
    except Exception as error:
        print(codeDirectory, ':', error, 'while trying to compare student program')

    resultFilePath = codeDirectory / 'rect/Rect.hack'
    expectedFilePath  = checkfilesDir / 'Rect.hack'
    try:
        compareLines(expectedFilePath, resultFilePath)
    except Exception as error:
        print(codeDirectory, ':', error, 'while trying to compare student program')


    resultFilePath = codeDirectory / 'pong/Pong.hack'
    expectedFilePath  = checkfilesDir / 'Pong.hack'
    try:
        compareLines(expectedFilePath, resultFilePath)
    except Exception as error:
        print(codeDirectory, ':', error, 'while trying to compare student program')

    print('\n', codeDirectory.name, 'done\n\n\n')




def assemble_06(codeDirectory, checkfilesDir):

        command = codeDirectory / 'Assembler.py'
        command = str(command)
        argDir = codeDirectory / 'add/Add.asm'
        arg = str(argDir)

        try:
            subprocess.call(['python3', command, arg])

        except subprocess.CalledProcessError as cpe:
            print(codeDirectory, ':', cpe, 'while trying to run student program')


        argDir = codeDirectory / 'max/Max.asm'
        arg = str(argDir)

        try:
            subprocess.call(['python3', command, arg])

        except subprocess.CalledProcessError as cpe:
            print(codeDirectory, ':', cpe, 'while trying to run student program')

        argDir = codeDirectory / 'rect/rect.asm'
        arg = str(argDir)


        try:
            subprocess.call(['python3', command, arg])

        except subprocess.CalledProcessError as cpe:
            print(codeDirectory, ':', cpe, 'while trying to run student program')

        argDir = codeDirectory / 'pong/Pong.asm'
        arg = str(argDir)


        try:
            subprocess.call(['python3', command, arg])

        except subprocess.CalledProcessError as cpe:
            print(codeDirectory, ':', cpe, 'while trying to run student program')



def testResults_07(studentPath):

    for eachtarget in targets07:
        if PLATFORM == NIX:
            command = 'python3 ' + studentPath.name + '/VMtoMnemonics.py ' + studentPath.name + '/' + eachtarget       #*NIX platform
        else:
            command = 'python ' + studentPath.name + '\\VMtoMnemonics.py ' + studentPath.name + '\\' + eachtarget                  #WIN platform

        try:
            subprocess.run(command, stdin=None, stdout=None, shell=True, check=True)

        except subprocess.CalledProcessError as cpe:
            print(studentPath.name, ':', cpe, 'while compiling', eachtarget )



    for eachtest in tests07:
        if PLATFORM == NIX:
            command = 'tools/CPUEmulator.sh ' + studentPath.name + eachtest + '.tst'       #*NIX platform
        else:
            command = 'tools\\CPUEmulator.bat ' + studentPath.name + eachtest + '.tst'     #WIN platform

        try:
            subprocess.run(command, stdin=None, stdout=None, shell=True, check=True)

        except subprocess.CalledProcessError as cpe:
            print(studentPath.name, ':', cpe, 'while running', eachtest )

    print('\n', studentPath.name, 'done\n\n\n')


def testResults_08(studentPath):

    for eachtarget in targets08:
        if PLATFORM == NIX:
            command = 'python3 ' + studentPath.name + '/VMtoMnemonics.py ' + studentPath.name + '/' + eachtarget       #*NIX platform
        else:
            command = 'python ' + studentPath.name + '\\VMtoMnemonics.py ' + studentPath.name + '\\' + eachtarget                  #WIN platform

        try:
            subprocess.run(command, stdin=None, stdout=None, shell=True, check=True)

        except subprocess.CalledProcessError as cpe:
            print(studentPath.name, ':', cpe, 'while compiling', eachtarget )


    for eachtest in tests08:
        if PLATFORM == NIX:
            command = 'tools/CPUEmulator.sh ' + studentPath.name + eachtest + '.tst'       #*NIX platform
        else:
            command = 'tools\\CPUEmulator.bat ' + studentPath.name + eachtest + '.tst'     #WIN platform

        try:
            subprocess.run(command, stdin=None, stdout=None, shell=True, check=True)

        except subprocess.CalledProcessError as cpe:
            print(studentPath.name, ':', cpe, 'while running', eachtest )

    print('\n', studentPath.name, 'done\n\n\n')




def testResults10(studentPath, checkFilesPath):


    #move existing .xml files
    for eachtarget in targets10:

        if PLATFORM == NIX:
            resultDirectory = studentPath.name + '/' + eachtarget
            newDir = resultDirectory + '/' +  'oldXML'
        else:
            resultDirectory = studentPath.name + '\\' + eachtarget    #WIN platform
            newDir = resultDirectory + '\\' +  'oldXML'

        resultDirectory = Path(resultDirectory)
        newDirPath = Path(newDir)
        if not newDirPath.exists():
            os.mkdir(newDir)

        for file in resultDirectory.iterdir():
            if file.suffix == '.xml':
                if PLATFORM == NIX:
                    newName = newDir + '/' + file.name
                else:
                    newName = newDir + '\\' + file.name    #WIN platform

                shutil.move( str(file)  , str(newName) )

    print('\n  xml moves complete for ' + studentPath.name)


    #run the project code
    for eachtarget in targets10:

        if PLATFORM == NIX:
            command = 'python3 ' + studentPath.name + '/JackAnalyzer.py ' + studentPath.name + '/' + eachtarget       #*NIX platform
        else:
            command = 'python ' + studentPath.name + '\\JackAnalyzer.py ' + studentPath.name + '\\' + eachtarget                  #WIN platform

        try:
            subprocess.run(command, stdin=None, stdout=None, shell=True, check=True)

        except subprocess.CalledProcessError as cpe:
            print(str(studentPath), ':', cpe, 'while compiling', eachtarget )


    print('\n  Translations complete for ' + studentPath.name)

    for eachtarget in targets10:

        resultDirectory = studentPath.name + '/' + eachtarget
        resultDirectory = Path(resultDirectory)

        expectedDirectory = checkFilesPath

        print('\n  Comparing', eachtarget)
        for file in resultDirectory.iterdir():
            found = False

            if file.suffix == '.xml':
                found = True

                result = open(str(file), 'r')

                expectedFileName = str( expectedDirectory / eachtarget / file.name )
                expected = open(expectedFileName, 'r')



                lineNumber = 0
                expectedLine = expected.readline().strip()
                resultLine  = result.readline().strip()
                while resultLine and expectedLine:
                    lineNumber += 1

                    if expectedLine != resultLine:
                        print('bad comparison', str(file.stem), 'your results file line', lineNumber)
                        expected.close()
                        result.close()
                        return

                    expectedLine = expected.readline().strip()
                    resultLine  = result.readline().strip()

                expected.close()
                result.close()
                print('    good:' , str(file.stem))


            elif file.is_dir:
                found = True

        if not found:
            print(' No file to translate')


    print('\n', studentPath.name, 'done\n\n\n')





def testMilestone11(studentPath, checkFilesPath):


    #move existing .xml files
    for eachtarget in targets11:

        if PLATFORM == NIX:
            resultDirectory = studentPath.name + '/' + eachtarget
            newDir = resultDirectory + '/' +  'oldFiles'
        else:
            resultDirectory = studentPath.name + '\\' + eachtarget    #WIN platform
            newDir = resultDirectory + '\\' +  'oldFiles'

        resultDirectory = Path(resultDirectory)
        newDirPath = Path(newDir)
        if not newDirPath.exists():
            os.mkdir(newDir)

        for file in resultDirectory.iterdir():
            if file.suffix == '.xml':
                if PLATFORM == NIX:
                    newName = newDir + '/' + file.name
                else:
                    newName = newDir + '\\' + file.name    #WIN platform

                shutil.move( str(file)  , str(newName) )

    print('\n  xml moves complete for ' + studentPath.name)


    #run the project code
    for eachtarget in targets11:

        if PLATFORM == NIX:
            command = 'python3 ' + studentPath.name + '/JackAnalyzer.py ' + studentPath.name + '/' + eachtarget       #*NIX platform
        else:
            command = 'python ' + studentPath.name + '\\JackAnalyzer.py ' + studentPath.name + '\\' + eachtarget                  #WIN platform

        try:
            subprocess.run(command, stdin=None, stdout=None, shell=True, check=True)

        except subprocess.CalledProcessError as cpe:
            print(str(studentPath), ':', cpe, 'while compiling', eachtarget )


    print('\n  Translations complete for ' + studentPath.name)

    for eachtarget in targets11:

        resultDirectory = studentPath.name + '/' + eachtarget
        resultDirectory = Path(resultDirectory)

        expectedDirectory = checkFilesPath

        print('\n  Comparing', eachtarget)
        for file in resultDirectory.iterdir():
            found = False

            if file.suffix == '.xml' or file.suffix == '.vm':
                found = True

                result = open(str(file), 'r')

                expectedFileName = str( expectedDirectory / eachtarget / file.name )
                expected = open(expectedFileName, 'r')

                lineNumber = 0
                expectedLine = expected.readline().strip()
                resultLine  = result.readline().strip()
                while resultLine and expectedLine:
                    lineNumber += 1

                    if expectedLine != resultLine:
                        print('bad comparison', str(file.stem), 'your results file line', lineNumber)
                        expected.close()
                        result.close()
                        return

                    expectedLine = expected.readline().strip()
                    resultLine  = result.readline().strip()

                expected.close()
                result.close()
                print('    good:' , str(file.name))


            elif file.is_dir:
                found = True

        if not found:
            print(' No file to translate')


    print('\n', studentPath.name, 'done\n\n\n')








#############################################################
#############################################################
#############################################################


if __name__ == '__main__':

    projectNum = '01'
    tests01 = [ 'And.', 'And16.', 'DMux.', 'DMux4Way.', 'DMux8Way.', 'Mux.', 'Mux4Way16.',
              'Mux8Way16.', 'Mux16.', 'Not.', 'Not16.', 'Or.', 'Or8Way.', 'Or16.', 'Xor.']

    tests02 = [ 'Add16.', 'ALU-nostat.', 'ALU.', 'FullAdder.', 'HalfAdder.', 'inc16.']

    tests03 = { 'a':['Bit.', 'PC.', 'RAM8.', 'RAM64.', 'Register.'],
                'b':['RAM4K.', 'RAM16K.', 'RAM512.'] }


    tests05 = [ 'ComputerAdd-external.', 'ComputerAdd.', 'ComputerMax-external.', 'ComputerMax.',
              'ComputerRect-external.', 'ComputerRect.', 'CPU-external.', 'CPU.'] # , 'Memory.'

    tests07 = [ '/StackArithmetic/SimpleAdd/SimpleAdd', '/StackArithmetic/StackTest/StackTest',
                '/MemoryAccess/BasicTest/BasicTest',    '/MemoryAccess/PointerTest/PointerTest',
                '/MemoryAccess/StaticTest/StaticTest']

    targets07 = [ 'StackArithmetic/SimpleAdd', 'StackArithmetic/StackTest',
                'MemoryAccess/BasicTest',    'MemoryAccess/PointerTest',
                'MemoryAccess/StaticTest']

    tests08 = [ '/ProgramFlow/BasicLoop/BasicLoop', '/ProgramFlow/FibonacciSeries/FibonacciSeries',
                '/FunctionCalls/SimpleFunction/SimpleFunction', '/FunctionCalls/NestedCall/NestedCall',
                '/FunctionCalls/FibonacciElement/FibonacciElement', '/FunctionCalls/StaticsTest/StaticsTest']

    targets08 = [ 'ProgramFlow/BasicLoop', 'ProgramFlow/FibonacciSeries',
                'FunctionCalls/SimpleFunction', 'FunctionCalls/NestedCall',
                'FunctionCalls/FibonacciElement', 'FunctionCalls/StaticsTest']


    targets10 = ['ExpressionlessSquare', 'ArrayTest', 'Square']

    targets11 = ['Seven', 'ConvertToBin', 'Square', 'Average', 'Pong', 'ComplexArrays']


    tests = {'tests01': tests01, 'tests02': tests02, 'tests03':tests03, 'tests05': tests05}
    singleDepth = ['tests01', 'tests02', 'tests05']

    #start with directory this file is in
    startingDirectory = Path.cwd()

    import argparse
    ap = argparse.ArgumentParser(prog='n2tGradingServer.py')
    ap.add_argument( '--01', action='store_const', const='tests01', dest="project", help='which project is being graded')
    ap.add_argument( '--02', action='store_const', const='tests02', dest="project", help='which project is being graded')
    ap.add_argument( '--03', action='store_const', const='tests03', dest="project", help='which project is being graded')
    ap.add_argument( '--04', action='store_const', const='tests04', dest="project", help='which project is being graded')
    ap.add_argument( '--05', action='store_const', const='tests05', dest="project", help='which project is being graded')
    ap.add_argument( '--06', action='store_const', const='tests06', dest="project", help='which project is being graded')
    ap.add_argument( '--07', action='store_const', const='tests07', dest="project", help='which project is being graded')
    ap.add_argument( '--08', action='store_const', const='tests08', dest="project", help='which project is being graded')
    ap.add_argument( '--10', action='store_const', const='tests10', dest="project", help='which project is being graded')
    ap.add_argument( '--11', action='store_const', const='milestone11', dest="project", help='which project is being graded')

    ap.add_argument( '--w', action='store_const', const='windows', dest="platform", help='which project is being graded')

    args = ap.parse_args()
    whichProject = args.project
    platformToggle = args.platform
    if platformToggle == 'windows':
        PLATFORM = WIN
    else:
        PLATFORM = NIX

    checkFilesPath = startingDirectory / 'zzzzCheckfiles'   #for 06, 10 & 11

    for studentPath in startingDirectory.iterdir():

        if studentPath.is_dir():
            print('\n\ndirectory:', studentPath.name)

            if ('zzzz' not in studentPath.name) and ('tools' not in studentPath.name):
                if whichProject in singleDepth:
                    testResults_01_02_05(studentPath.name, whichProject)
                elif whichProject == 'tests03':
                    testResults_03(studentPath.name)
                elif whichProject == 'tests04':
                    testResults_04(studentPath.name)
                elif whichProject == 'tests06':
                    assemble_06(studentPath, checkFilesPath)
                    compare_06(studentPath, checkFilesPath)
                elif whichProject == 'tests07':
                    testResults_07(studentPath)
                elif whichProject == 'tests08':
                    testResults_08(studentPath)
                elif whichProject == 'tests10':
                    testResults10(studentPath, checkFilesPath)
                elif whichProject == 'milestone11':
                    testMilestone11(studentPath, checkFilesPath)


                else:
                    print('projectName mismatch for', studentPath.name, whichProject)
            else:
                print(studentPath.name, 'skipped for zzzz')





