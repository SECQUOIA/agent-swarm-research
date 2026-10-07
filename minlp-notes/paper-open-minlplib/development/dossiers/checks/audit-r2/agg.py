import json, math
from fractions import Fraction as F
P = {r['name']: r for r in json.load(open('pages.json'))}
solu = {}
for line in open('minlplib.solu'):
    t = line.split()
    if len(t) >= 2:
        solu.setdefault(t[1], {})[t[0]] = t[2] if len(t) > 2 else None
def fr(s):
    try: v = float(s)
    except Exception: return None
    return F(s) if math.isfinite(v) else None
# proven exactly feasible objective upper ends (min instances): audit enclosures / exact values
proven = {
 'glider100': '-983842.2577716', 'topopt-cantilever_60x40_50': '10.33547432781', 'methanol50': '0.007930218899920',
 'sssd20-04persp': '347691.4104845', 'sssd22-08persp': '508713.7310120', 'sssd25-04persp': '300176.5636663',
 'sssd25-08persp': '472093.0779707', 'ghg_3veh': '7.754006050065', 'nuclear14': '-1.129687441170',
 'nd_netgen-2000-3-4-b-a-ns_7': '10729657.58532', 'smallinvDAXr1b150-165': '88.10493476001',
 'smallinvDAXr2b150-165': '88.10493476001', 'smallinvDAXr1b200-220': '156.604267884', 'smallinvDAXr2b200-220': '156.604267884',
 'watercontamination0303': '207.9850348024', 'eniplac': '-132117.0830141', 'lop97icx': '4099.059953601',
 'spring': '0.8462456656432', 'stockcycle': '119948.6883334',
 'rocket100': '-1.0128320069130', 'rocket200': '-1.0128356770677', 'rocket400': '-1.0128365294822'}
for n, f in proven.items():
    r = P[n]; f = F(f)
    assert r['sense'] == 'min'
    ds = sorted([(fr(d['value']), d['solver']) for d in r['duals'] if fr(d['value']) is not None], key=lambda x: -x[0])
    third = ds[2] if len(ds) >= 3 else None
    s = solu.get(n, {})
    agg_key = [k for k in s if k in ('=opt=', '=bestdual=')]
    agg = F(s[agg_key[0]]) if agg_key else None
    bold = [(str(d['value']), d['solver']) for d in r['duals'] if d['bold']]
    print(f"{n:28s} S={'S' if r['solved'] else '-'} ndual={len(ds)} third={None if third is None else (float(third[0]), third[1])} "
          f"solu={agg_key[0] if agg_key else s} {None if agg is None else float(agg)} "
          f"third-f={"n/a" if third is None else "%.3g" % float(third[0]-f)} agg-f={"n/a" if agg is None else "%.3g" % float(agg-f)}")
