import numpy as np
import sounddevice as sd
from toyradar.utils import generate_lfm_chirp


def capture_lfm_chirp(sample_rate, duration, f0, f1, amplitude=1.0):

    tone = generate_lfm_chirp(sample_rate, duration, f0, f1, amplitude)

    tone = np.pad(tone, (0, int(sample_rate*0.2))) # Pad 200ms to catch echos

    recorded_signal = sd.playrec(tone, samplerate=sample_rate, channels=1, dtype='float32', blocking=True)
    
    return recorded_signal
