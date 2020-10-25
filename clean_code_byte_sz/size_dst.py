import sys
from lru import *
from fifo import *
from util import *

tc = int(sys.argv[1])

f = open("results/" + str(tc) + "/out_trace.txt" , "r")
reqs = f.readline()
reqs = reqs.strip().split(",")
reqs = [int(r) for r in reqs if r != '']
f.close()

f = open("results/" + str(tc) + "/sampled_sizes.txt", "r")
sizes = f.readline()
sizes = sizes.strip().split(",")
sizes = [int(s) for s in sizes if s != '']
f.close()

### First run the requests for lru and fifo
size_gen = defaultdict(int)
pop_gen = defaultdict(int)
for r in reqs:
    r = int(r)
    obj_sz = int(sizes[r])
    size_gen[obj_sz] += 1
    pop_gen[r] += 1
print("number of objects sampled : ", len(size_gen.keys()))

size_gen_subset = defaultdict(int)
for sz in size_gen:
    if sz < 100:
        size_gen_subset[sz] = size_gen[sz]

popularity_g = defaultdict(int)
for o in pop_gen:
    no_r = pop_gen[o]
    popularity_g[no_r] += 1

popularity_g_subset = defaultdict(int)
for o in popularity_g:
    if o < 100:
        no_r = popularity_g[o]
        popularity_g_subset[o] = no_r

## run the requests 
sizes_real = defaultdict(int)
pop_real = defaultdict(int)
f1 = open("all_sort_int", "r")
i = 0
for l in f1:
    l = l.strip().split(" ")
    t = int(l[2])
    if t != tc:
        continue

    i += 1
    if i > len(reqs):
        break
    r = int(l[1])
    pop_real[r] += 1
    obj_sz = int(int(l[3])/1000)
    sizes_real[obj_sz] += 1
f1.close()

size_real_subset = defaultdict(int)
for sz in sizes_real:
    if sz < 100:
        size_real_subset[sz] = sizes_real[sz]

popularity_r = defaultdict(int)
for o in pop_real:
    no_r = pop_real[o]
    popularity_r[no_r] += 1

popularity_r_subset = defaultdict(int)
for o in popularity_r:
    if o < 100:
        no_r = popularity_r[o]
        popularity_r_subset[o] = no_r


print("number of objects real : ", len(sizes_real.keys()))

plot_dict(sizes_real, "real")
plot_dict(size_gen, "sampled")
plt.grid()
plt.legend()
plt.savefig("results/" + str(tc) + "/size_dst.png")
plt.clf()

plot_dict(popularity_r, "real")
plot_dict(popularity_g, "sampled")
plt.grid()
plt.legend()
plt.savefig("results/" + str(tc) + "/popularity_dst.png")
plt.clf()


plot_dict(popularity_r_subset, "real")
plot_dict(popularity_g_subset, "sampled")
plt.grid()
plt.legend()
plt.savefig("results/" + str(tc) + "/popularity_dst_subset.png")
plt.clf()


plot_dict(size_real_subset, "real")
plot_dict(size_gen_subset, "sampled")
plt.grid()
plt.legend()
plt.savefig("results/" + str(tc) + "/size_dst_subset.png")
plt.clf()

