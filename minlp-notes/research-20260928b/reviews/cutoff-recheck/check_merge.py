"""Recheck of Lemma 1.2(d) and the revised proof of Lemma 2.1(b).

(A) Restart enlargement (the first review's point), and Z* ⊆ Z0(Pi_x Z*).
(B) Lemma 1.2(d) on random boxes/cutoffs: every converged fixed point Z
    satisfies Z ⊆ Z0(Pi_x Z). Control: end-of-round boxes of unfinished runs
    need not (so the lemma has content).
(C) Tree simulation. 80 depth-3 trees per instance; each node runs one or two phases; each
    phase is 1-4 runs of 1-5 rounds (HC4 or random partial-step order), with
    - restarts from Z0(B_i), from Z0(B_i) ∩ previous final lifted box, or from
      inherited bounds Y ∩ Z0(B_i);
    - the cutoff (incumbent) nonincreasing in time, often decreasing inside a
      phase;
    - optional R-rel-like shrinks of the x-box between phases and before a
      child's first phase.
    Checks, with c = smallest cutoff of the phase and D = Z*(B_0, c):
      (i)  D ⊆ start box of every run of the phase;
      (ii) every frame piece S of B_0 \\ int B_f has Pi_x Z*(S, c) ⊆ B_f;
      (iii) an emptied phase has D = ∅.
    Negative control: (ii) with the largest cutoff of the phase instead.
(E) Incumbents that may INCREASE (the constrained note's model allows any
    UBD >= f* over time): the phase's smallest cutoff is then not enough for
    inherited starts, but the smallest cutoff along the inheritance chain is.
(D) Interleaved constraint propagation (the model's "and possibly
    propagation of the constraints"): (Π) can fail on a propagation leaf.
Run: python3 check_merge.py > logs/check_merge.log
"""
import random
import iprop as P
import inst as I

rng = random.Random(20260929)
MAXR = 20000


def fixed(dag, box, c):
    return P.fixpoint(dag, box, c, max_rounds=MAXR)


def part_a():
    E = I.endpoint()
    dag = E['dag']
    st, Z, r = P.run(dag, P.z0(dag, [(-1.0, 1.0)]), -0.01, 1000, rtol=1e-15)
    xb = P.xbox(dag, Z)
    Zr = P.z0(dag, xb)
    print('(A) -3x^2 + 2x^2 + 2x^2 on [-1,1], cutoff -0.01:')
    print(f'    run: {st} after {r} rounds, x-box {xb[0]}, square nodes '
          f'{[tuple(round(v, 5) for v in Z[k]) for k in (1, 2, 3)]}')
    print(f'    restart Z0(x-box) gives square nodes {[Zr[k] for k in (1, 2, 3)]}: '
          f'enlarged = {not P.inside(Zr, Z, 0.0)}; Z ⊆ Z0(Pi_x Z) = {P.inside(Z, Zr)}')


def instances():
    return {
        'endpoint': I.endpoint(),
        'linediag/exp': I.linediag('exp'),
        'linediag/s': I.linediag('s'),
        'rot0.1/exp': I.rot(0.1, 'exp'),
        'rot1/st': I.rot(1.0, 'st'),
        'iso2/exp': I.iso2(),
        'nondeg1/mono': I.nondeg1('mono'),
        'nondeg1/u': I.nondeg1('u'),
        'cnd1/exp': I.cnd1(),
    }


def centre(name, box):
    if name.startswith('linediag'):
        t = rng.uniform(-0.8, 1.0)
        return [t + 1, t]
    if name.startswith('rot'):
        return [1.0, 0.0]
    if name.startswith('iso2'):
        return [1.0, 1.0]
    if name.startswith('cnd1'):
        return [1.0]
    return [0.0]


def rand_box(name, box, scale):
    c0 = centre(name, box)
    return [(max(lo, ci - rng.uniform(0.002, scale)), min(hi, ci + rng.uniform(0.002, scale)))
            for (lo, hi), ci in zip(box, c0)]


