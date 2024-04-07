variables = {}
defuncs = {}
prefuncs = {}

reader = 0
fil = ""

#predefined hazmat-specific functions:

def printnoend(args):
  print(args, end="")
def saymoo(ms, os):
    for i in range(ms):
        print("M", end="", flush=True)
    for i in range(os):
        print("O", end="", flush=True)
    print("")

  


prefuncs.update({"#println": print})
prefuncs.update({"#getln": input})
prefuncs.update({"#print":printnoend})
prefuncs.update({"#moo":saymoo})

variables = {"x": 5, "y": "hello", "z": 3.14, "flag": True}

def gtype(val):
    global variables
    
    if val.startswith('"') and val.endswith('"'):
        return val[1:-1]

    elif val.startswith('!'):
        if val in variables:
            return variables[val]
        else:
            return "variable not found"

    elif val.isdigit():
        return int(val)
    elif val.replace('.', '', 1).isdigit():
        return float(val)
    elif val.lower() in ['true', 'false']:
        return bool(val)

    return "unknown"



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
            try:
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
            except Exception as e:
                exception_type = type(e).__name__
                
                print("\n")
                magicnumber=18
                print(rfile[reader:reader+magicnumber])
                for i in range(magicnumber):
                    if i>len(rfile):
                        break;
                    else:
                        print("^", end="", flush=True)
                print("\n")
                print(f"{exception_type} error at char {reader}.")
                break;
                


            reader+=1
           
        print("\n=====FINISHED=====\n")









