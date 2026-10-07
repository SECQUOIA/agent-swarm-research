from fractions import Fraction as Fr
import math
# graded grid of Definition def:graded (continuous)
def graded(lo, hi, c, h, th):
    nodes=[c]
    t=Fr(0)
    while True:
        t2=min(t+h+th*t, hi-c)
        nodes.append(c+t2); t=t2
        if t2==hi-c: break
    t=Fr(0)
    while True:
        t2=min(t+h+th*t, c-lo)
        nodes.append(c-t2); t=t2
        if t2==c-lo: break
    return sorted(set(nodes))
G1=graded(Fr(0),Fr(1),Fr(3,10),Fr(1,16),Fr(1,4))
print("grid c=3/10:",[str(x) for x in G1], len(G1))
G2=sorted(set(1-x for x in G1))
print("common:",[str(x) for x in sorted(set(G1)&set(G2))])
widths=[b-a for a,b in zip(G1,G1[1:])]
print("max width",max(widths), float(max(widths)))
deltas=[y2-y1 for y1 in G1 for y2 in G2 if y2>y1]
print("delta",min(deltas))
# corrections at common nodes with m=1/2, L=1
def w(G,v):
    i=G.index(v); ws=[]
    if i>0: ws.append(G[i]-G[i-1])
    if i<len(G)-1: ws.append(G[i+1]-G[i])
    return max(ws)
for nu in [Fr(0),Fr(1)]:
    print(nu, "lhs",(nu-Fr(1,2))**2, "d1+d2", (w(G1,nu)**2+w(G2,nu)**2)/8)
# Example tu-sum
G=graded(Fr(0),Fr(3),Fr(0),Fr(1),Fr(1,4)); print("tu-sum grid",[str(x) for x in G])
d={v: w(G,v)**2/8 for v in G}
print({str(k):str(v) for k,v in d.items()})
pts=[(a,b,a+b) for a in G for b in G if a+b in G]
vals=[(p, Fr(1,2)*((p[0]-1)**2+(p[1]-1)**2+(p[2]-2)**2)-d[p[0]]-d[p[1]]-d[p[2]]) for p in pts]
for p,v in vals: print([str(x) for x in p], v)
# Prop twocenters constant
print("0.23^2/20 > 1/379:", Fr(23,100)**2/20 > Fr(1,379))
# Example chain kappa bounds
# Prop star (B) kappa
print("2(3+sqrt5)=",2*(3+5**0.5))
# Lemma states constants
r=math.sqrt(17/15)
print("states const",3+2*r+(2+r)/math.sqrt(2))
phi=lambda m:0.75+8*math.log(1.25+4*math.sqrt(2*m)); print("phi(1),phi(2)",phi(1),phi(2))
psi=lambda m:0.75+8*math.log(1.25+3*math.sqrt(m)); print("psi(1),psi(2)",psi(1),psi(2))
print("G4 const",(2+r)*(1+1/math.sqrt(8)))
# Example family
print("tu-union nodes bound coefficient n_c*kappa_c per block:",3*72)
# TU-uniform claim (sqrt(2(n-2))+1)^2>=n
print(all((math.sqrt(2*(n-2))+1)**2>=n for n in range(4,10000,2)))
# Prop unique / moments numbers
for r_ in [1,2,3]:
    print("moments r",r_, Fr(1,4)-Fr(2*r_+1,16*r_), Fr(1,8*r_)*(r_-Fr(1,2)))
