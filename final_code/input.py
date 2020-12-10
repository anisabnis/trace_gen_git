import sys
from parser import *
from collections import defaultdict
from gen_trace import *
from treelib import *
from util import *
import random

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

dir = sys.argv[1]
t_file = sys.argv[2]

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
            print tmp.obj_id, tmp.s
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

        #print("inserting object ", o, " of size ", sz)
        
        if o in self.items:            
            
            if self.curr.obj_id == o:
                return 0

            n = self.items[o]

            #print("uniq bytes : ", self.uniq_bytes(n))
            
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

        #self.print_cache()
        return sd
                


parser = binaryParser(dir + "/" + t_file + "/akamai2.bin")
parser.open()

lru = cache(10000000000)

initial_objects = list()

## Required quantities to be processed later
obj_sizes = defaultdict(int)
sd_distances = defaultdict(list)
obj_reqs = defaultdict(int)


##### The code is for testing
# lru = cache(15)

# i = 0
# while True:
#     obj, sz = parser.readline()
#     sz = 1#int(sz)/1000
#     obj_reqs[obj] += 1
    
#     if obj not in obj_sizes:
#         initial_objects.append(obj)
#         obj_sizes[obj] = sz
        
#     if len(obj_sizes) > 7:
#         break

# lru.initialize(initial_objects, obj_sizes)

# for i in range(10000):
#     r_no = np.random.randint(100)
#     sd = lru.insert(r_no, 1)
#     print(sd)
    
# asdf

##### Testing code ends


i = 0
while True:
    obj, sz = parser.readline()
    sz = np.ceil(float(sz)/1000)
    obj_reqs[obj] += 1
    
    if obj not in obj_sizes:
        initial_objects.append(obj)
        obj_sizes[obj] = sz
        
    if len(obj_sizes) > 1023:
        break

lru.initialize(initial_objects, obj_sizes)

i = 0
max_len = 500000000

while True:
    obj, sz = parser.readline()
    
    sz = np.ceil(float(sz)/1000)
    
    obj_sizes[obj] = sz
    obj_reqs[obj] += 1
    
    try:
        sd = lru.insert(obj, sz)
    except :
        print("Number of requests : ", i, lru.curr_sz, lru.no_del, obj)
        #lru.print_cache()
        asdf
        
    if sd != -1:
        sd_distances[obj].append(sd)

    i += 1

    if i%100000 == 0:
        print("Processed : ", i)

    if i > max_len:
        break
        


### Stats Writing - write this in a differnet function -- looks dirty
    
fd_popularity = defaultdict(list)
for oid in sd_distances:
    popularity = obj_reqs[oid]
    fd_popularity[popularity].extend(sd_distances[oid])

f = open(dir + "/" + t_file + "/fd_bytes.txt", "w")
for p in fd_popularity:
    f.write(str(p) + "\n")
    keys, vals = convert_to_dict(fd_popularity[p], max_len)
    for i in range(len(keys)):
        f.write(str(keys[i]) + " " + str(vals[i]) + "\n")
f.close()

f = open(dir + "/" + t_file + "/joint_dst.txt", "w")
pop_sz = defaultdict(list)
for obj in obj_sizes:
    popularity = obj_reqs[obj]
    pop_sz[popularity].append(obj_sizes[obj])

for p in pop_sz:
    f.write(str(p) + "\n")
    keys, vals = convert_to_dict(pop_sz[p], max_len, 2)
    for i in range(len(keys)):
        f.write(str(keys[i]) + " " + str(vals[i]) + "\n")
f.close()



    
        


