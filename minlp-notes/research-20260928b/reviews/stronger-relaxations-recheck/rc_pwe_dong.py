"""Item (6): PWE ratios and an independent Dong-type exactness test for SDP1.

For every stored row of Tables 7.1, 7.2 and 7.4, regenerate the instance with my own generator copy,
recompute the PWE ratio at S* and compare with the stored `maxratio`. Recount the perspective-root-exact
cells: PWE ratio <= 1 when S* is optimal, otherwise the 1e-6 relative rule.

For rows with a stored SDP1 value, decide SDP1 root exactness at the OPT support T (|T| = k) by the
certificate of Proposition 3.1(a) / Dong's Theorem 2, written as one concave maximization:
    h(t) = lambda_min( Q - diag(mu(t)) ),  mu_i = t / b_i^2 (i in T),  mu_l = a_l^2 / t (l not in T),
with Q = X'X + lam I, b = beta^T, a = X' r_T. mu(t) is convex in t, so h is concave; SDP1 is exact iff
max_t h(t) >= 0. (My parametrization and optimizer differ from dong_check.py.)
usage: python3 rc_pwe_dong.py > rc_pwe_dong.log
"""
import json, os, collections
from rc_common import np, DATA, make_nested, make_pt, ridge, pwe_ratio
from scipy.optimize import minimize_scalar


def dong_h(X, y, lam, T):
    p = X.shape[1]
    T = list(T)
    _, bT, r = ridge(X, y, lam, T)
    a = X.T @ r
    Q = X.T @ X + lam * np.eye(p)
    inT = np.zeros(p, bool); inT[T] = True
    b2 = np.zeros(p); b2[T] = bT ** 2
    a2 = a ** 2
    qd = np.diag(Q)
    tlo = max(np.max(a2[~inT] / qd[~inT]), 1e-300)
    thi = np.min(b2[inT] * qd[inT])
    scale = np.linalg.eigvalsh(Q).max()

    def h(t):
        mu = np.where(inT, t / np.where(inT, b2, 1.0), a2 / t)
        return np.linalg.eigvalsh(Q - np.diag(mu)).min() / scale

    if tlo > thi:  # a diagonal entry of Q - diag(mu) is negative for every t
        return max(h(tlo), h(thi)), (tlo, thi)
    ts = np.geomspace(tlo, thi, 400) if thi > tlo else np.array([tlo])
    hv = np.array([h(t) for t in ts])
    j = int(np.argmax(hv))
    best = hv[j]
    if len(ts) > 1:
        lo, hi = ts[max(j - 1, 0)], ts[min(j + 1, len(ts) - 1)]
        res = minimize_scalar(lambda t: -h(t), bounds=(lo, hi), method="bounded",
                              options=dict(xatol=1e-14 * hi))
        best = max(best, -res.fun)
    return float(best), (tlo, thi)


def load(fn):
    return [json.loads(l) for l in open(os.path.join(DATA, fn))]


def optmap(fn):
    return {(o["p"], o["seed"], o["n"]): o for o in load(fn)}


def main():
    EX = 1e-6
    sets = [("n20", "mech_n20_k3.jsonl", "opt_mech_n20_k3.jsonl", "dong_n20.jsonl"),
            ("n40", "mech_n40_k3.jsonl", "opt_mech_n40_k3.jsonl", "dong_n40.jsonl"),
            ("cmp", "cmp_p100_k3.jsonl", "opt_cmp_p100_k3.jsonl", "dong_cmp.jsonl")]
    tot_agree = tot = 0
    for name, fn, ofn, dfn in sets:
        rows = load(fn)
        opt = optmap(ofn)
        dong = {(d["p"], d["seed"], d["n"]): d for d in load(dfn)}
        cells = collections.defaultdict(lambda: dict(runs=0, sopt=0, pe=0, s1=0, s1n=0, dg=0))
        max_ratio_err = 0.0
        agree = n1 = 0
        for r in rows:
            key = (r["p"], r["seed"], r["n"])
            o = opt.get(key)
            if o is None:
                continue
            if "OPT" in o:
                sopt, OPT = o["Sstar_opt"], min(r["fS"], o["OPT"])
            elif o.get("Sstar_opt") is True:
                sopt, OPT = True, r["fS"]
            else:
                continue  # OPT unknown: row not in the tables
            if name == "cmp":
                X, y, lam, S = make_pt(r["n"], r["p"], r["k"], r["seed"])
                ck = (r["p"], r["alpha"])
            else:
                X, y, lam, S = make_nested(r["n"], r["k"], 2560 if r["n"] == 20 else 3200, r["p"], r["seed"])
                ck = r["p"]
            assert abs(lam - r["lam"]) < 1e-12 * lam
            fS = ridge(X, y, lam, S)[0]
            assert abs(fS - r["fS"]) < 1e-9 * fS, (key, fS, r["fS"])
            ratio = pwe_ratio(X, y, lam, S)
            max_ratio_err = max(max_ratio_err, abs(ratio - r["maxratio"]) / ratio)
            pe = (ratio <= 1.0) if sopt else ((OPT - r["P"]) / OPT <= EX)
            c = cells[ck]
            c["runs"] += 1; c["sopt"] += bool(sopt); c["pe"] += bool(pe)
            if sopt and ratio <= 1.0 and (OPT - r["P"]) / OPT > EX:
                print(f"  [{name}] PWE-exact but solver gap > 1e-6: {key} ratio={ratio:.5f}")
            if sopt and ratio > 1.0 and (OPT - r["P"]) / OPT <= EX:
                print(f"  [{name}] solver gap <= 1e-6 but PWE ratio > 1: {key} ratio={ratio:.5f} "
                      f"gap={(OPT - r['P']) / OPT:.2e}")
            if r.get("sdp1") is not None and "OPT_support" in o:
                hmax, _ = dong_h(X, y, lam, o["OPT_support"])
                mine = hmax >= -1e-10
                solver = (OPT - r["sdp1"]) / OPT <= EX
                d = dong.get(key)
                c["s1n"] += 1; c["s1"] += solver; c["dg"] += mine
                n1 += 1
                ok = (mine == solver) and (d is not None and d["dong_exact"] == mine)
                agree += ok
                if not ok or abs(hmax) < 1e-3:
                    print(f"  [{name}] {key} alpha={r.get('alpha')} my max h={hmax:.3e} mine={mine} "
                          f"solver={solver} (gap {(OPT - r['sdp1']) / OPT:.2e}) dong_check="
                          f"{None if d is None else (d['dong_exact'], round(d['dong_minf'], 6))}")
        print(f"[{name}] max rel. error of stored PWE ratio: {max_ratio_err:.1e}; SDP1 rows {n1}, "
              f"three-way agreement (mine, solver rule, dong_check) {agree}/{n1}")
        tot += n1; tot_agree += agree
        for ck in sorted(cells):
            c = cells[ck]
            s1 = f"{c['s1']}/{c['s1n']} (mine {c['dg']}/{c['s1n']})" if c["s1n"] else "-"
            print(f"   cell {ck}: runs {c['runs']}, S* opt {c['sopt']}, persp exact {c['pe']}/{c['runs']}, "
                  f"SDP1 exact {s1}")
    print(f"TOTAL SDP1 rows {tot}, agreement {tot_agree}/{tot}")


if __name__ == "__main__":
    main()
