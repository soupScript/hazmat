variables = {}
defuncs = {}
prefuncs = {}

reader = 0
fil = ""

#predefined hazmat-specific functions:

def printnoend(args):
  print(args, end="")
  


prefuncs.update({"#println": print})
prefuncs.update({"#getln": input})
prefuncs.update({"#print":printnoend})

def gtype(val):
    if len(val) > 1 and val[0] == '"' and val[-1] == '"':
                        val = str(val)[1:-1]
                        return val
    elif "." not in val and val != 'True' and val != 'False' and val.strip()[0] != '!': 
        try:
            val = int(val)
            return val
        except:
            print("TYPE ERROR!!!int")
            return val
    elif "." in val and val != 'True' and val != 'False' and val[0] != '!':
        try:
            val = float(val)
            return val
        except:
            #print("TYPE ERROR!!!float")
            return val
    elif val == 'True' or val == 'False':
        if val == 'True':
            val = True
            return val
        else:
            val = False
            return val
    elif val.strip()[0] == '!':
        return variables.get(val)
    else:
         print("TYPE ERROR!!!else")
         return val
        
    

while fil != "end" and fil != "^C":
    fil = input("")
    if fil.strip() == "hazr -r":
        print("Filename or path?: ", end="", flush=True)
        fil = input("")
        with open(fil, 'r') as f:
            rfile = f.read()
        def finish(keywd):
            global reader
            reader = rfile.index(keywd, reader)
            
        
        while reader < len(rfile):
            if rfile[reader] == "?":
                statement = rfile[reader+1:rfile.index("{", reader)]
                statearr = statement.split("~")
                statestr = ""
                counter = 0
                while counter < len(statearr):
                    if statearr[counter] != statearr[1]:
                        statearr[counter] = gtype(statearr[counter])
                        statestr = statestr+ f"{statearr[counter]}"
                        counter+=1
                    else:
                         statestr = statestr+ f"{statearr[counter]}"
                         counter+=1
                if eval(statestr):
                    do = rfile[rfile.index("{", reader)+1:rfile.index("|", reader)]
                    if do in prefuncs:
                        argsff = rfile[rfile.index("|", reader)+1:rfile.index("}", reader)].split(",")
                        checkfstringc = 0
                        while checkfstringc < len(argsff):
                            argsff[checkfstringc] = gtype(argsff[checkfstringc])
                            checkfstringc+=1
                        prefuncs.get(do)(*argsff)
                    else:
                        pass
                        #IF DO IN DEFUNCS
                    
                else:
                    if "else{" in rfile:
                        finish("else{")
                        do = rfile[rfile.index("{", reader)+1:rfile.index("|", reader)]
                        if do in prefuncs:
                            argsff = rfile[rfile.index("|", reader)+1:rfile.index("}", reader)].split(",")
                            checkfstringc = 0
                            while checkfstringc < len(argsff):
                                argsff[checkfstringc] = gtype(argsff[checkfstringc])
                                checkfstringc+=1
                            prefuncs.get(do)(*argsff)
                        else:
                            pass#IF DO IN DEFUNCS


                

                finish("};")
            
            if rfile[reader] == "!":
                s = rfile[reader: rfile.index(";", reader)]
                if "=" in s:
                    cvattr = s.split("=")
                    variable_name = cvattr[0].strip()
                    variable_value = cvattr[1].strip()
                    variable_value = gtype(variable_value)

                    


                    if variable_name not in variables:
                         variables.update({variable_name:variable_value})
                    else:
                        variables[variable_name]=variable_value
                    finish(";")
                
                        
                
                
                

            
            if rfile[reader] == "#":

                name = rfile[reader:rfile.index("(", reader)]
                gargs = rfile[rfile.index('(', reader)+1:rfile.index(')', reader)]

                gargsarr = gargs.split(',')
                checkfstringc = 0
                while checkfstringc < len(gargsarr):
                    gargsarr[checkfstringc] = gtype(gargsarr[checkfstringc])
                    checkfstringc+=1

                if name in prefuncs:
                    prefuncs[name](*gargsarr)
                finish(";")


            reader+=1
        print("\n=====FINISHED=====\n")















    

      
