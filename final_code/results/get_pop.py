from collections import defaultdict
f = open("v/out_trace.txt", "r")
l = f.readline()
l = l.strip().split(",")
obj_reqs = defaultdict(int)
for o in l:
    obj_reqs[o] += 1

keys = obj_reqs.keys()
vals = []
for k in keys:
    vals.append(obj_reqs[k])

req = [x for x in vals if x == 1]
print(len(req))
print(len(keys))
print(len(req)/len(keys))

    
    
