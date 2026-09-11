import numpy as np
import scipy.io 
import glob
import os
import re

def load_ipix(path, channel):
    f = scipy.io.netcdf_file(path, mmap=False)

    meta = {
        "range_m": f.variables["range"].data.astype(np.float32),
        "prf_hz": float(f.variables["PRF"].data),
        "rf_ghz": float(f.variables["RF_frequency"].data),
        "u_velocity_mps": float(f.variables["Unambig_velocity"].data),
        "azimuth_deg":  float(f.variables["azimuth_angle"].data[0])
    }

    raw = f.variables["adc_data"].data.view(np.uint8).astype(np.float64)

    match channel:
        case "HH":
            tx = 0
            i_adc = 0
            q_adc = 1
        case "VV":
            tx = 1
            i_adc = 0
            q_adc = 1
        case "HV":
            tx = 0
            i_adc = 2
            q_adc = 3
        case "VH":
            tx = 1
            i_adc = 2
            q_adc = 3
        case _:
            print(f"Unknown Channel {channel}, (HH, VV, HV, VH)")
            return None

    I = raw[:, tx, :, i_adc]
    Q = raw[:, tx, :, q_adc]
    
    I -= np.mean(I)
    Q -= np.mean(Q)

    I /= np.std(I)
    Q /= np.std(Q)

    s = np.mean(I * Q)

    I = (I - Q * s) / np.sqrt(1 - s**2)

    complex_data = I + 1j * Q

    return complex_data, meta


def load_raddar(root):
    maps, cls, session, frame = [], [], [], []
    for c in ("Cars", "Drones", "People"):
        for sp in sorted(glob.glob(os.path.join(root, c, "*/"))):
            s = f"{c}/{os.path.basename(sp.rstrip('/'))}"
            files = sorted(glob.glob(os.path.join(sp, "*.csv")),
                           key=lambda p: int(re.findall(r"(\d+)\.csv$", p)[0]))
            for f in files:
                m = np.loadtxt(f, delimiter=",")
                if m.shape != (11, 61):
                    continue
                maps.append(m)
                cls.append(c)
                session.append(s)
                frame.append(int(re.findall(r"(\d+)\.csv$", f)[0]))
    return np.array(maps), np.array(cls), np.array(session), np.array(frame)
