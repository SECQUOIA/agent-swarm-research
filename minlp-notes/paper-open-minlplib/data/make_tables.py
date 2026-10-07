#!/usr/bin/env python3
"""Build data/numbers.json, run every number check and write the LaTeX tables.

Usage (from anywhere):  python3 paper-open-minlplib/data/make_tables.py

The script only READS files under research-20260929/ (R) and
paper-open-minlplib/development/ (D). It imports no project module and runs no
certificate or search. It writes exactly these files:
  paper-open-minlplib/data/numbers.json
  paper-open-minlplib/data/check.log
  paper-open-minlplib/tables/tab-*.tex

Every certified bound, primal, gap and margin display that this script
generates is checked with exact rational arithmetic (Fraction) against the exact
value or enclosure it summarises:
  dual bounds rounded down (up for the maximisation instance pricing050),
  primal values rounded up (down for pricing050), gaps rounded up,
  "at least" margins and improvement factors rounded down.
Hand-written tables in the LaTeX sources and the fixed text of the qualitative
tables below (TRUST, STAGED, POINTS13) are checked separately; where a fixed cell
holds a number, a check() below compares it with its source.
The script stops with a non-zero exit code if any check fails.
"""
import csv
import hashlib
import json
import math
import re
import sys
from datetime import date, datetime
from fractions import Fraction as Q
from pathlib import Path

HERE = Path(__file__).resolve().parent
P = HERE.parent                                   # paper-open-minlplib
ROOT = P.parent                                   # repository root
R = ROOT / 'research-20260929'
D = P / 'development'
TAB = P / 'tables'

# ---------------------------------------------------------------- utilities
SOURCES = {}
CHECKS = []          # (ok, label, detail)
FAILS = []


def rel(path):
    return str(Path(path).resolve().relative_to(ROOT))


def read(path):
    path = Path(path)
    data = path.read_bytes()
    SOURCES[rel(path)] = hashlib.sha256(data).hexdigest()
    return data.decode()


def J(path):
    return json.loads(read(path))


def q(s):
    """Exact rational from a decimal or fraction string (Unicode minus allowed)."""
    if isinstance(s, (int, Q)):
        return Q(s)
    s = str(s).strip().replace('−', '-').replace('+', '')
    return Q(s)


def qf(s):
    """Exact value of the binary64 number written as s."""
    return Q(float(str(s).replace('−', '-')))


def check(label, ok, detail=''):
    ok = bool(ok)
    CHECKS.append((ok, label, detail))
    if not ok:
        FAILS.append(label)
    return ok


def e10(x):
    """floor(log10(x)) for a positive Fraction, exactly."""
    x = Q(x)
    assert x > 0
    e = len(str(x.numerator)) - len(str(x.denominator))
    while Q(10) ** e > x:
        e -= 1
    while Q(10) ** (e + 1) <= x:
        e += 1
    return e


def sig(x, s=3, up=True):
    """Round a positive Fraction to s significant digits (up or down).
    Returns (exact rounded value, string like '7.21e-43')."""
    x = Q(x)
    if x == 0:
        return Q(0), '0'
    assert x > 0, x
    e = e10(x)
    unit = Q(10) ** (e - s + 1)
    m = x / unit
    mi = math.ceil(m) if up else math.floor(m)
    val = mi * unit
    if mi == 10 ** s:            # carry (only when rounding up)
        mi //= 10
        e += 1
    d = str(mi)
    mant = d[0] + ('.' + d[1:] if len(d) > 1 else '')
    return val, f'{mant}e{e}'


def fixed(x, k, up):
    """Round x to k decimals, up (toward +inf) or down (toward -inf); return (value, string)."""
    x = Q(x)
    n = math.ceil(x * 10 ** k) if up else math.floor(x * 10 ** k)
    v = Q(n, 10 ** k)
    sgn = '-' if n < 0 else ''
    a = str(abs(n)).rjust(k + 1, '0')
    s = sgn + (a[:-k] + '.' + a[-k:] if k > 0 else a)
    return v, s


def pct(x, up=True, s=3):
    """Percent display of a ratio x: two decimals, or s significant digits if that needs more."""
    p = Q(x) * 100
    k = max(2, s - 1 - e10(p))
    v, st = fixed(p, k, up)
    return v / 100, st + '%'


def ndec(s):
    s = str(s)
    return len(s.split('.')[1]) if '.' in s else 0


def dec40(x, k=40):
    """Truncated decimal string of a Fraction (for human reading only)."""
    x = Q(x)
    sgn = '-' if x < 0 else ''
    x = abs(x)
    n = math.floor(x * 10 ** k)
    a = str(n).rjust(k + 1, '0')
    return sgn + a[:-k] + '.' + a[-k:]


def fr(x):
    x = Q(x)
    return f'{x.numerator}/{x.denominator}' if x.denominator != 1 else str(x.numerator)


def last_iv_upper(text):
    """mpmath prints iv enclosures as '[a, a] [b, b]' (lower, upper); return b."""
    m = re.findall(r'\[([^,\]]+),\s*([^\]]+)\]', text)
    return q(m[-1][1])


def first_iv_lower(text):
    m = re.findall(r'\[([^,\]]+),\s*([^\]]+)\]', text)
    return q(m[0][0])


# ------------------------------------------------------------ instance list
CLOSED = ['lnts50', 'lnts100', 'lnts200', 'lnts400', 'dtoc5', 'optcdeg2',
          'lukvle10', 'chain50', 'chain100', 'chain200', 'chain400',
          'catmix100', 'catmix200', 'catmix400', 'catmix800',
          'camshape100', 'camshape200', 'camshape400', 'camshape800',
          'ex6_2_5', 'ex6_2_7', 'pricing050', 'etamac', 'pindyck',
          'powerflow0030p', 'powerflow0039p', 'powerflow0039r', 'hvycrash',
          'eg_int_s', 'eg_disc_s', 'eg_disc2_s']
WATER = ['waterno2_06', 'waterno2_09', 'waterno2_12', 'waterno2_18', 'waterno2_24']
KAN = ['kan_r3_h1_n4', 'kan_r3_h1_n5', 'kan_r3_h1_n9', 'kan_r5_h1_n3', 'kan_r5_h1_n5', 'kan_r5_h1_n8']
OTHER = WATER + ['ann_cumene_tanh'] + KAN
ALL = CLOSED + OTHER


def family(n):
    for pre, fam in [('lnts', 'lnts'), ('dtoc5', 'dtoc5'), ('optcdeg2', 'optcdeg2'),
                     ('lukvle10', 'lukvle10'), ('chain', 'chain'), ('catmix', 'catmix'),
                     ('camshape', 'camshape'), ('ex6_2', 'ex6_2'), ('pricing050', 'pricing050'),
                     ('etamac', 'etamac'), ('pindyck', 'pindyck'), ('powerflow', 'powerflow'),
                     ('hvycrash', 'hvycrash'), ('eg_', 'eg'), ('waterno2', 'waterno2'),
                     ('ann_', 'ann'), ('kan_', 'kan')]:
        if n.startswith(pre):
            return fam
    raise KeyError(n)


# ------------------------------------------------------- OSIL sizes, sense
OSIL_DIR = R / 'publication/minlplib-status/pages/models/osil'


def osil_info(n):
    path = OSIL_DIR / f'{n}.osil'
    text = read(path)
    nv = int(re.search(r'<variables numberOfVariables="(\d+)"', text).group(1))
    m = re.search(r'<constraints numberOfConstraints="(\d+)"', text)
    nc = int(m.group(1)) if m else 0
    ints = len(re.findall(r'<var [^>]*type="[BI]"', text))
    obj = re.search(r'<obj [^>]*>', text).group(0)
    sense = 'max' if 'maxOrMin="max"' in obj else 'min'
    return dict(variables=nv, integers=ints, rows=nc, sense=sense,
                osil=rel(path), osil_sha256=SOURCES[rel(path)])


# ----------------------------------------------------------- listed data
PAGES = {p['name']: p for p in J(R / 'bound-audit/pages.json')}


def listed(n):
    p = PAGES[n]
    s = p['sense']
    fin = [d for d in p['duals'] if d['value'].lower() not in ('inf', '-inf')]
    best = None
    if fin:
        best = (max if s == 'min' else min)(fin, key=lambda d: q(d['value']))
    pts = p['points']
    ok_pts = [x for x in pts if q(x['infeas']) <= q('1e-8')]
    bp = (min if s == 'min' else max)(ok_pts, key=lambda x: q(x['value'])) if ok_pts else None
    ap = (min if s == 'min' else max)(pts, key=lambda x: q(x['value'])) if pts else None
    return dict(
        best_dual=(dict(value=best['value'], solver=best['solver'], date=best['date'],
                        ties=[d['solver'] for d in fin if q(d['value']) == q(best['value'])])
                   if best else None),
        n_dual_entries=len(p['duals']),
        listing_dual=p['listing_dual'] or None,
        listing_primal=p['listing_primal'] or None,
        best_point=(dict(point=bp['point'], value=bp['value'], violation=bp['infeas'],
                         section=bp['section']) if bp else None),
        best_point_any=(dict(point=ap['point'], value=ap['value'], violation=ap['infeas'],
                             section=ap['section']) if ap else None),
        solved_mark=p['solved'],
        source='research-20260929/bound-audit/pages.json (pages fetched 2026-09-29/30; '
               'unchanged at the 2026-10-02 refresh)')


# =================================================== closed instances: data
# For each closed instance: exact certified dual value Lx (minimisation: a
# lower bound; pricing050: an upper bound), the end Ux of the primal objective
# enclosure on the unsafe side (upper end for min, lower end for max), the
# displays, and the sources. Exact optima: Lx, Ux are the ends of an enclosure
# of v*, and the gap is 0 by the theorem.
REC = {}


def put(n, **kw):
    REC[n] = kw


# ---- lnts (Theorem 4.6; independent review, integer-only code) -----------
LN = J(D / 'reviews/code/sol-lnts-review/certificate.json')
REG_LNTS = {50: ('0.5546687649386788', '0.5546687649386789'),
            100: ('0.5545954011669111', '0.5545954011669112'),
            200: ('0.5545770161030836', '0.5545770161030837'),
            400: ('0.5545724137006871', '0.5545724137006872')}
for N in (50, 100, 200, 400):
    r = next(r for r in LN['results'] if r['model']['N'] == N)
    lo, hi = map(q, r['opt_exact'])
    check(f'lnts{N}: review display_16 equals decision-register N-0x display',
          tuple(r['display_16']) == REG_LNTS[N])
    check(f'lnts{N}: review OSIL sha256 equals refreshed OSIL',
          r['model']['sha256'] == hashlib.sha256((OSIL_DIR / f'lnts{N}.osil').read_bytes()).hexdigest())
    check(f'lnts{N}: exact optimum enclosure width < 1.11e-91', hi - lo < q('1.11e-91') and hi > lo)
    put(f'lnts{N}', exact_opt=True, Lx=lo, Ux=hi,
        L=REG_LNTS[N][0], U=REG_LNTS[N][1],
        src_L='paper-open-minlplib/development/reviews/code/sol-lnts-review/certificate.json: '
              f'results[N={N}].opt_exact[0] (rational lower end of the optimum enclosure)',
        src_U='same file: opt_exact[1]',
        note='exact optimum N*h*, attained (Theorem 4.6; review sol-lnts-theorem3.md)')

# ---- dtoc5 (exact-rational certificate; review sol-dtoc5-exact.md) -------
DT = D / 'reviews/code/sol-dtoc5-review'
dres = J(DT / 'result.json')
d_lo = q(dres['decimal_enclosures']['dual']['down_100'])        # <= d(lambda) (full rational)
d_hi = q(dres['decimal_enclosures']['dual']['up_100'])
f_exact = q(read(DT / 'primal_exact.txt').strip())
f_ref = q(read(R / 'publication/primal/dtoc5-lukvle10/logs/dtoc5_check_objective_exact.txt').strip())
b256 = q(read(DT / 'dossier_lower_exact.txt').strip())
gap_up = q(dres['decimal_enclosures']['gap']['up_100'])
check('dtoc5: review primal rational equals primal-track objective', f_exact == f_ref)
check('dtoc5: dossier B_256 <= review dual lower end (both certify the display)', b256 <= d_lo)
check('dtoc5: primal - dual <= stored gap upper end', f_exact - d_lo <= gap_up + (d_hi - d_lo))
check('dtoc5: review safe displays equal outline/register strings',
      dres['safe_displays']['dual_down_44'] == '5.38967211918114046742396649913627186883131268'
      and dres['safe_displays']['primal_up_44'] == '5.38967211918114046742396649913627186883131341')
check('dtoc5: dossier B_256 also certifies the 44-decimal display',
      q('5.38967211918114046742396649913627186883131268') <= b256)
put('dtoc5', Lx=d_lo, Ux=f_exact,
    L='5.38967211918114046742396649913627186883131268',
    U='5.38967211918114046742396649913627186883131341',
    Lt='5.3896721191811404674', Ut='5.3896721191811404675',
    src_L='paper-open-minlplib/development/reviews/code/sol-dtoc5-review/result.json: '
          'decimal_enclosures.dual.down_100 (lower end of the full rational dual d(lambda)); '
          'dossier_lower_exact.txt (B_256) also certifies the display',
    src_U='paper-open-minlplib/development/reviews/code/sol-dtoc5-review/primal_exact.txt '
          '(= research-20260929/publication/primal/dtoc5-lukvle10/logs/dtoc5_check_objective_exact.txt)',
    note='certificate gap (exact primal minus rigorous rational dual) <= 7.21e-43; '
         'the 44-decimal displays have width 7.3e-43')

# ---- optcdeg2 -------------------------------------------------------------
qc = J(R / 'reviews/bangbang-verification/logs/qcal_exact.json')
L_opt = q(qc['bound_str']) / 10 ** 20
pcj = J(R / 'reviews/bangbang-verification/logs/primal_check.json')['rigorous_primal']
U_opt = q(re.match(r'\[([^,]+),\s*([^\]]+)\]', pcj['J_upper']).group(2))
rr = J(D / 'dossiers/checks/dtoc5-optcdeg2/rerun_reviewer_qcal_exact.json')
check('optcdeg2: critic rerun reproduces bound_str', rr.get('bound_str') == qc['bound_str'])
put('optcdeg2', Lx=L_opt, Ux=U_opt,
    L='293.87607509587509237', U='293.87607509587509328',
    src_L='research-20260929/reviews/bangbang-verification/logs/qcal_exact.json: bound_str/1e20 '
          '(truncation of the rigorous rational evaluation; rerun identical: '
          'paper-open-minlplib/development/dossiers/checks/dtoc5-optcdeg2/rerun_reviewer_qcal_exact.json)',
    src_U='research-20260929/reviews/bangbang-verification/logs/primal_check.json: '
          'rigorous_primal.J_upper (upper end); integer-interval re-proof optcdeg2_primal_int.log',
    note='do not print 293.87607509587509238 (rounded up)')

# ---- lukvle10 -------------------------------------------------------------
t = read(R / 'reviews/closing-confirm-r2-checks/logs/lukvle10_lower_end.log')
L_luk = q(re.search(r'prec 200 lo\(bound\) = \[([^,]+),', t).group(1))
le = J(R / 'publication/primal/dtoc5-lukvle10/logs/lukvle10_enclose.json')
U_luk = q(json.loads(le['objective_box'].replace("'", '"'))[1]) if isinstance(le['objective_box'], str) \
    else q(le['objective_box'][1])
bnb = J(R / 'reviews/open-instances-verification/logs/lukvle10_bnb.json')
check('lukvle10: verifier JSON dual 352.2380254050785 is above the certified lower end (unsafe string)',
      q(bnb['dual_bound']) > L_luk)
put('lukvle10', Lx=L_luk, Ux=U_luk, L='352.2380254050784', U='352.2380254064957',
    src_L='research-20260929/reviews/closing-confirm-r2-checks/logs/lukvle10_lower_end.log '
          '(prec 200 lower end of the verifier bound, v_lukvle10_bnb.py)',
    src_U='research-20260929/publication/primal/dtoc5-lukvle10/logs/lukvle10_enclose.json: objective_box[1]',
    note='never print 352.2380254050785 or 352.238025369202 as the dual')

# ---- chain (catenary calibration) ------------------------------------------
EDC = J(R / 'publication/reproduction/cops/logs/exact_display_checks.json')
REG_CHAIN = {50: ('5.0722614939828627', '5.0722614939828723165'),
             100: ('5.0697846107387505', '5.0697846107387605575'),
             200: ('5.0689173417931616', '5.0689173417931710002'),
             400: ('5.068621694604009', '5.0686216946040190144')}
for N in (50, 100, 200, 400):
    b = J(R / f'open-instances-wave2/cops/logs/chain{N}_bound.json')
    Lc = qf(b['bnb']['bound'])
    ver = next(x for x in EDC if x['instance'] == f'chain{N}' and x['source'].startswith('verifier'))
    check(f'chain{N}: author and verifier certify the same double', qf(ver['certified_double']) == Lc)
    box = J(R / f'publication/primal/chain/points/chain{N}_box.json')
    Uc = q(box['objective_enclosure_decimal'][1])
    put(f'chain{N}', Lx=Lc, Ux=Uc, L=REG_CHAIN[N][0], U=REG_CHAIN[N][1],
        src_L=f'research-20260929/open-instances-wave2/cops/logs/chain{N}_bound.json: bnb.bound '
              '(binary64, exact value); same double from v_chain_bnb.py (exact_display_checks.json)',
        src_U=f'research-20260929/publication/primal/chain/points/chain{N}_box.json: objective_enclosure_decimal[1]')