def part_b(insts):
    ok = bad = unconv = ctrl_fail = ctrl_n = 0
    for name, J in insts.items():
        dag = J['dag']
        for _ in range(40):
            C = rand_box(name, J['box'], 0.5)
            c = rng.uniform(-0.05, 0.3)
            st, Z, _ = fixed(dag, C, c)
            if st == 'fixed':
                if P.inside(Z, P.z0(dag, P.xbox(dag, Z))):
                    ok += 1
                else:
                    bad += 1
            elif st == 'limit':
                unconv += 1
            st2, Z2, _ = P.run(dag, P.z0(dag, C), c, 1)
            if st2 != 'empty':
                ctrl_n += 1
                if not P.inside(Z2, P.z0(dag, P.xbox(dag, Z2))):
                    ctrl_fail += 1
    print(f'(B) Lemma 1.2(d): {ok} converged nonempty fixed points satisfy Z ⊆ Z0(Pi_x Z), '
          f'{bad} do not; {unconv} unconverged skipped.')
    print(f'    control: after ONE round (not hull-consistent) {ctrl_fail} of {ctrl_n} boxes '
          f'violate Z ⊆ Z0(Pi_x Z).')


def frame(B0, Bf):
    n = len(B0)
    out = []
    for i in range(n):
        for side in (0, 1):
            S = []
            for j in range(n):
                if j < i:
                    S.append(Bf[j])
                elif j > i:
                    S.append(B0[j])
                else:
                    S.append((B0[i][0], Bf[i][0]) if side == 0 else (Bf[i][1], B0[i][1]))
            if all(hi - lo > 1e-12 for lo, hi in S):
                out.append(S)
    return out


class Stats:
    def __init__(self):
        self.__dict__.update(phases=0, runs=0, start_ok=0, start_bad=0, start_skip=0,
                             pieces=0, piece_bad=0, piece_skip=0, empties=0, empty_bad=0,
                             ctrl_pieces=0, ctrl_bad=0, inherited=0, multi_cut=0,
                             second_phase=0, depth_max=0)


class Clock:
    """Incumbent: nonincreasing cutoff c = UBD - eps."""
    def __init__(self, c0, floor):
        self.c, self.floor = c0, floor

    def maybe_drop(self, p=0.4):
        if rng.random() < p:
            self.c = max(self.floor, self.c - rng.uniform(0.0, 0.08))
        return self.c


def phase(dag, B0, Y, prevZ, clock, S):
    """One propagation phase; returns (status, Bf, final lifted box)."""
    S.phases += 1
    cuts, starts = [], []
    xb = B0
    lastZ = None
    status = 'ok'
    nruns = rng.randint(1, 4)
    for r in range(nruns):
        c = clock.maybe_drop() if r > 0 else clock.c
        base = P.z0(dag, xb)
        opts = ['z0']
        if lastZ is not None:
            opts.append('prev')
        if Y is not None:
            opts.append('inh')
        if r == 0 and prevZ is not None:
            opts.append('prevphase')
        how = rng.choice(opts)
        try:
            if how == 'prev':
                start = P.meet_boxes(lastZ, base)
            elif how == 'inh':
                start = P.meet_boxes(Y, base)
                S.inherited += 1
            elif how == 'prevphase':
                start = P.meet_boxes(prevZ, base)
            else:
                start = base
        except P.Empty:
            start = None
        cuts.append(c)
        starts.append(start)
        S.runs += 1
        if start is None:
            status = 'empty'
            break
        sched = 'hc4' if rng.random() < 0.7 else 'rand'
        st, Z, _ = P.run(dag, start, c, rng.randint(1, 5), schedule=sched, rng=rng)
        if st == 'empty':
            status = 'empty'
            break
        lastZ = Z
        xb = P.xbox(dag, Z)
    cmin, cmax = min(cuts), max(cuts)
    if cmax > cmin:
        S.multi_cut += 1
    stD, D, _ = fixed(dag, B0, cmin)
    # (i) D inside each start box
    for start in starts:
        if stD == 'empty':
            continue
        if stD == 'limit':
            S.start_skip += 1
            continue
        if start is not None and P.inside(D, start):
            S.start_ok += 1
        else:
            S.start_bad += 1
    if status == 'empty':
        S.empties += 1
        if stD != 'empty':
            S.empty_bad += 1
        return 'empty', None, None
    Bf = xb
    for Sx in frame(B0, Bf):
        S.pieces += 1
        st2, Z2, _ = fixed(dag, Sx, cmin)
        if st2 != 'empty' and not P.inside(P.xbox(dag, Z2), Bf):
            if st2 == 'limit':
                S.piece_skip += 1
            else:
                S.piece_bad += 1
        if cmax > cmin:
            S.ctrl_pieces += 1
            st3, Z3, _ = fixed(dag, Sx, cmax)
            if st3 == 'fixed' and not P.inside(P.xbox(dag, Z3), Bf):
                S.ctrl_bad += 1
    return 'ok', Bf, lastZ


