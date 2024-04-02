variables = {}
defuncs = {}
prefuncs = {}

reader = 0
fil = ""


prefuncs.update({"#println": print})
prefuncs.update({"#getln": input})

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
                    if statearr[counter][0] == "!":
                        statearr[counter] = statearr[counter].strip()
                        statearr[counter] = variables.get(statearr[counter])
                        statestr = statestr + statearr[counter]
                        counter+=1
                    else:
                        statestr = statestr + statearr[counter]
                        counter+=1
                if eval(statestr):
                    do = rfile[rfile.index("{", reader)+1:rfile.index("|", reader)]
                    if do in prefuncs:
                        argsff = rfile[rfile.index("|", reader)+1:rfile.index("}", reader)].split(",")
                        
                       

                        checkfstringc = 0
                        while checkfstringc < len(argsff):
                            if argsff[checkfstringc][0] == '"' and argsff[checkfstringc][len(argsff[checkfstringc])-1] == '"':
                                argsff[checkfstringc] = argsff[checkfstringc][1:len(argsff)-2]
                                checkfstringc+=1
                            elif argsff[checkfstringc][0] == '!':
                                argsff[checkfstringc] = variables.get(argsff[checkfstringc])
                                checkfstringc+=1
                        prefuncs.get(do)(*argsff)




                    else:
                        print(do)
                    
                else:
                    print("Nae!")

                

                finish("}/end")
            
            if rfile[reader] == "!":
                s = rfile[reader: rfile.index(";", reader)]
                if "=" in s:
                    cvattr = s.split("=")
                    variable_name = cvattr[0].strip()
                    variable_value = cvattr[1].strip()
                    if len(variable_value) > 1 and variable_value[0] == '"' and variable_value[-1] == '"':
                        variable_value = variable_value[1:-1]

                    variables[variable_name] = variable_value
                    finish(";")
                
                        
                
                
                

            
            if rfile[reader] == "#":

                name = rfile[reader:rfile.index("(", reader)]
                gargs = rfile[rfile.index('(', reader)+1:rfile.index(')', reader)]

                gargsarr = gargs.split(',')
                checkfstringc = 0
                while checkfstringc < len(gargsarr):
                    if gargsarr[checkfstringc][0] == '"' and gargsarr[checkfstringc][len(gargsarr[checkfstringc])-1] == '"':
                        gargsarr[checkfstringc] = gargsarr[checkfstringc][1:len(gargsarr)-2]
                        checkfstringc+=1
                    elif gargsarr[checkfstringc][0] == '!':
                        gargsarr[checkfstringc] = variables.get(gargsarr[checkfstringc])
                        checkfstringc+=1

                if name in prefuncs:
                    prefuncs[name](*gargsarr)
                finish(";")


            reader+=1
        print("\n=====FINISHED=====\n")












    

      
