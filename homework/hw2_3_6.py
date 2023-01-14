'''
    check the typical length of burst error.
    Question to answer: is it common to have burst error len > 3 symbol ? (also check 1 symbol err too)
'''
import serdespy as sdp
import numpy as np
import scipy
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
block_size = 10000
data = np.random.randint(0, 2, 5140*block_size, dtype=int)
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
cnt = np.zeros(6, dtype=int)
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
    # print(sym_start)
    # print(sym_mid)
    # print(sym_end)
    if (sym_end - sym_mid) == 0:
        burst_cont = 1
        burst_cnt = burst_cnt + burst_tmp
    else:   # burst is broken
        if burst_cont > 0:
            burst_cnt = burst_cnt + burst_tmp

            if burst_cnt == 2:
                cnt[1] = cnt[1] + 1
                # print(f'# of FEC 2x symbol error = {burst_cnt}, count = {cnt[1]}')
            elif burst_cnt == 3:
                cnt[2] = cnt[2] + 1
                # print(f'# of FEC 3x symbol error = {burst_cnt}, count = {cnt[2]}')
            elif burst_cnt == 4:
                cnt[3] = cnt[3] + 1
                # print(f'# of FEC 4x symbol error = {burst_cnt}, count = {cnt[3]}')
            elif burst_cnt == 5:
                cnt[4] = cnt[4] + 1
                # print(f'# of FEC 5x symbol error = {burst_cnt}, count = {cnt[4]}')
            else:
                cnt[5] = cnt[5] + 1
                # print(f'# of FEC 6x or more symbol error = {burst_cnt}, count = {cnt[5]}')

        burst_cont = 0
        burst_cnt = 0

tmp1 = 0
tmp2 = 0
tmp3 = 0
symbol_div = np.zeros(block_size, dtype=int)
err_storage = np.zeros((block_size, 2), dtype=int)
cnt_err = 1
cnt = np.zeros(6, dtype=int)
idx = 0
burst_cnt_arr = np.zeros(0)
while idx < np.size(err_record, 1)-1:
    jdx = err_record[0, idx]
    burst_len = err_record[1, idx]
    sym_start = jdx // 10
    sym_mid = (jdx + burst_len - 1) // 10

    burst_cnt = sym_mid - sym_start + 1
    if (5280 * (cnt_err-1)) <= err_record[0, idx] < (5280 * cnt_err):
        burst_cnt_arr = np.append(burst_cnt_arr, burst_cnt)
        symbol_div[cnt_err-1] = symbol_div[cnt_err-1] + burst_cnt
        if (5280 * (cnt_err)) <= err_record[0, idx+1]:
            if symbol_div[cnt_err - 1] == 2:
                if len(burst_cnt_arr) == 1:
                    err_storage[cnt_err - 1, 0] = burst_cnt_arr[0]
                else:
                    err_storage[cnt_err - 1, :] = burst_cnt_arr[0:2]
            burst_cnt_arr = np.zeros(0)
        idx = idx + 1
    else:
        cnt_err = cnt_err + 1
index_arr_sym2 = np.where(symbol_div == 2)[0]
err_storage = err_storage[index_arr_sym2, :]
err_storage_max = np.max(err_storage, axis=1)
num_1 = np.count_nonzero(err_storage_max == 1)
num_2 = np.count_nonzero(err_storage_max == 2)
index_arr_sym1 = np.where(symbol_div == 1)[0]
index_arr_noerr = np.where(symbol_div == 0)[0]
print(f'# of no errors: {len(index_arr_noerr)}')
print(f'# of 1 errors: {len(index_arr_sym1)}')
print(f'probability of having [1] = {len(index_arr_sym1)/block_size}')

print(f'# of 2 errors: {len(err_storage_max)}')
print(f'probability of having [1, 1] = {num_1/len(err_storage_max)}')
print(f'probability of having [2, 0] = {num_2/len(err_storage_max)}')

symbol_div = np.zeros(block_size, dtype=int)
err_storage = np.zeros((block_size, 3), dtype=int)
cnt_err = 1
cnt = np.zeros(6, dtype=int)
idx = 0
burst_cnt_arr = np.zeros(0)
while idx < np.size(err_record, 1)-1:
    jdx = err_record[0, idx]
    burst_len = err_record[1, idx]
    sym_start = jdx // 10
    sym_mid = (jdx + burst_len - 1) // 10

    burst_cnt = sym_mid - sym_start + 1
    if (5280 * (cnt_err-1)) <= err_record[0, idx] < (5280 * cnt_err):
        burst_cnt_arr = np.append(burst_cnt_arr, burst_cnt)
        symbol_div[cnt_err-1] = symbol_div[cnt_err-1] + burst_cnt
        if (5280 * (cnt_err)) <= err_record[0, idx+1]:
            if symbol_div[cnt_err - 1] == 3:
                if len(burst_cnt_arr) == 1:
                    err_storage[cnt_err - 1, 0] = burst_cnt_arr[0]
                elif len(burst_cnt_arr) == 2:
                    err_storage[cnt_err - 1, 0:2] = burst_cnt_arr[0:2]
                else:
                    err_storage[cnt_err - 1, :] = burst_cnt_arr[0:3]
            burst_cnt_arr = np.zeros(0)
        idx = idx + 1
    else:
        cnt_err = cnt_err + 1
index_arr_sym3 = np.where(symbol_div == 3)[0]
err_storage = err_storage[index_arr_sym3, :]
err_storage_max = np.max(err_storage, axis=1)
num_1 = np.count_nonzero(err_storage_max == 1)
num_2 = np.count_nonzero(err_storage_max == 2)
num_3 = np.count_nonzero(err_storage_max == 3)
print(f'# of 3 errors: {len(err_storage_max)}')
print(f'probability of having [1, 1, 1] = {num_1/len(err_storage_max)}')
print(f'probability of having [1, 2] = {num_2/len(err_storage_max)}')
print(f'probability of having [3, 0] = {num_3/len(err_storage_max)}')
print(f'probability of having [1, 1, 1] 22 = {num_1/(num_1 + num_3)}')
print(f'probability of having [3, 0] 22 = {num_3/(num_1 + num_3)}')

for idx in range(np.size(err_record, 1)):
    jdx = err_record[0, idx]
    burst_len = err_record[1, idx]
    sym_start = jdx // 10
    sym_mid = (jdx + burst_len - 1) // 10

    burst_cnt = sym_mid - sym_start + 1

    if burst_cnt == 1:
        cnt[0] = cnt[0] + 1
        tmp1 = tmp1 + burst_len
    elif burst_cnt == 2:
        cnt[1] = cnt[1] + 1
        tmp2 = tmp2 + burst_len
    else:
        cnt[2] = cnt[2] + 1
        tmp3 = tmp3 + burst_len
    burst_cnt = 0
print(symbol_div)

print(f'# of FEC 1x symbol error = {cnt[0]}')
print(f'# of FEC 2x symbol error = {cnt[1]}')
print(f'# of FEC 3x symbol error = {cnt[2]}')
print(f'# of FEC 4x symbol error = {cnt[3]}')
print(f'# of FEC 5x symbol error = {cnt[4]}')
print(f'# of FEC 6x symbol error = {cnt[5]}')

print(f'Avg bit error for 1x symbol = {tmp1/(cnt[0])}')
print(f'Avg bit error for 2x symbol = {tmp2/(cnt[1])}')
print(f'Avg bit error for 3x symbol = {tmp3/(cnt[2])}')

