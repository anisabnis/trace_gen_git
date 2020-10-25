f = open ("sampled_sizes.txt", "r")
l = f.readline()
l = l.strip().split(",")
l = [int(x) for x in l]


max_sz = max(l)
print(max_sz)

sizes = [x for x in l if x < 11]
print("< 11 : ", len(sizes))

sizes = [x for x in l if x > 11]
print("> 11 : ", len(sizes))

sizes = [x for x in l if x == 11]
print("= 11 : ", len(sizes))
