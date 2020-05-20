from parse_fd import *
import matplotlib.pyplot as plt

fd = FD("./", "sfd.txt")
plt.xlabel("Unique objects")
plt.ylabel("cdf")
plt.grid()
plt.savefig("sfd_uo.png")
plt.clf()

fd = FD("./", "sfd_bytes.txt")
plt.xlabel("Unique bytes")
plt.ylabel("cdf")
plt.grid()
plt.savefig("sfd_bytes.png")
plt.clf()


