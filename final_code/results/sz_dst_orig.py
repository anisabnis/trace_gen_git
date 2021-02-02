import sys
from parser import *
from util import *

MIL = 1000000
dir = sys.argv[1]
mod_u = int(sys.argv[2])

if dir == "v":
    trace = "akamai2.bin"
else:
    trace = "akamai1.bin"

input = binaryParser(dir + "/" + trace)
input.open()

obj_sz = defaultdict(int)

i = 0
while True:
    i += 1
    if i > 300*MIL:
        break

    r, sz, t = input.readline()

    if mod_u < 100 and r%8 != mod_u:
        continue
    
    sz = int(float(sz)/1000)

    obj_sz[sz] += 1

    if i % 100000 == 0:
        print("i : ", i)

plot_dict(obj_sz)
plt.xlabel("sizes")
plt.ylabel("CDF")
plt.grid()
plt.legend()
if mod_u > 100:
    plt.savefig(dir + "/sz_dst.png")
else :
    plt.savefig(dir + "/sz_dst_" + str(mod_u) + ".png")

