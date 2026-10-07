"""Operators and OSiL power nodes per instance (read-only; own copy of the decimal-preserving
reader osilx). For power nodes: (base kind, exponent kind) counts."""
import os
import sys
from collections import Counter
from fractions import Fraction

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import osilx_ro as osilx  # noqa: E402

P = os.path.expanduser('~/.cache/minlplib/minlplib/osil/')


def walk(t, ops, pw):
    if t is None or t[0] in ('num', 'var'):
        return
    ops[t[0]] += 1
    if t[0] == 'power':
        b, e = t[1], t[2]
        ek = ('int' if Fraction(e[1]).denominator == 1 else 'frac') if e[0] == 'num' else 'expr'
        bk = 'const' if b[0] == 'num' else b[0]
        pw[(bk, ek)] += 1
    for c in t[1:]:
        walk(c, ops, pw)


for name in sys.argv[1:]:
    I = osilx.read(P + name + '.osil')
    ops, pw = Counter(), Counter()
    for c in I['cons'] + [I['obj']]:
        walk(c['nl'], ops, pw)
    cons_attr = [c['constant'] for c in I['cons'] if c['constant'] != '0']
    print(f"{name:28s} ops={dict(ops)} power(base,exp)={dict(pw)} obj_constant={I['obj']['constant']} row_constants={len(cons_attr)}")
