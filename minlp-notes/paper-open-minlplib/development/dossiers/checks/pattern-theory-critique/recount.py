# pattern-theory critique check (2026-10-04). Run from a scratch dir holding copies of the inputs
# (pages.json, fetched.json, candidates.json, census_merged.json from research-20260929; OSIL from ~/.cache/minlplib).
import json, math
from decimal import Decimal as D, InvalidOperation
P={r['name']:r for r in json.load(open('pages.json'))}
C={r['name']:r for r in json.load(open('census_merged.json'))}
F={r['name']:r for r in json.load(open('fetched.json'))}
def dec(x):
    try:
        v=D(str(x).strip())
        return v if v.is_finite() else None
    except Exception: return None
def bestp(r,tol=D('1e-8')):
    pts=[dec(p['value']) for p in r['points'] if dec(p['infeas']) is not None and dec(p['infeas'])<=tol and dec(p['value']) is not None]
    if not pts: return None
    return min(pts) if r['sense']=='min' else max(pts)
def bestd(r):
    ds=[dec(d['value']) for d in r['duals'] if dec(d['value']) is not None]
    if not ds: return None
    return max(ds) if r['sense']=='min' else min(ds)
def rg(p,d):
    if p is None or d is None: return math.inf
    if p==d: return 0.0
    if p*d<=0: return math.inf
    return float(abs(p-d)/min(abs(p),abs(d)))
nc=[n for n,r in P.items() if not r['convex']]
print('pages',len(P),'nonconvex',len(nc))
ns=[n for n in nc if not P[n]['solved']]; print('nonconvex unsolved',len(ns))
def wok(c):
    a,b,k=c.get('tw_fac_ub'),c.get('tw_nlprimal_ub'),c.get('n_nl') or 0
    return (a is not None and a<=16) or (b is not None and b<=6 and k>=50)
w=[n for n in ns if n in C and wok(C[n])]; print('width ok (census, unsolved, nonconvex by page)',len(w))
def mg(c):
    try: return float(c['gap'])
    except: return math.inf
g=[n for n in w if mg(C[n])>1e-4]; print('meta gap',len(g))
# rule set computed directly from census without solved filter
rule={n for n,c in C.items() if not c['convex'] and wok(c) and mg(c)>1e-4}
print('rule over census (no S filter)',len(rule),' S in rule:',[n for n in rule if P[n]['solved']])
cand={r['name'] for r in json.load(open('candidates.json'))}
first='lnts50 lnts100 lnts200 lnts400 camshape100 camshape200 camshape400 camshape800 dtoc5 lukvle10 optcdeg2'.split()
print('rule - cand == first?', sorted(rule-cand)==sorted(first), 'cand-rule',cand-rule)
op={n for n in rule if rg(bestp(P[n]),bestd(P[n]))>1e-4}
print('open',len(op),'open&cand',len(op&cand), 'open first', sorted(op&set(first)))
# scout keep vs mine
keep={n for n,r in F.items() if r['keep']}
print('scout keep',len(keep),'mine',len(op&cand),'sym diff',keep^(op&cand))
# bands
from collections import Counter
b=Counter()
for n in keep:
    r=P[n]; p=bestp(r); d=bestd(r)
    if p is None: b['nopoint']+=1; continue
    if d is None: b['nodual']+=1; continue
    x=rg(p,d)
    b['inf' if math.isinf(x) else '>=1' if x>=1 else '[.1,1)' if x>=.1 else '[.01,.1)' if x>=.01 else '(1e-4,.01)']+=1
print(dict(b), sum(b.values()))
# fct
print('missing from census', sorted(set(P)-set(C)))
r=P['fct']; print('fct', r['convex'], r['solved'], r['nvars'], repr(r['listing_dual']), repr(r['listing_primal']), [d['raw'] for d in r['duals']], [(p['value'],p['infeas']) for p in r['points']])
