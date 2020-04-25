import sys
import numpy as np

global_trace = []
root = None

class node:
    def __init__(self, oid, val, is_lc):
        self.oid = oid
        self.val = val        

        self.parent = None
        self.l_c = None
        self.r_c = None

        self.is_lc = is_lc

    def set_parent(self, n):
        self.parent = n

    def set_left(self, c):
        self.l_c = c
        c.is_lc = True

    def set_right(self, c):
        self.r_c = c
        c.is_rc = False

    def find_next(self):
        if self.is_lc == True:
            try:
                if self.parent.r_c != None:
                    return parent.r_c
            except:
                print("Parent not found !")
                return 

        return self.find_cousin()

    def find_cousin(self):
        p = self.parent
        if p.parent == None:
            return None
        p = p.parent
        
        return p.find_leftmost_subleaf()
        

    def find_leftmost_subleaf(self):
        l_most = self
        if l_most.l_c == None and l_most.r_c != None:
            l_most = l_most.r_c

        while l_most.l_c != None:
            l_most = l.l_c
        return l_most
        
    def recompute(self):
        p_node = self.parent
        while p_node != None:
            tmp_val = 0
            if p_node.l_c != None:
                tmp_val += p_node.l_c.val
            if p_node.r_c != None:
                tmp_val += p_node.r_c.val
            p_node.val = tmp_val
            p_node = p_node.parent

    def fromLeftInsertToLeft(self, n):
        curr_node = self
        add_to_root = False

        while curr_node.is_lc == True:
            if curr_node.parent == None:
                add_to_root = True
            curr_node = curr_node.parent

        if add_to_root == True:
           global_trace.append(n.oid) 
            
        ## Add logic to insert the node between the curr_node and its parent
        ## you have curr_node, parent_node, and tmp
        p_node = curr_node.parent
        tmp = node("nl", curr_node.val, False)
        
        ## n is set
        tmp.set_left(n)
        n.parent = tmp

        ## The direction connections are done
        tmp.set_right(curr_node)
        p_node.set_right(tmp)

        ## Set the parental connections
        tmp.set_parent(p_node)
        curr_node.set_parent(tmp)    

        ## call recompute on n
        self.recompute(n)

        return True


    def fromLeftInsertToRight(self, n):
        curr_node = self
        p_node = curr_node.parent
        if p_node.r_c == None:
            p_node.r_c = n
            n.parent = p_node
            n.is_lc = False
            return

        r_child = p_node.r_c
        tmp = node("nl", r_child.val, False)
        
        ## add n to tmp
        tmp.set_left(n)
        n.parent = tmp
        n.is_lc = True

        ##set the directions
        tmp.set_right(r_child)
        p_node.set_right(tmp)
        
        ## set parent connections
        tmp.set_parent(p_node)
        r_child.set_parent(tmp)
        
        ## call recompute on n
        self.recompute(n)
        return True
                
    def fromRightInsertToLeft(self, n):
        curr_node = self
        p_node = curr_node.parent

        if p_node.l_c == None:
            p_node.set_left(n)
            n.set_parent(p_node)
            n.is_lc = True
            return False

        l_child = p_node.l_c
        tmp = node("nl", l_child.val, True)
        
        ## add n to tmp
        tmp.set_right(n)
        n.set_parent(tmp)
        n.is_lc = False

        ## set the directions
        tmp.set_left(l_child)
        p_node.set_left(tmp)

        ## set parents
        l_child.set_parent(tmp)
        tmp.set_parent(p_node)
        
        self.recompute(n)
        return True

    def fromRightInsertToRight(self, n):
        curr_node = self
        add_to_root = False
        
        while curr_node.is_lc == False:
            if curr_node.parent == None:
                add_to_root = True
            curr_node = curr_node.parent

        if add_to_root == True:
            # Do something here
            n_root = node("nl", root.val, False)
            n_root.set_left(root)
            n_root.set_right(n)
            n.parent = n_root
            root = n_root
            return True

        p_node = curr_node.parent
        tmp = node("nl", curr_node.val, True)
        
        ## set up n
        tmp.set_right(n)
        n.set_parent(tmp)

        ## Setup the directions
        tmp.set_left(curr_node)
        p_node.set_left(tmp)

        self.recompute(n)
        return True

        

    def insert_node(self, n, sd):
        ret = True
        if self.node.oid != "nl":
            # We have reached a leaf node
            if sd > self.val:
                print("sd > leaf_node.val")
                sys.exit()


            thr = float(sd)/self.val
            thr = 1 - thr

            ins_left = False
            z = np.random.random()
            
            if z < thr:
                ins_left = True

            ## You are a left child
            if self.is_lc == True:
                if ins_left == True:
                    return self.fromLeftInsertToLeft(n)
                else:
                    return self.fromLeftInsertToRight(n)
            else :
                if ins_left == True:
                    return self.fromRightInsertToLeft(n)
                else:
                    return self.fromRightInsertToRight(n)

        else:
            if self.left != None and self.left.val > sd:
                ret = self.left.insert_node(n, sd)
            elif self.right != None:
                if self.left != None:
                    sd = sd - self.left.val
                ret = self.right.insert_node(n, sd)
            else:
                print("Something is terribly wrong !")
                sys.exit()

        return ret


    ## Always maintain a root
    ## Think about how to update the root
    def insertAt(self, sd, n):
        ## should return a node on which the stack_d falls
        if root.val < sd:
            tmp = node("nl", n.val, True)
            n_root = node("nl", n.val + root.val, False)
            n_root.set_left(root)
            n_root.set_right(tmp)

            root.parent = n_root
            root.is_lc = True

            tmp.parent(n_root)
            tmp.set_left(n)

            root = n_root

        else:
            ins_left = False
            insert_node(self, n, sd)
            


    
def sample(cdf, vals):
    pass

def generate_trace_tree(sz_dst, pop_dst, fd, trace_len):
    
    ## Start with an initial object
    ## Popularity distribution does not make sense. It would just by virtue of stack distance dist

    new_obj_id = 0 
    init_obj = new_obj_id
    new_obj_id += 1

    
    
