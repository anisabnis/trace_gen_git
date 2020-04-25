import os, sys, time, pickle, math, json
import numpy as np
from collections import defaultdict
import struct

data_path = "/mnt/nfs/scratch1/asabnis/data/binary/"
dat_file = data_path + "akamai1.bin"
num_dirs = 100

sz_cnt_obj = defaultdict(int)
pop_cnt_obj = defaultdict(int)
seen_obj = set()
cnt = 0

s = struct.Struct("III")
with open(dat_file, "rb") as ifile:
    b = ifile.read(12)
    while b:
        cnt += 1        
        r = s.unpack(b)
        sz = r[2]
        oid = r[1]    
        pop_cnt_obj[oid] += 1

        if oid not in seen_obj:
            sz_cnt_obj[sz] += 1
            seen_obj.add(oid)

        b = ifile.read(12)


with open("/mnt/nfs/scratch1/asabnis/data/binary/{}.sizeCntObj.json".format(dat_file.split("/")[-1]), "w") as ofile:
    json.dump(sz_cnt_obj, ofile)
with open("/mnt/nfs/scratch1/asabnis/data/binary/{}.popCntObj.json".format(dat_file.split("/")[-1]), "w") as ofile:
    json.dump(pop_cnt_obj, ofile)