# ---- catmix (rigorous DP; verifier/recheck duals) ---------------------------
REG_CATMIX = {100: ('-0.048069432031144562', '-0.0480694320309595629'),
              200: ('-0.048059145599072769', '-0.0480591455801143935'),
              400: ('-0.048056547824671288', '-0.0480565477566115548'),
              800: ('-0.048055901479675652', '-0.0480559013312308003')}
for N in (100, 200, 400, 800):
    v = next(x for x in EDC if x['instance'] == f'catmix{N}' and x['source'].startswith('verifier dual'))
    Lc = qf(v['certified_double'])
    if N == 800:
        Uc = q(v['primal_hi'])
        srcU = 'exact_display_checks.json (verifier entry): primal_hi (reviewer DP-policy point, exact rational ceiling)'
    else:
        a = next(x for x in EDC if x['instance'] == f'catmix{N}' and x['source'].startswith('author catmix'))
        Uc = q(a['primal_hi'])
        srcU = 'exact_display_checks.json (author entry): primal_hi (upper end of the 60-digit enclosure of the authors\' exact point)'
    put(f'catmix{N}', Lx=Lc, Ux=Uc, L=REG_CATMIX[N][0], U=REG_CATMIX[N][1],
        src_L=f'research-20260929/publication/reproduction/cops/logs/exact_display_checks.json: '
              f'"{v["source"]}" certified_double (binary64, exact value)',
        src_U='research-20260929/publication/reproduction/cops/logs/' + srcU,
        note='displayed dual certified by one implementation (v_catmix_dp); the authors\' code certifies weaker bounds')
# catmix400 exact primal (dossier) must lie inside the stored enclosure end
cm400 = read(D / 'dossiers/primal-points-checks/logs/catmix400_author_exact.log')

# ---- camshape (exact optimum, Theorem 5.1) --------------------------------
CE = J(D / 'dossiers/checks/camshape/check_exact.json')
CV = J(R / 'reviews/open-instances-verification/logs/camshape_verify.json')
for n in (100, 200, 400, 800):
    c = next(x for x in CE if x['n'] == n)
    v30 = q(c['opt_30'])
    lo, hi = v30 - q('1e-30'), v30 + q('1e-30')
    vv = q(next(x for x in CV if x['n'] == n)['bound'])
    check(f'camshape{n}: verifier 20-digit value within 1e-19 of the 30-digit dossier value',
          abs(vv - v30) < q('1e-19'))
    Ld = fixed(lo, 14, up=False)[1]
    Ud = fixed(hi, 14, up=True)[1]
    check(f'camshape{n}: floor display equals summary display', Ld == c['summary_display'])
    put(f'camshape{n}', exact_opt=True, Lx=lo, Ux=hi, L=Ld, U=Ud,
        src_L='paper-open-minlplib/development/dossiers/checks/camshape/check_exact.json: '
              f'opt_30 (n={n}) minus 1e-30; cross-checked with research-20260929/reviews/'
              'open-instances-verification/logs/camshape_verify.json bound',
        src_U='same: opt_30 plus 1e-30',
        note='exact rational optimum v_n, attained by the envelope point')

# ---- hvycrash (identity) ----------------------------------------------------
hv = J(R / 'reviews/wave2-small-verification/logs/hvycrash.json')
check('hvycrash: identity objective = -437/2000 recorded', '-437/2000' in hv['identity'])
v_h = Q(-437, 2000)
put('hvycrash', exact_opt=True, Lx=v_h, Ux=v_h, L='-0.2185', U='-0.2185',
    src_L='research-20260929/reviews/wave2-small-verification/logs/hvycrash.json: identity (-50*4.37e-3 = -437/2000)',
    src_U='same (objective constant on the feasible set; explicit feasible point)',
    note='exact optimum -0.2185; a reading-(b) statement')

# ---- ex6_2_5, ex6_2_7 ------------------------------------------------------
lend = read(R / 'reviews/closing-confirm-r2-checks/logs/ex6_2_5_lower_end.log')
osc = read(D / 'dossiers/small-checks/own_osil_checks.log')
ex62 = read(D / 'dossiers/primal-points-checks/logs/ex62_check.log')
for name, Ld, Ud in [('ex6_2_5', '-70.75207783344770759', '-70.75207783344770558'),
                     ('ex6_2_7', '-0.16084761546364905', '-0.16084761546360086')]:
    Lg = q(re.search(name + r' lb\.a \(40 digits\) = (\S+)', lend).group(1))
    blk = ex62.split(name + ':', 1)[1]
    Ug = Q(int(re.search(r'hi \(25 dp, ceil\): (\S+)', blk).group(1)), 10 ** 25)
    own = next(l for l in osc.splitlines() if l.startswith(name + ' objective at verifier point'))
    check(f'{name}: own-reader mpmath enclosure lies below the mpmath-free upper end',
          last_iv_upper(own.split('|')[0]) <= Ug)
    bj = J(R / f'reviews/wave2-small-verification/logs/{name}_bound.json')
    check(f'{name}: verifier JSON dual string is not below the certified lower end',
          q(bj['dual_bound']) >= Lg)
    put(name, Lx=Lg, Ux=Ug, L=Ld, U=Ud,
        src_L='research-20260929/reviews/closing-confirm-r2-checks/logs/ex6_2_5_lower_end.log: '
              f'{name} lb.a (lower end of the verifier bound, gibbs_bb.py)',
        src_U='paper-open-minlplib/development/dossiers/primal-points-checks/logs/ex62_check.log: '
              f'{name} hi (25 dp, ceil) of the objective at the verifier\'s exact rational point (Fraction '
              'intervals, no mpmath); cross-checked with dossiers/small-checks/own_osil_checks.log')

# ---- etamac ------------------------------------------------------------------
et = read(D / 'dossiers/small-checks/r2/etamac_point.log')
line = next(l for l in et.splitlines() if l.startswith('objective of the exactly feasible point'))
U_et = last_iv_upper(line)
L_et = q('-15.2946756433680921685')
etj = J(R / 'reviews/wave2-small-verification/logs/etamac.json')
lxh = first_iv_lower(etj['bound']['l_at_xh'][0])
check('etamac: certified value -15.2946756433680921685 is below the lower end of l(x^) (gradient term)',
      L_et <= lxh and lxh - L_et < q('1e-19'))
put('etamac', Lx=L_et, Ux=U_et, L='-15.29467564336809217', U='-15.29467564336808959',
    src_L='certified lower end -15.29467564336809216848701... rounded down (verifier v_etamac.py; '
          'small dossier section 3.3; register N-09); consistent with '
          'research-20260929/reviews/wave2-small-verification/logs/etamac.json bound.l_at_xh',
    src_U='paper-open-minlplib/development/dossiers/small-checks/r2/etamac_point.log: upper end of the '
          'objective enclosure of the exactly feasible point from the authors\' saved decisions',
    note='do not print -15.294675643368092 or -15.294675643368092168 (above the certified end)')

# ---- pricing050 (maximisation) ----------------------------------------------
pl = read(D / 'dossiers/small-checks/r2/pricing_check.log')
U_dual = q(re.search(r'UB \(max form\) <= (\S+)', pl).group(1))
P_obj = q(re.search(r'objective \(exact rational\) = (\S+)', pl).group(1))
pj = J(R / 'reviews/wave2-small-verification/logs/pricing050.json')
check('pricing050: verifier certificate upper bound string equals the display',
      pj['certificate']['upper_bound'] == '-1813.8290784519730577')
put('pricing050', Lx=U_dual, Ux=P_obj, L='-1813.8290784519730577', U='-1813.8290784519730769',
    src_L='paper-open-minlplib/development/dossiers/small-checks/r2/pricing_check.log: UB (max form) '
          '(re-derivation of the verifier certificate; verifier upper_bound in '
          'research-20260929/reviews/wave2-small-verification/logs/pricing050.json)',
    src_U='same log: saved authors\' point, exactly feasible, objective exact rational',
    note='maximisation: the dual is an upper bound and is rounded up; the primal is rounded down')

# ---- pindyck (strong concavity, Theorem 6 of the small dossier; register N-12)
pe = read(R / 'reviews/pindyck-review-checks/logs/primal_enclosure.txt')
encl = {r.split()[0]: (q(r.split()[1]), q(r.split()[2])) for r in pe.splitlines() if r.strip()}
Jlo, Jhi = encl['J']
g2 = sum(max(abs(encl[f'g{t}'][0]), abs(encl[f'g{t}'][1])) ** 2 for t in range(1, 17))
mu = Q(1, 1000)
UBJ = Jhi + g2 / (2 * mu)
sc = read(D / 'dossiers/small-checks/r2/pindyck_sc.log')
check('pindyck: recomputed bound reproduces pindyck_sc.log display',
      fixed(-UBJ, 30, up=False)[1] == re.search(r'safe display \(rounded down, 30 decimals\): (\S+)', sc).group(1))
put('pindyck', Lx=-UBJ, Ux=-Jlo,
    L='-1170.486285436088562087577425069306', U='-1170.486285436088562087577425069288',
    Lt=fixed(-UBJ, 16, up=False)[1], Ut=fixed(-Jlo, 16, up=True)[1],
    src_L='-(J_hi + |g|^2/(2 mu)), mu = 1/1000, from research-20260929/reviews/pindyck-review-checks/'
          'logs/primal_enclosure.txt (exact rationals; strong concavity, small dossier Theorem 6, '
          'register N-12; dossiers/small-checks/r2/pindyck_sc.log)',
    src_U='-J_lo from the same file (objective of the exactly feasible point p*)',
    note='register N-12 strengthening adopted (checked: yes); the older dual -1170.4862854360886163932 also holds')

# ---- powerflow ------------------------------------------------------------
REG_PF = {'powerflow0030p': ('576.8934122988004', '576.8934134704'),
          'powerflow0039p': ('41869.05148485014', '41869.0515113203'),
          'powerflow0039r': ('41869.05148327243', '41869.0515113210')}
for name in REG_PF:
    tx = read(R / f'publication/primal/powerflow/logs/certify.{name}.log')
    lo, hi = map(q, re.search(r'objective enclosure: \[([^,]+), ([^]]+)\]', tx).groups())
    if name.endswith('0030p'):
        Lp = q(J(R / 'open-instances-wave3/logs/powerflow0030p.sdpcert.json')['bound_exact'])
        sL = 'research-20260929/open-instances-wave3/logs/powerflow0030p.sdpcert.json: bound_exact'
    else:
        Lp = q(J(R / f'open-instances-wave3/powerflow/ext/logs/{name}.bb3t.json')['LB_exact'])
        sL = f'research-20260929/open-instances-wave3/powerflow/ext/logs/{name}.bb3t.json: LB_exact'
    put(name, Lx=Lp, Ux=hi, L=REG_PF[name][0], U=REG_PF[name][1], src_L=sL,
        src_U=f'research-20260929/publication/primal/powerflow/logs/certify.{name}.log: objective enclosure upper end',
        note='never print 41869.05148327244 for powerflow0039r' if name.endswith('r') else '')

# ---- eg (route R targets and S-route binary64 bounds) -----------------------
dl = read(D / 'dossiers/checks/eg/r2/logs/displays.log')
vlog = {}
for f in sorted((R / 'reviews/eg-retry-review-checks/logs').glob('verify_*.log')):
    vlog.update({rel(f): read(f)})
thetas = set(re.findall(r'theta\* = (\S+?):', ''.join(vlog.values())))
REG_EG = {'eg_int_s': ('6.4531031529331155', '6.4531031593842275'),
          'eg_disc_s': ('5.760539610694993', '5.7605396164535107'),
          'eg_disc2_s': ('5.642100574331458', '5.6421005799711068')}
THETA = {'eg_int_s': '6.4531031529331155', 'eg_disc_s': '5.760539610694994', 'eg_disc2_s': '5.642100574331458'}
for name in REG_EG:
    check(f'{name}: route R target theta* found in the review verify logs', THETA[name] in thetas)
    b64 = qf(re.search(name + r': certified binary64 (\S+);', dl).group(1))
    Le = min(q(THETA[name]), b64)
    sol = read(R / f'open-instances-wave3/eg/retry/sol/{name}.retry.sol')
    Ue = q(dict(l.split() for l in sol.splitlines() if l.strip())['objvar'])
    put(name, Lx=Le, Ux=Ue, L=REG_EG[name][0], U=REG_EG[name][1],
        src_L='min(route R target theta* in research-20260929/reviews/eg-retry-review-checks/logs/verify_*.log, '
              'S-route binary64 bound in paper-open-minlplib/development/dossiers/checks/eg/r2/logs/displays.log)',
        src_U=f'research-20260929/open-instances-wave3/eg/retry/sol/{name}.retry.sol: objvar '
              '(rounded up at the 20th digit; interval-proved point)',
        note='do not print 5.760539610694994 (eg_disc_s)' if name == 'eg_disc_s' else '')

# ============================================== closed: derived quantities
GAPV = J(R / 'publication/integration/gap-values.json')
REL_FAMILIES = ('powerflow', 'eg')


def derive_closed(n):
    r = REC[n]
    s = 1 if n != 'pricing050' else -1
    Lx, Ux = r['Lx'], r['Ux']
    Ld, Ud = q(r['L']), q(r['U'])
    out = dict(sense='min' if s == 1 else 'max')
    # display directions
    if s == 1:
        check(f'{n}: dual display {r["L"]} <= certified value (rounded down)', Ld <= Lx, f'margin {float(Lx - Ld):.3e}')
        check(f'{n}: primal display {r["U"]} >= enclosure upper end (rounded up)', Ud >= Ux, f'margin {float(Ud - Ux):.3e}')
        check(f'{n}: dual value <= primal value', Lx <= Ux)
    else:
        check(f'{n}: dual (upper) display {r["L"]} >= certified upper bound (rounded up)', Ld >= Lx, f'margin {float(Ld - Lx):.3e}')
        check(f'{n}: primal display {r["U"]} <= primal value (rounded down)', Ud <= Ux, f'margin {float(Ux - Ud):.3e}')
        check(f'{n}: primal value <= dual upper bound', Ux <= Lx)
    for key in ('Lt', 'Ut'):
        if key in r:
            v = q(r[key])
            if key == 'Lt':
                check(f'{n}: table dual display {r[key]} safe', v <= Lx if s == 1 else v >= Lx)
            else:
                check(f'{n}: table primal display {r[key]} safe', v >= Ux if s == 1 else v <= Ux)
    exact = r.get('exact_opt', False)
    if exact:
        gap_abs, gap_abs_s = Q(0), '0'
        gap_rel, gap_rel_s = Q(0), '0'
        width = Ux - Lx
        check(f'{n}: exact-optimum enclosure has width < 1e-29', 0 <= width < q('1e-29'))
        delta_exact = Q(0)
    else:
        delta_exact = s * (Ux - Lx)
        check(f'{n}: exact gap is nonnegative', delta_exact >= 0)
        gap_abs, gap_abs_s = sig(delta_exact, 3, up=True)
        denom = min(abs(Lx), abs(Ux))
        rel_exact = delta_exact / denom
        gap_rel, gap_rel_s = sig(rel_exact, 3, up=True)
        check(f'{n}: abs gap cell {gap_abs_s} >= exact gap {float(delta_exact):.6e}', gap_abs >= delta_exact)
        check(f'{n}: rel gap cell {gap_rel_s} >= exact relative gap (denominator min(|L|,|U|))', gap_rel >= rel_exact)
        check(f'{n}: relative gap below the closure threshold 1e-6', rel_exact <= q('1e-6'))
        # consistency with the summary's gap-values.json (a weaker, display-based computation)
        gv = GAPV.get(n)
        if gv is not None:
            gvx = q(gv['display_value'])     # the summary's rounded-up cell
            if family(n) in REL_FAMILIES:
                check(f'{n}: relative gap <= summary cell {gv["text"]} (gap-values.json display_value)', rel_exact <= gvx,
                      f'{float(rel_exact):.6e} vs {float(gvx):.6e}')
            else:
                check(f'{n}: absolute gap <= summary cell {gv["text"]} (gap-values.json display_value)', delta_exact <= gvx,
                      f'{float(delta_exact):.6e} vs {float(gvx):.6e}')
    # display difference versus the gap cell
    Lt, Ut = q(r.get('Lt', r['L'])), q(r.get('Ut', r['U']))
    disp_diff = s * (Ut - Lt)
    needs_note = (not exact) and disp_diff > gap_abs
    out.update(
        L=dict(display=r['L'], table_display=r.get('Lt', r['L']),
               direction='down' if s == 1 else 'up (maximisation)', exact=fr(Lx), exact_decimal=dec40(Lx, 45),
               source=r['src_L']),
        U=dict(display=r['U'], table_display=r.get('Ut', r['U']),
               direction='up' if s == 1 else 'down (maximisation)', exact=fr(Ux), exact_decimal=dec40(Ux, 45),
               source=r['src_U']),
        exact_optimum=exact,
        gap_abs=dict(display=gap_abs_s, exact=fr(delta_exact) if not exact else '0',
                     exact_decimal=(dec40(delta_exact, 60) if not exact else '0'),
                     note='U - L from the exact certificate ends; rounded up to 3 significant digits'
                     if not exact else 'attained exact optimum; gap printed only with this qualifier'),
        gap_rel=dict(display=gap_rel_s,
                     note='Delta/min(|L|,|U|), rounded up to 3 significant digits'),
        table_display_difference=(sig(disp_diff, 3, up=True)[1] if disp_diff > 0 else '0'),
        table_footnote_cert_ends=needs_note,
        note=r.get('note', ''))
    if exact:
        out['optimum_enclosure_width'] = sig(Ux - Lx, 3, up=True)[1] if Ux > Lx else '0'
    return out


