import sys
import matplotlib.pyplot as plt

dir = sys.argv[1]
csize = int(sys.argv[2]) * 1000000

t1_lru_o = []
t1_lru_b = []
t1_fifo_o = []
t1_fifo_b = []

t2_lru_o = []
t2_lru_b = []
t2_fifo_o = []
t2_fifo_b = []

#str(obj_reqs) + " " + str(byte_reqs) + " " + str(obj_hits_fifo) + " " + str(byte_hits_fifo) + " " + str(obj_hits_lru) + " " + str(byte_hits_lru)

f = open("results/" + str(dir) + "/generated.stats" + str(csize) + ".txt", "r")

reqs = 0
bytes = 0
f_o_hit = 0
f_b_hit = 0
l_o_hit = 0
l_b_hit = 0
i = 1
plain_req_count = 0
for l in f:
    l = l.strip().split(" ")
    plain_req_count += int(l[0])
    
    #if plain_req_count < 25000000:
    #    continue


    reqs += int(l[0])
    bytes += int(l[1])

    f_o_hit += int(l[2])
    f_b_hit += int(l[3])
    
    if i % 1 == 0:
        t1_fifo_o.append(float(f_o_hit)/reqs)
        t1_fifo_b.append(float(f_b_hit)/bytes)

    l_o_hit += int(l[4])
    l_b_hit += int(l[5])

    if i%1 == 0:
        t1_lru_o.append(float(l_o_hit)/reqs)
        t1_lru_b.append(float(l_b_hit)/bytes)
        reqs = 0
        bytes = 0
        f_o_hit = 0
        f_b_hit = 0
        l_o_hit = 0
        l_b_hit = 0
    i += 1

reqs = 0
bytes = 0
f_o_hit = 0
f_b_hit = 0
l_o_hit = 0
l_b_hit = 0

f = open("results/" + str(dir) + "/original.stat" + str(csize) + ".txt", "r")
i = 1
plain_req_count = 0
for l in f:
    l = l.strip().split(" ")

    plain_req_count += int(l[0])    
    #if plain_req_count < 25000000:
    #    continue

    reqs  += int(l[0])
    bytes += int(l[1])

    f_o_hit += int(l[2])
    f_b_hit += int(l[3])

    if i % 1 == 0:
        t2_fifo_o.append(float(f_o_hit)/reqs)
        t2_fifo_b.append(float(f_b_hit)/bytes)

    l_o_hit += int(l[4])
    l_b_hit += int(l[5])

    if i % 1 == 0:
        t2_lru_o.append(float(l_o_hit)/reqs)
        t2_lru_b.append(float(l_b_hit)/bytes)
        reqs = 0
        bytes = 0
        f_o_hit = 0
        f_b_hit = 0
        l_o_hit = 0
        l_b_hit = 0        
    i += 1

# ## first fifo - obj
# plt.plot(t1_fifo_o, marker="o", markersize=3, label="result")
# plt.plot(t2_fifo_o, marker="^", markersize=3, label="original")
# plt.grid()
# plt.legend()
# plt.savefig("results/" + str(dir) + "/fifo_obj_" + str(csize) + ".png") 
# plt.clf()

# ## fifo - bytes
plt.plot(t1_fifo_b, marker="o", markersize=2, label="result")
plt.plot(t2_fifo_b, marker="^", markersize=2, label="original")
plt.grid()
plt.legend()
#plt.ylim([0.35, 0.5])
plt.savefig("results/" + str(dir) + "/fifo_byte_" + str(csize) + "_6hourly.png") 
plt.clf()
        
# ## first lru - obj
# plt.plot(t1_lru_o, marker="o", markersize=3, label="result")
# plt.plot(t2_lru_o, marker="^", markersize=3, label="original")
# plt.grid()
# plt.legend()
# plt.savefig("results/" + str(dir) + "/lru_obj_" + str(csize) + ".png") 
# plt.clf()

## lru - bytes
plt.plot(t1_lru_b, marker="o", markersize=2, label="result")
plt.plot(t2_lru_b, marker="^", markersize=2, label="original")
plt.grid()
plt.legend()
#plt.ylim([0.35, 0.5])
plt.savefig("results/" + str(dir) + "/lru_byte_" + str(csize) + "_6hourly.png") 

plt.clf()
