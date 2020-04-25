import os, sys, time, pickle, math, json
import numpy as np
from collections import defaultdict
import struct

data_path = "/mnt/nfs/scratch1/asabnis/data/binary/"
dat_file = data_path + "akamai1.bin"
num_dirs = 100

o_files = []
for i in range(num_dirs):
    if not os.path.exists(data_path + "small/" + str(i)):
        os.mkdir(data_path + "small/" + str(i))
    f = open(data_path + "small/" + str(i) + "/subtrace.txt", "w")
    o_files.append(f)

sz_cnt_obj = defaultdict(int)
pop_cnt_obj = defaultdict(int)
seen_obj = set()
cnt = 0

s = struct.Struct("III")
with open(dat_file, "rb") as ifile:
    b = ifile.read(12)
    while b:
        cnt += 1        

        if cnt > 1500000000:
            break

        r = s.unpack(b)
        sz = r[2]
        oid = r[1]    
        pop_cnt_obj[oid] += 1

        oid_bucket = oid%100        
        t_line = " ".join([str(x) for x in r])
        o_files[oid_bucket].write(t_line + "\n")
        
        if oid not in seen_obj:
            sz_cnt_obj[sz] += 1
            seen_obj.add(oid)

        b = ifile.read(12)

with open("/mnt/nfs/scratch1/asabnis/data/binary/small/{}.sizeCntObj.json".format(dat_file.split("/")[-1]), "w") as ofile:
    json.dump(sz_cnt_obj, ofile)
with open("/mnt/nfs/scratch1/asabnis/data/binary/small/{}.popCntObj.json".format(dat_file.split("/")[-1]), "w") as ofile:
    json.dump(pop_cnt_obj, ofile)

