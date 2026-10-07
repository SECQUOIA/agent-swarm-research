"""Targeted symbolic and arithmetic audit of the round 1 note corrections."""
import json
import re
from fractions import Fraction as Fr
from pathlib import Path
import sympy as sp


ROOT = Path(__file__).resolve().parent.parent
note = (ROOT / 'note.md').read_text()
a, b, c, m1, m2, n11, n12, n21, n22 = sp.symbols('a b c m1 m2 n11 n12 n21 n22')
S = sp.Matrix([[a, b], [b, c]])
J = sp.Matrix([[0, 1], [-1, 0]])
m = sp.Matrix([m1, m2])
N = sp.Matrix([[n11, n12], [n21, n22]])
v = J * S * m
assert (S * J.T * S + S.det() * J).applyfunc(sp.expand) == sp.zeros(2)
L = (m.T * J * N * J * S * m)[0]
assert sp.Poly(L, a, b, c).total_degree() <= 1
assert sp.expand(-(v.T * S * N * v)[0] - S.det() * L) == 0
assert sp.expand((v.T * S * v)[0] - S.det() * (m.T * S * m)[0]) == 0
assert sp.expand((v.T * S * m)[0]) == 0
print('PASS Lemma 8 identities for general symmetric S, m and N')

# Lemma 7: FT = [[f11, f12], [f21, f22]]. In the rank-two case,
# f21 = 0, and the image plane has constant A22 = f22 != 0.
f11, f12, f21, f22, x, y, w = sp.symbols('f11 f12 f21 f22 x y w')
FT = sp.Matrix([[f11, f12], [f21, f22]])
M = sp.Matrix([[w, x], [y, 1]])
A = (FT * M + (FT * M).T) / 2
linear = sp.Matrix([A[0, 0], A[0, 1], A[1, 1]]).jacobian([w, x, y])
assert sp.expand(linear.det() + f21 * FT.det() / 2) == 0
assert A[1, 1].subs(f21, 0) == f22
print('PASS Lemma 7 image-plane criterion and nonzero constant entry')

sb = sp.Matrix([[sp.Rational(3, 2), sp.Rational(-9, 2)], [0, 1]])
mt = sb.inv() * sp.Matrix([1, 0])
rays = [sp.Matrix([[sp.Rational(33, 2), sp.Rational(7, 2)], [-6, 0]]),
        sp.Matrix([[sp.Rational(-39, 2), sp.Rational(-1, 2)], [6, 0]]),
        sp.Matrix([[1, sp.Rational(9, 2)], [sp.Rational(5, 2), 0]])]
forms = [sp.expand((mt.T * J * sb.inv() * ray * J * S * mt)[0]) for ray in rays]
assert forms == [-8 * b / 3, 8 * b / 3, 10 * b / 9]
assert sp.expand((mt.T * S * mt)[0]) == 4 * a / 9
print('PASS Lemma 8 Theorem 14 forms:', forms)

cuts = json.loads((ROOT / 'logs/revision-r1/closure_lower_prop16_cuts.json').read_text())
value = Fr(cuts['value'])
original_log = (ROOT / 'logs/closure_lower_prop16.log').read_text()
original_value = re.search(r'exact LP value[^\n]*?: (\d+/\d+)', original_log).group(1)
assert value == Fr(original_value)
assert len(cuts['cuts']) == 60
assert Fr('0.9953611') <= value < Fr('0.9953612')
assert Fr('0.99536') <= value <= Fr(999, 1000)
assert Fr('0.97538') <= Fr('0.9753853514') < Fr('0.97539')
assert Fr('0.9753853514') <= Fr('0.9753853514025715')
assert Fr('0.9753853514557704') <= Fr('0.9753853515')
assert Fr(2539, 10000) == Fr('0.2539')
assert Fr(136, 525) <= Fr('0.25905') <= Fr('0.2591')
assert Fr(49, 50) == Fr('0.98')
assert Fr(4919, 5000) == Fr('0.9838')
assert Fr(9839, 10000) == Fr('0.9839')
weights = [Fr(11, 20), Fr(1, 10**6), Fr(9, 20)]
lam = [Fr(2211, 10000), Fr(8805, 10000), Fr(2464, 10000)]
zcl_upper = sum(wj * lj for wj, lj in zip(weights, lam))
assert zcl_upper == Fr(464971761, 2000000000) <= Fr('0.2324859')
assert Fr(649, 2500) == Fr('0.2596')
assert Fr('1.1166') <= Fr(649, 2500) / zcl_upper
# sqrt(65/14) > 1 + 4*0.2886, checked by squaring positive rationals.
assert Fr(65, 14) > (1 + 4 * Fr('0.2886'))**2
mu4 = 4 * (sp.sqrt(2) - 1)
wc_M = sp.Matrix([[1, 1], [-1, 1]])
wc_N4 = wc_M.inv() * sp.Matrix([[-1, 0], [0, 0]])
wc_A4 = sp.eye(2) + mu4 * (wc_N4 + wc_N4.T) / 2
assert sp.simplify(wc_A4.det()) == 0
assert wc_A4[0, 0] > 0 and wc_A4[1, 1] > 0
assert sp.simplify(1 / mu4 - (sp.sqrt(2) + 1) / 4) == 0
assert '0.9953612 ≤' not in note and '0.97539 ≤' not in note
assert 'certified `[0.97539' not in note
print('PASS all rounded certified endpoints, factor lower bound and case (v) bound')

section = note.split('## 7. ')[1].split('## 8. ')[0]
rows = [line.split('|') for line in section.splitlines() if line.startswith('| ')][1:]
assert len(rows) == 11
p_count = sum(row[5].strip() != '—' for row in rows)
bp_rows = [row for row in rows if row[6].strip() != '—']
different = [row[1].strip() for row in bp_rows
             if len(set(part.strip() for part in row[6].split('→'))) > 1]
assert (p_count, len(bp_rows), different) == (11, 7, ['adv8_1'])
assert '17 of 18 cases' in section
print('PASS Section 7 count: 11 P + 7 BP values; sole difference adv8_1 BP')

ratio_note = (ROOT.parent / 'ratio-bound/note.md').read_text()
b2 = ratio_note.split('**Theorem B2 (computer-assisted).**')[1].split('*Proof of (1).*')[0]
assert 'For every `ε ∈ (0, 1)`' in b2 and '137 √ε / z_0' in b2
assert 3 * 137 == 411
assert '411√ε/z_0' in note
print('PASS Corollary 14 rate and domain against ratio-bound Theorem B2(1)')

numbered = re.findall(r'^\*\*(?:Lemma|Theorem|Proposition|Corollary) (\d+)\b', note, re.M)
# Lemma 12 is the inline explanation immediately before Proposition 13.
assert [int(n) for n in numbered] == list(range(1, 12)) + [13, 14, 15, 16]
assert note.index('Lemma 12, proved') < note.index('**Proposition 13') < note.index('**Corollary 14')
body = note.split('### 11.1 Revision after review round 1')[0]
body += note.split('## 12. Checks actually run')[1]
assert not any(old in body for old in ('Lemma 14', 'Proposition 12', 'Corollary 13'))
print('PASS result numbering and updated references')
print('ALL ROUND 1 NOTE CHECKS PASS')
