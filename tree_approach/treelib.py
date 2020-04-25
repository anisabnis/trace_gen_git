# uncompyle6 version 3.6.6
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.7.6 (default, Dec 30 2019, 19:38:36) 
# [Clang 10.0.0 (clang-1000.11.45.5)]
# Embedded file name: /Users/asabnis/Research/trace_gen_git/tree_approach/treelib.py
# Compiled at: 2020-04-24 22:22:21
# Size of source mod 2**32: 3768 bytes
import numpy as np
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
        b = n
        while a != None:
            while b != None:
                if a.id == b.id:
                    return a.id

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
            return
        uniq_bytes = 0
        while uniq_bytes < sd:
            lca_id = curr_node.lca(next_node)
            local_uniq_bytes = 0
            curr_parent = curr_node.parent
            child_node = curr_node
            child_idx = child_node.child_idx
            while curr_parent.idx != lca_id:
                for i in range(child_idx, len(curr_parent.children)):
                    local_uniq_bytes += self.parent.children[i].s * self.parent.children[i].b

                curr_parent = curr_parent.parent
                child_node = child_node.parent

            uniq_bytes += local_uniq_bytes
            next_node = next_node.next
            curr_node = curr_node.next

        inserted_node.next = next_node

    def insertAt(self, sd, n, pos):
        if len(self.children) == 0:
            if self.obj_id != 'nl':
                print('Something disastrous has happened ')
                sys.exit()
            thr = 1 - float(sd) / self.s
            z = np.random.random()
            descrepency = -1 * sd
            if thr < z:
                pos += 1
                descrepency = self.s - sd
            self.parent.children.insert(pos, n)
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
                descrepency = c.insertAt(sd_rem, n, i)
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
        p_node = self.parent
        while curr_node.child_idx == len(p_node.children):
            curr_node = curr_node.parent
            p_node = p_node.parent

        while len(curr_node.children) > 0:
            curr_node = curr_node.children[0]

        return curr_node
# okay decompiling treelib.cpython-37.pyc
