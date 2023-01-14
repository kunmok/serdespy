'''
    check and see if sym err = 16 causes error on KP4
    Answer: sometimes no, sometimes yes.
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
    print(f'total # of errors : {total_err}\n')
    return payload_err, err_table


err_cnt = 0
while err_cnt != 16:
    # data = sdp.prbs20(1)[:1000000]
    # prob_range = 0.005
    prob_range = 0.0015
    # prob_range = 0.02
    prob_offset = 0.5 - prob_range/2
    # data = sdp.prbs20(1)[:1000]
    data = sdp.prbs20(1)[:5140]

    encoder_kr4 = sdp.RS_KR4()      # nsym=14, nsize=528, c_exp=10
    '''
        every symbol consists of 10 bits. Then it adds extra 14 parity symbols, adding 14*10 = 140 bits to every data block.
        Each RS-encoded block consists of maximum 10*528 = 5280 bits.
        This is able to correct up to 7 symbols (70)   
    '''
    data_encoded = sdp.rs_encode(data, encoder_kr4, pam4=False)
    data_encoded_with_err, err_record = burst_err_gen2(data_encoded, prob_offset, prob_offset + prob_range)
    print(err_record)

    # calculate number of symbols affected.
    block_err = np.zeros(np.size(err_record, 1), dtype=int)
    for idx in range(0, np.size(err_record, 1)):
        jdx = err_record[0, idx]
        burst_len = err_record[1, idx]
        sym_start = jdx // 10
        sym_end = (jdx + burst_len - 1) // 10
        block_err[idx] = sym_end - sym_start + 1
        print(f'# of FEC symbol error = {block_err[idx]} for {burst_len} burst errors. idx = {jdx}')
    print(f'total # of FEC symbol errors = {np.sum(block_err)}\n')

    data_decoded = sdp.rs_decode(data_encoded_with_err, encoder_kr4, pam4=False)
    err = data - data_decoded
    total_err = np.sum(abs(err) > 0)
    print(f' ***** RS-KR4 *****')
    print(f'# of error (KR4): {total_err}')
    print(f'# POST-FEC BER (KR4): {total_err / len(data)}\n')


    print(f' ***** RS-KP4 *****')
    encoder_kp4 = sdp.RS_KP4()
    data_encoded2 = sdp.rs_encode(data, encoder_kp4, pam4=False)
    data_encoded_with_err2 = np.copy(data_encoded2)

    for idx in range(0, np.size(err_record, 1)):
        jdx = err_record[0, idx]
        burst_len = err_record[1, idx]
        data_encoded_with_err2[jdx: jdx + burst_len] = 1 - data_encoded_with_err2[jdx: jdx + burst_len]

    data_decoded2 = sdp.rs_decode(data_encoded_with_err2, encoder_kp4, pam4=False)

    err2 = data - data_decoded2
    total_err2 = np.sum(abs(err2) > 0)
    print(f'# of error (KP4): {total_err2}')
    print(f'# POST-FEC BER (KP4): {total_err2 / len(data)}')

    err_cnt = np.sum(block_err)

