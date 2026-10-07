"""R1-math: checks of Theorem 5.4 counts, Ben-Or family, Remark 5.5 example."""
from fractions import Fraction as Fr
import random, itertools, math

random.seed(7)

def lines_of_leaf(leaf):
    """Return (lower_lines, upper_lines) as lists of (const, slope): x >= c + s*y or x <= c + s*y."""
    lo = [(Fr(leaf['l']), Fr(0))]; up = [(Fr(leaf['u']), Fr(0))]
    for (al, ga, de) in leaf['rows']:   # al*x + ga*y <= de
        c, s = Fr(de, 1)/al, -Fr(ga, 1)/al
        (up if al > 0 else lo).append((c, s))
    return lo, up

def ev(line, y): return line[0] + line[1]*y

def phi_and_rule(leaf, y):
    lo, up = lines_of_leaf(leaf)
    L = max(lo, key=lambda ln: (ev(ln, y), ln[1]))   # tie-break by slope (right-side piece)
    U = min(up, key=lambda ln: (ev(ln, y), -ln[1]))
    Lv, Uv = ev(L, y), ev(U, y)
    d, e, f = Fr(leaf['d']), Fr(leaf['e']), Fr(leaf['f'])
    psi = lambda t: d*t*t + (e*y+f)*t
    if d > 0:
        v = -(e*y+f)/(2*d)
        if v <= Lv: return psi(Lv), ('L', L)
        if v >= Uv: return psi(Uv), ('U', U)
        return psi(v), ('v',)
    else:
        if psi(Uv) < psi(Lv): return psi(Uv), ('U', U)
        return psi(Lv), ('L', L)

def all_lines(leaf):
    lo, up = lines_of_leaf(leaf)
    d, e, f = Fr(leaf['d']), Fr(leaf['e']), Fr(leaf['f'])
    out = list(lo) + list(up)
    if d > 0:
        out.append((-f/(2*d), -e/(2*d)))
    else:
        for L in lo:
            for U in up:
                # d(U+L) + e y + f
                out.append((d*(U[0]+L[0]) + f, d*(U[1]+L[1]) + e))
    return out

def candidate_points(leaf, ylo, yhi):
    pts = set()
    lns = all_lines(leaf)
    lo, up = lines_of_leaf(leaf)
    d = Fr(leaf['d'])
    for a, b in itertools.combinations(lns, 2):
        if a[1] != b[1]:
            y = (b[0]-a[0])/(a[1]-b[1])
            if ylo < y < yhi: pts.add(y)
    # zeros of endpoint factor lines themselves (d<=0 case: factor = 0)
    if d <= 0:
        for ln in lns[len(lo)+len(up):]:
            if ln[1] != 0:
                y = -ln[0]/ln[1]
                if ylo < y < yhi: pts.add(y)
    return sorted(pts)

def interval_I(leaves, ylo, yhi):
    lo_, hi_ = Fr(ylo), Fr(yhi)
    # J_i: L_i <= U_i ; compute by candidate points (exact): feasible set is interval
    pts = {lo_, hi_}
    for leaf in leaves:
        lo, up = lines_of_leaf(leaf)
        for a in lo:
            for b in up:
                if a[1] != b[1]:
                    y = (b[0]-a[0])/(a[1]-b[1])
                    if lo_ < y < hi_: pts.add(y)
    pts = sorted(pts)
    def feas(y):
        for leaf in leaves:
            lo, up = lines_of_leaf(leaf)
            if max(ev(a, y) for a in lo) > min(ev(b, y) for b in up): return False
        return True
    fe = [p for p in pts if feas(p)]
    if not fe: return None
    return fe[0], fe[-1]

def rule_key(leaf, y):
    _, r = phi_and_rule(leaf, y)
    if r[0] == 'v': return ('v',)
    # rule = which affine function of y is used: identify by the line (c, s)
    return r

def leaf_breaks(leaf, I):
    a, b = I
    pts = [a] + candidate_points(leaf, a, b) + [b]
    mids = [(pts[i]+pts[i+1])/2 for i in range(len(pts)-1)]
    rules = [rule_key(leaf, m) for m in mids]
    # merge equal consecutive rules; count changes
    br = sum(1 for i in range(1, len(rules)) if rules[i] != rules[i-1])
    return br

def s_of(leaf): return len(leaf['rows']) + 2

def V(leaves, center, y):
    a0, a1, a2 = center
    return a0 + a1*y + a2*y*y + sum(phi_and_rule(l, y)[0] for l in leaves)

def exact_min(leaves, center, I):
    a, b = I
    pts = set([a, b])
    for l in leaves: pts.update(candidate_points(l, a, b))
    pts = sorted(pts)
    best = None
    for i in range(len(pts)-1):
        lo_, hi_ = pts[i], pts[i+1]
        # fit quadratic from 3 points (exact since quadratic on piece)
        ys = [lo_, (lo_+hi_)/2, hi_]
        vs = [V(leaves, center, yy) for yy in ys]
        # Lagrange -> coefficients
        y0,y1,y2 = ys; v0,v1,v2 = vs
        c2 = ((v2-v1)/(y2-y1) - (v1-v0)/(y1-y0))/(y2-y0)
        c1 = (v1-v0)/(y1-y0) - c2*(y1+y0)
        cands = [lo_, hi_]
        if c2 > 0:
            st = -c1/(2*c2)
            if lo_ < st < hi_: cands.append(st)
        for yy in cands:
            val = V(leaves, center, yy)
            if best is None or val < best[0]: best = (val, yy)
    return best

