'''
    check number of symbol errors
'''

import serdespy as sdp
import numpy as np
import matplotlib.pyplot as plt
import time

max_burst = 20


def burst_err_gen2(payload, prob_start, prob_end):
    payload_err = np.copy(payload)
    idx = 0
    total_err = 0
    err_table = np.zeros((2, 0), dtype=int)
    err_cnt = 0
    while idx < len(payload):
        burst_prob = np.random.uniform(0, 1)
        if prob_start <= burst_prob <= prob_end:
            # create burst error
            burst_len = np.random.randint(1, max_burst + 1)
            if idx+burst_len > len(payload_err):
                burst_len = len(payload_err) - idx
            payload_err[idx:idx + burst_len] = 1 - payload_err[idx:idx + burst_len]
            # print(f'burst_len = {burst_len}')
            total_err = total_err + burst_len

            # update error table
            err_table = np.append(err_table, np.zeros((2, 1), dtype=int), axis=1)
            err_table[0, err_cnt] = idx
            err_table[1, err_cnt] = burst_len
            err_cnt = err_cnt + 1
        else:
            burst_len = 0
        idx = idx + burst_len + 1   # once the burst error is suppressed, the next symbol must be correct by definition
    # print(f'total # of errors : {total_err}\n')
    return payload_err, err_table


prob_range = 0.0005
prob_offset = 0.5 - prob_range/2
rs_encoder = sdp.RS_KR4()      # nsym=14, nsize=528, c_exp=10
# rs_encoder = sdp.RS_KP4()      # nsym=30, nsize=544, c_exp=10
# data = sdp.prbs20(1)[:5140*200]
# data = sdp.prbs20(1)[:5140]
nsize = rs_encoder.nsize
data = np.random.randint(0, 2, 5140*2000, dtype=int)

data_encoded = sdp.rs_encode(data, rs_encoder, pam4=False)
data_encoded_with_err, err_record = burst_err_gen2(data_encoded, prob_offset, prob_offset + prob_range)
# block_err = np.zeros(np.size(err_record, 1), dtype=int)
block_err = np.zeros(2000, dtype=int)
for idx in range(0, np.size(err_record, 1)):
    jdx = err_record[0, idx]
    burst_len = err_record[1, idx]
    sym_start = jdx // 10
    sym_end = (jdx + burst_len - 1) // 10
    tmp = sym_end - sym_start + 1
    kdx = jdx // (rs_encoder.nsize * rs_encoder.c_exp)
    block_err[kdx] = block_err[kdx] + tmp
    # block_err[idx] = sym_end - sym_start + 1
    # print(f'# of FEC symbol error = {block_err[idx]} for {burst_len} burst errors')

for idx in range(0, 2000):
    print(f'# of symbol error per block = {block_err[idx]}')

data_decoded = sdp.rs_decode(data_encoded_with_err, rs_encoder, pam4=False)

err = data - data_decoded
total_err = np.sum(abs(err) > 0)
print(f'# of error: {total_err}')
print(f'BER: {total_err / len(data)}')


