import sys
dir="/mnt/nfs/scratch1/asabnis/data/binary/small/" + sys.argv[1]

min_tm = 0
max_tm = 0

total_bytes = 0

f = open(dir + "/subtrace.txt", "r")
cnt = 0

for l in f:
    l = l.strip().split(" ")
    tm = int(l[0])

    if cnt == 0:
        min_tm = int(l[0])
        cnt = 1

    total_bytes += int(l[2])

max_tm = int(l[0])
f.close()

f = open(dir + "/bytes.txt", "w")
f.write(str(min_tm) + " " + str(max_tm) + " " + str(total_bytes))

    
