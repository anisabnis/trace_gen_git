import sys
from collections import defaultdict

s = int(sys.argv[1])
e = int(sys.argv[2])
d = sys.argv[3]

print(s, e, d)
joint_dst = defaultdict(lambda : defaultdict(float))

for i in range(s, e+1):
    f = open("results/" + str(d) + "/iat_pop_" + str(i) + ".txt", "r")
    cp = int(f.readline().strip())

    for l in f:
        l = l.strip().split(" ")

        if len(l) == 1:
            cp = int(l[0])
        else:
            sz = int(float(l[0]))
            pr = float(l[1])
            joint_dst[cp][sz] += float(pr)/(e - s + 1)

    f.close()

f = open("results/" + str(d) + "/iat_pop_fnl.txt", "w")
pops = joint_dst.keys()
pops.sort()

for p in pops:
    f.write(str(p) + "\n")
    szs = joint_dst[p].keys()
    szs.sort()    
    for s in szs:
        f.write(str(s) + " " + str(joint_dst[p][s]) + "\n")
f.close()
        
    
        


