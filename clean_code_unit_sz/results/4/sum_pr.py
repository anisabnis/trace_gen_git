from collections import defaultdict
import numpy as np
import matplotlib.pyplot as plt

fd_bytes = defaultdict(float)

popularity = 0

f = open("fd_bytes.txt", "r")
for l in f:
    l = l.strip().split(" ")

    if len(l) == 1:
        popularity = int(l[0])
        continue

    bytes = int(l[0])/1000
    if bytes > 1400000000:
        continue
    pr = float(l[1])
    fd_bytes[bytes] += popularity * pr

byte_keys = fd_bytes.keys()
byte_keys.sort()
byte_prs = []
for k in byte_keys:
    byte_prs.append(fd_bytes[k])

sum_prs = sum(byte_prs)
byte_prs = [float(x)/sum_prs for x in byte_prs]
byte_prs = np.cumsum(byte_prs)

plt.plot(byte_keys, byte_prs)
plt.grid()
plt.savefig("byte_dst.png")

        
