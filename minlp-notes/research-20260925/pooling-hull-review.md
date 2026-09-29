# Independent review: a common-denominator graph hull

Date: 2026-09-25. This record gives a complete proof, an explicit rational
second-order-cone formulation, two consequences, and the limits found during
adversarial review. It does not claim a substantial new theorem: the central
edge reduction is classical in linear-plus-linear-fractional optimization.

## Assessment

The proposed convex-hull statement is correct under its stated assumptions.
The zero-throughput part must be included explicitly. Degenerate polytopes,
constant-throughput edges, and edges incident to zero cause no obstruction.
The proposed rational algebraic-degree and fixed-resource-row consequences
are also correct. Neither gives a novelty claim without comparison with
classical fractional programming and basic-feasible-solution arguments.

The restriction on linear side constraints matters. The polytope is in the
unnormalized variables, while restrictions on the ratio variables alone are
homogenized into that polytope. Arbitrary linear constraints coupling both
groups are outside the theorem. A rational example below has a unique
degree-three feasible point after two such coupling rows are added.

## Model and assumptions

Let \(P\subseteq\mathbb R^{1+n+r}\) and \(Q\subseteq\mathbb R^n\) be nonempty
compact polytopes. Write \(p=(x,w,v)\), and assume that every \(p\in P\)
satisfies

\[
x\geq0,\qquad w\in xQ.
\tag{1}
\]

Define

\[
S=\{(p,q):p\in P,\ q\in Q,\ w=xq\}.
\tag{2}
\]

For \(x>0\), necessarily \(q=w/x\). For \(x=0\), condition (1) implies
\(w=0\), and every \(q\in Q\) is allowed. Thus (2) is exactly the union of the
positive-throughput graph and the prescribed zero-throughput set. In the
pooling interpretation, \(Q\) lies in a simplex and
\(w\geq0,\sum_iw_i=x\). Those additional assumptions are not needed for the
proof; compactness of \(Q\) and condition (1) suffice.

If \(Q=\{q:Cq\leq d,Dq=e\}\), condition \(w\in xQ\) can be imposed by
\(Cw\leq dx,Dw=ex,x\geq0\). At \(x=0\), these constraints force \(w=0\),
because a nonempty bounded polytope has no nonzero recession direction.
Thus restricting the original polytope by (1) is a linear operation. These
homogenized rows must be included when counting the resource rows below.

The set \(S\) is compact: it is a closed subset of the compact set \(P\times Q\).
In particular, its convex hull is compact. This argument avoids any need to
identify limits of positive-throughput points at zero.

## Slice vertices lie on vertices or edges

For \(t>0\), let \(P_t=P\cap\{x=t\}\). Every vertex of a nonempty \(P_t\) lies
on a vertex or an edge of \(P\).

To prove this, let \(z\) be such a vertex, and let \(F\) be the unique minimal
face of \(P\) containing \(z\), so \(z\in\operatorname{relint}F\). If
\(x\) is constant on \(F\) and \(\dim F\geq1\), a sufficiently short nonzero
segment through \(z\) in \(\operatorname{aff}F\) lies in \(F\cap P_t\), a
contradiction. If \(x\) is not constant on \(F\) and \(\dim F\geq2\), the
linear space parallel to \(\operatorname{aff}F\) has a nonzero direction
annihilated by the \(x\)-coordinate. A sufficiently short segment in that
direction again contradicts extremality in \(P_t\). Therefore
\(\dim F\leq1\).

Every \(p\in P_t\) is a convex combination of vertices \(p_j\) of \(P_t\).
Because the denominator \(t\) is common,

\[
\left(p,\frac wt\right)
=\sum_j\theta_j\left(p_j,\frac{w_j}t\right).
\tag{3}
\]

This proves the edge reduction for the entire vector graph, including the
retained variables \(v\). It is stronger than merely saying that a scalar
fractional objective has a vertex optimum, which would be false for the sum
of a linear and a fractional term.

## Each necessary edge graph has a small SOC hull

Consider an edge \(e\) of \(P\), with its endpoint throughputs ordered as
\(0\leq\ell_e\leq u_e\).

