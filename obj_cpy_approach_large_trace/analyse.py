import numpy as np

f = open("sampled_popularities_0.01.txt", "r")
l = f.readline()
l = l.strip().split(",")
l = l[:2097152]
f.close()

print(l[0])

f = open("req_count_0.01.txt", "r")
l1 = f.readline()
l1 = l1.strip().split(",")
l1 = l1[:2097152]
f.close()

print(l1[0])

for i in range(len(l1)):
    if l[i] != l1[i]:
        print("i : ", i, l[i], l1[i])

 



    
