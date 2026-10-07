"""Exact tests of lem:endpointid, thm:endpointset and cor:facecsp (Section 9.2).

Random quadratics with H_ii <= 0 on mixed boxes (path decomposition), small
integer coefficients so that ties occur. Checks:
  * M_{t0} = OPT (brute force over a fine rational sample of X and all integer points),
  * identity (eq:endpointid) at random rational points of the continuous hull,
  * characterization of thm:endpointset against brute force on a sample grid,
  * admissible patterns: (ii) S = union of faces, counts |S| when finite,
    uniqueness test.
"""
from fractions import Fraction as Fr
import itertools, random

random.seed(7)
ok = True

def run(n, cont, lo, hi, H, bvec):
    # F = 1/2 x^T H x + b^T x ; path bags {i,i+1}; factors: pair terms on bag i,
    # unary terms on the home bag (first bag containing i)
    N = n - 1
    bags = [(i, i + 1) for i in range(N)]
    def F(x):
        return sum(Fr(1, 2) * H[i][k] * x[i] * x[k] for i in range(n) for k in range(n)) + sum(bvec[i] * x[i] for i in range(n))
    def q(t, v):  # v: dict index->value for bag t
        i, k = bags[t]
        val = H[i][k] * v[i] * v[k]
        for idx in (i, k):
            home = 0 if idx == 0 else idx - 1
            if home == t:
                val += Fr(1, 2) * H[idx][idx] * v[idx] ** 2 + bvec[idx] * v[idx]
        return val
    E = [(lo[i], hi[i]) for i in range(n)]
    # root at bag 0; parent of bag t is t-1; B_t^up = {t} (shared var) for t>=1
    # post-order: t = N-1 ... 0
    Mt = {}
    r = {}
    for t in reversed(range(N)):
        i, k = bags[t]
        up = [i] if t > 0 else []
        free = [k] if t > 0 else [i, k]
        table = {}
        for vals in itertools.product(*[E[a] for a in (i, k)]):
            v = {i: vals[0], k: vals[1]}
            br = q(t, v)
            if t + 1 < N:
                br += Mt[t + 1][(v[k],)]
            table[vals] = br
        M = {}
        for vals, br in table.items():
            key = tuple(vals[0:1]) if t > 0 else ()
            M[key] = min(M.get(key, br), br)
        Mt[t] = M
        r[t] = {vals: br - M[tuple(vals[0:1]) if t > 0 else ()] for vals, br in table.items()}
    M0 = Mt[0][()]
    # brute-force OPT on a sample: continuous coords sampled at 1/8 steps, integers all
    def dom(i, step):
        if i in cont:
            return [lo[i] + (hi[i] - lo[i]) * Fr(k, step) for k in range(step + 1)]
        return list(range(lo[i], hi[i] + 1))
    sample = list(itertools.product(*[dom(i, 6) for i in range(n)]))
    vals = [F(x) for x in sample]
    opt_s = min(vals)
    res = True
    if opt_s != M0:
        print("FAIL OPT", opt_s, M0); res = False
    # identity at random points of hull
    def rhs(x):
        tot = Fr(0)
        for t in range(N):
            i, k = bags[t]
            for vals_, rv in r[t].items():
                pi = Fr(1)
                for a, va in zip((i, k), vals_):
                    e = (hi[a] - x[a]) if va == lo[a] else (x[a] - lo[a])
                    pi *= e / (hi[a] - lo[a])
                tot += rv * pi
        tot += Fr(1, 2) * sum(-H[i][i] * (x[i] - lo[i]) * (hi[i] - x[i]) for i in range(n))
        return tot
    for _ in range(20):
        x = [lo[i] + (hi[i] - lo[i]) * Fr(random.randint(0, 97), 97) for i in range(n)]
        if F(x) - M0 != rhs(x):
            print("FAIL identity"); res = False; break
    # characterization vs brute force on sample
    def char(x):
        for i in range(n):
            if H[i][i] < 0 and x[i] not in (lo[i], hi[i]):
                return False
        for t in range(N):
            i, k = bags[t]
            for vals_, rv in r[t].items():
                if rv > 0:
                    prod = Fr(1)
                    for a, va in zip((i, k), vals_):
                        prod *= (hi[a] - x[a]) if va == lo[a] else (x[a] - lo[a])
                    if prod != 0:
                        return False
        return True
    for x, v in zip(sample, vals):
        if (v == M0) != char(x):
            print("FAIL characterization at", x); res = False; break
    # patterns
    Sigma = []
    for i in range(n):
        s = ['L', 'U']
        interior = (i in cont) or (hi[i] - lo[i] >= 2)
        if H[i][i] == 0 and interior:
            s.append('*')
        Sigma.append(s)
    def cube_ok(t, chi):
        i, k = bags[t]
        opts = []
        for a in (i, k):
            c = chi[a]
            opts.append([lo[a]] if c == 'L' else [hi[a]] if c == 'U' else [lo[a], hi[a]])
        return all(r[t][v] == 0 for v in itertools.product(*opts))
    adm = [chi for chi in itertools.product(*Sigma) if all(cube_ok(t, chi) for t in range(N))]
    # union of faces vs brute-force optimal sample points
    def in_face(x, chi):
        return all((c == 'L' and x[i] == lo[i]) or (c == 'U' and x[i] == hi[i]) or c == '*' for i, c in enumerate(chi))
    for x, v in zip(sample, vals):
        if (v == M0) != any(in_face(x, chi) for chi in adm):
            print("FAIL union of faces at", x); res = False; break
    finite = all(not (c == '*' and i in cont) for chi in adm for i, c in enumerate(chi))
    if finite:
        count = sum(eval('*'.join(['1'] + [str(hi[i] - lo[i] - 1) for i, c in enumerate(chi) if c == '*'])) for chi in adm)
        # brute-force count over all points with continuous coords only at endpoints (finite S => S has no interior cont coords)
        allpts = list(itertools.product(*[([lo[i], hi[i]] if i in cont else list(range(lo[i], hi[i] + 1))) for i in range(n)]))
        bf = sum(1 for x in allpts if F(x) == M0)
        if bf != count:
            print("FAIL count", bf, count); res = False
    return res, len(adm), finite

stats = [0, 0, 0]
for trial in range(300):
    n = random.choice([2, 3, 4])
    cont = set(i for i in range(n) if random.random() < 0.5)
    lo, hi = [], []
    for i in range(n):
        if i in cont:
            a = Fr(random.randint(-2, 1)); lo.append(a); hi.append(a + random.choice([1, 2, Fr(3, 2)]))
        else:
            a = random.randint(-2, 1); lo.append(a); hi.append(a + random.choice([1, 2, 3]))
    H = [[Fr(0)] * n for _ in range(n)]
    for i in range(n):
        H[i][i] = -Fr(random.choice([0, 0, 0, 1, 2]))
        if i + 1 < n:
            v = Fr(random.choice([-1, 0, 1, 2]))
            H[i][i + 1] = H[i + 1][i] = v
    bvec = [Fr(random.choice([-2, -1, 0, 1, 2])) for _ in range(n)]
    res, nadm, finite = run(n, cont, lo, hi, H, bvec)
    ok = ok and res
    stats[0] += 1; stats[1] += nadm > 1; stats[2] += not finite
print("instances %d, with several admissible patterns %d, with continuum S %d" % tuple(stats))
print("ALL PASS" if ok else "SOME FAIL")
