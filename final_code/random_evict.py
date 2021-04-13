import sys
import numpy as np
from collections import OrderedDict
from collections import defaultdict
import random
    

class RNDCache: 
  
    # initialising capacity 
    def __init__(self, capacity): 
        self.cache = defaultdict() 
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
            return self.cache[key] 

  
    # first, we add / update the key by conventional methods. 
    # And also move the key to the end to show that it was recently used. 
    # But here we will also check whether the length of our 
    # ordered dictionary has exceeded our capacity, 
    # If so we remove the first key (least recently used) 
    def put(self, key, value, track=False): 

        self.cache[key] = value 
        self.occupied_space += value
        
        evicted_items = []

        if self.occupied_space > self.capacity: 

            while self.occupied_space > self.capacity:
                del_key = random.choice(self.cache.keys())
                v = self.cache[del_key]
                self.occupied_space -= v
                del self.cache[del_key]
                evicted_items.append(del_key)

        return evicted_items

