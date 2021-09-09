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

i = 0
total_bytes_req = 0
st_time = 0
end_time = 0

obj_sizes = defaultdict()

uniq_bytes = 0
while True:
    try:
        r, obj_sz, t = input.readline()
    except:
        break

    if i == 0:
        st_time = t

    end_time = t

    i += 1
    obj_sz = int(float(obj_sz)/1000)
    if obj_sz <= 0:
        obj_sz = 1

    if r not in obj_sizes:
        uniq_bytes += obj_sz
        obj_sizes[r] = obj_sz
        
    total_bytes_req += obj_sz
    if i % 1000000 == 0:
        print("i : ", i)
    
f = open("trace_prop.txt", "a")
f.write(tc + " total_reqs : " + str(i) + "\n")
f.write(tc + " total_bytes : " + str(total_bytes_req) + "\n")
f.write(tc + " total_time : " + str(end_time - st_time) + "\n")
f.write(tc + " uniq_bytes : " + str(uniq_bytes) + "\n")
f.write(tc + " total_objects : " + str(len(obj_sizes)) + "\n") 