def rand_leaf(nrows):
    l = random.randint(-3, 0); u = l + random.randint(1, 6)
    rows = []
    for _ in range(nrows):
        al = random.choice([-3,-2,-1,1,2,3]); ga = random.randint(-4, 4); de = random.randint(-6, 6)
        rows.append((al, ga, de))
    return dict(l=l, u=u, rows=rows, d=random.randint(-3, 3), e=random.randint(-4,4), f=random.randint(-4,4))

viol = 0; checked = 0; maxratio = 0
for trial in range(300):
    k = random.randint(1, 4)
    leaves = [rand_leaf(random.randint(0, 3)) for _ in range(k)]
    center = (Fr(random.randint(-3,3)), Fr(random.randint(-3,3)), Fr(random.randint(-3,3)))
    I = interval_I(leaves, -4, 4)
    if I is None or I[0] == I[1]: continue
    checked += 1
    m = sum(len(l['rows']) for l in leaves)
    tot = 0
    for l in leaves:
        br = leaf_breaks(l, I)
        bound = (s_of(l)+2) if l['d'] > 0 else (2*s_of(l)-3)
        if br > bound: viol += 1; print("per-leaf bound violated", l, br, bound)
        tot += br
    if tot + 1 > 2*m + 4*k + 1: viol += 1; print("total bound violated")
    best = exact_min(leaves, center, I)
    # brute-force grid
    N = 400
    grid = [I[0] + (I[1]-I[0])*Fr(i, N) for i in range(N+1)]
    gmin = min(V(leaves, center, yy) for yy in grid)
    if best[0] > gmin: viol += 1; print("exact min above grid min!", best, gmin)
print("star instances checked:", checked, " violations:", viol)

# Search for a concave leaf attaining 2s-3 breakpoints
found = {}
for trial in range(40000):
    nrows = random.randint(1, 3)
    l = rand_leaf(nrows); l['d'] = random.choice([-1,-2,-3])
    I = interval_I([l], -6, 6)
    if I is None or I[0] == I[1]: continue
    br = leaf_breaks(l, I)
    s = s_of(l)
    # effective s: count lines that actually appear on I is irrelevant; record max
    if br >= 2*s-3:
        found.setdefault(s, (br, l))
print("concave leaves attaining 2s-3:", {s: v[0] for s, v in found.items()})
# Search convex leaf maximum breakpoints for box leaf (s=2)
mx = 0
for trial in range(5000):
    l = rand_leaf(0); l['d'] = random.randint(1, 3)
    I = (Fr(-6), Fr(6))
    mx = max(mx, leaf_breaks(l, I))
print("max breakpoints for convex box leaf (bound s+2=4):", mx)

# Ben-Or family identity
def tent_identity(tv):
    return min(0, tv+1) + min(0, 1-tv) + 2*max(0, tv) - tv - 1 + max(0, 1-abs(tv))
assert all(tent_identity(Fr(i, 7)) == 0 for i in range(-50, 51))
r = 4
z = [Fr(random.randint(1, 79), 10) for _ in range(r)]
leaves = []
for zj in z:
    leaves.append(dict(l=0, u=1, rows=[], d=0, e=1, f=1 - zj))         # (y - z + 1) x
    leaves.append(dict(l=0, u=1, rows=[], d=0, e=-1, f=zj + 1))        # (z + 1 - y) x
    leaves.append(dict(l=0, u=2*r+1, rows=[(-1, 1, zj)], d=0, e=0, f=2))  # x >= y - z  <=>  -x + y <= z
center = (sum(z) - r, Fr(-r), Fr(0))
ok = all(V(leaves, center, Fr(i, 13)) == -sum(max(0, 1 - abs(Fr(i, 13) - zj)) for zj in z) for i in range(0, 2*r*13+1))
print("Ben-Or star V equals tent sum:", ok)

# Remark 5.5 / App depth-two example
def f3(x1, x2, x3): return (x2 - Fr(1,8))*x1 + x2*x2 - x2 + x2*x3 + x3*x3 - x3
def cond(t):
    # min over x1 in {0,1} (linear) and x2 in [0,1]
    best = None
    for x1 in (0, 1):
        # quadratic in x2: x2^2 + (x1 + t - 1) x2 - x1/8
        b = x1 + t - 1
        cands = [Fr(0), Fr(1)]
        st = -b/2
        if 0 < st < 1: cands.append(st)
        for x2 in cands:
            v = x2*x2 + b*x2 - Fr(x1, 8)
            best = v if best is None or v < best else best
    return best
okc = all(cond(Fr(i, 97)) == min(Fr(-1,8), -Fr(1,4)*(1-Fr(i,97))**2) for i in range(98))
print("conditional value formula holds on grid:", okc)
print("switch point 1-sqrt2/2 =", 1-math.sqrt(2)/2, " residual 2t^2-4t+1:", 2*(1-math.sqrt(2)/2)**2 - 4*(1-math.sqrt(2)/2) + 1)
gm = min(cond(Fr(i, 1000)) + Fr(i,1000)**2 - Fr(i,1000) for i in range(1001))
print("min f over grid:", gm, " f(1,0,1/2) =", f3(1, 0, Fr(1,2)))
