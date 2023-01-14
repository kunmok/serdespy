'''
    demo file provided from the class website.
'''

import serdespy as sdp
import numpy as np
import scipy as sp
import matplotlib.pyplot as plt
import time

data = sdp.prbs13(1)

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
for i in range(70):
    if codeword_rx[i] == 1:
        codeword_rx[i] = 0
    elif codeword_rx[i] == 0:
        codeword_rx[i] = 1

# decode the erred codeword
payload_dec = sdp.rs_decode(codeword_rx, KR4_encoder, pam4=False)

# check if decoded correctly
print(np.array_equal(payload_dec, payload))

codeword_rx = np.copy(codeword)

# add a burst of 71 errors at the beginning of the codeword
# this corrupts 8 FEC symbols and should be not correctable
for i in range(71):
    if codeword_rx[i] == 1:
        codeword_rx[i] = 0
    elif codeword_rx[i] == 0:
        codeword_rx[i] = 1

payload_dec = sdp.rs_decode(codeword_rx, KR4_encoder, pam4=False)

# check if decoded correctly
print(np.array_equal(payload_dec, payload))