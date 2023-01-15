'''
    sandbox
'''

import serdespy as sdp
import numpy as np
import scipy


def esym_calc():
    den_arr = np.array([55, 100, 45])

    E_sym1 = 0
    tmp = 0
    for idx in range(9 + 1):
        for jdx in range(1, 11 - idx):
            tmp = tmp + jdx
        E_sym1 = E_sym1 + tmp
        tmp = 0

    E_sym2 = 0
    tmp = 0
    for idx in range(9 + 1):
        for jdx in range(11 - idx, 20 - idx + 1):
            tmp = tmp + jdx
        E_sym2 = E_sym2 + tmp
        tmp = 0

    E_sym3 = 0
    tmp = 0
    for idx in range(10 + 1):
        for jdx in range(20, 20 - idx + 1, -1):
            tmp = tmp + jdx
        E_sym3 = E_sym3 + tmp
        tmp = 0

    Esym_arr = np.array([E_sym1, E_sym2, E_sym3]) / den_arr
    return Esym_arr


max_burst = 20
pe = 0.0005     # chance of bit error
# pe = 0.00025     # chance of bit error
# pe = 0.001
# pe = 0.0012
print(f'Pe = {pe}')
pu = 1/max_burst       # burst error distribution (uniform b/w 1 and 20)

p_noerr = ((1-pe)**10)
p_error = 1 - p_noerr
ratios = 1 + 1*100/55 + 1*45/55
# ratios = 55 + 100 + 45

p_sym = np.zeros(3)
p_sym[0] = p_error / ratios
p_sym[1] = p_error * (100/55) / ratios
p_sym[2] = p_error * (45/55) / ratios

e_sym = esym_calc()            # default: 4, 11, 17.333 for max_burst of 20.
rs_encoder = sdp.RS_KR4()      # nsym=14, nsize=528, c_exp=10
n = rs_encoder.nsize
m = rs_encoder.c_exp

num = pe * pu * np.sum(np.arange(1, max_burst + 1))
den = (1 - pe) + pe * pu * (np.sum(np.arange(1, max_burst + 1)) + max_burst)
pre_fec_ber = num/den
print(f'Stat-Domain PRE-FEC BER = {pre_fec_ber}')

err = np.zeros(7)
# error 1
err1 = scipy.special.comb(n, 1) * p_sym[0] * (p_noerr)**(n-1) * e_sym[0] * 1 / (n * m)                  # 1
err[0] = err1

# error 2
err2_arr = np.zeros(2)
err2_arr[0] = scipy.special.comb(n, 2) * (p_sym[0]**2) * (p_noerr)**(n-2) * e_sym[0] * 2 / (n * m)      # 11
err2_arr[1] = scipy.special.comb(n-1, 1) * p_sym[1] * (p_noerr)**((n-1)-1) * e_sym[1] * 1 / (n * m)     # 2
err[1] = np.sum(err2_arr)

# error 3
err3_arr = np.zeros(3)
err3_arr[0] = scipy.special.comb(n, 3) * (p_sym[0]**3) * (p_noerr)**(n-3) * e_sym[0] * 3 / (n * m)      # 111
err3_arr[1] = scipy.special.comb(n-1, 1) * p_sym[1] * \
              scipy.special.comb(n-2, 1) * p_sym[0] * (p_noerr)**((n-2)-1) * \
              (e_sym[0]+e_sym[1]) / (n * m)                                                             # 12
err3_arr[2] = scipy.special.comb(n-2, 1) * p_sym[2] * (p_noerr)**(n-2-1) * e_sym[2] * 1 / (n * m)       # 3
err[2] = np.sum(err3_arr)

# error 4
err4_arr = np.zeros(4)
err4_arr[0] = scipy.special.comb(n, 4) * (p_sym[0]**4) * (p_noerr)**(n-4) * e_sym[0] * 4 / (n * m)      # 1111
err4_arr[1] = scipy.special.comb(n-1, 1) * p_sym[1] * \
              scipy.special.comb(n-2, 2) * (p_sym[0]**2) * (p_noerr)**((n-2)-2) * \
              (e_sym[0]*2+e_sym[1]) / (n * m)                                                           # 112
err4_arr[2] = scipy.special.comb(n-2, 1) * p_sym[2] * \
              scipy.special.comb(n-3, 1) * p_sym[0] * (p_noerr)**((n-3)-1) * \
              (e_sym[0]+e_sym[2]) / (n * m)                                                             # 13
err4_arr[3] = scipy.special.comb(n-1, 1) * (p_sym[1]) * \
              scipy.special.comb(n-3, 1) * (p_sym[1]) * (p_noerr)**(n-3-1) * \
              (2*e_sym[1]) / (n * m)                                                                    # 22
err[3] = np.sum(err4_arr)

# error 5
err5_arr = np.zeros(5)
err5_arr[0] = scipy.special.comb(n, 5) * (p_sym[0]**5) * (p_noerr)**(n-5) * e_sym[0] * 5 / (n * m)      # 11111
err5_arr[1] = scipy.special.comb(n-1, 1) * p_sym[1] * \
              scipy.special.comb(n-2, 3) * (p_sym[0]**3) * (p_noerr)**((n-2)-3) * \
              (e_sym[0]*3+e_sym[1]) / (n * m)                                                           # 1112
