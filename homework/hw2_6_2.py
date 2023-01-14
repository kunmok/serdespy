'''
    demo file provided from the class website.
'''

import serdespy as sdp
import numpy as np
import scipy as sp
import matplotlib.pyplot as plt
import time

# data = np.random.randint(0, 2, 5140*2000, dtype=int)
data = np.random.randint(0, 2, 5140, dtype=int)

# This example uses the RS - KR4 code
# use sdp.RS_KP4() for KP4 FEC
KR4_encoder = sdp.RS_KR4()

# number of FEC symbols in codeword
N = 528

# number of FEC symbols in payload
K = 514

# correctability
T = 7

# bits in FEC symbol
n_bits_FEC_symbol = 10

# bits in payload
n_bits_payload = K * n_bits_FEC_symbol

# array of data bits to encode
payload = data[0:n_bits_payload]

# encode the payload
codeword = sdp.rs_encode(payload, KR4_encoder, pam4=False)

# artificailly introduce errors into the codeword


codeword_rx = np.copy(codeword)

# add a burst of 70 errors at the beginning of the codeword
# this corrupts 7 FEC symbols and should be correctable
idx_offset = 2005
max_burst = (idx_offset // 10 * 10 + 70) - idx_offset
codeword_rx[idx_offset:idx_offset + max_burst] = 1 - codeword[idx_offset:idx_offset + max_burst]

# decode the erred codeword
payload_dec = sdp.rs_decode(codeword_rx, KR4_encoder, pam4=False)

# check if decoded correctly
err = data - payload_dec
total_err = np.sum(abs(err) > 0)
print(f' ***** RS-KR4 *****')
print(f'# of error (KR4): {total_err}')
print(f'# POST-FEC BER (KR4): {total_err / len(data)}\n')

codeword_rx = np.copy(codeword)

max_burst = (idx_offset // 10 * 10 + 70) - idx_offset + 1
codeword_rx[idx_offset:idx_offset + max_burst] = 1 - codeword[idx_offset:idx_offset + max_burst]

payload_dec = sdp.rs_decode(codeword_rx, KR4_encoder, pam4=False)

# check if decoded correctly
err = data - payload_dec
total_err = np.sum(abs(err) > 0)
print(f' ***** RS-KR4 *****')
print(f'# of error (KR4): {total_err}')
print(f'# POST-FEC BER (KR4): {total_err / len(data)}\n')
