import sys
from parser import *
from collections import defaultdict
from llist import sllist
from gen_trace import *
from treelib import *
from util import *
import queue
import random


## cache_sz is the size of the cache

class LIRSCache:
    def __init__(self, cache_sz):
        self.items = defaultdict()
        self.debug = open("tmp.txt", "w")
        self.no_del = 0
        self.Q = sllist()
        self.itemsInQ = defaultdict(int)
        self.cache_size = cache_sz
        self.curr_sz = 0
        self.curr_qsize = 0
        
    def initialize(self, initial_objects, sizes, initial_times):        

        ## create a tree structure
        trace_list, self.curr_sz = gen_leaves_lirs(initial_objects, sizes, self.items, initial_times)
        st_tree, lvl = generate_tree(trace_list)
        self.root = st_tree[lvl][0]
        self.root.is_root = True
        self.curr = st_tree[0][0]
        self.last = st_tree[0][-1]
        self.prev_rid = self.root.id        
                    
        print(self.root.s)
        
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


    def putToTop(self, n):

        if n.obj_id in self.items:
        
            n.delete_node(self.debug)        
        
        p_c = self.curr.parent
        n.set_b()
        
        self.root = p_c.add_child_first_pos(n, self.debug)
        
        if self.root.id != self.prev_rid:
            print("Root id has changed ")
            self.prev_rid = self.root.id

        self.curr = n


    def insert(self, o, sz, tm):

        ## it is in stack:
        if o in self.items:
            
            n = self.items[o]

            ## if its a LIR node
            if n.lir == True:

                if self.curr.obj_id == o:
                    pass
                elif self.last.obj_id == n.obj_id:                    
                    prev, x = n.findPrevious()
                    self.putToTop(n)
                    self.last = self.prune(prev)
                else:
                    self.putToTop(n)
                return 1

            ## if its a hir node
            elif n.lir == False:
                ## if it is a resident
                if n.obj_id in self.itemsInQ:

                    item_pos = self.itemsInQ[n.obj_id]
                    self.Q.remove(item_pos)
                    del self.itemsInQ[n.obj_id]

                    ## move the node to top
                    n.setLIR()
                    self.putToTop(n)

                    ## remove last LIR node from the stack
                    ## add it to the Q, it will be a resident
                    item_pos = self.Q.appendleft(self.last)
                    self.itemsInQ[self.last.obj_id] = item_pos
                    self.last.unsetLIR()
                    self.last = self.prune(self.last)
                    
                    return 1                                        

                ## if it is a non resident, this was a cache miss
                else:
                    ## set it to a LIR node
                    
                    n.setLIR()
                    self.putToTop(n)
                    self.curr_sz += n.s

                    ## remove last LIR node from the stack
                    ## add it to the Q, it will be a resident
                    item_pos = self.Q.appendleft(self.last)
                    self.itemsInQ[self.last.obj_id] = item_pos
                    self.last.unsetLIR()
                    self.last = self.prune(self.last)
                    
                    ## evict till your used space is less than cache size
                    self.evict()

                    return -1

        ## the item is not in stack
        else:
            ## if it is a resident
            if o in self.itemsInQ:
                
                ## move the object to the begininning of the queue
                item_pos = self.itemsInQ[o]
                n = self.Q.remove(item_pos)
                item_pos = self.Q.appendleft(n)
                self.itemsInQ[o] = item_pos

                ## add object to the beginning of the stack
                self.items[o] = n                                        
                p_c = self.curr.parent
                self.root = p_c.add_child_first_pos(n, self.debug)
                self.curr = n

                return 1
                
            ## if it is not a resident
            else:
                
                n = lirsnode(o, sz)

                p_c = self.curr.parent
                self.root = p_c.add_child_first_pos(n, self.debug)
                self.curr = n
                self.curr_sz += sz
                self.items[o] = n
                
                item_pos = self.Q.appendleft(n)
                self.itemsInQ[n.obj_id] = item_pos
                
                self.evict()
            
                return -1
                

    def evict(self):
        ## evict from the Q first, if it is in the stack it should evicted from the stack as well
        while len(self.Q) > 0:

            if self.curr_sz <= self.cache_size:
                break

            n = self.Q.pop()
            
            del self.itemsInQ[n.obj_id]
            self.curr_sz -= n.s

            if n.obj_id in self.items:
                n.delete_node(self.debug)
                del self.items[n.obj_id]

        ## if curr size is still larger than cache size
        ## evict the lirs from the stack
        ## it comes to this point if the queue is empty
        ## hence the stack has only lir nodes
        curr_node = self.last
        while self.curr_sz > self.cache_size:

            prev_node, x = curr_node.findPrevious()
            curr_node.delete_node(self.debug)
            del self.items[curr_node.obj_id]

            if curr_node.lir == True:
                self.curr_sz -= curr_node.s
            curr_node = prev_node
                
        self.last = self.prune(curr_node)
        

    def prune(self, n):
        prev = n
        while prev.lir == False:
            prev.delete_node(self.debug)
            del self.items[prev.obj_id]
            prev, x = prev.findPrevious()
        return prev
    
    # def insert(self, o, sz, tm):
        
    #     if o in self.items:            

    #         n = self.items[o]

    #         ##   If the object is a  LIR
    #         if n.lir == True:
                
    #             if self.curr.obj_id == o:
    #                 return  1                
    #             self.putToTop(n)                                                           
    #             return 1

    #         else:
    #             ## It is a HIR but a resident
    #             if n.resident == True:                    
    #                 ## Then  it should be in  the queue and should also not be the last node  in  the stack
    #                 ## Remove it from  the queue and make it a LIR  and call evict
    #                 if n.obj_id not in self.itemsInQ:
    #                     print("undesirable case 1")
    #                     sys.exit()

    #                 item_pos = self.itemsInQ[n.obj_id]
    #                 self.Q.delete(item_pos)
    #                 del self.itemsInQ[n.obj_id]
    #                 n.lir  = True
    #                 self.putToTop(n)
                    
    #                 ## Need to remove the last node that is a lir in the stack
    #                 ## and add to the Q and call prune
    #                 item_pos =  self.Q.appendleft(self.last)
    #                 self.itemsInQ[self.last.obj_id] = item_pos
    #                 self.last.unsetLIR()
    #                 self.prune()
    #                 return 1
                    
                    
    #             ## It is a non-resident HIR
    #             else:
    #                 ## It is not in the Q,
    #                 ## Add it to the top stack and Q
    #                 ## And make it a resident
    #                 ## And  call evict
    #                 if n.obj_id in self.itemsInQ:
    #                     print("undesirable case  2")
    #                     sys.exit()

    #                 self.putToTop(n)
    #                 item_pos =  self.Q.appendleft(self.last)
    #                 self.itemsInQ[self.last.obj_id] = item_pos

    #                 self.curr_sz += n.s
                    
    #                 ## First try to  evict the resident HIRs
    #                 ## And then try to evict the  LIRs
    #                 self.prune()
    #                 return -1
    #     else:


    #         ## It is  a complete miss
    #         ##  Create  a new lirs node
    #         ## Add it to the top of the stack
    #         ## Make it a  resident HIR
    #         ## Add it to the queue and call evict
    #         n = lirsnode(o, sz)
    #         n.set_b()
    #         n.setResident()
            
    #         self.items[o] = n            
            
    #         p_c = self.curr.parent
    #         self.root = p_c.add_child_first_pos(n, self.debug)

    #         item_pos = self.Q.appendleft(n)
    #         self.itemsInQ[n.obj_id] = item_pos
            
    #         if self.root.id != self.prev_rid:
    #             print("Root Id has changed ")
    #             self.prev_rid = self.root.id
                            
    #         self.curr_sz += sz
    #         self.evict()
            
    #         return -1


    #     def evict(self):
            
    #         curr_node  = self.last
    #         while  self.curr_sz > self.cache_sz:
    #             curr_node.delete()
    #             if curr_node.resident == True:
    #                 self.curr_sz -= curr_node.obj_sz
    #             curr_node = curr_node.findPrevious()                
            
    #     def prune(self):
            
