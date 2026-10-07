# Independent exact recomputation of the summary gap cells (reviewer's own code).
# Reads saved JSON/log/text evidence only; imports no scientific module.
from pathlib import Path as _PublicPath
_PUBLIC_REPO = str(_PublicPath(__file__).resolve().parents[5])

import json, re, gzip, math
from fractions import Fraction as Q
from decimal import Decimal
R=(_PUBLIC_REPO + '/research-20260929/')
def J(p): return json.load(open(R+p))
def T(p): return open(R+p).read()
def q(s): return Q(Decimal(str(s).strip())) if '/' not in str(s) else Q(str(s).strip())
def up(x, unit):  # round x>=0 up to multiple of unit
    u=q(unit); return math.ceil(x/u)*u
out=[]
def chk(name, exact, shown, note=''):
    ok = q(shown) >= exact
    out.append((name, float(exact), shown, ok, note))
    print(f'{name:28s} exact={float(exact):.6e} shown<={shown:10s} {"OK" if ok else "FAIL"} {note}')
# --- lnts: displayed summary duals vs primal enclosure hi
disp={'lnts50':('0.5546687649381','5.79e-13'),'lnts100':('0.5545954011663','6.12e-13'),'lnts200':('0.5545770161025','5.84e-13'),'lnts400':('0.5545724137001','5.88e-13')}
ver={e['name']:e for e in J('reviews/open-instances-verification/logs/lnts_verify.json')}
mx=Q(0)
for n,(d,g) in disp.items():
    N=int(n[4:]); fhi=q(J(f'publication/primal/lnts/points/{n}_point.json')['objective_enclosure'][1])
    Nh2=N*q(ver[n]['cert_1e-12']['h2'])
    assert q(d)<=Nh2, n
    chk(n, fhi-q(d), g, f'(dual display <= N*h2 by {float(Nh2-q(d)):.2e}; fhi-N*h2={float(fhi-Nh2):.4e})')
    mx=max(mx,fhi-Nh2+Q(N)*Q(1,10**21)*5)  # allow h2 print error 5e-22? see note
    # primal display >= fhi
prim={'lnts50':'0.5546687649387','lnts100':'0.5545954011670','lnts200':'0.5545770161031','lnts400':'0.5545724137007'}
for n,p in prim.items():
    fhi=q(J(f'publication/primal/lnts/points/{n}_point.json')['objective_enclosure'][1]); assert q(p)>=fhi,(n,p)
print('lnts max fhi - N*h2 (+h2 print slack N*5e-22):',float(mx))
# --- dtoc5
f=Q(T('publication/primal/dtoc5-lukvle10/logs/dtoc5_check_objective_exact.txt').strip())
assert q('5.389672119181141')>=f
chk('dtoc5 (vs display dual)', f-q('5.38967211918114'), '4.7e-16')
print('   dtoc5 f - verifier dual 5.38967211918114046:', float(f-q('5.38967211918114046')))
# --- lukvle10
x=J('publication/primal/dtoc5-lukvle10/logs/lukvle10_enclose.json'); hi=q(x['objective_box'][1])
assert q('352.2380254064961')>=hi
chk('lukvle10', hi-q('352.2380254050784'), '1.5e-9')
# --- optcdeg2
L=Q(int(J('reviews/bangbang-verification/logs/qcal_exact.json')['bound_str']),10**20)
assert q('293.87607509587509')<=L
pc=T('reviews/bangbang-verification/logs/primal_check.json')
m=re.search(r'"J_upper":\s*"?\[?([^\],"]+),\s*([^\]"]+)\]?',pc)
print('   optcdeg2 J_upper raw:', re.search(r'J_upper[^\n]{0,200}',pc)[0][:200])
Ju=q(re.search(r'J_upper": "\[([0-9.]+),',pc)[1]); assert q('293.87607509587509328')>=Ju
chk('optcdeg2 (J_upper - cert)', Ju-L, '9e-16')
print('   optcdeg2 displayed primal - cert =', float(q('293.87607509587509328')-L))
# --- ex6_2_5 / ex6_2_7 (20-digit enclosures; add 1e-20 for the 20-digit rounding)
for n,g,pd in [('ex6_2_5','2.1e-15','-70.752077833447705'),('ex6_2_7','4.9e-14','-0.16084761546360086')]:
    v=J(f'reviews/wave2-small-verification/logs/{n}_bound.json')
    E=v['own_primal_objective_enclosure']; E=eval(E) if isinstance(E,str) else E; fhi=q(E[1]); L=q(v['dual_bound'])
    slack=Q(1,10**20) if n=='ex6_2_5' else Q(1,10**22)
    assert q(pd)>=fhi
    chk(n, fhi+slack-L, g)
