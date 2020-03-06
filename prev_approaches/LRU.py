from scipy import optimize
from datetime import datetime
from collections import defaultdict
import math
from obj_size_distribution import *


class LRUCache(object):
    def __init__(self, size):
        self.avail_size = size
        self.size = size
        self.hash = {}
        self.item_list = []
        self.hits = 0
        self.requests = 0
        self.oid_seen = set()
        self.oid_count = defaultdict(int)
        self.footprint = 0
        self.objects_seen = []
        self.cumulative_size = []

    def insertItem(self, item, replace, curr_time):
        self.requests += 1

        last_accessed_time = -1
        
        if item.key not in self.oid_seen:
            self.footprint += item.size
            self.objects_seen.append(item)
            
        self.oid_seen.add(item.key)


        if item.key in self.hash:
            last_accessed_time = item.timestamp
            item.timestamp = curr_time

            if replace == True:
                item_index = self.item_list.index(item)
                self.item_list[:] = self.item_list[:item_index] + self.item_list[item_index+1:]
                self.item_list.insert(0, item)            
                self.hits += 1

                item_sizes = [item.size for item in self.item_list]
                self.cumulative_size = np.cumsum(item_sizes)
                return [1, self.cumulative_size[item_index], curr_time - last_accessed_time]

            return [1, 0, 0]

        else:
            item.timestamp = curr_time
            if self.avail_size < item.size:
                while self.avail_size < item.size:
                    self.removeItem(self.item_list[-1])

            self.hash[item.key] = item
            self.item_list.insert(0, item)
            item_sizes = [item.size for item in self.item_list]
            self.cumulative_size = np.cumsum(item_sizes)
            self.avail_size -= item.size

        return [0, 0, 0]

    def removeItem(self, item):
        self.avail_size += item.size
        del self.hash[item.key]
        del self.item_list[self.item_list.index(item)]

    def computeHitrate(self):
        def func1(x):
            sum = 0
            for item in self.objects_seen:
                try:
                    sum += item.distribution.getContribution(x[0], item.popularity)*item.size
                except:
                    print("error")
            return [sum - self.size]

        def jac1(x):
            sum = 0
            for oid in self.oid_count:
                try:
                    sum += item.distribution.getConstributionDerivative(x[0], item.popularity)*item.size
                except:
                    print("error")
            return [sum]

        sol = optimize.root(func1, [200], jac=jac1, method='hybr')
        self.Tc = sol.x[0]
