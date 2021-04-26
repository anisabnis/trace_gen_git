from random_evict import *
rnd_c = RNDCache(2)

req_seq = [1,5,1,4,6,3,5,7,4,3,2,7,8,1,1,3]
for r in req_seq:
    if rnd_c.get(r) == -1
