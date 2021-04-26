import sys
from parser import *
from collections import defaultdict
from gen_trace import *
from treelib import *
from util import *
import random

class RNDCache:
    def __init__(self, max_sz):
        self.max_sz = max_sz
        self.items = defaultdict()
        self.curr_sz = 0
        self.debug = open("tmp.txt", "w")
        self.no_del = 0
        
    def initialize(self, initial_objects, sizes, initial_times):        

        ## create a tree structure
        trace_list, self.curr_sz = gen_leaves(initial_objects, sizes, self.items, initial_times)
        st_tree, lvl = generate_tree(trace_list)
        root = st_tree[lvl][0]
        root.is_root = True
        self.curr = st_tree[0][0]
        self.prev_rid = root.id        
                    
        print(root.s)
        
    def print_cache(self):
        tmp = self.curr
        while tmp != None:
            print(tmp.obj_id, tmp.s)
            tmp, s = tmp.findNext()

    def uniq_bytes(self, n):
        tmp = self.curr
        ubytes = 0
        while tmp != None:
            #print tmp.obj_id, tmp.s
            ubytes += tmp.s
            tmp, s = tmp.findNext()

            if tmp.obj_id == n.obj_id:
                break

        return ubytes            
        
            
    def insert(self, o, sz, tm):
        
        if o in self.items:            

            # n = self.items[o]
            # dt = tm - n.last_access
            
            # if self.curr.obj_id == o:
            #     return 0, dt
            
            # sd = self.curr.findUniqBytes(n, self.debug) + self.curr.s + n.s
            
            # n.delete_node(self.debug)
            # sd = 1
            
            # self.curr_sz -= n.s
            
            # p_c = self.curr.parent

            # n.s = sz
            # self.curr_sz += sz
            # n.last_access = tm
            
            # n.set_b()
            # self.root = p_c.add_child_first_pos(n, self.debug)
            
            # if self.root.id != self.prev_rid:
            #     print("Root Id has changed ")
            #     self.prev_rid = self.root.id
                
            # self.curr = n

            
            return 1,0
            
        else:

            n = node(o, sz)
            n.set_b()
            n.last_access = tm
            
            self.items[o] = n

            p_c = self.curr.parent
            self.root = p_c.add_child_first_pos(n, self.debug)

            if self.root.id != self.prev_rid:
                print("Root Id has changed ")
                self.prev_rid = self.root.id
                            
            self.curr = n            
            self.curr_sz += sz
            
            sd = -1
            dt = -1

        ## if cache not full
        while self.curr_sz > self.max_sz:
            try:
                sz, obj = self.root.delete_random_node(self.debug)
                self.curr_sz -= sz
                del self.items[obj]
                self.no_del += 1
            except:
                print("no of deletions : ", self.no_del, self.curr_sz, o)
                asdf                    
            
        return sd, dt
