f = open("out_trace_all.txt", "r")
l = f.readline()
l = l.strip().split(",")[:-1]
out_trace = [int(x) for x in l]
f.close()
out_trace = out_trace[:1000000]
max_obj = max(out_trace)

f = open("sampled_sizes_all.txt", "r")
l = f.readline()
l = l.strip().split(",")[:-1]
sampled_sizes = [int(x) for x in l]
sampled_sizes = sampled_sizes[:max_obj]

f = open("out_trace_tmp.txt", "w")
f.write(",".join([str(x) for x in out_trace]))
f.close()

f = open("sampled_sizes_tmp.txt", "w")
f.write(",". join([str(x) for x in sampled_sizes]))
f.close()    


