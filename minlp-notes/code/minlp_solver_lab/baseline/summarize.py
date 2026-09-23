"""Summarize baseline/out/*.txt (modelstat, solvestat, objval, objest, resusd, nodes)."""
import csv, glob, os, collections, math, sys
rows = {}
for f in glob.glob('baseline/out/*.txt'):
    name = os.path.basename(f)[:-4]
    inst, solver = name.rsplit('.', 1)
    parts = open(f).read().strip().split(',')
    try:
        ms, ss = int(parts[0]), int(parts[1])
        ov = float(parts[2]) if parts[2] not in ('NA', '') else math.nan
        oe = float(parts[3]) if parts[3] not in ('NA', '') else math.nan
        ru = float(parts[4]) if parts[4] not in ('NA', '') else math.nan
    except Exception:
        ms = ss = -1; ov = oe = ru = math.nan
    rows[(inst, solver)] = dict(ms=ms, ss=ss, obj=ov, est=oe, time=ru)
insts = sorted({k[0] for k in rows}); solvers = sorted({k[1] for k in rows})
# best known objective per instance from instancedata (primalbound)
import csv
meta = {r['name']: r for r in csv.DictReader(open('instances/instancedata.csv'), delimiter=';')}
def solved(r, inst):
    """optimal (ms 1) or integer solution with gap closed: |obj-est|<=1e-4|obj|+1e-6 and ss normal"""
    if r['ss'] not in (1,) : return False
    if r['ms'] == 1: return True
    if r['ms'] in (2, 8) and not math.isnan(r['est']) and abs(r['obj'] - r['est']) <= 1e-4 * abs(r['obj']) + 1e-6: return True
    return False
print(f"{'solver':10s} {'runs':>5s} {'solved':>6s} {'feasible':>8s} {'mean_time_solved':>16s}")
for s in solvers:
    rs = [(i, rows[(i, s)]) for i in insts if (i, s) in rows]
    n = len(rs); ns = sum(1 for i, r in rs if solved(r, i)); nf = sum(1 for i, r in rs if not math.isnan(r['obj']) and r['ms'] in (1, 2, 8))
    mt = [r['time'] for i, r in rs if solved(r, i) and not math.isnan(r['time'])]
    print(f"{s:10s} {n:5d} {ns:6d} {nf:8d} {sum(mt)/len(mt) if mt else float('nan'):16.2f}")
# instances unsolved by all
alls = [i for i in insts if all((i, s) in rows for s in solvers)]
print('instances with all solvers run:', len(alls))
un = [i for i in alls if not any(solved(rows[(i, s)], i) for s in solvers)]
print('unsolved by every solver within limit:', len(un), un[:40])
# disagreements: solvers claiming optimal with objective differing > 1e-4 rel
dis = []
for i in alls:
    opt = [(s, rows[(i, s)]['obj']) for s in solvers if solved(rows[(i, s)], i)]
    if len(opt) >= 2:
        vals = [v for s, v in opt]
        if max(vals) - min(vals) > 1e-4 * max(1, abs(min(vals))):
            dis.append((i, sorted(opt, key=lambda t: t[1])))
print('disagreements among "solved" claims:', len(dis))
for d in dis[:15]: print('  ', d[0], [(s, round(v, 6)) for s, v in d[1]])