# ===================================================== unclosed: waterno2
def derive_water(n):
    k = n.split('_')[1]
    v = J(R / f'publication/primal/water-ann-kan/points/{n}.exact.json')
    Ux = q(v['objective'])
    if k == '06':
        Lx = q(J(R / 'open-instances-wave2/waterno2/cellslopes/logs/certB_verify.json')['bound_exact'])
        sL = 'research-20260929/open-instances-wave2/waterno2/cellslopes/logs/certB_verify.json: bound_exact'
    else:
        Lx = q(J(R / f'open-instances-wave2/waterno2/logs/cert_{k}_w1_impl.json')['certified_bound_exact'])
        sL = f'research-20260929/open-instances-wave2/waterno2/logs/cert_{k}_w1_impl.json: certified_bound_exact'
    REG = {'06': ('278.230573', '282.888038'), '09': ('824.834692', '914.012'),
           '12': ('2089.754565', '2233.821346'), '18': ('4790.820715', '5023.983'),
           '24': ('6576.151388', '6963.795181')}
    Ld, Ud = REG[k]
    check(f'{n}: dual display {Ld} <= certified bound', q(Ld) <= Lx)
    check(f'{n}: primal display {Ud} >= exact objective', q(Ud) >= Ux)
    delta = Ux - Lx
    check(f'{n}: dual <= primal', delta > 0)
    rel_exact = delta / min(abs(Lx), abs(Ux))
    g, gs = pct(rel_exact, up=True)
    check(f'{n}: percent gap {gs} >= exact (dual denominator)', g >= rel_exact)
    gv = q(GAPV[n]['exact_upper']) / 100
    check(f'{n}: percent gap equals summary gap-values.json cell', gs == GAPV[n]['text'], f'{gs} vs {GAPV[n]["text"]}')
    check(f'{n}: exact relative gap equals gap-values.json exact value', rel_exact == gv)
    lst = listed(n)['best_dual']
    d = q(lst['value'])
    fac = Lx / d
    fv, fs = fixed(fac, 2, up=False)
    check(f'{n}: improvement factor {fs} <= L/listed dual (rounded down)', fv <= fac)
    out = dict(
        sense='min',
        L=dict(display=Ld, direction='down', exact=fr(Lx), exact_decimal=dec40(Lx, 30), source=sL),
        U=dict(display=Ud, direction='up', exact=fr(Ux), exact_decimal=dec40(Ux, 30),
               source=f'research-20260929/publication/primal/water-ann-kan/points/{n}.exact.json: objective (exact rational)'),
        gap_abs=dict(display=sig(delta, 3, True)[1], exact=fr(delta)),
        gap_rel=dict(display=gs, note='Delta/min(|L|,|U|) = Delta/L; two decimals, rounded up'),
        factor=dict(display=fs, exact_decimal=dec40(fac, 12), rounding='down',
                    listed_dual=lst['value'], listed_solver=lst['solver']),
        primal_note=('MINLPLib point p4 made exactly feasible (not our search point)' if k == '06' else
                     'exactly feasible point (exact algebraic arithmetic)'))
    if k == '06':
        w2 = q(J(R / 'open-instances-wave2/waterno2/logs/cert_06_w1_impl.json')['certified_bound_exact'])
        sb = q(J(R / 'open-instances-wave2/waterno2/sepbranch/logs/cert3_verify.json')['bound_exact'])
        prog = []
        for lab, x, disp, src in [('period Lagrangian', w2, '263.735099',
                                   'research-20260929/open-instances-wave2/waterno2/logs/cert_06_w1_impl.json: certified_bound_exact'),
                                  ('one slope vector per separator, with pair bounds over 113--162 cells per separator', sb, '272.584700',
                                   'research-20260929/open-instances-wave2/waterno2/sepbranch/logs/cert3_verify.json: bound_exact'),
                                  ('cellwise slopes', Lx, '278.230573', sL)]:
            check(f'waterno2_06 progression {lab}: display {disp} <= exact', q(disp) <= x)
            rg = (Ux - x) / x
            gg, ggs = pct(rg, True)
            prog.append(dict(stage=lab, display=disp, exact=fr(x), gap=ggs, source=src))
        cells = J(R / 'open-instances-wave2/waterno2/sepbranch/logs/cert3_verify.json')['leaves']
        check('waterno2_06 progression: the intermediate bound uses 113 to 162 cells per separator (5 separators)',
              (len(cells), min(cells), max(cells)) == (5, 113, 162), str(cells))
        out['progression'] = prog
    return out


# ======================================================== ann_cumene_tanh
def derive_ann():
    v = J(R / 'publication/primal/water-ann-kan/points/ann_cumene_tanh.point.json')
    Lx = q(v['dual_bound'])
    Ux = q(v['objective_hi'])
    check('ann: dual equals -7447080719734483*2^-41', Lx == Q(-7447080719734483, 2 ** 41))
    Ld, Ud = '-3386.5403', '-3379.9823940'
    check('ann: dual display -3386.5403 <= L*', q(Ld) <= Lx)
    check('ann: primal display -3379.9823940 >= objective upper end', q(Ud) >= Ux)
    delta = Ux - Lx
    rel_exact = delta / min(abs(Lx), abs(Ux))
    g, gs = pct(rel_exact, True)
    check(f'ann: relative gap {gs} >= exact (conservative denominator)', g >= rel_exact)
    check('ann: relative gap display is 0.195%', gs == '0.195%')
    rd = delta / max(abs(Lx), abs(Ux))
    g2, gs2 = pct(rd, True)
    return dict(sense='min',
                L=dict(display=Ld, exact=fr(Lx), exact_decimal=dec40(Lx, 20), direction='down',
                       source='research-20260929/publication/primal/water-ann-kan/points/ann_cumene_tanh.point.json: dual_bound '
                              '(= research-20260929/open-instances-wave3/ann/ext_logs final bound; extension review)'),
                U=dict(display=Ud, exact=fr(Ux), exact_decimal=dec40(Ux, 35), direction='up',
                       source='same file: objective_hi (upper end of the objective enclosure of the exactly feasible point)'),
                gap_abs=dict(display=sig(delta, 3, True)[1], exact=fr(delta)),
                gap_rel=dict(display=gs, note='Delta/min(|L|,|U|) (= Delta/|U|); the dual denominator gives ' + gs2),
                scope='applies verbatim to the algebraically identical ann_cumene_exp')


# ================================================================== KAN
KAN_DISP = {'kan_r3_h1_n4': ('0.002781237152581', '0.002781237221442'),
            'kan_r3_h1_n5': ('-0.01104267952179', '-0.01104267941448'),
            'kan_r3_h1_n9': ('0.01296365996347', '0.01296366005304'),
            'kan_r5_h1_n3': ('-262.8642259093', '-262.8642258850'),
            'kan_r5_h1_n5': ('0.2725832538548', '0.2725832539567'),
            'kan_r5_h1_n8': ('0.06932786051052', '0.06932786060620')}
# Published SCIP 9.0.1 "optimal" values (Karia et al. 2025, Zenodo 14961066, Default logs),
# as quoted in the solvers dossier Prop. 14 and the network literature report.
KAN_SCIP = {'kan_r3_h1_n4': '1.08116412047821e-3', 'kan_r3_h1_n5': '-1.30809958982354e-2'}


def derive_kan(n):
    v = J(R / f'publication/primal/water-ann-kan/points/{n}.point.json')
    res = J(R / f'open-instances-wave3/logs/{n}.result.json')
    Lx = q(v['dual_bound'])
    check(f'{n}: point-file dual equals wave-3 result dual_bound (binary64)', Lx == qf(res['dual_bound']))
    Ux = q(v['objective_hi'])
    Ld, Ud = KAN_DISP[n]
    check(f'{n}: L display {Ld} <= L', q(Ld) <= Lx)
    check(f'{n}: U display {Ud} >= U', q(Ud) >= Ux)
    delta = Ux - Lx
    check(f'{n}: U - L equals gap-values.json exact_upper', delta == q(GAPV[n]['exact_upper']))
    gd, gs = sig(delta, 3, True)
    lim = q('2.42e-8') if n == 'kan_r5_h1_n3' else q('1.08e-10')
    check(f'{n}: gap within the headline bound {lim}', delta <= lim)
    # rigorous-exp rerun of the verifier path: its bound must not be below L
    rx = D / f'dossiers/ann-kan-checks/logs/{n}.bnb.json'
    out = dict(sense='min',
               L=dict(display=Ld, exact=fr(Lx), exact_decimal=dec40(Lx, 25), direction='down',
                      source=f'research-20260929/publication/primal/water-ann-kan/points/{n}.point.json: dual_bound '
                             f'(= open-instances-wave3/logs/{n}.result.json dual_bound; weaker of the two bound codes)'),
               U=dict(display=Ud, exact=fr(Ux), exact_decimal=dec40(Ux, 25), direction='up',
                      source='same point file: objective_hi (point of R_P; enclosure width <= 3.2e-89 in review r1)'),
               gap_abs=dict(display=gs, exact=fr(delta)),
               object='R_P (OSIL model minus the partition-of-unity rows); L also bounds min over R')
    if rx.exists():
        lv = qf(J(rx)['lower_bound'])
        check(f'{n}: rigorous-exp verifier bound >= reported L', lv >= Lx, f'{float(lv - Lx):.3e}')
        out['verifier_rigexp_bound'] = dict(value=repr(float(lv)), source=rel(rx))
    if n in KAN_SCIP:
        sv = q(KAN_SCIP[n])
        mg = Lx - sv
        mv, ms = sig(mg, 3, up=False)
        check(f'{n}: published SCIP optimum lies below L by at least {ms}', mv <= mg and mg > 0)
        out['published_scip_optimum'] = dict(value=KAN_SCIP[n], below_L_by_at_least=ms,
                                             source='solvers dossier Prop. 14; Karia et al. (2025) Zenodo 14961066 Default logs '
                                                    '(literature KB karia2025-karia-et-al-zenodo-default)')
    return out


# ============================================================== metadata
# certificate class (outline section 9), arithmetic tags (dual/primal;
# outline section 4.6 and Table 1, corrected by the data-semantics report and
# the reviews), prior status (outline section 5, section 3.2), mechanism.
# Class, prior-status and evidence-level labels are words, not letters
# (development/terminology.md).
CLASS = {}
for n in ['lnts50', 'lnts100', 'lnts200', 'lnts400', 'dtoc5', 'optcdeg2', 'lukvle10',
          'chain50', 'chain100', 'chain200', 'chain400', 'catmix100', 'catmix200', 'catmix400', 'catmix800']:
    CLASS[n] = 'staged'
for n in ['camshape100', 'camshape200', 'camshape400', 'camshape800']:
    CLASS[n] = 'comparison'
for n in ['ex6_2_5', 'ex6_2_7', 'pricing050']:
    CLASS[n] = 'dense rows'
for n in ['etamac', 'pindyck', 'powerflow0030p', 'powerflow0039p', 'powerflow0039r']:
    CLASS[n] = 'convexity'
CLASS['hvycrash'] = 'identity'
for n in ['eg_int_s', 'eg_disc_s', 'eg_disc2_s']:
    CLASS[n] = 'reduced space'
for n in WATER:
    CLASS[n] = 'staged (not closed)'

ARITH = {'lnts': ('E', 'E'), 'dtoc5': ('E', 'E'), 'optcdeg2': ('E', 'E'), 'lukvle10': ('I', 'E'),
         'chain': ('I', 'E'), 'catmix': ('F', 'E'), 'camshape': ('E', 'E'), 'ex6_2': ('I', 'E'),
         'pricing050': ('I', 'I'), 'etamac': ('I', 'I'), 'pindyck': ('F+I', 'I'), 'powerflow': ('E', 'E'),
         'hvycrash': ('E', 'I'), 'eg': ('F', 'E'), 'waterno2': ('F/E', 'E'), 'ann': ('F', 'E'), 'kan': ('F', 'E')}
ARITH_NOTE = {
    'lnts': 'dual: integers, Fraction, isqrt (two integer-only codes); primal: attaining point of Theorem 4.6, and stored Krawczyk points re-proved without mpmath',
    'dtoc5': 'Fraction with GMP sums (two codes)',
    'optcdeg2': 'dual: exact rational stage minimisation (Sturm); primal: integer-interval proof (mpmath proof as second)',
    'lukvle10': 'dual: mpmath iv exp/log in both certificates; primal: integer-only fixed point',
    'chain': 'dual: mpmath iv sqrt/log in both codes; primal: exact in Q(sqrt R)',
    'catmix': 'dual: own outward binary64 +,-,*,/ only; primal: exact rational states',
    'camshape': 'exact rational checks K1-K6',
    'ex6_2': 'dual: mpmath iv (log) via the verifier compiler; primal: rows exact, objective by Fraction intervals',
    'pricing050': 'mpmath iv (exp); primal rows by iv slacks, objective exact rational',
    'etamac': 'mpmath iv (exp, log), one implementation',
    'pindyck': 'concavity proof: author padding analysis / review nextafter + iv; bound: exact rationals from the review enclosures',
    'powerflow': 'dual: exact rational Lagrangian and LDL^T PSD proof; primal: Krawczyk, dyadic re-proof without mpmath',
    'hvycrash': 'dual: identity checked in Fraction; primal: mpmath iv backward definitions (two codes)',
    'eg': 'route R: binary64 with Lemma A1 padding and exact final tests; exp/pow audit see trust table',
    'waterno2': 'rbb: outward binary64; vbb/vbb2: exact rational node bounds; primal: exact algebraic',
    'ann': 'two binary64 codes with outward rounding, no library transcendental; primal: exact rational intervals',
    'kan': 'two binary64 codes; both use the shared rigorous exp kan_iv/ia; primal: exact rational intervals'}

PRIOR = {
    'lnts50': ('F', 'Gurobi floating-point closure (Goess-Burlacu-Martin, Table 17; unchanged by the correction)'),
    'lnts100': ('f', 'PARA gap 0.00% (Goess 2026)'),
    'lnts200': ('f', 'PARA gap 0.00% (Goess 2026)'),
    'lnts400': ('f', 'PARA gap 0.01% (Goess 2026)'),
    'dtoc5': ('F', 'MINOTAUR closure of QPLIB_8585 (same model) with assumed default bounds'),
    'optcdeg2': ('Lst', 'MINOTAUR solve listing on QPLIB_8803 without value or log'),
    'lukvle10': ('N', 'CUTEst SOLTN 352.237 is a local value below the certified bound'),
    'camshape100': ('F', 'Octeract floating-point solve of the MINLPLib model (Bestuzheva et al. 2025)'),
    'camshape200': ('T', 'Octeract listed as solving the rounded copy QPLIB_2480 (value and log unavailable); '
                         'the copy is a different model (prop:camshape-copies)'),
    'camshape400': ('N', ''),
    'camshape800': ('T', 'MINOTAUR listed as solving the rounded copy QPLIB_3177, a different model; '
                         'its value is not attainable on the copy under exact feasibility'),
    'hvycrash': ('K', 'value -0.21850 recorded without proof in the CUTE SIF file'),
    'ex6_2_5': ('U', 'possible epsilon-global result in McDonald-Floudas 1997 (unread)'),
    'ex6_2_7': ('U', 'possible epsilon-global result in McDonald-Floudas 1997 (unread)'),
    'etamac': ('N', ''), 'pricing050': ('N', 'Davarnia-van Hoeve value 1813.3: model/data discrepancy'),
    'pindyck': ('N', 'COCONUT value -1612.18 belongs to a mistranscribed model'),
    'chain50': ('N', ''), 'chain100': ('N', ''), 'chain200': ('N', ''), 'chain400': ('N', ''),
    'catmix100': ('N', ''), 'catmix200': ('N', ''), 'catmix400': ('N', ''), 'catmix800': ('N', ''),
    'powerflow0030p': ('T', 'ANTIGONE closure of the rectangular twin powerflow0030r'),
    'powerflow0039p': ('T', 'floating-point global solution of MATPOWER case39 with taps (Ghaddar et al. 2016)'),
    'powerflow0039r': ('T', 'floating-point global solution of MATPOWER case39 with taps (Ghaddar et al. 2016)'),
    'eg_int_s': ('F', 'SCIP 8.1 floating-point closure (Goess-Burlacu-Martin)'),
    'eg_disc_s': ('N', 'CAMINO Gurobi 13.0.0 bound invalid (category B)'),
    'eg_disc2_s': ('N', 'CAMINO Gurobi 13.0.0 bound invalid (category B)'),
    'waterno2_06': ('U', 'Huang 2011 Diplom thesis, a 2022 waterno2_04 paper and Ghaddar et al. 2015 unread; no closure found'),
    'waterno2_09': ('U', 'as waterno2_06'), 'waterno2_12': ('U', 'as waterno2_06'),
    'waterno2_18': ('U', 'as waterno2_06'), 'waterno2_24': ('U', 'as waterno2_06'),
    'ann_cumene_tanh': ('T', 'exp twin ann_cumene_exp closed in floating point by SCIP and LINDO'),
    'kan_r3_h1_n4': ('F', 'SCIP 9.0.1 zero-gap value (Karia et al.) lies below min R: tolerance artifact'),
    'kan_r3_h1_n5': ('F', 'SCIP 9.0.1 zero-gap value (Karia et al.) lies below min R: tolerance artifact'),
    'kan_r3_h1_n9': ('N', ''), 'kan_r5_h1_n3': ('N', ''), 'kan_r5_h1_n5': ('N', ''), 'kan_r5_h1_n8': ('N', '')}
