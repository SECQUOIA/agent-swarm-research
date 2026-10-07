from pathlib import Path as _CleanupPath

import sys, math
sys.path.insert(0,'/tmp/scout'); from osil import read, V
name=sys.argv[1]; maxnl=int(sys.argv[2]) if len(sys.argv)>2 else 12; maxlin=int(sys.argv[3]) if len(sys.argv)>3 else 6
I=read((str(_CleanupPath.home()) + '/.cache/minlplib/minlplib/osil/')+name+'.osil'); N=I['names']
def vn(j):
    t=I['vt'][j]; l,u=I['lb'][j],I['ub'][j]
    return f"{N[j]}"
def s(t):
    if t[0]=='num': return f"{t[1]:.4g}"
    if t[0]=='var': return vn(t[1])
    if t[0]=='sum': return '('+' + '.join(s(c) for c in t[1:])+')'
    if t[0]=='times': return '*'.join(s(c) for c in t[1:])
    if t[0]=='negate': return '-'+s(t[1])
    if t[0]=='divide': return f"{s(t[1])}/{s(t[2])}"
    if t[0]=='power': return f"{s(t[1])}^{s(t[2])}"
    return t[0]+'('+','.join(s(c) for c in t[1:])+')'
def row(r,R):
    parts=[f"{c:+.4g}*{vn(j)}" for j,c in list(R['lin'].items())[:12]]
    if len(R['lin'])>12: parts.append(f"...({len(R['lin'])} lin)")
    parts+=[f"{c:+.4g}*{vn(i)}*{vn(j)}" for i,j,c in R['quad'][:10]]
    if len(R['quad'])>10: parts.append(f"...({len(R['quad'])} quad)")
    if R['nl'] is not None: parts.append(s(R['nl'])[:600])
    lo,hi=R['lb'],R['ub']
    return f"[{r}] {lo} <= "+' '.join(parts)+f" <= {hi}"
print(name,'sense',I['sense'],'nvars',len(N),'ncons',I['ncons'])
print('OBJ',row(-1,I['rows'][-1])[:1500])
nl=[r for r,R in I['rows'].items() if r>=0 and (R['quad'] or R['nl'] is not None)]
lin=[r for r,R in I['rows'].items() if r>=0 and not (R['quad'] or R['nl'] is not None)]
print('#nl rows',len(nl),'#lin rows',len(lin))
step=max(1,len(nl)//maxnl)
for r in nl[::step][:maxnl]: print(row(r,I['rows'][r])[:900])
step=max(1,len(lin)//maxlin)
for r in lin[::step][:maxlin]: print(row(r,I['rows'][r])[:500])
used=set()
for r in nl[:3]:
    R=I['rows'][r]; used|=set(R['lin']); 
    for i,j,c in R['quad']: used|={i,j}
    if R['nl'] is not None: used|=V(R['nl'])
print('bounds:',' '.join(f"{N[j]}:{I['vt'][j]}[{I['lb'][j]:.3g},{I['ub'][j]:.3g}]" for j in sorted(used)[:40]))
