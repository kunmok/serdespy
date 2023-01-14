import serdespy as sdp
import numpy as np
import matplotlib.pyplot as plt
import skrf as rf
import scipy as sp
from math import log10

nyquist_f = 25e9
samples_per_symbol = 64
voltage_levels = np.array([-3, -1, 1, 3])
# voltage_levels = np.array([-1, 1])
tx_rj = 0.025
rx_noise = 0.01

data = sdp.prqs10(1)

TX = sdp.Transmitter(data, voltage_levels, nyquist_f)
TX.FIR([0, 1])
TX.oversample(samples_per_symbol)
TX.gaussian_jitter(stdev_div_UI=tx_rj)
TX.tx_bandwidth(freq_bw=100e9)
signal_out = TX.signal

# CTLE
# create a Butterworth-type low-pass filter with 20, 30, 40, 50 GHz bandwidth
pi = np.pi
# lpf_bw = 10e9
# lpf_bw = 20e9
# lpf_bw = 30e9
# lpf_bw = 40e9
lpf_bw = 50e9

b, a = sp.signal.butter(4, lpf_bw*(2*pi), btype='low', analog=True)

#frequency vector in rad/s
f = np.arange(1e6, 100e9, 10e6)
w = f*(2*np.pi)

#calculate Frequency response of LPF at given frequencies
w, H_ctle = sp.signal.freqs(b, a, w)
f = w/(2*pi)

#%% compute and save impulse response of LPF transfer function
h_ctle, t_ctle = sdp.freq2impulse(H_ctle, f)
crop = 50
h_ctle = np.roll(h_ctle, crop)

signal_out_ctle = sp.signal.fftconvolve(signal_out, h_ctle, mode="same")
# RX = sdp.Receiver(signal_out_ctle, samples_per_symbol*2, nyquist_f, voltage_levels, shift=True, main_cursor=0.5006377086200736)
RX = sdp.Receiver(signal_out_ctle, samples_per_symbol, nyquist_f, voltage_levels, shift=True, main_cursor=1.0)
RX.noise(rx_noise)
RX.FFE(np.array([0, 1]), 2)
sdp.simple_eye(RX.signal[samples_per_symbol*3000:], samples_per_symbol*2, 2000, TX.UI/TX.samples_per_symbol,
               f"Eye Diagram @ Rx. LPF bw = {lpf_bw/1e9} GHz, \nTx Jitter = {tx_rj} UI_rms, Rx noise = {rx_noise/1e-3} mVrms",
               res=120)

# np.save("./data/signal.npy", signal_out)
