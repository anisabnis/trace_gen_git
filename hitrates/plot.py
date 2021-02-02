import matplotlib.pyplot as plt

#f = open("hitrate_trace_1.txt", "r")
f = open("hitrate_wiki_1.txt", "r")
to_plot = []

for l in f:
    l = l.strip().split(" ")
    b_hit = float(l[2])/float(l[1])
    to_plot.append(b_hit)

#plt.locator_params(nbins=len(to_plot)/12 + 1) 
plt.plot(to_plot[:170])
plt.xticks(list(range(0, 168, 12)),list(range(0, 168, 12)))
plt.grid()
plt.ylim([0.35, 0.9])
plt.savefig("hourly_eu_wiki.png")


