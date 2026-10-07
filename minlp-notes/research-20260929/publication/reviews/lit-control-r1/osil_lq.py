# Own minimal OSIL reader for linear/quadratic instances (no <nl> handling beyond counting).
import xml.etree.ElementTree as ET, os
NS='{os.optimizationservices.org}'
def _expand(el):
    out=[]
    if el is None: return out
    for e in el:
        tag=e.tag[len(NS):]
        mult=int(e.get('mult','1')); incr=e.get('incr')
        if tag=='el':
            v=e.text.strip()
            if incr is None: out+= [v]*mult
            else:
                v0=int(v); d=int(incr); out+=[str(v0+k*d) for k in range(mult)]
    return out
def read(name):
    root=ET.parse(os.path.expanduser(f'~/.cache/minlplib/minlplib/osil/{name}.osil')).getroot()
    I=root.find(NS+'instanceData')
    V=[(v.get('name'),v.get('lb','0'),v.get('ub','INF'),v.get('type','C')) for v in I.find(NS+'variables')]
    o=I.find(NS+'objectives').find(NS+'obj')
    objlin={int(c.get('idx')):c.text.strip() for c in o.findall(NS+'coef')}
    objinfo=(o.get('maxOrMin','min'),o.get('constant','0'))
    C=[(c.get('name'),c.get('lb','-INF'),c.get('ub','INF'),c.get('constant','0')) for c in I.find(NS+'constraints')]
    lin={}
    L=I.find(NS+'linearConstraintCoefficients')
    if L is not None:
        st=[int(x) for x in _expand(L.find(NS+'start'))]
        val=_expand(L.find(NS+'value'))
        if L.find(NS+'rowIdx') is not None:   # column-major
            idx=[int(x) for x in _expand(L.find(NS+'rowIdx'))]
            for col in range(len(st)-1):
                for k in range(st[col],st[col+1]): lin.setdefault(idx[k],{})[col]=val[k]
        else:
            idx=[int(x) for x in _expand(L.find(NS+'colIdx'))]
            for row in range(len(st)-1):
                for k in range(st[row],st[row+1]): lin.setdefault(row,{})[idx[k]]=val[k]
    quad={}
    Q=I.find(NS+'quadraticCoefficients')
    if Q is not None:
        for q in Q:
            quad.setdefault(int(q.get('idx')),[]).append((int(q.get('idxOne')),int(q.get('idxTwo')),q.get('coef','1')))
    nl=I.find(NS+'nonlinearExpressions')
    nnl=0 if nl is None else len(list(nl))
    return dict(V=V,objlin=objlin,objinfo=objinfo,C=C,lin=lin,quad=quad,nnl=nnl)
