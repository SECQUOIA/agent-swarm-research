import sys,json,pandas as pd,numpy as np
from collections import Counter
sys.path.insert(0,'/tmp/scout'); from fam import family
o=pd.read_csv('/tmp/scout/open.csv'); o['fam']=o.name.map(family)
S={}
for l in open('/tmp/scout/struct.jsonl'):
    r=json.loads(l); S[r['name']]=r
for f,g in sorted(o.groupby('fam'),key=lambda x:-len(x[1])):
    print('='*100); print(f, 'n=',len(g), 'gap median=%.3g'%g.gap.median(), 'n_inf=',int(np.isinf(g.gap).sum()))
    ac=Counter(); rs=Counter(); keys=['nvars','nbin','ncons','nlvars','nlbin','nl_unbounded','nleq','nlin','bilin_edges','maxdeg','multi_atom_vars','bigm_rows']
    agg={k:[] for k in keys}; objnl=0
    for n in g.name:
        r=S.get(n,{})
        if 'err' in r: continue
        for a,c in r['atoms']: ac[a]+=c
        for a,c in r['rowsigs']: rs[a]+=c
        for k in keys: agg[k].append(r[k])
        objnl+=r['objnl']
    print(' medians:',{k:int(np.median(v)) if v else None for k,v in agg.items()},'objnl',objnl)
    print(' atoms:',ac.most_common(10))
    print(' rows:',[ (a[:90],c) for a,c in rs.most_common(6)])
    print(' names:',' '.join(f'{n}({gp:.2g})' for n,gp in zip(g.name,g.gap)))
