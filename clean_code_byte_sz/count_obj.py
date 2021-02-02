from collections import defaultdict

f=open("all_sort_int", "r")
objects = defaultdict()
cnt = 0
obj_sizes = 0

for l in f:
    l = l.strip().split(" ")
    obj = l[1] + ":" + l[2]
    if obj not in objects:
        obj_sizes += int(l[3])

    objects[obj] = int(l[3])
    cnt += 1
    if cnt > 134217768:
        break    

    if cnt % 100000 == 0:
        print(cnt)

print(len(list(objects.keys())))
print(obj_sizes)
