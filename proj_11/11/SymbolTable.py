class SymbolTable(object):

# Constructor
  def __init__(self):
    self.class_level_symbol_table = {}
    self.method_level_symbol_table = {}
    self.CLASS_LEVEL_STATIC_COUNT = 0
    self.CLASSLEVELFIELDCOUNT = 0
    self.METHOD_SCOPE_ARG_COUNTER = 0
    self.METHOD_SCOPE_VAR_COUNTER = 0

  def resetClassLevelTable(self):
    self.CLASS_LEVEL_STATIC_COUNT = 0
    self.CLASSLEVELFIELDCOUNT = 0
    self.class_level_symbol_table = {}


  def startSubroutine(self):
    self.METHOD_SCOPE_ARG_COUNTER = 0
    self.METHOD_SCOPE_VAR_COUNTER = 0
    self.method_level_symbol_table = {}

  def define(self, name, typeOpt, kind):
    if (kind == "static"):
            num = self.CLASS_LEVEL_STATIC_COUNT
            self.class_level_symbol_table[name] = [typeOpt, kind, num]
            self.CLASS_LEVEL_STATIC_COUNT = self.CLASS_LEVEL_STATIC_COUNT+1
    elif(kind == "field"):
            num = self.CLASSLEVELFIELDCOUNT
            self.class_level_symbol_table[name] = [typeOpt, kind, num]
            self.CLASSLEVELFIELDCOUNT = self.CLASSLEVELFIELDCOUNT+1
    elif(kind == "arg"):
            num = self.METHOD_SCOPE_ARG_COUNTER
            self.method_level_symbol_table[name] = [typeOpt, kind, num]
            self.METHOD_SCOPE_ARG_COUNTER = self.METHOD_SCOPE_ARG_COUNTER+1
    else:
            num = self.METHOD_SCOPE_VAR_COUNTER
            self.method_level_symbol_table[name] = [typeOpt, kind, num]
            self.METHOD_SCOPE_VAR_COUNTER = self.METHOD_SCOPE_VAR_COUNTER+1


  def varCount(self):
    return(self.METHOD_SCOPE_VAR_COUNTER)



  def kindOf(self, cmd):
    if(cmd in self.method_level_symbol_table):
      return(self.method_level_symbol_table[cmd][1])
    elif(cmd in self.class_level_symbol_table):
      return(self.class_level_symbol_table[cmd][1])
    else:
      return("why2")

  def typeOf(self, cmd):
    if(cmd in self.method_level_symbol_table):
      return(self.method_level_symbol_table[cmd][0])
    elif(cmd in self.class_level_symbol_table):
      return(self.class_level_symbol_table[cmd][0])
    else:
      return("why3")

  def indexOf(self, cmd):
    if(cmd in self.method_level_symbol_table):
      return(str(self.method_level_symbol_table[cmd][2]))
    elif(cmd in self.class_level_symbol_table):
      return(str(self.class_level_symbol_table[cmd][2]))
    else:
      return("why1")

  def generateTag():
    pass

  def methodTable(self):
    return(self.method_level_symbol_table)

  def classTable(self):
    return(self.class_level_symbol_table)