CLASS_ORDER = ('staged', 'comparison', 'dense rows', 'convexity', 'identity', 'reduced space')
PRIOR_LABEL = {'F': 'fp closure', 'f': 'fp near-closure', 'Lst': 'listed solve', 'T': 'related model',
               'K': 'value only', 'U': 'unread source', 'N': 'none'}
PRIOR = {n: (PRIOR_LABEL[c], note) for n, (c, note) in PRIOR.items()}

MECH = {
    'lnts': 'aggregate Lagrangian with the linear-tangent law; monotone in h; exact optimum',
    'dtoc5': 'convex Lagrangian at the discrete costate (Mangasarian-type sufficiency)',
    'optcdeg2': 'quadratic split (Krotov-type verification function); exact stage minimisation',
    'lukvle10': 'partial chain Lagrangian plus 2-D interval B&B on an end window',
    'chain': 'catenary split (discrete calibration) plus 2-D end-value B&B',
    'catmix': 'rigorous DP lower bound on an exact 1-D projective reduction (chord minorants)',
    'camshape': 'discrete Sturm comparison in u = 1/r; envelope point',
    'ex6_2': 'mass-balance Lagrangian; tangent-plane test by 2-D interval B&B',
    'pricing050': 'Lagrangian over 5 rows; 50 certified 1-D minimisations',
    'etamac': 'concave majorant (hidden convexity) and KKT tangent plane',
    'pindyck': 'reduced objective strongly concave on a polytope containing the price set P; tangent plane',
    'powerflow': 'SDP/Lagrangian dual with exact LDL^T PSD proof (0039: leaf identity, vertex planes, 3-D branching)',
    'hvycrash': 'objective constant on the feasible set; explicit feasible point',
    'eg': 'reduced-space B&B with second-order Taylor models and per-box LP',
    'waterno2': 'period Lagrangian with rigorous per-period B&B (06: cellwise slopes)',
    'ann': 'reduced-space B&B with affine arithmetic and a per-box LP dual',
    'kan': 'reduced-space interval B&B over the inputs (bound for R)'}
LEVEL = {'lnts': 'hand+stored', 'dtoc5': 'hand+stored', 'optcdeg2': 'stored', 'lukvle10': 'rerun',
         'chain': 'rerun', 'catmix': 'rerun', 'camshape': 'hand+stored', 'ex6_2': 'rerun', 'pricing050': 'stored',
         'etamac': 'stored', 'pindyck': 'stored', 'powerflow': 'stored', 'hvycrash': 'hand', 'eg': 'rerun',
         'waterno2': 'rerun', 'ann': 'rerun', 'kan': 'rerun'}


# ====================================================== audit (Table 6)
AUD = J(R / 'bound-audit/results.json')
SECOND = {  # second implementation per (instance, solver): reviewer and method
    'ghg_3veh': 'Krawczyk', 'glider100': 'Krawczyk', 'methanol50': 'Krawczyk', 'nuclear14': 'Krawczyk',
    'sssd20-04persp': 'Krawczyk, exact', 'topopt-cantilever_60x40_50': 'linear Krawczyk',
    'nd_netgen-2000-3-4-b-a-ns_7': 'exact', 'watercontamination0303': 'exact',
    'smallinvDAXr1b150-165': 'exact', 'smallinvDAXr1b200-220': 'exact',
    'sssd22-08persp': 'exact', 'sssd25-04persp': 'exact', 'sssd25-08persp': 'exact',
    'smallinvDAXr2b150-165': 'exact', 'smallinvDAXr2b200-220': 'exact'}


def route_code(rt):
    # audit proof methods of Section 7.3 (listed-point check, Krawczyk proof,
    # shifted Krawczyk proof, dedicated proof); results.json calls them routes A-D
    if rt.startswith('A '):
        return 'listed point'
    if rt.startswith('snap'):
        return 'Krawczyk'
    if 'route C' in rt:
        return 'shifted Krawczyk'
    return 'dedicated'


def iso_date(s):
    # '25 Jun 2015' (page display) -> '2015-06-25'
    return datetime.strptime(s, '%d %b %Y').strftime('%Y-%m-%d')


def unit_of(s):
    s = s.strip()
    if '.' in s:
        k = len(s.split('.')[1])
        return Q(1, 10 ** k)
    return Q(1)


def derive_audit():
    cls_i = [x for x in AUD if x['cls'].startswith('(i) ')]
    pairs = {}
    for x in cls_i:
        key = (x['name'], x['solver'])
        if key not in pairs or q(x['obj_hi']) < q(pairs[key]['obj_hi']):
            pairs[key] = x
    rows = []
    for (name, solver), x in pairs.items():
        assert x['sense'] == 'min'
        d = q(x['d_listed'])
        f = q(x['obj_hi'])
        u = unit_of(x['d_listed'])
        mg = d - f
        check(f'audit {name}/{solver}: proven objective below the displayed bound by more than one display unit',
              mg > u, f'{float(mg / u):.4g} units')
        mv, ms = sig(mg, 3, up=False)
        rv, rs = sig(mg / abs(d), 3, up=False)
        uv, us = sig(mg / u, 3, up=False)
        fv, fs = sig(abs(f), 10, up=(f > 0))
        fdisp = ('-' if f < 0 else '') + fs
        fd_val = -fv if f < 0 else fv
        check(f'audit {name}/{solver}: displayed f {fdisp} >= proven upper end', fd_val >= f)
        label = 'gross' if mg / abs(d) > q('1e-6') else 'tolerance'
        check(f'audit {name}/{solver}: label agrees with results.json i_group',
              (label == 'gross') == (x['i_group'] == 'gross'))
        rows.append(dict(instance=name, solver=solver, date=iso_date(x['d_date']), d=x['d_listed'], point=x['point'],
                         f_upper=fdisp, f_upper_exact=x['obj_hi'], margin=ms, rel_margin=rs, units=us,
                         label=label, route=route_code(x['route']), route_detail=x['route'],
                         second=SECOND[name], solved_mark=x['solved'],
                         _rel=float(mg / abs(d)), _units=mg / u))
    rows.sort(key=lambda r: -r['_rel'])
    check('audit: 19 class (i) pairs', len(rows) == 19)
    check('audit: on 15 instances', len({r['instance'] for r in rows}) == 15)
    check('audit: 11 gross pairs on 9 instances', sum(r['label'] == 'gross' for r in rows) == 11
          and len({r['instance'] for r in rows if r['label'] == 'gross'}) == 9)
    check('audit: 8 tolerance-scale pairs on 6 instances', sum(r['label'] == 'tolerance' for r in rows) == 8
          and len({r['instance'] for r in rows if r['label'] == 'tolerance'}) == 6)
    minu = min(q(r['units']) for r in rows)
    check('audit: every margin exceeds 1.11 display units', minu >= q('1.11'))
    minx = min(r['_units'] for r in rows)
    check('audit: every class (i) margin is at least 1.115 display units, more than 10/9 (Lemma S4.1(a))',
          minx >= q('1.115') and minx > Q(10, 9), f'{float(minx):.10f}')
    four = [r for r in rows if r['_rel'] > 0.01]
    check('audit: four margins exceed 1% of |d|', len(four) == 4)
    seven = [r for r in rows if 1e-6 < r['_rel'] <= 0.01]
    check('audit: seven gross margins between 1.2e-5 and 7.3e-5 of |d|',
          len(seven) == 7 and all(1.2e-5 <= r['_rel'] <= 7.4e-5 for r in seven))
    tol = [r for r in rows if r['_rel'] <= 1e-6]
    check('audit: tolerance-scale margins between 1.9e-9 and 3.3e-7 of |d|',
          all(1.9e-9 <= r['_rel'] <= 3.4e-7 for r in tol))
    for r in rows:
        r.pop('_rel')
        r.pop('_units')
    # population counts
    pages = list(PAGES.values())
    n_points = sum(len(p['points']) for p in pages)
    n_bounds = sum(len(p['duals']) for p in pages)
    n_inf = sum(1 for p in pages for d in p['duals'] if d['value'].lower() in ('inf', '-inf'))
    labels = {d['solver'] for p in pages for d in p['duals']}
    scr = J(R / 'bound-audit/screen.json')
    counts = dict(pages=len(pages), points=n_points, per_solver_bounds=n_bounds,
                  finite_bounds=n_bounds - n_inf, solver_labels=len(labels),
                  screened_pairs=len(scr['pairs']), screened_instances=len({x['name'] for x in scr['pairs']}),
                  screened_points=len({(x['name'], x['point']) for x in scr['pairs']}),
                  display_ties=len(scr['ties']), display_tie_instances=len({x['name'] for x in scr['ties']}),
                  class_i_pairs=len(rows), class_i_instances=len({r['instance'] for r in rows}),
                  class_i_gross=sum(r['label'] == 'gross' for r in rows),
                  class_i_tolerance=sum(r['label'] == 'tolerance' for r in rows),
                  class_i_distinct_conflicts=len({(r['instance'].replace('r2b', 'r1b'), r['d']) for r in rows}),
                  class_ir_pairs=len({(x['name'], x['solver']) for x in AUD if x['cls'].startswith('(i-r)')}),
                  class_ir_instances=len({x['name'] for x in AUD if x['cls'].startswith('(i-r)')}),
                  osil_byte_identical_refetched=69)
    check('audit counts: 1633 pages, 2816 points, 11086 bounds (11031 finite), 19 labels',
          (counts['pages'], counts['points'], counts['per_solver_bounds'], counts['finite_bounds'],
           counts['solver_labels']) == (1633, 2816, 11086, 11031, 19))
    check('audit counts: screen 158 pairs on 46 instances (56 points); 3851 ties on 1133 instances',
          (counts['screened_pairs'], counts['screened_instances'], counts['screened_points'],
           counts['display_ties'], counts['display_tie_instances']) == (158, 46, 56, 3851, 1133))
    check('audit counts: 15 distinct numerical conflicts', counts['class_i_distinct_conflicts'] == 15)
    check('audit counts: 12 class (i-r) pairs on 4 instances', (counts['class_ir_pairs'], counts['class_ir_instances']) == (12, 4))
    check('audit counts: 69 refreshed OSIL files present', len(list(OSIL_DIR.glob('*.osil'))) == 69)
    rocket = []
    for nm, d, lo, hi in [('rocket100', '-1.0128319', '-1.0128320069151', '-1.0128320069130'),
                          ('rocket200', '-1.01283563', '-1.0128356770698', '-1.0128356770677'),
                          ('rocket400', '-1.01283634', '-1.0128365294842', '-1.0128365294822')]:
        mg = q(d) - q(hi)
        mv, ms = sig(mg, 3, up=False)
        rocket.append(dict(instance=nm, solver='LINDO', d=d, f_upper=hi, margin=ms,
                           source='audit dossier section 5.4; dossiers/checks/audit-r2/safe_margins.log'))
    check('rocket margins at least 1.06e-7, 4.7e-8, 1.89e-7',
          [r['margin'] for r in rocket] == ['1.06e-7', '4.70e-8', '1.89e-7'],
          str([r['margin'] for r in rocket]))
    return dict(counts=counts, pairs=rows, rocket=rocket,
                source='research-20260929/bound-audit/results.json, pages.json, screen.json')


# ==================================================== campaign (Table 8)
CAMP = list(csv.DictReader(read(R / 'publication/solver-runs/results_table.csv').splitlines()))


def finite_dual(x):
    return x['dual'] not in ('', 'Infinity', '-Infinity')


def derive_campaign():
    per = {}
    for s in ('BARON', 'GUROBI', 'SCIP'):
        rows = [x for x in CAMP if x['solver'] == s]
        fin = [x for x in rows if finite_dual(x)]
        st = [x['status'] for x in rows]
        per[s] = dict(runs=len(rows),
                      passing_measurements=sum(x['valid_time_measurement'] == 'True' for x in rows),
                      finite_final_duals=len(fin),
                      finite_without_globality_guarantee=sum(x['globality_warning'] == 'True' for x in fin),
                      finite_against_R=sum(x['certificate_scope'].startswith('R') for x in fin),
                      same_model_guaranteed_finite_duals=sum(x['globality_warning'] != 'True'
                                                             and x['scip_argument_bounds_tightened'] != 'True'
                                                             and not x['certificate_scope'].startswith('R')
                                                             for x in fin),
                      runs_within_1e_6=sum(1 for x in rows if x['primal'] != '' and finite_dual(x)
                                           and abs(q(x['primal']) - q(x['dual']))
                                           <= q('1e-6') * max(abs(q(x['primal'])), abs(q(x['dual'])))),
                      returned_primals=sum(x['primal'] != '' for x in rows),
                      raw_optimality_claims=sum(x['optimality_claim'] == 'True' for x in rows),
                      accepted_closures=sum(x['closes_within_1h'] == 'True' for x in rows),
                      capability_failures=st.count('capability failure'),
                      other_failures=st.count('interface/model-expression failure'),
                      memory_stops=st.count('stopped at the 8 GB memory limit'),
                      tightened_argument_bounds=sum(x['scip_argument_bounds_tightened'] == 'True' for x in rows),
                      overloaded_first_batch=sum(x['loaded_first_batch'] == 'True' for x in rows),
                      improves_best_listed_dual=sum(1 for x in rows if x['dual_improvement_vs_listed']
                                                    not in ('', 'Infinity', '-Infinity')
                                                    and q(x['dual_improvement_vs_listed']) > 0))
    tot = {k: sum(per[s][k] for s in per) for k in per['BARON']}
    exp = dict(BARON=(43, 35, 6, 2, 0, 8, 0, 0), GUROBI=(43, 36, 0, 0, 0, 0, 1, 0), SCIP=(40, 38, 0, 0, 0, 1, 0, 3))
    for s, e in exp.items():
        p = per[s]
        check(f'campaign {s}: passing/finite/no-guarantee/claims/closures/capability/other/memory = {e}',
              (p['passing_measurements'], p['finite_final_duals'], p['finite_without_globality_guarantee'],
               p['raw_optimality_claims'], p['accepted_closures'], p['capability_failures'],
               p['other_failures'], p['memory_stops']) == e)
    check('campaign: 129 kept outcomes, 126 passing, 109 finite duals', (tot['runs'], tot['passing_measurements'],
                                                                         tot['finite_final_duals']) == (129, 126, 109))
    check('campaign: 79 finite same-model duals with a globality guarantee and no tightened bounds (BARON 23, '
          'Gurobi 30, SCIP 26); with 6 disclaimed, 6 tightened and 18 KAN comparisons they make up the 109',
          [per[s]['same_model_guaranteed_finite_duals'] for s in ('BARON', 'GUROBI', 'SCIP')] == [23, 30, 26]
          and tot['same_model_guaranteed_finite_duals'] + tot['finite_without_globality_guarantee']
          + tot['tightened_argument_bounds'] + tot['finite_against_R'] == tot['finite_final_duals'] == 109
          and (tot['finite_without_globality_guarantee'], tot['finite_against_R']) == (6, 18)
          and all(x['scip_argument_bounds_tightened'] != 'True' or finite_dual(x) for x in CAMP))
    within = [(x['instance'], x['solver']) for x in CAMP if x['primal'] != '' and finite_dual(x)
              and abs(q(x['primal']) - q(x['dual'])) <= q('1e-6') * max(abs(q(x['primal'])), abs(q(x['dual'])))]
    check('campaign: only BARON camshape100/200 end with a relative gap of at most 1e-6 (|P-D|/max(|P|,|D|))',
          within == [('camshape100', 'BARON'), ('camshape200', 'BARON')] and tot['runs_within_1e_6'] == 2, str(within))
    check('campaign: 10 overloaded first-batch runs; 6 SCIP tightened; 5 listed-dual improvements; 18 against R',
          (tot['overloaded_first_batch'], tot['tightened_argument_bounds'], tot['improves_best_listed_dual'],
           tot['finite_against_R']) == (10, 6, 5, 18))
    weaker = all((1 if x['sense'] == 'min' else -1) * (q(x['certificate_dual']) - q(x['dual'])) > 0
                 for x in CAMP if finite_dual(x))
    check('campaign: every finite final dual is weaker than the (old summary) certificate dual', weaker)
    claims = [(x['instance'], x['solver']) for x in CAMP if x['optimality_claim'] == 'True']
    check('campaign: only optimality claims are BARON camshape100/200',
          claims == [('camshape100', 'BARON'), ('camshape200', 'BARON')])
    return dict(per_solver=per, totals=tot,
                setup='GAMS 54.3.1; BARON 26.5.27, Gurobi 13.0.2, SCIP 10.0.3; one thread; 3600 s; '
                      'requested gaps 1e-9; 8192 MiB; BARON limit is CPU time, Gurobi/SCIP wall time',
                source='research-20260929/publication/solver-runs/results_table.csv')


# ================================================== headline figure data
def best_guaranteed_dual(n, s):
    rows = [x for x in CAMP if x['instance'] == n and finite_dual(x)]
    good = [x for x in rows if x['globality_warning'] != 'True']
    flags = []
    if not rows:
        return None, ['no finite bound']
    if not good:
        return None, ['only BARON values that BARON disclaims']
    best = (max if s == 1 else min)(good, key=lambda x: q(x['dual']))
    if best['scip_argument_bounds_tightened'] == 'True':
        flags.append('SCIP on a tightened model')
    if best['certificate_scope'].startswith('R'):
        flags.append('R only (KAN)')
    return best, flags


