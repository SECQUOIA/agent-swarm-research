"""Compare the exp/pow-audited rerun with the saved results and summarize the audit.

    python3 compare_audit.py [--out DIR] [--no-cover]

1. eg_disc2_s: every DIR/res/disc2_p<k>_c<c>.npz is compared with the saved eg-recheck result
   research-20260929/publication/eg-recheck/res/p<k>_c<c>.npz: leaf boxes (lo, hi), leaf kinds,
   the author's bounds (plb), the decisions (ok), the certificate codes (how) and the margins (mg)
   byte for byte; the certifier statistics, the smallest LP margin and the coverage flags exactly.
   A file from a sample run (batches given) is compared on its leaves only.
2. eg_int_s and eg_disc_s (the per-leaf results of the review were not saved, only its logs):
   (a) the regenerated recordings: their logs against the original run logs (run C:
       retry/logs/int9_final.log; run E: disc9_p0.log, disc9_p1.log), apart from timings;
   (b) the certification log against the review's verify_tree.py logs (verify_int.log,
       verify_disc_p0.log, verify_disc_p1.log): the part and coverage lines, the leaf counts, every
       progress line and the final line (certified count, failures, the full stats dict, the
       smallest LP margin), apart from timings.
3. All three instances (complete runs only), from the audited outputs themselves: every leaf of
   every part is in this run's outputs (the chunks' leaf indices together are exactly
   0 .. n_leaves - 1; item 4 checks that all of them are certified), the recheck's bookkeeping
   flags (cov_ok, no bad reduced box), an exact tree-free coverage proof of the leaves of each
   part (prove_cover, copied unchanged from review r1's own_cover.py), and the domain check
   against the GAMS bounds (all parts together).
4. Audit: results checked per call site, violations, flagged leaves; the number of leaves that
   are certified AND audit-clean; per output file, every call site was exercised and the number
   of audited exp results at tay_E0, nat_Elo and nat_Ehi equals pieces x rows x terms (so no
   piece escaped the audit).
The last line starts with 'RESULT:'.
"""
import argparse
import ast
import glob
import os
import re
import sys
from fractions import Fraction as Fr

import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
R = os.environ.get("EG_AUDIT_R") or os.path.normpath(os.path.join(HERE, "..", "..", "..", "research-20260929"))
ORIG_RES = os.path.join(R, "publication", "eg-recheck", "res")
RUN_LOGS = os.path.join(R, "open-instances-wave3", "eg", "retry", "logs")
REV_LOGS = os.path.join(R, "reviews", "eg-retry-review-checks", "logs")
sys.path.insert(0, os.path.join(HERE, "cert"))
from gms_model import GmsModel  # noqa: E402

NCH = {0: 4, 1: 5, 2: 6, 3: 7, 4: 7, 5: 5, 6: 3, 7: 1}
ARRAYS = ("sel", "ok", "mg", "how", "kind", "plb", "lo", "hi")
SCALARS = ("n_leaves", "chunk", "nchunks", "cov_ok", "nbad_red", "n_gen", "n_proc", "n_pre", "n_open", "n_tiny",
           "kind_counts", "part", "root_lo", "root_hi")
INTDISC = {"int": ("eg_int_s", "int9_final.log", "verify_int.log", None),
           "disc_p0": ("eg_disc_s", "disc9_p0.log", "verify_disc_p0.log", 0),
           "disc_p1": ("eg_disc_s", "disc9_p1.log", "verify_disc_p1.log", 1)}


