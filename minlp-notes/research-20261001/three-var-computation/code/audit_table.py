"""Markdown tables of the triple-level audits.

spar: logs/spar_audit/*.json (spar_audit.py) and logs/audit/spar*.json (triple_audit.py).
sparse: logs/sparse_audit/*.json (sparse_audit.py) with the best known feasible value U
(minimum of ub_local.py runs in logs/ub and logs/ub2 and of Gurobi incumbents in
logs/gurobi and logs/gurobi2).  gap = U - B_safe; 'max gain' is the Lemma 3 bound on what
any triple-level constraints can add at the B solution.
Usage: python audit_table.py spar|sparse"""
import glob
import json
import os
import re
import sys

import numpy as np

from relax import all_triples, separate_triangles


def best_ub(tag):
    vals = []
    for d in ('ub', 'ub2'):
        p = '../logs/%s/%s.json' % (d, tag)
        if os.path.exists(p):
            try:
                vals.append(json.loads(open(p).read().strip().splitlines()[-1])['ub'])
            except (ValueError, IndexError, KeyError):
                pass
    for d in ('gurobi', 'gurobi2'):
        p = '../logs/%s/%s.log' % (d, tag)
        if os.path.exists(p):
            m = re.findall(r'Best objective ([-+0-9.e]+), best bound ([-+0-9.e]+)', open(p).read())
            if m:
                vals.append(float(m[-1][0]))
    return min(vals) if vals else None


def spar():
    recs = {}
    for f in glob.glob('../logs/audit/spar*.json') + glob.glob('../logs/spar_audit/*.json'):
        if f.endswith('.tri.json'):
            continue
        r = json.load(open(f))
        recs[r['name']] = r
    print('| instance | n | B status | gap (opt - B safe) | rel. gap | min depth | triples with depth < -1e-6 | family min | gain term (Lemma 3) | gain term / gap | primal infeasibility | triangle violation |')
    print('|---|---|---|---|---|---|---|---|---|---|---|---|')
    for name in sorted(recs, key=lambda k: -recs[k].get('relgap_safe', 0)):
        r = recs[name]
        opt = r.get('opt_min')
        if opt is None:
            for line in open('../sources/BoxQP_instances-master/README.txt'):
                t = line.split()
                if len(t) == 2 and t[0] == name:
                    opt = -float(t[1])
        gap = opt - r['B_safe']
        paths = glob.glob('../logs/audit/' + name + '.json.base.npz') + glob.glob('../logs/spar_audit/' + name + '.json.base.npz')
        if paths:
            with np.load(paths[-1]) as point:
                _, maximum = separate_triangles(point['x'], point['Y'], tol=0.0, cap=1,
                                                triples=all_triples(r['n']))
            triangle = '%.1e' % maximum
        elif r.get('max_triangle_violation') == 0:
            triangle = '< 1e-7'
        else:
            triangle = ('%.1e' % r['max_triangle_violation']) if r.get('max_triangle_violation') is not None else 'not recorded'
        ratio = 'solver accuracy' if r['B'] >= opt else '%.1e' % (r['max_triple_level_improvement'] / gap)
        print('| %s | %d | %s | %.4f | %.2e | %.1e | %d | %.1e | %.1e | %s | %.1e | %s |' % (
            name, r['n'], r['status'], gap, gap / abs(opt), r['min_depth'], r['count_depth_lt_1e-6'],
            r['family_stqp_min'], r['max_triple_level_improvement'], ratio, r['pinf'], triangle))


def sparse():
    print('| instance | n | clique triples | B safe | U (best feasible) | gap U - B | min depth | triples with depth < -1e-6 | family min | max gain (Lemma 3) | B time (s) |')
    print('|---|---|---|---|---|---|---|---|---|---|---|')
    fs = [f for f in glob.glob('../logs/sparse_audit/*.json')]

    def key(f):
        t = os.path.basename(f)[:-5]
        fam = t.split('_')[0]
        return (fam, json.load(open(f))['n'], t)
    for f in sorted(fs, key=key):
        t = os.path.basename(f)[:-5]
        r = json.load(open(f))
        U = best_ub(t)
        gap = (U - r['B_safe']) if U is not None else float('nan')
        print('| %s | %d | %d | %.4f | %s | %s | %.1e | %d | %.1e | %.1e | %.1f |' % (
            t, r['n'], r['triples'], r['B_safe'], ('%.4f' % U) if U is not None else 'n/a',
            ('%.4f' % gap) if U is not None else 'n/a', r['min_depth'], r['count_depth_lt_1e-6'],
            r['family_stqp_min'], r['max_triple_level_improvement'], r['time_base']))


if __name__ == '__main__':
    {'spar': spar, 'sparse': sparse}[sys.argv[1]]()
