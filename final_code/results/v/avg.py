#f = open("original.stats200000000_0.txt", "r")
f = open("generated.stats200000000_sz.txt", "r")
reqs = 0
i = 0
for l in f:
    l = l.strip().split(" ")
    r = int(l[4])
    reqs += r
    i += 1

print(reqs/i)
