import sys
import numpy as np
from boltons.cacheutils import LRI
from collections import OrderedDict
from collections import defaultdict
import random
    

class FIFOCache: 
  
    # initialising capacity 
    def __init__(self, capacity: int): 
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
    def get(self, key: int) -> int: 
        if key not in self.cache: 
            return -1
        else: 
            return self.cache[key] 

  
    # first, we add / update the key by conventional methods. 
    # And also move the key to the end to show that it was recently used. 
    # But here we will also check whether the length of our 
    # ordered dictionary has exceeded our capacity, 
    # If so we remove the first key (least recently used) 
    def put(self, key: int, value: int, track=False) -> None: 

        self.cache[key] = value 
        self.occupied_space += value
        
        evicted_items = []

        if self.occupied_space > self.capacity: 

            while self.occupied_space > self.capacity:
                k, v = self.cache.popitem(last = False) 
                self.occupied_space -= v
                evicted_items.append(k)

        return evicted_items

