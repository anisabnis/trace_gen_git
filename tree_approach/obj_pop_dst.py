import numpy as np
import json

class obj_pop:
    def __init__(self, dir, o_file):
        with open(dir + "/" + o_file, "r") as read_file:
            pop_dst = json.load(read_file)

        pops = list(pop_dst.keys())
        pops = [int(x.encode("utf-8")) for x in pops]
        pops.sort()

        pop_prs = []
        for s in pops:
            s = unicode(str(s), "utf-8")
            pop_prs.append(pop_dst[s])
            
        sum_pr = sum(pop_prs)
        pop_prs = [float(p)/sum_pr for p in pop_prs]
        pop_prs = np.cumsum(pop_prs)

        self.pops = pops
        self.pop_prs = np.cumsum(pop_prs)

    def sample(self):
        z = np.random.random()
        obj = self.pops[-1]
        for i in range(len(self.pops)):
            if z >= self.pop_prs[i]:
                obj = self.pops[i]
                break
        return obj


    def sample_object(self, objects):
        z = np.random.random()
        obj = objects[-1]
        for i in range(len(self.cdf_popularities)):
            if self.cdf_popularities[i] >= z:
                obj = objects[i]
                break
        return obj
        

    def assign_popularities(self, sz):
        objects = sz.objects
        self.popularities = []

        for i in range(len(objects)):
            p = self.sample()
            self.popularities.append(p)
            
        sum_pop = sum(self.popularities)
        self.popularities = [float(s)/sum_pop for s in self.popularities]
        self.cdf_popularities = np.cumsum(self.popularities)


    def get_trace(self, sz, t_len):
        trace = []
        objects = range(len(sz.objects))
        for i in range(t_len):
            o = self.sample_object(objects)
            trace.append(o)
        return trace


    def getDelta(self, objects, min_fd, max_fd, scale):
        probabilities = []
        d_vals = []

        #for d in range(min_fd, max_fd+1):
        init_val = min_fd
        while init_val < max_fd:
            prob = 0
            d = init_val
            for i in range(len(objects)):
                sz = objects[i]
                p = self.popularities[i]                
                if sz > abs(d):
                    prob += (p * sz) * (float(1)/(sz)) * (1 - float(abs(d))/sz)
        
            probabilities.append(prob)
            d_vals.append(d)
            init_val += scale

        sum_p = sum(probabilities)
        probabilities = [(float(p)/sum_p) for p in probabilities]        
        probabilities_sum = np.cumsum(probabilities)

        return probabilities_sum, d_vals, probabilities
