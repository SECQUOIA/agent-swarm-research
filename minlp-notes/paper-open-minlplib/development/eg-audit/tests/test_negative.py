"""End-to-end negative tests: inject wrong exp / power results into the audited certifier and
check that the audit flags exactly the affected leaf, through the real chunk pipeline.

    python3 test_negative.py <rec_disc2_p1.npz> <tmpdir>

Each case runs cert/recheck_audit.py's main() in this process on batch 0 (512 leaves) of chunk 0
of 5 of eg_disc2_s part 1, with Model._aexp or Model._apow replaced by a version that multiplies
ONE result (box B of the first 64-box group, the first call at the given site, an argument that
is actually used) by (1 + rel) before the audit sees it.  Expected: leaf B, and only leaf B, is
flagged when |rel| > eps = 1e-14; nothing is flagged when |rel| = 3e-15 (below the audit's
acceptance threshold of about 7e-15).  The clean case must reproduce the saved eg-recheck
result for these leaves bit for bit.
Two more cases check the flag bookkeeping: an exp error in piece B of the first 64-piece group at
splitting depth 1 must flag exactly the leaf that owns that piece (the (B // 2)-th leaf that was
split), and an error at the per-call site s2 (S ** 2, perbox=False) must flag all 64 boxes of the
first group.
"""
import os
import sys

import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
CERT = os.path.normpath(os.path.join(HERE, "..", "cert"))
sys.path.insert(0, CERT)
import indep_cert_audit as ica  # noqa: E402
import margin_cert_audit as mca  # noqa: E402
import recheck_audit  # noqa: E402

R = os.environ.get("EG_AUDIT_R") or os.path.normpath(os.path.join(HERE, "..", "..", "..", "..", "research-20260929"))
ORIG = os.path.join(R, "publication", "eg-recheck", "res", "p1_c0.npz")
B = 5
fails = 0
ORIG_AEXP, ORIG_APOW = ica.Model._aexp, ica.Model._apow
ORIG_BATCH = mca.MarginCertifier._batch
DEPTH = [0]                     # splitting depth of the _batch call in progress


def _batch_depth(self, lo, hi, depth):
    DEPTH[0] = depth
    return ORIG_BATCH(self, lo, hi, depth)


mca.MarginCertifier._batch = _batch_depth


def check(cond, msg):
    global fails
    print(f"  {'ok  ' if cond else 'FAIL'} {msg}", flush=True)
    fails += not cond


def injector(kind, site, rel, depth=0):
    state = {"done": False}

    def pick(x):
        """an element of box B whose result is used: E0 >= -700 for tay_E0, Elo >= -700 for nat_Elo."""
        if site == "s2":
            return 0
        xb = np.asarray(x)[B].ravel()
        cand = np.flatnonzero(xb >= -700) if site in ("tay_E0", "nat_Elo", "nat_Ehi") else np.flatnonzero(xb > 0)
        return B * xb.size + int(cand[0])

    def aexp(self, x, s):
        y = np.exp(x)
        if kind == "exp" and s == site and DEPTH[0] == depth and not state["done"]:
            y = y.copy()
            y.flat[pick(x)] *= 1 + rel
            state["done"] = True
        self.audit.exp(x, y, s)
        return y

    def apow(self, x, k, s, perbox=True):
        y = x ** k
        if kind == "pow" and s == site and DEPTH[0] == depth and not state["done"]:
            y = y.copy()
            y.flat[pick(x)] *= 1 + rel
            state["done"] = True
        self.audit.pow(x, k, y, s, perbox)
        return y
    return aexp, apow, state


def run(rec, out, kind=None, site=None, rel=0.0, depth=0):
    if kind is None:
        ica.Model._aexp, ica.Model._apow = ORIG_AEXP, ORIG_APOW
        state = {"done": True}
    else:
        ica.Model._aexp, ica.Model._apow, state = injector(kind, site, rel, depth)
    sys.argv = ["recheck_audit.py", rec, "eg_disc2_s", "5.642100574331458", "0", "5", out, "0"]
    stdout = sys.stdout
    sys.stdout = open(out + ".log", "w")
    try:
        recheck_audit.main()
    finally:
        sys.stdout.close()
        sys.stdout = stdout
    return np.load(out), state["done"]


def main():
    rec, tmp = sys.argv[1], sys.argv[2]
    os.makedirs(tmp, exist_ok=True)
    o = np.load(ORIG)
    print("== clean run of batch 0 (512 leaves) of eg_disc2_s part 1 chunk 0")
    z, _ = run(rec, os.path.join(tmp, "clean.npz"))
    clean = z
    same = all(o[k][:512].tobytes() == z[k].tobytes() for k in ("sel", "ok", "mg", "how", "lo", "hi"))
    check(same, "decisions, margins, certificate codes and boxes identical to eg-recheck/res/p1_c0.npz")
    check(int(z["abad"].sum()) == 0 and str(z["audit_viol"]) == "{}", "no audit violation")
    cases = [("exp", "tay_E0", 2e-14), ("exp", "tay_E0", -1.2e-14), ("exp", "nat_Elo", 1e-13), ("exp", "nat_Ehi", -5e-14),
             ("exp", "tay_ell", 1.5e-14), ("pow", "p3", 2e-14), ("pow", "p4", -1e-12), ("pow", "tau3", 3e-14),
             ("pow", "tau2", 1.1e-14), ("pow", "p2", 2e-14)]
    for kind, site, rel in cases:
        z, injected = run(rec, os.path.join(tmp, f"{kind}_{site}_{rel:g}.npz"), kind, site, rel)
        flagged = np.flatnonzero(z["abad"])
        viol = eval(str(z["audit_viol"]))
        check(injected and list(flagged) == [B] and viol == {site: 1},
              f"{kind} at {site}, relative error {rel:g}: flagged leaves {list(flagged)}, violations {viol}")
    for kind, site, rel in (("exp", "tay_E0", 3e-15), ("exp", "nat_Ehi", -3e-15), ("pow", "p3", 3e-15)):
        z, injected = run(rec, os.path.join(tmp, f"small_{kind}_{site}.npz"), kind, site, rel)
        check(injected and int(z["abad"].sum()) == 0, f"{kind} at {site}, relative error {rel:g} (below eps): not flagged")
    split = np.flatnonzero(clean["how"] == 5)          # leaves certified after splitting, in order
    z, injected = run(rec, os.path.join(tmp, "depth1_tay_E0.npz"), "exp", "tay_E0", 2e-14, depth=1)
    flagged = np.flatnonzero(z["abad"])
    viol = eval(str(z["audit_viol"]))
    check(injected and list(flagged) == [split[B // 2]] and viol == {"tay_E0": 1},
          f"exp at tay_E0 in piece {B} at depth 1: flagged leaves {list(flagged)} (owner {split[B // 2]}), violations {viol}")
    z, injected = run(rec, os.path.join(tmp, "s2.npz"), "pow", "s2", 2e-14)
    flagged = np.flatnonzero(z["abad"])
    viol = eval(str(z["audit_viol"]))
    check(injected and list(flagged) == list(range(64)) and viol == {"s2": 1},
          f"pow at s2 (one value per call): flagged {len(flagged)} leaves ({flagged.min() if len(flagged) else None}"
          f"..{flagged.max() if len(flagged) else None}), violations {viol}")
    ica.Model._aexp, ica.Model._apow = ORIG_AEXP, ORIG_APOW
    print("ALL NEGATIVE TESTS PASSED" if not fails else f"NEGATIVE TESTS FAILED: {fails}")
    return 1 if fails else 0


if __name__ == "__main__":
    sys.exit(main())
