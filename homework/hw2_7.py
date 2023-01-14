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


# data = sdp.prbs20(1)[:1000000]
data = np.random.randint(0, 2, 10000000, dtype=int)
# prob_range = 0.5
prob_range = 0.005
# prob_range = 0.006
# prob_range = 0.01
# prob_range = 0.02
prob_offset = 0.5 - prob_range/2
data_with_err = burst_err_gen(data, prob_offset, prob_offset + prob_range)
err = data - data_with_err
total_err = np.sum(abs(err) > 0)
print(f'# of error: {total_err}')
print(f'BER: {total_err / len(data)}')
