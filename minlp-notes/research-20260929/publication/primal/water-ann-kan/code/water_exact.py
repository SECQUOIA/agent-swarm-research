"""Exactly feasible points for waterno2_T (T = 06, 09, 12, 18, 24).

Every row of waterno2 is a polynomial with decimal coefficients.  The point is
built so that each coordinate is either rational or lies in one quadratic
field Q(w_k), where w_k is the speed of one pump station in one period:

1. Binaries are taken from the numerical point.  Rows are simplified with the
   binaries substituted.  Linear rows that pin a variable (a row bound meeting a
   variable bound), and pairs of rows that pin a linear form (big-M pairs for
   running pumps), become equalities.
2. The pumps of one station share a speed variable and a head; their flows are
   then equal in every feasible point, so the flows of the running pumps of a
   station are aliased to one representative.  The representatives are the
   seeds (free rational choices).
3. Linear phase: linear rows give every level and flow total as an affine
   form of the seeds.  Linear constraints that are active at the numerical
   point (tank levels at bounds, the horizon row) are imposed as exact
   equalities by a minimum-norm rational correction of the seeds.
4. Nonlinear phase: equality rows are solved one unknown at a time.  A row
   whose only unknown is a station speed (through w^2 and q w) becomes a
   quadratic in w with rational coefficients; w is its root nearest the
   numerical speed (rational isolating interval).  Other inequality rows that
   are active at the numerical point (station-B head lower bounds) are imposed
   as equalities.  A speed left free at the end is fixed at a rational value.
5. Each cost variable is set to a rational upper bound of its power expression
   (its row then holds strictly or with equality), so the objective is rational.
6. verify() evaluates every OSIL row and bound exactly (qfield arithmetic).

usage: python3 water_exact.py T point.(sol|json) out.json
"""
import json
import sys
import time
from fractions import Fraction as Fr

import mpmath as mp

import osil
import qfield as Q
from qfield import Val, Mixed

ACT_TOL = Fr(1, 10 ** 7)


def read_point(M, path):
    names = M["names"]
    idx = {n: i for i, n in enumerate(names)}
    if path.endswith(".json"):
        d = json.load(open(path))
        x = [Fr(s) for s in d["x"]]
        assert len(x) == len(names)
        return x
    x = [Fr(0)] * len(names)
    for line in open(path):
        p = line.split()
        if len(p) < 2 or p[0] == "objvar":
            continue
        x[idx[p[0]]] = Fr(p[1])
    return x


def evalF(c, x):
    return osil.eval_row(c, x, {"num": lambda q: q})


