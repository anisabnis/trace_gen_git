import sys
import numpy as np
from scipy import optimize
from llist import sllist
import math
import random
from collections import OrderedDict
from collections import defaultdict
from collections import OrderedDict 
  

class MarkersCache: 
  
    # initialising capacity 
    def __init__(self, capacity): 
        self.marked = defaultdict()
        self.unmarked = defaultdict()
        self.U = sllist()
        self.UPositions = defaultdict()
        self.eviction_round = 1
        self.capacity = capacity 
        self.occupied_space = 0

    # we return the value of the key 
    # that is queried in O(1) and return -1 if we 
    # don't find the key in out dict / cache. 
    # And also move the key to the end 
    # to show that it was recently used. 
    def get(self, key): 
        if key in self.marked:
            return 1
        elif key in self.unmarked:
            val = self.unmarked[key]
            self.marked[key] = val

            del self.unmarked[key]            
            item_pos = self.UPositions[key]
            del self.UPositions[key]
            self.U.remove(item_pos)

            return 1
        else:
            return -1

    # first, we add / update the key by conventional methods. 
    # And also move the key to the end to show that it was recently used. 
    # But here we will also check whether the length of our 
    # ordered dictionary has exceeded our capacity, 
    # If so we remove the first key (least recently used) 
    def put(self, key, value): 
        if len(self.unmarked) == 0 and self.eviction_round > 1:

            all_keys = list(self.marked.keys())
            random.shuffle(all_keys)

            for k in all_keys:
                item_pos = self.U.appendleft(k)
                self.UPositions[k] = item_pos
                self.unmarked[k] = self.marked[k]

            self.marked = defaultdict()
            self.eviction_round += 1
            print("eviction round : ", self.eviction_round)
            
        ## add key to marked list
        self.marked[key] = value
        self.occupied_space += value

        ## evict random keys from the list till we are within capacity
        while self.occupied_space > self.capacity:

            if self.eviction_round == 1:
                self.eviction_round += 1
                return

            if self.U.size <=  0:
                break

            k = self.U.pop()
            v = self.unmarked[k]
            del self.unmarked[k]
            del self.UPositions[k]
            self.occupied_space -= v


        

        

    
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
