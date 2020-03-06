import random
import math
from collections import defaultdict

class Tree:
    def __init__(self, id):
        self.id = id
        self.children = list()
        self.plr = list()
        self.is_nary = False 

    def leafs(self):
        if len(self.children) == 0:
            return [self]
        else:
            return [d for c in self.children for d in c.leafs()]


def printTree(tree):
    if len(tree.children) == 0:
        return
    print(tree.id + ' ' + ':'.join([c.id for c in tree.children]))
    return [printTree(c) for c in tree.children]


def intersect(a, b):
    return list(set(a) & set(b))


class objBuilder():
    def __init__(self, vertices, variableHolder, distances, correlations, path):
        self.vh = variableHolder
        self.vertices = vertices
        self.vars = list()
        self.coeffs = list()
        self.d = distances
        self.c = correlations
        self.path = path
        self.build()

    ### Add variables for the tree constraints for every edge
    def readTrees(self):
        trees = dict()
        paths = open(self.path + '/orig_path.txt', 'r')
        for p in paths:
            p = p.strip().split(' ')
            s = p[0]
            t = p[-1]
            
            if s not in trees:
                trees[s] = Tree(s)
                
            root = trees[s]
            curr_node = root

            for r in p[1:]:
                found = False
                if r in [c.id for c in curr_node.children]:
                    for c in curr_node.children:
                        if r == c.id:
                            curr_node = c
                            break
                else:
                    new_node = Tree(r)
                    curr_node.children.append(new_node)
                    curr_node = new_node
            
        paths.close()
        tree_children = trees[s].children
        x = tree_children[0]
        return trees


    def condense_trees(self,trees):
        for s in trees:
            tree = trees[s]
            pairs = list()
            for c in tree.children:
                pair = ((c, tree))
                pairs.append(pair)

            while len(pairs) > 0:
                p = pairs.pop(0)
                np = p[0]
                if len(p[0].children) == 1:
                    p[1].children = [ c for c in p[1].children if c.id != p[0].id]
                    p[1].children.extend(p[0].children)
                    np = p[1]
                for c in p[0].children:
                    pairs.append((c, np))

    def build(self):
        #pass
        for d in self.d:
            src = d[0]
            dst = d[1]
            distance = self.d[d][0]
            z_var = self.vh.getVariable('z', 'z_' + src + '_' + dst, 2, 12)
            self.vars.append([z_var])
            self.coeffs.append(1)


                        
class Constraint():
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


    ## Every variable has information about which constraints hold 
    ## the variable
    def updateVariables(self):
        for var_pair in self.vars:
            for var in var_pair:
                var.cons_id.append(self.id)


class ConstraintBuilder():
    def __init__(self, vertices, enclaves, correlations, distances, variable_holder, dir, obj, rd, no_trees):
        self.v = vertices
        self.e = enclaves
        self.c = correlations
        self.d = distances
        self.vh = variable_holder
        self.path = dir
        self.a = {}
        self.rd = rd
        self.ntrees = int(no_trees)

        for v in self.v:
            self.a[v] = self.v

        self.obj = obj

        self.labels = defaultdict(lambda: defaultdict(int))

        self.constraints = dict()

        self.edgeweight = dict()

        self.Trees = self.parseTrees()

        ## egress edge constraints
        self.egressConstraint()

        ## if the edge is in any source tree it is in the graph
        self.edgeExistsConstraint() 

        self.srcTreeConstraints()

        self.bidirectionaledges()

        self.rdConstraints()

        #self.rdConstraintsWithError()
        #self.distance()

        ## there should be no cycles in the graph
        ## distance is incremented
        ## helps find unique paths between src and dst and makes path bidirectional

        self.cycleConstraints()
        ## ensures there exists a tree from each source and
        ## every source has a path to the destination

        self.buildPathConstraints()

