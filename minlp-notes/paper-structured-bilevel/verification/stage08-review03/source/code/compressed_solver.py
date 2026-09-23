"""Exact scalar-tariff bilevel solver with a concave quadratic aggregate.

Paper copy of code/bilevel_nonconvex/scalar_solver.py.
Changes: rational sign fast path and rational-endpoint interior sampling.
All inputs are rational; arithmetic and branch comparisons are exact (SymPy).
See notes/bilevel-nonconvex-scalar-algorithm.md for model and limitations.
"""
from dataclasses import dataclass
from functools import cmp_to_key
import sympy as sp

X = sp.Symbol('x', real=True)


def rat(x):
    if isinstance(x, str):
        return sp.Rational(x)
    value = sp.sympify(x)
    if value.is_Rational is not True:
        raise TypeError('Use exact rational numbers or rational strings')
    return sp.Rational(value)


def sign(x):
    x = sp.sympify(x)
    if x.is_Rational:
        return 1 if x > 0 else -1 if x < 0 else 0
    x = sp.cancel(x)
    if x == 0:
        return 0
    if x.is_positive is True:
        return 1
    if x.is_negative is True:
        return -1
    # Relational comparison of explicit real algebraic numbers is exact.
    if bool(x > 0):
        return 1
    if bool(x < 0):
        return -1
    if x.equals(0):
        return 0
    raise ArithmeticError(f'Undecided algebraic sign: {x}')


def ordered(values):
    out = []
    for v in sorted(values, key=cmp_to_key(lambda a, b: sign(a-b))):
        if not out or sign(v-out[-1]):
            out.append(v)
    return out


def rational_between(a, b):
    """Exact rational point strictly between distinct real algebraic bounds."""
    if sign(a-b) == 0:
        return a
    a, b = sp.sympify(a), sp.sympify(b)
    if a.is_Rational and b.is_Rational:
        return (a + b)/2
    denominator = 1
    while True:
        point = (sp.floor(a*denominator)+1)/sp.Integer(denominator)
        if sign(point-b) < 0:
            return point
        denominator *= 2


def clip(v, lo, hi):
    return lo if sign(v-lo) < 0 else hi if sign(v-hi) > 0 else v


@dataclass(frozen=True)
class Instance:
    d: tuple
    c: tuple
    u: tuple
    lower: tuple
    upper: tuple
    h: object
    gamma: object
    x_lower: object
    x_upper: object

    def __post_init__(self):
        for name in ('d', 'c', 'u', 'lower', 'upper'):
            object.__setattr__(self, name, tuple(rat(v) for v in getattr(self, name)))
        for name in ('h', 'gamma', 'x_lower', 'x_upper'):
            object.__setattr__(self, name, rat(getattr(self, name)))
        n = len(self.d)
        if not n or any(len(getattr(self, k)) != n for k in ('c','u','lower','upper')):
            raise ValueError('Nonempty equal-length vectors required')
        if any(v <= 0 for v in self.d) or any(l > r for l,r in zip(self.lower,self.upper)):
            raise ValueError('Positive d and ordered box bounds required')
        if self.gamma == 0 or self.h < 0 or self.x_lower > self.x_upper:
            raise ValueError('Require gamma != 0, h >= 0 and ordered tariff bounds')


@dataclass(frozen=True)
class FiberPiece:
    left: object
    right: object
    alpha: tuple  # z(w) = alpha + beta*w
    beta: tuple
    A: object     # C(w)-h*w^2/2 = A*w^2+B*w+D
    B: object
    D: object

    def z(self, w):
        return tuple(sp.cancel(a+b*w) for a,b in zip(self.alpha,self.beta))

    def cost(self, x, w, gamma):
        return sp.cancel(self.A*w*w+self.B*w+self.D+gamma*x*w)


@dataclass(frozen=True)
class Branch:
    piece: FiberPiece
    w: object     # affine polynomial in X
    cost: object  # quadratic polynomial in X
    left: object
    right: object


