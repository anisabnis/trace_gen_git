import sys
del_ = float(sys.argv[1])

f = open("sampled_sizes_" + str(del_) + ".txt", "r")
l = f.readline()
l = l.strip().split(",")
print("Number of requests : ", len(l))
