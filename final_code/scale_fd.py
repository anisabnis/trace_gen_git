import sys
from collections import defaultdict

dir = sys.argv[1]
fd_file = sys.argv[2]
scale_factor = float(sys.argv[3])

fd = defaultdict(lambda : defaultdict(float))

f = open("results/" + dir + "/" + fd_file + ".txt" , "r")
l = f.readline()
l = l.strip().split(" ")
st = int(l[2])
end = int(l[3])

f1 = open("results/" + dir + "/" + fd_file + "_s" + str(scale_factor) + ".txt", "w")
f1.write(str(int(float(l[0])*2)) + " " + str(float(l[1]) * 2) + " " + str(st) + " " + str(end) + " " + str(int(float(l[4])*2)) + " " + str(float(l[5])*2) + "\n")

for l in f:
    l = l.strip().split()
    iat = int(l[0])
    iat = float(iat)/scale_factor
    iat = int(iat/200)*200
    sd  = int(l[1])
    pr  = float(l[2])
    fd[iat][sd] += pr

iat_keys = list(fd.keys())
iat_keys.sort()
for iat in iat_keys:
    sds = list(fd[iat].keys())
    sds.sort()
    for sd in sds:
        f1.write(str(iat) + " " + str(sd) + " " + str(fd[iat][sd]) + "\n")
f1.close()

    
