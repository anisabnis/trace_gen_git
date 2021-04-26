from collections import defaultdict
f = open("popularity_sd_all.txt", "r")
#f = open("pop_sd_0.txt", "r")
#f = open("popularity_sd_pop.txt", "r")
l = f.readline()
TB = 1000000000
a = defaultdict(lambda: defaultdict(float))
for l in f:
    l = l.strip().split(" ")
    k1 = int(l[0])
    k2 = int(float(l[1])/TB)
    a[k1][k2] = float(l[2])

#ps = [128, 256, 328]
ps = [271287,2048,1812, 46765, 35110, 19856,310,951, 1083,2001, 2010, 3000, 4001, 512, 851, 903]
for p in ps:
    vals = list(a[p].keys())
    vals.sort()
    sum_prs = 0
    prs = []
    for v in vals:
        prs.append(a[p][v])
        sum_prs += a[p][v]

    prs = [pr/sum_prs for pr in prs]
    for i in range(len(prs)):
        print(p, prs[i], vals[i])

        
        


