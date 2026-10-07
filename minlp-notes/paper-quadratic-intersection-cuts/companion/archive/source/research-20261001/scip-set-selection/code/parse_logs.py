"""Parse SCIP logs written by run_bench.py into one JSON record per run.

Usage: python3 parse_logs.py LOGDIR OUT.json
"""
import os, re, sys, json, gzip

NUM = r'([-+]?(?:\d+\.?\d*(?:[eE][-+]?\d+)?|inf(?:inity)?))'


def fnum(s):
    try:
        return float(s)
    except (TypeError, ValueError):
        return None


def parse(path):
    op = gzip.open if path.endswith('.gz') else open
    with op(path, 'rt', errors='replace') as f:
        txt = f.read()
    base = os.path.basename(path).replace('.gz', '')
    inst, setting, seed = base[:-4].rsplit('.', 2)
    r = dict(inst=inst, setting=setting, seed=int(seed[1:]), log=base)
    m = re.findall(r'SCIP Status\s+: (.*)', txt)
    r['status'] = m[-1].strip() if m else None
    for key, pat in [('time', r'Solving Time \(sec\)\s*:\s*' + NUM), ('nodes', r'Solving Nodes\s*:\s*(\d+)'),
                     ('primal', r'\nPrimal Bound\s*:\s*' + NUM), ('dual', r'\nDual Bound\s*:\s*' + NUM),
                     ('firstlp', r'First LP value\s*:\s*' + NUM), ('rootdual', r'Final Dual Bound\s*:\s*' + NUM),
                     ('wall', r'@@ wallclock ' + NUM)]:
        m = re.findall(pat, txt)
        r[key] = fnum(m[-1]) if m else None
    m = re.findall(r'@@ wallclock \S+ returncode (\S+)', txt)
    r['returncode'] = m[-1] if m else None
    m = re.findall(r'\nGap\s*:\s*(\S+)', txt)
    r['gap'] = m[-1] if m else None
    m = re.findall(r'  Quadratic Nlhdlr :\s+(\d+)\s+(\d+)\s+(\d+)\s+(\d+)\s+(\d+)\s+(\d+)\s+(\d+)\s+(\d+)\s+(\d+)', txt)
    if m:
        g = m[-1]
        r.update(gencuts=int(g[0]), addcuts=int(g[1]), nlargere=int(g[3]), abrtbadray=int(g[4]),
                 abrtposphi=int(g[5]), abrtnonbas=int(g[6]), nstrength=int(g[7]), nmonoidal=int(g[8]))
    m = re.findall(r'  Quadratic SetSel :\s+(\d+)\s+(\d+)\s+(-?\d+)\s+(\d+)\s+(\d+)\s+' + NUM + r'\s+' + NUM + r'\s+' + NUM
                   + r'\s+(\d+)\s+(\d+)\s+(\d+)(?:[ \t]+(\d+))?', txt)
    if m:
        g = m[-1]
        r.update(rule=int(g[0]), selcalls=int(g[1]), selchanged=int(g[2]), selfail=int(g[3]), selevals=int(g[4]),
                 selgain=fnum(g[5]), intercuttime=fnum(g[6]), seltime=fnum(g[7]), applied=int(g[8]),
                 active=int(g[9]), rootapplied=int(g[10]), degskip=int(g[11]) if g[11] else None)
    m = re.findall(r'\n  quadratic\s+:\s+(\d+)\s+(\d+)\s+' + NUM + r'\s+(\d+)\s+' + NUM + r'\s+(\d+)\s+' + NUM +
                   r'\s+(\d+)\s+(\d+)\s+(\d+)\s+' + NUM + r'\s+(\d+)', txt)
    if m:
        g = m[-1]
        r.update(nlq_detects=int(g[0]), nlq_enforce=int(g[9]), nlq_enfotime=fnum(g[10]), nlq_cuts=int(g[11]))
    m = re.findall(r'\n  nonlinear\s+:\s+(\d+)\s+(\d+)\s+(\d+)\s+(\d+)\s+(\d+)\s+(\d+)\s+(\d+)\s+(\d+)\s+(\d+)\s+(\d+)'
                   r'\s+(\d+)\s+(\d+)\s+(\d+)', txt)
    if m:
        g = m[-1]
        r.update(nl_cuts=int(g[11]), nl_applied=int(g[12]))
    r['error'] = bool(re.search(r'\[.*ERROR|^ERROR|violates the debugging solution|SIGSEGV|Segmentation|Aborted|'
                                r'memory limit reached', txt, re.M))
    r['debugsol_violation'] = 'debugging solution' in txt and 'violat' in txt
    return r


if __name__ == '__main__':
    d, out = sys.argv[1], sys.argv[2]
    recs = [parse(os.path.join(d, f)) for f in sorted(os.listdir(d)) if f.endswith('.log') or f.endswith('.log.gz')]
    json.dump(recs, open(out, 'w'), indent=0)
    print(len(recs), 'records')
