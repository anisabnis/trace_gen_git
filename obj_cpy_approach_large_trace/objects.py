#f = open("sampled_sizes_0.01.txt", "r")
#l = f.readline()
#l = l.strip().split(",")
#print("Length of L : ", len(l))

f = open("sampled_popularities.txt", "r")
l = f.readline()
l = l.strip().split(",")
l = [float(x) for x in l]
print(float(sum(l))/len(l))

print(max(l))
print(min(l))
