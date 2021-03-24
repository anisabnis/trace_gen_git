f = open("test_original.txt", "r")
vals = []
keys = []
for l in f:
    l = l.strip().split(" ")
    vals.append(float(l[1]))
    keys.append(int(l[0]))
sum_vals = sum(vals)
vals= [float(x)/sum_vals for x in vals]
f = open("test_original_new.txt", "w")
for i in range(len(keys)):
    f.write(str(keys[i]) + " " + str(vals[i]) + "\n")
f.close()
