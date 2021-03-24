f = open("sampled_pop_pop.txt", "r")
l = f.readline()
l = l.strip().split(",")[:-1]
l = [int(x) for x in l]
l.sort(reverse=True)
print(l[:100])
