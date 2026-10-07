"""Item 2 of theory-decomposition/revision_checks.py (the only item that calls certificate()),
with the current (widened) pair test: n = 9, x* = 0, theta = 1/16, h = 2^-8."""
import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", "theory-decomposition"))
import numpy as np
import dp_certificate as dc
print("PAIR_TOL = %g" % dc.PAIR_TOL)
r, size, _, _ = dc.certificate(9, 0.8, 0.1, np.zeros(9), np.zeros(9), 2.0 ** -8, 4)
print("gap %.3e size %d (full precision gap %.10e)" % (-r, size, -r))
