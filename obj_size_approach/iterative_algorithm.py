import sys
from collections import defaultdict
import math
import numpy as np
import copy

def gen_fd():
    p_s = []
    p_t_s = defaultdict(list)
    stack = list(range(3,20))

    i = 0

    alpha = 0.8

    for s in stack:
        p_t_s[s] = []

        for s in stack:
            if s == s:
                p_t_s[s].append(1)
            else:
                p_t_s[s].append(0)

        p_s.append(1/math.pow(i+1,alpha))
        i += 1

    sum_p = sum(p_s)
    p_s = [float(p)/sum_p for p in p_s]    
    c_p_s = np.cumsum(p_s)
    return stack, p_s, c_p_s, p_t_s

def sample_fd(stack, p_s, c_p_s, p_t_s):
    z = np.random.random()
    sd = stack[-1]

    for i in range(len(c_p_s)):
        if c_p_s[i] > z:
            sd = stack[i]
            break
    
    #print(sd)
    #sd1 = np.random.randint(int(sd * math.log(sd)), int(sd *math.log(sd)* 1.1)) 
    #sd1 = int(sd * math.log(sd))
    return [sd, sd]
    
            
def gen_prop(no_items, items, stack, p_s, c_p_s, p_t_s):
    props = dict()
    no_samples = 100

    for i in items:
        props[i] = []
        for k in range(no_samples):
            z = sample_fd(stack, p_s, c_p_s, p_t_s)            
            props[i].extend(z)

    return props

def obj_popularity(items):
    alpha = 0.8
    pop_distribution = []

    for i in items:
        #popularity = float(1)/math.pow(i+1, alpha)
        popularity = 1
        pop_distribution.append(popularity)

    pop_distribution = [float(p)/sum(pop_distribution) for p in pop_distribution]
    pop_distribution = np.cumsum(pop_distribution)
    #print(pop_distribution)
    return pop_distribution


def sample_item(items, pop_distribution):
    z = np.random.random()
    for i in range(len(pop_distribution)):
        if pop_distribution[i] > z:
            return items[i]
    return items[-1]


def sort_by_stack(trace, prop, items):
    counter = dict()

    for i in items:
        counter[i] = 0

    length = len(trace)

    for i in range(length):

        try :
            curr_item = trace[i]
        except:
            break

        try:
            j = trace[i+1:].index(curr_item)
            j = i + j
            req_sd = prop[curr_item][counter[curr_item]]
            counter[curr_item] += 2
            
            uniq_ele = set()

            for k in range(i+1, len(trace)):

                if trace[k] == curr_item:
#                    pass
                    trace = trace[:k] + trace[k+1:]
                    trace.append(curr_item)

                uniq_ele.add(trace[k])            

                if len(uniq_ele) > req_sd:
                    break

            ## put the object at j to k
            trace = trace[:j] + trace[j+1:]
            trace.insert(k, curr_item)                                


        except:
            pass
           # print("Failed ")



    return trace

def sort_by_timestamp(trace, prop, items):
    counter = dict()

    for i in items:
        counter[i] = 0

    length = len(trace)
    timestamps = [0] * length
    assigned = [0] * length
    curr_time = -0.7

    for i in range(length):
        curr_item = trace[i]

        if assigned[i] == 0:
            timestamps[i] = curr_time + 0.7
            curr_time += 0.7
            assigned[i] = 1
        else :
            curr_time = timestamps[i]
            
        try:
            j = trace[i+1:].index(curr_item)
            j = i + j + 1
            to_add = prop[curr_item][counter[curr_item]+1]
            counter[curr_item] += 2
            timestamps[j] = timestamps[i] + to_add
            assigned[j] = 1
        except:
            pass
        

    trace = [x for _,x in sorted(zip(timestamps,trace))]

    return trace




no_items = int(sys.argv[1])
items = range(no_items)
pop_distribution = obj_popularity(items)
stack, p_s, c_p_s, p_t_s = gen_fd()
props = gen_prop(no_items, items, stack, p_s, c_p_s, p_t_s)


trace = []
for i in range(1000):
    item = sample_item(items, pop_distribution)
    trace.append(item)

trace.append(-1)
# print("Before : ", trace)
# trace1 = sort_by_stack(trace, props, items)
# print("After stack: ", trace)
# trace2 = sort_by_timestamp(trace1, props, items)
# print("After timestamp: ", trace)
# print("-----------------------------\n")
# print("Error : ", [trace1[i] - trace2[i] for i in range(len(trace1))])



def stack_error(trace, props):
    counter = dict()

    for i in items:
        counter[i] = 0

    length = len(trace)

    error = 0

    for i in range(length):
        try :
            curr_item = trace[i]
        except:
            break

        try:
            #print("curr item : ", curr_item)
            j = trace[i+1:].index(curr_item)

            #print("j : ", j)
            req_sd = props[curr_item][counter[curr_item]]

            #print("req_sd : ", req_sd)
            counter[curr_item] += 2
            curr_sd = len(set(trace[i+1:i+j+1]))

            #print("curr sd : ", curr_sd)
            error += abs(curr_sd - req_sd)

            #print("error : ", error)

        except:
            pass


    return error
    

while True:
    trace = sort_by_stack(trace, props, items)

    #print("Trace Stack : ", trace)

    trace = sort_by_timestamp(trace, props, items)    

    #print("Trace Timestamp : ", trace)

    error = stack_error(trace, props)

    print("error : ", error)

    if error == 0:
        break


print(trace)