#        self.treeConstraints()

        ## Covariance trees
        self.covarianceTreeConstraints()

        #self.pathCorrectness()
        self.destinationTreeConstraints()
        
        #self.fixVariables()


    def distance(self):
        for d in self.d:
            src = d[0]
            dst = d[1]
            distance = self.d[d][0]
            z_var = self.vh.getVariable('z', 'z_' + src + '_' + dst, 2, 12)

            c = Constraint(int(distance) - 2, int(distance) + 2, [[z_var]], [1])
            self.constraints[c.id] = c            

    def parseTrees(self):
        trees = self.readTrees()
        self.condense_trees(trees)
        return trees


    def fixVariables(self):
        src_paths = defaultdict(list)
        dst_paths = defaultdict(list)

        paths = open(self.path + '/orig_path.txt', 'r')

        refined_paths = []
        routers = defaultdict()
        x = 0
        for l in paths:
            l = l.strip().split(' ')
            s = l[0]
            d = l[-1]
            

            for i in range(len(l) - 1):
                r = l[i]
                if i == 1:
                    routers[r] = s + '1'
                elif i == len(l) - 2:
                    routers[r] = d + '1'
                elif i == 0:
                    routers[r] = r
                elif r not in routers:
                    routers[r] = 'x' + str(x)
                    x += 1

        paths.close()

        paths = open(self.path + '/orig_path.txt', 'r')

        for l in paths:
            l = l.strip().split(' ')
            path = []
            for i in range(len(l)):
                r = l[i]
                path.append(routers[r])

            refined_paths.append(path)


        f = open(self.path + '/o_path.txt', 'w')
        for p in refined_paths:
            f.write(' '.join(p))
            f.write('\n')
        f.close()

        for l in refined_paths:
            src = l[0]
            dst = l[-1]

            src_paths[src].append(l)
            dst_paths[dst].append(l)

        for s in src_paths:
            for p in src_paths[s]:
                s = p[0]
                d = p[-1]
                ## fill s vars
                for i in range(len(p) - 1):
                    print("svar : " , 's_' + str(p[i]) + '_' + str(p[i+1]) + '_' + str(s))
                    s_var = self.vh.getVariableEdit('s',  's_' + str(p[i]) + '_' + str(p[i+1]) + '_' + str(s), 1, 1)
                    if i >= 2:
                        print('z_' + str(p[i]) + '_' + str(s))
                        #z_var = self.vh.getVariableEdit('z', 'z_' + str(p[i]) + '_' + str(s), i, i)
                    
                    #v_var = self.vh.getVariableEdit('v', 'v_' + str(p[i]) + '_' + str(s) + '_' + str(d), 1, 1)


        for d in dst_paths:
            for p in dst_paths[d]:
                for i in range(len(p) - 1):
                    #d_var = self.vh.getVariableEdit('d', 'd_' + str(p[i]) + '_' + str(p[i+1]) + '_' + str(d), 1, 1)
                    pass
                                                       

    def bidirectionaledges(self):
        for v1 in self.v:
            for v2 in self.v:
                if v1 <= v2:
                    continue
                
                w1_var = self.vh.getVariable('w' , 'w_' + str(v1) + '_' + str(v2), 0, 1)
                w2_var = self.vh.getVariable('w', 'w_' + str(v2) + '_' + str(v1), 0, 1)

                x_var = self.vh.getVariable('x' , 'x_' + str(v1) + '_' + str(v2), 0, 1)

                c = Constraint(0, "Na", [[x_var], [w1_var], [w2_var]], [1, -1, 1])
                self.constraints[c.id] = c

                c = Constraint(0, "Na", [[x_var], [w2_var], [w1_var]], [1, -1, 1])
                self.constraints[c.id] = c

                self.obj.vars.append([x_var])
                self.obj.coeffs.append(5)

                self.obj.vars.append([w1_var])
                self.obj.coeffs.append(5)


    def destinationTreeConstraints(self):
        ## Destination tree rules
        print("destination tree rulse ")
        for e in self.e:
            for i in [v for v in self.v if v not in self.e]:
                d_vars = list()
                for j in [v for v in self.v if v not in self.e]:
                    if j == i:
                        continue

                    d_var = self.vh.getVariable('d', 'd_' + str(i) + '_' + str(j) + '_' + str(e))
                    d_vars.append([d_var])
                    
                cons = Constraint(0, 1, d_vars, [1] * len(d_vars))
                self.constraints[cons.id] = cons

    
        ## Write the egress destination constraints
        for e1 in self.e:
            d_var = self.vh.getVariable('d', 'd_' + e + "1_" + str(e1) +  "_" + str(e1))
            c = Constraint(1, 1, [[d_var]], [1])
            self.constraints[cons.id] = c

            for e2 in self.e:
                if e2 == e1:
                    continue

                d_var = self.vh.getVariable('d', 'd_' + str(e2) + '_' + str(e2) + '1' + '_' + str(e1) , 0, 1)
                c = Constraint(1,1, [[d_var]], [1])
                self.constraints[cons.id] = c
                

        ## Write which d vars get a value of 1
        count = 1
        for d in self.e:
            for i in self.v:
                for j in self.v:
                    if i == j:
                        continue

                    k_vars = []
                    k_coeffs = []

                    for s in self.e:
                        if s == d:
                            continue

                        k_var = self.vh.getVariable('k' , 'k_' + str(count), 0, 1)
                        count += 1

                        s_var = self.vh.getVariable('s', 's_' + str(i) + '_' + str(j) + '_' + str(s), 0, 1)
                        v_var = self.vh.getVariable('v', 'v_' + str(j) + '_' + str(s) + '_' + str(d), 0, 1)
                        
                        
                        c = Constraint("Na", 0, [[k_var], [s_var]], [1, -1])
                        self.constraints[c.id] = c

                        c = Constraint("Na", 0, [[k_var], [v_var]], [1, -1])
                        self.constraints[c.id] = c

                        c = Constraint(-1, "Na", [[k_var], [s_var], [v_var]], [1 , -1, -1])
                        self.constraints[c.id] = c

                        k_vars.append([k_var])
                        k_coeffs.append(1)

                    d_var = self.vh.getVariable('d', 'd_' + str(i) + '_' + str(j) + '_' + str(d), 0 ,1)
                    k_vars.append([d_var])
                    k_coeffs.append(-1 * len(k_vars) - 1)

                    c = Constraint(-1 * len(k_vars), 0, k_vars, k_coeffs)
                    self.constraints[c.id] = c
                                                                                                
    def buildPathConstraints(self):
        count = 0
        for s in self.e:                
            for d in self.e:
                if s == d:
                    continue

                v_var = self.vh.getVariable('v', 'v_' + str(s) + '_' +  str(s) + '_' + str(d), 0, 1)
                c = Constraint(1, 1, [[v_var]], [1])
                self.constraints[c.id] = c

                v_var = self.vh.getVariable('v', 'v_' + str(d) + '_' + str(s) + '_' + str(d), 0, 1)
                c = Constraint(1, 1, [[v_var]], [1])
                self.constraints[c.id] = c

                for i in self.v:                    
                    v1_var = self.vh.getVariable('v' , 'v_' + str(i) + '_' + str(s) + '_' + str(d), 0, 1)
                    if i == d:
                        continue

                    l_vars = []
                    l_vars.append([v1_var])
                    coeff = []
                    coeff.append(1)

                    ## Here we are checking if i is in the path from s to d.
                    ## We know that one of the j is in the path from s to d, in the source tree of s
                    ## If there exists such an edge ij in the source tree of s
                    ## Then i exists in the path from s to d
                    ## Also d_ij of the destination is 1


                    for j in self.v:
                        if j == i:
                            continue

                        v2_var = self.vh.getVariable('v' , 'v_' + str(j) + '_' + str(s) + '_' + str(d), 0, 1)

                        s_var = self.vh.getVariable('s' , 's_' + str(i) + '_' + str(j) + '_' + str(s), 0, 1)

                        l_var = self.vh.getVariable('l',  'l_' + str(count), 0, 1)

                        count += 1
                        c = Constraint("Na", 0, [[l_var], [s_var]], [1, -1])
                        self.constraints[c.id] = c

                        c = Constraint("Na", 0, [[l_var], [v2_var]], [1, -1])
                        self.constraints[c.id] = c

                        c = Constraint(-1, "Na", [[l_var], [s_var], [v2_var]], [1 , -1, -1])
                        self.constraints[c.id] = c
                        
                        #l_vars.append([v2_var, s_var])
                        #coeff.append(-1)
                        l_vars.append([l_var])
                        coeff.append(-1)
                    
                    c = Constraint(0, "Na", l_vars, coeff) 
                    self.constraints[c.id] = c

                    c = Constraint("Na", 0, l_vars, coeff) 
                    self.constraints[c.id] = c


    def readTrees(self):
        trees = dict()
        paths = open(self.path + '/orig_path.txt', 'r')
        for p in paths:
            p = p.strip().split(' ')
            s = p[0]
            t = p[-1]

            if s not in trees:
                trees[s] = Tree(s)

            root = trees[s]
            curr_node = root

            for r in p[1:]:
                found = False
                if r in [c.id for c in curr_node.children]:
                    for c in curr_node.children:
                        if r == c.id:
                            curr_node = c
                            break
                else:
                    new_node = Tree(r)
                    curr_node.children.append(new_node)
                    curr_node = new_node
            
        paths.close()
        tree_children = trees[s].children
        x = tree_children[0]
        return trees

    def condense_trees(self,trees):
        for s in trees:
            tree = trees[s]
            pairs = list()
            for c in tree.children:
                pair = ((c, tree))
                pairs.append(pair)
            while len(pairs) > 0:
                p = pairs.pop(0)
                np = p[0]
                if len(p[0].children) == 1:
                    p[1].children = [ c for c in p[1].children if c.id != p[0].id]
                    p[1].children.extend(p[0].children)
                    np = p[1]
                for c in p[0].children:
                    pairs.append((c, np))


    def nTreeToBinaryTree(self, t):
        import random

        if len(t.children) == 0:
            return 
        else:
            while len(t.children) > 2:
                c2 = t.children.pop(2)
                pop_node = random.randint(0, 1)

                c0 = t.children.pop(pop_node)
                cnew = Tree('r')
                cnew.is_nary = True                
                cnew.children.append(c2)
                cnew.children.append(c0)
                t.children.append(cnew)                

            for c in t.children:
                self.nTreeToBinaryTree(c)


    def nTreesToBinary(self, trees):
        for s in trees:
            t = trees[s]
            self.nTreeToBinaryTree(t)
            
            

    # An edge should belong to only one segment
    def edgeInOnlyOneSegment(self):
        for src in self.Trees:
            for i in self.v:
                for j in self.v:
                    if i == j:
                        continue

                    adj_list = list()

                    c = self.Trees[src].children
                    adj_list.append([self.Trees[src], c[0]])
                    seg_no = 0
                
                    s_vars = list()
                    coeffs = list()

                    while len(adj_list) > 0:
                        pair = adj_list.pop(0)
                        s = pair[1]
                        d = s.id
                        s_no = 20 * (ord(src) - 97) + seg_no
                        s_seg_var = self.vh.getVariable('s', 's_' + str(i) + '_' + str(j) + '_' + str(s_no), 0, 1)
                        s_vars.append([s_seg_var])                        
                        coeffs.append(1)                        



                        for c in s.children:
                            adj_list.append([s, c])
                        
                        seg_no += 1

                    cons = Constraint(0, 1, s_vars, coeffs)
                    self.constraints[cons.id] = cons


    def segmentPresence(self):
        for src in self.Trees:
            adj_list = list()
            c = self.Trees[src].children
            adj_list.append([self.Trees[src], c[0]])
            
            seg_no = 0

            while len(adj_list) > 0:
                pair = adj_list.pop(0)
                s = pair[1]
                d = s.id
                s_no = 20 * (ord(src) - 97) + seg_no

                s_vars = []
                coeffs = []

                self.labels[src][(pair[0].id, pair[1].id)] = s_no
                ## each segment should have one edge at least
                for i in self.v:
                    for j in self.v:
                        if i == j:
                            continue

                        s_var = self.vh.getVariable('s', 's_' + str(i) + '_' + str(j) + '_' + str(s_no), 0, 1)
                        coeffs.append(1)                        
                        s_vars.append([s_var])
                        
                cons = Constraint(1, "Na", s_vars, coeffs)
                self.constraints[cons.id] = cons

                s_vars = []
                coeffs = []
                ## Calculate the number of edges in each segment
                for i in self.v:
                    for j in self.v:
                        if i == j:
                            continue

                        s_var = self.vh.getVariable('s', 's_' + str(i) + '_' + str(j) + '_' + str(s_no), 0, 1)
                        coeffs.append(1)                        
                        s_vars.append([s_var])


                z_var = self.vh.getVariable('z', 'z_' + str(s_no), 2, 12)
                s_vars.append([z_var])
                coeffs.append(-1)

                cons = Constraint(0, 0, s_vars, coeffs)
                #self.constraints[cons.id] = cons

                for c in s.children:
                    adj_list.append([s, c])
                    
                seg_no += 1


    def treeConstraints(self):
        ## write segment constraints here

        self.segmentInitiators()
        self.segmentPresence()
        self.segmentVariables()
        self.endToEndDistance()

        cc = 0

        sources = ['a', 'b', 'c', 'd', 'e']

        for src in sources:
            #if src == "e" or src == "d" or src == "c":
            #    continue
            skip = False
            adj_list = list()
            c = self.Trees[src].children
            adj_list.append([self.Trees[src], c[0]])
            
            #if cc > self.ntrees:
            #    continue


            seg_no = 0
            expended = 0

            while len(adj_list) > 0:
                pair = adj_list.pop(0)
                s = pair[1]

                d = s.id
                s_no = 20 * (ord(src) - 97) + seg_no

                for c in s.children:
                    expended += 1
                    e_no = 20 * (ord(src) - 97) + expended