If \(\ell_e=u_e>0\), the graph map on this edge is affine; its graph is the
segment joining the two endpoint graph points. If both throughputs are zero,
the edge is already covered by the zero-throughput set.

Suppose \(\ell_e<u_e\). There are unique vectors \(a_e,b_e\) such that

\[
p_e(t)=a_e t+b_e,\qquad t\in[\ell_e,u_e].
\]

Write \(\alpha_e,\beta_e\) for the \(w\)-coordinates of \(a_e,b_e\). Then,
for \(t>0\),

\[
q_e(t)=\alpha_e+\frac{\beta_e}{t}.
\tag{4}
\]

If \(\ell_e=0\), condition (1) gives \(\beta_e=0\). The positive graph on
this edge has constant \(q_e=\alpha_e\). Since \(\alpha_e\in Q\), its closure
is a segment between an admissible zero-throughput point and the positive
endpoint graph point. Thus no SOC is needed for this edge. Notice that this
only supplies one possible \(q\) at the zero endpoint; it does not supply the
whole zero-throughput set.

It remains to consider \(0<\ell_e<u_e\). For \(0<\ell<u\),

\[
\operatorname{conv}\{(t,1/t):\ell\leq t\leq u\}
=\left\{(t,s):\ell\leq t\leq u,\quad
ts\geq1,\quad
s\leq\frac{\ell+u-t}{\ell u}\right\}.
\tag{5}
\]

Here \(s\geq0\) follows from \(t>0\) and \(ts\geq1\). Convexity of \(1/t\)
gives the lower bound and the endpoint chord gives the upper bound. For the
reverse inclusion, the point on the chord at a fixed \(t\) is a convex
combination of the two graph endpoints; the point \((t,1/t)\) is itself on the
graph; their vertical segment gives all values between the bounds. The chord
gap identity is

\[
\frac{\ell+u-t}{\ell u}-\frac1t
=\frac{(t-\ell)(u-t)}{\ell u t}.
\]

The edge graph hull is the affine image of (5) under

\[
(t,s)\longmapsto(a_e t+b_e,\ \alpha_e+\beta_e s).
\tag{6}
\]

If \(\beta_e=0\), this image is a segment and the cone can also be omitted.

Let \(V_+\) denote the positive-throughput vertices of \(P\), let
\(E_{++}\) denote its edges with \(0<\ell_e<u_e\), and define

\[
Z=\{((0,0,v),q):(0,0,v)\in P,\ q\in Q\}.
\]

Equations (3)--(6), including the affine edge cases, prove

\[
\operatorname{conv}S
=\operatorname{conv}\left(
 Z\ \cup\ \{(p^j,w^j/x^j):j\in V_+\}
 \ \cup\ \bigcup_{e\in E_{++}} H_e\right),
\tag{7}
\]

where \(H_e\) is the edge hull in (6). Every generator on the right belongs
to \(\operatorname{conv}S\), and every original point is covered by the
slice argument. This also handles a zero-dimensional polytope, an empty
zero face, and an identically zero throughput.

## An explicit formulation, including zero disjunct weights

Give each \(j\in V_+\), each \(e\in E_{++}\), and the nonempty set \(Z\) a
nonnegative weight \(\lambda_j,\lambda_e,\lambda_0\), respectively. Require
their sum to be one. Omit the zero component if \(Z\) is empty.

For each \(e\in E_{++}\), introduce \(t_e,s_e\) and impose

\[
\ell_e\lambda_e\leq t_e\leq u_e\lambda_e,
\qquad
\left\|(2\lambda_e,t_e-s_e)\right\|_2\leq t_e+s_e,
\qquad
\ell_eu_e s_e\leq(\ell_e+u_e)\lambda_e-t_e.
\tag{8}
\]

The norm inequality is exactly
\(t_e,s_e\geq0,\ t_es_e\geq\lambda_e^2\).
For \(\lambda_e>0\), division by the weight recovers (5). For
\(\lambda_e=0\), the throughput bounds force \(t_e=0\), and the cone and
chord bounds force \(s_e=0\). Consequently (8) introduces no extra points
through a zero-weight recession direction.

Suppose \(P=\{p:Ap\leq b,Ep=f\}\). For the zero component introduce
\(p^0=(0,0,v^0)\) and \(q^0\), with

