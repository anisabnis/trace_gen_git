f1 = open("sampled_sds.txt" , "r")
l1 = f1.readline()
l1 = l1.split(",")
f1.close()

f2 = open("success.txt", "r")
l2 = f2.readline()
l2 = l2.split(",")
f2.close()

min_len = min(len(l1), len(l2))

for i in range(min_len):
    if l1[i] != l2[i]:
        print("Not equal : ", l1[i], l2[i])
