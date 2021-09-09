f = open("out_trace_all.txt", "r")
l = f.readline()
l = l.strip().split(",")
print(len(l))
