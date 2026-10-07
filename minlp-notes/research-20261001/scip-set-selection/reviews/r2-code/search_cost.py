"""Review r2 (m6): per-search and per-generated-cut cost of the lambda search, from raw seed-0 root logs.

Own parser. The 251-instance set: root finished (not time-limited) in all seven settings,
reference in minlplib.solu (=opt= or =best=), and |z_ref - z_LP1| > 1e-6 max(1, |z_ref|).
"""
import re
from pathlib import Path

BASE = Path(__file__).resolve().parents[2]
SETTINGS = ['off', 'scip', 'corner', 'eff', 'scipS', 'cornerS', 'effS']
inst = (BASE / 'logs/testset_root.txt').read_text().split()
solu = {}
for l in (BASE / 'sources/minlplib.solu').read_text().splitlines():
    f = l.split()
    if len(f) >= 3 and f[0] in ('=opt=', '=best='):
        solu[f[1]] = float(f[2])


def parse(p):
    if not p.exists():
        return None
    t = p.read_text(errors='replace')
    st = re.search(r'^SCIP Status\s*: (.*)$', t, re.M)
    fl = re.search(r'^  First LP value\s*: (\S+)', t, re.M)
    ss = re.search(r'^  Quadratic SetSel :\s+(\S+)\s+(\d+)\s+(\d+)\s+(\d+)\s+(\d+)\s+(\S+)\s+(\S+)\s+(\S+)', t, re.M)
    qn = re.search(r'^  Quadratic Nlhdlr :\s+(\d+)\s+(\d+)', t, re.M)
    return dict(status=st.group(1) if st else None, firstlp=float(fl.group(1)) if fl else None,
                calls=int(ss.group(2)) if ss else 0, changed=int(ss.group(3)) if ss else 0,
                evals=int(ss.group(5)) if ss else 0,
                itime=float(ss.group(7)) if ss else 0.0, stime=float(ss.group(8)) if ss else 0.0,
                gen=int(qn.group(1)) if qn else 0)


R = {(i, s): parse(BASE / f'logs/root/{i}.{s}.s0.log') for i in inst for s in SETTINGS}
complete = [i for i in inst if all(R[i, s] and R[i, s]['status'] and 'time limit' not in R[i, s]['status'] for s in SETTINGS)]
comp = [i for i in complete if i in solu and R[i, 'scip']['firstlp'] is not None
        and abs(solu[i] - R[i, 'scip']['firstlp']) > 1e-6 * max(1, abs(solu[i]))]
print(f'root instances {len(inst)}, complete in all 7 settings {len(complete)}, with defined RGC {len(comp)}')
allinst = [i for i in inst]
for s in ('corner', 'eff'):
    for label, pop in (('251 RGC set', comp), ('all seed-0 root logs', allinst)):
        rs = [R[i, s] for i in pop if R[i, s]]
        calls = sum(r['calls'] for r in rs); ch = sum(r['changed'] for r in rs)
        st = sum(r['stime'] for r in rs); gen = sum(r['gen'] for r in rs)
        ev = sum(r['evals'] for r in rs)
        nch = sum(1 for r in rs if r['changed'] > 0)
        print(f'{s:6s} {label:22s}: logs {len(rs)} searches {calls} changed {ch} ({ch / max(calls, 1):.3%}) '
              f'gen cuts {gen} searches/gen {calls / max(gen, 1):.3f} evals {ev} select time {st:.2f} s -> '
              f'{1e3 * st / max(calls, 1):.3f} ms/search, {1e3 * st / max(gen, 1):.3f} ms/gen cut; instances with a change {nch}')
    rs = [R[i, s] for i in comp]
    print(f'   r1 mixing: {s} 251-set select time / all-log searches = '
          f'{1e3 * sum(r["stime"] for r in rs) / sum(R[i, s]["calls"] for i in allinst if R[i, s]):.3f} ms')

# Variant: the note's 251 may exclude instances where SCIP's first LP equals the reference after
# presolve or where the root solved the problem; try excluding root-solved instances.
comp2 = [i for i in comp if not any('optimal' in R[i, s]['status'] for s in SETTINGS)]
print(f'excluding root-solved instances: {len(comp2)}')
for s in ('corner', 'eff'):
    rs = [R[i, s] for i in comp2]
    calls = sum(r['calls'] for r in rs); st = sum(r['stime'] for r in rs); gen = sum(r['gen'] for r in rs)
    print(f'  {s}: searches {calls} gen {gen} select {st:.2f} s -> {1e3 * st / calls:.3f} ms/search, {1e3 * st / gen:.3f} ms/gen cut')
