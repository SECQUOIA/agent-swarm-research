from fractions import Fraction as Fr
def graded(lo, hi, c, h, th):
    nodes = {c}
    for direction, end in ((1, hi - c), (-1, c - lo)):
        t = Fr(0)
        while t < end:
            t = min(t + h + th * t, end)
            nodes.add(c + direction * t)
    return sorted(nodes)
G1 = graded(Fr(0), Fr(1), Fr(3,10), Fr(1,16), Fr(1,4))
G2 = graded(Fr(0), Fr(1), Fr(7,10), Fr(1,16), Fr(1,4))
print("G1", [str(x) for x in G1], len(G1))
print("G2", [str(x) for x in G2], len(G2))
print("common", set(G1) & set(G2))
print("max interval", max(max(b-a for a,b in zip(G,G[1:])) for G in (G1,G2)))
print("delta", min(y2-y1 for y1 in G1 for y2 in G2 if y2>y1))
# misaligned example 1
L = Fr(1)
def w(G, v):
    i = G.index(v); ws=[]
    if i>0: ws.append(G[i]-G[i-1])
    if i<len(G)-1: ws.append(G[i+1]-G[i])
    return max(ws)
G1b=[Fr(0),Fr(1,2),Fr(1)]; G2b=[Fr(0),Fr(1,3),Fr(1)]
tb=Fr(2,5)
for t in set(G1b)&set(G2b):
    print(t, L*(t-tb)**2, L/8*w(G1b,t)**2 + L/8*w(G2b,t)**2)
d=min(y2-y1 for y1 in G1b for y2 in G2b if y2>y1); print("delta", d)
print("lambda thr", (max(L/8*w(G1b,v)**2 for v in G1b)+max(L/8*w(G2b,v)**2 for v in G2b))/d)
# ex tu-sum
G = graded(Fr(0), Fr(3), Fr(0), Fr(1), Fr(1,4)); print("G", G)
def dcorr(v): return L/8*w(G,v)**2
pts=[(a,b,c) for a in G for b in G for c in G if a+b==c]
vals=[(p, Fr(1,2)*L*sum((x-y)**2 for x,y in zip(p,(1,1,2))) - sum(dcorr(x) for x in p)) for p in pts]
for p,v in vals: print([str(x) for x in p], v)
print("min F", min(Fr(1,2)*L*sum((x-y)**2 for x,y in zip(p,(1,1,2))) for p in pts))
print("allowance", 3*L*Fr(5,4)**2/8)
