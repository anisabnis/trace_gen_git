import os, sys, time, pickle, math, json
from multiprocessing import Process
import struct
import logging
import numpy as np
from collections import defaultdict

logging.basicConfig(format='%(asctime)s: %(levelname)s: \t%(message)s', level=logging.INFO, datefmt='%H:%M:%S')

if not os.path.exists("data_30"):
    os.mkdir("data_30")


def divide(value, divide_by):
    value = value >> divide_by
    return value


def generate_sub_trace(dat, sz_gran = 10, sample_rate=30000, pop=True, obj=True):
    sz_cnt_obj = defaultdict(int)
    pop_cnt_obj = defaultdict(int)
    
#     if os.path.exists("data/{}.sizeCntObj.json".format(dat.split("/")[-1])):
#         if obj:
#             with open("data/{}.sizeCntObj.json".format(dat.split("/")[-1])) as ifile:
#                 sz_cnt_obj = json.load(ifile)
#         if pop:
#             with open("data/{}.popCntObj.json".format(dat.split("/")[-1])) as ifile:
#                 pop_cnt_req = json.load(ifile)

#         return sz_cnt_obj, pop_cnt_obj


    f = open("data_30/sub_trace.txt", "w")

    seen_obj = set()
    cnt = 1

    s = struct.Struct("III")

    with open(dat, "rb") as ifile:
        b = ifile.read(12)

        while b:
            cnt += 1
            if cnt % 100000000 == 0:
                logging.info("calculated {}".format(cnt))
                #break

            r = s.unpack(b)
            o_id = r[1]

            if o_id % sample_rate != 0:
                b = ifile.read(12)
                continue
            
            sz = divide(int(r[2]), sz_gran)
            pop_cnt_obj[o_id] += 1
            
            if r[1] not in seen_obj:
                sz_cnt_obj[sz] += 1
                seen_obj.add(r[1])

            st = [str(x) for x in r]
            st = " ".join(st)
            f.write(st)
            f.write("\n")
            b = ifile.read(12)

    f.close()

    with open("data_30/{}.sizeCntObj.json".format(dat.split("/")[-1]), "w") as ofile:
        json.dump(sz_cnt_obj, ofile)

    with open("data_30/{}.popCntObj.json".format(dat.split("/")[-1]), "w") as ofile:
        json.dump(pop_cnt_obj, ofile)

    return sz_cnt_obj, pop_cnt_obj


if __name__ == "__main__":

    dat = "/Data/Sorted-ClusterLogs/akamai1.bin"
    generate_sub_trace(dat)    
    


