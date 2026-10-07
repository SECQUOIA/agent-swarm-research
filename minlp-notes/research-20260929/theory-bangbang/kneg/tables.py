"""Markdown tables for kappa-negative.md from the JSON logs (no computation).
usage: python3 tables.py two|kink|close|close_compact|row|n2lift|sweep"""
import json
import os
import sys

LOG = os.path.join(os.path.dirname(os.path.abspath(__file__)), "logs")


def load(name):
    with open(os.path.join(LOG, f"{name}.json")) as f:
        return json.load(f)


def two():
    print("| `kappa` | `(t_1, t_2)` | `ell` | `N` | switching stages | fractional (`u`) | plain gap `/h^2` | certificate |")
    print("|---|---|---|---|---|---|---|---|")
    for r in load("two"):
        if "kappa" not in r:
            continue
        frac = ", ".join(f"{t} ({u:.3f})" for t, u in zip(r["frac"], r["u_frac"])) or "none"
        if r["exact_gap_zero"]:
            cert = "exact, no window"
        elif "cert_ok" in r:
            inc = ""
            if r.get("incumbent_improved"):
                inc = (f"; better point found: `J - J(zbar)` = {r['incumbent_J_minus_J_over_h2']:.4f} `h^2`, "
                       f"fractional {r['incumbent_frac']} ({r['incumbent_u_frac'][0]:.4f}), monotone")
            cert = f"{'exact' if r['cert_ok'] else 'FAILED'}, {r['cert_nodes']} nodes ({r['cert_leaves']} leaves){inc}"
        else:
            cert = "not run (`N` > 2000)"
        fails = "; ".join(f"{t}: {v:.4f}" for t, v in r["failing"])
        gap = f"{r['gap_over_h2']:.4f}" + (f" ({fails})" if fails else "")
        print(f"| {r['kappa']:+.1f} | ({r['t1']}, {r['t2']}) | {r['ell']:.3f} | {r['N']} | {r['switch_stages']} | {frac} | {gap} | {cert} |")


def kink():
    print("| `(t_1, t_2)` | `ell` | `N` | fractional | failing stages (loss `/h^3`) | window deficits `/h^3`, `K = 0, 1, 2` |")
    print("|---|---|---|---|---|---|")
    for r in load("kink"):
        fails = "; ".join(f"{t}: {v:.4f}" for t, v in r["failing"]) or "none"
        wins = "; ".join(f"{t}: " + ", ".join(f"{v:.3g}" for v in w) for t, w in r["window_deficits_over_h3_K012"].items()) or "—"
        print(f"| ({r['t1']}, {r['t2']}) | {r['ell']:.3f} | {r['N']} | {r['frac']} | {fails} | {wins} |")


def close():
    print("| `kappa_1 -> kappa_2` | `(t_1, t_2)` | `ell` | predicted `eta^X_1` | `N` | fractional | recursion breaks at (time - `tau_1`) |")
    print("|---|---|---|---|---|---|---|")
    for r in load("close"):
        if "N" not in r or "eta_X_pred" not in r:
            print(f"| {r} |")
            continue
        br = "never" if r["break_stage"] is None else f"stage {r['break_stage']} ({r['break_minus_tau1']:+.4f})"
        if r["break_stage"] is None and "max_stage_loss_float" in r:
            br += f"; max stage loss {r['max_stage_loss_float']:.1e}"
        print(f"| {r['kappa1']:+.1f} -> {r['kappa2']:+.1f} | ({r['t1']}, {r['t2']}) | {r['ell']:.3f} | {r['eta_X_pred']:+.3f} | {r['N']} | {r['frac']} | {br} |")


def _z(v):
    return 0.0 if v == 0 else v


def close_compact():
    """One row per configuration (close and close2): break position per N, in stages from the first
    switching stage when known."""
    groups = {}
    for name in ("close", "close2"):
        for r in load(name):
            if "N" not in r:
                continue
            key = (_z(r["kappa1"]), _z(r["kappa2"]), r["t1"], r["t2"])
            groups.setdefault(key, []).append(r)
    print("| `kappa_1 -> kappa_2` | `(t_1, t_2)` | `ell` | predicted `eta^X_1` | `N` = 1000 | 2000 | 4000 | 8000 |")
    print("|---|---|---|---|---|---|---|---|")
    for key, rs in groups.items():
        r0 = rs[0]
        cells = []
        for r in sorted(rs, key=lambda q: q["N"]):
            if r["break_stage"] is None:
                cells.append("no break")
            elif r.get("break_minus_s1_stages") is not None:
                cells.append(f"break at `s_1{r['break_minus_s1_stages']:+d}`")
            else:
                cells.append(f"break at `t = {r['break_time']:.4f}`")
        print(f"| {key[0]:+.1f} -> {key[1]:+.1f} | ({key[2]}, {key[3]}) | {r0['ell']:.3f} | {r0['eta_X_pred']:+.3f} | " + " | ".join(cells) + " |")


