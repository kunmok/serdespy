import serdespy as sdp
import numpy as np
import matplotlib.pyplot as plt
import time

# data = sdp.prbs20(1)[:1000000]
data = sdp.prbs20(1)[:1000]

# encoder = sdp.RSCodec(nsym=8, nsize=544, c_exp=10)
encoder_kr4 = sdp.RS_KR4()

t1 = time.time()
data_encoded = sdp.rs_encode(data, encoder_kr4, pam4=False)
t2 = time.time()
print(f'time to encode: {t2-t1}')

t1 = time.time()
data_decoded = sdp.rs_decode(data_encoded, encoder_kr4, pam4=False)
t2 = time.time()
print(f'time to decode: {t2-t1}')

err = data - data_decoded
print(f'# of error: {np.sum(err)}\n')

# encoder_kp4 = sdp.RS_KP4()