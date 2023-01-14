'''
    check and see if the provided RS-coding is systematic coding.
    answer: Yes, it seems like systematic encoding is chosen for this project.
'''

import serdespy as sdp
import numpy as np
import matplotlib.pyplot as plt
import time

# data = sdp.prbs20(1)[:1000000]
data = sdp.prbs20(1)[:5140]

# encoder = sdp.RSCodec(nsym=8, nsize=544, c_exp=10)
encoder_kr4 = sdp.RS_KR4()

t1 = time.time()
data_encoded = sdp.rs_encode(data, encoder_kr4, pam4=False)
t2 = time.time()
print(f'time to encode: {t2-t1}')

offset = 0
target_size = 5140
data_b4enc = data[offset:offset+target_size]
data_a4enc = data_encoded[offset:offset+target_size]
err = np.abs(data_b4enc - data_a4enc)
# print(data[-200:])
# print(data_encoded[-200:])
# print(data[0:100])
# print(data_encoded[0:100])
print(data_b4enc)
print(data_a4enc)
print(f'# of error: {np.sum(err)}')
print(f'data length before encoding: {len(data)}')
print(f'data length after encoding: {len(data_encoded)}')

# t1 = time.time()
# data_decoded = sdp.rs_decode(data_encoded, encoder_kr4, pam4=False)
# t2 = time.time()
# print(f'time to decode: {t2-t1}')
#
# err = data - data_decoded
# print(f'# of error: {np.sum(err)}\n')

# encoder_kp4 = sdp.RS_KP4()