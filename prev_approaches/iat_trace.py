import sys
from collections import defaultdict
import math
import numpy as np
import copy

def sample(cdf, values):
    z = np.random.random()
    for i in range(len(cdf)):
        if cdf[i] > z:
            return values[i]
    return values[-1]

p_s_t = defaultdict(lambda : defaultdict(float))
p_t_s = defaultdict(lambda : defaultdict(float))

f = open("st.web.download", "r")
for l in f:
    l = l.strip().split(" ")

    iat = int(l[0])
    sd = int(l[1])
    p = float(l[2])

    p_s_t[iat][sd] = p
    p_t_s[sd][iat] = p

print("done reading footprint descriptor ")

iats = list(p_s_t.keys())
iats.sort()
sds = list(p_t_s.keys())
sds.sort()

iat_dst = []
sd_dst = []

for iat in iats:
    p = 0
    for ps in p_s_t[iat]:
        p += p_s_t[iat][ps]
    iat_dst.append(p)

print("done generating IAT distribution")

for sd in sds:
    p = 0
    for iat in p_t_s[sd]:
        p += p_t_s[sd][iat]
    sd_dst.append(p)


iat_dst = np.cumsum(iat_dst)
sd_dst = np.cumsum(sd_dst)



#print("iat dst : ", iat_dst)
#print("sd dst : ", len(sd_dst))