def figure_rows(inst):
    out = []
    for n in ALL:
        r = inst[n]
        s = 1 if r['sense'] == 'min' else -1
        U = q(r['U']['exact'])
        L = q(r['L']['exact'])
        lst = r['listed']['best_dual']

        def dist(d):
            return s * (U - d) / abs(U)
        row = dict(instance=n, family=family(n))
        row['listed'] = None if lst is None else float(dist(q(lst['value'])))
        row['listed_flag'] = 'no finite bound' if lst is None else ''
        best, flags = best_guaranteed_dual(n, s)
        row['solver'] = None if best is None else float(dist(q(best['dual'])))
        row['solver_name'] = None if best is None else best['solver']
        row['solver_flags'] = flags
        row['certified'] = 0.0 if r.get('exact_optimum') else float(dist(L))
        row['certified_exact_optimum'] = bool(r.get('exact_optimum'))
        # Separate kinds of one-hour bounds (LD-4): same stored model with a globality guarantee and no
        # tightened bounds; BARON values that BARON disclaims; SCIP bounds on tightened models; KAN rows
        # compare with the bound for R only (panel b, descriptive).
        fin = [x for x in CAMP if x['instance'] == n and finite_dual(x)]
        same = [x for x in fin if x['globality_warning'] != 'True' and x['scip_argument_bounds_tightened'] != 'True'
                and not x['certificate_scope'].startswith('R')]
        bs = (max if s == 1 else min)(same, key=lambda x: q(x['dual'])) if same else None
        row['same_model'] = None if bs is None else float(dist(q(bs['dual'])))
        row['same_model_solver'] = None if bs is None else solver_name(bs['solver'])
        row['baron_disclaimed'] = [float(dist(q(x['dual']))) for x in fin if x['globality_warning'] == 'True']
        row['scip_tightened'] = [float(dist(q(x['dual']))) for x in fin if x['scip_argument_bounds_tightened'] == 'True']
        row['kan_descriptive'] = n in KAN
        for x in fin:
            check(f'figure {n}: {x["solver"]} final dual weaker than the certified dual', dist(q(x['dual'])) > dist(L))
        if best is not None:
            check(f'figure {n}: solver dual weaker than certified dual', dist(q(best['dual'])) > dist(L))
        if lst is not None:
            check(f'figure {n}: listed dual weaker than certified dual', dist(q(lst['value'])) > dist(L))
        out.append(row)
    return out


# ========================================== Table 7: contradicted claims
def derive_claims(inst):
    """Table 7. Margins: distance of the reported value to the certified bound or
    exact value, rounded down. Values that are page or table displays are widened
    by half a unit of their last digit ('allow'); published single numbers and
    evaluated objectives are taken literally.

    'evaluation' records what the value is (round-3 review sol-status 4): 'none', a
    number printed by its source; 'exact', the objective at a listed point evaluated
    exactly; 'numerical', an ordinary high-precision evaluation without an enclosure
    (numerical evidence). For the one-hour points ('numerical'), the returned objective
    value of the trace file is also compared exactly with the bound; that comparison
    proves that the point is not exactly feasible."""
    rows = []

    def L_of(n):
        return q(inst[n]['L']['exact'])

    def add(source, model, claim, value, margin, meaning, viol, proof, qual, src, s=3, allow='none',
            evaluation='none', returned=None):
        group = 'campaign' if source == 'one-hour runs' else ('listed' if source.startswith('MINLPLib point')
                                                             or source.startswith('MINLPLib best') else 'published')
        mv, ms = sig(margin, s, up=False)
        check(f'claims: {model} / {claim}: margin {ms} > 0 and rounded down', margin > 0 and mv <= margin)
        row = dict(source=source, model=model, claim=claim, value=value, margin=ms, meaning=meaning,
                   violation=viol, category='A', proof=proof, qualifier=qual, allowance=allow,
                   data_source=src, group=group, evaluation=evaluation)
        if returned:
            row.update(returned)
        rows.append(row)

    def half(v):
        return unit_of(v) / 2

    # MINLPLib listed points
    lv = J(R / 'reviews/open-instances-verification/logs/lnts_verify.json')
    p1 = next(x for x in lv if x['name'] == 'lnts50')['minlplib_p1']
    # The objective of lnts50 is 50 times the variable at index 255 (no nonlinear objective), so its
    # value at the decimal point p1 is an exact decimal; recompute it from the .sol file.
    osil50 = read(R / 'publication/minlplib-status/pages/models/osil/lnts50.osil')
    names50 = re.findall(r'<var name="([^"]+)"', osil50)
    obj50 = re.search(r'<obj [^>]*>(.*?)</obj>', osil50).group(1)
    sol50 = dict(l.split() for l in read(R / 'open-instances/minlplib_sol/lnts50.p1.sol').splitlines()
                 if len(l.split()) == 2)
    check('claims: lnts50 objective is 50 x_256 and its value at p1 equals the evaluated value exactly',
          re.findall(r'<coef idx="(\d+)">([^<]*)</coef>', obj50) == [('255', '50')]
          and '<nl idx="-1"' not in osil50 and 50 * q(sol50[names50[255]]) == q(p1['obj']),
          f"{names50[255]} = {sol50.get(names50[255])}")
    add('MINLPLib point', 'lnts50', 'p1', p1['obj'], L_of('lnts50') - q(p1['obj']), 'below $v^*$',
        p1['rowviol'], 'exact optimum', 'exact objective $N h$ of p1',
        'research-20260929/reviews/open-instances-verification/logs/lnts_verify.json (minlplib_p1); '
        'research-20260929/open-instances/minlplib_sol/lnts50.p1.sol; optimum: lnts review', evaluation='exact')
    for n, pt in [('camshape200', 'p1'), ('camshape400', 'p1'), ('camshape400', 'p2'), ('camshape800', 'p2')]:
        c = next(x for x in CE if x['n'] == int(n[8:]))['minlplib_points'][pt]
        obj = Q(c['obj'])            # binary64 print of a high-precision evaluation
        add('MINLPLib point', n, pt, f'{c["obj"]:.15g}', L_of(n) - obj - q('1e-14'), 'below $v^*$',
            f'{c["row_viol"]:.2g}', 'exact optimum', 'exact evaluation, agreed by three codes',
            'paper-open-minlplib/development/dossiers/checks/camshape/check_exact.json (minlplib_points)',
            s=2 if pt == 'p1' else 3, allow='1e-14 (float print)', evaluation='exact')
    for pt in ('p1', 'p2'):
        pg = next(x for x in PAGES['hvycrash']['points'] if x['point'] == pt)
        add('MINLPLib point', 'hvycrash', pt, pg['value'], q(pg['value']) - Q(-437, 2000) - half(pg['value']),
            'above $v^*=-0.2185$', pg['infeas'], 'identity', 'objective is constant on $\\feas$',
            'research-20260929/bound-audit/pages.json', allow='half unit')
    et = J(R / 'reviews/wave2-small-verification/logs/etamac.json')['minlplib_p1']
    # v_etamac.py evaluates this objective (with logarithms) in ordinary mpmath arithmetic, without an
    # enclosure: the comparison of the printed value is exact, the value itself numerical evidence.
    add('MINLPLib point', 'etamac', 'p1', et['objective'], L_of('etamac') - q(et['objective']) - q('1e-13'),
        'below $L$', et['max_row_violation'], 'certified dual', 'objective evaluated without an enclosure (numerical evidence)',
        'research-20260929/reviews/wave2-small-verification/logs/etamac.json (minlplib_p1)', allow='1e-13 (print)',
        evaluation='numerical')
    pr = J(R / 'reviews/wave2-small-verification/logs/pricing050.json')['minlplib_p1']
    # v_pricing050.py sums the linear objective exactly (Fraction) and prints float(), which is
    # correctly rounded; the allowance 1e-12 exceeds half a unit in the last place at 1813.
    check('claims: pricing050 p1 allowance 1e-12 exceeds half an ulp of the printed binary64 value',
          q('1e-12') > Q(2) ** (math.frexp(abs(pr['objective']))[1] - 54))
    add('MINLPLib point', 'pricing050', 'p1', repr(pr['objective']), q(repr(pr['objective'])) - L_of('pricing050') - q('1e-12'),
        'above $L$ (max.)', f'{pr["max_row_violation"]:.2g}', 'certified dual', 'exact objective, printed in binary64',
        'research-20260929/reviews/wave2-small-verification/logs/pricing050.json (minlplib_p1)', allow='1e-12 (print)',
        evaluation='exact')
    EMFL = {'emfl050_3_3': '10.4017521318429', 'emfl050_5_5': '18.9136329557291',
            'emfl100_3_3': '18.1326531242336', 'emfl100_5_5': '32.6381903545115'}
    for n, lo in EMFL.items():
        p = PAGES[n]
        bp = min([x for x in p['points'] if x['section'] == 'primal'], key=lambda x: q(x['value']))
        add('MINLPLib point', n, bp['point'] + ', best primal', bp['value'], q(lo) - q(bp['value']) - half(bp['value']),
            'below $v^*$', bp['infeas'], 'exact optimum enclosure',
            'every listed dual valid' + ('; marked solved' if p['solved'] else ''),
            'optimum lower end: research-20260929/reviews/bound-audit-recheck.md; value: pages.json', allow='half unit')
    # our campaign: every evaluated point beyond a certified bound (point_checks.json). The value is
    # an ordinary 50-digit evaluation (numerical evidence). The returned objective value printed in
    # the trace file (inconsistencies.json) must agree with it to its printed digits and lie beyond
    # the bound by more than half a unit of its last digit; this exact comparison proves that the
    # returned point is not exactly feasible (S6.3).
    pc = J(R / 'publication/solver-runs/point_checks.json')
    trace = {(x['instance'], x['solver']): x for x in J(R / 'publication/solver-runs/inconsistencies.json')
             if x['kind'] == 'returned primal beyond certificate'}
    for (n, sv), t in sorted(trace.items()):
        if t['within_source_print_precision']:
            continue
        s_ = 1 if inst[n]['sense'] == 'min' else -1
        check(f'claims: {n} {sv}: returned objective value {t["value"]} of the trace file, widened by half a unit '
              'of its last digit, lies beyond the certified bound (exact)',
              s_ * (L_of(n) - q(t['value'])) - q(t['source_print_halfunit']) > 0)
    for x in pc:
        n = x['instance']
        s = 1 if inst[n]['sense'] == 'min' else -1
        mg = s * (L_of(n) - q(x['obj']))
        if mg <= 0:
            continue
        t = trace.get((n, x['solver']))
        tv, hu = (q(t['value']), q(t['source_print_halfunit'])) if t else (None, None)
        tmg = s * (L_of(n) - tv) - hu if t else None
        check(f'claims: {n} {x["solver"]}: the returned objective value of the trace lies beyond the bound by '
              'more than half a unit of its last digit and agrees with the 50-digit evaluation to its printed digits',
              t is not None and not t['within_source_print_precision'] and tmg > 0 and abs(q(x['obj']) - tv) <= hu,
              str(t and t['value']))
        tms = sig(tmg, 3, up=False)[1] if t else None
        claim = 'optimality claim' if any(c['instance'] == n and c['solver'] == x['solver'] and c['optimality_claim'] == 'True'
                                          for c in CAMP) else 'returned point'
        isk = n.startswith('kan')
        add('one-hour runs', n + (' ($R$)' if isk else ''), f'{solver_name(x["solver"])} {claim}',
            dec40(q(x['obj']), 12).rstrip('0'), mg,
            'below $L$ for $R$' if isk else ('below $L$' if s == 1 else 'above $L$ (max.)'),
            f'{float(q(x["max_viol"])):.2g}', 'certified dual',
            'valid dual; tolerance-level closure' if claim == 'optimality claim' else '',
            'research-20260929/publication/solver-runs/point_checks.json (50-digit evaluation); returned value: '
            'research-20260929/publication/solver-runs/inconsistencies.json (trace file)', evaluation='numerical',
            returned=dict(returned_value=t['value'], returned_value_halfunit=t['source_print_halfunit'],
                          returned_margin=tms))
    # published claims
    add('MINLPLib (Gurobi)', 'optcdeg2', 'listed dual = value of p2', '292.4171346',
        L_of('optcdeg2') - q('292.4171346') - q('5e-8'), 'below $L$', '1e-6', 'certified dual',
        'the listed dual bound is valid', 'pages.json (p2, listed dual); dtoc5-optcdeg2 dossier section 2', allow='half unit')
    add('CUTEst SIF', 'lukvle10', 'SOLTN', '352.237', L_of('lukvle10') - q('352.237'), 'below $L$', 'not reported',
        'certified dual', 'cause unknown; violation not reported', 'lnts-lukvle10 dossier; control literature report')
    for n in ('kan_r3_h1_n4', 'kan_r3_h1_n5'):
        add('Karia et al.\\ (SCIP 9.0.1)', n + ' ($R$)', 'optimum, gap 0', KAN_SCIP[n], L_of(n) - q(KAN_SCIP[n]),
            'below $L$ for $R$', 'about $10^{-6}$', 'certified dual',
            'valid as duals of the infeasible OSIL model',
            'solvers dossier Prop. 14; violation from the SCIP 10 rerun at the fixed input (network literature review)')
    add('Karia et al.\\ (ConvexHull)', 'kan_r5_h1_n5 ($R$)', 'primal value', '0.2725188',
        L_of('kan_r5_h1_n5') - q('0.2725188'), 'below $L$ for $R$', 'not reported', 'certified dual', '',
        'network literature report section 4.6; L2 synthesis')
    add('Kosolap (2019)', 'ex6_2_5', 'reported optimum', '-70.9586', L_of('ex6_2_5') - q('-70.9586'), 'below $L$',
        'not reported', 'certified dual', 'cause unknown; violation not reported', 'small literature report section 12; L2 synthesis')
    add('CAMINO (S-B-MIQP)', 'eg_disc2_s', 'recorded objective', '5.642100351878204',
        L_of('eg_disc2_s') - q('5.642100351878204'), 'below $L$', 'not recorded', 'certified dual', '',
        'eg dossier section 1.4; ghezzi2026-camino-benchmark-results-for-nonconvex')
    add('GAMS World', 'eg_int_s', 'old point (objvar)', '6.4531031527', L_of('eg_int_s') - q('6.4531031527'),
        'below $L$', '6.37e-9', 'certified dual', '', 'eg dossier section 1.4')
    # QPLIB copies: the reported value is assumed to lie within one unit of its last displayed digit
    # (no rounding direction assumed); the margin is measured from the floor of the copy's exact optimum.
    cl = read(D / 'dossiers/solvers-checks/r2/claims.log')
    rob = {x['file']: q(x['v_floor16']) for x in J(D / 'dossiers/checks/camshape/robust.json') if 'QPLIB' in x['file']}
    for solver, copy, gms, pat, thr, need in [
            ('MINOTAUR 0.4.1', 'QPLIB_3177 (copy of camshape800)', 'QPLIB_3177.gms',
             r'MINOTAUR 0\.4\.1 QPLIB_3177.*?claimed (\S+) ', '-4.2773', '$>8\\cdot10^{-9}$ needed'),
            ('ANTIGONE 1.1', 'QPLIB_2738 (copy of camshape100)', 'QPLIB_2738.gms',
             r'ANTIGONE 1\.1 QPLIB_2738.*?claimed (\S+) ', '-4.284301', '$>2.5\\cdot10^{-8}$ needed')]:
        c = re.search(pat, cl).group(1)
        top = q(c) + unit_of(c)
        check(f'claims: {copy}: one-unit threshold of the display {c} is {thr}', top == q(thr))
        add(solver + ' (QPLIB benchmark)', copy, 'global optimum', c, rob[gms] - top, "below the copy's bound",
            need, 'separate copy bound', 'assumes .nl = .gms' if 'MINOTAUR' in solver else '',
            'paper-open-minlplib/development/dossiers/checks/camshape/robust.json (v_floor16); '
            'paper-open-minlplib/development/dossiers/solvers-checks/r2/claims.log', s=3, allow='one unit')
    # the violation thresholds come from the copies' deficit bounds at eps = 8e-9 and 2.5e-8, which
    # exceed the one-unit thresholds by more than 1e-6 (so they hold whatever the display rounding)
    # (values printed at ten decimals; one unit of the tenth decimal is allowed for their rounding)
    eps = read(D / 'dossiers/solvers-checks/critic/eps_check.log')
    for gms, e, thr in (('QPLIB_3177.gms', '8e-9', '-4.2773'), ('QPLIB_2738.gms', '2.5e-8', '-4.284301')):
        val = re.search(re.escape(gms) + ' eps ' + re.escape(e) + r' v_eps=(\S+)', eps).group(1)
        check(f'claims: {gms} deficit bound {val} at eps {e} exceeds the one-unit threshold {thr} by more than 1e-6',
              q(val) - q('1e-10') - q(thr) > q('1e-6'))
    return rows


