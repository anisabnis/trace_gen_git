import sys
import matplotlib.pyplot as plt 
from operator import itemgetter
from LRU import *
from obj_size_distribution import *

print("Popularity Distribution (zipf/uniform)")
print("Arrival distribution ")
print("total objects ")

popularity_distribution = sys.argv[1]
arrival_distribution = sys.argv[2].split(":")
total_objects = int(sys.argv[3])

obj_catalogue = ObjectCatalogue(total_objects, popularity_distribution, arrival_distribution)

number_requests = 150000
requests_hit = 0

cache = LRUCache(80000)

IATs = defaultdict(list)
SDs = list()

if arrival_distribution[0] == "poisson":
    curr_timestamp = 0

    for i in range(number_requests):
        time_diff = np.random.normal(1, 0.2)        

        if i%10000 == 0:
            print(i)

        curr_timestamp += time_diff
        obj = obj_catalogue.getObject()    
        [hit, sd, iat] = cache.insertItem(obj, True, curr_timestamp)       

        sd = int(sd/200)
        if hit == 1:
            IATs[sd].append(iat)
            SDs.append(sd)

else:
    traces = []
    time_window = 500000
    iter = 0

    for obj in obj_catalogue.catalogue:
        times = []
        curr_timestamp = 0

        while curr_timestamp < time_window:
            next = int(obj.distribution.getNext(obj.popularity))
            curr_timestamp += next
            traces.append([curr_timestamp, obj])
            iter += 1
            times.append(curr_timestamp)
        
    print("traces generated ", iter)

    number_requests = iter
    traces = sorted(traces, key=itemgetter(0))
    
    iter = 0
    for t in traces:
        obj = t[1]

        [hit, sd, iat] = cache.insertItem(obj, True, t[0])
        sd = sd/50

        if hit == 1:
            IATs[sd].append(iat)
            SDs.append(sd)

cache.computeHitrate()

theory_hit = 0

for obj in obj_catalogue.catalogue:
    tc = cache.Tc

    try :
        obj_p_hit = obj.distribution.getContribution(tc, obj.popularity)
        obj_pop = obj.popularity        
        theory_hit += obj_p_hit * obj_pop
    except:
        print("error 1")

print(theory_hit)

SDs.sort()


uniq_sds = np.unique(SDs)
uniq_sds.sort()

print("len(sds) : ", len(SDs))
print("len(uniq_sds) : ", len(uniq_sds))

MIN = []
MAX = []

for us in uniq_sds:
    timestamps = IATs[us]
    min_ts = min(timestamps)
    max_ts = max(timestamps)
    
    MIN.append(min_ts)
    MAX.append(max_ts)


print("len(MIN) : ", len(MIN))
print("len(MAX) : ", len(MAX))
print(uniq_sds)

plt.plot(SDs)
plt.savefig("StackDistance.png")
plt.clf()

plt.plot(MIN)
plt.plot(MAX)
plt.savefig("iat.png")
plt.clf()
