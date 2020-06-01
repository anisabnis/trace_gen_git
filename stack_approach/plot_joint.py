f = open("joint_dst.txt", "r")
no_objects = 0
for l in f:
    l = l.strip().split(" ")
    if len(l) == 1:
        continue
    no_objects += int(l[1])
print(no_objects)
