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
obj_mod = sys.argv[2]

print(t_file, obj_mod)

obj_mod = [int(x) for x in obj_mod]

#obj_mod = int(sys.argv[2])
#if obj_mod > 7:
#    sys.exit(0)

if t_file == "v":
    inp_file = "akamai2.bin"
elif t_file == "w":
    inp_file = "akamai1.bin"
elif t_file.find("eu") != -1:
    inp_file = t_file
elif t_file == "tc":
    inp_file = "all.gz"
else:
    sys.exit()



## objects are assumed to be in KB
class cache:
    def __init__(self, max_sz):
        self.max_sz = max_sz
        self.items = defaultdict()
        self.curr_sz = 0
        self.debug = open("tmp.txt", "w")
        self.no_del = 0
        
    def initialize(self, inital_objects, sizes, initial_times):        

        ## create a tree structure
        trace_list, self.curr_sz = gen_leaves(initial_objects, sizes, self.items, initial_times)
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
        
            
    def insert(self, o, sz, tm):
        
        if o in self.items:            

            n = self.items[o]
            dt = tm - n.last_access
            
            if self.curr.obj_id == o:
                return 0, dt
            
            sd = self.curr.findUniqBytes(n, self.debug) + self.curr.s + n.s
            
            n.delete_node(self.debug)
            
            p_c = self.curr.parent

            n.s = sz
            n.last_access = tm
            
            n.set_b()
            self.root = p_c.add_child_first_pos(n, self.debug)
            
            if self.root.id != self.prev_rid:
                print("Root Id has changed ")
                self.prev_rid = self.root.id
                
            self.curr = n
            
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
            dt = -1
            
        return sd, dt
                

if t_file == "v" or t_file == "w":
    parser = binaryParser("/mnt/nfs/scratch1/asabnis/data/binary/" + inp_file)
elif t_file == "tc":
    parser = allParser("/mnt/nfs/scratch1/asabnis/trace_gen/tc/all.gz")
else:
    parser = euParser("/mnt/nfs/scratch1/asabnis/data/binary/" + inp_file)
    
parser.open()

lru = cache(10*TB)
initial_objects = list()
initial_times = {}

## Required quantities to be processed later
obj_sizes = defaultdict(int)
obj_iats  = defaultdict(list)
sd_distances = defaultdict(lambda : defaultdict(lambda : 0))
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
bytes_in_cache = 0
line_count = 0

while bytes_in_cache < 1*MIL:
    try:
        obj, sz, tm, tc = parser.readline()
    except:
        print("here")
        sys.exit()

    line_count += 1

    if line_count % 10000 == 0:
        print("lines counted : ", line_count, bytes_in_cache)
        
    if tc not in obj_mod:
        continue
    
    sz = np.ceil(float(sz)/1000)

    obj_reqs[obj] += 1

    obj_iats[obj].append(-1)
    
    if obj not in obj_sizes:

        initial_objects.append(obj)
        
        obj_sizes[obj] = sz

        bytes_in_cache += sz

    initial_times[obj] = tm
            
    i += 1
    

lru.initialize(initial_objects, obj_sizes, initial_times)

i = 0
line_count = 0
max_len = 300000000
#max_len = 100000000
#max_len = 300000
start_tm = 0
total_bytes_req = 0
total_reqs = 0
total_misses = 0
bytes_miss = 0

## Stack distance is grouped in multiples of 200 MB and inter-arrival time in 200 seconds
while True:
    try:
        obj, sz, tm, tc = parser.readline()
    except:
        break

    line_count += 1

    if i == 0:
        start_tm = tm    
    
    if line_count%100000 == 0:
        print("Processed : ", line_count)
    
    if tc not in obj_mod:
        continue
    
    sz = np.ceil(float(sz)/1000)
    
    obj_sizes[obj] = sz
    obj_reqs[obj] += 1

    total_bytes_req += sz
    total_reqs += 1 
   
    k = lru.insert(obj, sz, tm)

    sd, iat = k
    
    if sd != -1:
        sd = float(sd)/200000
        sd = int(sd) * 200000
        iat = float(iat)/200
        iat = int(iat) * 200        
        sd_distances[iat][sd] += sz
    else:
        total_misses += 1
        bytes_miss += sz

    obj_iats[obj].append(iat)
        
    i += 1
    
    if line_count > max_len:
        break

end_tm = tm        
### Stats Writing - write this in a differnet function -- looks dirty    
    
obj_mod = "".join([str(x) for x in obj_mod])
f = open("/mnt/nfs/scratch1/asabnis/trace_gen/" + t_file + "/All/byte_footprint_desc_" + str(obj_mod) + ".txt", "w")
## Write the other stats into the file
f.write(str(total_reqs) + " " + str(total_bytes_req) + " " + str(start_tm) + " " + str(end_tm) + " " + str(total_misses) + " " + str(bytes_miss) + "\n")
iat_keys = list(sd_distances.keys())
iat_keys.sort()
for iat in iat_keys:
    sd_keys = sd_distances[iat].keys()
    sd_keys.sort()
    for sd in sd_keys:
        count = sd_distances[iat][sd]
        count = float(count)/total_bytes_req
        f.write(str(iat) + " " + str(sd) + " " + str(count) + "\n") 
f.close()

avg_obj_iat = defaultdict(int)
no_objects = 0
one_hits = 0
for obj in obj_iats:
    if len(obj_iats[obj]) > 1:
        iat = np.mean(obj_iats[obj][1:])/200
        iat = int(iat) * 200        
    else:
        iat = -1
        one_hits += 1
        
    avg_obj_iat[obj] = iat
    no_objects += 1    
f = open("/mnt/nfs/scratch1/asabnis/trace_gen/" + t_file + "/All/one_hits_" + str(obj_mod) + ".txt", "w")
f.write(str(one_hits) + " " + str(no_objects) + "\n")
f.close()


#write iat sz distribution
iat_sz = defaultdict(list)
for obj in obj_sizes:
    iat = avg_obj_iat[obj]
    iat_sz[iat].append(obj_sizes[obj])
    
f = open("/mnt/nfs/scratch1/asabnis/trace_gen/" + t_file + "/All/iat_sz_" + str(obj_mod) + ".txt", "w")
j = 0
for iat in iat_sz:
    f.write(str(iat) + "\n")
    keys, vals = convert_to_dict(iat_sz[iat], no_objects)
    j += 1
    if j % 10000 == 0:
        print("Parsed : ", j)        
    for i in range(len(keys)):
        f.write(str(keys[i]) + " " + str(vals[i]) + "\n")
f.close()





    
        


