from collections import defaultdict
import json

f = open("st.web.download", "r")
uniq_bytes = defaultdict(int)
rate = 0

for l in f:
    l = l.strip().split(" ")
    iat = int(l[0])
    sd = int(l[1])
    uniq_bytes_rate = sd/iat
    pr = float(l[3])
    
    rate += pr * uniq_bytes_rate

    if uniq_bytes_rate < 0.0000001:
        continue
    uniq_bytes[uniq_bytes_rate] += pr


with open("data/uniq_bytes_distribution.json", "w") as ofile:
    json.dump(uniq_bytes, ofile)
    

print("Average Rate for unique bytes : ", rate)

import matplotlib.pylab as plt

lists = sorted(uniq_bytes.items()) # sorted by key, return a list of tuples

x, y = zip(*lists) # unpack a list of pairs into two tuples

plt.plot(x, y)
plt.savefig("uniq_bytes_dst.png")    
plt.clf()


plt.plot(x[:500], y[:500])
plt.savefig("uniq_bytes_dst_500.png")
plt.clf()


plt.plot(x[:200], y[:200])
plt.savefig("uniq_bytes_dst_200.png")


