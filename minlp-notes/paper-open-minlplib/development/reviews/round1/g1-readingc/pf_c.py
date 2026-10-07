import osilx, json
from fractions import Fraction as F
def coefs(t,out):
    if t[0]=='var':
        out.append(t[2])
    elif t[0]=='num':
        out.append(t[1])
    else:
        for c in t[1:]: coefs(c,out)
    return out
rows={'powerflow0030p':'e2','powerflow0039p':'e65','powerflow0039r':'e65'}
for name,row in rows.items():
    I=osilx.read(name+'.osil'); P=json.load(open(name+'.json')); names=I['names']
    c=[c for c in I['cons'] if c['name']==row][0]
    print(name,row,c['lb'],c['ub'],c['constant'],c['lin'],c['quad'],c['nl'])
    (j,a),=c['lin'].items(); assert a=='1' and F(c['lb'])==0==F(c['ub'])
    cs=coefs(c['nl'],[]) if c['nl'] else []
    cs+= [q[2] for q in c['quad']]
    nonunit=[F(s) for s in cs if F(s) not in (1,-1)]
    mags=set(abs(x) for x in nonunit); assert len(mags)==1
    cmag=mags.pop()
    # every nonunit coefficient appears exactly once per product term? check each product has exactly one nonunit factor
    flc=F(float(cmag)); print('  |c| =',cmag,'=',float(cmag),' fl(c)!=c:',flc!=cmag, ' fl(-c)==-fl(c):', F(float(-cmag))==-flc)
    n=names[j]; v=F(P['free'][n]) if n in P['free'] else F(P['fixed'][n]['value']); r=F(P['radius'])
    print('  P var',n,'centre',float(v),'radius',float(r),'|P|>r:',abs(v)>r, ' residual_c approx', float(v*(cmag-flc)/cmag))
