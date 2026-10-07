# Own check: does every quadratic row of powerflow0039r commute with J (rotation invariance)?
import xml.etree.ElementTree as ET
from fractions import Fraction as Fr
from collections import defaultdict
ns={'o':'os.optimizationservices.org'}
root=ET.parse('/tmp/pfcrit/powerflow0039r.osil').getroot()
q=defaultdict(lambda: defaultdict(Fr))
for t in root.iter('{os.optimizationservices.org}qTerm'):
    r=int(t.get('idx')); i=int(t.get('idxOne')); j=int(t.get('idxTwo')); c=Fr(t.get('coef','1'))
    a,b=min(i,j),max(i,j)
    q[r][(a,b)]+=c
# x185..x223 = e (0-based 184..222), x224..x262 = f (0-based 223..261)
E=list(range(184,223)); F=list(range(223,262))
pos={}
for k,(e,f) in enumerate(zip(E,F)):
    pos[e]=(k,0); pos[f]=(k,1)
bad=0; nrows=0
for r,terms in q.items():
    if r<0: continue
    xs=[(a,b,c) for (a,b),c in terms.items() if a in pos and b in pos]
    other=[(a,b) for (a,b),c in terms.items() if not (a in pos and b in pos)]
    if not xs: continue
    nrows+=1
    # symmetric matrix entries M[(k,s),(m,t)]
    M=defaultdict(Fr)
    for a,b,c in xs:
        if a==b: M[(pos[a],pos[a])]+=c
        else:
            M[(pos[a],pos[b])]+=c/2; M[(pos[b],pos[a])]+=c/2
    # check block structure: for each block (k,m): [[p, r],[s, t]] commutes with J2=[[0,-1],[1,0]] iff p==t and r==-s
    blocks=defaultdict(lambda: [[Fr(0),Fr(0)],[Fr(0),Fr(0)]])
    for ((k,s),(m,t)),c in M.items(): blocks[(k,m)][s][t]+=c
    for (k,m),B in blocks.items():
        if B[0][0]!=B[1][1] or B[0][1]!=-B[1][0]:
            bad+=1
            if bad<=10: print('row',r,'block',k,m,[[float(x) for x in row] for row in B], 'diff', float(B[0][0]-B[1][1]), float(B[0][1]+B[1][0]))
print('quadratic rows with x-terms:',nrows,'non-commuting blocks:',bad)
