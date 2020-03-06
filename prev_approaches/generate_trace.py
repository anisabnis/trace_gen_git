import sys
import matplotlib.pylab as plt
from collections import Counter
import numpy as np
import json

def sample(values, cdf):
    z = np.random.random()
    for i in range(cdf):
        if cdf[i] > z:
            return values[i]
    return values[-1]

req_rate_dst = []
req_rate = []
f = open("data/req_rate.txt" ,"r")
i = 0
for l in f:
    i += 1
    if i < 2000:
        continue
    l = l.strip().split(" ")
    req_rate.append(int(l[0]))

req = Counter(req_rate).keys()
freq = Counter(req_rate).values()
sum_f = sum(freq)
req_rate_dst = [float(f)/sum_f for f in freq]
req_rate_dst = np.cumsum(req_rate_dst)

obj_size_dst = []
obj_size_count = json.loads("data/akamai1.bin.sizeCntReq.json")
objects = [int(obj) for obj in obj_size_count.keys()]
objects.sort()

#objects = obj_size_count.keys()








obj_pop_dst = []
footprint_d = []


