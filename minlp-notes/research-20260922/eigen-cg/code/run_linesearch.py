"""Line-search heuristic E-CG separation (linesearch.py) at every surveyed fractional vertex of
P_BH(6) (pbh6_fractional_vertices.json).  Usage: python run_linesearch.py restarts iters nworkers"""
import json, sys, time
import numpy as np
import multiprocessing as mp
from fractions import Fraction as Fr
from linesearch import LineSearch


def work(args):
    k, z, restarts, iters = args
    rng = np.random.default_rng(k)
    ls = LineSearch(6, np.array([float(Fr(t)) for t in z]))
    f, v = ls.search(rng, restarts=restarts, iters=iters)
    return k, f, None if v is None else v.tolist()


if __name__ == "__main__":
    restarts, iters, nw = map(int, sys.argv[1:4])
    Z = json.load(open("pbh6_fractional_vertices.json"))
    t = time.time()
    with mp.Pool(nw) as pool:
        res = pool.map(work, [(k, z, restarts, iters) for k, z in enumerate(Z)])
    res.sort(key=lambda r: r[1])
    print("points:", len(res), "time", time.time() - t)
    print("lowest F found:", [(r[0], r[1]) for r in res[:5]])
    json.dump(res, open("linesearch_results.json", "w"))
