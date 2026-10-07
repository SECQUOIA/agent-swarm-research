"""Dossier check (camshape): exact evaluation of the QPLIB reference points in their own (rounded) models,
against the exact optimum of each copy (envelope value from check_gms). Exact Fractions throughout."""
import sys
import json
from fractions import Fraction as Fr

sys.set_int_max_str_digits(0)
from check_gms import parse_gms, to_model
from check_exact import certificate, dec


def evalp(p, x):
    s = Fr(0)
    for mono, v in p.items():
        t = v
        for var in mono:
            t *= x[var]
        s += t
    return s


def main(gms, sol):
    G = parse_gms(gms)
    K = to_model(G)
    n = K['n']
    C = certificate(dict(c=K['c'], ub1=K['ub1'], alpha=K['alpha']), n)
    opt = -K['c0'] * sum(C['E'][1:])
    x = {v: Fr(0) for v in G['variables']}
    seen = set()
    for line in open(sol):
        a = line.split()
        if len(a) == 2:
            x[a[0]] = Fr(a[1]); seen.add(a[0])
    missing = [v for v in G['variables'] if v not in seen]
    worst, wname = Fr(0), None
    for k, (p, s) in G['eqs'].items():
        if any('objvar' in m for m in p):
            continue
        v = evalp(p, x)
        viol = max(v, Fr(0)) if s == 'L' else (abs(v) if s == 'E' else max(-v, Fr(0)))
        if viol > worst:
            worst, wname = viol, k
    bworst = Fr(0)
    for v in G['variables']:
        if v in G['lo']:
            bworst = max(bworst, G['lo'][v] - x[v])
        if v in G['up']:
            bworst = max(bworst, x[v] - G['up'][v])
    # objective recomputed from r (objective-defining row assumed exact)
    objrow = [k for k, (p, s) in G['eqs'].items() if any('objvar' in m for m in p)][0]
    p, _ = G['eqs'][objrow]
    co = p[('objvar',)]
    obj = -sum(v * x[m[0]] for m, v in p.items() if m != ('objvar',)) / co
    return dict(file=gms, n=n, copy_opt_floor16=dec(opt, 16), sol_objvar=float(x['objvar']), obj_from_r=float(obj),
                obj_minus_copy_opt=float(obj - opt), max_row_viol=float(worst), worst_row=wname,
                max_bound_viol=float(bworst), missing=len(missing))


if __name__ == '__main__':
    out = []
    for a in sys.argv[1:]:
        g, s = a.split(':')
        r = main(g, s)
        print(json.dumps(r), flush=True)
        out.append(r)
    json.dump(out, open('eval_qplib_points.json', 'w'), indent=1)
