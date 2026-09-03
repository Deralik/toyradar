import sounddevice as sd
import numpy as np
import matplotlib.pyplot as plt
import toyradar.utils as utils


try:
    sd.default.samplerate = 48000

    t = np.arange(48000) / 48000
    tone = (0.3 * np.sin(2 * np.pi * 1000 * t)).astype(np.float32)
    out = sd.playrec(tone, channels=1, blocking=True)

    plt.plot(out[47000:])
    plt.title("Recorded Audio Signal")
    plt.xlabel("Sample Index")
    plt.ylabel("Amplitude")

    np.save("./data/audio/1kHz_tone.npy", out)

    print(f'avg DB: {utils.power_to_db(np.var(out)):.2f} dB')

    plt.show()

except KeyboardInterrupt:
    print("\nExiting...")
    exit(0)
except Exception as e:
    print(f"Error: {e}")
    exit(1)