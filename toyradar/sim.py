import numpy as np

def simulate(targets, n_pulses, prf, wavelength, noise_power, n_bins, cell_m, stationary=None):

    real_noise = np.random.normal(0, np.sqrt(noise_power / 2), (n_pulses, n_bins))
    imag_noise = np.random.normal(0, np.sqrt(noise_power / 2), (n_pulses, n_bins))

    block = np.zeros((n_pulses, n_bins), dtype=np.complex128) + (real_noise + 1j * imag_noise)

    for target in targets:
        r0 = target['range_m']
        v = target['velocity_m_s']
        a = target['amplitude']

        bin_index = min(n_bins-1, int(r0 / cell_m))

        for pulse in range(n_pulses):
            r = r0 - pulse * v / prf
            block[pulse, bin_index] += a * np.exp(-1j * 4 * np.pi * r / wavelength)

    if stationary:
        r = stationary['range_m']
        a = stationary['amplitude']
        bin_index = min(n_bins-1, int(r / cell_m))
        block[:, bin_index] += a * np.exp(-1j * 4 * np.pi * r / wavelength)


    return block