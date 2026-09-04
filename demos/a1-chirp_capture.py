import numpy as np
import matplotlib.pyplot as plt
from toyradar.capture import capture_lfm_chirp
import time
import sys



time.sleep(3) 

output = np.empty(0, dtype=np.float32)
for i in range(5):
    chirp = capture_lfm_chirp(sample_rate=48000, duration=0.05, f0=2000, f1=10000, amplitude=0.5)
    output = np.concatenate((output, chirp.flatten()))


plt.plot(output)
plt.title("Captured LFM Chirp Signal")
plt.xlabel("Sample Index")
plt.ylabel("Amplitude")
plt.show()

if len(sys.argv) > 1:
    np.save(f'./data/audio/a1_{sys.argv[1]}.npy', output)
