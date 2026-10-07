# Complete weak separation for a compact polynomial graph

The new separator closes a specific algorithmic gap: exact support in a proposed
direction does not by itself provide complete separation. The implementation now
has a finite fallback that returns either a rational separating inequality or a
certificate that the query is within a specified distance of the convex hull.
An explicitly bounded run can still return `unresolved`.

This is a completeness result, not a claim that exhaustive separation is fast.
The optimization/separation relationship is classical; see Grötschel, Lovász,
and Schrijver, [The ellipsoid method and its consequences in combinatorial
optimization](https://doi.org/10.1007/BF02579273), Combinatorica 1 (1981),
169–197 ([author-hosted text](https://www.zib.de/userpage/groetschel/pubnew/paper/groetschellovaszschrijver1981b.pdf)).
Its oracle-model polynomial-time equivalence has additional representation
assumptions; the elementary finite-net proof below makes no such runtime claim.
The contribution here is
an explicit rational construction, implemented certificates, model binding, and
a finite fallback for the supported graphs. The SCIP integration uses its own
bounded direction search; it does not silently run the exhaustive fallback.

## Domain, norm, and status contract

Let

\[
 P=\{x\in\mathbb R^d:l\le x\le u,\ Ax\le b\},\qquad
 H=\operatorname{conv}\{F(x):x\in P\},
\]

where all data are rational, the box is finite, and each coordinate of
\(F:P\to\mathbb R^m\) is a rational polynomial. Equalities can be represented by
two inequalities; empty, singleton, and lower dimensional domains are allowed.
The exact query is \(q\in\mathbb Q^m\), and \(\epsilon>0\) is rational.
Python floats mean their exact binary values. SymPy floating constants are
converted to their exact stored rational values without first narrowing them to
binary64. Source feature trees must already have polynomial syntax: constants,
declared symbols, addition, multiplication, and nonnegative integer powers.
Strings and expressions whose simplification would hide a function domain are
rejected. Domains erased before the caller supplies an expression cannot be
recovered.

The primary distance is \(\ell_1\), so the corresponding normalized normals
satisfy \(\|c\|_\infty\le1\). The four statuses are:

| Status | Certified assertion |
|---|---|
| `cut` | A rational \(c^T F(x)\ge\beta>c^Tq\) is valid for every \(x\in P\). |
| `within_tolerance` | \(\operatorname{dist}_1(q,H)\le\epsilon\). This is not exact membership. |
| `empty_domain` | Exact vertex enumeration proves \(P=\varnothing\). |
| `unresolved` | A stated enumeration budget stopped the search. No distance or membership assertion is made. |

A point at distance at most \(\epsilon\), but outside the hull, may receive a
valid cut. The contract is a weak separation alternative, not an exact decision
at the distance threshold. If the distance exceeds \(\epsilon\), a completed
run must return a cut.

## Optional one-sided normals for row aggregation

For an index set \(I\), the API parameter `nonnegative=I` restricts
\(c_i\in[0,1]\) for \(i\in I\); the other coordinates remain in \([-1,1]\).
Let

\[
 C_I=\{s:s_i\ge0\ (i\in I),\ s_j=0\ (j\notin I)\}.
\]

The resulting geometric assertion is distance to \(H+C_I\), rather than to
\(H\). This is the upper closure needed when graph coordinates representing
signed upper rows must have nonnegative multipliers. The certificate records
\(I\); replay rejects a changed cone.

For both the full graph and this extension,

\[
 \operatorname{dist}_1(q,H+C_I)
 =\max_{c\in\mathcal C_I}\left[\min_{x\in P}c^TF(x)-c^Tq\right],
\]

where \(\mathcal C_I\) is the restricted normal box and \(C_\varnothing=\{0\}\).
To see this, write the \(\ell_1\) norm as the maximum over the dual unit box
and apply convex minimax to the compact hull and that box. In the cone case,
minimizing over its nonnegative coordinates makes any negative cone-coordinate
normal inadmissible; the remaining normals give the displayed box. Equivalently,
eliminate each cone coordinate explicitly: its contribution to the distance is
\(\max(y_i-q_i,0)\), with the other contributions \(|y_i-q_i|\), and apply
minimax to this compact optimization over \(y\in H\). The set \(H+C_I\) is
closed because \(H\) is compact and \(C_I\) is closed. No boundedness claim is
made for the upper closure itself.

## A finite normal net

Compute rational feature enclosures
\(F_j(P)\subseteq[L_j,U_j]\), using interval evaluation of polynomial monomials
over the original box. Define

\[
 R=\sum_{j=1}^{m}\max(|L_j-q_j|,|U_j-q_j|),\qquad
 g(c)=\min_{x\in P}c^T(F(x)-q).
\]

For every pair of normals,

\[
 |g(c)-g(c')|\le R\|c-c'\|_\infty.
\]

Indeed, the corresponding linear functions differ by at most this quantity at
every feasible point, and taking minima preserves the bound. If \(R=0\), any
feasible vertex directly certifies \(F(x)=q\).

Suppose a support computation returns a valid lower bound \(a(c)\) and an
attained upper value \(u(c)=c^TF(x_c)\) with

\[
 a(c)\le\min_{x\in P}c^TF(x)\le u(c),\qquad u(c)-a(c)\le\delta<\epsilon.
\]

Choose

\[
 N=\max\!\left(1,\left\lceil\frac{2R}{\epsilon-\delta}\right\rceil\right).
\]

In a free coordinate, enumerate \(-1+2k/N\), \(k=0,\ldots,N\); in a
nonnegative coordinate, enumerate \(k/N\). Every admissible normal has a grid
point at infinity-norm distance at most \(2/N\). This is a conservative covering
bound; nearest-grid rounding would give a smaller constant.

At a grid point, if \(a(c)>c^Tq\), return the valid cut. Otherwise

\[
 g(c)\le u(c)-c^Tq\le\delta.
\]

If every grid point has been processed without a cut, the Lipschitz bound gives

\[
 \max_{c\in\mathcal C_I}g(c)\le\delta+2R/N\le\epsilon.
\]

This proves the approximate-membership alternative. Its certificate needs only
one exact feasible point \(x_c\) per grid normal whose value satisfies
\(c^T(F(x_c)-q)\le\delta\), together with the covering bound. Replay reconstructs
the complete ordered grid and checks each point. It does not trust the numerical
proposal LP, claimed oracle lower bounds, or a list of unverified direction
labels. Missing positions or points that fail their own assigned direction are
rejected. Reusing a feasible point at several directions is valid when it meets
each inequality.

## Exact quadratic support

When all graph features have total degree at most two, every scalarization is
a quadratic. The exact polytope oracle in `quadratic_polytope.py` returns its
attained minimum and a replayable face-enumeration certificate. Thus
\(\delta=0\), and the algorithm uses that exact value both as lower bound and
upper value. This includes overlapping quadratic blocks on a general bounded
rational polytope; it is not restricted to pairs or stars. Enumeration may be
exponential. The separate integration wrapper imposes its own small-block and
face-count caps.

## A finite support bracket for general polynomials

Let the exact vertices of a nonempty \(P\) be \(v_1,\ldots,v_k\). For a positive
integer \(M\), define the feasible domain net

\[
 V_M=\left\{\sum_{i=1}^{k}(n_i/M)v_i:n_i\in\mathbb Z_{\ge0},\ 
                   \sum_i n_i=M\right\}.
\]

Write \(D=\max_{i,j}\|v_i-v_j\|_\infty\). Every \(x\in P\) has a convex
combination representation. Round its first \(k-1\) weights down to multiples
of \(1/M\), and put the remaining mass on the last vertex. The resulting
\(\hat x\in V_M\) satisfies

\[
 \|x-\hat x\|_\infty\le (k-1)D/M.
\]

Every sample is exactly feasible, including on thin equality domains. No
tolerance-based box-grid feasibility filter is used.

Interval-evaluate each polynomial derivative over the box and set

\[
 L=\sum_{j=1}^{m}\sum_{r=1}^{d}
       \sup_{x\in[l,u]}|\partial_rF_j(x)|,
\]

where the implementation uses rational upper bounds for these suprema. Along
the segment from \(x\) to \(\hat x\), the mean-value inequality gives

\[
 \|F(x)-F(\hat x)\|_1\le L\|x-\hat x\|_\infty.
\]

Choose

\[
 M=\max\!\left(1,\left\lceil\frac{2L(k-1)D}{\epsilon}\right\rceil\right),
 \qquad\delta=L(k-1)D/M\le\epsilon/2.
\]

For any admissible normal, let
\(u(c)=\min_{v\in V_M}c^TF(v)\). Then

\[
 u(c)-\delta\le\min_{x\in P}c^TF(x)\le u(c).
\]

The right inequality uses a feasible minimizing sample; the left follows by
approximating an actual minimizer in \(P\). This supplies the support bracket
required by the normal-net proof. A cut certificate records the domain-net
denominator and error; replay enumerates the exact net and recomputes its
minimum. These shared exact arithmetic routines form the trusted implementation
base. Replay is independent of numerical direction proposals, not a separate
formal proof system.

## Implementation and rounding

`solver/separation.py` exposes:

```python
separate_graph(features, symbols, box, query, *, rows=(), epsilon=...,
               complete=False, max_directions=256, max_samples=20000,
               proposal_rounds=8, initial_points=(),
               use_quadratic_oracle=True, nonnegative=())

replay_separation(result, features, symbols, box, query, *, rows=(),
                  epsilon=..., nonnegative=())
```

The initial feasible samples are vertices and their centroid, with optional
exactly checked caller points. A numerical LP can propose a convex combination
or a direction. Its weights are made nonnegative and normalized with exact
rational arithmetic, and the actual resulting distance is checked. Such a
convex combination can certify the distance directly. A proposed direction is
independently passed through the support routine; unsuccessful bounded exchanges
do not establish membership. Clipping the relevant components makes proposed
normals respect the one-sided restriction. The finite fallback is separate from
these shortcuts, so its completeness does not depend on the LP's accuracy or
success.

The authoritative cut has rational coefficients. For optional binary64 export,
let \(\bar c\) be the actual rounded coefficients. Shift the right side by

\[
 \sum_j\min\{(\bar c_j-c_j)L_j,(\bar c_j-c_j)U_j\}
\]

and round the result downward. This preserves validity for the actual exported
row. The export also reports whether it still separates the exact query.
Subnormal underflow may erase a tiny separation; overflow may make export
unavailable. Neither changes the valid rational certificate. The complete
theorem does not promise that every rational separation is expressible as a
strictly violated binary64 row.

## Termination, complexity, and practical limits

Exact bounded-polytope vertex enumeration is finite. The polynomial domain net
has at most \(\binom{M+k-1}{k-1}\) points; duplicate points are removed. The
normal net has \((N+1)^m\) points. At every point its support computation is a
finite exact quadratic face enumeration or a finite scan of polynomial samples.
Consequently `complete=True` terminates in exact arithmetic with sufficient
resources. This is not a polynomial-time claim, a practical runtime guarantee,
or a general efficient convex-hull representation. The all-vertex barycentric
net deliberately uses the simplest proof and implementation; its large vertex
dependence is explicit.

Normal coordinates and Cartesian products are generated lazily; a small
bounded request does not first allocate its entire theoretical net. Both normal
and barycentric enumeration are iterative, so their dimension is not limited
by Python's recursion depth. A zero-radius graph has a direct certificate.

With `complete=False`, the support-call count and polynomial-net sample count
are capped. These are cardinality budgets, not wall-clock or total-operation
budgets: vertex enumeration and an individual exact quadratic support call can
still be expensive. The deployed integration uses a separate capped support
wrapper. `unresolved` cannot be replayed as a geometric certificate.

Finite exact support plus the implemented fallback closes the completeness gap
for this stated class. Efficient separation for much larger blocks, arbitrary
nonpolynomial graphs, and numerical certificates for a whole SCIP solve are
outside this contract.

## Targeted evidence

`solver/test_separation.py` checks complete fallback beyond three support calls,
polynomial-net exhaustion, an analytic quartic support bracket, exact equality
domains, convex-combination certificates, one-sided closures, explicit budget
failure, source-domain refusals, precision and overflow boundaries, certificate
mutations, and lazy behavior at an extremely small tolerance. Independent tests
and review are recorded separately in `reviews/separation-review.md`.

Command:

```sh
code/minlp_solver_lab/.venv/bin/python -m pytest -q \
  research-20261003-convexification/solver/test_separation.py
```

Result: **16 passed**, 1.68 seconds. No project-wide or CI checks were run.