err5_arr[2] = scipy.special.comb(n-2, 1) * p_sym[2] * \
              scipy.special.comb(n-3, 2) * (p_sym[0]**2) * (p_noerr)**(n-3-2) * \
              (e_sym[0]*2+e_sym[2]) / (n * m)                                                           # 113
err5_arr[3] = scipy.special.comb(n-1, 1) * (p_sym[1]) * \
              scipy.special.comb(n-3, 1) * (p_sym[1]) * \
              scipy.special.comb(n-4, 1) * (p_sym[0]) * (p_noerr)**(n-4-1) * \
              (e_sym[0]+e_sym[1]*2) / (n * m)                                                           # 122
err5_arr[4] = scipy.special.comb(n-2, 1) * p_sym[2] * \
              scipy.special.comb(n-4, 1) * p_sym[1] * (p_noerr)**((n-4)-1) * \
              (e_sym[1]+e_sym[2]) / (n * m)                                                             # 23
err[4] = np.sum(err5_arr)

# error 6
err6_arr = np.zeros(6)
err6_arr[0] = scipy.special.comb(n, 6) * (p_sym[0]**6) * (p_noerr)**(n-6) * e_sym[0] * 6 / (n * m)      # 111111
err6_arr[1] = scipy.special.comb(n-1, 1) * p_sym[1] * \
              scipy.special.comb(n-2, 4) * (p_sym[0]**4) * (p_noerr)**((n-2)-4) * \
              (e_sym[0]*4+e_sym[1]) / (n * m)                                                           # 11112
err6_arr[2] = scipy.special.comb(n-2, 1) * p_sym[2] * \
              scipy.special.comb(n-3, 3) * (p_sym[0]**3) * (p_noerr)**((n-3)-3) * \
              (e_sym[0]*3+e_sym[2]) / (n * m)                                                           # 1113
err6_arr[3] = scipy.special.comb(n-1, 1) * (p_sym[1]) * \
              scipy.special.comb(n-3, 1) * (p_sym[1]) * \
              scipy.special.comb(n-4, 2) * (p_sym[0]**2) * (p_noerr)**((n-4)-2) * \
              (e_sym[0]*2+e_sym[1]*2) / (n * m)                                                         # 1122
err6_arr[4] = scipy.special.comb(n-2, 1) * p_sym[2] * \
              scipy.special.comb(n-4, 1) * (p_sym[1]) * \
              scipy.special.comb(n-5, 1) * (p_sym[0]) * (p_noerr)**((n-5)-1) * \
              (e_sym[0]+e_sym[1]+e_sym[2]) / (n * m)                                                    # 123
err6_arr[5] = scipy.special.comb(n-2, 1) * (p_sym[2]) * \
              scipy.special.comb(n-5, 1) * (p_sym[2]) * (p_noerr)**(n-5-1) *\
              e_sym[2] * 2 / (n * m)                                                                    # 33
err[5] = np.sum(err6_arr)

# error 7
err7_arr = np.zeros(6)
err7_arr[0] = scipy.special.comb(n, 7) * (p_sym[0]**7) * (p_noerr)**(n-7) * e_sym[0] * 7 / (n * m)      # 1111111
err7_arr[1] = scipy.special.comb(n-1, 1) * p_sym[1] * \
              scipy.special.comb(n-2, 5) * (p_sym[0]**5) * (p_noerr)**((n-2)-5) * \
              (e_sym[0]*5+e_sym[1]) / (n * m)                                                           # 111112
err7_arr[2] = scipy.special.comb(n-2, 1) * p_sym[2] * \
              scipy.special.comb(n-3, 4) * (p_sym[0]**4) * (p_noerr)**((n-3)-4) * \
              (e_sym[0]*4+e_sym[2]) / (n * m)                                                           # 11113
err7_arr[3] = scipy.special.comb(n-1, 1) * (p_sym[1]) * \
              scipy.special.comb(n-3, 1) * (p_sym[1]) * \
              scipy.special.comb(n-4, 3) * (p_sym[0]**3) * (p_noerr)**((n-4)-3) * \
              (e_sym[0]*3+e_sym[1]*2) / (n * m)                                                         # 11122
err7_arr[4] = scipy.special.comb(n-2, 1) * p_sym[2] * \
              scipy.special.comb(n-4, 1) * (p_sym[1]) * \
              scipy.special.comb(n-5, 2) * (p_sym[0]**2) * (p_noerr)**((n-5)-2) * \
              (e_sym[0]*2+e_sym[1]+e_sym[2]) / (n * m)                                                  # 1123
err7_arr[5] = scipy.special.comb(n-2, 1) * (p_sym[2]) * \
              scipy.special.comb(n-5, 1) * (p_sym[2]) * \
              scipy.special.comb(n-6, 1) * (p_sym[0]) * (p_noerr)**(n-6-1) * \
              (e_sym[0]+e_sym[2]*2) / (n * m)                                                           # 133
err[6] = np.sum(err7_arr)

post_fec_ber = pre_fec_ber - np.sum(err)
if post_fec_ber < 0:
    post_fec_ber = 0
print(f'Stat-Domain POST-FEC BER = {post_fec_ber}')
