from joint_dst import *
from util import *
ps = pop_sz_dst("joint_dst.txt")
pss = ps.sample_popularities(4194304)
#pss = ps.sample_popularities(10)
sum_sizes = 0
sizes = []
for p in pss:
    sz = ps.sample(p)
    sizes.append(sz)
    sum_sizes += sz
    #print(sz)
    
print("sum : ", sum_sizes)
sz = np.cumsum(sizes)

plt.plot(sz)
plt.xlabel("Number of objects")
plt.ylabel("Uniq Bytes")
plt.grid()
plt.savefig("ubytes_objects.png")


#print("pop : ", )

# f = open("popularities_trace.txt", "r")
# sizes = []
# for l in f:
#     l = l.strip().split(" ")
#     obj_id = int(l[0])
#     pop = float(l[1])
#     sizes.append(ps.sample(pop))

# print("sum-sizes : ", sum(sizes))
# plot_list(sizes)
# plt.grid()
# plt.savefig("sizes.png")




    




