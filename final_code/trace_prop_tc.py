import sys
from lru import *
from fifo import *
from util import *
from parser import *
from random_cache import *
from collections import defaultdict
import random

tc = sys.argv[1]

if tc == "w":
    input = binaryParser("results/" + str(tc) + "/akamai1.bin")
elif tc == "v":
    input = binaryParser("results/" + str(tc) + "/akamai2.bin")
elif tc == "eu":
    input = euParser("results/" + str(tc) + "/all_sort_int")
elif tc == "tc":
    input = allParser("results/" + str(tc) + "/all.gz")    
input.open()

total_bytes_req = defaultdict(lambda : 0)
st_time = defaultdict(lambda : 10000000000)
end_time = defaultdict(lambda : 0)
total_reqs = defaultdict(lambda : 0)
obj_sizes = defaultdict(lambda: defaultdict())
uniq_bytes = defaultdict(lambda : 0)
i = 0

while True:
    try:
        r, obj_sz, t, tc = input.readline()
    except:
        break

    if total_reqs[tc] == 0:
        st_time[tc] = t

    total_reqs[tc] += 1
        
    end_time[tc] = t

    i += 1
    obj_sz = int(float(obj_sz)/1000)
    if obj_sz <= 0:
        obj_sz = 1

    if r not in obj_sizes[tc]:
        uniq_bytes[tc] += obj_sz
        obj_sizes[tc][r] = obj_sz
        
    total_bytes_req[tc] += obj_sz

    if i % 1000000 == 0:
        print("i : ", i)
    
f = open("trace_prop_tc.txt", "a")
for tc in total_bytes_req:
    f.write(str(tc) + " total_reqs : " + str(total_reqs[tc]) + "\n")
    f.write(str(tc) + " total_bytes : " + str(total_bytes_req[tc]) + "\n")
    f.write(str(tc) + " total_time : " + str(end_time[tc] - st_time[tc]) + "\n")
    f.write(str(tc) + " uniq_bytes : " + str(uniq_bytes[tc]) + "\n")
    f.write(str(tc) + " total_objects : " + str(len(obj_sizes[tc])) + "\n") 
