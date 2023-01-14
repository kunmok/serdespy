import numpy as np
import math


max_burst = 20
pe = 0.0005
# pe = 0.001
p_unif = 1/max_burst

# reference: hw_2_5_3.py
num = pe * p_unif * np.sum(np.arange(1, max_burst + 1))
den = (1 - pe) + pe * p_unif * (np.sum(np.arange(1, max_burst + 1)) + max_burst)
print(num/den)
