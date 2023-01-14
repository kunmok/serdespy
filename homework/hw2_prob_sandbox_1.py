import serdespy as sdp
import numpy as np
import scipy
import matplotlib.pyplot as plt
import time

max_burst = 20
pe = 0.0005     # chance of bit error
pu = 1/20       # burst error distribution (uniform b/w 1 and 20)

p_error = 1 - ((1-pe)**10)
ratios = 1 + 1*100/55 + 1*45/55

p_sym = np.zeros(3)
p_sym[0] = p_error / ratios
p_sym[1] = p_error * (100/55) / ratios
p_sym[2] = p_error * (45/55) / ratios

rs_encoder = sdp.RS_KR4()      # nsym=14, nsize=528, c_exp=10
n = rs_encoder.nsize
m = rs_encoder.c_exp
prob1 = scipy.special.comb(n, 1) * p_sym[0] * (1-p_sym[0])**(n-1)
prob2 = scipy.special.comb(n, 2) * (p_sym[0]**2) * (1-p_sym[0])**(n-2)
print(p_sym)        # probability of having 1 symbol error
print(prob1)
print(prob2)

