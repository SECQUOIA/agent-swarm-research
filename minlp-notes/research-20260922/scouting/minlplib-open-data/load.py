import pandas as pd, numpy as np, re
d=pd.read_csv('/tmp/instancedata.csv',sep=';')
def fam(n):
    n=n.lower()
    m=re.match(r'([a-z]+(?:_[a-z]+)*?)(?=[_\-]?\d|$)',n)
    return m.group(1) if m else n
d['family']=d.name.map(fam)
opcols=[c for c in d.columns if c.startswith('op')]
def ops(r):
    s=[c[2:] for c in opcols if r[c]==True or r[c]=='True']
    return ','.join(s)
d['ops']=d.apply(ops,axis=1)
d['open']=d.gap>1e-4
