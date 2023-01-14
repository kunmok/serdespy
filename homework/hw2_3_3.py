'''
    check the typical length of burst error.
    Question to answer: is it common to have burst error len > 3 symbol ?
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


# prob_range = 0.005
prob_range = 0.0005
# prob_range = 0.02
prob_offset = 0.5 - prob_range/2
data = np.random.randint(0, 2, 5140*2000, dtype=int)
# data = np.random.randint(0, 2, 5140*200, dtype=int)
# data = sdp.prbs20(1)[:2500]
# data = sdp.prbs20(1)[:5140]

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
burst_cnt = 0
burst_cont = 0
cnt = 1
for idx in range(np.size(err_record, 1) - 1):
    jdx = err_record[0, idx]
    burst_len = err_record[1, idx]
    sym_start = jdx // 10
    sym_mid = (jdx + burst_len - 1) // 10

    if burst_cont == 0:
        burst_tmp = sym_mid - sym_start + 1
    else:
        burst_tmp = sym_mid - sym_start
    sym_end = err_record[0, idx+1] // 10

    if (sym_end - sym_mid) == 0:
        burst_cont = 1
        burst_cnt = burst_cnt + burst_tmp
    else:
        if burst_cont > 0:
            burst_cnt = burst_cnt + burst_tmp
            # print(f'# of FEC symbol error = {burst_cnt}')
            # if burst_cnt > 5:
            # if burst_cnt > 4:
            if burst_cnt > 3:
                print(f'# of FEC symbol error = {burst_cnt}, count = {cnt}')
                cnt = cnt + 1
        burst_cont = 0
        burst_cnt = 0


# print(f'total # of FEC symbol errors = {np.sum(err_record[1,:])}\n')

data_decoded = sdp.rs_decode(data_encoded_with_err, encoder_kr4, pam4=False)
err = data - data_decoded
total_err = np.sum(abs(err) > 0)

pe = prob_range
max_burst = 20
p_unif = 1/max_burst
num = pe * p_unif * np.sum(np.arange(1, max_burst + 1))
den = (1 - pe) + pe * p_unif * (np.sum(np.arange(1, max_burst + 1)) + max_burst)
prefec_ber = num / den

print(f' ***** RS-KR4 *****')
print(f'# of error (KR4): {total_err}')
print(f'PRE-FEC BER (KR4): {prefec_ber}')
print(f'POST-FEC BER (KR4): {total_err / len(data)}\n')

