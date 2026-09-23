"""Independent exact checks of the extended-RPD support compiler.

Uses a separate value-only implementation with ordinary lower/upper channels,
not the compiler's Affine/MC arithmetic. Rational comparisons include empty
endpoint objects. Run with the isolated research project environment.
"""

from dataclasses import dataclass
from fractions import Fraction as Q
import hashlib
import json
from pathlib import Path
import random

from extended_rpd import PolynomialModel, dimerization, penalty_dual, shift_methanation


@dataclass
class Value:
    lo: Q
    hi: Q
    c: Q
    C: Q

    def cut(self):
        return Value(self.lo, self.hi, max(self.lo, self.c), min(self.hi, self.C))

    @staticmethod
    def scalar(x):
        x = Q(x)
        return Value(x, x, x, x)

    def __add__(self, other):
        if not isinstance(other, Value):
            other = self.scalar(other)
        a, b = self.cut(), other.cut()
        return Value(a.lo+b.lo, a.hi+b.hi, a.c+b.c, a.C+b.C)

    __radd__ = __add__

    def __neg__(self):
        a = self.cut()
        return Value(-a.hi, -a.lo, -a.C, -a.c)

    def __sub__(self, other):
        return self + (-other)

    def __rsub__(self, other):
        return -self + other

    def __mul__(self, other):
        if not isinstance(other, Value):
            other = self.scalar(other)
        a, b = self.cut(), other.cut()
        low = lambda d, x: d*(x.c if d >= 0 else x.C)
        high = lambda d, x: d*(x.C if d >= 0 else x.c)
        products = [u*v for u in (a.lo, a.hi) for v in (b.lo, b.hi)]
        return Value(min(products), max(products),
                     max(low(b.lo,a)+low(a.lo,b)-a.lo*b.lo,
                         low(b.hi,a)+low(a.hi,b)-a.hi*b.hi),
                     min(high(b.lo,a)+high(a.hi,b)-a.hi*b.lo,
                         high(b.hi,a)+high(a.lo,b)-a.lo*b.hi))

    __rmul__ = __mul__


def value_field(model, p, v, *, row_sweeps=0, self_exclude=True, bundles=None):
    """Exact values of all max/min expressions, with no affine propagation."""
    n = len(model.state_box)
    parameters = [Value(lo,hi,t,t) for (lo,hi),t in zip(model.parameter_box,p)]
    result = []
    for output in range(2*n):
        own = output % n
        c, C = list(v[:n]), [-a for a in v[n:]]
        if output < n:
            C[own] = c[own]
        else:
            c[own] = C[own]
        if row_sweeps:
            for j,(lo,hi) in enumerate(model.state_box):
                if not (self_exclude and j == own):
                    c[j], C[j] = max(lo,c[j]), min(hi,C[j])
            for _ in range(row_sweeps):
                for a,b,d in zip(model.invariant_A,model.invariant_b,model.invariant_D):
                    for j,divisor in enumerate(a):
                        if not divisor or (self_exclude and j == own):
                            continue
                        low = high = (b+sum(x*y for x,y in zip(d,p)))/divisor
                        for k,ak in enumerate(a):
                            if k == j:
                                continue
                            coef = -ak/divisor
                            low += coef*(c[k] if coef >= 0 else C[k])
                            high += coef*(C[k] if coef >= 0 else c[k])
                        c[j], C[j] = max(c[j],low), min(C[j],high)
        if bundles is not None:
            old_c, old_C = list(c), list(C)
            for j in range(n):
                if self_exclude and j == own:
                    continue
                for sign in (1,-1):
                    for alpha,beta,q in bundles.get((j,sign),()):
                        value = sum(x*y for x,y in zip(alpha,old_c))
                        value -= sum(x*y for x,y in zip(beta,old_C))
                        value -= sum(qi*(b+sum(x*y for x,y in zip(d,p)))
                                     for qi,b,d in zip(q,model.invariant_b,model.invariant_D))
                        for k,(lo,hi) in enumerate(model.state_box):
                            coef = Q(sign*(k == j))-alpha[k]+beta[k]
                            coef += sum(qi*a[k] for qi,a in zip(q,model.invariant_A))
                            value += min(lo*coef,hi*coef)
                        if sign == 1:
                            c[j] = max(c[j],value)
                        else:
                            C[j] = min(C[j],-value)
        states = [Value(lo,hi,a,b) for (lo,hi),a,b in zip(model.state_box,c,C)]
        rhs = model.rhs(parameters,states)[own]
        if not isinstance(rhs,Value):
            rhs = Value.scalar(rhs)
        result.append(rhs.c if output < n else -rhs.C)
    return result


