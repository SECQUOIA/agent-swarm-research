"""Independent finite integer checks; this is not a proof of universal claims."""
from itertools import combinations, product
from fractions import Fraction
import json

checked = 0
for n in range(1, 5):
    edges = list(combinations(range(n), 2))
    signs = list(product((-1, 1), repeat=n))
    masks = list(range(1 << n))
    for weights in product((-1, 0, 1), repeat=len(edges)):
        active = [(i,j,a) for (i,j),a in zip(edges,weights) if a]
        values = [sum(a*s[i]*s[j] for i,j,a in active) for s in signs]
        R = Fraction(max(values)-min(values),2)
        L = sum(abs(a) for i,j,a in active)
        rho = max((Fraction(sum(bool(w&(1<<i)) and bool(w&(1<<j)) for i,j,a in active), w.bit_count()) for w in masks if w), default=Fraction(0))
        degree = [sum(i in (u,v) for u,v,a in active) for i in range(n)]
        delta = max(degree, default=0)
        assert L*L <= 16*rho*R*R
        assert L*L <= 4*delta*R*R
        rect_beta = Fraction(0)
        polarized = 0
        for w in masks:
            crossing = [(i,j,a) for i,j,a in active if bool(w&(1<<i)) != bool(w&(1<<j))]
            polarized = max(polarized,max(sum(a*s[i]*s[j] for i,j,a in crossing) for s in signs))
            for z in masks:
                if not (w or z): continue
                rect_count = sum(bool(w&(1<<i)) and bool(z&(1<<j)) for i,j,a in active)
                rect_count += sum(bool(w&(1<<j)) and bool(z&(1<<i)) for i,j,a in active)
                rect_beta = max(rect_beta,Fraction(rect_count,w.bit_count()+z.bit_count()))
        assert polarized == R
        assert rect_beta == rho
        norm_A = max(sum(a*(s[i]*t[j]+s[j]*t[i]) for i,j,a in active) for s in signs for t in signs)
        assert norm_A <= 4*R
        for s in signs:
            for t in signs:
                # p=(s+t)/2 and q=(s-t)/2, integer coordinates.
                p=[(u+v)//2 for u,v in zip(s,t)]
                q=[(u-v)//2 for u,v in zip(s,t)]
                lhs=sum(a*(s[i]*t[j]+s[j]*t[i]) for i,j,a in active)
                rhs=2*sum(a*(p[i]*p[j]-q[i]*q[j]) for i,j,a in active)
                assert lhs == rhs
        checked += 1
result={'status':'PASS','coefficient_vectors':checked,'vertices':'1 through 4','weights':[-1,0,1], 'arithmetic':'exact integers and Fraction', 'checks':['cut polarization','density bound squared','maximum-degree bound squared','rectangle density equals induced density','Schur decoupling identity','infinity-to-one norm <= 4 cut range']}
print(json.dumps(result,indent=2))
