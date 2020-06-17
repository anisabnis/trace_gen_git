import sys
import matplotlib.pyplot as plt

d = sys.argv[1]

f = open(d + "/joint_dst.txt", "r")

l = f.readline().strip()
curr_p = int(l)
trace_len = 0
total_objects = 0
no_objects = 0

popularities = []
objects = []

for l in f:
    l = l.strip().split(" ")

    if len(l) == 1:
        trace_len += no_objects * curr_p
        total_objects += no_objects

        popularities.append(curr_p)
        objects.append(no_objects)

        no_objects = 0
        curr_p = int(l[0])    
    else:
        no_objects = int(l[1]) + no_objects

trace_len += no_objects * curr_p
total_objects += no_objects

print("trace len : ", trace_len)
print("total objects : ", total_objects)
f.close()

f = open(d + "/properties.txt", "w")
f.write("trace length : " + str(trace_len) + "\n")
f.write("number of objects : " +  str(total_objects) + "\n")
f.close()

plt.plot(popularities, objects)
plt.xlabel("popularities")
plt.ylabel("req_count")
plt.grid()
plt.savefig(d + "/pop" + ".png")
