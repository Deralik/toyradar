import numpy as np


def apply_matched_filter(raw_signal, ref_signal):
    raw_norm = raw_signal / np.linalg.norm(raw_signal)
    ref_norm = ref_signal / np.linalg.norm(ref_signal)

    return np.correlate(raw_norm, ref_norm).astype(np.float32)

def index_to_distance(index, peak_index, sample_rate, c=343.0):
    time_delay = (index - peak_index) / sample_rate
    distance = (time_delay * c) / 2
    
    return distance
