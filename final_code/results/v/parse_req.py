f = open("sampled_pop_pop.txt", "r")
l = f.readline()
l = l.strip().split(",")[:-1]
l1 = [int(x) for x in l]
f.close()

f = open("req_count_pop.txt", "r")
l = f.readline()
l = l.strip().split(",")[:-1]
l2 = [int(x) for x in l]
f.close()

f = open("diff.txt", "w")
for i in range(len(l1)):
    if l1[i] - l2[i] > 0:
        f.write(str(i) +  " " + str(l1[i]) + " " + str(l2[i]) + " " + str(l1[i] - l2[i]) + "\n")
f.close()