def row():
    print("| `kappa` | `N` | fractional (`u`) | plain gap `/h^2` (exact) | `eta_hat_1`, row (`P_N = +inf`) | `eta_hat_1`, free end | recursion break, row / free |")
    print("|---|---|---|---|---|---|---|")
    for r in load("row"):
        frac = ", ".join(f"{t} ({u:.3f})" for t, u in zip(r.get("frac", []), r.get("u_frac", []))) or "none"
        gap = f"{r['exact_gap_over_h2']:.4f}" if "exact_gap_over_h2" in r else "—"
        e1 = f"{r['eta_hat_1']:.4f}" if r.get("eta_hat_1") is not None else "—"
        e2 = f"{r['free_eta_hat_1']:.4f}" if r.get("free_eta_hat_1") is not None else "—"
        print(f"| {r['kappa']:+.1f} | {r['N']} | {frac} | {gap} | {e1} | {e2} | {r.get('rmax_break')} / {r.get('free_break', '—')} |")


def n2lift():
    for r in load("n2lift"):
        if "V" not in r:
            print(f"| {r['N']} | none | — | — | — | transferred family exact |")
            continue
        fl = "; ".join(f"{t}: {v:.4f}" for t, v in r["failing"])
        outs = "; ".join(f"[{o['l']:.3f}, {o['r']:.3f}]: {o['bound_minus_J_over_h2']:+.4f}" for o in r["outer"]) or "—"
        print(f"| {r['N']} | {fl} | {r['u_n']:.4f} | [{r['V'][0]:.4f}, {r['V'][1]:.4f}] | {outs} | {'yes' if r['certified'] else 'no'} |")


def sweep():
    """Revision after review (F1): break position (stages from s1) per N, one row per configuration;
    then, per grid of the eta^X = -0.275 configuration, the second-switch type, e_2 and eta_hat_1."""
    rs = [r for r in load("sweep") if "N" in r]
    Ns = sorted({r["N"] for r in rs})
    groups = {}
    for r in rs:
        key = (_z(r.get("kappa1", -r.get("k1", 0))), _z(r.get("kappa2", -r.get("k2", 0))), r["t1"], r["t2"])
        groups.setdefault(key, {})[r["N"]] = r
    print("| `kappa_1 -> kappa_2` | `(t_1, t_2)` | `eta^X_1` | " + " | ".join(str(N) for N in Ns) + " |")
    print("|---|---|---|" + "---|" * len(Ns))
    for key, g in groups.items():
        eta = next(r["eta_X_pred"] for r in g.values() if "eta_X_pred" in r)
        cells = []
        for N in Ns:
            r = g.get(N)
            if r is None or "kkt" in r:
                cells.append("n/f")
            elif r["break_minus_s1"] is None:
                cells.append("—")
            else:
                cells.append(f"{r['break_minus_s1']:+d}")
        print(f"| {key[0]:+.1f} -> {key[1]:+.1f} | ({key[2]}, {key[3]}) | {eta:+.3f} | " + " | ".join(cells) + " |")
    print()
    for key, g in groups.items():
        print(f"configuration {key}")
        print("| `N` | second switch | `e_2` | `eta_hat_1` | `|sigma|/h` at `s_1 - 1, s_1, s_1 + 1` | break - `s_1` | break time - `theta_1` |")
        print("|---|---|---|---|---|---|---|")
        for N in Ns:
            r = g.get(N)
            if r is None or "kkt" in r:
                print(f"| {N} | KKT not found | | | | | |")
                continue
            sw2 = "fractional" if r["s2"] in r["frac"] else "vertex"
            e2 = "—" if r["e2"] is None else f"{r['e2']:+.3f}"
            e1 = "—" if r["eta_hat_1"] is None else f"{r['eta_hat_1']:+.3f}"
            br = "none" if r["break_minus_s1"] is None else f"{r['break_minus_s1']:+d}"
            bt = "—" if r["break_time_minus_theta1"] is None else f"{r['break_time_minus_theta1']:+.5f}"
            print(f"| {N} | {sw2} | {e2} | {e1} | {r['sig_over_h_s1m1_s1_s1p1']} | {br} | {bt} |")
        print()


if __name__ == "__main__":
    dict(two=two, kink=kink, close=close, close_compact=close_compact, row=row, n2lift=n2lift,
         sweep=sweep)[sys.argv[1]]()
