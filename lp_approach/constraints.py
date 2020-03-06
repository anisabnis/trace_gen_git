import copy
import bisect

class objBuilder:
    def __init__(self, variableHolder):
        self.vh = variableHolder
        self.vars = list()
        self.coeffs = list()

                        
class Constraint:
    id = 0

    def __init__(self, lb, ub, vars, coeffs, rewrite='',strict = ''):

        self.id = Constraint.id
        
        Constraint.id = Constraint.id + 1
        
        self.ub = ub

        self.lb = lb

        self.vars = vars

        self.coeffs = coeffs

        self.strict = strict

        if rewrite == '':
            self.rewrite = False
        else :
            self.rewrite = True

        if strict == 'c' :
            self.updateVariables()
            
        self.lhs_dual_var = 0
        self.rhs_dual_var = 0


class ConstraintBuilder():
    def __init__(self, vh, obj, trace):
        self.vh = vh
        self.obj = obj
        self.trace = trace
        self.constraints = dict()
        self.writeConstraints()
        

    def writeConstraints(self):
        
        count = 0
        count1 = 0

        for i in range(len(self.trace)):

            obj = self.trace[i]

            nxt_ts = obj[2]
            obj_id = obj[1]

            if nxt_ts <= 0:
                count1 += 1
                continue
            
            req_trace = self.trace[i+1:]

            index = bisect.bisect_left(req_trace, [nxt_ts, 0, 0, 0])

            index = i + index
            
            uniq_objects = set()
            uniq_bytes = 0

            found = False

            for j in range(index-1, len(self.trace)):
                if self.trace[j][1] == obj_id:
                    uniq_bytes = self.trace[i][3]
                    found = True
                    break
                else:
                    not_found = True

            if found == False:
                count1 += 1
                continue


            #print("index : ", index, " i : ", i, " j : ", j, "nxt_ts : ", nxt_ts )

            for ii in range(i, j+1):
                n_obj_id = self.trace[ii][1]                
                uniq_objects.add(n_obj_id)

            w_vars = []
            coeffs = []

            for obj in uniq_objects:
                w_var = self.vh.getVariable('w', 'w_' + str(obj), 0, 100000000)
                w_vars.append([w_var])
                coeffs.append(1)


            if len(w_vars) <= 0:
                count1 += 1
                continue

            e_var = self.vh.getVariable('e', 'e_' + str(count), 0, 10000000)
            count += 1

            self.obj.vars.append([e_var])
            self.obj.coeffs.append(1)

            w_vars_copy = copy.deepcopy(w_vars)
            coeffs_copy = copy.deepcopy(coeffs)


            w_vars.append([e_var])
            coeffs.append(1)
            cons = Constraint(uniq_bytes, "Na", w_vars, coeffs)
            self.constraints[cons.id] = cons
            
            w_vars_copy.append([e_var])
            coeffs_copy.append(-1)
            cons = Constraint("Na", uniq_bytes, w_vars_copy, coeffs_copy)
            self.constraints[cons.id] = cons
            
        print("Number of constraints missed ", count1, count)
            
    
