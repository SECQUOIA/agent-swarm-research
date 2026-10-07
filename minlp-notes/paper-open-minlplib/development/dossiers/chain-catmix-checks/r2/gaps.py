from pathlib import Path as _PublicPath
_PUBLIC_REPO = str(_PublicPath(__file__).resolve().parents[5])

import json, re
from fractions import Fraction as F
from decimal import Decimal, getcontext, ROUND_FLOOR, ROUND_CEILING
getcontext().prec = 60
R = (_PUBLIC_REPO + '/research-20260929/')
def dual_from(path):
    s = open(path).read()
    m = re.findall(r'"dual_bound": *(-?[0-9.e-]+)', s)
    assert len(m) == 1, (path, m)
    return m[0]
def fdec(x, digits, mode):
    d = Decimal(x.numerator) / Decimal(x.denominator)
    q = Decimal(1).scaleb(-digits)
    return d.quantize(q, rounding=mode)
def up_sig(x, sig=3):
    # round positive fraction x upward to `sig` significant digits
    d = Decimal(x.numerator) / Decimal(x.denominator)
    e = d.adjusted()
    q = Decimal(1).scaleb(e - sig + 1)
    return d.quantize(q, rounding=ROUND_CEILING)
# catmix: certified duals of record (stronger, verifier code) and author duals
cat = {
 100: (R+'reviews/cops-verification/logs/catmix100_cfgB.log', R+'open-instances-wave2/cops/logs/catmix100_bound_1e-05_200_1e-07_band0.0685_0.0725_1e-06.json', F(-48069432030959562924734533987, 10**30), 'authors point (ceil 1e-30)'),
 200: (R+'reviews/cops-verification/logs/catmix200_cfgA.log', R+'open-instances-wave2/cops/logs/catmix200_bound_1e-05_200_1e-07_band0.0685_0.0725_1e-06.json', F(-48059145580114393563745030822, 10**30), 'authors point'),
 400: (R+'reviews/catmix-recheck-checks/logs/catmix400_final.log', R+'open-instances-wave2/cops/logs/catmix400_bound_1e-05_200_1e-07_band0.0685_0.0725_1e-06.json', F(-48056547756611554855186829086, 10**30), 'authors point (now exact)'),
 800: (R+'reviews/catmix-recheck-checks/logs/catmix800_final.log', R+'open-instances-wave2/cops/logs/catmix800_bound_1e-05_200_1e-07_band0.0685_0.0725_1e-06.json', F(-48055901331230800339383491203, 10**30), 'recheck policy point'),
}
newton100 = F(-48069432030979599106538896272, 10**30)
solu = {100: '-0.0480693911', 200: '-0.0480591228', 400: '-0.0480565180', 800: '-0.0480558393',
        50: '5.0722614940', 'c100': '5.0697846110', 'c200': '5.0689173420', 'c400': '5.0686216950'}
page = {100: '-0.04806939', 200: '-0.04805912', 400: '-0.04805652', 800: '-0.04805584'}
for N, (pv, pa, prim, lab) in cat.items():
    sv, sa = dual_from(pv), dual_from(pa)
    dv, da = F(float(sv)), F(float(sa))
    print('catmix%d verifier dual %s exact %s  display<=double? %s  safe17 %s' % (N, sv, fdec(dv, 40, ROUND_FLOOR), F(sv) <= dv, fdec(dv, 18, ROUND_FLOOR)))
    print('          authors dual %s  display<=double? %s;  verifier - authors = %.3e' % (sa, F(sa) <= da, float(dv - da)))
    g = prim - dv
    print('          gap (%s) = %.6e -> <= %s ; rel(|d|) = %.4e -> <= %s ; vs authors dual %.4e' % (lab, float(g), up_sig(g), float(g / -dv), up_sig(g / -dv), float(prim - da)))
    print('          primal upper display (19 dp, ceil) %s' % fdec(prim, 19, ROUND_CEILING))
    sl = F(solu[N]); pg = F(page[N])
    print('          listed solu %s - ours = %.4e (>= %.4e allowing +-5e-11);  page %s - ours = %.4e (>= %.4e if truncated toward 0)' % (
        solu[N], float(sl - prim), float(sl - F(5, 10**11) - prim), page[N], float(pg - prim), float(pg - F(1, 10**8) - prim)))
    print('          13-sig dual display (floor):', fdec(dv, 14, ROUND_FLOOR))
g100n = newton100 - F(float(dual_from(cat[100][0])))
print('catmix100 Newton-point gap %.6e' % float(g100n))
# chain
chain = {}
for N in (50, 100, 200, 400):
    d = json.load(open(R+'open-instances-wave2/cops/logs/chain%d_bound.json' % N))
    b = F(d['bnb']['bound']); assert d['bnb']['unresolved'] == 0
    box = json.load(open(R+'publication/primal/chain/points/chain%d_box.json' % N))
    lo, hi = (F(Decimal(s)) for s in box['objective_enclosure_decimal'])
    safe = {50: '5.0722614939828627', 100: '5.0697846107387505', 200: '5.0689173417931616', 400: '5.068621694604009'}[N]
    assert F(safe) <= b
    print('chain%d double %s safe %s; gap vs double %.4e -> <=%s; vs safe %.4e -> <=%s (2sig %s); rel %.4e -> <= %s; primal hi ceil19 %s' % (
        N, fdec(b, 25, ROUND_FLOOR), safe, float(hi - b), up_sig(hi - b), float(hi - F(safe)), up_sig(hi - F(safe)), up_sig(hi - F(safe), 2), float((hi - F(safe)) / F(safe)), up_sig((hi - F(safe)) / F(safe)), fdec(hi, 19, ROUND_CEILING)))
    key = 50 if N == 50 else 'c%d' % N
    sl = F(solu[key])
    print('        listed solu %s - our primal hi = %.4e ; - (5e-11 rounding) = %.4e' % (solu[key], float(sl - hi), float(sl - F(5, 10**11) - hi)))
    pagev = {50: '5.07226149', 100: '5.06978461', 200: '5.06891734', 400: '5.0686217'}[N]
    print('        page %s ; our optimum interval rounded to 8 dp: [%s, %s]' % (pagev, fdec(b, 8, ROUND_FLOOR).quantize(Decimal('1e-8')), fdec(hi, 8, ROUND_CEILING)))
