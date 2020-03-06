import numpy as np
import matplotlib.pyplot as plt 
from collections import defaultdict

def analyse_timestamps(timestamps, probabilities):
    v3 = sum(probabilities)

    if v3 <= 0:
        return [0, 0, 0]

    probabilities = [float(p)/v3 for p in probabilities]
    prob_dist = np.cumsum(probabilities)
    found_first = False
    for i in range(len(probabilities)):
        if prob_dist[i] > 0.25 and found_first == False:
            v1 = timestamps[i]
            found_first = True
        elif prob_dist[i] > 0.75 :
            v2 = timestamps[i]
            break

    return [v1, v2, v3]

f = open("st.web.download", "r")

curr_iat = 200
timestamps = []
probabilities = []

p_s = []
MIN = []
MAX = []

sd_values = defaultdict(list)
sd_prob = defaultdict(list)

for l in f:
    l = l.strip().split(" ")
    iat = int(l[0])
    sd = int(l[1])
    pr = float(l[3])

    sd_values[sd].append(iat)
    sd_prob[sd].append(pr)
    
sds = list(sd_values.keys())
sds.sort()

for sd in sds:

    timestamps = sd_values[sd]
    probabilities = sd_prob[sd]

    #plt.plot(probabilities)
    #plt.savefig("plots/" + str(sd) + ".png")
    #plt.clf()
    
    v1, v2, v3 = analyse_timestamps(timestamps, probabilities)

    if v3 == 0:
        break

    p_s.append(v3)
    MIN.append(v1)
    MAX.append(v2)
    
plt.plot(MIN)
plt.plot(MAX)

#locs, labels = plt.xticks() 
#plt.xticks(locs, [int(str(l)) * 200 for l in labels])

plt.savefig("IATDistribution.png")
plt.clf()

plt.plot(p_s)
plt.xscale('log')
#locs, labels = plt.xticks() 
#plt.xticks(locs, [int(l) * 200 for l in labels])

plt.savefig("P_S.png")
plt.clf()

