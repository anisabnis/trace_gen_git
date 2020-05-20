import matplotlib.pyplot as plt
from obj_size_dst import *
from obj_pop_dst import *
import json


## Plot the size distribution - overall
print("Reading size distribution")
sz  = obj_size("./", "subtrace.txt.sizeCntObj.json")
plt.grid()
plt.legend()
plt.savefig("size_dst.png")
plt.clf()


## Plit the popularity distribution - overall
print("Reading pop dst")
pop = obj_pop("./", "subtrace.txt.popCntReq.json")        
plt.grid()
plt.legend()
plt.savefig("pop_dst.png")
plt.clf()





