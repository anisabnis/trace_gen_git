import json
import numpy as np
from collections import defaultdict

file = "akamai1.bin.popCntObj.json"
with open(file, "r") as read_file:

    pop_dst = json.load(read_file)
    pops = list(pop_dst.keys())    
    pop_prs = defaultdict()

    for s in pops:        
        r_no = np.random.random()
        if r_no > 0.01:            
            pop_dst.pop(s, 'None')

    js = json.dumps(pop_dst)
    f = open("sub_pop_dst2.json","w")
    f.write(js)
    f.close()
    

