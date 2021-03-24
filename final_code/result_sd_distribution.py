import sys
from parser import *
from collections import defaultdict
from gen_trace import *
from treelib import *
from util import *
import random

TB = 1000000000
MIL = 1000000

def get_dict(x, max_len):
    keys = list(x.keys())
    keys.sort()
    vals = []

    for k in keys:
        vals.append(x[k])

    vals = [float(x)/max_len for x in vals]
    return keys, vals

def get_dict_2(x, max_len):

    keys = list(x.keys())
    keys.sort()
    vals = []

    for k in keys:
        vals.append(x[k])

    max_len = sum(vals)
    vals = [float(x)/max_len for x in vals]

    return keys, vals

def convert_to_dict(x, max_len, type=1):
    a = defaultdict(int)

    for v in x:
        a[v] += 1

    if type==1:
        keys, vals = get_dict(a, max_len)
    else :
        keys, vals = get_dict_2(a, max_len)
        
    return keys, vals

## Get the input parameters
t_file = sys.argv[1]


## objects are assumed to be in KB
class cache:
    def __init__(self, max_sz):
        self.max_sz = max_sz
        self.items = defaultdict()
        self.curr_sz = 0
        self.debug = open("tmp.txt", "w")
        self.no_del = 0
        
    def initialize(self, inital_objects, sizes):        

        ## create a tree structure
        trace_list, self.curr_sz = gen_leaves(initial_objects, sizes, self.items)
        st_tree, lvl = generate_tree(trace_list)
        root = st_tree[lvl][0]
        root.is_root = True
        self.curr = st_tree[0][0]
        self.prev_rid = root.id        
        print(self.curr_sz)

        
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
        
            
    def insert(self, o, sz):
        
        if o in self.items:            

            n = self.items[o]
            
            if self.curr.obj_id == o:
                return 0
            
            sd = self.curr.findUniqBytes(n, self.debug) + self.curr.s
            
            n.delete_node(self.debug)
            
            p_c = self.curr.parent

            n.s = sz
            
            n.set_b()
            self.root = p_c.add_child_first_pos(n, self.debug)
            
            if self.root.id != self.prev_rid:
                print("Root Id has changed ")
                self.prev_rid = self.root.id
                
            self.curr = n
            
        else:

            n = node(o, sz)
            n.set_b()
            
            self.items[o] = n

            p_c = self.curr.parent
            self.root = p_c.add_child_first_pos(n, self.debug)

            if self.root.id != self.prev_rid:
                print("Root Id has changed ")
                self.prev_rid = self.root.id
                            
            self.curr = n
            
            self.curr_sz += sz
            
            ## if cache not full
            while self.curr_sz > self.max_sz:
                try:
                    sz, obj = self.root.delete_last_node(self.debug)
                    self.curr_sz -= sz
                    del self.items[obj]
                    self.no_del += 1
                except:
                    print("no of deletions : ", self.no_del, obj, o)
                    asdf
                    
            sd = -1
            
        return sd
    
#parser = listParser("results/" + t_file + "/generated_traces/out_trace_all.txt")
parser = listParser("results/" + t_file + "/out_trace_pop_init.txt")
parser.open()

f = open("results/" + t_file + "/sampled_sizes_pop_init.txt", "r")
sizes = f.readline().strip().split(",")
sizes = [int(x) for x in sizes]

lru = cache(10*TB)

initial_objects = list()

## Required quantities to be processed later
sd_distances = defaultdict(int)

i = 0
bytes_in_cache = 0
line_count = 0

obj_sizes = {}

while bytes_in_cache < 2*TB:

    obj = parser.readline()

    sz = sizes[obj]
    
    line_count += 1    
    
    if obj not in obj_sizes:

        obj_sizes[obj] = sz
        
        initial_objects.append(obj)
    
        bytes_in_cache += sz
        
    if line_count % 10000 == 0:
        print("lines counted : ", line_count, bytes_in_cache)
    
    i += 1
    

lru.initialize(initial_objects, sizes)

line_count = 0
max_len = parser.length() - i - 100
#max_len = 10000
total_bytes_req = 0
total_reqs = 0
total_misses = 0
flags = 0

i = 0
total_requests = 0

## Stack distance is grouped in multiples of 200 MB and inter-arrival time in 200 seconds
while True:
    obj = parser.readline()
    line_count += 1
    
    if line_count%100000 == 0:
        print("Processed : ", line_count)        
    
    sz = sizes[obj]

    total_requests += 1
    sd = lru.insert(obj, sz)
    
    if sd != -1:
        sd = float(sd)/400000
        sd = int(sd) * 400000
        sd_distances[sd] += 1
    else:
        sd_distances[sd] += 1
        total_misses += 1
    
    i += 1
    
    if line_count > max_len:
        break

f = open("results/" + t_file + "/footprint_desc_constructed_pop_init.txt", "w")
keys, vals = get_dict_2(sd_distances, max_len)
for i in range(len(keys)):
    f.write(str(keys[i]) + " " + str(vals[i]) + "\n")
f.close()



