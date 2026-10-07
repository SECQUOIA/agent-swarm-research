"""Read-only exact check of lnts displays (issues 1, 8, 9)."""
from pathlib import Path as _PublicPath
_PUBLIC_REPO = str(_PublicPath(__file__).resolve().parents[5])

import json
from fractions import Fraction as F
from decimal import Decimal
R = (_PUBLIC_REPO + '/research-20260929/')
P = R + 'publication/primal/lnts/points/'
V = json.load(open(R + 'reviews/open-instances-verification/logs/lnts_verify.json'))
summary_dual = {50: '0.5546687649381', 100: '0.5545954011663', 200: '0.5545770161025', 400: '0.5545724137001'}
safe = {50: '0.5546687649381242', 100: '0.5545954011663565', 200: '0.5545770161025290', 400: '0.5545724137001325'}
summary_primal = {50: '0.5546687649387', 100: '0.5545954011669', 200: '0.5545770161031', 400: '0.5545724137007'}
def sig_halfulp(s):
    # half a unit in the last printed digit of a decimal string
    d = Decimal(s); exp = d.as_tuple().exponent
    return F(1, 2) * F(10) ** exp
def e(x): return '%.6e' % float(x)
for v in V:
    N = int(v['name'][4:])
    pt = json.load(open(P + f'lnts{N}_point.json'))
    lo, hi = (F(Decimal(x)) for x in pt['objective_enclosure'])
    h2s = v['cert_1e-12']['h2']
    h2 = F(Decimal(h2s)); hu = sig_halfulp(h2s)
    # nstr(h2,20) gives 20 significant digits with trailing zeros stripped; bound the
    # true h2 by +-0.5 unit of the 20th significant digit
    d = Decimal(h2s); digits = len(d.as_tuple().digits); exp = d.as_tuple().exponent
    unit20 = F(10) ** (exp + digits - 20)
    hu20 = unit20 / 2
    Nh2_lo = N * (h2 - hu20); Nh2_hi = N * (h2 + hu20)
    # cross-check h2 from h_star (25 sig digits)
    hs = F(Decimal(v['h_star'])); hs_u = F(10) ** (Decimal(v['h_star']).as_tuple().exponent) / 2
    h2_from_hs_lo = (hs - hs_u) * (1 - F(1, 10**12)); h2_from_hs_hi = (hs + hs_u) * (1 - F(1, 10**12))
    s = F(Decimal(safe[N])); b = F(Decimal(v['cert_1e-12']['bound']))
    print(f'lnts{N}: h2 str={h2s} sigdigits={digits} unit20={e(unit20)}')
    print('  h2 from h_star in [%s, %s]; printed h2 consistent: %s' % (e(h2_from_hs_lo - h2), e(h2_from_hs_hi - h2), h2_from_hs_lo - hu20 <= h2 <= h2_from_hs_hi + hu20))
    print('  N*h2 in [%s, %s] (width %s)' % (float(Nh2_lo), float(Nh2_hi), e(Nh2_hi - Nh2_lo)))
    print('  safe display %s <= N*h2_lo: %s  margin %s' % (safe[N], s <= Nh2_lo, e(Nh2_lo - s)))
    print('  verifier bound field %s <= N*h2_lo: %s  diff %s' % (v['cert_1e-12']['bound'], b <= Nh2_lo, e(b - Nh2_lo)))
    sd = F(Decimal(summary_dual[N])); sp = F(Decimal(summary_primal[N]))
    print('  summary dual <= N*h2_lo: %s; summary primal %s >= f_hi: %s (diff %s)' % (sd <= Nh2_lo, summary_primal[N], sp >= hi, e(sp - hi)))
    print('  0.5545954011670 >= f_hi:', F(Decimal('0.5545954011670')) >= hi if N == 100 else '-')
    g_cert = hi - Nh2_lo; g_safe = hi - s; g_sum = hi - sd
    print('  gap vs N*h2 (upper) %s rel(/N*h2) %s rel(/f) %s' % (e(g_cert), e(g_cert / Nh2_lo), e(g_cert / lo)))
    print('  gap vs safe display %s rel(/disp) %s rel(/f) %s' % (e(g_safe), e(g_safe / s), e(g_safe / lo)))
    print('  gap vs summary dual %s rel(/disp) %s rel(/f) %s' % (e(g_sum), e(g_sum / sd), e(g_sum / lo)))
    for name, g in (('cert', g_cert), ('safe', g_safe)):
        print('   ', name, '<=5.55e-13:', g <= F(555, 10**15), ' rel/disp<=1.01e-12:', g / (Nh2_lo if name == 'cert' else s) <= F(101, 10**14))
