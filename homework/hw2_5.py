import numpy as np
import math


def nchoosek(n, k):
    return math.comb(n, k)


pe = 0.005
p_unif = 1/20
# 1 symbol error
symerr_1 = 0
for idx in range(10, 0, -1):
    symerr_1 = symerr_1 + idx * pe * p_unif * ((1-pe)**(idx-1))
print(symerr_1)

symerr_2 = 0
for idx in range(10, 0, -1):
    symerr_2 = symerr_2 + 10 * pe * p_unif * ((1-pe)**(idx-1))
print(symerr_2)

symerr_3 = 0
for idx in range(9, 0, -1):
    # symerr_3 = symerr_3 + idx * pe * p_unif * ((1-pe)**(9-idx))
    symerr_3 = symerr_3 + idx * pe * p_unif * ((1 - pe)**idx)
print(symerr_3)

print(1-((1-pe)**10))     # having any error in a symbol
print(symerr_1 + symerr_2 + symerr_3)

print(pe * (20+1)/2 - pe)
print(pe*((21/2)-1))