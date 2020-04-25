import json
import matplotlib.pyplot as plt
import numpy as np

with open("akamai1.bin.sizeCntObj.json", "r") as read_file:
    data = json.load(read_file)

dat = list(data.keys())
dat = [int(x.encode("utf-8")) for x in dat]
dat.sort()

aa = unicode(str(dat[0]), "utf-8")
#print(data[aa])

sizes = []
for d in dat:
    d = unicode(str(d), "utf-8")
    sizes.append(data[d])

print(sizes[:100])
sum_sizes = sum(sizes)
pr = [float(s)/sum_sizes for s in sizes]
pr = np.cumsum(pr)
print(pr[-10:])
print(len(dat))

plt.plot(dat[:100000], pr[:100000])
plt.grid()
plt.savefig("size_dst.png")





