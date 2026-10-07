"""Sample test of the audited rerun: selected 512-leaf batches, audited vs the original code.

    python3 sample_test.py <workdir> <rec_int.npz> <rec_disc_p1.npz> plan|audit|ref|compare

Batches (each certified exactly as in a full run, so results are bit-comparable):
  eg_disc2_s: batch 0 of chunk 0 of every part, plus every batch that holds one of the 25 leaves
              with the smallest finite margin over all parts, or one of the 3 smallest in each of
              parts 0 and 2-7 (margins from the saved eg-recheck res/ files);
  eg_int_s, eg_disc_s part 1: batch 0, plus the batches that hold the 25 closed boxes with the
              smallest recorded author bound minus theta* (the tightest leaves; their certified
              margins are not saved anywhere).
Modes:
  plan    print the batches;
  audit   run cert/recheck_audit.py (audited) on them -> <workdir>/audit/*.npz;
  ref     run the same script with the certifier replaced by the ORIGINAL unaudited
          eg-recheck/margin_cert.py + reviews/eg-retry-review-checks/indep_cert.py (both copied
          unchanged into <workdir>/reflayout/) -> <workdir>/ref/*.npz;
  compare audited vs original (per leaf: ok, margin, certificate code, boxes; stats; smallest LP
          margin), eg_disc2_s also vs eg-recheck/res; audit violations; time per piece.
"""
import ast
import os
import shutil
import sys
import types

import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
A = os.path.normpath(os.path.join(HERE, ".."))
R = os.environ.get("EG_AUDIT_R") or os.path.normpath(os.path.join(A, "..", "..", "..", "research-20260929"))
RES = os.path.join(R, "publication", "eg-recheck", "res")
REC2 = os.path.join(R, "publication", "eg-recheck", "rec")
NCH = {0: 4, 1: 5, 2: 6, 3: 7, 4: 7, 5: 5, 6: 3, 7: 1}
TH = {"eg_int_s": "6.4531031529331155", "eg_disc_s": "5.760539610694994", "eg_disc2_s": "5.642100574331458"}