\[
Ap^0\leq b\lambda_0,\quad Ep^0=f\lambda_0,
\qquad
Cq^0\leq d\lambda_0,\quad Dq^0=e\lambda_0.
\tag{9}
\]

At \(\lambda_0=0\), boundedness and nonemptiness of \(P,Q\) force
\(p^0=q^0=0\). At positive weight, (9) describes a scaled point of \(Z\).
The aggregate equalities are

\[
p=p^0+\sum_{j\in V_+}\lambda_jp^j
     +\sum_{e\in E_{++}}(a_et_e+b_e\lambda_e),
\]

\[
q=q^0+\sum_{j\in V_+}\lambda_j\frac{w^j}{x^j}
     +\sum_{e\in E_{++}}(\alpha_e\lambda_e+\beta_es_e).
\tag{10}
\]

Equations (8)--(10) and the weight simplex project exactly to (7).
There is at most one three-dimensional Lorentz cone per edge of \(P\).
All coefficients are rational when \(P,Q\) are rational: vertices, edge
slopes, edge intercepts, and positive endpoint reciprocals are rational, and
the norm representation uses no irrational constants.

This is a finite-size existence statement. A rational inequality
description can have exponentially many edges. The construction therefore
does not provide a polynomial-size formulation for arbitrary \(P\).

## Rational data admit an optimizer of degree at most two

Let the objective be rational and linear in \((p,q)\). There is an optimum
of \(S\), and hence an optimum of its convex hull, whose coordinates all lie
in a single extension of \(\mathbb Q\) of degree at most two.

By (7), at least one generating component attains the optimum. The zero
component is a product of rational polytopes, so it has a rational optimal
vertex. Positive vertex and affine edge components have rational optimal
endpoints. On a remaining edge the objective has the form

\[
F(t)=A+Bt+C/t,\qquad t\in[\ell,u],\quad0<\ell<u,
\tag{11}
\]

with rational \(A,B,C,\ell,u\). If an endpoint is optimal it is rational.
An interior strict minimum can only occur when \(B,C>0\), in which case

\[
t=\sqrt{C/B}.
\tag{12}
\]

The remaining flat case has a rational endpoint optimum. Formulas (4) and
(12) put all coordinates in the same quadratic field. The statement is
existential: some other optimizers can be arbitrary convex combinations and
need not have this degree bound.

The bound is attained. Take

\[
P=\{(x,w):1\leq x\leq2,\ w=(1,x-1)\},\qquad Q=\Delta_2.
\]

Minimizing \(x+2q_1=x+2/x\) gives the unique throughput
\(x=\sqrt2\) and value \(2\sqrt2\).

This consequence and its square-root calculation are closely reflected in
the classical source discussed below; they should not be advertised as an
independent new phenomenon.

## Polynomial size with a fixed number of non-coordinate rows

Consider a nonempty bounded polytope

\[
F=\{z\in\mathbb R^N:z\geq0,\ Mz\leq h\},
\tag{13}
\]

where \(M\) has \(m\) rows. Suppose \(x,w,v\) are affine functions of \(z\)
and satisfy (1) throughout \(F\). One can retain \(z\) as part of \(v\),
apply the preceding proof on \(F\), and then take the desired affine image.

Every edge of \(F\) has at most \(m+1\) nonzero coordinates on its relative
interior; every vertex has at most \(m\). For an edge, let \(J\) be its
positive-coordinate support at a relative interior point, and let \(I\) be
the indices of tight non-coordinate rows there. All other inequalities are
strict locally. The dimension of this minimal face is therefore

\[
1=|J|-\operatorname{rank}M_{I,J},
\]

which implies \(|J|\leq m+1\). The vertex proof uses dimension zero.

For any fixed pair \((I,J)\), the constraints

\[
z_{J^c}=0,\qquad M_{I,J}z_J=h_I
\tag{14}
\]

intersected with \(F\) define one face. If
\(|J|-\operatorname{rank}M_{I,J}=1\), that face lies in an affine line, so it
contains at most one edge. Hence the number of edges is at most

\[
2^m\sum_{s=1}^{\min(N,m+1)}\binom Ns,
\tag{15}
\]

and a valid vertex bound is

