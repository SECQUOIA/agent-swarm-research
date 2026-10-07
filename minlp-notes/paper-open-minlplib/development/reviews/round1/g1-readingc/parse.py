import xml.etree.ElementTree as ET
from fractions import Fraction as F
NS='{os.optimizationservices.org}'
def load(path):
    root=ET.parse(path).getroot()
    d=root.find(NS+'instanceData')
    vars_=[v.attrib for v in d.find(NS+'variables')]
    cons=[c.attrib for c in d.find(NS+'constraints')] if d.find(NS+'constraints') is not None else []
    # linear coefficients (row-major or column-major)
    lin={}
    lcc=d.find(NS+'linearConstraintCoefficients')
    def expand(el):
        out=[]
        for e in el:
            mult=int(e.attrib.get('mult','1')); incr=e.attrib.get('incr')
            txt=e.text
            if incr is not None:
                v0=int(txt); inc=int(incr)
                out+= [v0+k*inc for k in range(mult)]
            else:
                out+=[txt]*mult
        return out
    if lcc is not None:
        start=[int(x) for x in expand(lcc.find(NS+'start'))]
        rowIdx=lcc.find(NS+'rowIdx'); colIdx=lcc.find(NS+'colIdx')
        val=[F(x) for x in expand(lcc.find(NS+'value'))]
        if colIdx is not None:
            idx=[int(x) for x in expand(colIdx)]
            for r in range(len(start)-1):
                for k in range(start[r],start[r+1]):
                    lin.setdefault(r,[]).append((idx[k],val[k]))
        else:
            idx=[int(x) for x in expand(rowIdx)]
            for c in range(len(start)-1):
                for k in range(start[c],start[c+1]):
                    lin.setdefault(idx[k],[]).append((c,val[k]))
    q={}
    qc=d.find(NS+'quadraticCoefficients')
    if qc is not None:
        for t in qc:
            a=t.attrib
            q.setdefault(int(a['idx']),[]).append((int(a['idxOne']),int(a['idxTwo']),F(a['coef'])))
    return d,vars_,cons,lin,q
