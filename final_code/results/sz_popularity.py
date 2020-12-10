import sys
from util import *
from parser import *
from collections import defaultdict

dir = sys.argv[1]

f = open(dir + "/sampled_sizes.txt", "r")
l = f.readline()
l = l.strip().split(",")
sizes = [int(x) for x in l]
f.close()
plot_list(sizes, "generated")

input = binaryParser( dir + "/akamai2.bin")
input.open()

i = 0
obj_sizes = defaultdict()
obj_popularities = defaultdict(lambda : 0)
while True:
    r, obj_sz, t = input.readline()
    obj_sizes[r] = int(obj_sz)/1000
    obj_popularities[r] += 1

    i += 1

    #if i >= 300000000:
    #    break

    if i % 10000 == 0:
        print("Parsed : ", i)
        
    if i >= 300000000:
        break
    
    
sizes = list(obj_sizes.values())
plot_list(sizes, "orig")
plt.xscale("log")
plt.xlabel("sizes")
plt.ylabel("CDF ")
plt.legend()
plt.savefig(dir + "/sz_dst.png")
plt.clf()

f = open(dir + "/sampled_popularities.txt", "r")
l = f.readline()
l = l.strip().split(",")
pops = [int(x) for x in l]
f.close()
plot_list(pops, "generated")

pops = list(obj_popularities.values())
plot_list(pops, "orig")
plt.xlabel("popularities")
plt.ylabel("CDF")
plt.legend()
plt.xscale("log")
plt.savefig(dir + "/pop_dst.png")


