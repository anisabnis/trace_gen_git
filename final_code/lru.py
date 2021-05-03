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
    def get(self, key, eviction_age, r_count): 
        if key not in self.cache: 
            return -1
        else:
            eviction_age[key][-1] = r_count
            self.cache.move_to_end(key) 
            return self.cache[key] 
  

    def get_occupied_space(self):
        return self.occupied_space

    # first, we add / update the key by conventional methods. 
    # And also move the key to the end to show that it was recently used. 
    # But here we will also check whether the length of our 
    # ordered dictionary has exceeded our capacity, 
    # If so we remove the first key (least recently used) 
    def put(self, key, value, eviction_age, r_count, track=False): 

        self.cache[key] = value 
        self.cache.move_to_end(key) 
        self.occupied_space += value
        eviction_age[key].append(r_count)
        
        evicted_items = []
        if self.occupied_space > self.capacity: 
            
            while self.occupied_space > self.capacity:
                k, v = self.cache.popitem(last = False)
                eviction_age[k].append(r_count)
                self.occupied_space -= v
                evicted_items.append(k)
            
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
