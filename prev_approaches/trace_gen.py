from LRU import *
from collections import defaultdict
import numpy as np
import sys

p_s_timestamps = defaultdict(list)
p_s_probabilities = defaultdict(list)
p_s = defaultdict()
object_size_distribution = []


## Read FD and Generate P(S) and P(S|T)
f = open("st.web.download", "r")
for l in f:
    l = l.strip().split(" ")

    iat = int(l[0])
    sd = int(l[1])
    p = float(l[2])

    p_s_timestamps[sd].append(iat)
    p_s_probabilities[sd].append(p)


p_s_t = defaultdict()
sds = p_s_timestamps.keys()
sds.sort()

total_sum = 0
for sd in sds:
    probabilities = p_s_probabilities[sd]
    sum_p = sum(probabilities)

    if sum_p <= 0:
        continue

    total_sum += sum_p

    p_s[sd] = sum_p
    p_s_t[sd] =  [float(p)/sum_p for p in probabilities]

print(p_s[400])
print(p_s[600])
print(p_s[800])

#asdf

     
p_s[200] =  1 - total_sum  
p_s_t[200] = p_s_t[400]

P_S = []
stack_distances = p_s.keys()
stack_distances.sort()
number_sds = len(stack_distances)
for s in stack_distances:
    P_S.append(p_s[s])
P_S = np.cumsum(P_S)

def binarySearchCount(arr, n, key): 
  
    left = 0
    right = n 
   
    mid = 0
    while (left < right): 
      
        mid = (right + left)//2
   
        # Check if key is present in array 
        if (arr[mid] == key): 
          
            # If duplicates are 
            # present it returns 
            # the position of last element 
            while (mid + 1<n and arr[mid + 1] == key): 
                 mid+= 1
            break
          
   
        # If key is smaller, 
        # ignore right half 
        elif (arr[mid] > key): 
            right = mid 
   
        # If key is greater, 
        # ignore left half 
        else: 
            left = mid + 1
      
   
    # If key is not found in 
    # array then it will be 
    # before mid 
    while (mid > -1 and  arr[mid] > key): 
        mid-= 1
   
    # Return mid + 1 because 
    # of 0-based indexing 
    # of array 
    return mid + 1
  


def uniform_sample(distribution, values):
    v = np.random.random()
    index = binarySearchCount(distribution, number_sds, v)
    return values[index]

def findStackPos(stack, stack_distance, object_size_distribution):
    size = 0
    i = 0
    #print(stack_distance)
    while size <= stack_distance:
        size += object_size_distribution[stack[i]]
        i += 1

    return i



def findSize(stack, pos, object_size_distribution):
    size = 0
    i = 0
    #print(stack_distance)
    while i < pos:
        size += object_size_distribution[stack[i]]
        i += 1

    return size

## Generate a trace that matches P(S)

## 1. Initialize the stack

LRUStack = []
number_objects = int(sys.argv[1])
object_size_distribution = defaultdict()
for i in range(number_objects):
    size = np.random.uniform(3000)
    obj_id = str(i)
    object_size_distribution[obj_id] = size
    LRUStack.append(obj_id)

np.random.shuffle(LRUStack)

trace = []
for i in range(1000000):
    sample = uniform_sample(P_S, stack_distances)
    stack_pos = findStackPos(LRUStack, sample, object_size_distribution)
    trace.append(LRUStack[stack_pos])    
    item = LRUStack[stack_pos]
    LRUStack = LRUStack[:stack_pos] + LRUStack[stack_pos + 1:]
    LRUStack.insert(0, item)

trace_file = open("trace.txt", "w")
for t in trace:
    trace_file.write(str(t) + "\n")
trace_file.close()

## Compute stack distance count.

req_trace = trace[700000:]
LRUStack = []
StackCount = defaultdict(int)

for item in req_trace:
    if item in LRUStack:
        index = LRUStack.index(item)
        size = findSize(LRUStack, index , object_size_distribution)
        size = int(size)/200
        StackCount[size] += 1
        LRUStack = LRUStack[:index] + LRUStack[index+1:]
        LRUStack.insert(0, item)
    else:
        LRUStack.insert(0, item)

print(StackCount)

        


#for 


## Generate timestamps


 
