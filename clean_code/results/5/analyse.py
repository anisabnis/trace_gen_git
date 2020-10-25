f = open("sampled_popularities.txt", "r")
l = f.readline()
l = l.strip().split(",")
l = l[:2097152]
f.close()

f = open("req_count.txt", "r")
l1 = f.readline()
l1 = l1.strip().split(",")
l1 = l1[:2097152]
f.close()


for i in range(2097152):
    if l[i] != l1[i]:
        print(i , l[i], l1[i])
