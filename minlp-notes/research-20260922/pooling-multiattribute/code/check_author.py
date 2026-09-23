"""Check the author's rebuilt pq model (spp.SppInst + instance.build_pq) and outer LP (gridrelax.build outer=True)
against the original OSiL model:
  rows   : every original linear row appears (identically, after variable mapping) in the rebuilt pq LP;
           every bilinear row has its McCormick rows; bounds used by the rebuild are compared with OSiL bounds.
  points : feasible points of the original model (gen_points.py) are lifted into the author's outer LP
           (lambda = 1 on the x-interval piece containing y_lj) and all rows/bounds are evaluated.
Usage: check_author.py <osil> <points.npz> <G> [nolp]"""
import sys, json
import numpy as np
import gurobipy as gp
import spp, instance as I, gridrelax as GR
import indep_bound as B


def master_map(P, vars_):
    m, q, y, z, v = vars_
    mp = {}
    for k, var in q.items(): mp[var.index] = P.idx_q[k]
    for k, var in y.items(): mp[var.index] = P.idx_y[k]
    for k, var in z.items(): mp[var.index] = P.idx_z[k]
    for k, var in v.items(): mp[var.index] = P.idx_w[k]
    return mp


def row_coverage(S, P):
    vars_ = I.build_pq(P); m = vars_[0]; mp = master_map(P, vars_)
    assert len(set(mp.values())) == len(mp) == S.n, (len(mp), S.n)
    A = m.getA().tocsr(); rhs = m.getAttr("RHS", m.getConstrs()); sen = m.getAttr("Sense", m.getConstrs())
    have = {}
    for r in range(A.shape[0]):
        cols = A.indices[A.indptr[r]:A.indptr[r + 1]]; vals = A.data[A.indptr[r]:A.indptr[r + 1]]
        key = (tuple(sorted((mp[c], round(float(a), 12)) for c, a in zip(cols, vals) if a != 0)), sen[r], round(rhs[r], 9))
        have[key] = r
    missing = []
    for (row, lb, ub, r) in S.lin:
        items = tuple(sorted((j, round(float(a), 12)) for j, a in row.items()))
        for s, bnd in (("<", ub), (">", lb)):
            if bnd is None: continue
            if lb == ub and (items, "=", round(float(bnd), 9)) in have: continue
            if (items, s, round(float(bnd), 9)) not in have: missing.append((S.M.cnames[r], s))
    # bilinear rows: McCormick present with the author's bounds; compare bounds with OSiL
    xs = m.getVars(); inv = {mp[i]: i for i in mp}
    lbad = []
    for (l, j), yv in vars_[2].items():
        yb = P.ybound(l, j); yo = float(S.ub[P.idx_y[(l, j)]])
        if yb < yo - 1e-9: lbad.append(((l, j), yb, yo))
    obj = m.getAttr("Obj", xs); objdiff = max(abs(obj[i] - float(S.c.get(mp[i], 0))) for i in mp)
    ubdiff = [(S.M.vnames[mp[i]], xs[i].UB, float(S.ub[mp[i]])) for i in mp if xs[i].UB > float(S.ub[mp[i]]) + 1e-9]
    ubtight = [(S.M.vnames[mp[i]], xs[i].UB, float(S.ub[mp[i]])) for i in mp if xs[i].UB < float(S.ub[mp[i]]) - 1e-9]
    return dict(rebuilt_rows=A.shape[0], osil_linear_rows=len(S.lin), missing=missing, bilinear=len(S.W),
                pq_vars=len(vars_[4]), ybound_tighter_than_osil=len(lbad), ybound_examples=lbad[:3],
                objective_maxdiff=objdiff, looser_var_bounds=len(ubdiff), tighter_var_bounds=len(ubtight),
                tighter_examples=ubtight[:5])


def lift_author(P, m, blocks, mp, z):
    xs = m.getVars(); Z = np.zeros(len(xs))
    for i, o in mp.items(): Z[i] = z[o]
    vals = Z  # master values by index (only master part filled so far)
    for b in blocks:
        lam, ps, C = b._grid
        coords = [I.eval_expr(c, vals) for c in b.coords]
        pmv = b.pm.getVars(); full = np.zeros(len(pmv))
        for r, e in enumerate(b.pvars): full[e.index] = coords[r]
        full[pmv[1].index] = sum(coords[1 + 2 * len(b.P.inl[b.l]):])  # zb = sum of bypass flows
        XU = b.XU; xv = coords[0]
        grid = b._gridpts
        g = next((i for i in range(len(grid) - 1) if grid[i] <= xv <= grid[i + 1]), 0 if xv < grid[0] else len(grid) - 2)
        Z[lam.tolist()[g].index] = 1.0
        pv = ps[g].tolist()
        for k, var in enumerate(pv): Z[var.index] = full[k]
    return Z


if __name__ == "__main__":
    osil, ptsf, G = sys.argv[1], sys.argv[2], int(sys.argv[3])
    S = B.Struct(osil); P = spp.SppInst(osil)
    print("ROWS", json.dumps(row_coverage(S, P), default=str), flush=True)
    if "nolp" in sys.argv: sys.exit()
    D = np.load(ptsf); pts, tags = D["P"], D["tags"]
    grid = np.unique(np.concatenate([np.linspace(0, 1, G), np.geomspace(1e-3, 0.05, 6)]))
    m, blocks = GR.build(P, "D", grid, outer=True); m.update()
    for b in blocks: b._gridpts = b.XU * np.asarray(grid)
    mp = {}
    # master variables are the first variables of the model (build_pq), identical order to a fresh build_pq
    vars0 = I.build_pq(P); mp = master_map(P, vars0)
    A = m.getA().tocsr(); rhs = np.array(m.getAttr("RHS", m.getConstrs())); sen = np.array(m.getAttr("Sense", m.getConstrs()))
    lb = np.array(m.getAttr("LB", m.getVars())); ub = np.array(m.getAttr("UB", m.getVars()))
    print("AUTHOR_LP", A.shape, A.nnz, flush=True)
    worst = []
    for z, t in zip(pts, tags):
        Z = lift_author(P, m, blocks, mp, z)
        v = B.violation(A, rhs, sen, lb, ub, Z)
        worst.append((v["row_rel"], v["row_abs"], v["bound"], str(t), m.getConstrs()[v["worst_row"]].ConstrName))
    worst.sort(reverse=True)
    print("AUTHOR_POINTS", json.dumps(dict(n=len(worst), worst=worst[:5])), flush=True)