@dataclass(frozen=True)
class Response:
    piece: FiberPiece
    left: object  # entire minimizing w interval; singleton ordinarily
    right: object


@dataclass
class Atlas:
    instance: Instance
    pieces: list
    branches: list
    cells: list   # (open left, open right, winning branch indices)
    points: list  # (tariff, list[Response]), including all boundaries


@dataclass(frozen=True)
class Constraint:
    a: object
    b: tuple
    rhs: object  # a*x + b^T*z <= rhs

    def __post_init__(self):
        object.__setattr__(self, 'a', rat(self.a))
        object.__setattr__(self, 'b', tuple(rat(v) for v in self.b))
        object.__setattr__(self, 'rhs', rat(self.rhs))


@dataclass(frozen=True)
class Optimum:
    value: object
    attained: bool
    x: object = None
    w: object = None
    z: object = None
    limit_x: object = None
    limit_w: object = None


def fiber_pieces(ins):
    """Resource-allocation fiber compression by sorted multiplier events."""
    events = ordered([(di*v+ci)/ui for di,ci,ui,l,r in
                      zip(ins.d,ins.c,ins.u,ins.lower,ins.upper)
                      if ui and l != r for v in (l,r)])
    pieces = []
    for p,q in zip(events,events[1:]):
        lam = (p+q)/2
        az, bz = [], []
        for di,ci,ui,l,r in zip(ins.d,ins.c,ins.u,ins.lower,ins.upper):
            zi = (lam*ui-ci)/di
            if l < zi < r:
                az.append(-ci/di); bz.append(ui/di)
            else:
                az.append(clip(zi,l,r)); bz.append(sp.S.Zero)
        w0 = sum(ui*a for ui,a in zip(ins.u,az))
        slope = sum(ui*b for ui,b in zip(ins.u,bz))
        if slope == 0:
            continue
        left,right = w0+slope*p,w0+slope*q
        alpha = tuple(a-b*w0/slope for a,b in zip(az,bz))
        beta = tuple(b/slope for b in bz)
        A = sum(di*b*b/2 for di,b in zip(ins.d,beta))-ins.h/2
        B = sum((di*a+ci)*b for di,ci,a,b in zip(ins.d,ins.c,alpha,beta))
        D = sum(di*a*a/2+ci*a for di,ci,a in zip(ins.d,ins.c,alpha))
        pieces.append(FiberPiece(left,right,alpha,beta,A,B,D))
    if not pieces:
        z = tuple(clip(-ci/di,l,r) for di,ci,l,r in
                  zip(ins.d,ins.c,ins.lower,ins.upper))
        w = sum(ui*zi for ui,zi in zip(ins.u,z))
        val = sum(di*zi*zi/2+ci*zi for di,ci,zi in zip(ins.d,ins.c,z))-ins.h*w*w/2
        pieces = [FiberPiece(w,w,z,tuple(sp.S.Zero for _ in z),0,0,val)]
    return pieces


def _branches(ins, pieces):
    branches = []
    seen = set()
    for p in pieces:
        for w in (p.left,p.right):
            if w not in seen:
                branches.append(Branch(p,w,p.cost(X,w,ins.gamma),ins.x_lower,ins.x_upper))
                seen.add(w)
        if p.A > 0 and p.left < p.right:
            w = -(p.B+ins.gamma*X)/(2*p.A)
            a,b = sorted(((-2*p.A*p.left-p.B)/ins.gamma,
                          (-2*p.A*p.right-p.B)/ins.gamma))
            a,b = max(a,ins.x_lower),min(b,ins.x_upper)
            if a <= b:
                branches.append(Branch(p,w,p.cost(X,w,ins.gamma),a,b))
    return branches


def _roots(poly):
    poly = sp.Poly(poly,X)
    if poly.is_zero or poly.degree() == 0:
        return []
    if poly.degree() == 1:
        b,c = poly.all_coeffs()
        return [-c/b]
    a,b,c = poly.all_coeffs()
    disc = b*b-4*a*c
    if disc < 0:
        return []
    return [(-b-sp.sqrt(disc))/(2*a),(-b+sp.sqrt(disc))/(2*a)]


