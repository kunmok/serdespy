import serdespy as sdp
import numpy as np
import matplotlib.pyplot as plt
import time

max_burst = 20


def burst_err_gen(payload, prob_start, prob_end):
    payload_err = np.copy(payload)
    idx = 0
    total_err = 0
    while idx < len(payload):
        burst_prob = np.random.uniform(0, 1)
        if prob_start <= burst_prob <= prob_end:
            burst_len = np.random.randint(1, max_burst + 1)
            if idx+burst_len > len(payload_err):
                burst_len = len(payload_err) - idx
            payload_err[idx:idx + burst_len] = 1 - payload_err[idx:idx + burst_len]
            # print(f'burst_len = {burst_len}')
            total_err = total_err + burst_len
        else:
            burst_len = 0
        idx = idx + burst_len + 1   # once the burst error is suppressed, the next symbol must be correct by definition
    print(f'total # of errors : {total_err}\n')
    return payload_err


# prob_range = 0.001
# prob_range = 0.0005
prob_range = 0.0012
prob_offset = 0.5 - prob_range/2
rs_encoder = sdp.RS_KR4()      # nsym=14, nsize=528, c_exp=10
block_size = 2000

iter_num = 10
ber_postfec = np.zeros(iter_num)
for idx in range(iter_num):

    # rs_encoder = sdp.RS_KP4()      # nsym=30, nsize=544, c_exp=10
    # data = sdp.prbs20(1)[:5140*200]
    # data = sdp.prbs20(1)[:5140]
    data = np.random.randint(0, 2, 5140*block_size, dtype=int)

    data_encoded = sdp.rs_encode(data, rs_encoder, pam4=False)
    data_encoded_with_err = burst_err_gen(data_encoded, prob_offset, prob_offset + prob_range)
    data_decoded = sdp.rs_decode(data_encoded_with_err, rs_encoder, pam4=False)

    err_pre = data_encoded - data_encoded_with_err
    total_pre_err = np.sum(abs(err_pre) > 0)
    print(f'PRE-FEC BER: {total_pre_err / len(data_encoded)}')

    err = data - data_decoded
    total_err = np.sum(abs(err) > 0)
    ber_postfec[idx] = total_err / len(data)
    print(f'# of error: {total_err}')
    print(f'POST-FEC BER: {ber_postfec[idx]}')


print(ber_postfec)
print(np.mean(ber_postfec))