# =================================== qualitative tables (sourced text)
# Table 1 (tab:trust, compact, main text) and its full form (tab:trust-full,
# supplement S7.2). Fields of each row: family; dual arithmetic and trusted
# primitives, then '; ' and the data reading (the compact table drops the
# reading, which is the text after the last '; '); which implementation
# certifies the displayed dual and what the separately written second
# implementation certifies, in full and in a short form; status (Section 2.6;
# the status words are defined in the caption of tab:trust: verified = verified
# by a separately written implementation; weaker / partial second = proved, and
# a separately written implementation certifies a weaker bound / part of the
# domain; proved = no separately written second implementation; shared core =
# both KAN paths use one exponential and interval core); evidence level;
# primal construction (full table only); the full table adds the column TRUST_READ (below). Which
# primal proofs avoid mpmath is
# stated in tab:points-all. TRUST_FAMILY maps each row to the family key of
# LEVEL. Round-2 review (G6-02): 'by hand' replaced by 'on paper' / 'written
# proof' (the evidence level hand names the form of a proof); ann_cumene_tanh
# has the status proved, because its second code copied an idiom of the first
# (Section 2.6 and rem:ann-saturation, as revised by G1-02 on 2026-10-05).
TRUST_KEYS = ('family', 'dual', 'displayed_dual', 'displayed_dual_short', 'status', 'level', 'primal')
TRUST = [
    ('\\inst{lnts50}--\\inst{lnts400}', '[E] integers, rationals, integer square roots; exact', 'two integer-only codes certify the enclosure of $\\vstar$', 'two codes', 'verified', 'hand+stored', 'attaining point (\\cref{thm:lnts-opt}); Krawczyk points as a second witness'),
    ('\\inst{dtoc5}', '[E] rationals, sums in GMP; exact', 'two exact codes (full rational $q(\\lambda)$; fractions rounded up to $2^{-256}$) certify the displays', 'two exact codes', 'verified', 'hand+stored', 'explicit rational point [E]'),
    ('\\inst{optcdeg2}', '[E] exact stage minimization (Sturm sequences); exact', 'one exact code; a separately written interval code certifies 293.8760750958728', 'one code; second weaker', 'weaker second', 'stored', 'intermediate-value bracket; integer intervals [E]'),
    ('\\inst{camshape100}--\\inst{camshape800}', '[E] exact rational checks; exact', 'two exact codes and one with directed rounding agree to all printed digits', 'three codes', 'verified', 'hand+stored', 'envelope point [E]'),
    ('\\inst{lukvle10}', '[I] exp, log (both codes); exact / outward', 'one code; a separately written one certifies 352.238025369202', 'one code; second weaker', 'weaker second', 'rerun', 'triangular definitions from 640-digit seeds'),
    ('\\inst{chain50}--\\inst{chain400}', '[I] sqrt, log (both codes); outward', 'two codes certify the same binary64 bound', 'two codes, same bound', 'verified', 'rerun', 'explicit point in a real quadratic field [E]'),
    ('\\inst{catmix100}--\\inst{catmix800}', '[F] $+,-,\\times,\\div$ only; exact, then outward', 'one code; a separately written one certifies weaker bounds', 'one code; second weaker', 'weaker second', 'rerun', 'exact rational states [E]'),
    ('\\inst{ex6_2_5}, \\inst{ex6_2_7}', '[I] log; exact, then outward', 'one code; a separately written one certifies slightly stronger bounds', 'one code; second stronger', 'verified', 'rerun', 'rational point; objective in exact rational intervals'),
    ('\\inst{pricing050}', '[I] exp; outward', 'one code; a separately written one reproduces it', 'two codes, same bound', 'verified', 'stored', 'interior point; row slacks [I] (two codes)'),
    ('\\inst{etamac}', '[I] exp, log; exact / outward', 'one code; a separately written one certifies only $-15.294675643368096$', 'one code; second weaker', 'weaker second', 'stored', 'triangular definitions [I] (one code)'),
    ('\\inst{pindyck}', '[F]+[I] concavity proof; bound [E] from [I] enclosures; exact / outward', "concavity by two codes; bound from one code's [I] enclosures, a slightly weaker one from the other's", 'one code; second weaker', 'weaker second', 'stored', 'interval Newton per state [I] (two codes)'),
    ('the three \\inst{powerflow} instances', '[E] Lagrangian; PSD proof by exact LDL$^\\top$; exact', 'two exact codes', 'two exact codes', 'verified', 'stored', 'Krawczyk test on an active-set system; dyadic re-proof'),
    ('\\inst{hvycrash}', 'written proof of an identity, checked in exact rationals; exact / outward', 'written proof; one code checks the identities exactly', 'written proof; one checker', 'proved', 'hand', 'backward triangular definitions; feasibility by a written proof; two witnesses checked in [I]'),
    ('the three \\inst{eg} instances', '[F] under \\cref{hyp:fp-ieee} with \\cref{lem:eg-padding}; exp and powers EGAUDIT; rounded', 'leaf re-certifier on all leaves; second certificate for \\inst{eg_int_s}, \\inst{eg_disc_s}, part of \\inst{eg_disc2_s}', 'leaf re-certifier and a second code', 'verified; \\inst{eg_disc2_s}: partial second', 'rerun', 'interior points; dyadic intervals [E]'),
    ('\\inst{waterno2_06}--\\inst{waterno2_24}', "[F] / [E] rational node bounds; Python's correctly rounded \\texttt{math.fsum}; outward / exact", 'either of two codes yields every value', 'either of two codes', 'verified', 'rerun', 'exact algebraic point [E]'),
    ('\\inst{ann_cumene_tanh}', '[F], no library transcendental function; outward / rounded', 'two codes on one partition', 'two codes, one partition', 'proved; the second code copied an idiom of the first', 'rerun', 'forward triangular definitions; rational intervals'),
    ('KAN (six instances)', '[F]; one rigorous exp and interval core shared by both codes; outward', 'reported $L$: the weaker of two paths; path~(II) assumes no NaN; path~(I) replayed with guarded bounds', 'weaker of two paths', 'verified; shared core', 'rerun', 'points of $\\RP$; rational intervals'),
]
# Short arithmetic entries of the compact Table 1 where the full entry is long; the
# full entries are in tab:trust-full.
TRUST_ARITH_SHORT = {'lnts': '[E] rationals, integer square roots', 'optcdeg2': '[E] Sturm sequences',
                     'pindyck': '[F]+[I] concavity; [E] bound from [I] enclosures',
                     'powerflow': '[E] PSD proof by exact LDL$^\\top$',
                     'hvycrash': 'written proof of an identity, checked in [E]',
                     'eg': '[F] with \\cref{lem:eg-padding}; exp and powers EGSHORT',
                     'waterno2': '[F] / [E] node bounds; \\texttt{math.fsum}',
                     'ann': '[F], no library transcendental function', 'kan': '[F]; shared exp and interval core'}
# Short family names of the compact Table 1 (number of instances in parentheses).
TRUST_SHORT = {'lnts': '\\inst{lnts} (4)', 'camshape': '\\inst{camshape} (4)', 'chain': '\\inst{chain} (4)',
               'catmix': '\\inst{catmix} (4)', 'powerflow': '\\inst{powerflow} (3)', 'eg': '\\inst{eg} (3)',
               'waterno2': '\\inst{waterno2} (5)', 'kan': 'KAN (6)'}
TRUST_FAMILY = ['lnts', 'dtoc5', 'optcdeg2', 'camshape', 'lukvle10', 'chain', 'catmix', 'ex6_2', 'pricing050', 'etamac',
                'pindyck', 'powerflow', 'hvycrash', 'eg', 'waterno2', 'ann', 'kan']
# Column "read" of tab:trust-full (round-3 review opus-referee 2): whether, by the session records,
# the agent session that wrote the later of the two implementations had read the earlier one's code
# before its own results. Source: the records check of G1 (development/revise4-result.json,
# edits[0].rejected, session transcripts of 2026-09-30 to 2026-10-04): read first for lnts, dtoc5,
# optcdeg2, camshape, chain, catmix, the ex6_2 third code and the pricing050 check (one session), pindyck,
# powerflow0039p/r and both waterno2 lines; lukvle10 (open-instances verifier) read only the report
# and data; the wave-2 small verifier (etamac) read the first code only after its own numbers; the
# powerflow0030p session read the first certificate code only to learn its format. The ann review
# session read the first code in full (research-20260929/reviews/ann-extension-review.md, section 4);
# the records do not show whether before its own results. G1 did not check eg, the KAN second path or
# hvycrash. Count: 11 of the 15 families whose status rests on a second implementation (all but
# hvycrash and ann) read first; 2 did not; 2 were not checked.
TRUST_READ = {'lnts': 'yes', 'dtoc5': 'yes', 'optcdeg2': 'yes', 'camshape': 'yes', 'lukvle10': 'no', 'chain': 'yes',
              'catmix': 'yes', 'ex6_2': 'yes', 'pricing050': 'yes', 'etamac': 'no', 'pindyck': 'yes',
              'powerflow': '0039p, 0039r: yes; 0030p: format only', 'hvycrash': 'not checked', 'eg': 'not checked',
              'waterno2': 'yes', 'ann': 'read; order not recorded', 'kan': 'not checked'}

STAGED = [  # instance(s), stages / separator, free variables, split form, validity, window, stage check / branching, arithmetic
    ('\\inst{lnts50}--\\inst{lnts400}', '$N$ steps; states eliminated', 'states except the fixed end values', 'affine, for each fixed $h$', '\\cref{lem:split-bound}(d)', 'global $h$ by monotonicity', 'closed form; none', '[E]'),
    ('\\inst{dtoc5}', '$T=49{,}999$; dim.\\ 1', 'all except $y_0$', 'affine (costates)', '\\cref{lem:split-bound}(a)', 'none', 'closed-form convex quadratics; none', '[E]'),
    ('\\inst{optcdeg2}', '$N=50{,}000$; dim.\\ 2', '$y_1,\\dots,y_N$', 'quadratic in $v$, $q_t=0$ at both switches', '\\cref{lem:split-bound}(a) with state enclosures', 'none', 'exact (Sturm); 1-D cells in $v$', '[E]'),
    ('\\inst{lukvle10}', '497 pairs + tail; dim.\\ 2', 'all', 'affine (pair Lagrangian)', '\\cref{lem:split-bound}(d); row form of \\cref{prop:split-window}', '3-pair tail, 2-D entry state', 'interval B\\&B; 2-D', '[I]'),
    ('\\inst{chain50}--\\inst{chain400}', '$N$ stages; lifted dim.\\ 2', 'all except ends', 'field type (discrete catenary)', '\\cref{lem:split-bound}(c), (a)', 'end values (2-D)', 'interval B\\&B; 2-D', '[I]'),
    ('\\inst{catmix100}--\\inst{catmix800}', '$N$ stages; ray dim.\\ 1', 'states except $x_0$', 'concave chord minorants', '\\cref{lem:split-minorant}', 'none', 'per-ray interval bounds; 1-D', '[F]'),
    ('\\inst{waterno2_06} (not closed)', '6 periods of 166 variables; dim.\\ 3', 'monomial auxiliaries only', 'cellwise affine', '\\cref{prop:split-cellwise}', 'none', 'B\\&B per cell pair', '[F]/[E]'),
]

POINTS13 = [  # instances, earlier violation, method, arithmetic, mpmath-free re-proof, enclosure width
    ('\\inst{lnts50}--\\inst{lnts400}', '$\\le1.3\\cdot10^{-14}$', 'attaining point of \\cref{thm:lnts-opt} (scalar root); gives $U$', '[E]', 'yes (integers)', '$<1.11\\cdot10^{-91}$'),
    ('\\quad second witness', '', 'interval existence proof (Krawczyk test on 3 terminal equations)', '[I], 110 digits', 'yes (integers)', '$<3\\cdot10^{-109}$'),
    ('\\inst{dtoc5}', '$2.4\\cdot10^{-20}$', 'explicit exact point (rational)', '[E]', 'yes (exact)', 'exact'),
    ('\\inst{lukvle10}', '$3.48\\cdot10^{-15}$', 'triangular definitions (forward from 640-digit seeds)', '[I], 750 digits', 'yes (integer fixed point)', '$6.1\\cdot10^{-58}$ (box)'),
    ('\\inst{chain50}--\\inst{chain400}', '$\\le3.6\\cdot10^{-16}$', 'explicit exact point in a real quadratic field', '[E]', 'yes (exact)', 'exact field element'),
    ('\\inst{powerflow0030p}, \\inst{powerflow0039p}, \\inst{powerflow0039r}', '$2.1\\cdot10^{-13}$ / $1.2\\cdot10^{-12}$ / $7.9\\cdot10^{-12}$', 'interval existence proof (Krawczyk test on a fixed-coordinate square subsystem)', '[I], 80 digits', 'yes (dyadic)', '$\\le2.83\\cdot10^{-42}$'),
]
# Exact objective-enclosure widths behind the POINTS13 width cells.
PF_WIDTH_LOG = D / 'reviews/round1/g7-checks/powerflow-widths.log'      # exact widths, certify.py rerun in /tmp
LNTS_KRAW_LOG = R / 'publication/primal/lnts/logs/review_r2_check.log'  # widths of the Krawczyk points


def check_point_widths():
    txt = read(PF_WIDTH_LOG)
    ws = dict(re.findall(r'^(powerflow\w+) exact width (\d+/\d+)', txt, re.M))
    check('points table: three exact powerflow objective-enclosure widths read', len(ws) == 3, str(sorted(ws)))
    for n, w in sorted(ws.items()):
        check(f'points table: {n} exact width {float(Q(w)):.6e} <= 2.83e-42 (displayed cap)', Q(w) <= q('2.83e-42'))
    kw = [float(x) for x in re.findall(r'objective width (\S+)', read(LNTS_KRAW_LOG))]
    # binary64 prints of the widths; a relative print error of 1e-15 cannot reach the cap
    check('points table: lnts Krawczyk-point objective widths < 3e-109 (four prints, largest below 2.9e-109)',
          len(kw) == 4 and max(kw) < 2.9e-109, str(kw))

# ============================================================ LaTeX helpers
def inst_tex(n):
    return '\\inst{' + n + '}'   # \\inst is URL-based: underscores stay unescaped


def solver_name(s):
    # Vendors' spelling (development/terminology.md); MINLPLib's pages and the
    # run tables write GUROBI.
    return {'GUROBI': 'Gurobi'}.get(s, s)


def tags(s):
    # Arithmetic tags written '[E]' in the table data -> \\arith{E}
    s = re.sub(r'\[([EIFL])\]', r'\\arith{\1}', s)
    return s


def arith_cell(s):
    # Bare tags of the closures table ('E', 'F+I', 'F/E') -> \\arith{E}, ...
    return re.sub(r'(?<![A-Za-z{])([EIF])(?![A-Za-z}])', r'\\arith{\1}', s)


def num(s):
    """A decimal or 'a.bce-X' string as LaTeX math."""
    s = str(s).strip()
    m = re.fullmatch(r'(-?)(\d(?:\.\d+)?)e(-?\d+)', s)
    if m:
        sg, mant, ex = m.groups()
        if -3 <= int(ex) <= 5:
            v = Q(mant) * Q(10) ** int(ex)
            k = max(0, ndec(mant) - int(ex))
            return f'${sg}{fixed(v, k, up=False)[1]}$'
        if mant == '1':
            return f'${sg}10^{{{int(ex)}}}$'
        return f'${sg}{mant}\\cdot10^{{{int(ex)}}}$'
    if s.endswith('%'):
        return s[:-1] + '\\%'
    if s.endswith('.'):
        s = s[:-1]
    return f'${s}$'


def write(name, text):
    (TAB / name).write_text(text)


HEADER = ('% Generated by paper-open-minlplib/data/make_tables.py from data/numbers.json.\n'
          '% Do not edit by hand; rerun the script. Requires booktabs, array and rotating;\n'
          '% \\inst{} typesets an instance name; underscores are not escaped (macros.tex).\n')


def tab_closures(inst):
    # Round-1 review (G7-01): no size or arithmetic columns (sizes in tab:sem-hashes,
    # arithmetic in tab:trust); class and prior status are defined in Section 3; the
    # gap cells of attained exact optima read "exact optimum".
    rows = []
    for n in CLOSED:
        r = inst[n]
        lst = r['listed']['best_dual']
        ld = f'{num(lst["value"])} ({solver_name(lst["solver"])})'
        Ld = num(r['L']['table_display'])
        Ud = num(r['U']['table_display'])
        if r['exact_optimum']:
            gaps = '\\multicolumn{2}{l}{exact optimum}'
        else:
            gaps = (num(r['gap_abs']['display']) + ('\\textsuperscript{a}' if r['table_footnote_cert_ends'] else '')
                    + ' & ' + num(r['gap_rel']['display']))
        name = inst_tex(n) + ('\\textsuperscript{b}' if r['sense'] == 'max' else '')
        rows.append(' & '.join([name, ld, Ld, Ud, gaps, r['certificate']['class'], r['prior']['code']]) + ' \\\\')
    body = '\n'.join(rows)
    return HEADER + r'''\begin{sidewaystable}
\centering
\footnotesize
\setlength{\tabcolsep}{4pt}
\caption{The 31 closures (instance pages of 2026-09-29 and 2026-09-30, unchanged on 2026-10-02). Best listed dual: best single-solver bound on the instance page (MINLPLib writes GUROBI for Gurobi).
$L$: certified dual bound, rounded down; $U$: upper end of a rigorous enclosure of the objective at an exactly feasible point, rounded up (directions reversed for the maximization instance\textsuperscript{b}).
$\Delta=s(U-L)$ from the exact certificate ends and $\delta=\Delta/\min(|L|,|U|)$, both rounded up; for an attained exact optimum, $L$ and $U$ are the floor and ceiling displays of $v^*$.
Class and prior status: \cref{sec:results-closed,sec:results-prior}. \textsuperscript{a}The printed displays are shortened; $\Delta$ uses the certificate ends.}
\label{tab:closures}
\begin{tabular}{@{}llllllll@{}}
\toprule
instance & best listed dual (solver) & $L$ & $U$ & $\Delta$ & $\delta$ & class & prior status \\
\midrule
''' + body + r'''
\bottomrule
\end{tabular}
\end{sidewaystable}
'''


