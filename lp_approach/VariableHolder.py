### Defines all the variables required
### Also a variable holder for all the variables

class Variable():
    def __init__(self, name, lb, ub, type):
        self.name = name
        self.lb = lb
        self.ub = ub
        self.type = type
        self.cons_id = list()
        self.value = 0

    def __hash__(self):
        return hash(self.name)

    
class intVariable(Variable):
    def __init__(self, name, ub, lb):
        Variable.__init__(self, name, ub, lb, "int")
        

class realVariable(Variable):
    def __init__(self, name, ub, lb):
        Variable.__init__(self, name, ub, lb, "real")

class binaryVariable(Variable):
    def __init__(self, name):
        Variable.__init__(self, name, 0, 1, "binary")


### Introduce all variables here
### Will be helpful to know all

class VariableHolder():
    def __init__(self):
        self.variables = dict()
    
    def getVariableEdit(self, type, name, lb, ub):
        if name in self.variables:
            self.variables[name].lb = lb
            self.variables[name].ub = ub
            return self.variables[name]
        else :
            v = self.getVariable(type, name, lb,ub)
            return v

    def getVariable(self, type, name, lb = 0, ub = 1):
        if name in self.variables.keys():
            return self.variables[name]


        elif type == 'w' or type == 'e' :
            v = realVariable(name, lb, ub)
            self.variables[name] = v
            return v
        

        #### a variables specify if a flow is active at a particular time
        elif type == 'a' or type == 'b' or type == 'q' or type == "s" or type == "q" or type == 'm' or type == 'l' or type == 'x'  or type == 'v' or type =='d': 
            v = binaryVariable(name)
            self.variables[name] = v
            return v

        
        elif type == 'f':
            v = intVariable(name, lb, ub)
            self.variables[name] = v
            return v

        elif type == 's' or type == 'r' or type=='n'  or type== 'k' or type=='i' or type == 'j'  or type == 'm' or type == 'p' or type == 'rn' or type == 'rb' or type == 'ra' or type == 'z' or type == 'x' or type == 'e' or type == 'z':
            v = intVariable(name, lb, ub)
            self.variables[name] = v
            return v

 #       elif type == 's' or type == 'x' or type == 'z' or type == 'k' or type == 'e' or type == 'p':

        asdf
        print("missing variable type")

        

    
            

