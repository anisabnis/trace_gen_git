f = open("joint_dst.txt", "r")
count = 0
no_objects = 0
for l in f:
    l = l.strip().split(" ")
    if len(l) == 1:
        count += int(l[0])
    else:
        no_objects += int(l[1])

print(count, no_objects)
