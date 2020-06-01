f = open("req_count_0.1.txt", "r")
l = f.readline()
l = l.strip().split(",")

f = open("sampled_popularities_0.1.txt", "r")
l1 = f.readline()
l1 = l1.strip().split(",")[:len(l)]


for i in range(len(l)):
    if l1[i] != l[i]:
        print(i , l1[i], l[i])


