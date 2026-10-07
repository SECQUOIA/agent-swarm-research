# Independent GAMS-subset parser: equations -> exact polynomials (dict monomial->Fraction), bounds.
import re
from fractions import Fraction as F
TOK=re.compile(r'\s*(?:(\d+\.?\d*(?:[eE][+-]?\d+)?|\.\d+(?:[eE][+-]?\d+)?)|([A-Za-z_]\w*)|(\*\*|[-+*/()]))')
def tokenize(s):
    pos=0; out=[]
    s=s.strip()
    while pos<len(s):
        m=TOK.match(s,pos)
        if not m or m.end()==pos: raise ValueError('bad token at %r'%s[pos:pos+20])
        num,name,op=m.groups(); pos=m.end()
        if num is not None: out.append(('n',F(num)))
        elif name is not None: out.append(('v',name))
        else: out.append(('o',op))
        while pos<len(s) and s[pos].isspace(): pos+=1
    return out
def padd(a,b,sg=1):
    r=dict(a)
    for k,v in b.items():
        r[k]=r.get(k,F(0))+sg*v
        if r[k]==0: del r[k]
    return r
def pmul(a,b):
    r={}
    for k1,v1 in a.items():
        for k2,v2 in b.items():
            k=tuple(sorted(k1+k2)); r[k]=r.get(k,F(0))+v1*v2
            if r[k]==0: del r[k]
    return r
class P:
    def __init__(s,t): s.t=t; s.i=0
    def peek(s): return s.t[s.i] if s.i<len(s.t) else None
    def eat(s,x=None):
        tok=s.t[s.i]
        if x is not None and tok!=x: raise ValueError('expected %r got %r'%(x,tok))
        s.i+=1; return tok
    def expr(s):
        r=s.term()
        while s.peek() in (('o','+'),('o','-')):
            op=s.eat()[1]; t=s.term(); r=padd(r,t,1 if op=='+' else -1)
        return r
    def term(s):
        r=s.factor()
        while s.peek()==('o','*'):
            s.eat(); r=pmul(r,s.factor())
        return r
    def factor(s):
        tok=s.peek()
        if tok==('o','-'): s.eat(); return {k:-v for k,v in s.factor().items()}
        if tok==('o','+'): s.eat(); return s.factor()
        if tok==('o','('):
            s.eat(); r=s.expr(); s.eat(('o',')')); return r
        if tok[0]=='n': s.eat(); return {():tok[1]} if tok[1]!=0 else {}
        if tok[0]=='v':
            s.eat()
            if tok[1]=='sqr':
                s.eat(('o','(')); r=s.expr(); s.eat(('o',')')); return pmul(r,r)
            return {(tok[1],):F(1)}
        raise ValueError('unexpected %r'%(tok,))
def parse_poly(txt):
    p=P(tokenize(txt)); r=p.expr()
    if p.i!=len(p.t): raise ValueError('trailing tokens')
    return r
def parse_gms(path):
    txt=open(path).read()
    eqs={}
    for m in re.finditer(r'^(e\d+)\.\.(.*?);',txt,re.S|re.M):
        name,body=m.group(1),m.group(2)
        mm=re.match(r'(.*)=([ELGelg])=(.*)$',body,re.S)
        lhs,sense,rhs=mm.groups()
        pl=parse_poly(lhs); pr=parse_poly(rhs)
        g=padd(pl,pr,-1)          # g(x) sense 0
        eqs[name]=(g,sense.upper())
    lo={};up={}
    for m in re.finditer(r'\b(\w+)\.(lo|up|fx)\s*=\s*([-+]?[\d.]+(?:[eE][+-]?\d+)?)\s*;',txt):
        v,k,val=m.group(1),m.group(2),F(m.group(3))
        if k in('lo','fx'): lo[v]=val
        if k in('up','fx'): up[v]=val
    # count declared equations
    decl=re.search(r'Equations(.*?);',txt,re.S).group(1)
    ndecl=len([e for e in re.split(r'[\s,]+',decl) if e])
    assert ndecl==len(eqs),(path,ndecl,len(eqs))
    pos=set()
    m=re.search(r'Positive Variables(.*?);',txt,re.S)
    if m: pos={e for e in re.split(r'[\s,]+',m.group(1)) if e}
    return eqs,lo,up,pos