# ------------------------------------------------------------------ coverage (review r1)
def prove_cover(lo, hi, isint, rlo, rhi):
    """copied unchanged from research-20260929/publication/reviews/eg-recheck-r1/own_cover.py"""
    n = len(lo)
    # leaves inside the root, nonempty, integral integer ends
    assert np.all(lo <= hi), "empty leaf"
    assert np.all(lo >= rlo) and np.all(hi <= rhi), "leaf outside root"
    ii = np.flatnonzero(isint)
    assert np.all(lo[:, ii] == np.round(lo[:, ii])) and np.all(hi[:, ii] == np.round(hi[:, ii]))
    stack = [(np.arange(n), rlo.copy(), rhi.copy())]
    nodes = 0
    maxdepth = 0
    depth_of = {0: 0}
    while stack:
        I, L, U = stack.pop()
        nodes += 1
        if len(I) == 1:
            j = I[0]
            if not (np.all(lo[j] <= L) and np.all(hi[j] >= U)):
                return False, f"leaf {j} does not contain its node box {L.tolist()} {U.tolist()}", nodes
            continue
        best = None
        m = len(I)
        for d in range(7):
            a = lo[I, d]
            order = np.argsort(a, kind="stable")
            a_s = a[order]
            cm = np.maximum.accumulate(hi[I, d][order])
            valid = (cm[:-1] < a_s[1:]) if isint[d] else (cm[:-1] <= a_s[1:])
            pos = np.flatnonzero(valid)
            if len(pos):
                j = pos[np.argmin(np.abs(pos - (m - 1) / 2))]
                score = abs(j - (m - 1) / 2)
                if best is None or score < best[0]:
                    best = (score, d, j, order, a_s[j + 1])
        if best is None:
            return False, f"no guillotine cut for a node with {m} leaves, box {L.tolist()} {U.tolist()}", nodes
        _, d, j, order, v = best
        Il, Ir = I[order[:j + 1]], I[order[j + 1:]]
        Ul = U.copy(); Ul[d] = v - 1 if isint[d] else v
        Lr = L.copy(); Lr[d] = v
        stack.append((Il, L.copy(), Ul))
        stack.append((Ir, Lr, U.copy()))
    return True, "covered", nodes


def gms_bounds(name):
    G = GmsModel(name)
    dv = [v for v in G.vars if v != "objvar"]
    return [G.lb[v] for v in dv], [G.ub[v] for v in dv], np.array([v in G.ints for v in dv])


def cover_and_domain(name, parts):
    """parts: one list of chunk results (npz) per part of instance name, all chunks present.
    Prints the checks of item 3 of the module docstring and returns the problems found."""
    problems = []
    lb, ub, isint = gms_bounds(name)
    ranges = []
    dom_ok = True
    for p, zs in enumerate(parts):
        n = int(zs[0]["n_leaves"])
        rlo, rhi = zs[0]["root_lo"], zs[0]["root_hi"]
        same = all(int(z["n_leaves"]) == n and same_bytes(z["root_lo"], rlo) and same_bytes(z["root_hi"], rhi)
                   for z in zs)
        sel = np.concatenate([z["sel"] for z in zs])
        all_leaves = same and np.array_equal(np.sort(sel), np.arange(n))
        book = all(bool(z["cov_ok"]) and int(z["nbad_red"]) == 0 for z in zs)
        okc, msg, nodes = prove_cover(np.concatenate([z["lo"] for z in zs]), np.concatenate([z["hi"] for z in zs]),
                                      isint, rlo, rhi)
        print(f"  {name} part {p}: every leaf of the part is in this run's outputs: {all_leaves} ({len(sel)} of {n}); "
              f"bookkeeping cov_ok and no bad reduced box: {book}; guillotine coverage proof: {okc} ({msg}; {nodes} nodes)")
        if not (all_leaves and book and okc):
            problems.append(f"coverage {name} part {p}")
        for i in range(len(lb)):
            if isint[i]:
                dom_ok &= rlo[i] == int(rlo[i]) and rhi[i] == int(rhi[i])
            else:
                dom_ok &= Fr(rlo[i]) <= lb[i] and Fr(rhi[i]) >= ub[i]
        ranges.append([(int(rlo[i]), int(rhi[i])) if isint[i] else None for i in range(len(lb))])
    for i in np.flatnonzero(isint):     # integer coordinates: the parts tile [lb, ub] exactly
        iv = sorted(r[i] for r in ranges)
        if len(set(iv)) == 1:
            dom_ok &= iv[0] == (lb[i], ub[i])
        else:
            dom_ok &= iv[0][0] == lb[i] and iv[-1][1] == ub[i] and all(
                iv[t + 1][0] == iv[t][1] + 1 for t in range(len(iv) - 1))
    print(f"  {name}: root boxes contain the GAMS continuous box and tile every integer range: {dom_ok}")
    if not dom_ok:
        problems.append(f"domain {name}")
    return problems


# ------------------------------------------------------------------ helpers
def norm(line):
    line = re.sub(r"\(\d+s\)", "(Ts)", line.rstrip())
    line = re.sub(r" t \d+s$", " t Ts", line)
    line = re.sub(r"time \d+s", "time Ts", line)
    line = re.sub(r", \d+s, stats", ", Ts, stats", line)
    return line


