'''
    check the typical length of burst error.
    Question to answer: is it common to have burst error len > 3 symbol ? (also check 1 symbol err too)
'''
import serdespy as sdp
import numpy as np
import matplotlib.pyplot as plt
import time

punif = 1/20
# pe = 0.0005
pe = 0.0002
p_error = 1 - ((1-pe)**10)
print(p_error)

ratios = 1 + 1*100/55 + 1*45/55

p_sym = np.zeros(3)
p_sym[0] = p_error / ratios
p_sym[1] = p_error * (100/55) / ratios
p_sym[2] = p_error * (45/55) / ratios

print(p_sym)
print(f'1x sym prob from time domain = {1441/(528 * 2000)}')
print(f'2x sym prob from time domain = {2583/(528 * 2000)}')
print(f'3x sym prob from time domain = {1180/(528 * 2000)}')

E_sym1 = 0
tmp = 0
for idx in range(9 + 1):
    for jdx in range(1, 11-idx):
        tmp = tmp + jdx
    E_sym1 = E_sym1 + tmp
    tmp = 0

E_sym2 = 0
tmp = 0
for idx in range(9 + 1):
    for jdx in range(11-idx, 20-idx + 1):
        tmp = tmp + jdx
    E_sym2 = E_sym2 + tmp
    tmp = 0

E_sym3 = 0
tmp = 0
for idx in range(10 + 1):
    for jdx in range(20, 20-idx + 1, -1):
        tmp = tmp + jdx
    E_sym3 = E_sym3 + tmp
    tmp = 0

print(f'Avg BER for 1x sym error = {E_sym1 / 55}')
print(f'Avg BER for 2x sym error = {E_sym2 / 100}')
print(f'Avg BER for 3x sym error = {E_sym3 / 45}')

print(f'Avg BER for 1x and 2x sym error = {(E_sym2+E_sym1) / (100+55)}')
print(E_sym1)
print(E_sym2)
print(E_sym3)
