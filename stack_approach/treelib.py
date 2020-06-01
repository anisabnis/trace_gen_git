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
        self.is_root = False
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
        

        p = self.parent
        if p.s == 0:
            p.delete_node()
        

    def rebalance(self):
        if self.is_root == True or self == None:
            return

        if len(self.children) > 8:
            self.split_node()
        self.parent.rebalance()


    def split_node(self):
        n_pos = self.child_idx

        new_node = node("nl", 0)

        rm_children = self.children[4:]
        i = 0
        rm_val = 0
        for r_c in rm_children:
            r_c.child_idx = i
            i += 1
            rm_val += (r_c.s * r_c.b)
            r_c.parent = new_node

        new_node.children = rm_children
        new_node.s = rm_val
        new_node.set_b()
        new_node.parent = self.parent
        self.parent.children.insert(n_pos + 1, new_node)

        i = 0
        for c in self.parent.children:
            c.child_idx = i
            i += 1

        self.children = self.children[:4]
        self.s = self.s - rm_val
        
    def insertAt(self, sd, n, pos, curr_id):

        if len(self.children) == 0:

            self.parent.children.insert(pos, n)            
            n.parent = self.parent

            i = 0
            for c in self.parent.children:
                c.child_idx = i
                i += 1

            n.update_till_root()
            return 1

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


    def removeAt(self, sd, n, pos, curr_id):

        if len(self.children) == 0:
            self.delete_node()
            return self

        i = 0
        sd_rem = sd
        node = None
        for c in self.children:
            if sd_rem < c.s:
                node = c.removeAt(sd_rem, n, i, curr_id)
                break
            i += 1
            sd_rem = sd_rem - (c.s * c.b)

        return node


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
            curr_node = curr_node.parent
            p_node = p_node.parent

            if p_node == None:
                return [None, 1]

        n_node = p_node.children[curr_node.child_idx + 1]
            
        while len(n_node.children) > 0:
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

    def del_till_root(self):        
        val = self.s * self.b

        p = self.parent
        while p != None:
            p.s -= val
            p = p.parent

# okay decompiling treelib.cpython-37.pyc
