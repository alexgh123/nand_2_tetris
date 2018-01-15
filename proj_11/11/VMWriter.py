from JTConstants import *

class VMWriter(object):





# Constructor
  def __init__(self):
      self.vmCommands = []

  def writePush(self, segment, index):
    string = "push " + segment + " " + index
    return([string])

  def writePop(self, segment, index):
    string = "pop " + segment + " " + index
    return([string])

  def writeArithmetic(self, cmd):
    if((cmd == "*") | (cmd == "/")):
      string = "call " + BINARY_OPERATORS[cmd] + " 2"
    else:
      string = BINARY_OPERATORS[cmd]
    return([string])

  def writeUnaryOpp(self, cmd):
    return([UNARY_OPERATORS[cmd]])

  def WriteLabel(self, label):
    return("label " + label)

  def WriteGoto(self, label):
    return("goto " + label)

  def WriteIf(self, label):
    return("if-goto " + label)

  def writeCall(self, name, nArgs):
    string = "call " + name + " " + str(nArgs)
    return([string])

  def writeFunction(self, name, nLocals):
    return([name + " " + str(nLocals)])

  def writeReturn(self):
    return(["return"])
