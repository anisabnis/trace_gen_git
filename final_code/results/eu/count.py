from collections import defaultdict
obj_ = defaultdict(int)
f = open("byte_out_trace_mix.txt", "r")
l = f.readline()
l = l.strip().split(",")
for r in l:
    obj_[r] += 1
print(len(list(obj_.keys())))