def run_lines(path):
    return [norm(x) for x in open(path) if x.startswith(("== ", "  it ", "B&B:", "  certified lower bound"))]


def verify_lines(path):
    keep = []
    for x in open(path):
        if x.startswith(("rec_", "  coverage:", "  leaves:", "    ", "  independent certification")) \
                and not x.startswith(("    failed leaf", "    audit violation")):
            keep.append(norm(x))
    return keep


def same_bytes(a, b):
    return a.dtype == b.dtype and a.shape == b.shape and a.tobytes() == b.tobytes()


SITES = {"nat_Elo", "nat_Ehi", "tay_E0", "tay_ell", "tau2", "tau3", "s2", "p2", "p3", "p4"}


class Audit:
    def __init__(self, name):
        self.checked, self.viol, self.leaves, self.ok, self.clean, self.flagged = {}, {}, 0, 0, 0, 0
        self.examples = []
        T = GmsModel(name).terms()
        self.terms_per_box = len(T) * len(T[0]["terms"])     # exp arguments per box and call: rows x terms
        self.bad_counts = []

    def add(self, z, label):
        chk = ast.literal_eval(str(z["audit_checked"]))
        # every certified piece had its exp results audited: one Taylor and one natural call per piece,
        # terms_per_box arguments each; every call site was exercised
        n_exp = ast.literal_eval(str(z["stats"]))["pieces"] * self.terms_per_box
        if not (set(chk) == SITES and chk["tay_E0"] == chk["nat_Elo"] == chk["nat_Ehi"] == n_exp):
            self.bad_counts.append(label)
        for k, v in chk.items():
            self.checked[k] = self.checked.get(k, 0) + v
        for k, v in ast.literal_eval(str(z["audit_viol"])).items():
            self.viol[k] = self.viol.get(k, 0) + v
        ok, abad = z["ok"], z["abad"]
        self.leaves += len(ok)
        self.ok += int(ok.sum())
        self.flagged += int(abad.sum())
        self.clean += int((ok & ~abad).sum())
        self.examples += ast.literal_eval(str(z["audit_examples"]))[:5]


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--out", default=os.path.join(HERE, "out"))
    ap.add_argument("--no-cover", action="store_true", help="skip the guillotine coverage proofs")
    a = ap.parse_args()
    OUT = os.path.abspath(a.out)
    problems, missing = [], []
    AU = {name: Audit(name) for name in ("eg_int_s", "eg_disc_s", "eg_disc2_s")}
    full = {"eg_int_s": True, "eg_disc_s": True, "eg_disc2_s": True}

    # ---------------- 1. eg_disc2_s
    print("== eg_disc2_s: audited chunks vs eg-recheck/res (byte-for-byte)")
    n_cmp = 0
    disc2_parts = []
    for k in range(8):
        disc2_parts.append([])
        for c in range(NCH[k]):
            f = os.path.join(OUT, "res", f"disc2_p{k}_c{c}.npz")
            if not os.path.exists(f):
                missing.append(f"disc2_p{k}_c{c}")
                full["eg_disc2_s"] = False
                continue
            z, o = np.load(f), np.load(os.path.join(ORIG_RES, f"p{k}_c{c}.npz"))
            sample = str(z["batches"]) != "all"
            full["eg_disc2_s"] &= not sample
            if sample:
                pos = np.searchsorted(o["sel"], z["sel"])
                assert np.all(o["sel"][pos] == z["sel"])
            else:
                pos = np.arange(len(o["sel"]))
            bad = [key for key in ARRAYS if not same_bytes(o[key][pos], z[key])]
            bad += [key for key in SCALARS if not same_bytes(np.asarray(o[key]), np.asarray(z[key]))]
            if not sample:
                bad += [key for key in ("stats",) if str(o[key]) != str(z[key])]
                mo, mz = float(o["min_lp_margin"]), float(z["min_lp_margin"])
                if not (mo == mz or (np.isnan(mo) and np.isnan(mz))):
                    bad.append("min_lp_margin")
            AU["eg_disc2_s"].add(z, f"disc2_p{k}_c{c}")
            disc2_parts[k].append(z)
            n_cmp += len(z["sel"])
            tag = f"sample of {len(z['sel'])} leaves (batches {z['batches']})" if sample else f"all {len(z['sel'])} leaves"
            print(f"  p{k}_c{c}: {tag}: {'identical' if not bad else 'DIFFERENT: ' + ', '.join(bad)}; "
                  f"audit flagged {int(z['abad'].sum())}")
            if bad:
                problems.append(f"disc2_p{k}_c{c} differs in {bad}")
    print(f"  compared {n_cmp} leaves of eg_disc2_s")

    # ---------------- 2. eg_int_s, eg_disc_s
    for job, (name, runlog, verlog, part) in INTDISC.items():
        print(f"== {name} {job}")
        rl = os.path.join(OUT, "logs", f"record_{job}.log")
        if os.path.exists(rl) and any(x.startswith("recorded") for x in open(rl)):
            A_, B_ = run_lines(os.path.join(RUN_LOGS, runlog)), run_lines(rl)
            same = A_ == B_
            print(f"  recording vs original run log {runlog}: {len(A_)} / {len(B_)} lines, identical apart from timings: {same}")
            if not same:
                problems.append(f"recording {job} differs from {runlog}")
        else:
            missing.append(f"record_{job}")
        f = os.path.join(OUT, "res", f"{job}.npz")
        cl = os.path.join(OUT, "logs", f"cert_{job}.log")
        if not os.path.exists(f):
            missing.append(f"cert_{job}")
            full[name] = False
            continue
        z = np.load(f)
        sample = str(z["batches"]) != "all"
        full[name] &= not sample
        AU[name].add(z, job)
        if sample:
            print(f"  sample run (batches {z['batches']}): {len(z['sel'])} leaves; not comparable with the review's "
                  f"whole-tree log (use tests/sample_test.py)")
        else:
            A_, B_ = verify_lines(os.path.join(REV_LOGS, verlog)), verify_lines(cl)
            same = A_ == B_
            print(f"  certification vs review log {verlog}: {len(A_)} / {len(B_)} lines, identical apart from timings: {same}")
            if not same:
                problems.append(f"cert {job} differs from {verlog}")
                for x, y in zip(A_, B_):
                    if x != y:
                        print("    first difference:\n    review:", x, "\n    audit: ", y)
                        break
            print(f"  {B_[-1].strip()[:200]}")
    # ---------------- 3. every leaf certified, coverage and domain (complete runs only)
    if not a.no_cover:
        print("== coverage and domain (from the audited outputs)")
        for name, jobs_ in (("eg_int_s", ["int"]), ("eg_disc_s", ["disc_p0", "disc_p1"])):
            files = [os.path.join(OUT, "res", f"{j}.npz") for j in jobs_]
            if full[name] and all(os.path.exists(f) for f in files):
                problems += cover_and_domain(name, [[np.load(f)] for f in files])
        if full["eg_disc2_s"]:
            problems += cover_and_domain("eg_disc2_s", disc2_parts)

    # ---------------- 4. audit summary
    print("== audit")
    tot_checked, tot_viol = 0, 0
    for name, A in AU.items():
        nchk = sum(A.checked.values())
        nv = sum(A.viol.values())
        tot_checked += nchk
        tot_viol += nv
        print(f"  {name}: leaves {A.leaves}, certified {A.ok}, flagged by the audit {A.flagged}, "
              f"certified and audit-clean {A.clean}; results checked {nchk} {A.checked}; violations {nv} {A.viol}")
        for e in A.examples[:5]:
            print("    example violation (site, x, y):", e)
        if A.flagged or nv or A.ok != A.leaves:
            problems.append(f"audit/certification {name}: flagged {A.flagged}, violations {nv}, uncertified {A.leaves - A.ok}")
        print(f"    every piece's exp results audited and every call site exercised: {not A.bad_counts}"
              + (f" (not in {A.bad_counts})" if A.bad_counts else ""))
        if A.bad_counts:
            problems.append(f"audit counts {name}: {A.bad_counts}")
    complete = not missing and all(full.values())
    if missing:
        print(f"  missing outputs: {missing}")
    verdict = "PASS" if not problems else "PROBLEMS: " + "; ".join(problems)
    scope = "complete run" if complete else "PARTIAL/SAMPLE run"
    if a.no_cover:
        scope = "coverage NOT checked (--no-cover); " + scope.replace("complete run", "all outputs present")
    print(f"RESULT: {verdict} ({scope}; {sum(A.leaves for A in AU.values())} leaves compared or checked; "
          f"{tot_checked} exp/power results audited, {tot_viol} violations)")
    return 0 if not problems else 1


if __name__ == "__main__":
    sys.exit(main())
