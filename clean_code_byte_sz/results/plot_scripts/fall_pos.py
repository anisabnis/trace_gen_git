import json, sys
from collections import defaultdict
import numpy as np
import matplotlib.pyplot as plt
import random
import os

w_dir = sys.argv[1]

with open("../" + w_dir + "/land_position.json", "r") as read_file:
    descrepency = json.load(read_file)

overall_land_positions = []

sum_1 = 0
sum_2 = 0
sum_3 = 0

descrepency_ = defaultdict()
for d in descrepency:
    d1 = int(d.encode('ascii', 'ignore'))
    descrepency_[d1] = descrepency[d]
    vals = descrepency[d]
    vals = [float(x) for x in vals]

    overall_land_positions.extend(vals)

    v1 = [x for x in vals if x < 0.5]
    v2 = [x for x in vals if x == 0.5]
    v3 = [x for x in vals if x > 0.5]

    sum_1 += len(v1)
    sum_2 += len(v2)
    sum_3 += len(v3)

print(" < 0.5 : ", sum_1)
print(" = 0.5 : ", sum_2)
print(" > 0.5 : ", sum_3)


if not os.path.exists("../" + w_dir + "/fall"):
    os.mkdir("../" + w_dir + "/fall")

def plot_list(vals, label):
    a = defaultdict(int)
    for v in vals:
        a[v] += 1
    
    keys = a.keys()
    keys.sort()
    vals = []
    for k in keys:
        vals.append(a[k])

    s_vals = sum(vals)
    vals = [float(v)/s_vals for v in vals]
    vals = np.cumsum(vals)    

    plt.plot(keys, vals)
    plt.grid()
    plt.xlabel("fall position")
    plt.ylabel("probability")
    plt.title("size : " + str(label))
    plt.savefig("../" + w_dir + "/fall/" + str(label) + ".png")
    plt.clf()



plot_list(overall_land_positions, "overall")

# f = open("../" + w_dir + "/sampled_sizes.txt")
# l = f.readline()
# l = l.strip().split(",")
# l = [int(x) for x in l]
# f.close()

# f = open("../" + w_dir + "/sampled_popularities.txt")
# l1 = f.readline()
# l1 = l1.strip().split(",")
# l1 = [int(x) for x in l1]
# f.close()


# keys = descrepency_.keys()
# for i in range(1000):
#     c_k = random.choice(keys)
#     vals = descrepency_[c_k]
#     if len(vals) > 100:
#         vals = [float(x) for x in vals]    
#         plot_list(vals, str(l[c_k]) + "_" + str(l1[c_k]) + "_" + str(i))

