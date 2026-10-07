import xml.etree.ElementTree as ET, math, re
from collections import Counter, defaultdict
NS="{os.optimizationservices.org}"
def fl(s):
    s=s.replace("-INF","-inf").replace("INF","inf"); return float(s)
def _tree(node):
    tag=node.tag.replace(NS,"")
    if tag=="number": return ("num",float(node.get("value")))
    if tag=="variable":
        coef=float(node.get("coef","1")); v=("var",int(node.get("idx")))
        return v if coef==1.0 else ("times",("num",coef),v)
    kids=[_tree(c) for c in node]
    if tag in("sum","plus"): return ("sum",*kids)
    if tag=="minus": return ("sum",kids[0],("negate",kids[1]))
    if tag in("times","product"): return ("times",*kids)
    return (tag,*kids)
def read(path):
    root=ET.parse(path).getroot(); data=root.find(f"{NS}instanceData")
    lb,ub,vt,names=[],[],[],[]
    for v in data.find(f"{NS}variables"):
        t=v.get("type","C"); vt.append(t)
        lb.append(fl(v.get("lb","0"))); ub.append(fl(v.get("ub","1" if t=="B" else "INF"))); names.append(v.get("name"))
    rows={-1:{"lin":{},"quad":[],"nl":None,"lb":None,"ub":None}}
    objs=data.find(f"{NS}objectives"); sense="min"
    if objs is not None and len(objs):
        o=objs[0]; sense=o.get("maxOrMin","min")
        for c in o: rows[-1]["lin"][int(c.get("idx"))]=float(c.text)
    cons=data.find(f"{NS}constraints"); n=0
    if cons is not None:
        for i,c in enumerate(cons):
            rows[i]={"lin":{},"quad":[],"nl":None,"lb":fl(c.get("lb","-INF")),"ub":fl(c.get("ub","INF")),"name":c.get("name")}; n+=1
    lcc=data.find(f"{NS}linearConstraintCoefficients")
    if lcc is not None:
        def expand(el):
            out=[]
            for e in el:
                m=int(e.get("mult","1")); inc=float(e.get("incr","0")); val=float(e.text)
                out+=[val+k*inc for k in range(m)]
            return out
        start=[int(v) for v in expand(lcc.find(f"{NS}start"))]; vals=expand(lcc.find(f"{NS}value"))
        if lcc.find(f"{NS}rowIdx") is not None:
            idx=[int(v) for v in expand(lcc.find(f"{NS}rowIdx"))]
            for col in range(len(start)-1):
                for k in range(start[col],start[col+1]): rows[idx[k]]["lin"][col]=vals[k]
        else:
            idx=[int(v) for v in expand(lcc.find(f"{NS}colIdx"))]
            for r in range(len(start)-1):
                for k in range(start[r],start[r+1]): rows[r]["lin"][idx[k]]=vals[k]
    qc=data.find(f"{NS}quadraticCoefficients")
    if qc is not None:
        for q in qc: rows[int(q.get("idx"))]["quad"].append((int(q.get("idxOne")),int(q.get("idxTwo")),float(q.get("coef","1"))))
    nle=data.find(f"{NS}nonlinearExpressions")
    if nle is not None:
        for e in nle: rows[int(e.get("idx"))]["nl"]=_tree(e[0])
    return dict(lb=lb,ub=ub,vt=vt,names=names,sense=sense,rows=rows,ncons=n)

def V(t,acc=None):
    acc=set() if acc is None else acc
    if t[0]=="var": acc.add(t[1])
    elif t[0]!="num":
        for c in t[1:]: V(c,acc)
    return acc
def islin(t):
    if t[0] in("num","var"): return True
    if t[0] in("sum","negate"): return all(islin(c) for c in t[1:])
    if t[0]=="times":
        nc=[c for c in t[1:] if V(c)]
        return len(nc)<=1 and all(islin(c) for c in t[1:])
    if t[0]=="divide": return islin(t[1]) and not V(t[2])
    return False
