f = open("v/joint_dst_0.txt", "r")
l = f.readline()
sum_pr = 0
for l in f:
    l = l.strip().split(" ")
    if len(l) == 1:
        break
    pr = float(l[1])
    sum_pr += pr

print(sum_pr)
