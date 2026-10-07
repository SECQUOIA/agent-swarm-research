"""Rerun research-20260928b/sfree/code/exp_loop.py with the corner bound computed by zk_fast
(exact for bilinear constraints, rho = 2, with the antiparallel-ray guard) instead of
core.corner_bound, whose two_ray can underestimate z_K when two projected rays are antiparallel.
exp_loop uses z_K as the bisection scale of the orbit rule (the orbit bound is capped at z_K)
and for the corner-optimal cut.  Arguments are passed unchanged to exp_loop.py."""
import os, sys, runpy
import numpy as np
SFREE = os.path.join(os.path.dirname(os.path.abspath(__file__)), '../../../research-20260928b/sfree/code')
sys.path.insert(0, SFREE)
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import core
import zk_fast as Z


def corner_bound_fixed(Q, b, c, sbar, P, w, max_support=None, return_point=False):
    Qr, br, cr, sr, Pr, rho, _ = Z.reduce_space(Q, b, c, sbar, P)
    assert rho <= 2
    z, _ = Z.zK_upto2(Qr, br, cr, sr, Pr, w)
    return (z, None) if return_point else z


core.corner_bound = corner_bound_fixed
sys.argv = [os.path.join(SFREE, 'exp_loop.py')] + sys.argv[1:]
runpy.run_path(os.path.join(SFREE, 'exp_loop.py'), run_name='__main__')
