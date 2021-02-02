from collections import defaultdict
f = open("trace.csv", "w")
f.write("timestamp,obj_id,traffic_class,obj_sz,bytes_req\n")

f1 = open("trace_4.txt", "r")
objects = defaultdict()
for l in f1:
    l = l.strip().split(" ")
    obj_id = l[1] + ":" + l[2]
    objects[obj_id] = int(l[3])
f1.close()

f1 = open("trace_4.txt", "r")
for l in f1:
    l = l.strip().split(" ")
    obj_id = l[1] + ":" + l[2]
    l[3] = str(objects[obj_id])
    l = ",".join(l)
    f.write(l)
    f.write("\n")
f.close()
f1.close()
