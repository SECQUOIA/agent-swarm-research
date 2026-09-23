"""Root audit: directly sum line currents for the proposed NO-instance family."""
from pathlib import Path
from fractions import Fraction as F
import sys,json
sys.path.insert(0,str(Path(__file__).resolve().parents[2]/'checks'))
from check_resistive_exact import build,profile,structural_checks
rows=[]
for k in range(11):
    names=['t','h']+[f'x{j}' for j in range(k+1)]
    eqs=[('inv','t','t'),('add','h','h','t'),('add','t','h','x0')]
    vals={'t':F(1),'h':F(1,2),'x0':F(3,2)}
    d=2
    for j in range(k):
        a,b,c=(f'{s}{j}' for s in 'abc');x=f'x{j}';z=f'x{j+1}'
        names.extend([a,b,c]);eqs.extend([('add',a,'h',x),('inv',x,b),('add',a,b,c),('add',z,'h',c)])
        vals[a]=vals[x]-vals['h'];vals[b]=1/vals[x];vals[c]=vals[a]+vals[b];vals[z]=vals[c]-vals['h']
        d*=d+1
        assert vals[z]==1+F(1,d)
    eqs.append(('inv',f'x{k}','t'))
    assert len(names)==4*k+3 and len(eqs)==4*k+4
    net=build(names,eqs);structural_checks(net);v=profile(net,vals)
    cur={i:F(0) for i in net.buses}
    for (i,j),g in net.edges.items():
        flow=g*(v[i]-v[j]);cur[i]+=flow;cur[j]-=flow
    violations=[]
    for i,bus in net.buses.items():
        assert bus.voltage[0]<=v[i]<=bus.voltage[1]
        p=v[i]*cur[i];e=max(bus.injection[0]-p,p-bus.injection[1],F(0))
        if e:violations.append((i,e))
    assert violations==[(net.gadgets[-1][1][-1],F(1,d+1))]
    assert F(1,d+1)<F(1,2**(2**k))
    rows.append({'k':k,'buses':len(net.buses),'lines':len(net.edges),'residual_denominator_bits':(d+1).bit_length(),'violated_bus_count':len(violations)})
print(json.dumps({'status':'PASS','families':rows,'scope':'exact finite original-network checks, not a quantified proof'},indent=2))
