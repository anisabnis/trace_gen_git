# uncompyle6 version 3.6.6
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.7.6 (default, Dec 30 2019, 19:38:36) 
# [Clang 10.0.0 (clang-1000.11.45.5)]
# Embedded file name: /Users/asabnis/Research/trace_gen_git/tree_approach/treelib.py
# Compiled at: 2020-04-24 22:22:21
# Size of source mod 2**32: 3768 bytes

import numpy as np
import sys

root = None

class node:
    counter = 0

    def __init__(self, obj_id, size):
        self.obj_id = obj_id
        self.s = size
        self.b = 0
        self.stop_del = False
        self.children = []
        self.next = None
        self.parent = None
        self.id = node.counter
        self.child_idx = 0
        node.counter += 1

    def addValTillRoot(self, val):
        p = self.parent
        while p != None:
            p.s += val
            p = p.parent

    def __del__(self):
        pass

    def lca(self, n):
        a = self
        while a != None:
            b = n
            while b != None:
                if a.id == b.id:                    
                    return a.id
                b = b.parent
            a = a.parent

        print('LCA : Parent connections not correct ', self.id, n.id)
        sys.exit()

    def add_child(self, n):
        n.child_idx = len(self.children)
        self.children.append(n)
        n.parent = self

    def set_parent(self, n):
        self.parent = n

    def set_next(self, n):
        self.next = n


    def findUniqBytes(self, n):

        curr_node = self
        next_node = n
        
        lca_id = curr_node.lca(next_node)        

        curr_parent = curr_node.parent
        child_node = curr_node
        child_idx = child_node.child_idx
            
        local_uniq_bytes = 0

        while curr_parent.id != lca_id:
                
            if child_idx == len(curr_parent.children):
                curr_parent = curr_parent.parent
                child_node  = child_node.parent
                child_idx   = child_node.child_idx
                continue

            for i in range(child_idx + 1, len(curr_parent.children)):
                lb = curr_parent.children[i].s * curr_parent.children[i].b
                local_uniq_bytes += lb

            curr_parent = curr_parent.parent
            child_node  = child_node.parent
            child_idx   = child_node.child_idx

        curr_parent = next_node.parent
        child_node = next_node
        child_idx = child_node.child_idx

        while curr_parent.id != lca_id:

            if child_idx == 0:
                curr_parent = curr_parent.parent
                child_node  = child_node.parent
                child_idx   = child_node.child_idx
                continue
            
            for i in range(0, child_idx):
                lb = curr_parent.children[i].s * curr_parent.children[i].b
                local_uniq_bytes += lb

            curr_parent = curr_parent.parent
            child_node  = child_node.parent
            child_idx   = child_node.child_idx


        return local_uniq_bytes



    def cleanUpAfterInsertion(self, sd, inserted_node):
        curr_node = self
        next_node = curr_node.next

        if next_node == None:
            self.delete_node()
            return

        uniq_bytes = curr_node.s
        cnt = 0
        to_del_nodes = []

        while uniq_bytes < sd:

            if next_node == None:
                break

            to_del_nodes.append(curr_node)
            uniq_bytes += curr_node.findUniqBytes(next_node)
            next_node = next_node.next
            curr_node = curr_node.next

        for d in to_del_nodes:
            inserted_node.next = d.next
            d.delete_node()

        inserted_node.set_b()
        return to_del_nodes


    def delete_node(self):
        weight = self.s * self.b
        p = self.parent
        
        if p == None:
            return

        self.parent.children = [c for c in self.parent.children if c.id != self.id]

        i = 0
        for c in self.parent.children:
            c.child_idx = i
            i += 1

        while p != None:
            p.s = p.s - weight
            p = p.parent        
        

    def split_node(self):

        c_p = self
        c_children = c_p.children

        c1 = node("nl", 0)
        c1.set_b()
        c2 = node("nl", 0)
        c2.set_b()

        child_1 = c_children[:len(c_children)/2]
        child_2 = c_children[len(c_children)/2+1:]

        for i in range(len(child_1)):
            c1.s += (child_1[i].s * child_1[i].b)
            c1.add_child(child_1[i])
            child_1[i].child_idx = i

        for i in range(len(child_2)):
            c2.s += (child_2[i].s * child_2[i].b)
            c2.add_child(child_2[i])
            child_2[i].child_idx = i

        c_p.children = []
        c_p.add_child(c1)
        c_p.add_child(c2)



    def insertAt(self, sd, n, pos, curr_id):

        #print("Inserting at node : ", self.id, self.s)

        if len(self.children) == 0:

            thr = float(sd)/self.s
            z = np.random.random()
            descrepency = -1 * sd

            if self.id == curr_id:
                pos += 1
                ## Thats okay! Correct this later
                descrepency = 0                

            elif thr > z:
                pos += 1
                descrepency = self.s - sd

            self.parent.children.insert(pos, n)
            n.parent = self.parent
            i = 0
            for c in self.parent.children:
                c.child_idx = i
                i += 1

            #if len(self.parent.children) > 7:
                #self.parent.split_node()

            return descrepency

        i = 0
        sd_rem = sd
        descrepency = 0
        for c in self.children:
            if sd_rem < c.s:
                descrepency = c.insertAt(sd_rem, n, i, curr_id)
                break

            i += 1
            sd_rem = sd_rem - (c.s * c.b)
        return descrepency

    def set_b(self):
        self.b = 1

    def unset_b(self):
        self.b = 0

    def inorder(self):
        print(self.o_id)
        if len(self.children) == 0:
            return
        for c in self.children:
            c.inorder()


    def findNext(self):
        curr_node = self
        p_node = curr_node.parent

        while curr_node.child_idx >= len(p_node.children) - 1:
            #print("curr node : ", curr_node.id, " parent node : ", p_node.id)

            curr_node = curr_node.parent
            p_node = p_node.parent

            if p_node == None:
                return [None, 1]


        #print("All children : ", str([c.obj_id for c in p_node.children]))
        n_node = p_node.children[curr_node.child_idx + 1]
            
        while len(n_node.children) > 0:
            #print("All children : ", str([c.obj_id for c in n_node.children]))
            n_node = n_node.children[0]
            
        if n_node.obj_id == "nl":
            return [n_node, -1]

        return [n_node, 1]


    def update_till_root(self):        
        val = self.s * self.b

        p = self.parent
        while p != None:
            p.s += val
            p = p.parent

# okay decompiling treelib.cpython-37.pyc
