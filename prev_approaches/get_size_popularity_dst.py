import os, sys, time, pickle, math, json
import logging
import copy
from multiprocessing import Process
import struct
from collections import defaultdict


logging.basicConfig(format='%(asctime)s: %(levelname)s: \t%(message)s', level=logging.INFO, datefmt='%H:%M:%S')

KB = 1000
MB = 1000*1000
GB = 1000*1000*1000
GiB = 1024*1024*1024

if not os.path.exists("data"):
    os.mkdir("data")


######################### request size ##########################
def cal_size_distribution(dat, req=True, obj=True):
    sz_cnt_req = defaultdict(int)
    sz_cnt_obj = defaultdict(int)
    seen_obj = defaultdict()

#     if os.path.exists("data/{}.sizeCntObj.json".format(dat.split("/")[-1])):
#         if obj:
#             with open("data/{}.sizeCntObj.json".format(dat.split("/")[-1])) as ifile:
#                 sz_cnt_obj = json.load(ifile)
#         if req:
#             with open("data/{}.sizeCntReq.json".format(dat.split("/")[-1])) as ifile:
#                 sz_cnt_req = json.load(ifile)
#         return sz_cnt_req, sz_cnt_obj

    cnt = 0

    s = struct.Struct("III")
    with open(dat, "rb") as ifile:
        b = ifile.read(12)
        while b:
            cnt += 1
            if cnt >= 2000000000:
                break
            if cnt % 100000000 == 0:
                logging.info("calculated {}".format(cnt))
            r = s.unpack(b)
            sz = r[2]
            sz_cnt_req[sz] += 1
            if r[1] not in seen_obj:
                sz_cnt_obj[sz] += 1
                seen_obj[r[1]] = 1
            else:
                seen_obj[r[1]] += 1                

            b = ifile.read(12)

    with open("data/{}.sizeCntObj.json".format(dat.split("/")[-1]), "w") as ofile:
        json.dump(sz_cnt_obj, ofile)
    ofile.close()
    with open("data/{}.sizeCntReq.json".format(dat.split("/")[-1]), "w") as ofile:
        json.dump(sz_cnt_req, ofile)
    ofile.close()
    with open("data/{}.popCntReq.json".format(dat.split("/")[-1]), "w") as ofile:
        json.dump(seen_obj, ofile)
    ofile.close()


#########################
if __name__ == "__main__":
    dat1 = "/Data/Sorted-ClusterLogs/akamai1.bin"
    cal_size_distribution(dat1)


    # cal_size_distribution(dat2)
    # plot_req_size_distr_cdf(dat1, dat2)



