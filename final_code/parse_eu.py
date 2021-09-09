f = open("trace_prop_eu.txt", "r")

from collections import defaultdict
l = f.readline()
key = 0
prop = defaultdict()

for l in f:

    l = l.strip().split(" ")

    if int(l[0]) != key:
        print(key, prop)
        print("total requests : ", prop["total_reqs"])
        print("requests/time : ", prop["total_reqs"]/prop["total_time"])
        print("number of objects  : ", prop["total_objects"])
        print("volume  : ", float(prop["total_bytes"])/prop["total_time"])
        print("avg object size : ", float(prop["uniq_bytes"])/prop["total_objects"])
        key = int(l[0])
        prop = defaultdict()

    prop[l[1]] = int(l[3])
        