def _winners(branches,x):
    winners, best = [], None
    for i,b in enumerate(branches):
        if sign(x-b.left) < 0 or sign(x-b.right) > 0:
            continue
        val = b.cost.subs(X,x) if hasattr(b.cost,'subs') else b.cost
        cmp = -1 if best is None else sign(val-best)
        if cmp < 0:
            best,winners = val,[i]
        elif cmp == 0:
            winners.append(i)
    return winners,best


def _insert_envelope(branches, lower, upper):
    """Incremental lower envelope, retaining every possible isolated contact.

    Branch zero is an endpoint candidate valid on the entire tariff interval.
    A retained contact may later be dominated; final point reconstruction checks
    every branch globally. Crossings above the current envelope are never added.
    """
    cells = [(lower, upper, 0)] if lower < upper else []
    contacts = [lower, upper]
    for i, branch in enumerate(branches[1:], 1):
        contacts.extend((branch.left, branch.right))
        updated = []
        for left, right, old in cells:
            splits = [left, right]
            for edge in (branch.left, branch.right):
                if sign(edge-left)>0 and sign(edge-right)<0:
                    splits.append(edge)
            lo = left if sign(left-branch.left)>=0 else branch.left
            hi = right if sign(right-branch.right)<=0 else branch.right
            if sign(lo-hi)<=0:
                roots = [r for r in _roots(branch.cost-branches[old].cost)
                         if sign(r-lo)>=0 and sign(r-hi)<=0]
                splits.extend(roots)
                contacts.extend(roots)
            splits = ordered(splits)
            for a,b in zip(splits,splits[1:]):
                sample = rational_between(a,b)
                winner = old
                if sign(sample-branch.left)>=0 and sign(sample-branch.right)<=0:
                    if sign((branch.cost-branches[old].cost).subs(X,sample))<0:
                        winner = i
                if updated and updated[-1][2]==winner and sign(updated[-1][1]-a)==0:
                    updated[-1] = (updated[-1][0],b,winner)
                else:
                    updated.append((a,b,winner))
        cells = updated
    return cells, contacts


def build_atlas(ins):
    """Build every globally minimizing response, including isolated flat ties."""
    pieces = fiber_pieces(ins)
    branches = _branches(ins,pieces)
    envelope, cuts = _insert_envelope(branches,ins.x_lower,ins.x_upper)
    for p in pieces:
        if p.A == 0:
            x = -p.B/ins.gamma
            if ins.x_lower <= x <= ins.x_upper:
                cuts.append(x)
    cuts = ordered(cuts)
    cells = []
    position = 0
    for a,b in zip(cuts,cuts[1:]):
        while position+1 < len(envelope) and sign(a-envelope[position][1])>=0:
            position += 1
        cells.append((a,b,[envelope[position][2]]))
    points = []
    for x in cuts:
        win,best = _winners(branches,x)
        responses = []
        seen = []
        for i in win:
            b = branches[i]
            w = b.w.subs(X,x) if hasattr(b.w,'subs') else b.w
            if not any(sign(w-v)==0 for v in seen):
                responses.append(Response(b.piece,w,w)); seen.append(w)
        for p in pieces:
            if p.left < p.right and p.A == 0 and sign(p.B+ins.gamma*x)==0 and sign(p.cost(x,p.left,ins.gamma)-best)==0:
                responses.append(Response(p,p.left,p.right))
        points.append((x,responses))
    return Atlas(ins,pieces,branches,cells,points)


def _restrict(lo,hi,a,b):
    """Intersect a closed interval with a*v+b <= 0."""
    s = sign(a)
    if s == 0:
        return None if sign(b)>0 else (lo,hi)
    edge = -b/a
    if s > 0 and sign(edge-hi)<0:
        hi = edge
    if s < 0 and sign(edge-lo)>0:
        lo = edge
    return None if sign(lo-hi)>0 else (lo,hi)


