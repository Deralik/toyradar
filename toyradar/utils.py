import numpy as np


def power_to_db(p):
    return 10 * np.log10(p)

def db_to_power(db):
    return 10 ** (db / 10)