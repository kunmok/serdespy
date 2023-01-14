import serdespy as sdp
import numpy as np
import matplotlib.pyplot as plt
import time


def burst_err_gen(payload, prob_start, prob_end):
    payload_err = np.copy(payload)
    idx = 0
    total_err = 0
    while idx < len(payload):
        burst_prob = np.random.uniform(0, 1)
        if prob_start <= burst_prob <= prob_end:
            burst_len = np.random.randint(1, 21)
            if idx+burst_len > len(payload_err):
                burst_len = len(payload_err) - idx
            payload_err[idx:idx + burst_len] = 1 - payload_err[idx:idx + burst_len]
            print(f'burst_len = {burst_len}')
            total_err = total_err + burst_len
        else:
            burst_len = 0
        idx = idx + burst_len + 1   # once the burst error is suppressed, the next symbol must be correct by definition
    print(f'total # of errors : {total_err}\n')
    return payload_err


# data = sdp.prbs20(1)[:1000000]
prob_range = 0.005
prob_offset = 0.5 - prob_range/2
data = sdp.prbs20(1)[:5140]

# encoder = sdp.RSCodec(nsym=8, nsize=544, c_exp=10)
encoder_kr4 = sdp.RS_KR4()      # nsym=14, nsize=528, c_exp=10
'''
    every symbol consists of 10 bits. Then it adds extra 14 parity symbols, adding 14*10 = 140 bits to every data block.
    Each RS-encoded block consists of maximum 10*528 = 5280 bits.  
'''
print(f' ***** RS-KR4 *****')
data_encoded = sdp.rs_encode(data, encoder_kr4, pam4=False)
data_encoded_with_err = burst_err_gen(data_encoded, prob_offset, prob_offset + prob_range)

data_decoded = sdp.rs_decode(data_encoded_with_err, encoder_kr4, pam4=False)

err = data - data_decoded
total_err = np.sum(abs(err) > 0)
print(f'# of error (KR4): {total_err}\n')
print(f'# POST-FEC BER (KR4): {total_err / len(data)}')


encoder_kp4 = sdp.RS_KP4()
print(f' ***** RS-KP4 *****')
data_encoded2 = sdp.rs_encode(data, encoder_kp4, pam4=False)
data_encoded_with_err2 = burst_err_gen(data_encoded2, prob_offset, prob_offset + prob_range)

data_decoded2 = sdp.rs_decode(data_encoded_with_err2, encoder_kp4, pam4=False)

err2 = data - data_decoded2
total_err2 = np.sum(abs(err2) > 0)
print(f'# of error (KP4): {total_err2}')
print(f'# POST-FEC BER (KP4): {total_err2 / len(data)}')