\[
2^m\sum_{s=0}^{\min(N,m)}\binom Ns.
\tag{16}
\]

Enumerating these pairs, solving their rational affine systems, and
intersecting the resulting line with the inequalities recovers all edges;
duplicates can be removed. Inconsistent, empty, and zero-length candidates
are harmless. Rank-deficient row sets are handled by the displayed rank
condition; no nondegeneracy assumption is needed.

For fixed \(m\), (15)--(16) and the preceding conic construction give a
polynomial-size rational SOC formulation. They also give a polynomial-time
exact optimization procedure for rational linear objectives: inspect
rational endpoints and the admissible square-root stationary point of each
edge, then compare real algebraic numbers of degree at most two. This is
polynomial for each fixed \(m\); it is not a claim of fixed-parameter
tractability with an exponent independent of \(m\).

All inequalities other than the coordinate nonnegativity bounds count
toward \(m\). This includes individual upper capacities, positive lower
bounds, throughput lower bounds, and homogenized quality/specification
rows. A bound expressed using a fixed number of quality rows alone does
not follow when there are arbitrarily many individual capacities.
The support bound is sharp: for \(m=1\), the simplex
\(\{z\geq0:\sum_jz_j\leq1\}\) has edges with two positive coordinates.
When \(m=N\), the cube \([0,1]^N\) has \(N2^{N-1}\) edges, demonstrating why
the unrestricted construction can grow exponentially.

The support and counting arguments are standard consequences of polyhedral
face dimension. Their combination with this explicit hull may be useful,
but substantial originality has not been established.

There is a further application limitation for the usual normalization in
which \(w\) is a linear function of \(z\). If (13) consists only of
\(z\geq0\), homogeneous quality rows \(Az\leq0\), and a cap
\(x=\sum_jz_j\leq U\), every nonzero vertex has \(x=U\): any point with
\(0<x<U\) can be scaled slightly up and down within the polytope. An edge
then either has constant positive throughput or joins zero to throughput
\(U\). Both cases have affine ratio graphs, so the hull construction is
polyhedral. If a total-throughput lower bound is added, the same conclusion
follows by expressing each positive point as \(z=xr\), where \(r\) belongs
to the fixed normalized base: decompose \(r\) into base vertices, then
interpolate \(x\) between its bounds. Thus a fixed number of homogeneous
quality rows plus throughput bounds alone does not demonstrate a need for
the SOC result. Nonhomogeneous restrictions that change available
compositions with throughput are needed for its curved cases.

## Counterexamples and limits

### The full zero face is not the positive graph's closure

Let \(P=\{(x,w):0\leq x\leq1,w=(x,0)\}\) and \(Q=\Delta_2\).
Every positive-throughput point has \(q=(1,0)\), including its limit as
\(x\downarrow0\). But \(S\) also contains the zero-throughput point with
\(q=(0,1)\). Omitting \(Z\) loses a feasible point and its convex
combinations. Compactness of the completed set does not imply that its
zero face is approached from positive throughput.

### Extra ratio bounds must enter before convexification

Use the quadratic example above and add \(q_1=3/4\). The original graph now
has \(x=4/3\). Intersecting its previously computed hull with \(q_1=3/4\)
also admits \(x=3/2\), since at that point

\[
1/x=2/3\leq3/4=\frac{3-x}{2}.
\]

The theorem remains exact after adding the bound to \(Q\) and homogenizing
it into \(P\), which forces \(w_1=(3/4)x\). Merely intersecting the old hull
with the new row need not be exact.

### Mixed linear side constraints can produce degree three

Let \(q\in\Delta_3\), impose \(w=xq\), and use the rational constraints

\[
\frac25\leq x\leq\frac12,\qquad w_2=\frac1{10},\qquad
q_1+x=1,\qquad w_1=q_2.
\tag{17}
\]

The unnormalized variables also satisfy \(w\geq0\) and
\(\sum_iw_i=x\), defining a compact rational polytope before the two mixed
rows in (17) are imposed. The full system implies

\[
q=(1-x,x(1-x),x^2),\qquad
w=(x(1-x),1/10,x^3),
\]

and

\[
10x^3-10x^2+1=0.
\tag{18}
\]

