import sys
from gamsWriter import *
from constraints import *
from VariableHolder import *

class lp:
    def __init__(self, trace):

        self.trace = trace
        self.vh = VariableHolder()
        self.obj = objBuilder(self.vh)        
        self.constraints = ConstraintBuilder(self.vh, self.obj, self.trace)
        
        g_writer = gamsWriter(self.vh, self.obj, self.constraints, "lp.gams")
        g_writer.writeOPT()
        g_writer.close()

 
