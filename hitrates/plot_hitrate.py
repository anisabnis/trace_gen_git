import sys
import gzip
from lru import *

data_path = "/Data/Logs/Web/US-trace/23.220.100.6_output_logs.tgz"
bytes_req = 0
bytes_hit = 0
tt = 12
b = open("hitrate_us.txt", "w")

cache = LRUCache(800000000)

p_time = 1422462171

with gzip.open(data_path, "rt") as f:
    
    for l in f:
        l = l.strip().split(" ")

        c_time = int(l[0])
        obj_id = int(l[1])
        obj_sz = float(l[2])/1000

        bytes_req += obj_sz
        
        if cache.get(obj_id) == -1:
            cache.put(obj_id, obj_sz)
        else:
            bytes_hit += obj_sz
        
        if c_time - p_time > 3600:
            p_time = c_time
            b.write(str(tt%24) + " " + str(bytes_req) + " " + str(bytes_hit) + "\n")
            b.flush()
            tt += 1
            print("processed trace worth time : ", str(tt))
            
            
        
        

