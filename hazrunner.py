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
        while reader < len(rfile):
            if rfile[reader] == "!":
                s = rfile[reader: rfile.index(";", reader)]
                if "=" in s:
                    cvattr = s.split("=")
                    variable_name = cvattr[0].strip()
                    variable_value = cvattr[1].strip()
                    if len(variable_value) > 1 and variable_value[0] == '"' and variable_value[-1] == '"':
                        variable_value = variable_value[1:-1]

                    variables[variable_name] = variable_value
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


            reader+=1
        print("\n\n=====FINISHED=====\n\n")









    

      