def plan(rec_int, rec_disc):
    jobs = []
    sel = {}
    allm = []
    for k in range(8):
        for c in range(NCH[k]):
            z = np.load(os.path.join(RES, f"p{k}_c{c}.npz"))
            mg = z["mg"]
            fin = np.flatnonzero(np.isfinite(mg))
            for pos in fin:
                allm.append((float(mg[pos]), k, c, int(pos // 512)))
    allm.sort()
    want = {(k, 0, 0) for k in range(8)}
    want |= {(k, c, b) for _, k, c, b in allm[:25]}
    for k in (0, 2, 3, 4, 5, 6, 7):
        want |= {(kk, c, b) for _, kk, c, b in [t for t in allm if t[1] == k][:3]}
    for k, c, b in sorted(want):
        sel.setdefault((k, c), set()).add(b)
    for (k, c), bs in sorted(sel.items()):
        jobs.append((f"disc2_p{k}_c{c}", os.path.join(REC2, f"rec_disc2_p{k}.npz"), "eg_disc2_s", c, NCH[k], sorted(bs)))
    for tag, rec, name in (("int", rec_int, "eg_int_s"), ("disc_p1", rec_disc, "eg_disc_s")):
        z = np.load(rec)
        plb = z["P_lb"][~z["P_keep"].astype(bool)]           # closed boxes come first in the leaf list
        tight = np.argsort(plb)[:25]
        jobs.append((tag, rec, name, 0, 1, sorted({0} | set(int(i // 512) for i in tight))))
    return jobs, allm[:5]


class _Dummy:
    n_checked, n_viol, examples = {}, {}, []


def ref_certifier(work):
    lay = os.path.join(work, "reflayout")
    pe = os.path.join(lay, "publication", "eg-recheck")
    rv = os.path.join(lay, "reviews", "eg-retry-review-checks")
    os.makedirs(pe, exist_ok=True)
    os.makedirs(os.path.join(rv, "data"), exist_ok=True)
    shutil.copy2(os.path.join(R, "publication", "eg-recheck", "margin_cert.py"), pe)
    for f in ("indep_cert.py", "gms_model.py"):
        shutil.copy2(os.path.join(R, "reviews", "eg-retry-review-checks", f), rv)
    for f in ("eg_int_s.gms", "eg_disc_s.gms", "eg_disc2_s.gms"):
        shutil.copy2(os.path.join(R, "reviews", "eg-retry-review-checks", "data", f), os.path.join(rv, "data"))
    sys.path.insert(0, pe)
    import margin_cert
    assert os.path.realpath(os.path.dirname(margin_cert.indep_cert.__file__)) == os.path.realpath(rv)

    class RefCert(margin_cert.MarginCertifier):
        """the original certifier; only adds the attributes recheck_audit.py reads (no effect on decisions)."""
        def __init__(self, *a, **k):
            super().__init__(*a, **k)
            self.viol_boxes = []
            self.M.audit = _Dummy()

        def certify_batch(self, lo, hi):
            ok = super().certify_batch(lo, hi)
            self.last_abad = np.zeros(len(lo), bool)
            return ok
    return RefCert


def run(work, jobs, mode):
    sys.path.insert(0, os.path.join(A, "cert"))
    import recheck_audit
    if mode == "ref":
        recheck_audit.Certifier = ref_certifier(work)
    out = os.path.join(work, mode)
    os.makedirs(out, exist_ok=True)
    for tag, rec, name, c, n, bs in jobs:
        f = os.path.join(out, tag + ".npz")
        sys.argv = ["recheck_audit.py", rec, name, TH[name], str(c), str(n), f, ",".join(map(str, bs))]
        stdout, sys.stdout = sys.stdout, open(f + ".log", "w")
        try:
            recheck_audit.main()
        finally:
            sys.stdout.close()
            sys.stdout = stdout
        z = np.load(f)
        print(f"  {mode} {tag}: {len(z['sel'])} leaves, {ast.literal_eval(str(z['stats']))['pieces']} pieces, "
              f"{float(z['time']):.1f}s, flagged {int(z['abad'].sum())}", flush=True)


def compare(work, jobs):
    bad = 0
    tot = {"audit": [0, 0.0], "ref": [0, 0.0]}
    nleaves = {}
    for tag, rec, name, c, n, bs in jobs:
        a, r = np.load(os.path.join(work, "audit", tag + ".npz")), np.load(os.path.join(work, "ref", tag + ".npz"))
        diff = [k for k in ("sel", "ok", "mg", "how", "kind", "plb", "lo", "hi") if a[k].tobytes() != r[k].tobytes()]
        diff += [k for k in ("stats",) if str(a[k]) != str(r[k])]
        if not (float(a["min_lp_margin"]) == float(r["min_lp_margin"]) or
                (np.isnan(float(a["min_lp_margin"])) and np.isnan(float(r["min_lp_margin"])))):
            diff.append("min_lp_margin")
        line = f"  {tag} batches {bs}: {len(a['sel'])} leaves; audited vs original: {'identical' if not diff else 'DIFFERENT ' + str(diff)}"
        if tag.startswith("disc2"):
            k = int(tag[7])
            o = np.load(os.path.join(RES, f"p{k}_c{c}.npz"))
            pos = np.searchsorted(o["sel"], a["sel"])
            d2 = [kk for kk in ("sel", "ok", "mg", "how", "kind", "plb", "lo", "hi") if o[kk][pos].tobytes() != a[kk].tobytes()]
            line += f"; vs eg-recheck/res: {'identical' if not d2 else 'DIFFERENT ' + str(d2)}"
            diff += d2
        fin = a["mg"][np.isfinite(a["mg"])]
        line += (f"; audit violations {ast.literal_eval(str(a['audit_viol'])) or 0}, flagged {int(a['abad'].sum())}; "
                 f"certified {int(a['ok'].sum())}; smallest margin {fin.min() if len(fin) else None:.3e}; "
                 f"min LP margin {float(a['min_lp_margin']):.3e}")
        print(line)
        bad += bool(diff) + int(a["abad"].sum()) + int((~a["ok"]).sum())
        nleaves[name] = nleaves.get(name, 0) + len(a["sel"])
        for m, z in (("audit", a), ("ref", r)):
            tot[m][0] += ast.literal_eval(str(z["stats"]))["pieces"]
            tot[m][1] += float(z["time"])
    ma, mr = 1e3 * tot["audit"][1] / tot["audit"][0], 1e3 * tot["ref"][1] / tot["ref"][0]
    print(f"  leaves per instance: {nleaves}")
    print(f"  time per piece: audited {ma:.2f} ms, original {mr:.2f} ms (audit overhead {ma - mr:.2f} ms, "
          f"{100 * (ma / mr - 1):.0f}%), over {tot['audit'][0]} pieces")
    print("SAMPLE TEST PASSED" if not bad else f"SAMPLE TEST FAILED ({bad})")
    return 1 if bad else 0


def main():
    work, rec_int, rec_disc, mode = sys.argv[1:5]
    os.makedirs(work, exist_ok=True)
    jobs, tight = plan(rec_int, rec_disc)
    if mode == "plan":
        for j in jobs:
            print(f"  {j[0]}: {j[2]} chunk {j[3]}/{j[4]} batches {j[5]}")
        print("  5 smallest finite eg_disc2_s margins (margin, part, chunk, batch):", tight)
        return 0
    if mode in ("audit", "ref"):
        run(work, jobs, mode)
        return 0
    return compare(work, jobs)


if __name__ == "__main__":
    sys.exit(main())
