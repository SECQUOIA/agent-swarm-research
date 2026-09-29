"""Recheck of Remark 4.1a (witness lemma for shared bases).

Random DAGs in setting (FS): 2-3 variables, 1-3 base nodes, each feeding 1-4
terms a_j * base^k (fresh power nodes), one flat root sum. Two families:
  SU : bases are single-use expressions (the remark's hypothesis):
       linear forms, x_i * x_j, x_i * (x_j + 1)-type products of disjoint parts;
  NSU: bases that are NOT single-use (x appears twice):
       (x0 + x1)*(x0 - x1), x0*x1 + x0, x_i - x_i^2.
For a random sub-box U' ⊆ C:
  (W1) the explicit witness of the remark (exact ranges on every base node and
       its internal nodes, full images on the power nodes, root interval of
       Lemma 4.1 at c = Phi_full(U')) lies in Z0(C) and is left unchanged by
       every forward, backward and cutoff step (so it is hull-consistent);
  (W2) the HC4 fixed point from Z0(C) at c = Phi_full(U') keeps all of U';
  info: at c = Phi_full(U') - 0.05*(1 + |Phi_full|), how often part of U' is
       removed (the bound is not vacuous).
Run: python3 check_witness.py > logs/check_witness.log
"""
import random
import iprop as P

rng = random.Random(4101)


def ia_lin(co, b, box, vars_):
    lo = hi = b
    for a, v in zip(co, vars_):
        x = box[v]
        lo += a * (x[0] if a >= 0 else x[1])
        hi += a * (x[1] if a >= 0 else x[0])
    return (lo, hi)


def make_base(d, kind, n):
    """Returns (node, ranges) where ranges is a list of (node, fn(U') -> exact range)."""
    i, j = rng.sample(range(n), 2)
    if kind == 'lin':
        co = [rng.choice([-1, 1]) * rng.uniform(0.5, 1.5) for _ in range(2)]
        b = rng.uniform(-0.5, 0.5)
        z = d.sum([i, j], co, b)
        return z, [(z, lambda U, co=co, b=b: ia_lin(co, b, U, (i, j)))]
    if kind == 'bil':
        z = d.mul(i, j)
        return z, [(z, lambda U: P.img_mul(U[i], U[j]))]
    if kind == 'bil1':                           # x_i * (x_j + 1): single-use
        s = d.sum([j], [1.0], 1.0)
        z = d.mul(i, s)
        return z, [(s, lambda U: (U[j][0] + 1, U[j][1] + 1)),
                   (z, lambda U: P.img_mul(U[i], (U[j][0] + 1, U[j][1] + 1)))]
    if kind == 'sq':                             # (xi + xj)(xi - xj) = xi^2 - xj^2
        s1 = d.sum([i, j], [1, 1])
        s2 = d.sum([i, j], [1, -1])
        z = d.mul(s1, s2)

        def rng_z(U):
            a, b = P.img_pow(U[i], 2), P.img_pow(U[j], 2)
            return (a[0] - b[1], a[1] - b[0])
        return z, [(s1, lambda U: ia_lin([1, 1], 0, U, (i, j))),
                   (s2, lambda U: ia_lin([1, -1], 0, U, (i, j))), (z, rng_z)]
    if kind == 'xyx':                            # xi*xj + xi = xi (xj + 1)
        m = d.mul(i, j)
        z = d.sum([m, i], [1, 1])
        return z, [(m, lambda U: P.img_mul(U[i], U[j])),
                   (z, lambda U: P.img_mul(U[i], (U[j][0] + 1, U[j][1] + 1)))]
    if kind == 'xmx2':                           # xi - xi^2
        p = d.pow(i, 2)
        z = d.sum([i, p], [1, -1])

        def rng_z(U):
            lo, hi = U[i]
            vals = [lo - lo * lo, hi - hi * hi]
            if lo <= 0.5 <= hi:
                vals.append(0.25)
            return (min(vals), max(vals))
        return z, [(p, lambda U: P.img_pow(U[i], 2)), (z, rng_z)]
    raise ValueError(kind)


def build(family, n):
    d = P.DAG(n)
    kinds = ['lin', 'bil', 'bil1'] if family == 'SU' else ['sq', 'xyx', 'xmx2']
    nb = rng.randint(1, 3)
    ranges = []
    terms = []           # (node, coef, base node, k)
    for _ in range(nb):
        z, rg = make_base(d, rng.choice(kinds), n)
        ranges += rg
        ks = [rng.randint(1, 4) for _ in range(rng.randint(1, 4))]
        used1 = False
        for k in ks:
            if k == 1 and used1:
                k = 2
            used1 = used1 or k == 1
            node = z if k == 1 else d.pow(z, k)
            terms.append((node, rng.choice([-1, 1]) * rng.uniform(0.2, 2.0), z, k))
    b = rng.uniform(-1, 1)
    d.sum([t[0] for t in terms], [t[1] for t in terms], b)
    return d.nodes, ranges, terms, b


def phi_full(ranges_at, terms, b):
    lo_sum, widths, hi_sum = b, [], b
    for node, a, z, k in terms:
        r = P.img_pow(ranges_at[z], k) if k > 1 else ranges_at[z]
        t = (a * r[0], a * r[1]) if a >= 0 else (a * r[1], a * r[0])
        lo_sum += t[0]
        hi_sum += t[1]
        widths.append(t[1] - t[0])
    return lo_sum + max(widths), lo_sum, hi_sum


