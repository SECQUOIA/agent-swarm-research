from pathlib import Path as _CleanupPath

import sys
sys.path.insert(0,'/tmp/scout'); from osil import read, V
name=sys.argv[1]; targets=set(sys.argv[2].split(','))
I=read((str(_CleanupPath.home()) + '/.cache/minlplib/minlplib/osil/')+name+'.osil'); N=I['names']; idx={n:i for i,n in enumerate(N)}
T={idx[t] for t in targets}
def s(t):
    if t[0]=='num': return f"{t[1]:.4g}"
    if t[0]=='var': return N[t[1]]
    if t[0]=='sum': return '('+' + '.join(s(c) for c in t[1:])+')'
    if t[0]=='times': return '*'.join(s(c) for c in t[1:])
    if t[0]=='negate': return '-'+s(t[1])
    if t[0]=='divide': return f"{s(t[1])}/{s(t[2])}"
    if t[0]=='power': return f"{s(t[1])}^{s(t[2])}"
    return t[0]+'('+','.join(s(c) for c in t[1:])+')'
for r,R in I['rows'].items():
    vs=set(R['lin'])|{i for i,j,c in R['quad']}|{j for i,j,c in R['quad']}|(V(R['nl']) if R['nl'] is not None else set())
    if vs&T:
        parts=[f"{c:+.4g}*{N[j]}" for j,c in R['lin'].items()]+[f"{c:+.4g}*{N[i]}*{N[j]}" for i,j,c in R['quad']]
        if R['nl'] is not None: parts.append(s(R['nl']))
        print(f"[{r}] {R['lb']} <= {' '.join(parts)[:700]} <= {R['ub']}")
for t in sorted(T): print(N[t],I['vt'][t],I['lb'][t],I['ub'][t])
