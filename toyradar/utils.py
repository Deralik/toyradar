import numpy as np

# 00-Initial tests
def power_to_db(p):
    return 10 * np.log10(p)

def db_to_power(db):
    return 10 ** (db / 10)


#01-Waveform generation
def generate_lfm_chirp(sample_rate, duration, f0, f1, amplitude=1.0):

    n_samples = int(sample_rate * duration)
    t = np.linspace(0, duration, n_samples, endpoint=False)

    c = (f1 - f0) / duration

    return (amplitude * np.sin(2 *np.pi * (c * t**2 / 2 + f0 * t))).astype(np.float32)