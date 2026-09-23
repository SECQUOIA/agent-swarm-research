"""Check the Stage 6 physical constructions with exact rational arithmetic.

Run from any working directory with Python 3:
    python /path/to/check_stage06_physical_exact.py

Dependencies: Python standard library only (fractions and itertools).
No manuscript parsing, external solver, input files, or network access is used.
Assertions check finite instances; they do not prove the parameterized results.
"""

from fractions import Fraction as F
from itertools import product

def verts(s):
    vs=[]
    for bits in product((0,1),repeat=len(s)):
        t=[]; prev=F(0)
        for a,b in zip(s,bits):
            prev=b*a+(1-2*b)*prev; t.append(prev)
        vs.append(t)
    assert len({v[-1] for v in vs})==len(vs)
    return vs

def physical(s,t,z,relay):
    n=len(s); S=[]; C=[]; T=[]; resets=set()
    for j in range(n):
        S.append(s[j]); C.append(F(1 if j==0 else 0) if relay else F(n-1-j)); T.append(t[j])
        if relay and 0<j<n-1:
            resets.add(len(S)); S.append(s[j]); C.append(F(1)); T.append(t[j])
    m=len(S); terminal=t[-1]; q=2-terminal
    # Arc capacities, exact path supply contracts and original product rows.
    profit=F(0)
    for i in range(m):
        l,r=S[i]-T[i],T[i]
        assert 0<=l<=S[i] and 0<=r<=S[i]
        assert l+r==S[i]
        profit-=S[i]*(l+r)
    for j in range(m+1):
        qty=F(0); mass=F(0)
        if j>0: qty+=T[j-1];mass+=C[j-1]*T[j-1]
        if j<m: qty+=S[j]-T[j];mass+=C[j]*(S[j]-T[j])
        if j==0: cap=S[0];bound=C[0]
        elif j==m:
            qty+=1-terminal;mass+=1-terminal;cap=F(1);bound=F(1)
            assert qty==1
        elif j in resets:
            cap=S[j];bound=F(1);assert qty==cap
        else:cap=S[j];bound=(C[j-1]+C[j])/2
        assert 0<=qty<=cap and mass<=bound*qty
        profit+=(S[j] if j<m else 1)*qty
    An=1-terminal;AP=terminal;BP=1-terminal;BW=terminal;PW=1-terminal;PV=terminal
    assert all(0<=a<=1 for a in (An,AP,BP,BW,PW,PV,z))
    assert An+AP==BP+BW==AP+BP==PW+PV==1
    assert AP+2*BP==q and BW+PW==1
    assert 2*BW+q*PW<=2*(BW+PW)
    assert PV+z<=2 and q*PV<=PV+z
    profit+=BW+PW+PV+z-1-1-2*z
    dsum=sum((s[j+1]-s[j])*t[j] for j in range(n-1))
    assert profit==dsum-z
    cert=sum((t[j]-(t[j-1] if j else 0))*(s[j]-(t[j-1] if j else 0)-t[j]) for j in range(n))
    assert terminal-terminal**2-dsum==cert>=0
    assert profit<=-cert
    return profit,cert

count=0
for n in range(2,8):
    for general in (False,True):
        s=[F(1)]
        for j in range(n-1):s.insert(0,s[0]/(3+(j%3) if general else 4))
        vs=verts(s);pts=vs+[[ (a+b)/2 for a,b in zip(vs[j],vs[j+1])] for j in range(len(vs)-1)]
        for relay in ((False,) if general else (False,True)):
            for t in pts:
                least=t[-1]-t[-1]**2
                for z in (least,(least+1)/2,F(1)):
                    p,c=physical(s,t,z,relay);count+=1
                    if t in vs and z==least:assert p==0 and c==0
                    elif t not in vs:assert c>0 and p<0
print('PASS:',count,'exact original-network bound, mixing, conservation, economics and certificate checks; n=2..7; descending and relay geometric paths; nongeometric descending supplies; vertex and midpoint path flows; minimum/intermediate/maximum clean flows.')
