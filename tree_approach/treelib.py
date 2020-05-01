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

        print('LCA : Parent connections not correct')
        sys.exit()

    def add_child(self, n):
        n.child_idx = len(self.children)
        self.children.append(n)
        n.parent = self

    def set_parent(self, n):
        self.parent = n

    def set_next(self, n):
        self.next = n

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

            lca_id = curr_node.lca(next_node)

            #print("curr_node : ", curr_node.id, curr_node.obj_id)
            #print("next_node : ", next_node.id, curr_node.obj_id)
            #print("LCA found : ", lca_id)

            local_uniq_bytes = 0

            ### This is going from curr_node to the LCA
            curr_parent = curr_node.parent
            child_node = curr_node
            child_idx = child_node.child_idx
            
            to_del_nodes.append(curr_node)

            while curr_parent.id != lca_id:
                #print("child_idx : ", child_idx, " and currently at parent : ", curr_parent.id , " and child : ", child_node.id)
                
                if child_idx == len(curr_parent.children):
                    curr_parent = curr_parent.parent
                    child_node  = child_node.parent
                    child_idx   = child_node.child_idx
                    continue

                for i in range(child_idx + 1, len(curr_parent.children)):
                    lb = curr_parent.children[i].s * curr_parent.children[i].b
                    #print("lb added 1 : ", lb, i, curr_parent.children[i].id)
                    local_uniq_bytes += lb

                curr_parent = curr_parent.parent
                child_node  = child_node.parent
                child_idx   = child_node.child_idx

            #print("Local unique bytes 1 : ", local_uniq_bytes, curr_node.id, next_node.id)

            ### This is going from next_node to the LCA
            curr_parent = next_node.parent
            child_node = next_node
            child_idx = child_node.child_idx

            while curr_parent.id != lca_id:

                #print("child_idx : ", child_idx)

                if child_idx == 0:
                    curr_parent = curr_parent.parent
                    child_node  = child_node.parent
                    child_idx   = child_node.child_idx
                    continue

                for i in range(0, child_idx):
                    lb = curr_parent.children[i].s * curr_parent.children[i].b
                    #print("lb added 2 : ", lb, i, curr_parent.children[i].id)
                    local_uniq_bytes += lb

                curr_parent = curr_parent.parent
                child_node  = child_node.parent
                child_idx   = child_node.child_idx

            #print("Local unique bytes 2 : ", local_uniq_bytes, curr_node.id, next_node.id)

            uniq_bytes += local_uniq_bytes
            next_node = next_node.next
            curr_node = curr_node.next


        for d in to_del_nodes:
            inserted_node.next = d.next
            d.delete_node()
        inserted_node.set_b()
        #print("Unique Bytes : ", uniq_bytes)

    def delete_node(self):
        weight = self.s * self.b
        p = self.parent
        self.parent.children = [c for c in self.parent.children if c.id != self.id]

        i = 0
        for c in self.parent.children:
            c.child_idx = i
            i += 1

        while p != None:
            p.s = p.s - weight
            p = p.parent


    def insertAt(self, sd, n, pos, curr_id):

        print("Inserting at node : ", self.id, self.s)

        if len(self.children) == 0:

            if self.id == curr_id:
                print("Adding at the same position")
                return "Na"

            thr = 1 - float(sd)/self.s
            z = np.random.random()
            descrepency = -1 * sd

            if thr < z:
                pos += 1
                descrepency = self.s - sd

            self.parent.children.insert(pos, n)
            n.parent = self.parent

            i = 0
            for c in self.parent.children:
                c.child_idx = i
                i += 1

            return descrepency

        i = 0
        sd_rem = sd
        descrepency = 0
        for c in self.children:
            if sd_rem < c.s:
                descrepency = c.insertAt(sd_rem, n, i, curr_id)
                break

            i += 1
            sd_rem = sd_rem - c.s
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
            print("curr node : ", curr_node.id, " parent node : ", p_node.id)

            curr_node = curr_node.parent
            p_node = p_node.parent

            if p_node == None:
                return None


        print("All children : ", str([c.obj_id for c in p_node.children]))
        n_node = p_node.children[curr_node.child_idx + 1]
            
        while len(n_node.children) > 0:
            print("All children : ", str([c.obj_id for c in n_node.children]))
            n_node = n_node.children[0]
            
        return n_node


    def update_till_root(self):        
        val = self.s * self.b

        print("Val to be updated : ", val)

        p = self.parent
        while p != None:
            print("Updating the value for : ", p.id)
            p.s += val
            p = p.parent

# okay decompiling treelib.cpython-37.pyc
