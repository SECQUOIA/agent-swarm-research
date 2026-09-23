from fractions import Fraction as Fr
import numpy as np, sys
from ecg_feas import ecg_feasibility
z13 = np.array([4, 2, 2, 4, 2, 2, 1, 2, 2, 2, 1, 1, 1, 1, 1, 1, 1, 0, 1, 1, 1]) / 6
print(ecg_feasibility(6, z13, 1/6 - 1e-6, timelimit=float(sys.argv[1]), threads=4))
