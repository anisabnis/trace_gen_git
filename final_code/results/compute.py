f = open("v/footprint_desc_01.txt", "r")
f.readline()
total_prs = 0
for l in f:
    l = l.strip().split(" ")
    pr = float(l[2])
    total_prs += pr

print(total_prs)
    
