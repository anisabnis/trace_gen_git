import matplotlib.pyplot as plt

class noise:
    def __init__(self, sd, obj_sizes, obj_sizes_pr):
        self.sd = sd
        self.obj_sizes = obj_sizes
        self.obj_sizes_pr = obj_sizes_pr

    def noise_pr(self, s1, s2):
        sum = 0
        for i in range(len(self.obj_sizes)):
            obj_size = self.obj_sizes[i]
            obj_pr = self.obj_sizes_pr[i]
            if obj_size >= abs(s2 - s1):
                sum += (obj_pr * (float(1)/(obj_size * obj_size)) * (obj_size - abs(s2 - s1)))
        return sum
            

    def modelNoise(self):
        max_sd = max(self.sd.sds[:100])
        max_sd /= 10        

        for s1 in self.sd.sds[:100]:
            vals = []

#            r_s1 = (s1 - 800)/10
#            r_s2 = (s1 + 800)/10

            #req_sds = [10*x for x in range(r_s1, r_s2)]

            req_sds = range(s1 - 1000, s1 + 1000, 10)
            #req_sds = [10 * x for x in range(max_sd)]

            for s2 in req_sds:
                vals.append(self.noise_pr(s1, s2))

            plt.plot(req_sds, vals)
            plt.axvline(s1)
            plt.xlabel("Resulting Stack Distance")
            plt.ylabel("Probability")
            plt.grid()
            plt.savefig("Noise/" + str(s1) + ".png")
            plt.clf()
        
        