class Ana:
    def __init__(s,ins): s.I=ins
    def vsig(s,j):
        I=s.I; t=I["vt"][j]
        if t=="B": return "B"
        if t=="I": return "I"
        l,u=I["lb"][j],I["ub"][j]
        if math.isinf(l) or math.isinf(u): return "Cu"
        if l<0<u: return "C±"
        return "C"
    def sig(s,t,depth=0):
        if t[0]=="num": return "k"
        if t[0]=="var": return s.vsig(t[1])
        if islin(t):
            vs=V(t)
            if len(vs)==1: return s.vsig(next(iter(vs)))
            return "L"
        if depth>4: return "…"
        op=t[0]
        if op=="negate": return s.sig(t[1],depth)
        if op=="sum":
            parts=sorted(set(s.sig(c,depth) for c in t[1:] if V(c)))
            return "+".join(parts) if len(parts)>1 else parts[0]
        if op=="times":
            nc=[c for c in t[1:] if V(c)]
            if len(nc)==1: return s.sig(nc[0],depth)
            return "*".join(sorted(s.sig(c,depth+1) for c in nc))
        if op=="divide":
            if not V(t[2]): return s.sig(t[1],depth)
            return f"({s.sig(t[1],depth+1)})/({s.sig(t[2],depth+1)})"
        if op=="power":
            if not V(t[2]):
                p=t[2][1] if t[2][0]=="num" else "k"
                return f"({s.sig(t[1],depth+1)})^{p:g}" if isinstance(p,float) else f"({s.sig(t[1],depth+1)})^k"
            if not V(t[1]): return f"k^({s.sig(t[2],depth+1)})"
            return f"({s.sig(t[1],depth+1)})^({s.sig(t[2],depth+1)})"
        if op=="signpower":
            p=t[2][1] if t[2][0]=="num" else 0
            return f"signpow({s.sig(t[1],depth+1)},{p:g})"
        return f"{op}("+",".join(s.sig(c,depth+1) for c in t[1:])+")"
    def atoms(s,t,out):
        """collect maximal nonlinear terms under linear wrappers (sum, negate, const*)"""
        if islin(t): return
        op=t[0]
        if op in("sum",):
            for c in t[1:]: s.atoms(c,out)
            return
        if op=="negate": s.atoms(t[1],out); return
        if op=="times":
            nc=[c for c in t[1:] if V(c)]
            if len(nc)==1: s.atoms(nc[0],out); return
        if op=="divide" and not V(t[2]): s.atoms(t[1],out); return
        out.append(t)
def analyze(path,maxrows=None):
    I=read(path); A=Ana(I); vt=I["vt"]
    atomc=Counter(); rowsig=Counter(); varatoms=defaultdict(set); nlrows_eq=0; nlrows_ineq=0; objnl=False
    bilin_edges=set(); nlvars=set()
    for r,row in I["rows"].items():
        sigs=[]
        for i,j,c in row["quad"]:
            if i==j: sg=f"({A.vsig(i)})^2"; varatoms[i].add("sq")
            else:
                sg="*".join(sorted([A.vsig(i),A.vsig(j)])); bilin_edges.add((min(i,j),max(i,j)))
                varatoms[i].add(("bl",j)); varatoms[j].add(("bl",i))
            sigs.append(sg); nlvars.update([i,j])
        if row["nl"] is not None:
            at=[]; A.atoms(row["nl"],at)
            for a in at:
                sg=A.sig(a); sigs.append(sg); vs=V(a); nlvars|=vs
                for v in vs: varatoms[v].add(sg)
                if a[0]=="times":
                    nc=[c for c in a[1:] if V(c)]
                    if len(nc)==2 and all(c[0]=="var" for c in nc):
                        i,j=nc[0][1],nc[1][1]; bilin_edges.add((min(i,j),max(i,j)))
        if not sigs: continue
        for sg in sigs: atomc[sg]+=1
        if r==-1: objnl=True
        else:
            eq = row["lb"]==row["ub"]
            if eq: nlrows_eq+=1
            else: nlrows_ineq+=1
            rowsig[("EQ" if eq else "IN")+":"+" | ".join(f"{k}x{v}" for k,v in sorted(Counter(sigs).items()))]+=1
    deg=Counter()
    for i,j in bilin_edges: deg[i]+=1; deg[j]+=1
    nb=sum(1 for t in vt if t=="B"); ni=sum(1 for t in vt if t=="I")
    nlbin=sum(1 for v in nlvars if vt[v] in "BI")
    unb=sum(1 for v in nlvars if vt[v]=="C" and (math.isinf(I["lb"][v]) or math.isinf(I["ub"][v])))
    # big-M: linear rows with a binary coef magnitude >= 100x the median other coef
    bigm=0
    for r,row in I["rows"].items():
        if r<0 or row["quad"] or row["nl"] is not None: continue
        bc=[abs(c) for k,c in row["lin"].items() if vt[k]=="B"]; cc=[abs(c) for k,c in row["lin"].items() if vt[k]=="C" and k in nlvars]
        if bc and cc and max(bc)>=50*max(min(cc),1e-9): bigm+=1
    return dict(nvars=len(vt),nbin=nb,nint=ni,ncons=I["ncons"],objnl=objnl,nleq=nlrows_eq,nlin=nlrows_ineq,
                nlvars=len(nlvars),nlbin=nlbin,nl_unbounded=unb,bilin_edges=len(bilin_edges),maxdeg=max(deg.values()) if deg else 0,
                multi_atom_vars=sum(1 for v,s in varatoms.items() if len(s)>=2),
                bigm_rows=bigm,atoms=atomc.most_common(12),rowsigs=rowsig.most_common(8))
