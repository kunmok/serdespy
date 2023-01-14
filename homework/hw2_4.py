'''
    Test how many of symbol errors KP4 can correct.
'''
import serdespy as sdp
import numpy as np
import matplotlib.pyplot as plt
import time


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
            burst_len = np.random.randint(1, 21)
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


# data = sdp.prbs20(1)[:1000000]
prob_range = 0.005
prob_offset = 0.5 - prob_range/2
data = sdp.prbs20(1)[:3000]

cnt = 0
while cnt < 20:
    encoder_kp4 = sdp.RS_KP4()
    data_encoded2 = sdp.rs_encode(data, encoder_kp4, pam4=False)
    data_encoded_with_err2, err_record = burst_err_gen2(data_encoded2, prob_offset, prob_offset + prob_range)

    # calculate number of symbols affected.
    block_err = np.zeros(np.size(err_record, 1), dtype=int)
    for idx in range(0, np.size(err_record, 1)):
        jdx = err_record[0, idx]
        burst_len = err_record[1, idx]
        sym_start = jdx // 10
        sym_end = (jdx + burst_len - 1) // 10
        block_err[idx] = sym_end - sym_start + 1
        # print(f'# of FEC symbol error = {block_err[idx]} for {burst_len} burst errors')

    if np.sum(block_err) == 16:     # sometimes it fails to correct errors
    # if np.sum(block_err) == 15:     # no failure
        print(f' ***** RS-KP4 *****')
        print(f'total # of FEC symbol errors = {np.sum(block_err)}\n')
        print(err_record)
        print(block_err)
        data_decoded2 = sdp.rs_decode(data_encoded_with_err2, encoder_kp4, pam4=False)

        err2 = data - data_decoded2
        total_err2 = np.sum(abs(err2) > 0)
        print(f'# of error (KP4): {total_err2}')
        print(f'# POST-FEC BER (KP4): {total_err2 / len(data)}')
        cnt = cnt + 1

        print(f'!!!!! End !!!!! \n\n')

        # Conclusion: KP4 performs slightly better than KR4.
