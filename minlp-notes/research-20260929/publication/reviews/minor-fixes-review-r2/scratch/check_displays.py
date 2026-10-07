"""Independent exact check of every numeric display in the round-2 integration
list and of every primal/dual/gap display in open-instances-summary.md.
Reads saved data only; never imports project code."""
from pathlib import Path as _PublicPath
_PUBLIC_REPO = str(_PublicPath(__file__).resolve().parents[5])

import json, re, gzip
from fractions import Fraction as Q
from decimal import Decimal, getcontext
getcontext().prec = 80
R = (_PUBLIC_REPO + '/research-20260929')
P = R + '/publication'
J = lambda p: json.load(open(p))
def D(q, n=25): return str(Decimal(q.numerator) / Decimal(q.denominator))[:n+3]
def F(x): return f'{float(x):.6g}'
def ceil_sig(q, sig):  # round positive q up to sig significant digits
    from math import floor, log10
    e = floor(log10(float(q))) - sig + 1
    u = Q(10)**e; k = -((-q) // u); return k*u
def report(name, kind, shown, ok, extra=''):
    print(f"{'OK ' if ok else 'BAD'} {name:16s} {kind:28s} {shown:28s} {extra}")
def primal_min(name, shown, hi, extra=''):
    s = Q(shown.replace('−','-')); report(name, 'primal (min) >= f_hi', shown, s >= hi, f'display-f_hi={F(s-hi)} {extra}')
def dual_min(name, shown, L, extra=''):
    s = Q(shown.replace('−','-')); report(name, 'dual (min) <= cert', shown, s <= L, f'cert-display={F(L-s)} {extra}')
def gap(name, shown, exact, kind='abs'):
    s = Q(shown.replace('%','').replace('≤','').strip()) / (100 if '%' in shown else 1)
    sig = len(re.sub(r'[^0-9]','',shown.split('e')[0]).lstrip('0'))
    up = ceil_sig(exact, sig)
    report(name, f'gap {kind} >= exact', shown, s >= exact, f'exact={float(exact):.6g} upward@{sig}sig={float(up):.4g}')

print('== lnts (summary dual = displayed; cert = N*h2 from verifier) ==')
ver = {v['name']: v for v in J(R+'/reviews/open-instances-verification/logs/lnts_verify.json')}
summ = {50:('0.5546687649381','0.5546687649387','5.79e-13'),100:('0.5545954011663','0.5545954011670','6.12e-13'),
        200:('0.5545770161025','0.5545770161031','5.84e-13'),400:('0.5545724137001','0.5545724137007','5.88e-13')}
for n,(d,p,g) in summ.items():
    lo,hi = map(Q, eval(J(P+f'/primal/lnts/points/lnts{n}_point.json')['objective_enclosure']) if isinstance(J(P+f'/primal/lnts/points/lnts{n}_point.json')['objective_enclosure'],str) else J(P+f'/primal/lnts/points/lnts{n}_point.json')['objective_enclosure'])
    h2 = ver[f'lnts{n}']['cert_1e-12']['h2']; ulp = Q(1, 10**len(h2.split('.')[1]))
    Lc = n*(Q(h2)-ulp)   # conservative: allow one unit error in last printed digit of h2
    primal_min(f'lnts{n}', p, hi); dual_min(f'lnts{n}', d, Lc)
    gap(f'lnts{n}', g, hi-Q(d)); print('    gap vs N*h2 (cons.)', F(hi-Lc), '<= 5.55e-13:', hi-Lc <= Q('5.55e-13'))
    safe = {50:'0.5546687649381242',100:'0.5545954011663565',200:'0.5545770161025290',400:'0.5545724137001325'}[n]
    print('    safe verifier display <= N*h2-ulp:', Q(safe) <= Lc, ' rel gap vs safe', F((hi-Q(safe))/Q(safe)))

print('== dtoc5 ==')
f = Q(open(P+'/reviews/minor-fixes-review-r2/scratch/dtoc5_f.txt').read().strip())
dv = J(R+'/reviews/open-instances-verification/logs/dtoc5_verify.json')['dual_bound']
dlo = Q(re.search(r'\[([0-9.]+),', dv)[1]) if isinstance(dv,str) else Q(re.search(r'\[([0-9.]+),', dv[0])[1])
print('    verifier dual lower end', D(dlo,32), ' f', D(f,32))
primal_min('dtoc5','5.389672119181141',f); report('dtoc5','old primal invalid','5.38967211918114', Q('5.38967211918114')<f)
dual_min('dtoc5','5.38967211918114',dlo); gap('dtoc5','1e-14',f-Q('5.38967211918114'))

print('== chain ==')
for n in (50,100,200,400):
    hi = Q(J(P+f'/primal/chain/points/chain{n}_box.json')['objective_enclosure_decimal'][1])
    b = J(R+f'/open-instances-wave2/cops/logs/chain{n}_bound.json')['bnb']['bound']; assert isinstance(b,float)
    L = Q(b)
    safe = {50:'5.0722614939828627',100:'5.0697846107387505',200:'5.0689173417931616',400:'5.068621694604009'}[n]
    dual_min(f'chain{n}', safe, L); dual_min(f'chain{n} range', {50:'5.07226',400:'5.06862'}.get(n,'5.06862'), L)
    print(f'    gap vs L {F(hi-L)}; vs safe {F(hi-Q(safe))}; <=1.01e-14: {hi-Q(safe) <= Q("1.01e-14")}')
    if n in (50,200):
        old = {50:'5.072261493982863',200:'5.068917341793162'}[n]
        print(f'    old display {old} - L = {F(Q(old)-L)} (positive means invalid); truncation check: safe is L truncated to 16 dp: {safe == str(Decimal(L.numerator)/Decimal(L.denominator))[:len(safe)]}')
        # older-doc collateral: wave-2 cops report gap column uses double primal points
        prim = {50:'5.0722614939828724',200:'5.0689173417931710'}[n]
        print(f'    cops report row: primal {prim} - new display = {F(Q(prim)-Q(safe))}; - old display = {F(Q(prim)-Q(old))}')

print('== ex6_2_5 / ex6_2_7 (enclosure printed to 20 sig digits; bracket by one unit) ==')
for name, p, d, g in [('ex6_2_5','-70.752077833447705','-70.75207783344770759','2.0e-15'),('ex6_2_7','-0.16084761546360086','-0.16084761546364905','4.8e-14')]:
    v = J(R+f'/reviews/wave2-small-verification/logs/{name}_bound.json')
    e = v['own_primal_objective_enclosure']; u = Q(1,10**len(e[1].split('.')[1]))
    hi = Q(e[1]) + u
    primal_min(name, p, hi); dual_min(name, d, Q(v['dual_bound'])); gap(name, g, hi - Q(v['dual_bound']))
report('ex6_2_5','old primal invalid','-70.752077833447706', Q('-70.752077833447706') < Q(J(R+'/reviews/wave2-small-verification/logs/ex6_2_5_bound.json')['own_primal_objective_enclosure'][0]) - Q(1,10**17))

print('== powerflow ==')
for name, p, d, g in [('powerflow0030p','576.8934134704','576.8934122988004','2.0e-9'),('powerflow0039p','41869.0515113203','41869.05148485014','6.3e-10'),('powerflow0039r','41869.0515113210','41869.05148327243','6.7e-10')]:
    t = open(P+f'/primal/powerflow/logs/certify.{name}.log').read()
    lo, hi = map(Q, re.search(r'objective enclosure: \[([^,]+), ([^\]]+)\]', t).groups())
    L = Q(J(R+'/open-instances-wave3/logs/powerflow0030p.sdpcert.json')['bound_exact']) if name.endswith('0030p') else Q(J(R+f'/open-instances-wave3/powerflow/ext/logs/{name}.bb3t.json')['LB_exact'])
    primal_min(name, p, hi); dual_min(name, d, L); gap(name, g, (hi-L)/L, 'rel (/dual)'); print('    rel /primal', F((hi-L)/lo))
    ud = Q(str(Decimal(hi.numerator)/Decimal(hi.denominator))[:len(p)]) + Q(1,10**10)
    print('    minimal upward 10-dp display:', str(Decimal(hi.numerator)/Decimal(hi.denominator))[:len(p)], '+1e-10 ->', D(ud,16))

print('== eg (objvar of the exactly feasible retry points; dual = verifier decimal target) ==')
for name, p, d in [('eg_int_s','6.4531031593842275','6.4531031529331155'),('eg_disc_s','5.7605396164535107','5.760539610694994'),('eg_disc2_s','5.6421005799711068','5.642100574331458')]:
    pt = dict(l.split() for l in open(R+f'/open-instances-wave3/eg/retry/sol/{name}.retry.sol') if l.strip())
    f = Q(pt['objvar']); primal_min(name, p, f, f'objvar={pt["objvar"]}')
    gap(name, '1.0e-9', (f-Q(d))/Q(d), 'rel (/dual)')

print('== waterno2 (exact rational objectives; recomputed in recompute_objs.py) ==')
wd = {'06':Q(J(R+'/open-instances-wave2/waterno2/cellslopes/logs/certB_verify.json')['bound_exact'])}
for n in ('09','12','18','24'): wd[n] = Q(J(R+f'/open-instances-wave2/waterno2/logs/cert_{n}_w1_impl.json')['certified_bound_exact'])
rows = {'06':('282.888038','278.230573','1.68%'),'09':('914.012','824.834692','10.82%'),'12':('2233.821346','2089.754565','6.90%'),'18':('5023.983','4790.820715','4.87%'),'24':('6963.795181','6576.151388','5.90%')}
for n,(p,d,g) in rows.items():
    f = Q(J(P+f'/primal/water-ann-kan/points/waterno2_{n}.exact.json')['objective'])
    primal_min(f'waterno2_{n}', p, f); dual_min(f'waterno2_{n}', d, wd[n]); gap(f'waterno2_{n}', g, (f-wd[n])/wd[n], 'rel (/dual)')
    print('    gap using displays', F((Q(p)-Q(d))/Q(d)))
f06 = Q(J(P+'/primal/water-ann-kan/points/waterno2_06.exact.json')['objective'])
for d, g, lab in [('272.584700','3.78%','sepbranch'),('263.735099','7.26%','wave2')]:
    gap(f'waterno2_06 {lab}', g, (f06-Q(d))/Q(d), 'rel (/displayed dual)')
dual_min('waterno2_06','278.230573774', wd['06'], '(line 82)'); gap('waterno2_06 l82/186', '1.67%', (f06-wd['06'])/wd['06'], 'rel')

print('== ann_cumene_tanh ==')
v = J(P+'/primal/water-ann-kan/points/ann_cumene_tanh.point.json')
lo, hi = Q(v['objective_lo']), Q(v['objective_hi']); L = Q(v['dual_bound'])
print('    f in', D(lo,20), D(hi,20), ' dual cert', D(L,20))
primal_min('ann_cumene_tanh','-3379.9823940',hi); report('ann','old primal invalid','-3379.9824',Q('-3379.9824')<lo)
dual_min('ann_cumene_tanh','-3386.5403',L)
gap('ann 0.194% /|primal|','0.194%',(hi-L)/abs(hi),'rel (/|primal|, f_hi)'); gap('ann 0.194% /|dual|','0.194%',(hi-L)/abs(L),'rel (/|dual|)')
w3 = Q('-4024.495'); gap('ann wave3 /|primal|','19%',(hi-w3)/abs(hi)); gap('ann wave3 /|dual|','16.0%',(hi-w3)/abs(w3))

print('== other summary rows (scan) ==')
lk = Q('352.238025405078455654095')  # verifier lo(bound) 64b, below the stated exact cert 352.238025405078455701737
lkhi = Q('352.2380254064956226308712710293664647979979')
primal_min('lukvle10','352.2380254064961',lkhi); dual_min('lukvle10','352.2380254050784',lk); gap('lukvle10','1.4e-9',lkhi-lk)
v = J(R+'/reviews/bangbang-verification/logs/primal_check.json')['rigorous_primal']
oh = Q(re.search(r'\[([^,]+),', v['J_upper'])[1]); oc = Q(J(R+'/reviews/bangbang-verification/logs/qcal_exact.json')['bound_str'])/10**20
primal_min('optcdeg2','293.87607509587509328',oh); dual_min('optcdeg2','293.87607509587509',oc,f'cert={D(oc,24)} (cell says "exact value")'); gap('optcdeg2','9.0e-16',oh-oc)
v = J(R+'/reviews/wave2-small-verification/logs/etamac.json')
eh = Q(re.search(r'\[([^,]+),', eval(v['own_primal'])['objective'][1] if isinstance(v['own_primal'],str) else v['own_primal']['objective'][1])[1])
ed = Q(v['bound']['dual_bound'] if isinstance(v['bound'],dict) else eval(v['bound'])['dual_bound'])
dual_min('etamac','-15.294675643368093',ed); gap('etamac','2.6e-15',eh-ed)
v = J(R+'/reviews/wave2-small-verification/logs/pricing050.json')
o20 = Q(v['own_primal']['objective_20']); ub = Q(v['certificate']['upper_bound'])
report('pricing050','primal (max) <= f_lo','-1813.8290784519731', Q('-1813.8290784519731') <= o20 - Q(1,10**16), f'f~{v["own_primal"]["objective_20"]}')
mu = v.get('multipliers'); 
muR = Q(mu['e5'])*Q(-788)+Q(mu['e6'])*Q(-984); UBx = muR - Q(v['certificate']['sum_minF_certified'])
print('    pricing UB exact (muR - sum_minF_certified) =', D(UBx,30), ' display', '-1813.8290784519730577', 'display >= UB:', Q('-1813.8290784519730577') >= UBx)
print('    pricing gap UB - f: using objective_20 +-0.5e-16:', F(UBx-o20-Q(1,2*10**16)), '..', F(UBx-o20+Q(1,2*10**16)), '(cell 1.0e-17)')
t = open(R+'/reviews/pindyck-review-checks/logs/primal_check.txt').read(); pf = Q(re.search(r'objective \(min form\) = (\S+)', t)[1])
primal_min('pindyck','-1170.486285436088562',pf+Q(1,10**36)); gap('pindyck','5.44e-14',pf+Q(1,10**36)-Q('-1170.4862854360886163932'))
for v in J(R+'/reviews/open-instances-verification/logs/camshape_verify.json'):
    b = Q(v['bound']); u = Q(1,10**len(v['bound'].split('.')[1]))
    s = {'100':'-4.28414712174675','200':'-4.27850023299273','400':'-4.27568847892555','800':'-4.27427414195420'}[str(v['n'])]
    dual_min('camshape'+str(v['n']), s, b-u)