def rel_shrink(B):
    out = []
    for lo, hi in B:
        w = hi - lo
        out.append((lo + rng.uniform(0, 0.15) * w, hi - rng.uniform(0, 0.15) * w))
    return out


def node(dag, B, Y, clock, depth, S):
    S.depth_max = max(S.depth_max, depth)
    if rng.random() < 0.3:
        B = rel_shrink(B)                       # R-rel round before the phase
    useY = Y if (Y is not None and rng.random() < 0.8) else None
    st, Bf, Zf = phase(dag, B, useY, None, clock, S)
    if st == 'empty':
        return
    if rng.random() < 0.3:                      # R-rel round, then a second phase
        S.second_phase += 1
        B2 = rel_shrink(Bf)
        st, Bf, Zf2 = phase(dag, B2, useY, Zf, clock, S)
        if st == 'empty':
            return
        Zf = Zf2
    if depth >= 3:
        return
    i = max(range(len(Bf)), key=lambda k: Bf[k][1] - Bf[k][0])
    lo, hi = Bf[i]
    if hi - lo < 1e-9:
        return
    m = lo + rng.uniform(0.3, 0.7) * (hi - lo)
    for part in ((lo, m), (m, hi)):
        child = list(Bf)
        child[i] = part
        node(dag, child, Zf, clock, depth + 1, S)


def part_c(insts):
    print('(C) merged phases, restarts, decreasing cutoffs, inherited bounds (depth-3 trees):')
    tot = Stats()
    for name, J in insts.items():
        S = Stats()
        for _ in range(80):
            B = rand_box(name, J['box'], 10 ** rng.uniform(-2, -0.2))
            clock = Clock(rng.uniform(0.0, 0.25), -1e-3)
            node(J['dag'], B, None, clock, 0, S)
        print(f'    {name:13s}: phases {S.phases:3d} (runs {S.runs:3d}, multi-cutoff {S.multi_cut:3d}, '
              f'inherited starts {S.inherited:3d}, second phases {S.second_phase:2d}); '
              f'D⊆start {S.start_ok}/{S.start_ok + S.start_bad}; pieces {S.pieces}, bad {S.piece_bad}, '
              f'skip {S.piece_skip}; empties {S.empties}, bad {S.empty_bad}; '
              f'control(c_max) {S.ctrl_bad}/{S.ctrl_pieces}')
        for k, v in S.__dict__.items():
            if k != 'depth_max':
                setattr(tot, k, getattr(tot, k) + v)
    print(f'    TOTAL: phases {tot.phases}, runs {tot.runs}, inherited starts {tot.inherited}, '
          f'second phases {tot.second_phase}, multi-cutoff phases {tot.multi_cut}')
    print(f'    (i)   D ⊆ start box: {tot.start_ok} ok, {tot.start_bad} violations, '
          f'{tot.start_skip} skipped (D not converged)')
    print(f'    (ii)  frame pieces: {tot.pieces}, violations {tot.piece_bad}, '
          f'unconverged-and-not-inside {tot.piece_skip}')
    print(f'    (iii) emptied phases: {tot.empties}, with D nonempty: {tot.empty_bad}')
    print(f'    control, largest cutoff of the phase instead of smallest: '
          f'{tot.ctrl_bad} of {tot.ctrl_pieces} pieces NOT certified (test has power)')