#                    print(e_no, end=' ')

                    for j in self.v:
                        if j == src:
                            continue
                        
                        inc_vars = []
                        for i in self.v:
                            if i == j:
                                continue
                            s_var = self.vh.getVariable('s', 's_' + str(i) + '_' + str(j) + '_' + str(s_no), 0, 1)
                            inc_vars.append([s_var])
                                                    
                        out_vars = []
                        for k in self.v:
                            if k != src:
                                if k == j:
                                    continue

                                s_var = self.vh.getVariable('s', 's_' + str(j) + '_' + str(k) + '_' + str(s_no), 0 ,1)
                                out_vars.append([s_var])
                            
                                s_var = self.vh.getVariable('s', 's_' + str(j) + '_' + str(k) + '_' + str(e_no), 0, 1)
                                out_vars.append([s_var])
                        
                        cons = Constraint("Na", 0, inc_vars + out_vars, [1] * len(inc_vars) + [-1] * len(out_vars))
                        self.constraints[cons.id] = cons

                    
                ## number of out_vars is greater than or equal to number of in vars.
                if len(s.children) == 0:
                    ## segments to the destination
                    for j in self.v:
                        if j == src:
                            continue

                        inc_vars = []
                        for i in self.v:
                            if i == j:
                                continue
                            s_var = self.vh.getVariable('s', 's_' + str(i) + '_' + str(j) + '_' + str(s_no), 0, 1)
                            inc_vars.append([s_var])
                                                    
                        out_vars = []
                        for k in self.v:
                            if k != src:
                                if k == j:
                                    continue
                                s_var = self.vh.getVariable('s', 's_' + str(j) + '_' + str(k) + '_' + str(s_no), 0 ,1)
                                out_vars.append([s_var])
                            
                        
                        if j in self.e:
                            # number of incoming is less than 1
                            # number of outgoing is 0
                            cons = Constraint(0, 1, inc_vars, [1] * len(inc_vars))
                            self.constraints[cons.id] = cons

                            cons = Constraint(0, 0, out_vars, [1] * len(out_vars))
                            #self.constraints[cons.id] = cons
                        else:
                       #     if s_no == 88 or s_no == 47 or s_no == 8 or s_no == 28 or s_no == 108 or s_no == 63:
                      #         continue

                            #          if s_no == 4 or s_no == 23 or s_no == 43 or s_no == 63 or s_no == 83:
                  #              continue

                            #         if s_no == 84 or s_no == 105:
                            #             continue
                            #if s_no == 22 or s_no == 82:
                            #    continue
                            
                            #if s_no == 5 or s_no == 27 or s_no == 47 or s_no == 63 or s_no == 85 or s_no == 105:
                                #continue

                            # bandcon
                            #if s_no == 2 or s_no == 23 or s_no == 45 or s_no == 63 or s_no == 83:
                            #    continue
                            #if s_no == 63 or s_no == 83 or s_no == 45:
                            #    continue


                            #integra
                            #if s_no == 23 or s_no == 65 or s_no == 84 or s_no == 43 or s_no == 66 or s_no == 82 or s_no == 83 or s_no == 63:
                            #    continue

                            #bics
                            #if s_no == 83 or s_no == 84 or s_no == 86 or s_no == 45 or s_no == 26 or s_no == 7 or s_no == 3 or s_no == 65 or s_no == 64 or s_no == 107 or s_no == 108 or s_no == 105:
                                #continue

                            if s_no == 7:
                                continue

                            ## colt
