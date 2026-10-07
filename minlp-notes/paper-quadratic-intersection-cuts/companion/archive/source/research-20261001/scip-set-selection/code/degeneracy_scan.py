"""Per-instance dual degeneracy of SCIP's root intersection-cut corners (SCIP's rule, seed 0).

For each instance: one root run with nlhdlr/quadratic/dumpfile (SCIP's own lambda, setrule 0), then a summary of
the dumped corners: number of corners, mean share of rays with zero reduced cost (|w_j| <= 1e-9 max_j |w_j|), share
of corners whose single-cut criterion min_j wt_j alpha_j (wt = w floored at 1e-6 max w) is attained at a zero-cost
ray, share of corners with dim(lambda) >= 2 (where a rule can change lambda), and share of corners where every ray
has zero reduced cost.  The dump is deleted afterwards;
only the summary line is kept (one JSON object per instance, appended to OUT; finished instances are skipped).

Usage: python3 degeneracy_scan.py INSTLIST OUT.jsonl TMPDIR
"""
from pathlib import Path as _PublicPath
_PUBLIC_HOME = str(_PublicPath.home())

import sys, os, json, subprocess
import numpy as np

B = (_PUBLIC_HOME + '/build-scip/selection/build-lapack/bin/scip')
O = os.path.expanduser('~/.cache/minlplib/minlplib/osil')


def summarize(path):
    n = 0; zs = []; att = 0; dim2 = 0; allz = 0
    with open(path) as f:
        for l in f:
            d = json.loads(l.replace('-nan', 'NaN').replace('nan', 'NaN'))
            if d['type'] != 'corner' or not d['w']:
                continue
            w = np.array(d['w']); a = np.array(d['alpha0'], float); a[a < 0] = np.inf
            zero = w <= 1e-9 * max(w.max(), 1e-300)
            wt = np.maximum(w, 1e-6 * max(w.max(), 1e-9))
            v = np.where(np.isfinite(a), wt * a, np.inf)
            n += 1; zs.append(float(zero.mean())); dim2 += d['dim'] >= 2; allz += bool(zero.all())
            if np.isfinite(v.min()) and zero[int(np.argmin(v))]:
                att += 1
    return dict(corners=n, zero_share=float(np.mean(zs)) if zs else None, crit_at_zero=att / n if n else None,
                dim2_share=dim2 / n if n else None, allzero_share=allz / n if n else None)


def main():
    insts = [l.strip() for l in open(sys.argv[1]) if l.strip()]
    out, tmp = sys.argv[2], sys.argv[3]
    os.makedirs(tmp, exist_ok=True)
    done = set()
    if os.path.exists(out):
        done = {json.loads(l)['inst'] for l in open(out) if l.strip()}
    for inst in insts:
        if inst in done:
            continue
        dump = os.path.join(tmp, inst + '.jsonl')
        if os.path.exists(dump):
            os.remove(dump)
        cmd = ('set nlhdlr quadratic useintersectioncuts TRUE set nlhdlr quadratic dumpfile %s set limits nodes 1 '
               'set limits time 120 set timing clocktype 1 read %s/%s.osil opt quit' % (dump, O, inst))
        try:
            subprocess.run([B, '-c', cmd], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, timeout=400)
            rec = summarize(dump) if os.path.exists(dump) else dict(corners=0)
        except subprocess.TimeoutExpired:
            rec = dict(corners=None, timeout=True)
        rec['inst'] = inst
        if os.path.exists(dump):
            os.remove(dump)
        with open(out, 'a') as f:
            f.write(json.dumps(rec) + '\n')


if __name__ == '__main__':
    main()
