f = open("merge_01by_byte.txt", "r")
i1 = 0
i2 = 0
for l in f:
    l = l.strip().split(" ")
    c = int(l[1].split(":")[1])
    if c == 0:
        i1 += 1
    else :
        i2 += 1

print(i1, i2)
    
