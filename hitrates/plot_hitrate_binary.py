import sys
import gzip
from lru import *
import struct
import matplotlib.pyplot as plt

s = struct.Struct("III")
dat = "akamai2.bin"

bytes_req = 0
bytes_hit = 0

tt = 0
t = 1
cache = LRUCache(50000000000)

f1 = open("hitrate_wiki_" + str(t) + ".txt", "w")
f = open("cdn1_500m_sigmetrics18.tr", "r")
l = f.readline().strip().split(" ")
tm = int(l[0])
i = 0
    
for l in f:

    l = l.strip().split(" ")
    r = int(l[2])
    sz = float(l[1])/1000
    ct = int(l[0])
    bytes_req += sz
    i += 1

    if cache.get(r) == -1:
        cache.put(r, sz)
    else:
        bytes_hit += sz
        
    if ct - tm > 1000000:
        print("time taken : ", tt)
        tm = ct
        tt += 1
        f1.write(str(tt%24) + " " + str(bytes_req) + " " + str(bytes_hit) + "\n") 
        bytes_req = 0
        bytes_hit = 0


# for t in range(7,8):

#     cache = LRUCache(800000)

#     f1 = open("hitrate_trace_" + str(t) + ".txt", "w")
#     f = open("../clean_code_byte_sz/trace_" + str(t) + ".txt", "r")
#     l = f.readline().strip().split(" ")
#     tm = int(l[0])
#     i = 0
    
#     for l in f:

#         l = l.strip().split(" ")
#         r = int(l[1])
#         sz = float(l[3])/1000
#         ct = int(l[0])
#         bytes_req += sz
#         i += 1

#         if cache.get(r) == -1:
#             cache.put(r, sz)
#         else:
#             bytes_hit += sz
        
#         if ct - tm > 3600:
#             print("time taken : ", tt)
#             tm = ct
#             tt += 1
#             f1.write(str(tt%24) + " " + str(bytes_req) + " " + str(bytes_hit) + "\n") 
#             bytes_req = 0
#             bytes_hit = 0

# cache = LRUCache(800000000)

# reqs_hr = []
# r_hr = 0
# with open(dat, "rb") as ifile:
#     b = ifile.read(12)
#     r = s.unpack(b)
#     ct = r[0]
#     print(ct)
    
#     while b:
#         r = s.unpack(b)
#         sz = float(r[2])/1000
#         tm = r[0]
#         oid = r[1]
#         b = ifile.read(12)

#         r_hr += 1

#         bytes_req += sz

#         if cache.get(oid) == -1:
#             cache.put(oid, sz)
#         else:
#             bytes_hit += sz

#         if tm - ct > 3600:
#             ct = tm
#             tt += 1
#             f1.write(str(tt%24) + " " + str(bytes_req) + " " + str(bytes_hit) + "\n") 
#             print("time taken : ", tt)
#             reqs_hr.append(r_hr)
#             r_hr = 0

#         if tt > 200:
#             break
    
# plt.plot(reqs_hr)
# plt.savefig("reqs_hr_video.png")
            
# data_path = "/Data/Logs/Web/US-trace/23.220.100.6_output_logs.tgz"
# tt = 12
# b = open("hitrate_us.txt", "w")

# cache = LRUCache(800000000)

# p_time = 1422462171

# with gzip.open(data_path, "rt") as f:
    
#     for l in f:
#         l = l.strip().split(" ")

#         c_time = int(l[0])
#         obj_id = int(l[1])
#         obj_sz = float(l[2])/1000

#         bytes_req += obj_sz
        
#         if cache.get(obj_id) == -1:
#             cache.put(obj_id, obj_sz)
#         else:
#             bytes_hit += obj_sz
        
#         if c_time - p_time > 3600:
#             p_time = c_time
#             b.write(str(tt%24) + " " + str(bytes_req) + " " + str(bytes_hit) + "\n")
#             b.flush()
#             tt += 1
#             print("processed trace worth time : ", str(tt))
            
            
        
        

