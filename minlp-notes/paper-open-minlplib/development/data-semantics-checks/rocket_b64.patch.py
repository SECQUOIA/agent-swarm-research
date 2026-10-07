"""Turn copies of the first bound-audit verifier's reader (osil.py) and of the dossier's
rocket_kraw.py into their binary64-data versions (reading (c)): every decimal string is
replaced by the exact value of its binary64 rounding; the literal 0.6 in rocket_kraw.py's
structure asserts becomes float(0.6). Run inside the /tmp copy."""
src = open('osil.py').read()
old = "from fractions import Fraction as F\n"
assert src.count(old) == 1
new = old.replace("Fraction as F", "Fraction as _Fr") + '''

def F(x=0, d=None):
    """data-semantics audit: decimal strings -> their binary64 values (reading (c))"""
    if isinstance(x, str):
        return _Fr(float(x))
    return _Fr(x) if d is None else _Fr(x, d)
'''
open('osil.py', 'w').write(src.replace(old, new))
s = open('rocket_kraw.py').read()
n = s.count("F('0.6')")
assert n == 5
open('rocket_kraw.py', 'w').write(s.replace("F('0.6')", "F(float('0.6'))"))
print("patched osil.py and rocket_kraw.py (5 literals)")
