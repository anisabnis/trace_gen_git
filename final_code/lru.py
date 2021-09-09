import sys
import numpy as np
from scipy import optimize
import math
from collections import OrderedDict
from collections import defaultdict
from collections import OrderedDict 
  

class LRUCache: 
  
    # initialising capacity 
    def __init__(self, capacity): 
        self.cache = OrderedDict() 
        self.capacity = capacity 
        self.occupied_space = 0
        self.obj_a_tm = defaultdict(lambda : [])
        self.obj_e_tm = defaultdict(lambda : [])

    # we return the value of the key 
    # that is queried in O(1) and return -1 if we 
    # don't find the key in out dict / cache. 
    # And also move the key to the end 
    # to show that it was recently used. 
    def get(self, key, i): 
        if key not in self.cache: 
            return -1, -1
        else:            
            self.cache.move_to_end(key)
            sz = self.cache[key][0]
            self.cache[key] = (sz, i)
            return self.cache[key] 
  

    def get_occupied_space(self):
        return self.occupied_space

    # first, we add / update the key by conventional methods. 
    # And also move the key to the end to show that it was recently used. 
    # But here we will also check whether the length of our 
    # ordered dictionary has exceeded our capacity, 
    # If so we remove the first key (least recently used) 
    def put(self, key, value, eviction_age): 

        self.cache[key] = value 
        self.cache.move_to_end(key)
        print(value[0])
        self.occupied_space += value[0]
        
        evicted_items = []
        if self.occupied_space > self.capacity:             
            while self.occupied_space > self.capacity:
                k, v = self.cache.popitem(last = False)
                self.occupied_space -= v[0]
                eviction_age.append(value[1] - v[1])
                evicted_items.append((k,v))
            
        return evicted_items



class LRUCacheSimple: 
  
    # initialising capacity 
    def __init__(self, capacity): 
        self.cache = OrderedDict() 
        self.capacity = capacity 
        self.occupied_space = 0

    # we return the value of the key 
    # that is queried in O(1) and return -1 if we 
    # don't find the key in out dict / cache. 
    # And also move the key to the end 
    # to show that it was recently used. 
    def get(self, key): 
        if key not in self.cache: 
            return -1
        else:            
            self.cache.move_to_end(key)
            sz = self.cache[key]
            self.cache[key] = sz
            return self.cache[key] 
  

    def get_occupied_space(self):
        return self.occupied_space

    # first, we add / update the key by conventional methods. 
    # And also move the key to the end to show that it was recently used. 
    # But here we will also check whether the length of our 
    # ordered dictionary has exceeded our capacity, 
    # If so we remove the first key (least recently used) 
    def put(self, key, value): 

        self.cache[key] = value 
        self.cache.move_to_end(key)
        self.occupied_space += value
        
        evicted_items = []
        
        while self.occupied_space > self.capacity:
            k, v = self.cache.popitem(last = False)
            self.occupied_space -= v
            evicted_items.append((k,v))
            
        return evicted_items



    
class SLRUCache:
    def __init__(self, number_segments, capacity):
        self.caches = [LRUCacheSimple(capacity)] * number_segments
        self.number_segments = number_segments

    def get(self, key):

        for j in range(self.number_segments):

            if self.caches[j].get(key) != -1:

                if j == self.number_segments - 1:
                    self.caches[j].move_to_end(key)
                    return self.caches[j].cache[key]
                else:
                    val = self.caches[j].cache[key]
                    del self.caches[j].cache[key]
                    self.caches[j].occupied_space -= val

                    evicted_items = self.caches[j+1].put(key, val)
                    req = list(range(j+1))
                    req.reverse()

                    for jj in req:
                        req_items = []
                        for item in evicted_items:
                            req_items.extend(self.caches[jj].put(item[0], item[1]))
                        evicted_items = req_items

                    return val

        return -1

    def put(self, key, value):
        evicted_items = self.caches[0].put(key, value)
        return evicted_items

class KLRUCache:
    def __init__(self, number_segments, capacity):
        self.caches = [LRUCacheSimple(capacity)] * number_segments
        self.number_segments = number_segments

    def get(self, key):

        for j in range(self.number_segments):

            if self.caches[j].get(key) != -1:

                if j == self.number_segments - 1:
                    self.caches[j].move_to_end(key)
                    return self.caches[j].cache[key]
                else:
                    val = self.caches[j].cache[key]
                    del self.caches[j].cache[key]
                    self.caches[j].occupied_space -= val

                    evicted_items = self.caches[j+1].put(key, val)
                    req = list(range(j+1))
                    req.reverse()

                    for jj in req:
                        req_items = []
                        for item in evicted_items:
                            req_items.extend(self.caches[jj].put(item[0], item[1]))
                        evicted_items = req_items

                    ## This is the only change from SLRU
                    return -1

        return -1

    def put(self, key, value):
        evicted_items = self.caches[0].put(key, value)
        return evicted_items

    

    
def test_cache():
    capacity = 4
    requests = [1,2,3,1,4,5,3,6]
    cache = LRUCache(4)

    for r in requests:
        if cache.get(r) == -1:
            items = cache.put(r, 1)
            print("request : ", r, " evicted : ", items)
        else:
            pass
        

if __name__ == "__main__":
    test_cache()
