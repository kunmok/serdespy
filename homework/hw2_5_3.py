import numpy as np
import math

'''
    case study: 
        burst error length can only be 3 or 4. pe is 0.5. what is the BER? 
'''

pe = 0.5
p_unif = 1/2

# exp_err = np.zeros(20, dtype=int)
burst_len1 = 3
burst_len2 = 4
exp_err1 = (pe * burst_len1) / ((1 - pe) + pe * (burst_len1 + 1))
exp_err2 = (pe * burst_len2) / ((1 - pe) + pe * (burst_len2 + 1))

# exp_err3 = (pe * (p_unif * burst_len1 + p_unif * burst_len2)) / ((1 - pe) + pe * p_unif * (burst_len1 + 1) + pe * p_unif * (burst_len2 + 1))
exp_err3 = (pe * p_unif * (burst_len1 + burst_len2)) / ((1 - pe) + pe * p_unif * ((burst_len1 + 1) + (burst_len2 + 1)))
print(exp_err1)
print(exp_err2)
print((exp_err1 + exp_err2)/2)
print(exp_err3)
