import gdb

def isint(valvarname):
    try:
      if valvarname == int(valvarname):
         return True
      else:
         return False
    except (ValueError, TypeError):
      return False
    
def isstring(valvarname):
    try:
      if valvarname == string(valvarname):
         return True
      else:
         return False
    except (ValueError, TypeError):
      return False
    
def isfloat(valvarname):
    try:
      if valvarname == float(valvarname):
         return True
      else:
         return False
    except (ValueError, TypeError):
      return False
    
def ischar(valvarname):
    try:
      if valvarname[0] == valvarname:
         return True
      else:
         return False
    except (ValueError, TypeError):
      return False


    

gdb.addt('prefuncs')
gdb.addt('defuncs')
variables = {}

gdb.insertvtt('#printlin', 'prefuncs', False)
gdb.insertvtt(print, 'prefuncs', False)
gdb.insertvtt('manargs', 'prefuncs', False)
gdb.insertvtt(1, 'prefuncs', False)
gdb.insertvtt(False, 'prefuncs', False)

gdb.insertvtt('#getlin', 'prefuncs', False)
gdb.insertvtt(input, 'prefuncs', False)
gdb.insertvtt('manargs', 'prefuncs', False)
gdb.insertvtt(1, 'prefuncs', False)
gdb.insertvtt(True, 'prefuncs', False)

gdb.insertvtt('#isint', 'prefuncs', False)
gdb.insertvtt(isint, 'prefuncs', False)
gdb.insertvtt('manargs', 'prefuncs', False)
gdb.insertvtt(1, 'prefuncs', False)
gdb.insertvtt(True, 'prefuncs', False)

gdb.insertvtt('#isstring', 'prefuncs', False)
gdb.insertvtt(isstring, 'prefuncs', False)
gdb.insertvtt('manargs', 'prefuncs', False)
gdb.insertvtt(1, 'prefuncs', False)
gdb.insertvtt(True, 'prefuncs', False)

gdb.insertvtt('#isfloat', 'prefuncs', False)
gdb.insertvtt(isfloat, 'prefuncs', False)
gdb.insertvtt('manargs', 'prefuncs', False)
gdb.insertvtt(1, 'prefuncs', False)
gdb.insertvtt(True, 'prefuncs', False)

gdb.insertvtt('#ischar', 'prefuncs', False)
gdb.insertvtt(ischar, 'prefuncs', False)
gdb.insertvtt('manargs', 'prefuncs', False)
gdb.insertvtt(1, 'prefuncs', False)
gdb.insertvtt(True, 'prefuncs', False)

def gettype(value):
            try:
              if value[0] == '"':
                if value[len(value) -1] == '"':
                  return 'String'
                else:
                  return 'Raw'
              elif isinstance(value, int):
                return 'Int'
              elif isinstance(value, float):
                  return 'Float'
              elif value[0] == '#':
                testtgvt = value.split('(')
                if testtgvt[1][0] == '(' and len(testtgvt[1] -1) == ')':
                  return 'FuncRef'
                else:
                  return 'FuncKey'
              elif value[0] == '!':
                return 'OtherVar'
              elif value[0] == '[':
                if value[len(value) -1] == ']':
                  return 'Array'
                else:
                  return 'Raw'
              elif value[0] == '@':
                if value[1] == '{' and value[len(value) -1] == '}':
                  return 'Def'
                else:
                  return 'Raw'
              else:
                return 'Raw'
              #end
            except (IndexError, ValueError, TypeError):
              pass




print('type help to get list of commands')
functionkey = '#'
variablekey = '!'
definefunctionkey = '@'
keywordkey = '$'
codea = []
#TYPE LIST!!!!!!!!!!!!!!!!!
types = ['OtherVar', 'String', 'Int', 'Float', 'Raw', 'Array', 'FuncRef', 'FuncKey', 'Def']


try:
  while True:
    print('hazrunner>', end='', flush=True)
    command = input('')
    if command == 'help':
      print('hazr COMMANDS:')
      print('-r: runs a file. Type hazr -r, then you will be prompted to give either a file path or name\n (Depending whether or not the haz file is in the same dir \n as the runner, which it should be, for convenience. )')
      print('\n')
      print('-sc: shows the contents of a file. Type hazr -sc')
    elif command == 'hazr -sc':
      
      
      print('hazrunner>filename/path?> ', end='', flush=True)
      command = input('')
      try:
        with open(command, 'r') as f:
          code = f.read()
        print(code)
        
      except:
        print('FILE NOT FOUND ERROR!')
    elif command == 'hazr -r':
    
      print('hazrunner>filename/path?> ', end='', flush=True)
      command = input('')
      with open(command, 'r') as f:
        code = f.read()
      counter = 0
      letter = code[counter]
      while counter < len(code):
        #handle variable declarations

        
        if letter == variablekey:
          string = code[counter:code.index(';', counter)]
          if '=' in string:
                        var_name, var_value = string.split('=')
                        variables[var_name.strip()] = var_value.strip()
        #handle functions
        elif letter == functionkey:
          openingparentheses = code.index('(', counter)
          funcname = code[counter: openingparentheses]

          if funcname in gdb.db[gdb.db.index('prefuncs'):gdb.db.index('endtab;', gdb.db.index('prefuncs'))]:
            index = gdb.db.index(funcname) + 1
            actualfunction = gdb.db[index] 
            args = []

            argam = 0
            subcounter = code.index('(', counter)
            subletter = code[subcounter]
            arg_string = code[subcounter + 1: code.index(')', counter)]
            ends = len(arg_string)
            args = arg_string.split(',')
            subcounter2 = 0          
            subletter2 =  args[subcounter2]
            string2 = code[subcounter2 + 1:code.index(')', counter)]
            #add to after *1
            
            #*1
            
            


            for i, arg in enumerate(args):
              if gettype(arg) == 'OtherVar':
                  var_name = arg.strip()  
                  if var_name in variables:
                      args[i] = variables[var_name]
                  else:
                      print(f'ERROR {var_name} NOT FOUND!')

              if gettype(arg) == 'FuncRef':
                if gdb.db[gdb.db.index(arg) + 5] == True:
                    argsoa = arg.split('(')
                    two = argsoa[1]
                    argsoa = two.split(',')
                    argsoa[0] = argsoa[0].split('(')
                    argsoa[len(argsoa) - 1].split(')')
                    try:
                        var1234 = arg(*args)
                    except Exception as e:
                        print(f"Error: {e}")
                        args[i] = var1234
                            

            actualfunction(*args)

          elif funcname in gdb.db[gdb.db.index('defuncs'):gdb.db.index('endtab;', gdb.db.index('defuncs'))]:
            pass
          else:
            print(f'FUNCTION {funcname} NOT FOUND!')
          
        codea.append(letter)
        counter += 1
        if counter < len(code):  
          letter = code[counter]
    

except KeyboardInterrupt:
  pass




    

      
