"""Data-semantics survey of the cached OSIL files (read-only).

For each instance: number of distinct numeric strings, how many are not binary64-exact
(Fraction(float(s)) != Fraction(s)), the largest number of significant digits, how many
strings have >= 16 significant digits (shortest-repr prints of binary64 values), and how
many strings fail the repr round trip Fraction(repr(float(s))) == Fraction(s) (relevant
to camshape_bound.py, which encloses iv.mpf(repr(float(s)))).
usage: python3 data_survey.py <instance> ...
"""
import os
import re
import sys
from fractions import Fraction

P = os.path.expanduser('~/.cache/minlplib/minlplib/osil/')


def strings(name):
    t = open(P + name + '.osil').read()
    s = set(re.findall(r'(?:value|coef|lb|ub|constant)="([^"]*)"', t))
    s |= set(re.findall(r'<el[^>]*>([^<]*)</el>', t))
    s |= set(re.findall(r'<coef[^>]*>([^<]*)</coef>', t))
    out = set()
    for x in s:
        x = x.strip()
        if x.upper() in ('INF', '-INF', '+INF'):
            continue
        try:
            Fraction(x)
        except (ValueError, ZeroDivisionError):
            continue
        out.add(x)
    return out


def sig(x):
    m = re.sub(r'[eE].*', '', x).replace('-', '').replace('+', '').replace('.', '').lstrip('0')
    return len(m.rstrip('0')) if m else 0


if __name__ == "__main__":
    print(f"{'instance':28s} {'distinct':>8s} {'non-b64':>8s} {'maxsig':>6s} {'>=16sig':>7s} {'repr-fail':>9s}  non-b64 examples")
    for name in sys.argv[1:]:
        s = strings(name)
        non = sorted((x for x in s if Fraction(float(x)) != Fraction(x)), key=len)
        long_ = [x for x in s if sig(x) >= 16]
        rf = [x for x in s if Fraction(repr(float(x))) != Fraction(x)]
        print(f"{name:28s} {len(s):8d} {len(non):8d} {max(sig(x) for x in s):6d} {len(long_):7d} {len(rf):9d}  {non[:4]}")