class Builder:
    def __init__(self, M, xh, log=print, shifts=None):
        self.M, self.xh, self.log = M, xh, log
        self.shifts = shifts or {}
        n = len(M["names"])
        self.n = n
        self.isbin = [M["vtype"][j] == "B" for j in range(n)]
        self.bval = {}
        for j in range(n):
            if self.isbin[j]:
                b = round(xh[j])
                assert abs(xh[j] - b) < Fr(1, 10 ** 6)
                self.bval[j] = Fr(b)
        self.objvars = set(M["obj"]["lin"])

    # ---------- step 1: rows with binaries substituted ----------
    def simplify_rows(self):
        R = []
        for c in self.M["cons"]:
            const = c["const"]
            lin = {}
            for j, a in c["lin"].items():
                if self.isbin[j]:
                    const += a * self.bval[j]
                else:
                    lin[j] = lin.get(j, Fr(0)) + a
            quad = []
            for i, j, a in c["quad"]:
                bi, bj = self.isbin[i], self.isbin[j]
                if bi and bj:
                    const += a * self.bval[i] * self.bval[j]
                elif bi:
                    if self.bval[i] != 0:
                        lin[j] = lin.get(j, Fr(0)) + a * self.bval[i]
                elif bj:
                    if self.bval[j] != 0:
                        lin[i] = lin.get(i, Fr(0)) + a * self.bval[j]
                else:
                    quad.append((i, j, a))
            if c["nl"] is not None:
                assert not any(self.isbin[v] for v in osil.tree_vars(c["nl"]))
            lin = {j: a for j, a in lin.items() if a != 0}
            R.append(dict(name=c["name"], const=const, lin=lin, quad=quad, nl=c["nl"],
                          lb=c["lb"], ub=c["ub"]))
        self.R = R

    def tighten(self):
        """Pinned variables and pinned linear forms (exact)."""
        n = self.n
        lo = list(self.M["lb"])
        hi = list(self.M["ub"])
        pinned = {}
        derived = []  # (lin, value, names)
        changed = True
        while changed:
            changed = False
            groups = {}
            for r in self.R:
                if r["quad"] or r["nl"] is not None:
                    continue
                const = r["const"]
                lin = {}
                for j, a in r["lin"].items():
                    if j in pinned:
                        const += a * pinned[j]
                    else:
                        lin[j] = a
                if not lin:
                    continue
                rl = None if r["lb"] is None else r["lb"] - const
                ru = None if r["ub"] is None else r["ub"] - const
                if len(lin) == 1:
                    (j, a), = lin.items()
                    bl, bu = (rl, ru) if a > 0 else (ru, rl)
                    bl = None if bl is None else bl / a
                    bu = None if bu is None else bu / a
                    if bl is not None and (lo[j] is None or bl > lo[j]):
                        lo[j] = bl
                    if bu is not None and (hi[j] is None or bu < hi[j]):
                        hi[j] = bu
                    continue
                # normalise: first index coefficient +1
                j0 = min(lin)
                s = lin[j0]
                key = tuple(sorted((j, a / s) for j, a in lin.items()))
                l2, u2 = (rl, ru) if s > 0 else (ru, rl)
                l2 = None if l2 is None else l2 / s
                u2 = None if u2 is None else u2 / s
                g = groups.setdefault(key, [None, None, []])
                if l2 is not None and (g[0] is None or l2 > g[0]):
                    g[0] = l2
                if u2 is not None and (g[1] is None or u2 < g[1]):
                    g[1] = u2
                g[2].append(r["name"])
            for j in range(n):
                if self.isbin[j] or j in pinned:
                    continue
                if lo[j] is not None and hi[j] is not None:
                    assert lo[j] <= hi[j], (self.M["names"][j], lo[j], hi[j])
                    if lo[j] == hi[j]:
                        pinned[j] = lo[j]
                        changed = True
            derived = []
            for key, (l2, u2, names) in groups.items():
                if l2 is not None and u2 is not None:
                    assert l2 <= u2, (names, l2, u2)
                    if l2 == u2 and len(names) >= 2:
                        derived.append((dict(key), l2, names))
        self.pinned, self.derived = pinned, derived
        self.lo, self.hi = lo, hi
        self.log(f"pinned variables: {len(pinned)}; derived equalities from row pairs: {len(derived)}")

    # ---------- step 2: pumps, speeds, aliases, seeds ----------
    def pumps(self):
        M = self.M
        cube = set()
        for c in M["cons"]:
            t = c["nl"]
            if t is not None and t[0] == "pow" and t[1][0] == "var" and t[2] == ("num", Fr(3)):
                cube.add(t[1][1])
        speeds = sorted(j for j in cube if M["lb"][j] is not None and M["lb"][j] > 0)
        flows = sorted(j for j in cube if M["lb"][j] == 0)
        flowset = set(flows)
        pumps_of = {w: set() for w in speeds}
        for c in M["cons"]:
            for i, j, a in c["quad"]:
                if i in pumps_of and j in flowset:
                    pumps_of[i].add(j)
                if j in pumps_of and i in flowset:
                    pumps_of[j].add(i)
        self.speeds, self.flows, self.pumps_of = speeds, flows, pumps_of
        assert sorted(f for w in speeds for f in pumps_of[w]) == flows, "every flow belongs to one speed"
        rep = {}
        seeds = []
        for w in speeds:
            run = sorted(f for f in pumps_of[w] if f not in self.pinned)
            if not run:
                continue
            vals = [self.xh[f] for f in run]
            assert max(vals) - min(vals) < Fr(1, 10 ** 6), ("running pumps of one station differ", vals)
            for f in run:
                rep[f] = run[0]
            seeds.append(run[0])
        self.rep, self.seeds = rep, seeds
        # running stations whose speed sits at a bound in the numerical point
        self.atbound = {}
        for w in speeds:
            run = [f for f in pumps_of[w] if f not in self.pinned]
            if not run or w in self.pinned:
                continue
            if self.xh[w] - self.lo[w] < Fr(1, 10 ** 6):
                self.atbound[rep[run[0]]] = (w, +1)
            elif self.hi[w] - self.xh[w] < Fr(1, 10 ** 6):
                self.atbound[rep[run[0]]] = (w, -1)
        self.log(f"speeds: {len(speeds)}, flows: {len(flows)}, seed flows (running stations): {len(seeds)}")

    def R_(self, j):
        return self.rep.get(j, j)

    # ---------- active constraints at the numerical point ----------
    def active(self):
        xh = self.xh
        act_rows, act_bounds = [], []
        derived_names = {nm for _, _, names in self.derived for nm in names}
        for r, c in zip(self.R, self.M["cons"]):
            if r["lb"] is not None and r["ub"] is not None and r["lb"] == r["ub"]:
                continue
            if r["name"] in derived_names:
                continue
            if not r["lin"] and not r["quad"] and r["nl"] is None:
                continue
            if set(r["lin"]) & self.objvars:
                continue  # cost rows: handled at the end
            v = evalF(c, xh)
            for side, b in (("lb", r["lb"]), ("ub", r["ub"])):
                if b is None:
                    continue
                s = v - b if side == "lb" else b - v
                if abs(s) <= ACT_TOL * max(1, abs(b)):
                    vs = set(r["lin"]) | {a for a, _, _ in r["quad"]} | {b2 for _, b2, _ in r["quad"]}
                    if all(j in self.pinned for j in vs):
                        continue
                    if len(r["lin"]) == 1 and not r["quad"] and r["nl"] is None:
                        continue  # single-variable rows are bounds (tightened); handled below
                    act_rows.append((r, side, b))
        for j in range(self.n):
            if self.isbin[j] or j in self.pinned or j in self.objvars:
                continue
            for side, b in (("lb", self.lo[j]), ("ub", self.hi[j])):
                if b is None:
                    continue
                s = xh[j] - b if side == "lb" else b - xh[j]
                if abs(s) <= ACT_TOL * max(1, abs(b)):
                    act_bounds.append((j, side, b))
        self.act_rows, self.act_bounds = act_rows, act_bounds
        self.log(f"active at the numerical point: {len(act_rows)} rows, {len(act_bounds)} bounds")
        for r, side, b in act_rows:
            self.log(f"   active row {r['name']} {side} {float(b)}")
        for j, side, b in act_bounds:
            self.log(f"   active bound {self.M['names'][j]} {side} {float(b)} (point {float(self.xh[j])})")

    # ---------- step 3: linear phase ----------
    def linear_phase(self):
        """Affine forms (dict seed -> coef, plus key None) through linear equality rows."""
        A = {}
        for j, v in self.pinned.items():
            A[j] = {None: v}
        for s in self.seeds:
            A[s] = {s: Fr(1)}
        for f, r in self.rep.items():
            if f != r:
                A[f] = A[r]
        eqs = []
        for r in self.R:
            if r["quad"] or r["nl"] is not None:
                continue
            if r["lb"] is not None and r["lb"] == r["ub"]:
                eqs.append((r["lin"], r["lb"] - r["const"]))
        for lin, val, _ in self.derived:
            eqs.append((lin, val))
        done = [False] * len(eqs)
        prog = True
        while prog:
            prog = False
            for k, (lin, rhs) in enumerate(eqs):
                if done[k]:
                    continue
                unk = [j for j in lin if j not in A]
                if len(unk) > 1:
                    continue
                if len(unk) == 0:
                    done[k] = True
                    continue
                v = unk[0]
                acc = {None: rhs}
                for j, a in lin.items():
                    if j == v:
                        continue
                    for s, cf in A[j].items():
                        acc[s] = acc.get(s, Fr(0)) - a * cf
                A[v] = {s: cf / lin[v] for s, cf in acc.items() if cf != 0 or s is None}
                done[k] = True
                prog = True
        self.aff = A
        # equations from active linear constraints
        rows = []
        for r, side, b in self.act_rows:
            if r["quad"] or r["nl"] is not None or not all(j in A for j in r["lin"]):
                continue
            acc = {None: r["const"]}
            for j, a in r["lin"].items():
                for s, cf in A[j].items():
                    acc[s] = acc.get(s, Fr(0)) + a * cf
            rows.append((acc, b, f"row {r['name']}"))
            r["_lin_phase"] = True
        for j, side, b in self.act_bounds:
            if j in A:
                rows.append((dict(A[j]), b, f"bound {self.M['names'][j]} {side}"))
        self.lin_act = rows
        # stations with a speed at a bound: move the flow so that the speed moves inside
        # (the speed increases with the station flow when the head is fixed by the rows)
        for s, (w, dirn) in self.atbound.items():
            if self.M["names"][w] in self.shifts:
                d = self.shifts[self.M["names"][w]]
                rows.append(({s: Fr(1)}, self.xh[s] + dirn * d, f"speed {self.M['names'][w]} at bound: flow shift {float(d):.0e}"))
                self.log(f"   station with speed {self.M['names'][w]}: flow shifted by {dirn * float(d):.0e}")
        # solve: sum_s acc[s] * seed_s + acc[None] = b, seeds = s0 + d
        s0 = {s: self.xh[s] for s in self.seeds}
        eq = []
        for acc, b, nm in rows:
            coef = {s: cf for s, cf in acc.items() if s is not None and cf != 0}
            resid = b - acc.get(None, Fr(0)) - sum(cf * s0[s] for s, cf in coef.items())
            if not coef:
                assert resid == 0, ("active constraint independent of seeds is violated", nm, float(resid))
                continue
            eq.append((coef, resid, nm))
        d = min_norm(eq, self.seeds)
        self.seedval = {s: s0[s] + d.get(s, Fr(0)) for s in self.seeds}
        mx = max([abs(v) for v in d.values()], default=Fr(0))
        self.log(f"linear phase: {len(eq)} active linear constraints imposed; max seed correction {float(mx):.3e}")
        for coef, resid, nm in eq:
            got = sum(cf * self.seedval[s] for s, cf in coef.items()) - sum(cf * s0[s] for s, cf in coef.items())
            assert got == resid, nm

    # ---------- step 4: nonlinear phase ----------
    def nonlinear_phase(self):
        x = {}
        self.x = x
        for j, b in self.bval.items():
            x[j] = Val.const(b)
        for j, v in self.pinned.items():
            x[j] = Val.const(v)
        for s, v in self.seedval.items():
            x[s] = Val.const(v)
        self.symvar = {}
        for w in self.speeds:
            if w in self.pinned:
                continue
            k = Q.SYM.new(self.M["names"][w])
            self.symvar[k] = w
            x[w] = Val(k, (Fr(0), Fr(1)))
        rows = []
        for r in self.R:
            if r["lb"] is not None and r["lb"] == r["ub"]:
                rows.append(dict(r, rhs=r["lb"]))
        for lin, val, names in self.derived:
            rows.append(dict(name="pair:" + "+".join(names), const=Fr(0), lin=lin, quad=[], nl=None, rhs=val))
        for r, side, b in self.act_rows:
            if r.get("_lin_phase"):
                continue
            rows.append(dict(r, rhs=b, name=r["name"] + "(active " + side + ")"))
            self.log(f"   imposing active row {r['name']} {side} as an equality")
        self.eqrows = rows
        done = [False] * len(rows)
        nfix = 0
        while True:
            prog = True
            while prog:
                prog = False
                for k, r in enumerate(rows):
                    if done[k]:
                        continue
                    st = self.try_row(r)
                    if st:
                        done[k] = True
                        prog = True
            unknown = [j for j in range(self.n) if not self.isbin[j] and self.R_(j) not in x and j not in self.objvars]
            if not unknown:
                break
            free = [k for k in self.symvar if not Q.SYM.solved(k)]
            if free:
                k = free[0]
                wj = self.symvar[k]
                wv = Fr(mp.nstr(mp.mpf(float(self.xh[wj])), 15))
                wv = min(max(wv, self.lo[wj]), self.hi[wj])
                Q.SYM.S[k].update(solved=True, rational=wv)
                nfix += 1
                self.log(f"   speed {Q.SYM.S[k]['name']} left free; fixed at rational {wv}")
                continue
            # a free continuous variable (slack-like, e.g. a head of a station that is off):
            # fix it at an active bound if it has one, else at its numerical value
            act = {j: b for j, side, b in self.act_bounds}
            cand = [j for j in unknown if j in act]
            j = cand[0] if cand else unknown[0]
            v = act[j] if cand else self.xh[j]
            x[self.R_(j)] = Val.const(v)
            self.log(f"   free variable {self.M['names'][j]} fixed at {'its active bound' if cand else 'the numerical value'} {float(v)}")
        for j in list(x):
            x[j] = x[j].norm()
        for f, r in self.rep.items():
            x[f] = x[r]
        pend = [rows[k]["name"] for k in range(len(rows)) if not done[k]]
        # rows not used are checked by verify(); report how many
        self.log(f"nonlinear phase: {sum(done)} equality rows used, {len(pend)} not used (checked by verify)")
        unsolved = [k for k in self.symvar if not Q.SYM.solved(k)]
        assert not unsolved

    def val(self, j):
        return self.x.get(self.R_(j))

    def try_row(self, r):
        x = self.x
        try:
            unk = set()
            for j in r["lin"]:
                if self.val(j) is None:
                    unk.add(self.R_(j))
            for i, j, a in r["quad"]:
                for v in (i, j):
                    if self.val(v) is None:
                        unk.add(self.R_(v))
            if r["nl"] is not None:
                for v in osil.tree_vars(r["nl"]):
                    if self.val(v) is None:
                        unk.add(self.R_(v))
            if len(unk) > 1:
                return False
            if len(unk) == 1:
                (v,) = unk
                if r["nl"] is not None and any(self.R_(t) == v for t in osil.tree_vars(r["nl"])):
                    return False
                coef = Val.const(0)
                rest = Val.const(r["const"])
                for j, a in r["lin"].items():
                    if self.R_(j) == v:
                        coef = coef + Val.const(a)
                    else:
                        rest = rest + self.val(j) * a
                for i, j, a in r["quad"]:
                    ri, rj = self.R_(i), self.R_(j)
                    if ri == v and rj == v:
                        return False
                    if ri == v:
                        coef = coef + self.val(j) * a
                    elif rj == v:
                        coef = coef + self.val(i) * a
                    else:
                        rest = rest + self.val(i) * self.val(j) * a
                if r["nl"] is not None:
                    rest = rest + osil.eval_tree(r["nl"], self._xv(), {"num": Val.const})
                coef = coef.norm()
                if coef.k is not None and not Q.SYM.solved(coef.k):
                    return False
                if Q.sign(coef) == 0:
                    return False
                x[v] = ((Val.const(r["rhs"]) - rest) / coef).norm()
                return True
            # no unknowns: an equation in the symbols
            val = Val.const(r["const"])
            for j, a in r["lin"].items():
                val = val + self.val(j) * a
            for i, j, a in r["quad"]:
                val = val + self.val(i) * self.val(j) * a
            if r["nl"] is not None:
                val = val + osil.eval_tree(r["nl"], self._xv(), {"num": Val.const})
            res = (val - r["rhs"]).norm()
            if res.k is None:
                assert res.c[0] == 0, ("conflict in row", r["name"], float(res.c[0]))
                return True
            if Q.SYM.solved(res.k):
                assert Q.sign(res) == 0, ("conflict in row", r["name"])
                return True
            if len(res.c) > 3:
                return False
            k = res.k
            near = mp.mpf(float(self.xh[self.symvar[k]]))
            Q.solve_symbol(k, res.c, near)
            return True
        except Mixed:
            return False

    def _xv(self):
        class XV:
            def __getitem__(s, j):
                return self.val(j)
        return XV()

    # ---------- step 5: costs ----------
    def costs(self, grid=10 ** 30):
        x = self.x
        for j in self.objvars:
            rows = [r for r in self.R if j in r["lin"]]
            assert len(rows) == 1, self.M["names"][j]
            r = rows[0]
            a = r["lin"][j]
            rest = Val.const(r["const"])
            for i, aa in r["lin"].items():
                if i != j:
                    rest = rest + self.val(i) * aa
            for i, i2, aa in r["quad"]:
                rest = rest + self.val(i) * self.val(i2) * aa
            assert r["nl"] is None
            # need lb <= a c + rest <= ub
            lo_c, hi_c = self.lo[j], self.hi[j]
            need_lo = None
            if a < 0 and r["ub"] is not None:
                lo_e, hi_e = Q.enclose((rest - r["ub"]) / (-a))
                need_lo = hi_e
            elif a > 0 and r["lb"] is not None:
                lo_e, hi_e = Q.enclose((Val.const(r["lb"]) - rest) / a)
                need_lo = hi_e
            else:
                raise AssertionError("unexpected cost row shape " + r["name"])
            c = Fr(-((-need_lo * grid).numerator // (-need_lo * grid).denominator), grid)  # ceil on grid
            if lo_c is not None and c < lo_c:
                c = lo_c
            x[j] = Val.const(c)
        self.obj = self.M["obj"]["const"] + sum(a * x[j].c[0] for j, a in self.M["obj"]["lin"].items())

    def full_point(self):
        out = []
        for j in range(self.n):
            v = self.val(j)
            assert v is not None, self.M["names"][j]
            out.append(v.norm())
        return out


def min_norm(eq, seeds):
    """Exact minimum-norm d with sum_s coef[s] d[s] = resid for every equation (dependent rows dropped)."""
    if not eq:
        return {}
    cols = sorted({s for coef, _, _ in eq for s in coef})
    ci = {s: i for i, s in enumerate(cols)}
    rows = []
    for coef, resid, nm in eq:
        a = [Fr(0)] * len(cols)
        for s, cf in coef.items():
            a[ci[s]] = cf
        rows.append((a, resid, nm))
    # independent subset by exact elimination
    basis, keep = [], []
    for a, r, nm in rows:
        v = list(a) + [r]
        for (piv, bv) in basis:
            if v[piv] != 0:
                f = v[piv] / bv[piv]
                v = [p - f * q for p, q in zip(v, bv)]
        nz = [i for i in range(len(cols)) if v[i] != 0]
        if not nz:
            assert v[-1] == 0, ("inconsistent active constraints", nm, float(v[-1]))
            continue
        basis.append((nz[0], v))
        keep.append((a, r))
    m = len(keep)
    G = [[sum(keep[i][0][k] * keep[j][0][k] for k in range(len(cols))) for j in range(m)] for i in range(m)]
    rhs = [keep[i][1] for i in range(m)]
    y = solve_exact(G, rhs)
    d = {}
    for k, s in enumerate(cols):
        d[s] = sum(keep[i][0][k] * y[i] for i in range(m))
    return d


def solve_exact(G, b):
    n = len(G)
    A = [list(G[i]) + [b[i]] for i in range(n)]
    for c in range(n):
        p = next(i for i in range(c, n) if A[i][c] != 0)
        A[c], A[p] = A[p], A[c]
        for i in range(n):
            if i != c and A[i][c] != 0:
                f = A[i][c] / A[c][c]
                A[i] = [u - f * v for u, v in zip(A[i], A[c])]
    return [A[i][n] / A[i][i] for i in range(n)]


def verify(M, xv, log=print):
    """Exact check of every row, bound and integrality requirement."""
    F = {"num": Val.const}
    worst = None
    nrow = neq = 0
    for c in M["cons"]:
        v = osil.eval_row(c, xv, F).norm()
        nrow += 1
        if c["lb"] is not None and c["ub"] is not None and c["lb"] == c["ub"]:
            neq += 1
            if Q.sign(v - c["lb"]) != 0:
                return False, f"equality row {c['name']} fails"
            continue
        if c["lb"] is not None and Q.sign(v - c["lb"]) < 0:
            return False, f"row {c['name']} below its lower bound"
        if c["ub"] is not None and Q.sign(v - c["ub"]) > 0:
            return False, f"row {c['name']} above its upper bound"
    for j in range(len(xv)):
        v = xv[j]
        if M["lb"][j] is not None and Q.sign(v - M["lb"][j]) < 0:
            return False, f"variable {M['names'][j]} below its lower bound"
        if M["ub"][j] is not None and Q.sign(v - M["ub"][j]) > 0:
            return False, f"variable {M['names'][j]} above its upper bound"
        if M["vtype"][j] in ("B", "I"):
            if not (v.k is None and v.c[0].denominator == 1):
                return False, f"variable {M['names'][j]} not integral"
    obj = M["obj"]["const"] + sum((xv[j] * a for j, a in M["obj"]["lin"].items()), Val.const(0))
    for i, j, a in M["obj"]["quad"]:
        obj = obj + xv[i] * xv[j] * a
    assert M["obj"]["nl"] is None
    return True, dict(rows=nrow, equalities=neq, obj=obj.norm())


def dump(M, xv, obj, path, meta):
    syms = {}
    xs = {}
    for j, v in enumerate(xv):
        if v.k is None:
            xs[M["names"][j]] = str(v.c[0])
        else:
            s = Q.SYM.S[v.k]
            syms[v.k] = dict(name=s["name"], A=str(s["A"]), B=str(s["B"]), C=str(s["C"]),
                             lo=str(s["lo"]), hi=str(s["hi"]))
            xs[M["names"][j]] = dict(w=v.k, c0=str(v.c[0]), c1=str(v.c[1]))
    json.dump(dict(meta, objective=str(obj), objective_float=float(obj),
                   symbols={str(k): s for k, s in sorted(syms.items())},
                   symbol_note="w_k is the unique root of A w^2 + B w + C in the open interval (lo, hi); "
                               "a variable given as {w, c0, c1} equals c0 + c1 * w_k",
                   x=xs), open(path, "w"), indent=0)


def main():
    T = int(sys.argv[1])
    src, out = sys.argv[2], sys.argv[3]
    name = f"waterno2_{T:02d}"
    t0 = time.time()
    M = osil.load(name)
    xh = read_point(M, src)
    shifts = {}
    while True:
        Q.SYM = Q.Symbols()
        print(f"--- attempt with flow shifts {dict((k, float(v)) for k, v in shifts.items())}")
        B = Builder(M, xh, shifts=shifts)
        B.simplify_rows()
        B.tighten()
        B.pumps()
        B.active()
        B.linear_phase()
        B.nonlinear_phase()
        B.costs()
        xv = B.full_point()
        ok, info = verify(M, xv)
        print("verify:", ok, info if not ok else f"{info['rows']} rows ({info['equalities']} equalities) and all bounds hold exactly")
        if ok:
            break
        # a running station's speed outside its bound: shift that station's flow (x10 each retry)
        bad = info.split()[1]
        assert info.startswith("variable") and bad in [M["names"][w] for _, (w, _) in B.atbound.items()], info
        shifts[bad] = shifts.get(bad, Fr(1, 10 ** 10)) * 10
        assert shifts[bad] <= Fr(1, 10 ** 5), "giving up"
    obj = info["obj"]
    assert obj.k is None and obj.c[0] == B.obj
    nsym = sum(1 for k in B.symvar if Q.SYM.S[k]["rational"] is None)
    print(f"{name}: exactly feasible point, objective = {float(B.obj):.12f} (exact rational, "
          f"{len(str(B.obj.denominator))}-digit denominator); irrational speeds: {nsym}; "
          f"numerical point objective {float(sum(a * xh[j] for j, a in M['obj']['lin'].items())):.12f}")
    # evidence: distance to the numerical point
    with mp.workdps(50):
        dmax = max(abs(Q.to_mpf(v) - mp.mpf(float(xh[j]))) for j, v in enumerate(xv))
    print(f"max |exact point - numerical point| = {mp.nstr(dmax, 3)}; time {time.time() - t0:.1f} s")
    dump(M, xv, B.obj, out, dict(instance=name, source=src))


if __name__ == "__main__":
    main()
