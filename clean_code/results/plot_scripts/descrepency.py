import json, sys
from collections import defaultdict
import numpy as np
import matplotlib.pyplot as plt

w_dir = sys.argv[1]

with open("../" + w_dir + "/descrepency1.json", "r") as read_file:
    descrepency = json.load(read_file)

descrepency_ = defaultdict()
for d in descrepency:
    d1 = int(d.encode('ascii', 'ignore'))
    if d1 > 10 or d1 < -10:
        continue
    descrepency_[d1] = descrepency[d]

d_keys = descrepency_.keys()
d_keys.sort()
d_vals = []
for k in d_keys:
    d_vals.append(descrepency_[k])
    
sum_d = sum(d_vals)
d_vals = [float(d)/sum_d for d in d_vals]
d_vals = np.cumsum(d_vals)

plt.plot(d_keys, d_vals, label="descrepency")
plt.xlabel("Descrepency")
plt.ylabel("CDF")
plt.grid()
plt.savefig("../" + w_dir + "/descrepency1.png")



