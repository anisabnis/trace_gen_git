f = open("req_hr.txt", "r")
c = 0
for l in f:
    l = int(l.strip())
    c += l

print(c)