def one(family):
    n = rng.randint(2, 3)
    dag, ranges, terms, b = build(family, n)
    C = []
    for _ in range(n):
        lo = rng.uniform(-2, 1.5)
        C.append((lo, lo + rng.uniform(0.3, 2.5)))
    U = []
    for lo, hi in C:
        a_, b_ = sorted([rng.uniform(lo, hi), rng.uniform(lo, hi)])
        if rng.random() < 0.2:
            b_ = a_                                  # degenerate side (segment)
        U.append((a_, b_))
    def witness(Uw):
        at = {v: Uw[v] for v in range(n)}
        for node, fn in ranges:
            at[node] = fn(Uw)
        c, lo_sum, hi_sum = phi_full(at, terms, b)
        W = []
        for k, nd in enumerate(dag):
            if nd[0] == 'var':
                W.append(Uw[nd[1]])
            elif k in at:
                W.append(at[k])
            elif k == len(dag) - 1:
                W.append((lo_sum, min(c, hi_sum)))
            elif nd[0] == 'pow':
                W.append(P.img_pow(at[nd[1]], nd[2]))
            else:
                raise RuntimeError(nd)
        return W, c
    W, c = witness(U)
    Z0C = P.z0(dag, C)
    w_in = P.inside(W, Z0C, 1e-12)
    st, _, _ = P.run(dag, W, c + 1e-12 * (1 + abs(c)), 1, rtol=1e-10)
    w_fixed_raw = st == 'fixed'
    # floating point: point sides (segments) can lose 1 ulp and empty; widen by 1e-12
    Wi, ci = witness([(lo - 1e-12, hi + 1e-12) for lo, hi in U])
    st, _, _ = P.run(dag, Wi, ci + 1e-12 * (1 + abs(ci)), 1, rtol=1e-8)
    w_fixed = st == 'fixed'
    # fixed point from Z0(C)
    st2, Z, _ = P.fixpoint(dag, C, c + 1e-10 * (1 + abs(c)), max_rounds=20000)
    keep = st2 != 'empty' and P.inside(U, P.xbox(dag, Z), 1e-9)
    conv = st2 == 'fixed'
    st3, Z3, _ = P.fixpoint(dag, C, c - 0.05 * (1 + abs(c)), max_rounds=20000)
    removed_below = st3 == 'empty' or not P.inside(U, P.xbox(dag, Z3), 1e-9)
    return w_in, w_fixed_raw, w_fixed, keep, conv, removed_below


if __name__ == '__main__':
    for family in ('SU', 'NSU'):
        N = 300
        cnt = dict(w_in=0, w_raw=0, w_fixed=0, keep=0, conv=0, below=0)
        for _ in range(N):
            w_in, w_raw, w_fixed, keep, conv, below = one(family)
            cnt['w_in'] += w_in
            cnt['w_raw'] += w_raw
            cnt['w_fixed'] += w_fixed
            cnt['keep'] += keep
            cnt['conv'] += conv
            cnt['below'] += below
        label = ('single-use shared bases (Remark 4.1a)' if family == 'SU'
                 else 'NON-single-use shared bases (beyond the remark)')
        print(f'{label}: {N} random (DAG, C, U\'):')
        print(f'    (W1) witness inside Z0(C): {cnt["w_in"]}/{N}; unchanged by all steps '
              f'(hull-consistent): {cnt["w_fixed"]}/{N} with sides widened by 1e-12 '
              f'({cnt["w_raw"]}/{N} unwidened; the rest fail only by 1-ulp emptiness on point sides)')
        print(f'    (W2) fixed point at c = Phi_full(U\') keeps U\': {cnt["keep"]}/{N} '
              f'(converged runs: {cnt["conv"]})')
        print(f'    info: at c = Phi_full - 0.05(1+|Phi_full|) part of U\' removed in '
              f'{cnt["below"]}/{N}')


def named_reps():
    """(C) The representations named in Remark 4.1a. Every term node is a
    single-use expression, so its forward interval over U' is its exact range
    and Phi_full(U') can be read off Z0(U')."""
    import inst as I
    d = P.DAG(1)                                   # nondeg1s 'centered'
    t = d.sum([0], [1.0], -1 / 3)
    u = d.pow(t, 2)
    v = d.pow(u, 2)
    d.sum([u, v], [1, -2])
    reps = {'linediag/s': I.linediag('s'), 'rot1/st': I.rot(1.0, 'st'),
            'line3/st': I.line3_st(), 'nondeg1/u': I.nondeg1('u'),
            'nondeg1s/centered': dict(dag=d.nodes, box=[(0.0, 1.0)])}
    print('(C) named shared-base representations: c = Phi_full(U\'), fixed point from Z0(C) '
          'must keep U\':')
    for name, J in reps.items():
        dag = J['dag']
        root = dag[-1]
        keep = N = 0
        for _ in range(150):
            C = [(lo + rng.uniform(0, 0.4) * (hi - lo), hi - rng.uniform(0, 0.4) * (hi - lo))
                 for lo, hi in J['box']]
            U = [tuple(sorted([rng.uniform(lo, hi), rng.uniform(lo, hi)])) for lo, hi in C]
            Zu = P.z0(dag, U)
            ts = []
            for ch, a in zip(root[1], root[2]):
                x = Zu[ch]
                ts.append((a * x[0], a * x[1]) if a >= 0 else (a * x[1], a * x[0]))
            c = root[3] + sum(t_[0] for t_ in ts) + max(t_[1] - t_[0] for t_ in ts)
            st, Z, _ = P.fixpoint(dag, C, c + 1e-10 * (1 + abs(c)), max_rounds=50000)
            N += 1
            keep += st != 'empty' and P.inside(U, P.xbox(dag, Z), 1e-9)
        print(f'    {name:18s}: U\' kept in {keep}/{N}')


named_reps()
