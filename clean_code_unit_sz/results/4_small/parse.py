f = open("debug.txt", "r")
debug = []
for l in f:
    l = int(l.strip().split(" ")[2])
    debug.append(l)
f.close()

f = open("debug_post.txt", "r")
debug_post = []
for l in f:
    try:
        l = int(l.strip().split(" ")[2])        
        debug_post.append(l)

    except:
        break

for i in range(len(debug_post)):
    if debug[i] == -1:
        continue

    if debug[i] != debug_post[i]:
        print("i : ", i, debug[i], debug_post[i])
    
