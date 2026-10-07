# Critic: apply the enclosure criterion to the dossier's pattern-scan hits (copy of pattern_scan.py imported from /tmp only).
import importlib.util,os,math,sys
from fractions import Fraction as F
from collections import Counter
spec=importlib.util.spec_from_file_location('ps',os.path.join(os.path.dirname(os.path.abspath(__file__)),'ps.py')); ps=importlib.util.module_from_spec(spec); spec.loader.exec_module(ps)
def up(q):
    d=float(q)
    if F(d)<q: d=math.nextafter(d,math.inf)
    return d
def dn(q):
    d=float(q)
    if F(d)>q: d=math.nextafter(d,-math.inf)
    return d
for nm in sys.argv[1:]:
    h=ps.scan(os.path.expanduser('~/.cache/minlplib/minlplib/osil/%s.osil'%nm))
    c=Counter(); strong=Counter()
    for (cname,xn,yn,k,side,bx,by,res,bad) in h:
        if bad: c[(side,bx,k)]+=1
        ex=F(float(bx))**k; y=float(F(by))
        if ((up(ex)<y) if side=='lb' else (dn(ex)>y)): strong[(side,bx,k)]+=1
    print(nm,'residual-sign hits',sum(c.values()),dict(sorted(c.items())),'| enclosure-missing hits',sum(strong.values()),dict(strong))
