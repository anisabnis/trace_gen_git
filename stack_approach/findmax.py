maxsz = 0
f = open("subtrace.txt", "r")
for l in f:
    l = l.strip().split(" ")
    sz = int(l[2])
    if sz > maxsz:
        maxsz = sz

print(maxsz)