def exact_evaluate(row, point):
    return sum(a*x for a,x in zip(row[:-1],point))+row[-1]


def run():
    rng = random.Random(409731)
    random_q = lambda: Q(rng.randrange(-16,17),rng.choice((1,2,3,5)))
    mixed = PolynomialModel(((-1,2),),((-2,1),(-1,3)),
        lambda p,x: [x[0]*x[1]-p[0]*x[0]*x[0]+2*x[1]-1,
                     p[0]-x[1]*x[1]*x[1]],
        ((0,0),(0,0)), ((1,2),), (1,), ((1,),))
    models = [dimerization(),shift_methanation(),mixed]
    report = {"seed":409731,"support_inequalities":0,"contact_checks":0,
              "metzler_rows":0,"bundle_tuples":0,"regressions":0,
              "field_dominance_checks":0,"physical_boundary_checks":0}
    for model in models:
        m,n = len(model.parameter_box),len(model.state_box)
        reference = [random_q() for _ in range(m+2*n)]
        bundles = {}
        for j in range(n):
            for sign in (1,-1):
                dual = penalty_dual(model,j,sign,reference[:m],reference[m:],rho=Q(2))
                alpha,beta,q = dual
                assert all(Q(0)<=a<=2 for a in (*alpha,*beta))
                assert all(-2<=a<=2 for a in q)
                bundles[j,sign] = (dual,)
                report["bundle_tuples"] += 1
        for sweeps in (0,1,2):
            for excluded in (False,True):
                for bundle in (None,bundles):
                    options = dict(row_sweeps=sweeps,self_exclude=excluded,bundles=bundle)
                    for _ in range(5):
                        ref = [random_q() for _ in range(m+2*n)]
                        rows = model.supports(ref[:m],ref[m:],**options)
                        at_ref = value_field(model,ref[:m],ref[m:],**options)
                        # Non-dyadic references can round onto another max branch.
                        # Such a choice must remain a lower support, not contact.
                        for j,row in enumerate(rows):
                            assert all(isinstance(a,Q) for a in row)
                            assert all(a>=0 for k,a in enumerate(row[m:-1]) if k!=j)
                            assert exact_evaluate(row,ref)<=at_ref[j]
                            report["metzler_rows"] += 1
                        for _ in range(8):
                            point = [random_q() for _ in range(m+2*n)]
                            values = value_field(model,point[:m],point[m:],**options)
                            if bundle is not None:
                                old = value_field(model,point[:m],point[m:],
                                    row_sweeps=sweeps,self_exclude=excluded)
                                assert all(a>=b for a,b in zip(values,old))
                                report["field_dominance_checks"] += len(values)
                            for row,value in zip(rows,values):
                                assert exact_evaluate(row,point)<=value
                                report["support_inequalities"] += 1
                    # Integer references make arithmetic choices exact in these
                    # small cases; verify the intended active-piece evaluation.
                    zero = [Q(0)]*(m+2*n)
                    rows = model.supports(zero[:m],zero[m:],**options)
                    values = value_field(model,zero[:m],zero[m:],**options)
                    for row,value in zip(rows,values):
                        assert exact_evaluate(row,zero)==value
                        report["contact_checks"] += 1

    # These exact evaluations supplement the analytic conservation/positivity
    # proof; the mixed-sign artificial model above has no physical tube claim.
    for model in models[:2]:
        for _ in range(20):
            p = [lo+(hi-lo)*Q(rng.randrange(21),20) for lo,hi in model.parameter_box]
            x = [lo+(hi-lo)*Q(rng.randrange(21),20) for lo,hi in model.state_box]
            rhs = model.rhs(p,x)
            assert all(sum(a*f for a,f in zip(row,rhs))==0 for row in model.invariant_A)
            for j in range(len(x)):
                boundary = list(x)
                boundary[j] = 0
                assert model.rhs(p,boundary)[j]>=0
                report["physical_boundary_checks"] += 1

    # Integer metadata once produced an invalid rational bound through /.
    model = PolynomialModel((),((0,1),(0,1)),lambda p,x:[x[1],0],
        ((0,),(Q(1,3),)),((0,3),),(1,),((),))
    rows = model.supports([], [0,0,0,-1],row_sweeps=1)
    physical = [Q(0),Q(1,3),Q(0),Q(-1,3)]
    assert exact_evaluate(rows[2],physical)==Q(-1,3)
    assert exact_evaluate(rows[1],physical)==0
    report["regressions"] += 2
    source = Path(__file__).with_name("extended_rpd.py")
    report["source_sha256"] = hashlib.sha256(source.read_bytes()).hexdigest()
    report["status"] = "passed"
    return report


if __name__ == "__main__":
    print(json.dumps(run(),indent=2))