def tab_unclosed(inst, water, ann):
    rows = []
    for n in WATER + ['ann_cumene_tanh']:
        r = inst[n]
        sz = r['size']
        size = f'{sz["variables"]}' + (f' ({sz["integers"]})' if sz['integers'] else '') + f'/{sz["rows"]}'
        lst = r['listed']['best_dual']
        ld = 'none' if lst is None else f'{num(lst["value"])} ({solver_name(lst["solver"])})'
        fac = water[n]['factor']['display'] if n in water else '---'
        mark = '\\textsuperscript{a}' if n == 'waterno2_06' else ('\\textsuperscript{b}' if n.startswith('ann') else '')
        rows.append(' & '.join([inst_tex(n) + mark, size, ld, num(r['L']['display']), num(r['U']['display']),
                                num(r['gap_rel']['display']), fac]) + ' \\\\')
    w6 = water['waterno2_06']['progression']
    prog = ', '.join(f'{p["display"]} ({p["stage"]}, $\\delta\\le{p["gap"].replace("%", chr(92) + "%")}$)' for p in w6)
    return HEADER + r'''\begin{table}
\centering
\footnotesize
\setlength{\tabcolsep}{4pt}
\caption{Improved bounds for the five \inst{waterno2} instances and \inst{ann_cumene_tanh} (not closed).
$L$: certified dual bound, rounded down. $U$: objective of an exactly feasible point, rounded up.
$\delta=(U-L)/\min(|L|,|U|)$, rounded up. Factor: $L$ divided by the best listed dual bound, rounded down.
\textsuperscript{a}The primal point is MINLPLib's listed point p4 made exactly feasible. The dual bound improved in three steps: ''' + prog + r'''.
\textsuperscript{b}$L^*=-7447080719734483\cdot2^{-41}$; MINLPLib lists no dual bound; the bound also holds for the algebraically identical \inst{ann_cumene_exp}.}
\label{tab:unclosed}
\begin{tabular}{@{}lllllll@{}}
\toprule
instance & $n$ ($n_{\mathrm{int}}$)/$m$ & best listed dual (solver) & $L$ & $U$ & $\delta$ & factor \\
\midrule
''' + '\n'.join(rows) + r'''
\bottomrule
\end{tabular}
\end{table}
'''


def tab_kan(inst, kan):
    rows, notes = [], []
    marks = iter('ab')
    for n in KAN:
        r = inst[n]
        lst = r['listed']
        sc = kan[n].get('published_scip_optimum')
        mk = ''
        if sc is not None:
            mk = next(marks)
            notes.append(f'\\textsuperscript{{{mk}}}{num(sc["value"])}, at least {num(sc["below_L_by_at_least"])} below $L$')
        rows.append(' & '.join([inst_tex(n) + (f'\\textsuperscript{{{mk}}}' if mk else ''),
                                num(lst['best_dual']['value']), num(lst['best_point']['value']),
                                num(r['L']['display']), num(r['U']['display']), num(r['gap_abs']['display'])]) + ' \\\\')
    return HEADER + r'''\begin{table}
\centering
\footnotesize
\setlength{\tabcolsep}{4pt}
\caption{The six KAN instances of our set. The OSIL models have no exactly feasible point; $\RP$ is the OSIL model without the partition-of-unity rows.
$L$: certified lower bound on $\vstar(\Rnet)\le\vstar(\RP)$, the weaker of two bounding codes, rounded down.
$U$: upper end of the objective enclosure at a point of $\RP$, rounded up. $U-L$ is computed from the exact ends and rounded up.
Listed dual (Gurobi in all six cases) and listed primal: MINLPLib page values; the listed points are feasible only within a tolerance.
Published SCIP~9.0.1 values with zero gap (Karia et al.): ''' + '; '.join(notes) + r'''.}
\label{tab:kan}
\begin{tabular}{@{}llllll@{}}
\toprule
instance & listed dual & listed primal & $L$ & $U$ & $U-L$ \\
\midrule
''' + '\n'.join(rows) + r'''
\bottomrule
\end{tabular}
\end{table}
'''


def tab_audit(audit):
    # Portrait table: the gross/tolerance label follows from the sorted (d-phi)/|d| column
    # (the caption names the threshold), the absolute margin d-phi (numbers.json 'margin')
    # is not printed, the audit proof method is named in words (Section 7.3), and the
    # second implementations are listed in tab:audit-second (supplement) only.
    rows = []
    tol = 0
    for r in audit['pairs']:
        tol += r['label'] != 'gross'
        rows.append(' & '.join([inst_tex(r['instance']) + ('$^{\\checkmark}$' if r['solved_mark'] else ''),
                                solver_name(r['solver']), r['date'], num(r['d']), num(r['f_upper']),
                                num(r['rel_margin']), num(r['units']), r['route']]) + ' \\\\')
    check('audit table: tolerance-scale pairs are the last rows',
          all(r['label'] != 'gross' for r in audit['pairs'][len(audit['pairs']) - tol:]))
    c = audit['counts']
    return HEADER + r'''\begin{table}[t]
\centering
\scriptsize
\setlength{\tabcolsep}{2.6pt}
\caption{Listed bounds refuted under Hypothesis~H: the ''' + str(c['class_i_pairs']) + r''' listed per-solver dual bounds on ''' + str(c['class_i_instances']) + r''' instances of class~(i).
Pages fetched 2026-09-30, unchanged on 2026-10-02; all instances minimize. $d=\dval{s}$: value of the displayed dual bound~$s$.
$\varphi$: upper end of the enclosure of the objective at an exactly feasible point (audit implementation), rounded up to ten significant digits.
Margins: $(d-\varphi)/|d|$ (rel.)\ and $d-\varphi$ in units of the last displayed digit of $d$, computed from the exact upper end and rounded down; the last ''' + str(tol) + r''' rows, with $(d-\varphi)/|d|\le10^{-6}$, are tolerance-scale.
Audit proof (methods of \cref{sec:audit-existence}): \emph{listed point}, listed-point check; \emph{Krawczyk}, Krawczyk proof; \emph{shifted Krawczyk}, shifted Krawczyk proof; \emph{dedicated}, dedicated proof.
\Cref{tab:audit-second} gives the second, separately written proof of each pair.
$^{\checkmark}$: marked solved on MINLPLib.}
\label{tab:audit-pairs}
\begin{tabular}{@{}>{\raggedright\arraybackslash}p{3.55cm}llllll>{\raggedright\arraybackslash}p{1.26cm}@{}}
\toprule
instance & solver & date & $d$ & $\varphi\le$ & rel.\ $\ge$ & units $\ge$ & audit proof \\
\midrule
''' + '\n'.join(rows) + r'''
\bottomrule
\end{tabular}
\end{table}
'''


def trust_rows(eg_status):
    rows = []
    for r, fam in zip(TRUST, TRUST_FAMILY):
        r = dict(zip(TRUST_KEYS, r))
        r['family_short'] = TRUST_SHORT.get(fam, r['family'])
        r['arith_short'] = TRUST_ARITH_SHORT.get(fam, r['dual'].rsplit('; ', 1)[0]).replace(
            'EGSHORT', 'checked by the accuracy auditor' if eg_status == 'passed' else 'pending the accuracy audit')
        r['dual'] = r['dual'].replace('EGAUDIT', 'checked by the accuracy auditor (complete run passed)' if eg_status == 'passed'
                                      else 'pending the accuracy audit (until then: named assumptions A2$\'$ and pow)')
        r['read'] = TRUST_READ[fam]
        # long family names may break after the dash; the level may break after '+'
        r['family'] = r['family'].replace('}--\\inst{', '}--\\allowbreak\\inst{')
        r['level'] = r['level'].replace('+', '+\\allowbreak ')
        rows.append({k: tags(v) for k, v in r.items()})
    return rows


TRUST_STATUS = (r'''Status (\cref{sec:semantics-protocol}): \emph{verified} by a separately written implementation;
\emph{weaker second} or \emph{partial second}: proved, and a separately written implementation certifies a weaker bound or part of the domain;
\emph{proved}: no separately written second implementation (\inst{hvycrash}: a written proof; \inst{ann_cumene_tanh}: its second code copied an idiom of the first);
\emph{shared core}: both KAN bounding paths use one rigorous exponential and interval core.''')


def tab_trust(eg_status):
    # Main-text Table 1 (round-2 review G6-02): upright, without the data-reading and
    # primal columns, which tab:trust-full (supplement S7.2) keeps.
    rows = [' & '.join([r['family_short'], r['arith_short'], r['displayed_dual_short'], r['status'], r['level'].replace('+\\allowbreak ', '+')])
            + ' \\\\' for r in trust_rows(eg_status)]
    # [tb]: as a float page, the table left about 0.4 page empty (round-2 build)
    return HEADER + r'''\begin{table}[tb]
\centering
\footnotesize
\setlength{\tabcolsep}{3pt}
\caption{Trust base and verification by certificate family (number of instances in parentheses).
Arithmetic: tags (\cref{sec:semantics-trust}) and trusted primitives of the dual certificate.
Certified by: the codes that certify the displayed dual bound; ``second weaker'' or ``stronger'': the second implementation certifies a weaker or stronger bound.
''' + TRUST_STATUS + r'''
Level: evidence level (\cref{sec:semantics-trust}).
\Cref{tab:trust-full} gives the full entries, the data readings and the primal constructions.}
\label{tab:trust}
\begin{tabular}{@{}>{\raggedright\arraybackslash}p{2.5cm}>{\raggedright\arraybackslash}p{4.4cm}>{\raggedright\arraybackslash}p{3.4cm}>{\raggedright\arraybackslash}p{3.0cm}>{\raggedright\arraybackslash}p{1.8cm}@{}}
\toprule
family & arithmetic and trusted primitives & certified by & status & level \\
\midrule
''' + '\n'.join(rows) + r'''
\bottomrule
\end{tabular}
\end{table}
'''


def tab_trust_full(eg_status):
    # Supplement S7.2 (tab:trust-full): the full form of Table 1, sideways. Wider column
    # gaps than in revision 3, where the lnts and catmix cells touched (sol-referee round 2, item 7).
    rows = [' & '.join(r[k] for k in ('family', 'dual', 'displayed_dual', 'status', 'read', 'level', 'primal')) + ' \\\\'
            for r in trust_rows(eg_status)]
    return HEADER + r'''\begin{sidewaystable}
\centering
\scriptsize
\setlength{\tabcolsep}{4pt}
\caption{Trust base, data readings and primal constructions by certificate family (the full form of \cref{tab:trust}).
Dual: tags and level (\cref{sec:semantics-trust}), trusted primitives, data reading (\cref{app:semantics-codes}; ``X / Y'': codes differ).
Status as in \cref{tab:trust}.
Read first: whether, according to the session records, the agent session that wrote the later of the two implementations had read the code of the earlier one before its own results (\emph{format only}: only to learn the file format; \emph{not checked}: records not examined).
Primal: construction (\cref{sec:points-constructions}); mpmath-free proofs: \cref{tab:points-all}.}
\label{tab:trust-full}
\begin{tabular}{@{}>{\raggedright\arraybackslash}p{2.7cm}>{\raggedright\arraybackslash}p{4.7cm}>{\raggedright\arraybackslash}p{5.0cm}>{\raggedright\arraybackslash}p{2.3cm}>{\raggedright\arraybackslash}p{1.6cm}>{\raggedright\arraybackslash}p{1.4cm}>{\raggedright\arraybackslash}p{4.9cm}@{}}
\toprule
family & dual: arithmetic, trusted primitives; data reading & displayed dual certified by; second implementation & status & read first & level & primal construction and arithmetic \\
\midrule
''' + '\n'.join(rows) + r'''
\bottomrule
\end{tabular}
\end{sidewaystable}
'''


def tab_solvers(camp):
    per = camp['per_solver']
    items = [('kept outcomes', 'runs'), ('passing the measurement rule', 'passing_measurements'),
             ('finite final dual bounds', 'finite_final_duals'),
             ('\\quad unmodified model (GAMS file), globality guarantee, no tightened bounds', 'same_model_guaranteed_finite_duals'),
             ('\\quad without a globality guarantee', 'finite_without_globality_guarantee'),
             ('\\quad on tightened log/pow argument bounds', 'tightened_argument_bounds'),
             ('\\quad compared with $\\Rnet$ (KAN)', 'finite_against_R'),
             ('final dual improves the best listed dual', 'improves_best_listed_dual'),
             ('returned primal points', 'returned_primals'), ('raw optimality claims', 'raw_optimality_claims'),
             ('runs ending with relative gap at most $10^{-6}$', 'runs_within_1e_6'),
             ('accepted closures', 'accepted_closures'), ('capability failures', 'capability_failures'),
             ('other failures', 'other_failures'), ('memory stops', 'memory_stops'),
             ('runs in the overloaded first batch', 'overloaded_first_batch')]
    rows = []
    for lab, k in items:
        rows.append(' & '.join([lab] + [str(per[s][k]) for s in ('BARON', 'GUROBI', 'SCIP')] + [str(camp['totals'][k])]) + ' \\\\')
    return HEADER + r'''\begin{table}
\centering
\footnotesize
\setlength{\tabcolsep}{5pt}
\caption{One-hour runs on the 43 instances: GAMS~54.3.1 with BARON~26.5.27, Gurobi~13.0.2 and SCIP~10.0.3, one thread, 3600\,s, requested absolute and relative gaps $10^{-9}$, 8192\,MiB.
BARON's limit is CPU time; Gurobi and SCIP use wall time. The four indented rows partition the finite final dual bounds. A closure is accepted only if it is consistent with the certificates under exact feasibility.
The counts support no performance ranking.}
\label{tab:solvers}
\begin{tabular}{@{}lrrrr@{}}
\toprule
 & BARON & Gurobi & SCIP & total \\
\midrule
''' + '\n'.join(rows) + r'''
\bottomrule
\end{tabular}
\end{table}
'''


def tab_staged():
    rows = [' & '.join(tags(c) for c in r) + ' \\\\' for r in STAGED]
    return HEADER + r'''\begin{sidewaystable}
\centering
\footnotesize
\setlength{\tabcolsep}{3pt}
\caption{The 15 staged certificates and the \inst{waterno2_06} bound.
Stages and separator dimension; free variables (no finite bounds in the model); split form; validity result; window or case split;
how each stage problem is minimized and the branching dimension; arithmetic tags of the dual (\cref{sec:semantics-trust}).}
\label{tab:staged}
\begin{tabular}{@{}>{\raggedright\arraybackslash}p{2.4cm}>{\raggedright\arraybackslash}p{2.6cm}>{\raggedright\arraybackslash}p{2.2cm}>{\raggedright\arraybackslash}p{3.0cm}>{\raggedright\arraybackslash}p{2.4cm}>{\raggedright\arraybackslash}p{2.6cm}>{\raggedright\arraybackslash}p{3.2cm}>{\raggedright\arraybackslash}p{1.0cm}@{}}
\toprule
instances & stages; separator & free variables & split form & validity & window or case split & stage check; branching & arith. \\
\midrule
''' + '\n'.join(rows) + r'''
\bottomrule
\end{tabular}
\end{sidewaystable}
'''


def tab_points():
    rows = [' & '.join(tags(c) for c in r) + ' \\\\' for r in POINTS13]
    return HEADER + r'''\begin{table}
\centering
\footnotesize
\setlength{\tabcolsep}{3pt}
\caption{The 13 closures whose earlier points were feasible only within a tolerance.
Earlier violation: largest row violation of the point used before. Method: construction of \cref{sec:points-constructions} and its details.
The width is that of the enclosure of the objective of the exactly feasible point.}
\label{tab:points}
\begin{tabular}{@{}>{\raggedright\arraybackslash}p{2.4cm}>{\raggedright\arraybackslash}p{2.3cm}>{\raggedright\arraybackslash}p{3.6cm}>{\raggedright\arraybackslash}p{1.6cm}>{\raggedright\arraybackslash}p{2.0cm}>{\raggedright\arraybackslash}p{1.6cm}@{}}
\toprule
instances & earlier violation & method & arithmetic & mpmath-free re-proof & width \\
\midrule
''' + '\n'.join(rows) + r'''
\bottomrule
\end{tabular}
\end{table}
'''


def tab_sem_hashes(inst):
    # Supplement S7 (tab:sem-hashes): sizes and SHA-256 prefixes of the 43 stored models; the sizes
    # moved here from Table 2 (round-1 review G7-01).
    cells = []
    for n in ALL:
        sz = inst[n]['size']
        size = f'{sz["variables"]}' + (f' ({sz["integers"]})' if sz['integers'] else '') + f'/{sz["rows"]}'
        cells.append(f'{inst_tex(n)} & {size} & \\texttt{{{sz["osil_sha256"][:16]}}}')
    half = (len(cells) + 1) // 2
    left, right = cells[:half], cells[half:] + [' & & ']
    rows = [f'{a} & {b} \\\\' for a, b in zip(left, right)]
    return HEADER + r"""\begin{table}[htbp]
\centering
\footnotesize
\setlength{\tabcolsep}{3pt}
\caption{The 43 stored OSIL models: $n$ ($n_{\mathrm{int}}$)/$m$, variables (integer variables)/rows, and the first 16 hexadecimal digits of the SHA-256 hash. The files were fetched on 2026-09-29 and found unchanged on 2026-10-02.}
\label{tab:sem-hashes}
\begin{tabular}{@{}lll@{\qquad}lll@{}}
\toprule
instance & $n$ ($n_{\mathrm{int}}$)/$m$ & SHA-256 prefix & instance & $n$ ($n_{\mathrm{int}}$)/$m$ & SHA-256 prefix \\
\midrule
""" + '\n'.join(rows) + r"""
\bottomrule
\end{tabular}
\end{table}
"""


def model_tex(m):
    """Model cell of the claims tables: instance names through \\inst."""
    if m.endswith(')') and ' (copy of ' in m:
        a, b = m[:-1].split(' (copy of ')
        return inst_tex(a) + ' (copy of ' + inst_tex(b) + ')'
    if m.endswith(' ($R$)'):
        return inst_tex(m[:-len(' ($R$)')]) + ' ($\\Rnet$)'
    return inst_tex(m)


