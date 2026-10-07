"""Dossier check (camshape): optimum enclosure that is robust to perturbing the constants.

Monotonicity (proved in the dossier): with u = 1/r > 0 the convexity rows u_{j-1} - c u_j + u_{j+1} >= 0
tighten as c grows; r_1 <= ub1 and |d_j| <= alpha tighten as ub1, alpha shrink; -c0 sum r decreases as c0 grows.
Hence for every model whose constants satisfy c >= c-, ub1 <= ub1+, alpha <= alpha+, c0 <= c0+ (c2 <= 4, cE <= 2,
lbn <= 2 unchanged in role), the optimum is >= -c0+ * sum E(c-, ub1+, alpha+)   [Theorem 1 at the corner],
and for every model with c <= c+, ub1 >= ub1-, alpha >= alpha-, c0 >= c0- the corner envelope E(c+, ub1-, alpha-)
is feasible (checked exactly here), so the optimum is <= -c0- * sum E(c+, ub1-, alpha-).
Usage: python3 robust.py file:eta ...   (file = .osil or .gms; eta = absolute perturbation, e.g. 1e-14)
"""
import sys
import json
from fractions import Fraction as Fr

sys.set_int_max_str_digits(0)
from check_exact import read_osil, structure, certificate, dec, dec_up
from check_gms import parse_gms, to_model, feasible_envelope


def consts(path):
    if path.endswith('.osil'):
        n = int(''.join(ch for ch in path if ch.isdigit()))
        M = read_osil(path)
        K = structure(M, n)
        K['cE'] = K['c']
        K['n'] = n
        return K
    G = parse_gms(path)
    return to_model(G)


def main(path, eta):
    K = consts(path)
    n = K['n']
    lo = dict(c=K['c'] - eta, ub1=K['ub1'] + eta, alpha=K['alpha'] + eta)
    hi = dict(c=K['c'] + eta, ub1=K['ub1'] - eta, alpha=K['alpha'] - eta)
    Cl = certificate(lo, n)
    assert all(u >= 0 for u in Cl['U'][:n])
    vlow = -(K['c0'] + eta) * sum(Cl['E'][1:])
    Ch = certificate(hi, n)
    Kh = dict(K); Kh.update(hi)
    rowmax, bv, _ = feasible_envelope(Kh, Ch['E'])
    assert Ch['E'][n] == 2 and Ch['E'][n - 1] == 2
    assert rowmax <= 0 and bv <= 0 and K['c2'] <= 4 and K['cE'] <= 2 and K['lbn'] <= 2
    vup = -(K['c0'] - eta) * sum(Ch['E'][1:])
    v0 = -K['c0'] * sum(certificate(K, n)['E'][1:])
    return dict(file=path, n=n, eta=str(eta), v_floor16=dec(v0, 16), low_floor16=dec(vlow, 16), up_ceil16=dec_up(vup, 16),
                width=float(vup - vlow), below=float(v0 - vlow), above=float(vup - v0))


if __name__ == '__main__':
    out = []
    for a in sys.argv[1:]:
        p, e = a.split(':')
        r = main(p, Fr(e))
        print(json.dumps(r), flush=True)
        out.append(r)
    json.dump(out, open('robust.json', 'w'), indent=1)
