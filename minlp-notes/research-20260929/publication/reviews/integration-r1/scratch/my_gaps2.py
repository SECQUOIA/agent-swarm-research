# Part 2: pindyck, eg, waterno2, ann, emfl; dual-display validity for eg and camshape800.
from pathlib import Path as _PublicPath
_PUBLIC_REPO = str(_PublicPath(__file__).resolve().parents[5])

import json, re, math
from fractions import Fraction as Q
from decimal import Decimal
R=(_PUBLIC_REPO + '/research-20260929/')
def J(p): return json.load(open(R+p))
def T(p): return open(R+p).read()
def q(s): s=str(s).strip(); return Q(s) if '/' in s else Q(Decimal(s))
def chk(name, exact, shown, note=''):
    print(f'{name:30s} exact={float(exact):.7e} shown<={shown:9s} {"OK" if q(shown)>=exact else "FAIL"} {note}')
t=T('reviews/pindyck-review-checks/logs/primal_check.txt')
f=q(re.search(r'objective \(min form\) = (\S+)',t)[1])
print('pindyck primal_check lines:'); print('\n'.join(t.splitlines()[:12]))
chk('pindyck (f+1e-36 - display dual)', f+Q(1,10**36)-q('-1170.4862854360886163932'), '5.44e-14')
assert q('-1170.486285436088562')>=f+Q(1,10**36)
# eg: certified binary64 duals (exact double values), retry .sol objvar
egcert={'eg_int_s':'6.4531031529331155','eg_disc_s':'5.760539610694994','eg_disc2_s':'5.642100574331458'}
egprim={'eg_int_s':'6.4531031593842275','eg_disc_s':'5.7605396164535107','eg_disc2_s':'5.6421005799711068'}
for n,d in egcert.items():
    x=dict(l.split() for l in T(f'open-instances-wave3/eg/retry/sol/{n}.retry.sol').splitlines() if l.strip())
    o=q(x['objvar']); Ld=Q(float(d))
    print(f'{n}: display dual {d} <= exact double? {q(d)<=Ld} (double - display = {float(Ld-q(d)):.3e}); primal display >= objvar? {q(egprim[n])>=o}')
    chk(n+' rel (vs exact double)', (o-Ld)/Ld, '1e-9')
# waterno2
duals={'06':'278.230573','09':'824.834692','12':'2089.754565','18':'4790.820715','24':'6576.151388'}
prims={'06':'282.888038','09':'914.012','12':'2233.821346','18':'5023.983','24':'6963.795181'}
gaps={'06':'1.68','09':'10.82','12':'6.90','18':'4.87','24':'5.90'}
for n in duals:
    v=J(f'publication/primal/water-ann-kan/points/waterno2_{n}.exact.json'); f=q(v['objective'])
    L=q(J('open-instances-wave2/waterno2/cellslopes/logs/certB_verify.json')['bound_exact']) if n=='06' else q(J(f'open-instances-wave2/waterno2/logs/cert_{n}_w1_impl.json')['certified_bound_exact'])
    assert q(duals[n])<=L and q(prims[n])>=f, n
    chk(f'waterno2_{n} %', (f-L)/L*100, gaps[n])
    if n=='06':
        for lab,d,g in [('sep','272.584700','3.78'),('wave2','263.735099','7.27')]:
            chk(f'waterno2_06 {lab} %', (f-q(d))/q(d)*100, g)
        chk('waterno2_06 prose 1.68%', (f-L)/L*100,'1.68')
# ann
v=J('publication/primal/water-ann-kan/points/ann_cumene_tanh.point.json'); hi=q(v['objective_hi']); L=q(v['dual_bound'])
assert q('-3386.5403')<=L and q('-3379.9823940')>=hi
chk('ann /|primal| %', (hi-L)/abs(hi)*100, '0.195'); chk('ann /|dual| % (prose 0.194)', (hi-L)/abs(L)*100, '0.194')
chk('ann wave3 /|primal| %', (hi-q('-4024.495'))/abs(hi)*100, '20'); chk('ann wave3 /|dual| %', (hi-q('-4024.495'))/q('4024.495')*100, '16.1')
# emfl050_3_3
v=J('bound-audit/logs/cert_socp_emfl050_3_3.json'); print('emfl keys', [k for k in v][:20])
L=q(v['lower_bound_30_digits_rounded_down']); p=q('10.40173793')
print('emfl abs >=1.42e-5:', L-p>=q('1.42e-5'), float(L-p), ' rel (L-p)/L =', float((L-p)/L), ' >=1.36e-6:', (L-p)/L>=q('1.36e-6'))
