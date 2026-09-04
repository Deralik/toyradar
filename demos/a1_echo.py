import matplotlib.pyplot as plt
import numpy as np
import sys
from toyradar.utils import generate_lfm_chirp
from toyradar.compress import apply_matched_filter, index_to_distance

sample_rate = 48000
duration = 0.05
f0 = 2000
f1 = 10000
amplitude = 0.5
c=343.0

def plot_echo(raw, ref, ax, title):
    comp = apply_matched_filter(raw, ref)

    peak_i = np.argmax(comp)
    offset = int((0.5 / c) * sample_rate) #Set a minimum distance of half a meter

    echos = np.where(abs(comp[peak_i+offset:]) > 0.1)[0]

    echo_i = echos[0] + peak_i + offset if len(echos) > 0 else peak_i

    dist = index_to_distance(echo_i, peak_i, sample_rate, c)

    ax[0].plot(raw)
    ax[0].set_title("Raw Signal")
    ax[0].set_xlabel("Sample Index")
    ax[0].set_ylabel("Amplitude")

    ax[1].plot(comp)
    ax[1].axvline(peak_i, color='r', linestyle='--')
    ax[1].axvline(echo_i, color='g', linestyle='--', label=f"Echo Distance: {dist:.2f} m")
    ax[1].set_title(f"Matched Filter Output - {title}")
    ax[1].set_xlabel("Sample Index")
    ax[1].set_ylabel("Amplitude")
    ax[1].legend()

    return

raw_close = np.load('./data/audio/a1_1m_1.npy')[:int(sample_rate*duration * 5)]
raw_far = np.load('./data/audio/a1_1.5m_1.npy')[:int(sample_rate*duration * 5)]
raw_empty = np.load('./data/audio/a1_empty_1.npy')[:int(sample_rate*duration * 5)]

ref_signal = generate_lfm_chirp(sample_rate, duration, f0, f1, amplitude)

fig, ax = plt.subplots(3, 2, figsize=(12, 9), sharex="col")

plot_echo(raw_close, ref_signal, ax[0], "1.0 m")
plot_echo(raw_far,   ref_signal, ax[1], "1.5 m")
plot_echo(raw_empty, ref_signal, ax[2], "empty room")

fig.tight_layout()
fig.savefig("reports/a1_echo.png", dpi=300)
plt.show()
