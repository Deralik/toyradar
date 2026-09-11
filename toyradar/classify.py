import numpy as np
from toyradar.utils import db_to_power, power_to_db

FEATURE_NAMES = ["range_offset", "doppler_peak_offset", "doppler_centroid", "doppler_spread",
                 "main_lobe_fraction_db", "half_power_width", "contrast_db", "peak_power_dbm",
                 "range_extent"]

def features(map):
    power = db_to_power(map)

    n_range, n_doppler = power.shape
    centre_range = n_range // 2
    centre_doppler = n_doppler // 2

    power_dist = power.sum(axis=1)

    peak_i = np.argmax(power_dist)

    peak_row = power[peak_i]
    peak_col = np.argmax(peak_row)

    d_offset = np.arange(n_doppler) - centre_doppler

    #First feature: dist of the peak range from the center
    r_offset = peak_i - centre_range                

    #Second: dist between the peak doppler bin and center
    d_offset_peak = peak_col - centre_doppler       

    #Third: dist of the power-weighted centroid from the center
    doppler_centroid = np.sum(d_offset * peak_row) / np.sum(peak_row)

    #Forth: power-weighted standard deviation around the centroid
    doppler_spread = np.sqrt(np.sum((d_offset - doppler_centroid) ** 2 * peak_row) / np.sum(peak_row))  

    #Fith: Share of the power dist near the peak velocity bin. How rigid the object is. 
    near_bins = 2
    lo = max(peak_col - near_bins, 0)
    hi = min(peak_col + near_bins + 1, n_doppler)
    main_lobe_fraction_db = power_to_db(np.sum(peak_row[lo:hi]) / np.sum(peak_row))

    #Sixth: count of activated velocity bins above half the peak. 
    half_power_width = np.sum(peak_row > 0.5 * peak_row.max())

    #Seventh: how far the peak stands above its own floor
    contrast_db = power_to_db(peak_row.max() / np.median(power))

    #Eighth: peak echo strength. (prob the least unique because of distance)
    peak_power_dbm = power_to_db(power.max())

    #Nineth: span of the echo along the range. (how long the object is)
    range_extent = np.sum(power_dist > 0.1 * power_dist.max())

    return np.array([
        r_offset,
        d_offset_peak,
        doppler_centroid,
        doppler_spread,
        main_lobe_fraction_db,
        half_power_width,
        contrast_db,
        peak_power_dbm,
        range_extent,
    ], dtype=np.float32)

