"""Leaf shapes of omega and multi on m = eps + (x-a)^2 + 0.01 (z-b)^2, eps = 1e-7:
histogram of log2(w_z/w_x) and of leaves per metric shell.  Usage: python3 leafshape.py"""
import sys; sys.path.insert(0,'.')
import numpy as np, math, collections
from sep_families import A
from poly1d import from_function
from sep2d import node1
g=0.01; e=1e-7
I1=from_function(lambda t:(t-A[0])**2, e/2, K=801, extra=[A[0]])
I2=from_function(lambda t:g*(t-A[1])**2, e/2, K=801, extra=[A[1]])
Is=[I1,I2]
def leaves(rule):
    stack=[((0.0,1.0),(0.0,1.0))]; out=[]
    while stack:
        box=stack.pop()
        vals,ys=zip(*[node1(I,l,u) for I,(l,u) in zip(Is,box)])
        if sum(vals)>=-1e-12: out.append(box); continue
        a=[(y-l)*(u-y) for (l,u),y in zip(box,ys)]
        if rule=="multi": cuts=[j for j in range(2) if a[j]>0]
        else: cuts=[int(np.argmax(a))]
        boxes=[box]
        for i in cuts:
            nb=[]
            for b in boxes:
                l,u=b[i]; s=ys[i]
                b1=list(b); b1[i]=(l,s); b2=list(b); b2[i]=(s,u); nb+=[tuple(b1),tuple(b2)]
            boxes=nb
        stack.extend(boxes)
    return out
for rule in ("omega","multi"):
    L=leaves(rule)
    asp=collections.Counter()
    for (x0,x1),(z0,z1) in L:
        asp[round(math.log2((z1-z0)/(x1-x0)))]+=1
    print(rule, len(L), "log2(wz/wx) histogram:", sorted(asp.items()))
    # leaves near the minimizer: distance shells in the metric (x-a)^2+g(z-b)^2
    sh=collections.Counter()
    for (x0,x1),(z0,z1) in L:
        cx,cz=(x0+x1)/2,(z0+z1)/2
        r=math.sqrt((cx-A[0])**2+g*(cz-A[1])**2+e)
        sh[round(math.log2(r))]+=1
    print("   leaves per metric shell log2 r:", sorted(sh.items()))