#                            if s_no == 4 or s_no == 27 or s_no == 47 or s_no == 65 or s_no == 86 or s_no == 104:
#                                continue

                            # number of incoming is equal to number of outgoing

                            # integra
                            #if seg_no == 6 or seg_no == 23 or seg_no == 63 or seg_no == 66 or seg_no == 83 or seg_no == 43 or seg_no == 85:
                            #    continue

                            if skip == False:
                                skip = True
                                continue



                            cons = Constraint("Na", 0, inc_vars + out_vars, [1] * len(inc_vars) + [-1] * len(out_vars))
                            self.constraints[cons.id] = cons

                for c in s.children:
                    adj_list.append([s, c])

                seg_no += 1


    def calcDistance(self, src, node, parent_seg):
        if len(node.children) == 0:
            print(src, node.id, parent_seg)
            z_vars = []
            coeffs = []

            for ps in parent_seg:
                z_var = self.vh.getVariable('z', 'z_' + str(ps), 2, 12)
                z_vars.append([z_var])
                coeffs.append(1)

            z_var = self.vh.getVariable('z','z_' +  str(node.id) + '_' + str(src), 2, 12)
            z_vars.append([z_var])
            coeffs.append(-1)

            #cons = Constraint(0, 0, z_vars, coeffs)
            #self.constraints[cons.id] = cons

        for c in node.children:
            s_no = self.labels[src][(node.id, c.id)]
            self.calcDistance(src, c, parent_seg + [s_no])
        
    def endToEndDistance(self):
        for src in self.Trees:
            self.calcDistance(src, self.Trees[src], [])

    def segmentInitiators(self):
        for src in self.Trees:
            seg_no = 20 * (ord(src) - 97)
            s_var = self.vh.getVariable('s', 's_' + str(src) + '_' + str(src) + '1' + '_' + str(seg_no), 0, 1)
            cons = Constraint(1, 1, [[s_var]], [1])
            self.constraints[cons.id] = cons
        
        for src in self.Trees:
            adj_list = list()
            c = self.Trees[src].children
            adj_list.append([self.Trees[src], c[0]])
            
            seg_no = 0

            while len(adj_list) > 0:
                pair = adj_list.pop(0)
                s = pair[1]
                d = s.id
                s_no = 20 * (ord(src) - 97) + seg_no
                
                if len(s.children) == 0:
                    s_var = self.vh.getVariable('s', 's_' + str(d) + '1_' + str(d) + '_' +  str(s_no), 0 , 1) 
                    cons = Constraint(1, 1, [[s_var]], [1])
                    self.constraints[cons.id] = cons

                for c in s.children:
                    adj_list.append([s, c])
                    
                seg_no += 1
            

    def segmentVariables(self):
        ## segment connect to edge variables
        for src in self.Trees:
            for i in self.v:
                for j in self.v:
                    ## Across all segments if the edge exists, it should exist in the tree
                    
                    adj_list = list()
                    c = self.Trees[src].children
                    adj_list.append([self.Trees[src], c[0]])
            
                    seg_no = 0
                    coeffs = []
                    s_var = self.vh.getVariable('s', 's_' + str(i) + '_' + str(j) + '_' + str(src))
                    coeffs.append(-1)
                    s_vars = []
                    s_vars.append([s_var])

                    while len(adj_list) > 0:
                        pair = adj_list.pop(0)
                        s = pair[1]
                        s_no = 20 * (ord(src) - 97) + seg_no
                        s_var = self.vh.getVariable('s', 's_' + str(i) + '_' + str(j) + '_' +  str(s_no), 0 , 1) 
                        s_vars.append([s_var])
                        coeffs.append(1)

                        for c in s.children:
                            adj_list.append([s, c])

                        seg_no += 1
                        #cons = Constraint(0, 0, [[s_var]], [1])
                        #self.constraints[cons.id] = cons

                    cons = Constraint("Na", 0, s_vars, coeffs)
                    self.constraints[cons.id] = cons

                    cons = Constraint(0, "Na", s_vars, coeffs)
                    self.constraints[cons.id] = cons



    def covarianceTreeConstraints(self):
        trees = self.readTrees()
        self.condense_trees(trees)
        #self.nTreesToBinary(trees)

        count_constraints = 0

        count = 0
        count2 = 0
        count3 = 0
        count4 = 0

        f = open("covariances.txt", "w")
        f1 = open("covarianceconstraints.txt", "w")
        #sources = self.ntrees.split(":")        

        for s in trees:
#            if s == 'f':
#                printTree(trees[s])
#                continue

            tree = trees[s].children[0]
            
            node_list = list()
            node_list.append(tree)            

            while len(node_list) > 0:
                curr_node = node_list.pop(0)
                

                for c in curr_node.children:
                    if len(c.children) == 0:
                        continue
                    if len(c.children) == 1:
                        node_list.append(c)
                        continue

                    node_list.append(c)

                    ## Writing a constraint for currnode and c
                    v1_list = c.leafs()

                    v2_list = [d for d in curr_node.leafs() if d.id not in [x.id for x in c.leafs()]]

                    if len(v1_list) == 0 or len(v1_list) == 1 or len(v2_list) == 0:
                        continue

                    ucv1 = v1_list[0]
                    cv = v1_list[-1]
                    ucv2 = v2_list[0]

                    ## shared path length between ucv1 and cv
                                        
                    p1_var = self.vh.getVariable('p', 'p_' +  str(count),0, 10)
                    count += 1
                    p_vars = []
                    p_coeffs = []

                    p_vars.append([p1_var])
                    p_coeffs.append(1)

                    f.write(str(count) + " " + str(s) + " " + str(cv.id) + " " + str(ucv1.id))
                    f.write("\n")

                    for v1 in self.v:
                        q_var = self.vh.getVariable('q', 'q_' + str(count2), 0, 1)
                        v1_var = self.vh.getVariable('v', 'v_' + str(v1) + '_' + str(s) + '_' + str(ucv1.id), 0, 1)
                        v2_var = self.vh.getVariable('v', 'v_' + str(v1) + '_' + str(s) + '_' + str(cv.id), 0, 1)
                        
                        co = Constraint("Na", 0, [[q_var], [v1_var]], [1, -1])
                        self.constraints[co.id] = co

                        co = Constraint("Na", 0, [[q_var], [v2_var]], [1, -1])
                        self.constraints[co.id] = co

                        co = Constraint(-1 , "Na", [[q_var], [v1_var], [v2_var]], [1, -1, -1])
                        self.constraints[co.id] = co

                        #p_vars.append([v1_var, v2_var])
                        p_vars.append([q_var])
                        count2 += 1
                        p_coeffs.append(-1)
                        
                    co = Constraint("Na", 0, p_vars, p_coeffs)
                    co.rewrite = True
                    self.constraints[co.id] = co
                    
                    co = Constraint(0, "Na", p_vars, p_coeffs)
                    co.rewrite = True
                    self.constraints[co.id] = co


                    ## shared path length between ucv2 and cv
                    p2_var = self.vh.getVariable('p', 'p_' +  str(count),0, 10)

                    f1.write(str(s) + " " + str(cv.id) + " " + str(ucv1.id) + " " + str(ucv2.id) + " " + str(curr_node.id) + " " + str(c.id) + " " + str(count - 1) + " " + str(count) + " " + str(count3))
                    f1.write("\n")

                    count += 1
                    p_vars = []
                    p_coeffs = []

                    p_vars.append([p2_var])
                    p_coeffs.append(1)

                    f.write(str(count) + " " + str(s) + " " + str(cv.id) + " " + str(ucv2.id))
                    f.write("\n")

                    for v1 in self.v:
                        q_var = self.vh.getVariable('q', 'q_' + str(count2), 0, 1)
                        v1_var = self.vh.getVariable('v', 'v_' + str(v1) + '_' + str(s) + '_' + str(ucv2.id), 0, 1)
                        v2_var = self.vh.getVariable('v', 'v_' + str(v1) + '_' + str(s) + '_' + str(cv.id), 0, 1)
                        
                        co = Constraint("Na", 0, [[q_var], [v1_var]], [1, -1])
                        self.constraints[co.id] = co

                        co = Constraint("Na", 0, [[q_var], [v2_var]], [1, -1])
                        self.constraints[co.id] = co

                        co = Constraint(-1 , "Na", [[q_var], [v1_var], [v2_var]], [1, -1, -1])
                        self.constraints[co.id] = co

                        p_vars.append([q_var])
                        count2 += 1
                        p_coeffs.append(-1)
                        
                    co = Constraint(0, "Na", p_vars, p_coeffs)
                    co.rewrite = True
                    self.constraints[co.id] = co                    

                    co = Constraint("Na", 0, p_vars, p_coeffs)
                    co.rewrite = True
                    self.constraints[co.id] = co                    

                    e_var = self.vh.getVariable('e' , 'e_' + str(count3), 0, 1)
                    count3 += 1

