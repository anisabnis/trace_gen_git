f = open("footprint_desc_all.txt", "r")
l = f.readline()
total_pr = 0
for l in f:
    l = l.strip().split(" ")
    pr = float(l[2])
    total_pr += pr

print(total_pr)

    