def part_d():
    """f = -3x^2 + 2x^2 + 2x^2 on X0 = [-1, 1], F = {x >= 0.5}, f* = 0.25."""
    d = P.DAG(1)
    p = [d.pow(0, 2) for _ in range(3)]
    g = d.sum([0], [-1.0], 0.5)                 # g = 0.5 - x <= 0
    d.sum(p, [-3, 2, 2])
    dag = d.nodes
    eps = 1e-3
    c = 0.25 - eps
    st, _, r = P.fixpoint(dag, [(-1.0, 1.0)], c, cons=[g])
    E = I.endpoint()['dag']
    stf, Zf, _ = P.fixpoint(E, [(-1.0, 1.0)], c)
    y = 0.75
    q = (y + 1) * (1 - y)
    m = y * y - 0.25
    print('(D) interleaved constraint propagation: f = -3x^2 + 2x^2 + 2x^2 on [-1,1], '
          'F = {x >= 0.5}, f* = 0.25, cutoff f* - 1e-3:')
    print(f'    objective + constraint in one run: {st} after {r} rounds (leaf B_0 = [-1,1])')
    print(f'    objective alone at the same cutoff: {stf}, x-box {P.xbox(E, Zf)[0] if Zf else None}'
          f' -> pi_D([-1,1], y) <= c for every y, so (Π) fails at the feasible y = {y}')
    print(f'    (V) at y = {y}: m + eps = {m + eps:.4f}, q_C = {q:.4f}; fails for alpha > '
          f'{(m + eps) / q:.3f} (e.g. alphaBB with alpha = 1)')


class UpDownClock(Clock):
    def maybe_drop(self, p=0.5):
        if rng.random() < p:
            self.c = min(0.3, max(self.floor, self.c + rng.uniform(-0.08, 0.08)))
        return self.c


def part_e(insts):
    tot = dict(pieces=0, bad_phase=0, bad_chain=0, starts=0, start_bad_phase=0, start_bad_chain=0)

    def node_e(dag, B, Y, clock, depth, chain):
        cuts = []
        xb, lastZ, starts = B, None, []
        for r in range(rng.randint(1, 3)):
            c = clock.maybe_drop()
            cuts.append(c)
            base = P.z0(dag, xb)
            try:
                start = P.meet_boxes(Y, base) if (Y is not None and r == 0) else (
                    P.meet_boxes(lastZ, base) if lastZ is not None else base)
            except P.Empty:
                start = None
            starts.append(start)
            if start is None:
                return
            st, Z, _ = P.run(dag, start, c, rng.randint(1, 5))
            if st == 'empty':
                return
            lastZ, xb = Z, P.xbox(dag, Z)
        cph = min(cuts)
        cch = min(cph, chain)
        for cc, key, skey in ((cph, 'bad_phase', 'start_bad_phase'), (cch, 'bad_chain', 'start_bad_chain')):
            stD, D, _ = fixed(dag, B, cc)
            if stD == 'fixed':
                for s_ in starts:
                    if not P.inside(D, s_):
                        tot[skey] += 1
        tot['starts'] += len(starts)
        for Sx in frame(B, xb):
            tot['pieces'] += 1
            for cc, key in ((cph, 'bad_phase'), (cch, 'bad_chain')):
                st2, Z2, _ = fixed(dag, Sx, cc)
                if st2 == 'fixed' and not P.inside(P.xbox(dag, Z2), xb):
                    tot[key] += 1
        if depth >= 3:
            return
        i = max(range(len(xb)), key=lambda k: xb[k][1] - xb[k][0])
        lo, hi = xb[i]
        m = lo + rng.uniform(0.3, 0.7) * (hi - lo)
        for part in ((lo, m), (m, hi)):
            child = list(xb)
            child[i] = part
            node_e(dag, child, lastZ, clock, depth + 1, cch)

    for name, J in insts.items():
        for _ in range(40):
            B = rand_box(name, J['box'], 10 ** rng.uniform(-2, -0.2))
            node_e(J['dag'], B, None, UpDownClock(rng.uniform(-1e-3, 0.25), -1e-3), 0, float('inf'))
    print(f"(E) incumbents that may increase, children always start from inherited bounds: "
          f"{tot['starts']} run starts, {tot['pieces']} frame pieces.")
    print(f"    certificate at the phase's smallest cutoff (note's proof): D not inside a start box "
          f"{tot['start_bad_phase']} times, uncertified pieces {tot['bad_phase']}")
    print(f"    certificate at the smallest cutoff along the inheritance chain: D not inside a start "
          f"box {tot['start_bad_chain']} times, uncertified pieces {tot['bad_chain']}")


if __name__ == '__main__':
    part_a()
    insts = instances()
    part_b(insts)
    part_c(insts)
    part_e(insts)
    part_d()
