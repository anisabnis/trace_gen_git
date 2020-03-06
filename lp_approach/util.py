from collections import defaultdict
import numpy as np

def sample(cdf, values):
    z = np.random.random()
    for i in range(len(cdf)):
        if cdf[i] > z:
            return values[i]
    return values[-1]