def optimize_tariff(atlas,constraints=(),semantics='optimistic'):
    """Maximize x*w, with exact optimistic or robust pessimistic semantics.

    Pessimistic: every global follower response must satisfy every upper row,
    and revenue is the minimum x*w over all global follower responses.
    Return None when infeasible. An unattained supremum has only limit fields.
    """
    if semantics not in ('optimistic','pessimistic'):
        raise ValueError('Unknown semantics')
    ins = atlas.instance
    constraints = tuple(constraints)
    if any(len(row.b)!=len(ins.d) for row in constraints):
        raise ValueError('Constraint dimension mismatch')
    best = None

    def record(x,w,piece,value,attained):
        nonlocal best
        value = sp.cancel(value)
        if best is None or sign(value-best.value)>0 or (sign(value-best.value)==0 and attained and not best.attained):
            best = Optimum(value,attained,x if attained else None,w if attained else None,
                           piece.z(w) if attained else None,
                           None if attained else x,None if attained else w)

    for left,right,win in atlas.cells:
        # gamma != 0 implies identical global aggregate responses throughout
        # an open cell, even when duplicate candidates represent that response.
        branch = atlas.branches[win[0]]
        w = branch.w
        z = branch.piece.z(w)
        interval = (left,right)
        for row in constraints:
            expr = sp.Poly(row.a*X+sum(bi*zi for bi,zi in zip(row.b,z))-row.rhs,X)
            interval = _restrict(*interval,expr.nth(1),expr.nth(0))
            if interval is None:
                break
        if interval is None:
            continue
        lo,hi = interval
        if sign(hi-left)<=0 or sign(lo-right)>=0:
            continue
        objective = sp.Poly(X*w,X)
        candidates = [lo,hi,rational_between(lo,hi)]
        if objective.nth(2)<0:
            stationary = -objective.nth(1)/(2*objective.nth(2))
            if sign(stationary-lo)>=0 and sign(stationary-hi)<=0:
                candidates.append(stationary)
        for x in candidates:
            wx = w.subs(X,x) if hasattr(w,'subs') else w
            record(x,wx,branch.piece,x*wx,sign(x-left)>0 and sign(x-right)<0)

    for x,responses in atlas.points:
        if semantics == 'optimistic':
            for response in responses:
                p = response.piece
                interval = (response.left,response.right)
                for row in constraints:
                    a = sum(bi*zi for bi,zi in zip(row.b,p.beta))
                    b = row.a*x+sum(bi*zi for bi,zi in zip(row.b,p.alpha))-row.rhs
                    interval = _restrict(*interval,a,b)
                    if interval is None:
                        break
                if interval is not None:
                    w = interval[1] if sign(x)>=0 else interval[0]
                    record(x,w,p,x*w,True)
        else:
            feasible = True
            worst = None
            for response in responses:
                for w in (response.left,response.right):
                    z = response.piece.z(w)
                    if any(sign(row.a*x+sum(bi*zi for bi,zi in zip(row.b,z))-row.rhs)>0 for row in constraints):
                        feasible = False
                        break
                    val = x*w
                    if worst is None or sign(val-worst[0])<0:
                        worst = (val,w,response.piece)
                if not feasible:
                    break
            if feasible and worst is not None:
                val,w,p = worst
                record(x,w,p,val,True)
    return best


if __name__ == '__main__':
    instance = Instance((1,1),(-1,'-1/2'),(1,1),(0,0),(1,1),'3/5',1,0,1)
    atlas = build_atlas(instance)
    print('fiber pieces:',len(atlas.pieces),'branches:',len(atlas.branches),
          'open cells:',len(atlas.cells),'points:',len(atlas.points))
    constraints = [Constraint(0,(1,1),1)]
    print('optimistic:',optimize_tariff(atlas,constraints))
    print('pessimistic:',optimize_tariff(atlas,constraints,semantics='pessimistic'))
