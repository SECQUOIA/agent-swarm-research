"""Re-audit one saved spar triangle model without the original early stop.

Run under timeout 1800 with OMP_NUM_THREADS=1. This follows the r1 reviewer's
strict audit, but accepts an instance name and records the unthresholded
maximum triangle violation. Original checkpoints and review files are read-only.
Usage from the stream directory: python code/strict_spar_audit.py NAME
"""
import json
import sys
import time
from pathlib import Path

import numpy as np

from relax import Relax, all_triples, read_boxqp, separate_triangles, triple_moment_matrices
import hullsep


def main():
    name = sys.argv[1]
    root = Path(__file__).resolve().parent.parent
    out = root / 'logs/strict_r1' / name
    out.parent.mkdir(exist_ok=True)
    sources = root / 'sources/BoxQP_instances-master'
    H, g = read_boxqp(str(next(sources.glob('*/' + name + '.in'))))
    opt = next(-float(t[1]) for line in (sources / 'README.txt').read_text().splitlines()
               if len(t := line.split()) == 2 and t[0] == name)
    started = time.time()
    T = all_triples(len(g))
    R = Relax(H, g, name)
    for c in json.loads((root / 'logs/spar_audit' / (name + '.json.tri.json')).read_text()):
        R.add_triangle(*c)
    rounds = []
    solve_tol = 1e-8
    for rnd in range(8):
        res = R.solve('clarabel', tol=solve_tol)
        x, Y = res['xv'], res['Y']
        cuts, _ = separate_triangles(x, Y, tol=1e-8, cap=None, triples=T)
        new = [c for c in cuts if c not in R.tri_added]
        i, j, k = T.T
        maximum = max(0.0, float(np.max(np.stack([
            Y[i, j] + Y[i, k] - x[i] - Y[j, k],
            Y[i, j] + Y[j, k] - x[j] - Y[i, k],
            Y[i, k] + Y[j, k] - x[k] - Y[i, j],
            x[i] + x[j] + x[k] - Y[i, j] - Y[i, k] - Y[j, k] - 1]))))
        rounds.append(dict(round=rnd, B=res['pobj'], B_safe=res['safe'],
                           status=res['status'], pinf=float(res['pinf']),
                           time_solve=res['time_solve'], solve_tol=solve_tol,
                           new_triangles=len(new), max_triangle_violation=maximum))
        print(json.dumps(rounds[-1]), flush=True)
        info = dict(rounds[-1], name=name, tri=len(R.tri_added), rounds=rounds,
                    triangle_strict=maximum <= 1e-8)
        np.savez(str(out) + '.base.npz', x=x, Y=Y, info=json.dumps(info))
        Path(str(out) + '.base.json').write_text(json.dumps(info, indent=2) + '\n')
        if maximum <= 1e-8:
            break
        if not new:
            if solve_tol == 1e-10:
                raise RuntimeError('Existing triangles exceed strict tolerance; no strict audit claimed')
            solve_tol = 1e-10
        for c in new:
            R.add_triangle(*c)
    else:
        raise RuntimeError('Triangle round limit reached; no strict audit claimed')

    depth_started = time.time()
    depths = np.full(len(T), np.nan)
    for s in range(0, len(T), 20000):
        M = triple_moment_matrices(x, Y, T[s:s + 20000])
        depths[s:s + len(M)] = [hullsep.depth(Mi)[0] for Mi in M]
        np.savez(str(out) + '.depth.npz', depths=depths)
        print(json.dumps(dict(depths_done=min(s + 20000, len(T)),
                              min_depth=float(np.nanmin(depths)))), flush=True)
    fc = float(np.trace(H) / 3 + (H.sum() - np.trace(H)) / 4 + g.sum() / 2)
    eps = max(0.0, -float(depths.min()))
    gain = eps * (fc - info['B']) / (1 + eps)
    gap = opt - info['B_safe']
    rec = dict(info, opt=opt, triples=len(T), min_depth=float(depths.min()),
               deepest_triple=T[int(np.argmin(depths))].tolist(),
               count_depth_lt_1e_7=int((depths < -1e-7).sum()),
               count_depth_lt_1e_6=int((depths < -1e-6).sum()),
               f_uniform=fc, gain_term=gain, gap_safe=gap, gain_over_gap=gain / gap,
               gain_plus_margin_over_gap=(gain + info['B'] - info['B_safe']) / gap,
               time_depth=time.time() - depth_started, time_total=time.time() - started)
    Path(str(out) + '.json').write_text(json.dumps(rec, indent=2) + '\n')
    print(json.dumps(rec), flush=True)


if __name__ == '__main__':
    main()
