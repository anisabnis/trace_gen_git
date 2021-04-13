import matplotlib.pyplot as plt
from util import *

f = open("v/age_distribution_generated.txt", "r")
l = f.readline()
l = l.strip().split(",")
l = l[:-1]
gen = [int(x) for x in l]
gen = [x for x in gen if x < 5000000]

f = open("v/age_distribution_original.txt", "r")
l = f.readline()
l = l.strip().split(",")
l = l[:-1]
orig = [int(x) for x in l]
orig = [x for x in orig if x < 5000000]

plot_list(orig, "orig")
plot_list(gen, "generated")
plt.xlabel("Age distribtuion")
plt.ylabel("CDF")
plt.grid()
plt.legend()
plt.savefig("v/age.png")
