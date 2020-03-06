class gamsWriter():
    def __init__(self, vh, objectives, constraints, file_name):
        self.vh = vh
        self.objectives = objectives
        self.constraints = constraints
        self.file = open(file_name, 'w')

    def writeObj(self, obj, vh):
        f = self.file
        f.write("$MAXCOL 255\n$OFFDIGIT\n\n")
        f.write("Variables\n")
        f.write(" ")
        
        first = True
        i = 0

        k = len(vh.variables)
        int_vars = list()

        for v in vh.variables:
            if vh.variables[v].type == "int" or vh.variables[v].type == "binary":
                int_vars.append(v)

            if first == True:
                f.write(v)
                first = False
            else :
                f.write(', ' + v)

            if (i+1)%9 == 0 and i != k:
                f.write(',\n ')
                first = True
            i = i + 1

        if first == True:
            f.write('objvar;\n\n\n')
        else :
            f.write(', objvar;\n\n\n')

        #f.write('Integer variables\n')
        #f.write(" ")

        k = len(int_vars) - 1

        first = True
        i = 0
        for v in int_vars:
            if first == True:
                f.write(v)
                first = False
            else :
                f.write(', ' + v)

            if (i+1)%9 == 0 and i != k:
                f.write(',\n ')
                first = True
            i = i + 1


        if first == True:
            f.write('\n\n')
        else :
            f.write(';\n\n')

        ### Write variable bounds
        f.write('* Variable bounds \n')

        for v in vh.variables:
            ub = vh.variables[v].ub
            lb = vh.variables[v].lb
            
            f.write(' '+ v + '.up = ' + str(ub) + ';\n')
            f.write(' ' + v + '.lo = ' + str(lb) + ';\n')

        f.write('\n')


    def printSimpleConstraint(self, vars, coeffs):
        print(coeffs)

        for var in vars:
            for v in var:
                print(v.name)

        print(coeffs)

    def writeConstraints(self, constraints):
        f = self.file

        cons = constraints.constraints
        vh = self.vh

        f.write("Equations\n")

        i = 1
        k = len(cons)
        first = True
        for c in cons:
            for type in ["lhs", "rhs"]:

                if type == "lhs" and cons[c].ub == "Na":
                    continue
                
                if type == "lhs" and cons[c].ub == cons[c].lb:
                    continue

                if type == "rhs" and cons[c].lb == "Na":
                    continue
                
                if first == True:
                    if (type == "rhs" and cons[c].lb == cons[c].ub) or  (cons[c].lb == "Na" or cons[c].ub == "Na"): 
                        f.write(' e' + str(c + 1))
                    else :
                        f.write(' e' + str(c + 1) + '_' + type)
                    first = False
                else:
                    if (type == "rhs" and cons[c].lb == cons[c].ub) or (cons[c].lb == "Na" or cons[c].ub == "Na"):
                        f.write(' ,e' + str(c + 1))
                    else :
                        f.write(' ,e' + str(c + 1) + '_' + type)


                if (i+1)%10 == 0 and i != k:
                    f.write(',\n ')
                    first = True
                i =  i + 1

        if first == True:
            f.write("objequ;\n\n")
        else :
            f.write(", objequ;\n\n")

        f.write(' objequ .. objvar =e= (')
        
        obj = self.objectives

        m = 1
        for i in range(len(obj.vars)):
            if m%5 == 0:
                f.write("\n")
            
            if len(obj.vars[i]) == 1:
                if i == len(obj.vars) - 1:
                    f.write('(( ' + '( ' + str(obj.coeffs[i]) + ') * ' + str(obj.vars[i][0].name) +  ' ))')
                else:
                    f.write('(( ' + '( ' + str(obj.coeffs[i]) + ') * ' + str(obj.vars[i][0].name)  + ' )) + ') 
            else :
                if i == len(obj.vars) - 1:
                    f.write('(( '  + '( ' + str(obj.coeffs[i]) + ') * ' + str(obj.vars[i][0].name) + ' '+ '* ' + str(obj.vars[i][1].name) + ' ))')
                else:
                    f.write('(( '  + '( ' + str(obj.coeffs[i]) + ') * ' + str(obj.vars[i][0].name) +  ' '+ '* ' + str(obj.vars[i][1].name) + ' )) + ') 
                
            m = m + 1

        f.write(');')
        f.write('\n\n')
        
        i = 1
        for c in cons:
            k = 0
            for type in ["lhs", "rhs"]:
                if type == "lhs" and cons[c].ub == "Na":
                    continue

                if type == "lhs" and cons[c].ub == cons[c].lb:
                    continue

                if type == "rhs" and cons[c].lb == "Na":
                    continue

                if (type == "rhs" and cons[c].ub == cons[c].lb) or (cons[c].lb == "Na" or cons[c].ub == "Na"):
                    f.write(' e' + str(c + 1) + " " + '..+1 * ')
                else:
                    f.write(' e' + str(c + 1) + '_' + type + " " + '..+1 * ')

                vars = cons[c].vars
                coeffs = cons[c].coeffs

                #self.printSimpleConstraint(vars, coeffs)

                f.write('(')

                j = 0

                first = True

                ### Rewrite this and check each and every constraint writter
                m = 1
                for var in vars:
                    #print(var[0].name)
                    if m%3 == 0:
                        f.write("\n")
                    m = m + 1
                    if first == False :
                        f.write(' + ((' + str(coeffs[j]) + ')')
                    else :
                        f.write('(' + str(coeffs[j]) + ')')
                        first = False

                    for v in var:
                        f.write(' * (' + str(v.name) + ')')

                    f.write(')')
                    j = j + 1
                                        
                #f.write(') ')

                if cons[c].strict == 's':
                    f.write(' - 0.01 ')
                elif cons[c].strict == 'ss':
                    f.write(' + 0.01 ')

                if type == "lhs":
                    f.write("=l= " + str(cons[c].ub) + ";\n")
                else :
                    if type == "rhs" and cons[c].lb == cons[c].ub:
                        f.write("=e= " + str(cons[c].lb) + ";\n")            
                    else:
                        f.write("=g= " + str(cons[c].lb) + ";\n")            

            i = i + 1
            f.write("\n")

    def writeSolver(self):
        f = self.file
        #f.write("$include initial_values.txt\n\n")
        f.write("Model m / all /;\n\n")
        f.write("m.optfile = 1;\n\n")
        f.write("option limrow = 0;\n")
        f.write("option limcol = 0;\n\n")
        f.write("option reslim=50000;\n")
        f.write("option threads=24;\n")
        f.write("option optcr=0.1;\n")
        f.write("option mip=convert;\n")
        f.write("Solve m using mip minimizing objvar;\n")
        
    def writeOPT(self):
        self.writeObj(self.objectives, self.vh)
        self.writeConstraints(self.constraints)
        self.writeSolver()

    def close(self):
        self.file.close()