#                     co = Constraint(-50, -1, [[p2_var], [p1_var], [e_var]], [1, -1, -50])
#                     self.constraints[co.id] = co
#                     self.obj.vars.append([e_var])
 #                     self.obj.coeffs.append(15)

                    count_constraints += 1

                    c.is_nary = False
                                               
                    if c.is_nary == False:
                        co = Constraint(-50, -1, [[p2_var], [p1_var], [e_var]], [1, -1, -50])
                        self.constraints[co.id] = co
                        self.obj.vars.append([e_var])
                        self.obj.coeffs.append(2)
                    else :
                        co = Constraint(-49, 0, [[p2_var], [p1_var], [e_var]], [1, -1, -50])
                        err_var = self.vh.getVariable('f', 'f_' + str(count4), 0, 5)
                        co = Constraint(0, "Na", [[err_var], [p2_var], [p1_var]], [1, -1, 1])
                        self.constraints[co.id] = co
                                                
                        co = Constraint(0, "Na", [[err_var], [p2_var], [p1_var]], [1, 1, -1])
                        self.constraints[co.id] = co

                        self.obj.vars.append([err_var])
                        self.obj.coeffs.append(2)

                        count4 += 1
                    
                        


    def covarianceTreeConstraints2(self):
        count_constraints = 0

        count = 0
        count2 = 0
        count3 = 0
        count4 = 0

        f = open("covariances.txt", "w")
        f1 = open("covarianceconstraints.txt", "w")

        fil = open(self.path + '/covariance.txt' , 'r')
        for line in fil:
            line = line.strip().split(" ")
            s = line[0]
            ucv1 = line[1]
            cv = line[2]
            ucv2 = line[3]            
                                        
            p1_var = self.vh.getVariable('p', 'p_' +  str(count),0, 10)
            count += 1
            p_vars = []
            p_coeffs = []            
            p_vars.append([p1_var])
            p_coeffs.append(1)

            f.write(str(count) + " " + str(s) + " " + str(cv) + " " + str(ucv1))
            f.write("\n")

            for v1 in self.v:
                q_var = self.vh.getVariable('q', 'q_' + str(count2), 0, 1)
                v1_var = self.vh.getVariable('v', 'v_' + str(v1) + '_' + str(s) + '_' + str(ucv1), 0, 1)
                v2_var = self.vh.getVariable('v', 'v_' + str(v1) + '_' + str(s) + '_' + str(cv), 0, 1)
                        
                co = Constraint("Na", 0, [[q_var], [v1_var]], [1, -1])
                self.constraints[co.id] = co

                co = Constraint("Na", 0, [[q_var], [v2_var]], [1, -1])
                self.constraints[co.id] = co

                co = Constraint(-1 , "Na", [[q_var], [v1_var], [v2_var]], [1, -1, -1])
                self.constraints[co.id] = co

                p_vars.append([q_var])
                count2 += 1
                p_coeffs.append(-1)
                        
            co = Constraint("Na", 0, p_vars, p_coeffs)
            co.rewrite = True
            self.constraints[co.id] = co
                    
            co = Constraint(0, "Na", p_vars, p_coeffs)
            co.rewrite = True
            self.constraints[co.id] = co


            ## shared path length between ucv2 and cv
            p2_var = self.vh.getVariable('p', 'p_' +  str(count),0, 10)

            #f1.write(str(s) + " " + str(cv) + " " + str(ucv1) + " " + str(ucv2) + " " + str(curr_node) + " " + str(c) + " " + str(count - 1) + " " + str(count) + " " + str(count3))
            #f1.write("\n")

            count += 1
            p_vars = []
            p_coeffs = []

            p_vars.append([p2_var])
            p_coeffs.append(1)

            f.write(str(count) + " " + str(s) + " " + str(cv) + " " + str(ucv2))
            f.write("\n")

            for v1 in self.v:
                q_var = self.vh.getVariable('q', 'q_' + str(count2), 0, 1)
                v1_var = self.vh.getVariable('v', 'v_' + str(v1) + '_' + str(s) + '_' + str(ucv2), 0, 1)
                v2_var = self.vh.getVariable('v', 'v_' + str(v1) + '_' + str(s) + '_' + str(cv), 0, 1)
                        
                co = Constraint("Na", 0, [[q_var], [v1_var]], [1, -1])
                self.constraints[co.id] = co

                co = Constraint("Na", 0, [[q_var], [v2_var]], [1, -1])
                self.constraints[co.id] = co

                co = Constraint(-1 , "Na", [[q_var], [v1_var], [v2_var]], [1, -1, -1])
                self.constraints[co.id] = co

                p_vars.append([q_var])
                count2 += 1
                p_coeffs.append(-1)
                        
            co = Constraint(0, "Na", p_vars, p_coeffs)
            co.rewrite = True
            self.constraints[co.id] = co                    

            co = Constraint("Na", 0, p_vars, p_coeffs)
            co.rewrite = True
            self.constraints[co.id] = co                    

            e_var = self.vh.getVariable('e' , 'e_' + str(count3), 0, 1)
            count3 += 1

            count_constraints += 1
            #if count_constraints % 2 == 0:
            #    continue
            
            ## if else condition here
            if line[4] == "g":
                co = Constraint(-50, -1, [[p2_var], [p1_var], [e_var]], [1, -1, -50])
                self.constraints[co.id] = co
                self.obj.vars.append([e_var])
                self.obj.coeffs.append(4)                    
            elif line[4] == "l":
                co = Constraint(-50, -1, [[p1_var], [p2_var], [e_var]], [1, -1, -50])
                self.constraints[co.id] = co
                self.obj.vars.append([e_var])
                self.obj.coeffs.append(4)                                
            else:
                co = Constraint("Na", 0, [[p2_var], [p1_var], [e_var]], [1, -1, -1])
                self.constraints[co.id] = co
                self.obj.vars.append([e_var])
                self.obj.coeffs.append(4)                    


                co = Constraint("Na", 0, [[p1_var], [p2_var], [e_var]], [1, -1, -1])
                self.constraints[co.id] = co
                self.obj.vars.append([e_var])
                self.obj.coeffs.append(4)                    


                        


    ## looks fine now
    def pathCorrectness(self):
        count = 0
        for s in self.e:
            for d in self.e:
                if s == d:
                    continue
                
                for j in [v for v in self.v if v not in self.e]:
                    inc_vars = list()

                    ## All the incoming edges at j
                    for i in self.a[j]:
                        if i == j:
                            continue
                        s_var = self.vh.getVariable('s' , 's_' + str(i) + '_' + str(j) + '_' + str(s))
                        d_var = self.vh.getVariable('s' , 's_' + str(j) + '_' + str(i) + '_' + str(d))

                        ### TODO : Linearize bilinearly
                        #b_var = self.vh.getVariable('b', 'b_' + str(i) + '_' + str(j) + '_' + str(s) + '_' + str(d))
                        b_var = self.vh.getVariable('b', 'b_' + str(count))
                        count = count + 1

                        eq1 = Constraint("Na", 0, [[b_var], [s_var]], [1, -1])
                        self.constraints[eq1.id] = eq1

                        eq2 = Constraint("Na", 0, [[b_var], [d_var]], [1, -1])
                        self.constraints[eq2.id] = eq2

                        eq3 = Constraint(-1, "Na", [[b_var],[s_var],[d_var]], [1,-1,-1])
                        self.constraints[eq3.id] = eq3

                        inc_vars.append([b_var])
                    
                    ## All the outgoing edges at j
                    out_vars = list()
                    for k in self.a[j]:
                        if k == j:
                            continue

                        s_var = self.vh.getVariable('s', 's_' + str(j) + '_' + str(k) + '_' + str(s))
                        d_var = self.vh.getVariable('s', 's_' + str(k) + '_' + str(j) + '_' + str(d))

                        b_var = self.vh.getVariable('b', 'b_' + str(count))
                        count = count + 1

                        eq1 = Constraint("Na", 0, [[b_var], [s_var]], [1, -1])
                        self.constraints[eq1.id] = eq1

                        eq2 = Constraint("Na", 0, [[b_var], [d_var]], [1, -1])
                        self.constraints[eq2.id] = eq2

                        eq3 = Constraint(-1, "Na", [[b_var],[s_var],[d_var]], [1,-1,-1])
                        self.constraints[eq3.id] = eq3

                        out_vars.append([b_var])

                    coefs1 = [1] * len(inc_vars)
                    cons = Constraint(0, 1, inc_vars, coefs1)
                    #self.constraints[cons.id] = cons

                    coefs2 = [1] * len(out_vars) + [-1] * len(inc_vars)
                    cons = Constraint(0, "Na", out_vars + inc_vars, coefs2)
                    self.constraints[cons.id] = cons


    ## this is fine
    def egressConstraint(self):

        ## There is no edge from a router to an enclave if it is not its egress router (across all source trees)
        #to a server if the router is not the servers
        ## egress router
        for e in self.e:
            for v2 in self.a[e]:
                
                w1_var = self.vh.getVariable('w', 'w_' + e + '_' + v2)
                w2_var = self.vh.getVariable('w', 'w_' + v2 + '_' + e)
                
                if v2 == e + '1':
                    cons = Constraint(1,1, [[w1_var]], [1])
                    self.constraints[cons.id] = cons
                    cons = Constraint(1,1, [[w2_var]], [1])
                    self.constraints[cons.id] = cons
                else :
                    cons = Constraint(0,0, [[w1_var]], [1])
                    self.constraints[cons.id] = cons
                    cons = Constraint(0,0, [[w2_var]], [1])
                    self.constraints[cons.id] = cons
                                    
        ## For the source tree
        for e in self.e:
            ## Egress router to source link should be missing
            s_var = self.vh.getVariable('s', 's_' + e + '1_' + str(e) + '_' + str(e))
            cons = Constraint(0, 0, [[s_var]], [1])
            self.constraints[cons.id] = cons

            ## enclave to egress router link is available
            s_var = self.vh.getVariable('s', 's_' + e + '_' + str(e) + '1_' + str(e))
            cons = Constraint(1, 1, [[s_var]], [1])
            self.constraints[cons.id] = cons

            for e1 in self.e:
                if e1 == e:
                    continue

                # edge from egress router of destination to a destination exists
                s_var = self.vh.getVariable('s', 's_' + e1 + '1_' + e1 + '_' + e)
                cons = Constraint(1, 1, [[s_var]], [1])
                self.constraints[cons.id] = cons

                # edge from dst to its egress router does not exist
                s_var = self.vh.getVariable('s', 's_' + e1 + '_' + e1 +'1_' + e)
                cons = Constraint(0, 0, [[s_var]], [1])
                self.constraints[cons.id] = cons


    def rdConstraints(self):
        for s in self.rd:

            distances = self.rd[s]
            distances.sort(key=lambda x: x[1])
            
            #distances = [x for x in distances if x[0] in sources]

            for i in range(1, len(distances)):
                s1 = distances[i-1][0]
                d1 = distances[i-1][1]
                s2 = distances[i][0]
                d2 = distances[i][1]
                

                z1_var = self.vh.getVariable('z', 'z_' + s1 + '_' + s, 2, 12)
                z2_var = self.vh.getVariable('z', 'z_' + s2 + '_' + s, 2, 12)

                if d2 == d1:
                    cons = Constraint(0, "Na", [[z2_var], [z1_var]], [1, -1])
                    self.constraints[cons.id] = cons
                else:
                    cons = Constraint(1, "Na", [[z2_var], [z1_var]], [1, -1])
                    self.constraints[cons.id] = cons


    def rdConstraintsWithError(self):

        counter = 1000
        path = "/".join(self.path.split("/")[:-1])
        
        f = open(path + "/rd" + str(self.ntrees - 1) + ".txt", "r")

        f1 = open(path + "/rd" + str(self.ntrees) + ".txt", "w")

        newrds = []
        newbools = []

        print("n trees ", self.ntrees)

        for l in f:
            l = l.strip().split(";")
            rds = l[1].split(" ")
            bools = l[2].split(" ")
            src = l[0]

            nrds = []
            nbs  = []

            for i in range(len(rds) - 1):
                bool = bools[i]
                if bool == "f":
                    nrds.append(rds[i])
                    nbs.append("f")
                else :
                    if random.randint(1,10 - self.ntrees) <= 1:
                        nrds.append(rds[i+1])
                        ## Introduced an error
                        nbs.append("f")

                        ## swap the constraint
                        swap_var = rds[i+1]
                        rds[i+1] = rds[i]
                        rds[i] = swap_var
                    else :
                        nrds.append(rds[i])
                        nbs.append("t")

            nrds.append(rds[-1])
            
            str1 = " ".join(nrds)
            f1.write(src + ";" + str1 + ";" + " ".join(nbs) + "\n")

            e_var = self.vh.getVariable('e' , 'e_' + str(counter), 0, 1)
            counter+=1 

            for i in range(len(rds) - 1):
                s1 = nrds[i]
                s2 = nrds[i+1]

                d1 = self.d[((src, s1))][0]
                d2 = self.d[((src, s2))][0]
                
                z1_var = self.vh.getVariable('z', 'z_' + s1 + '_' + src, 2, 12)
                z2_var = self.vh.getVariable('z', 'z_' + s2 + '_' + src, 2, 12)

                if d2 == d1:

                    co = Constraint("Na", 0, [[z2_var], [z1_var], [e_var]], [1, -1, -1])
                    self.constraints[co.id] = co
                    self.obj.vars.append([e_var])
                    self.obj.coeffs.append(4)                    


                    co = Constraint("Na", 0, [[z1_var], [z2_var], [e_var]], [1, -1, -1])
                    self.constraints[co.id] = co
                    self.obj.vars.append([e_var])
                    self.obj.coeffs.append(4)                    

                else:
                    co = Constraint(-2, -1, [[z1_var], [z2_var], [e_var]], [1, -1, -2])
                    self.constraints[co.id] = co
                    self.obj.vars.append([e_var])
                    self.obj.coeffs.append(4)                                



        f1.close()


    # this is fine
    def cycleConstraints(self):
        count = 0
        for e in self.e:
            for j in self.v:
                if j == e:
                    continue


                # TODO : upper bound of z is number of vertices
                ## m_j^e = \sigma (s_(ij)^e * m_i) + 1
                new_equ = list()

                new_coeffs = list()

                equ = list()
                coeffs = list()

                #m_var = self.vh.getVariable('m', 'm_' + str(j) + '_' + e, 0, 100)
                #equ.append([m_var])
                #coeffs.append(1)

                z_var = self.vh.getVariable('z', 'z_' + j + '_' + e, 2, 12)
                new_equ.append([z_var])
                new_coeffs.append(1)

                for i in self.a[j]:
                    if i != j:
                        z_var = self.vh.getVariable('z', 'z_' + str(i) + '_' + e, 2, 12)
                        s_var = self.vh.getVariable('s', 's_' + str(i) + '_' + str(j) + '_' + e)
                        #m_var = self.vh.getVariable('m', 'm_' + str(i) + '_' + e, 0, 100)
                        
                        #equ.append([m_var, s_var])
                        #equ.append([s_var])

                        edge = [j,i]
                        edge.sort()
                        edge = tuple(edge)

                        #coeffs.append(-1)
                        #coeffs.append(-1 * self.edgeweight[edge])                


                        ## r_var should be s_i_j_e
                        ## three equations here
                        ## TODO : Linearize these constraints

                        r_var = self.vh.getVariable('r', 'r_' + str(count), 0, 12)
                        count = count + 1
                                                 
                        #new_equ.append([z_var, s_var])
                        new_equ.append([r_var])
                        new_coeffs.append(-1)
        
                        eq1 = Constraint("Na", 0, [[r_var],[s_var]], [1, -12])
                        self.constraints[eq1.id] = eq1

                        eq2 = Constraint(0, "Na", [[r_var],[s_var]], [1, -2])
                        self.constraints[eq2.id] = eq2

                        eq3 = Constraint(2, "Na", [[z_var], [r_var], [s_var]], [1, -1, 2])
                        self.constraints[eq3.id] = eq3

                        eq4 = Constraint(-12, "Na", [[r_var], [z_var], [s_var]], [1,-1,-12])
                        self.constraints[eq4.id] = eq4

                cons1 = Constraint(1, "Na", new_equ, new_coeffs)
                self.constraints[cons1.id] = cons1

                cons1 = Constraint("Na", 1, new_equ, new_coeffs)
                self.constraints[cons1.id] = cons1

                #cons = Constraint(0, 0, equ, coeffs)
                #self.constraints[cons.id] = cons


    ### If an edge exists in any of the source tree then the edge exists
    # this is fine
    ## todo 
    ## this has to be changed to do it only for egress edges
    def edgeExistsConstraint(self):            
        for i in self.v:
            for j in self.a[i]:
                if i == j:
                    continue
                edge_vars = list()

                for e in self.e:
                    s_var = self.vh.getVariable('s', 's_' + str(i) + '_' + str(j) + '_' + e)
                    #d_var = self.vh.getVariable('d', 'd_' + str(i) + '_' + str(j) + '_' + e)
                    edge_vars.append([s_var])
                    #edge_vars.append([d_var])
                
                coefs = [1] * len(edge_vars) 
                coefs.append(-1 * len(edge_vars) - 1)
                w_var = self.vh.getVariable('w', 'w_' + i + '_' + j)
                edge_vars.append([w_var])
                cons = Constraint(-1 * len(edge_vars), 0, edge_vars, coefs)
                self.constraints[cons.id] = cons

    # The structure from any source is a tree
    # this is fine
    def srcTreeConstraints(self):
        # e is the source
        for e in self.e:
            ## i is the vertex at number of incoming edges is <= 1 for all sources
            for i in [v for v in self.v if v not in self.e]:
                
                s_vars = list()
                out_vars = []

                for j in [v for v in self.a[i] if v not in self.e]:
                    if j == i :
                        continue
                    s_var = self.vh.getVariable('s', 's_' + str(j) + '_' + str(i) + '_' + str(e))
                    s_vars.append([s_var])


                for j in [v for v in self.a[i] if v != e]:
                    if j == i:
                        continue

                    s_var = self.vh.getVariable('s', 's_' + str(i) + '_' + str(j) + '_' + str(e))
                    out_vars.append([s_var])


                cons = Constraint(0, 1, s_vars, [1] * len(s_vars))
                self.constraints[cons.id] = cons

                cons = Constraint(0, "Na", out_vars + s_vars, [1] * len(out_vars) + [-1] * len(s_vars))
                self.constraints[cons.id] = cons


    def readTrees(self):
        trees = dict()
        paths = open(self.path + '/orig_path.txt', 'r')
        for p in paths:
            p = p.strip().split(' ')
            s = p[0]
            t = p[-1]

            if s not in trees:
                trees[s] = Tree(s)

            root = trees[s]
            curr_node = root

            for r in p[1:]:
                found = False
                if r in [c.id for c in curr_node.children]:
                    for c in curr_node.children:
                        if r == c.id:
                            curr_node = c
                            break
                else:
                    new_node = Tree(r)
                    curr_node.children.append(new_node)
                    curr_node = new_node
            
        paths.close()
        tree_children = trees[s].children
        x = tree_children[0]
        return trees

            
                    