def claim_rows(claims):
    def cell(v):
        v = str(v)
        return num(v) if re.fullmatch(r'-?\d+(\.\d+)?(e-?\d+)?', v) else v
    rows = []
    for c in claims:
        # the basis of the margin (exact optimum, certified dual, ...) is named by the position cell
        rows.append(' & '.join([c['source'], model_tex(c['model']), c['claim'].replace('_', '\\_'),
                                cell(c['value']), '$\\ge' + num(c['margin'])[1:], c['meaning'].replace('$R$', '$\\Rnet$'), cell(c['violation']),
                                c['qualifier']]) + ' \\\\')
    return rows


CLAIM_COLS = ('\\begin{tabular}{@{}' + ''.join('>{\\raggedright\\arraybackslash}p{%s}' % w for w in
              ['2.8cm', '3.3cm', '3.4cm', '2.9cm', '1.9cm', '2.6cm', '1.9cm', '4.2cm']) + '@{}}\n'
              '\\toprule\nsource & model & claim & value & margin & position & violation & qualifier \\\\\n\\midrule\n')
KEY_CAMPAIGN = {('camshape100', 'BARON'), ('camshape200', 'BARON'), ('camshape100', 'SCIP')}


def tab_claims(claims):
    camp = [c for c in claims if c['group'] == 'campaign']
    key = [c for c in camp if (c['model'], c['claim'].split()[0]) in KEY_CAMPAIGN]
    main = [c for c in claims if c['group'] == 'listed'] + key + [c for c in claims if c['group'] == 'published']
    n_other = len(camp) - len(key)
    # returned values beyond a certified bound, beyond the printing precision of the trace
    # files (5 of them KAN values compared with the bound for R_net); the evaluated ones are
    # the campaign rows of the claims table (S6.3)
    flags = [x for x in J(R / 'publication/solver-runs/inconsistencies.json')
             if x['kind'] == 'returned primal beyond certificate']
    beyond = [x for x in flags if not x['within_source_print_precision']]
    check('claims table: 36 returned-primal flags, 35 beyond printing precision, of which the '
          f'{len(camp)} campaign rows are the evaluated ones',
          (len(flags), len(beyond), len(camp)) == (36, 35, 15)
          and {(x['instance'], x['solver']) for x in beyond if x['point_checked']}
          == {(c['model'].split()[0], c['claim'].split()[0].upper()) for c in camp},
          f'{len(flags)}, {len(beyond)}, {len(camp)}')
    return HEADER + r'''\begin{sidewaystable}
\centering
\scriptsize
\setlength{\tabcolsep}{2pt}
\caption{Reported values that no exactly feasible point attains (category~A; ``tolerance artifact'' names the category, not a diagnosed cause).
Margin: distance to the certified bound $L$ or exact optimum $v^*$ named in the position column (for the QPLIB copies, the copy's own bound), rounded down; page or table displays are first widened by half a unit of their last digit, the QPLIB values by one unit.
Value: the number as reported, except for the listed points of \inst{lnts50}, \inst{camshape}, \inst{etamac} and \inst{pricing050} and for the one-hour runs, whose value is the objective at the point as we evaluated it, exactly except for \inst{etamac} and the one-hour runs (ordinary evaluations without an enclosure; numerical evidence).
Violation: largest row or bound violation of the reported point, where known.
One-hour runs: the two optimality claims and the SCIP point on \inst{camshape100}; of the ''' + str(len(beyond)) + r''' returned values beyond a certified bound (\cref{app:solvers-points}), \cref{tab:claims-campaign} lists the ''' + str(len(camp)) + r''' that we evaluated at 50 digits, ''' + str(n_other) + r''' of them not repeated here.}
\label{tab:claims}
''' + CLAIM_COLS + '\n'.join(claim_rows(main)) + r'''
\bottomrule
\end{tabular}
\end{sidewaystable}
'''


def tab_claims_campaign(claims):
    # Portrait table (round-1 revision, G7-18): the source column is "one-hour runs" in every row.
    camp = [c for c in claims if c['group'] == 'campaign']
    rows = [' & '.join(r.split(' & ')[1:]) for r in claim_rows(camp)]
    cols = ('\\begin{tabular}{@{}' + ''.join('>{\\raggedright\\arraybackslash}p{%s}' % w for w in
            ['2.6cm', '2.5cm', '2.7cm', '1.6cm', '1.8cm', '1.4cm', '2.4cm']) + '@{}}\n'
            '\\toprule\nmodel & claim & value & margin & position & violation & qualifier \\\\\n\\midrule\n')
    # [tb]: with p, this half-page table took a float page of its own (round-2 build)
    return HEADER + r"""\begin{table}[tb]
\centering
\scriptsize
\setlength{\tabcolsep}{2pt}
\caption{Returned points and optimality claims of the one-hour runs whose objective lies beyond a certified bound: the """ + str(len(camp)) + r""" points that we evaluated at 50 digits (\cref{app:solvers-points}).
Value and violation: ordinary 50-digit evaluations of the objective and of the largest row or bound violation at the returned point (numerical evidence); margins are rounded down.
The returned objective value in each run's trace file agrees with the value to its printed digits and lies beyond the bound by more than half a unit of its last digit; this exact comparison proves that the returned point is not exactly feasible (\cref{app:solvers-points}).
For the KAN instances the bound is the bound $L$ for the relaxation $\Rnet$.}
\label{tab:claims-campaign}
""" + cols + '\n'.join(rows) + r"""
\bottomrule
\end{tabular}
\end{table}
"""


# ===================================================== display provenance
PROV_DOCS = {'decision register': D / 'decision-register.md', 'outline': D / 'outline.md',
             'summary': R / 'open-instances-summary.md',
             'lnts review': D / 'reviews/sol-lnts-theorem3.md', 'dtoc5 review': D / 'reviews/sol-dtoc5-exact.md'}
for _f in sorted((D / 'dossiers').glob('*.md')):
    PROV_DOCS['dossier ' + _f.stem] = _f
_PROV_TEXT = {}


def provenance(disp):
    """Documents that print this exact display string (ASCII or Unicode minus)."""
    if not _PROV_TEXT:
        for k, f in PROV_DOCS.items():
            _PROV_TEXT[k] = read(f)
    alts = {disp, disp.replace('-', '−')}
    hits = []
    for k, t in _PROV_TEXT.items():
        for a in alts:
            if re.search(r'(?<![0-9.])' + re.escape(a) + r'(?![0-9])', t):
                hits.append(k)
                break
    return hits


# ===================================================================== main
def eg_audit_status():
    log = D / 'eg-audit/out/compare.log'
    if not log.exists():
        return 'pending', 'compare.log not present'
    last = [l for l in read(log).splitlines() if l.strip()]
    last = last[-1] if last else ''
    if last.startswith('RESULT: PASS (complete run'):
        return 'passed', last
    return 'pending', last


def main():
    inst = {}
    for n in ALL:
        info = osil_info(n)
        rec = dict(instance=n, family=family(n), sense=info['sense'],
                   size={k: info[k] for k in ('variables', 'integers', 'rows', 'osil', 'osil_sha256')},
                   listed=listed(n))
        check(f'{n}: OSIL sense equals page sense', info['sense'] == PAGES[n]['sense'])
        check(f'{n}: OSIL variable and row counts equal the page counts',
              (str(info['variables']), str(info['rows'])) == (PAGES[n]['nvars'], PAGES[n]['ncons']))
        check(f'{n}: no solved mark', PAGES[n]['solved'] is False)
        if n in CLOSED:
            rec['status'] = 'closed'
            rec.update(derive_closed(n))
        elif n in WATER:
            rec['status'] = 'improved, not closed'
            rec.update(derive_water(n))
        elif n == 'ann_cumene_tanh':
            rec['status'] = 'improved, not closed (no listed dual)'
            rec.update(derive_ann())
        else:
            rec['status'] = 'OSIL model exactly infeasible; enclosure for R_P'
            rec.update(derive_kan(n))
        fam = family(n)
        rec['certificate'] = dict(**{'class': CLASS.get(n)}, arith=dict(dual=ARITH[fam][0], primal=ARITH[fam][1]),
                                  arith_note=ARITH_NOTE[fam], mechanism=MECH[fam], evidence_level=LEVEL[fam])
        rec['prior'] = dict(code=PRIOR[n][0], note=PRIOR[n][1])
        for side in ('L', 'U'):
            for key in ('display', 'table_display'):
                if key in rec[side]:
                    hits = provenance(rec[side][key])
                    rec[side][key + '_printed_in'] = hits or ['new: generated here from the exact value']
        inst[n] = rec
    # catmix400: stored primal end consistent with the dossier's exact rerun
    fl = q(re.search(r'J \* 1e30 \(floor\) = (\S+)', cm400).group(1))
    check('catmix400: exact objective of the authors\' point lies in [floor, floor+1]*1e-30 around the stored upper end',
          fl / 10 ** 30 <= q(inst['catmix400']['U']['exact']) <= (fl + 1) / 10 ** 30)
    # aggregate checks behind the headline statements
    worst = max(CLOSED, key=lambda n: 0 if inst[n]['exact_optimum'] else
                q(inst[n]['gap_abs']['exact']) / min(abs(q(inst[n]['L']['exact'])), abs(q(inst[n]['U']['exact']))))
    wr = q(inst[worst]['gap_abs']['exact']) / min(abs(q(inst[worst]['L']['exact'])), abs(q(inst[worst]['U']['exact'])))
    check('headline: largest relative gap over the 31 closures <= 3.1e-9 (catmix800)', wr <= q('3.1e-9') and worst == 'catmix800',
          f'{worst} {float(wr):.4e}')
    check('headline: 9 exact optima', sum(inst[n]['exact_optimum'] for n in CLOSED) == 9)
    check('trust table: one row per family, levels equal the evidence levels of numbers.json',
          len(TRUST) == len(TRUST_FAMILY) and all(len(r) == len(TRUST_KEYS) and r[5] == LEVEL[f]
                                                   for r, f in zip(TRUST, TRUST_FAMILY)))
    lev = [LEVEL[family(n)] for n in CLOSED]
    check('evidence levels of the 31 closures: 14 rerun, 7 stored, 9 hand+stored, 1 hand',
          [lev.count(k) for k in ('rerun', 'stored', 'hand+stored', 'hand')] == [14, 7, 9, 1],
          str([lev.count(k) for k in ('rerun', 'stored', 'hand+stored', 'hand')]))
    pri = [PRIOR[n][0] for n in CLOSED]
    grp = [sum(c in g for c in pri) for g in (('fp closure', 'fp near-closure'),
                                              ('listed solve', 'related model', 'value only', 'unread source'), ('none',))]
    check('prior status of the 31 closures: 7 fp (near-)closures, 9 other earlier results, 15 none', grp == [7, 9, 15], str(grp))
    check_point_widths()
    check('class counts: staged 15, comparison 4, dense rows 3, convexity 5, identity 1, reduced space 3',
          [sum(CLASS[n] == c for n in CLOSED) for c in CLASS_ORDER] == [15, 4, 3, 5, 1, 3])
    water = {n: {k: inst[n][k] for k in ('factor', 'progression') if k in inst[n]} for n in WATER}
    facs = [q(inst[n]['factor']['display']) for n in WATER]
    check('headline: waterno2 factors 1.68 to 6.21 (rounded down)', min(facs) == q('1.68') and max(facs) == q('6.21'))
    kan = {n: inst[n] for n in KAN}
    audit = derive_audit()
    aud_tot = dict(bounds=len(audit['pairs']) + len(audit['rocket']),
                   instances=len({r['instance'] for r in audit['pairs']} | {r['instance'] for r in audit['rocket']}),
                   lindo=sum(r['solver'] == 'LINDO' for r in audit['pairs']) + len(audit['rocket']))
    check('headline: 22 invalid listed bounds on 18 instances with the rocket bounds, 16 of them LINDO',
          (aud_tot['bounds'], aud_tot['instances'], aud_tot['lindo']) == (22, 18, 16), str(aud_tot))
    camp = derive_campaign()
    claims = derive_claims(inst)
    fig = figure_rows(inst)
    weaker_new = [(x['instance'], x['solver']) for x in CAMP if finite_dual(x)
                  and not ((1 if inst[x['instance']]['sense'] == 'min' else -1)
                           * (q(inst[x['instance']]['L']['exact']) - q(x['dual'])) > 0)]
    check('campaign: every finite final dual is weaker than the certified dual of this file', not weaker_new, str(weaker_new))
    egs, egline = eg_audit_status()
    check('eg exp/pow audit status read from development/eg-audit/out/compare.log', True, f'{egs}: {egline}')
    # wrap up numbers.json
    numbers = dict(
        generated_by='paper-open-minlplib/data/make_tables.py',
        generated_on=str(date.today()),
        conventions=dict(
            semantics='OSIL decimals read as exact rationals (reading (b)); exact feasibility without tolerance',
            displays='dual bounds rounded down (up for maximisation), primal values rounded up (down for maximisation), '
                     'gaps rounded up, at-least margins and factors rounded down; never to nearest',
            abs_gap='Delta = s(U - L) from the exact certificate ends; 3 significant digits, rounded up',
            rel_gap='delta = Delta/min(|L|,|U|); 3 significant digits rounded up; percent cells two decimals '
                    '(three significant digits below 1%) rounded up',
            listed='best single-solver dual bound on the instance page; best point with listed violation <= 1e-8',
            snapshot='site updated 2026-09-14; instance pages fetched 2026-09-29, audit pages 2026-09-30; '
                     'unchanged at the 2026-10-02 refresh'),
        headline=dict(
            closures=len(CLOSED), exact_optima=sum(inst[n]['exact_optimum'] for n in CLOSED),
            max_relative_gap=dict(instance=worst, value=sig(wr, 2, True)[1], exact_decimal=dec40(wr, 20)),
            waterno2_factor_range=[inst['waterno2_06']['factor']['display'], max((inst[n]['factor']['display'] for n in WATER), key=q)],
            waterno2_gaps=[inst[n]['gap_rel']['display'] for n in WATER],
            ann_gap=inst['ann_cumene_tanh']['gap_rel']['display'],
            kan_max_gap=dict(kan_r5_h1_n3=inst['kan_r5_h1_n3']['gap_abs']['display'],
                             others=max((inst[n]['gap_abs']['display'] for n in KAN if n != 'kan_r5_h1_n3'), key=q)),
            audit=dict(bounds=audit['counts']['per_solver_bounds'], pages=audit['counts']['pages'],
                       points=audit['counts']['points'], invalid_pairs=audit['counts']['class_i_pairs'],
                       instances=audit['counts']['class_i_instances'],
                       invalid_with_rocket=aud_tot['bounds'], instances_with_rocket=aud_tot['instances'],
                       lindo_with_rocket=aud_tot['lindo'],
                       note='class (i) counts from the screen; the totals add the three LINDO rocket bounds '
                            'outside the screen (Section 7.4)'),
            campaign=dict(kept=camp['totals']['runs'], accepted_closures=camp['totals']['accepted_closures'],
                          finite_final_duals=camp['totals']['finite_final_duals'],
                          same_model_guaranteed_finite_duals=camp['totals']['same_model_guaranteed_finite_duals'],
                          runs_within_1e_6=camp['totals']['runs_within_1e_6'])),
        instances=inst,
        waterno2=water,
        ann=inst['ann_cumene_tanh'],
        kan=kan,
        audit=audit,
        campaign=camp,
        claims_table=claims,
        headline_figure=fig,
        eg_audit=dict(status=egs, compare_log_last_line=egline),
        trust_table=[dict(zip(TRUST_KEYS, r)) for r in TRUST],
        sources=dict(sorted(SOURCES.items())))
    TAB.mkdir(exist_ok=True)
    write('tab-closures.tex', tab_closures(inst))
    write('tab-unclosed.tex', tab_unclosed(inst, {n: inst[n] for n in WATER}, inst['ann_cumene_tanh']))
    write('tab-kan.tex', tab_kan(inst, kan))
    write('tab-audit-pairs.tex', tab_audit(audit))
    write('tab-trust.tex', tab_trust(egs))
    write('tab-trust-full.tex', tab_trust_full(egs))
    write('tab-solvers.tex', tab_solvers(camp))
    write('tab-staged.tex', tab_staged())
    write('tab-points.tex', tab_points())
    write('tab-sem-hashes.tex', tab_sem_hashes(inst))
    write('tab-claims.tex', tab_claims(claims))
    write('tab-claims-campaign.tex', tab_claims_campaign(claims))
    (HERE / 'numbers.json').write_text(json.dumps(numbers, indent=1, ensure_ascii=False) + '\n')
    lines = [f'make_tables.py check log ({date.today()}); {len(CHECKS)} checks, {len(FAILS)} failed',
             f'eg exp/pow audit: {egs} ({egline})', '']
    for ok, lab, det in CHECKS:
        lines.append(('PASS ' if ok else 'FAIL ') + lab + (f'  [{det}]' if det else ''))
    lines.append('')
    lines.append('Sources read (sha256):')
    for k, v in sorted(SOURCES.items()):
        lines.append(f'  {v}  {k}')
    lines.append('')
    lines.append('ALL CHECKS PASSED' if not FAILS else 'FAILED: ' + '; '.join(FAILS))
    (HERE / 'check.log').write_text('\n'.join(lines) + '\n')
    print('\n'.join(l for l in lines if l.startswith('FAIL')))
    print(f'{len(CHECKS)} checks, {len(FAILS)} failed')
    return 1 if FAILS else 0


if __name__ == '__main__':
    sys.exit(main())
