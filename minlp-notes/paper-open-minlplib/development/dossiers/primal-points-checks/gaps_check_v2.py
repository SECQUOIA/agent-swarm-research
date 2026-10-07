"""Exact recomputation of primal displays and gaps (dossier primal-points v2)."""
import json
from fractions import Fraction as Fr
from math import floor, log10
def up(x, sig):
    e = floor(log10(float(x))); q = Fr(10) ** (e - sig + 1); n = -((-x) // q); return n * q
def s(x, sig=3): return f"{float(up(x, sig)):.{sig-1}e}"
R = lambda t: Fr(t)
rows = []
# lnts: (summary dual display, verifier N*h2 display, summary primal display)
L = {50: ('0.5546687649381', '0.5546687649381242', '0.5546687649387'),
     100: ('0.5545954011663', '0.5545954011663565', '0.5545954011670'),
     200: ('0.5545770161025', '0.5545770161025290', '0.5545770161031'),
     400: ('0.5545724137001', '0.5545724137001325', '0.5545724137007')}
for N, (dd, dv, pd) in L.items():
    lo, hi = map(R, json.load(open(f'data/lnts{N}_point.json'))['objective_enclosure'])
    print(f'lnts{N}: primal display >= f_hi {R(pd) >= hi}; gap(summary dual) {s(hi-R(dd))}; gap(verifier) {s(hi-R(dv))}; enclosure width {float(hi-lo):.1e}')
f = R(open('data/dtoc5_check_objective_exact.txt').read().strip())
print(f'dtoc5: denominator digits {len(str(f.denominator))}; display 5.389672119181141 >= f {R("5.389672119181141") >= f}; '
      f'old 5.38967211918114 >= f {R("5.38967211918114") >= f}; gap {s(f-R("5.38967211918114"),4)}; vs verifier lower end {s(f-R("5.38967211918114046742396472386"),4)}')
d = json.load(open('data/lukvle10_enclose.json')); lo, hi = map(R, d['objective_box'])
print(f'lukvle10: display 352.2380254064961 >= f_hi {R("352.2380254064961") >= hi}; gap {s(hi-R("352.2380254050784"),4)} rel {s((hi-R("352.2380254050784"))/R("352.2380254050784"),4)}')
safe = {50: '5.0722614939828627', 100: '5.0697846107387505', 200: '5.0689173417931616', 400: '5.068621694604009'}
for N in (50, 100, 200, 400):
    Ld = Fr(json.load(open(f'data/chain{N}_bound.json'))['bnb']['bound'])  # exact double
    b = json.load(open(f'data/chain{N}_box.json'))
    oe = b['objective_enclosure_decimal']; oe = eval(oe) if isinstance(oe, str) else oe
    lo, hi = map(R, oe)
    print(f'chain{N}: safe display <= L {R(safe[N]) <= Ld}; shortest repr {repr(float(Ld))} > L by {float(R(repr(float(Ld)))-Ld):.3e}; '
          f'gap vs L {s(hi-Ld)}; gap vs safe {s(hi-R(safe[N]))}; rel vs safe {s((hi-R(safe[N]))/R(safe[N]))}')
pf = {'0030p': ('576.8934122988004', '576.8934134704', '576.8934134703742598676684'),
      '0039p': ('41869.05148485014', '41869.0515113203', '41869.0515113202038027683845'),
      '0039r': ('41869.05148327243', '41869.0515113210', '41869.0515113209830932768582')}
for k, (dl, pd, hi) in pf.items():
    g = R(hi) - R(dl)
    print(f'powerflow{k}: display >= f_hi {R(pd) >= R(hi)}; gap abs {s(g,10)}; rel/dual {s(g/R(dl),4)}')
wd = {'06': Fr('39157472136693483/140737488355328'), '09': Fr('3627661341387654598825371/4398046511104000000000'),
      '12': Fr('9190837775594918144252281/4398046511104000000000'), '18': Fr('5267563083146225483626937/1099511627776000000000'),
      '24': Fr('115688878681251187594323079/17592186044416000000000')}
wdisp = {'06': ('278.230573', '282.888038', '1.68'), '09': ('824.834692', '914.012', '10.82'), '12': ('2089.754565', '2233.821346', '6.90'),
         '18': ('4790.820715', '5023.983', '4.87'), '24': ('6576.151388', '6963.795181', '5.90')}
for t, D in wd.items():
    p = R(json.load(open(f'data/waterno2_{t}.exact.json'))['objective'])
    dd, pd, gd = wdisp[t]
    pct = 100 * (p - D) / abs(D)
    pct_disp = 100 * (R(pd) - R(dd)) / R(dd)
    print(f'waterno2_{t}: dual display <= exact {R(dd) <= D}; primal display >= p {R(pd) >= p}; gap% exact {float(pct):.5f} <= {gd}: {pct <= R(gd)}; via displays {float(pct_disp):.5f} <= {gd}: {pct_disp <= R(gd)}')
for k in ['ann_cumene_tanh', 'kan_r3_h1_n4', 'kan_r3_h1_n5', 'kan_r3_h1_n9', 'kan_r5_h1_n3', 'kan_r5_h1_n5', 'kan_r5_h1_n8']:
    d = json.load(open(f'data/{k}.point.json'))
    lo, hi, du = R(d['objective_lo']), R(d['objective_hi']), R(d['dual_bound'])
    g = hi - du
    extra = ''
    if k.startswith('ann'):
        extra = (f'; display -3379.9823940 >= hi {R("-3379.9823940") >= hi}; gap/|primal| {float(100*g/abs(hi)):.5f}% gap/|dual| {float(100*g/abs(du)):.5f}%;'
                 f' dual display -3386.5403 <= dual {R("-3386.5403") <= du}; abs gap {s(g,6)}')
    print(f'{k}: width {float(hi-lo):.1e}; gap {s(g,3)}{extra}')