# --- etamac
v=J('reviews/wave2-small-verification/logs/etamac.json')
s=v['own_primal'] if isinstance(v['own_primal'],dict) else eval(v['own_primal'])
o=s['objective'][1]; hi=q(re.findall(r'[-\d.]+',o)[-1]); L=q(v['bound']['dual_bound'] if isinstance(v['bound'],dict) else eval(v['bound'])['dual_bound'])
chk('etamac', hi-L, '2.6e-15')
# --- pricing050 (max): conservative display subtraction, and verifier U
v=J('reviews/wave2-small-verification/logs/pricing050.json')
chk('pricing050 (displays)', q('-1813.8290784519731')*-1 - q('-1813.8290784519730577')*-1, '4.23e-14')
mlt=v['multipliers']; U=q(mlt['e5'])*-788+q(mlt['e6'])*-984-q(v['certificate']['sum_minF_certified'])
print('   pricing U recomputed', U, ' display upper -1813.8290784519730577 >= U:', q('-1813.8290784519730577')>=U, ' primal_20', v['own_primal']['objective_20'], ' U - primal20 =', float(U-q(v['own_primal']['objective_20'])))
# --- chain: safe displays vs exact-point hi
safe={'50':'5.0722614939828627','100':'5.0697846107387505','200':'5.0689173417931616','400':'5.0686216946040092'}
cm=Q(0)
for n,d in safe.items():
    b=J(f'publication/primal/chain/points/chain{n}_box.json'); hi=q(b['objective_enclosure_decimal'][1])
    Lb=Q(float(J(f'open-instances-wave2/cops/logs/chain{n}_bound.json')['bnb']['bound'])); assert q(d)<=Lb,(n,d,Lb)
    assert q(d) >= q('5.06862') ; cm=max(cm,hi-q(d))
chk('chain max', cm, '1.01e-14')
# --- catmix: verifier duals (certified doubles) vs author exact points (100/200/400) and verifier DP point (800)
ed=J('publication/reproduction/cops/logs/exact_display_checks.json')
for n,g in [('100','1.85e-13'),('200','1.90e-11'),('400','6.81e-11'),('800','1.49e-10')]:
    ver=[e for e in ed if e['instance']==f'catmix{n}' and e['source'].startswith('verifier')][0]
    auth=[e for e in ed if e['instance']==f'catmix{n}' and e['source'].startswith('author')][0]
    L=Q(float(ver['certified_double']))
    hi=q(auth['primal_hi']) if n!='800' else q(ver['primal_hi'])
    chk(f'catmix{n}', hi-L, g, f"(primal: {'author exact' if n!='800' else ver['primal_label']})")
# --- powerflow (relative to dual)
for n,g in [('0030p','2.1e-9'),('0039p','6.4e-10'),('0039r','6.7e-10')]:
    t=T(f'publication/primal/powerflow/logs/certify.powerflow{n}.log'); lo,hi=map(q,re.search(r'objective enclosure: \[([^,]+), ([^\]]+)\]',t).groups())
    if n=='0030p': x=J('open-instances-wave3/logs/powerflow0030p.sdpcert.json')
    else: x=J(f'open-instances-wave3/powerflow/ext/logs/powerflow{n}.bb3t.json')
    be=x.get('bound_exact') or x.get('LB_exact')
    print('   pf',n,'bound_exact type', be[:40], '...')
    L=q(be) if '/' in be else None
    if L is None:
        print('   (non-fraction exact bound; skip)'); continue
    chk(f'powerflow{n} rel', (hi-L)/L, g)
