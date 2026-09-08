import numpy as np

def rd_map(block, prf, wavelength, window):
    n_pulses, n_bins = block.shape

    if window is None:
        window = np.ones(n_pulses)

    fft_block = np.fft.fft(block * window[:, None], axis=0)
    fft_block = np.fft.fftshift(fft_block, axes=0)

    power_map = np.abs(fft_block) ** 2
    velocities = np.fft.fftshift(np.fft.fftfreq(n_pulses, d=1/prf)) * wavelength / 2

    return power_map.T, velocities


def mti(block):
    return block[1:] - block[:-1]