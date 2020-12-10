import sys
from collections import defaultdict

dir = sys.argv[1]
popularity_dst = defaultdict(int)

f = open(dir + "/fd_bytes.txt", "r")
l = f.readline()
p = int(l.strip())

f1 = open(dir + "/fd_bytes_bucket.txt", "w")

for l in f:
    l = l.strip().split(" ")        
    
    if len(l) == 1:
        f1.write(str(p) + "\n")

        print("Popularity : ", p)

        for k in popularity_dst:
            f1.write(str(k) + " " + str(popularity_dst[k]) + "\n")

        p = int(l[0])

        popularity_dst = defaultdict(float)

    else:

        sd = float(l[0])/200000
        sd = int(sd) * 200000
        pr = float(l[1])                 

        popularity_dst[sd] += pr
