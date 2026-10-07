# Extension: treat exp/sqrt/log as opaque function symbols whose arguments are compared exactly.
import sys
from fractions import Fraction as F
import exact_forms as X
def key(fn, x):
    num, den = x
    if not (len(den) == 1 and X.ONE in den):
        raise NotImplementedError('non-polynomial function argument')
    c = den[X.ONE]
    num = {m: v / c for m, v in num.items()}
    return '%s[%s]' % (fn, repr(sorted((tuple(m), str(v)) for m, v in num.items())))
_atom = X.Parser.atom
def atom(self):
    kind, val = self.peek()
    if kind == 'id' and val.lower() in ('exp', 'sqrt', 'log') and self.t[self.i + 1][1] == '(':
        self.take(); self.take('(')
        a = self.expr(); self.take(')')
        return X.R_(X.p_var(key(val.lower(), a)))
    return _atom(self)
X.Parser.atom = atom
_tree = X.tree
def tree(e, var):
    tag = e.tag[len(X.NS):]
    if tag in ('exp', 'sqrt', 'ln'):
        a = X.tree(e[0], var)
        return X.R_(X.p_var(key({'ln': 'log'}.get(tag, tag), a)))
    return _tree(e, var)
X.tree = tree
sys.argv = ['drive.py'] + sys.argv[1:]
exec(open('drive.py').read())
