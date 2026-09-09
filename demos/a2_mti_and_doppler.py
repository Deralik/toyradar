from toyradar.datasets import load_ipix
from toyradar.rdmap import rd_map
from toyradar.sim import simulate

import matplotlib.pyplot as plt
import numpy as np

IPIX_DIR   = "./data/ipix/" 
RESULT_DIR = "./reports/"

SNTH_PRF = 5000
SNTH_WAV_L = 0.03
SNTH_N_PULSE = 128
SNTH_N_BINS = 64
SNTH_CELL_W = 30
SNTH_VEL_UA = SNTH_WAV_L * SNTH_PRF / 4
SNTH_DV = 2 * SNTH_VEL_UA / SNTH_N_PULSE


