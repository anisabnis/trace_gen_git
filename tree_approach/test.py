from collections import defaultdict

f = open("init_trace.txt", "r")
l = f.readline()
l = l.strip().split(",")

count = defaultdict(int)

for k in l:
    count[k] += 1

print(count)
        
