# Independent exact recomputation of primal displays and gaps (dossier check).
import json, gzip
from fractions import Fraction as F
from decimal import Decimal
def D(s): return F(Decimal(s))
def up(x, sig=3):
    # round positive Fraction x upward to `sig` significant digits; return string
    from math import floor, log10
    e = floor(log10(float(x)))
    q = F(10)**(e - sig + 1)
    n = -((-x) // q)  # ceil
    return f"{float(n*q):.{sig-1}e}"
out = []
def rec(*a): print(*a); out.append(' '.join(map(str,a)))
# lnts
summ = ['0.5546687649381','0.5545954011663','0.5545770161025','0.5545724137001']
ver  = ['0.5546687649381242','0.5545954011663565','0.5545770161025290','0.5545724137001325']
pdisp= ['0.5546687649387','0.5545954011670','0.5545770161031','0.5545724137007']
for i,N in enumerate([50,100,200,400]):
    d = json.load(open(f'data/lnts{N}_point.json'))
    lo, hi = [D(s) for s in eval(d['objective_enclosure'])] if isinstance(d['objective_enclosure'], str) else [D(s) for s in d['objective_enclosure']]
    g1 = hi - D(summ[i]); g2 = hi - D(ver[i])
    rec(f'lnts{N}: f in [{float(lo)!r}, ...], width {float(hi-lo):.1e}; primal display {pdisp[i]} >= f_hi: {D(pdisp[i])>=hi}; '
        f'gap vs summary dual <= {up(g1)} (rel {up(g1/D(summ[i]))}); gap vs verifier display <= {up(g2)}')
# dtoc5
f = F(open('data/dtoc5_check_objective_exact.txt').read().strip())
rec(f'dtoc5: f = {float(f)!r}; display 5.389672119181141 >= f: {D("5.389672119181141")>=f}; old display 5.38967211918114 >= f: {D("5.38967211918114")>=f}; '
    f'gap vs 5.38967211918114 <= {up(f-D("5.38967211918114"))}; gap vs verifier 5.38967211918114046742396472386 <= {up(f-D("5.38967211918114046742396472386"))}')
# lukvle10
L = json.load(open('data/lukvle10_enclose.json'))
lo, hi = D(L['objective_box'][0]), D(L['objective_box'][1])
rec(f'lukvle10: f_hi {L["objective_box"][1]}; display 352.2380254064961 >= f_hi: {D("352.2380254064961")>=hi}; gap <= {up(hi-D("352.2380254050784"))} (rel {up((hi-D("352.2380254050784"))/D("352.2380254050784"))}); '
    f'listed p5 display 352.2380254064961 - f_hi = {float(D("352.2380254064961")-hi):.3e}')
# chain
safe = {50:'5.0722614939828627',100:'5.0697846107387505',200:'5.0689173417931616',400:'5.068621694604009'}
dbl  = {50:5.072261493982863,100:5.0697846107387505,200:5.068917341793162,400:5.068621694604009}
for N in [50,100,200,400]:
    d = json.load(open(f'data/chain{N}_box.json'))
    oe = d['objective_enclosure_decimal']; oe = eval(oe) if isinstance(oe,str) else oe; lo, hi = [D(s) for s in oe]
    Ld = F(dbl[N]); Ls = D(safe[N])
    rec(f'chain{N}: f_hi {float(hi)!r}; safe display <= double: {Ls<=Ld}; gap vs double <= {up(hi-Ld)}; gap vs safe display <= {up(hi-Ls)} (rel {up((hi-Ls)/Ls)})')
# powerflow
pf = {'powerflow0030p':('576.8934122988004','576.8934134704','[576.8934134703742598676683, 576.8934134703742598676684]'),
      'powerflow0039p':('41869.05148485014','41869.0515113203','[41869.0515113202038027683844, 41869.0515113202038027683845]'),
      'powerflow0039r':('41869.05148327243','41869.0515113210','[41869.0515113209830932768581, 41869.0515113209830932768582]')}
for k,(dl,pd,enc) in pf.items():
    lo, hi = [D(s.strip()) for s in enc.strip('[]').split(',')]
    g = hi - D(dl)
    rec(f'{k}: display {pd} >= f_hi: {D(pd)>=hi}; gap <= {up(g)} abs, rel(dual) <= {up(g/D(dl),2)}')
# water
wd = {'06':'278.230573','09':'824.834692','12':'2089.754565','18':'4790.820715','24':'6963.795181'}
wd['24']='6576.151388'
wdisp = {'06':'282.888038','09':'914.012','12':'2233.821346','18':'5023.983','24':'6963.795181'}
for t in ['06','09','12','18','24']:
    d = json.load(open(f'data/waterno2_{t}.exact.json'))
    f = F(d['objective'])
    g = f - D(wd[t])
    rec(f'waterno2_{t}: f = {float(f)!r}; display {wdisp[t]} >= f: {D(wdisp[t])>=f}; gap/|dual display| = {float(100*g/D(wd[t])):.5f}% -> up {up(100*g/D(wd[t]),3)}%')
# ann & kan
for k in ['ann_cumene_tanh','kan_r3_h1_n4','kan_r3_h1_n5','kan_r3_h1_n9','kan_r5_h1_n3','kan_r5_h1_n5','kan_r5_h1_n8']:
    d = json.load(open(f'data/{k}.point.json'))
    hi = D(d['objective_hi']) if 'e' in d['objective_hi'] or '.' in d['objective_hi'] else F(d['objective_hi'])
    lo = D(d['objective_lo'])
    du = F(d['dual_bound'])
    g = hi - du
    extra = ''
    if k.startswith('ann'):
        extra = f'; display -3379.9823940 >= f_hi: {D("-3379.9823940")>=hi}; gap/|primal| <= {up(100*g/abs(hi),3)}%, gap/|dual| <= {up(100*g/abs(du),3)}%; dual display -3386.5403 <= dual: {D("-3386.5403")<=du}'
    rec(f'{k}: f in [{float(lo)!r}], width {float(hi-lo):.1e}; dual {float(du)!r}; gap <= {up(g)}{extra}')
open('gaps_check.log','w').write('\n'.join(out)+'\n')
