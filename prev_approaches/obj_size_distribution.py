import numpy as np
import math
import random

class PoissonDistribution:
    def __init__(self, rate):
        self.type = "poisson"
        self.rate = rate

    def getContribution(self, T, popularity):
        return (1 - math.exp(-1 * popularity * self.rate * T)) 

    def getContributionDerivative(self, T, popularity):
        return (popularity * self.rate * math.exp(-1 * popularity * self.rate * T))

    def getNext(self, popularity):
        lambd = popularity * self.rate
        beta = float(1)/lambd
        return np.random.exponential(beta, 1)[0]

class HyperTDistribution:
    def __init__(self, rate, p):
        self.type = "hyperexponential"
        self.pop = p
        self.avg_rate = rate
        self.compute_params()

    def compute_params(self):
        c_v = (random.random() + 0.2) * 5
        r = self.avg_rate * self.pop
        p1 = 0.5 * (1 + math.sqrt(float(c_v - 1)/(c_v + 1)))
        p2 = 1 - p1

        r1 = 2 * p1 * r
        r2 = 2 * p2 * r

        self.rates = [r1, r2]
        self.ps = [p1, p2]
        print(r1, r2, p1, p2)


    def getContribution(self, T, popularity):
        sum = 1
        for i in range(len(self.ps)):
            sum -= self.ps[i] * math.exp(-1 * self.rates[i] * T)
        return sum

    def getConstributionDerivative(self, T , popularity):
        sum = 0
        for i in range(len(self.ps)):
            sum += self.ps[i] * self.rates[i] * math.exp(-1 * self.rates[i] * T)
        return sum

    def getNext(self, popularity):
        cum_ps = np.cumsum(self.ps)
        p = random.random()
        req_p = 0
        req_rate = 0

        for j,pr in enumerate(cum_ps):
            if pr > p:
                req_p = self.ps[j]
                req_rate = self.rates[j]

        lambd = req_rate
        beta = float(1)/lambd
        return np.random.exponential(beta, 1)[0]

class LRUCacheItem(object):
    def __init__(self, key, size, popularity, d):
        self.key = key
        self.size = size
        self.popularity = popularity
        self.distribution = d
        self.timestamp = 0


class ObjectCatalogue(object):
    def __init__(self, count, pop_distribution, arrival_rate_distribution):
        self.count = count
        self.distribution = pop_distribution
        self.arrival = arrival_rate_distribution
        self.catalogue = []
        self.popularity = []
        self.cumulative_popularity = []
        self.buildPopularities()
        self.buildCatalogue()

    def buildPopularities(self):
        if self.distribution == "zipf":
            self.popularity = [float(1)/math.pow(i+1, 0.8) for i in range(self.count)]

        elif self.distribution == "uniform":
            self.popularity = [1 for i in range(self.count)]
            
        elif self.distribution == "geometric":
            pass

        self.popularity = [p/sum(self.popularity) for p in self.popularity]
        self.cumulative_popularity = np.cumsum(self.popularity)

    def buildCatalogue(self):
        for i in range(self.count):
            s = (random.random() * 50)
            p = self.popularity[i]
            k = random.randint(0, len(self.arrival) - 1)
            if self.arrival[k] == "poisson":
                d = PoissonDistribution(4)
            elif self.arrival[k] == "hyperexp":
                d = HyperTDistribution(2, p)

                            
            a = LRUCacheItem(i, s, p, d)
            self.catalogue.append(a)
            
    def getObject(self):
        p = random.random()
        for j, pr in enumerate(self.cumulative_popularity):
            if pr > p:
                return self.catalogue[j]
            

            
