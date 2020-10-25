f = open("debug.txt", "r")
i = 0
for l in f:
    l = l.strip().split(" ")
    if len(l) != 4:
        continue
    if (int(l[1]) - int(l[0])) > 90000000:
        print(i, int(l[1]) - int(l[0]), int(l[0]), int(l[1]))
    i += 1