The polynomial is strictly decreasing on \([2/5,1/2]\), takes values
\(1/25\) and \(-1/4\) at the endpoints, and therefore has one root there.
It is irreducible over \(\mathbb Q\): modulo three it is
\(x^3+2x^2+1\), which has no root in \(\mathbb F_3\). The unique feasible
point thus has degree three. This refutes extension of the degree-two
claim to arbitrary linear side constraints in \((p,q)\). It does not by
itself refute SOC representability of their hull.

### Pooling scope and objective scope

The theorem permits arbitrary linear objectives in the retained ratios and
unnormalized variables. It does not make minimization of an arbitrary
convex nonlinear objective over the original nonconvex set equivalent to
minimization over its hull. It also does not directly handle several
independent denominators, or simultaneous products of one composition
vector with several independent output flows. Such products are central
to general pooling models. A complete model reduction is required before
claiming that this hull solves a particular pooling class.

## Literature comparison and significance

An independent literature agent examined the following primary sources and
reported the indicated results. This reviewer independently checked the
mathematical reduction and its consequences above. The book URL returned
HTTP 403 to this reviewer's web fetch, so the precise page inspection of
that source is the literature agent's verification, not a second successful
fetch by this reviewer.

1. Cambini and Martein, *Generalized Convexity and Optimization* (2009),
   Theorem 8.3.1(i), printed p.175, proves an edge optimum for the sum of a
   linear and a linear-fractional function over a polyhedron when an optimum
   is attained and the denominator is positive. Its proof fixes the
   denominator, obtains a linear-programming slice vertex, and locates that
   vertex on an original edge. A linear objective in the full vector graph
   combines the ratio coefficients into one numerator, so this theorem
   applies to every such objective. Support-function equality then gives
   the simultaneous graph reduction. Page 179 displays a square-root
   stationary parameter, and pages 179 and 181 contain quadratic-radical
   optimizers. The algorithm sections impose additional conditions; they
   should not be conflated with the unconditional edge statement.
   [Open book](https://www.convexoptimization.com/TOOLS/GeneralizedConvexity.pdf).
2. Santana and Dey, *The convex hull of a quadratic constraint over a
   polytope*, Theorem 1, proves SOC representability for one quadratic
   equality over any bounded polyhedron. This covers the scalar ratio
   equation with arbitrary linear side constraints. The present vector
   statement uses several equations with a shared denominator, but its
   edge-arc conic construction is adjacent to their finite-disjunction
   method. [Open paper](https://arxiv.org/pdf/1812.10160).
3. He, Liu, and Tawarmalani, *Convexification techniques for fractional
   programs*, Theorems 1--2 and Section 6, develop exact projective
   convexification correspondences and discuss retaining original
   variables alongside ratios through moment hulls. The inspected
   statements do not directly assert this arbitrary-polytope finite SOC
   graph hull. Their strict positive-denominator hypotheses also do not
   directly cover the completed zero face here.
   [Open paper](https://arxiv.org/pdf/2310.08424).
4. Dey, Kocuk, and Santana, *A study of rank-one sets with linear side
   constraints and application to the pooling problem*, Theorem 2,
   addresses a bounded nonnegative rank-one set with two arbitrary linear
   inequalities. Two inequalities must not be confused with a two-row
   matrix with arbitrarily many inequalities. Theorem 3 allows a special
   common rank-two coefficient structure. Neither inspected statement
   directly subsumes arbitrary \(P\) here.
   [Author manuscript](https://www2.isye.gatech.edu/~sdey30/RankonePool.pdf).
5. Jalilian and Kocuk, *Improved Rank-One-Based Relaxations and Bound
   Tightening Techniques for the Pooling Problem*, Theorem 1 in the arXiv
   version and Theorem 2 in the published version, gives a generally
   exponential SOC hull for nonnegative rank-one matrices with simultaneous
   row-sum, column-sum, and total-sum bounds. Its decomposition is an
   important precedent for the formulation-size caveat.
   [Open preprint](https://arxiv.org/pdf/2306.10810),
   [published author copy](https://research.sabanciuniv.edu/52174/1/Improved.pdf).

The book points to Martein (1985), Cambini--Martein--Schaible (1989), and
Konno--Kuno (1990) as earlier relevant work. Those original articles were
not examined in this review; no stronger statement is attributed to them.
The repository's [common-factor literature audit](../notes/common-factor-literature-audit.md)
was also consulted and identifies related simultaneous-convexification
work by Tawarmalani and a 2026 common-variable bilinear abstract. Those
comparisons do not establish novelty of the current formulation.

No exact published statement of the full formulation (8)--(10) was found
in the targeted search. That is not evidence sufficient to establish
novelty. The defensible status is a mathematically checked, explicit SOC
consequence of a classical edge theorem, with careful treatment of zero
throughput and useful restricted-size consequences. It is a resource for
further work, not a sufficient main contribution for the user's goal of a
substantial theoretical advance.

Potential practical value would come from a model class whose edge set has
additional usable structure, a compact separation procedure that avoids
edge enumeration, or a demonstrably strong solver block. None of those
capabilities follows for general pooling from finite SOC representability
alone. The fixed-\(m\) consequence supplies one such structural regime, but
its originality and application relevance need separate validation.

## Verification record

Only targeted checks were run; no project-wide verification or CI inspection
was performed. The core argument was checked by direct proof, including
minimal-face degeneracy and all zero-weight cases. No Lean formalization
was attempted: the important uncertainty here is significance and prior
art, rather than a long symbolic proof.

The formatting check command

~~~bash
git diff --no-index --check /dev/null research-20260925/pooling-hull-review.md
~~~

produced no whitespace diagnostics. Its exit status was one because the
new file differs from the empty file.

A `python - <<'PY' ... PY` command using `fractions.Fraction` and SymPy
completed successfully. It checked:

- irreducibility modulo three and the exact endpoint signs of (18);
- the mass-balance identity for the cubic counterexample;
- the exact objective and stationary derivative at \(x=\sqrt2\);
- the symbolic reciprocal-chord gap identity;
- 36 exact rational scaled points against the bounds, product inequality,
  and norm-square inequality in (8), for three positive intervals and three
  weights.

The command reported:

```text
PASS: cubic boundary example, quadratic optimizer, reciprocal chord identity, 36 perspective points
```

The exact substantive check command was:

~~~bash
python - <<'PY'
from fractions import Fraction as F
import sympy as sp
x=sp.symbols('x')
f=10*x**3-10*x**2+1
assert sp.Poly(f,x, modulus=3).is_irreducible
assert f.subs(x,sp.Rational(2,5)) == sp.Rational(1,25)
assert f.subs(x,sp.Rational(1,2)) == -sp.Rational(1,4)
assert sp.simplify(x*(1-x)+sp.Rational(1,10)+x**3-x) == f/10
r=sp.sqrt(2)
assert sp.simplify(r+2/r-2*sp.sqrt(2)) == 0
assert sp.simplify(sp.diff(x+2/x,x).subs(x,r)) == 0
# Reciprocal chord gap: U(t)-1/t = (t-l)(u-t)/(l*u*t).
l,u,t=sp.symbols('l u t', positive=True)
assert sp.factor((l+u-t)/(l*u)-1/t-(t-l)*(u-t)/(l*u*t)) == 0
# Exact rational points inside each perspective reciprocal hull.
for lo,hi in [(F(1),F(2)),(F(1,3),F(7,3)),(F(2),F(5))]:
  for weight in [F(1,7),F(1,2),F(1)]:
    for frac in [F(0),F(1,3),F(1,2),F(1)]:
      xx=lo+(hi-lo)*frac
      sec=(lo+hi-xx)/(lo*hi)
      zz=(1/xx+sec)/2
      tt=weight*xx; ss=weight*zz
      assert lo*weight<=tt<=hi*weight
      assert tt*ss>=weight*weight
      assert lo*hi*ss <= (lo+hi)*weight-tt
      assert (2*weight)**2+(tt-ss)**2 <= (tt+ss)**2
print('PASS: cubic boundary example, quadratic optimizer, reciprocal chord identity, 36 perspective points')
PY
~~~

These computations check the displayed examples and algebra. They do not
prove the general hull theorem, the edge count, the literature comparisons,
or practical solver benefit. Those conclusions rest on the arguments and
source comparisons stated above.
