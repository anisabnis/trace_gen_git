import sys
import matplotlib.pyplot as plt

dir = sys.argv[1]
mod_u = int(sys.argv[2])

# f = open(dir + "/generated.stats1000000000_lrusm_unit.txt", "r")
# generated = []

# hit = 0
# req = 0
# for l in f:
#     l = l.strip().split(" ")
#     hit += int(l[-1])
#     req += int(l[1])
#     p = float(hit)/req
#     generated.append(p)

# f.close()

if mod_u < 100:
    f = open(dir + "/original.stats8000000000_" + str(mod_u) + ".txt", "r")
else:
    f = open(dir + "/original.stats1000000000.txt", "r")
    
original = []
original_obj = []
hit = 0
req = 0
hit_o = 0
req_o = 0
for l in f:
    l = l.strip().split(" ")
    hit += int(l[-1])
    req += int(l[1])
    p = float(hit)/req
    original.append(p)

    hit_o += int(l[-2])
    req_o += int(l[0])
    p = float(hit_o)/req_o
    original_obj.append(p)
    
f.close()

#plt.plot(generated, label="generated")
plt.plot(original, label="original_byte")
plt.plot(original_obj, label="original_obj")
plt.legend()
plt.grid()
if mod_u > 100:
    plt.savefig(dir + "/hitrate.png")
else:
    plt.savefig(dir + "/hitrate_" + str(mod_u) + ".png")
    









