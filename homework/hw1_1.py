import serdespy as sdp
import numpy as np
import matplotlib.pyplot as plt
import skrf as rf
import scipy as sp
from math import log10

nyquist_f = 25e9
samples_per_symbol = 64
voltage_levels = np.array([-1, 1])

data = sdp.prbs13(1)

TX = sdp.Transmitter(data, voltage_levels, nyquist_f)
TX.FIR([0, 1])
TX.oversample(samples_per_symbol)
TX.gaussian_jitter(stdev_div_UI=0.025)
TX.tx_bandwidth(freq_bw=100e9)

# sdp.simple_eye(TX.signal, samples_per_symbol*2, 2000, TX.UI/TX.samples_per_symbol, "TX Bandwidth-Limited Eye Diagram (-3dB frequency at 120GHz)", res=100)
signal_out = TX.signal

# CTLE
# create a Bessel-type low-pass filter with 20, 30, 40, 50 GHz bandwidth
pi = np.pi
# lpf_bw = 1e9
lpf_bw = 20e9
# lpf_bw = 30e9
# lpf_bw = 40e9
# lpf_bw = 50e9

b, a = sp.signal.butter(4, lpf_bw*(2*pi), btype='low', analog=True)
# b, a = sp.signal.butter(4, lpf_bw*(2*pi), btype='low', analog=True)
# b, a = sp.signal.bessel(4, lpf_bw*(2*pi), btype='low', analog=True)
# b, a = sp.signal.zpk2tf([1], [lpf_bw*2*np.pi], 1)
# b *= 1/(b[-1]/a[-1])

#frequency vector in rad/s
f = np.arange(1e6, 100e9, 10e6)
w = f*(2*np.pi)

#calculate Frequency response of CTLE at given frequencies
w, H_ctle = sp.signal.freqs(b, a, w)
f = w/(2*pi)

#bode plot of CTLE transfer function
# plt.figure(dpi=100)
# plt.semilogx(f*1e-9, 20*np.log10(abs(H_ctle)), color="red", label="ctle")
# plt.ylabel('Mag. Response [dB]')
# plt.xlabel('Frequency [GHz]')
# plt.title("CTLE Bode Plot")
# plt.xlim([1, 100])
# plt.ylim([-20, 5])
# plt.grid()
# plt.axvline(x=20, color='grey', label="Nyquist Frequency")
# plt.show()

#%% compute and save impulse response of CTLE transfer function
h_ctle, t_ctle = sdp.freq2impulse(H_ctle, f)

# crop = 200
# crop = 10000
crop = 50

h_ctle = np.roll(h_ctle, crop)

# plt.figure(dpi=100)
# plt.plot(t_ctle, h_ctle, linewidth=3)
# plt.show()

signal_out_ctle = sp.signal.fftconvolve(signal_out, h_ctle, mode="same")
# RX = sdp.Receiver(signal_out_ctle, samples_per_symbol*2, nyquist_f, voltage_levels, shift=True, main_cursor=0.5006377086200736)
RX = sdp.Receiver(signal_out_ctle, samples_per_symbol, nyquist_f, voltage_levels, shift=True, main_cursor=1.0)
# RX.noise(0.00001)
# RX.FFE(np.array([0, 1]), 2)
sdp.simple_eye(RX.signal[samples_per_symbol*3000:], samples_per_symbol*2, 2000, TX.UI/TX.samples_per_symbol, f"Eye Diagram with Low-Pass Filter", res=100)

# np.save("./data/signal.npy", signal_out)
