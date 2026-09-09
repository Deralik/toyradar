from toyradar.datasets import load_ipix
from toyradar.rdmap import rd_map, mti
from toyradar.sim import simulate

from scipy.signal.windows import hann
import matplotlib.pyplot as plt
import numpy as np

np.random.seed(0)

IPIX_DIR   = "./data/ipix/" 
RESULT_DIR = "./reports/"

SNTH_PRF = 5000
SNTH_WAV_L = 0.03
SNTH_N_PULSE = 128
SNTH_N_BINS = 64
SNTH_CELL_W = 30
SNTH_VEL_UA = SNTH_WAV_L * SNTH_PRF / 4
SNTH_DV = 2 * SNTH_VEL_UA / SNTH_N_PULSE

sim_fig,  sim_ax  = plt.subplots(2,  2, figsize=(13, 9))
# real_fig, real_ax = plt.subplots(2,  2, figsize=(13, 9))
# full_fig, full_ax = plt.subplots(14, 2, figsize=(14, 14))

def sim(targets, noise_power, n_pulses=SNTH_N_PULSE, stationary=None):
    return simulate(targets, n_pulses, SNTH_PRF, SNTH_WAV_L, noise_power, SNTH_N_BINS, SNTH_CELL_W, stationary)

# Raw Simulated Signals

stay  = {'range_m': 200, 'velocity_m_s': 0, 'amplitude': 10}
clut  = {'range_m': 900,  'velocity_m_s': 0.3, 'amplitude': 100}
weak   = {'range_m': 900,  'velocity_m_s': 4,   'amplitude': 2}
tgt10 = {'range_m': 1500, 'velocity_m_s': 10, 'amplitude': 10}
tgt50 = {'range_m': 600, 'velocity_m_s': 50, 'amplitude': 10}
targets = [stay, clut, weak, tgt10, tgt50]
block = sim(targets, noise_power=1)

im = sim_ax[0,0].imshow(block.real, aspect='auto', origin='lower',
                        extent=[0, SNTH_N_BINS*SNTH_CELL_W, 0, SNTH_N_PULSE],
                        cmap='RdBu', vmin=-10, vmax=10)
sim_ax[0,0].set_xlabel("Range [m]")
sim_ax[0,0].set_ylabel("Pulse Index")
sim_ax[0,0].set_title(f"Raw Simulated Signals")
sim_fig.colorbar(im, ax=sim_ax[0,0], label="Amplitude (real component)")
sim_fig.tight_layout()

# MTI

block_mti = mti(block)
im = sim_ax[0,1].imshow(block_mti.real, aspect='auto', origin='lower',
                        extent=[0, SNTH_N_BINS*SNTH_CELL_W, 0, SNTH_N_PULSE-1],
                        cmap='RdBu', vmin=-10, vmax=10)
sim_ax[0,1].set_xlabel("Range [m]")
sim_ax[0,1].set_ylabel("Pulse Index")
sim_ax[0,1].set_title("After Two-Pulse MTI")
sim_fig.colorbar(im, ax=sim_ax[0,1], label="Amplitude (real component)")

# Doppler Maps

def top_peaks(row, floor, thr_db=15, n=2, sep=4):
    order = np.argsort(row)[::-1]
    picked = []
    for k in order:
        if 10*np.log10(row[k]/floor) < thr_db:
            break
        if all(abs(k - p) > sep for p in picked):
            picked.append(k)
        if len(picked) == n:
            break
    return picked

def draw_map(fig, ax, power, vel, range_m, title, rows=None, thr_db=15):
    floor = np.median(power)
    cell = range_m[1] - range_m[0]
    img = ax.imshow(10*np.log10(power.T/floor), aspect='auto', origin='lower',
                    extent=[range_m[0], range_m[-1] + cell, vel[0], vel[-1]], vmin=0, vmax=60)
    ax.set_xlabel("Range [m]")
    ax.set_ylabel("Velocity [m/s]")
    ax.set_title(title)
    fig.colorbar(img, ax=ax, label="SNR (dB)")
    for row in (range(power.shape[0]) if rows is None else rows):
        for k in top_peaks(power[row], floor, thr_db):
            ax.plot(range_m[row] + cell/2, vel[k], 'r+', ms=10)
            ax.annotate(f"{vel[k]:+.1f} m/s", (range_m[row], vel[k]), color='w',
                        xytext=(6, 4), textcoords='offset points', fontsize=8)

power, vel = rd_map(block, SNTH_PRF, SNTH_WAV_L, window=None)
draw_map(sim_fig, sim_ax[1,0], power, vel, np.arange(SNTH_N_BINS)*SNTH_CELL_W, "Range-Doppler Map")
power, vel = rd_map(block, SNTH_PRF, SNTH_WAV_L, window=hann(SNTH_N_PULSE))
draw_map(sim_fig, sim_ax[1,1], power, vel, np.arange(SNTH_N_BINS)*SNTH_CELL_W,  "Range-Doppler Map (Hann)")

sim_fig.tight_layout()
sim_fig.savefig(RESULT_DIR + "a2_synthetic.png", dpi=120)

# Real Data

iq, meta = load_ipix(IPIX_DIR + "19931107_135603_starea.cdf", "HH")
prf   = meta['prf_hz']
lam   = 3e8 / (meta['rf_ghz'] * 1e9)
rng_m = meta['range_m']
NB    = 512
blk   = iq[:NB]
lim   = np.percentile(np.abs(blk.real), 99)

real_fig, real_ax = plt.subplots(2, 2, figsize=(13, 9))

im = real_ax[0,0].imshow(blk.real, aspect='auto', origin='lower',
                         extent=[rng_m[0], rng_m[-1] + 15, 0, NB], cmap='RdBu', vmin=-lim, vmax=lim)
real_ax[0,0].set_xlabel("Range [m]"); real_ax[0,0].set_ylabel("Pulse Index")
real_ax[0,0].set_title("IPIX File 17 (HH)")
real_fig.colorbar(im, ax=real_ax[0,0], label="Amplitude (real component)")

blk_mti = mti(blk)
im = real_ax[0,1].imshow(blk_mti.real, aspect='auto', origin='lower',
                         extent=[rng_m[0], rng_m[-1] + 15, 0, NB-1], cmap='RdBu', vmin=-lim, vmax=lim)
real_ax[0,1].set_xlabel("Range [m]"); real_ax[0,1].set_ylabel("Pulse Index")
real_ax[0,1].set_title("After Two-Pulse MTI")
real_fig.colorbar(im, ax=real_ax[0,1], label="Amplitude (real component)")

power, vel = rd_map(blk, prf, lam, hann(NB))
draw_map(real_fig, real_ax[1,0], power, vel, rng_m, "Range-Doppler Map (one block)")

nblk = iq.shape[0] // NB
acc = np.zeros_like(power)
for k in range(nblk):
    acc += rd_map(iq[k*NB:(k+1)*NB], prf, lam, hann(NB))[0]
acc /= nblk
draw_map(real_fig, real_ax[1,1], acc, vel, rng_m, f"Range-Doppler Map ({nblk} blocks averaged)")
for ax in real_ax[1]:
    ax.axvline(rng_m[8] + 7.5, color='r', ls=':', lw=1)

real_fig.tight_layout()
real_fig.savefig(RESULT_DIR + "a2_ipix17.png", dpi=120)

plt.show()