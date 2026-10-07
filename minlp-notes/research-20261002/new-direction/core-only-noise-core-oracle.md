# Core-coordinate Cauchy output from certified retained hulls

Date: 2026-10-02. Status: passed
[fresh actual-file review](../reviews/core-only-noise-core-oracle-review.md).
This is an output extension of the reviewed
[all-scale value theorem](all-scale-core-value-oracle.md), not a new
count estimate. It uses the same convex recourse oracle and allows
arbitrary residual optimizer fibers. No publication-priority claim is made.

## 1. Statement and one fixed selected core

Use the all-scale theorem's input: a fixed-degree explicit rational
polynomial `F_0(v,z)` on `[0,1]^k x [0,1]^m`, with `k>=1`, verified
convexity in `z` for every core `v`, and verified rational upper bounds
`F_{v_i v_i}<=L`, where `L>=0`. The rational noise half-width
`sigma>0`, structural certificates, and their encoded lengths belong to
the base input `I`. The stated bound requires polynomial certificate
verification; otherwise add the actual verifier cost separately.

Let `F_gamma=F_0+gamma'v`, with independent endpoint-inclusive uniform
finite-grid core noise. There is one base-computable grid size `M`, with
`log M=poly_d(I)`, chosen before all accuracy queries, for which the
following holds.

**Theorem.** Fix the lexicographically first global optimizer, ordering
the core coordinates before the residual coordinates, and call its core
`a_gamma`. For every draw and every integer `q>=0`, an evaluator returns
a feasible rational pair `(v_q,z_q)` and rational bounds `ell_q,U_q`
such that

```
ell_q <= min F_gamma <= U_q = F_gamma(v_q,z_q),
U_q-ell_q <= 2^(-q),
||v_q-a_gamma||_2 <= 2^(-q).                              (1)
```

Its expected bit work and expected proof/output size are at most

```
f_d(k) (1+L/sigma)^k poly_d(I+q),                         (2)
```

with a polynomial exponent independent of `k,m`. One random work factor
of that expected size controls every query precision simultaneously.
No resampling, residual strong convexity, supplied growth constant, or
residual-coordinate distance guarantee is used. The Cauchy descriptor
is the sampled rational objective and this fixed evaluator. Expanded
algebraic coordinates need not have polynomial output length.

The fixed selector has a precise bit interface. Sections 2--5 of the
[generic polynomial fallback](polynomial-exact-fallback.md) construct
one lexicographic optimizer by scalar singleton formulas with two
quantified blocks. Reordering the variables to put the core first does
not change their dimensions or encoding bounds. It gives a base-only
budget `B_0=2^(poly_d(I))` and point/value refinement in
`B_0 poly_d(I+b+q)` bit work, where `b` is sampled coefficient length.
The selected point is independent of `q`. This uses that generic
fallback, not an arbitrary-root selector from a different specialized
algorithm. In fact any fixed exact selector with the same bit interface
would suffice, since the ordinary certificate contains all optimal cores.

## 2. Two containment invariants

Use the predecessor's dyadic cells, approximate corner evaluations, and
two-pass filtering with the final level incumbent. A cell `C` has a
globally valid conditional lower bound `LB(C)`. Retain it when
`LB(C)<=U`, where `U` is the best objective of a feasible point obtained
so far. All ties are retained.

Every optimal core survives. Initially the cells cover the core box.
Whenever a retained cell containing an optimal core is subdivided, its
children still cover that core. Every such child has
`LB<=min F_gamma<=U`, so at least one remains. The same argument applies
to each optimal core, not just a preferred optimizer.

The current incumbent's core also survives. When inserted, the incumbent
is the feasible completion of a queried corner of a generated cell.
Any generated cell containing its core has

```
LB(C) <= min_z F_gamma(v_inc,z)
      <= F_gamma(v_inc,z_inc) = U.                       (3)
```

If an old incumbent remains best, a child of a cell containing its core
still contains that core, and (3) applies again. An improved incumbent
has just been inserted at a current corner. Thus the second filtering
pass preserves a containing cell in either case. Previously removed
cells had a lower bound strictly greater than their then incumbent,
which was at least the current incumbent; they cannot contain its core.

Let `H_j` be the coordinate hull of all retained cells at a completed
level. It is nonempty and contains every optimal core and the current
incumbent's core. Consequently the rational test

```
sum_i (upper_i(H_j)-lower_i(H_j))^2 <= 2^(-2q)            (4)
```

certifies `||v_inc-a_gamma||_2<=2^(-q)`. Its validity does not rely on
uniqueness, a growth bound, or any probable event. A verifier checks the
inherited cell-coverage and lower-bound record, then (4). It need not
compute the selected exact core.

## 3. A base precision cutoff, with growth used only for cost

Replace the supplied curvature bound by

```
L_+ = L+sigma > 0.                                      (5)
```

This changes neither the objective nor its feasible set. It supplies a
positive bound for the inherited grid proof, including originally
zero-curvature instances. Since `1+L_+/sigma=2+L/sigma`, the change is
absorbed into the parameter factor of (2).

At mesh `h_j=2^(-j)`, write `e_j=k L_+ h_j^2/8`. The reviewed proof gives
`U-min F_gamma<=2e_j`, the certified interval `[U-2e_j,U]`, and for every
retained cell a corner `w` satisfying

```
V_gamma(w)-min V_gamma <= 4e_j.                          (6)
```

Let `g` be the optimal projected point-growth constant, set to zero
when there is more than one optimal core. The
[projected growth tail](core-only-noise-value-oracle.md), whose norm uses
only the `k` core coordinates, supplies a base-computable
`C_g=2^(poly_d(I))` with

```
Pr(g<t) <= k t/sigma + C_g/M,  t>0.                     (7)
```

The proof of (7) has no `k<=2` restriction: that restriction applied
only to the predecessor's truncated count moment. Residual ties do not
force `g=0`. Its two-block good-event formula includes feasible residual
witnesses and compares against every feasible competitor.

Choose the same base budget `B>=max(2,B_0)` used for the count cap, and put

```
g_0 = sigma/(2kB),
D = 4k + k^2 L_+/g_0.                                   (8)
```

On `g>=g_0` the optimal core is unique. Equation (6) puts its witness
corner within `h_j sqrt(kL_+/(2g_0))` in Euclidean distance. Every point
of that cell differs from this corner by at most `h_j` in each coordinate.
It follows that every coordinate width of `H_j` is at most
`2h_j(1+sqrt(kL_+/(2g_0)))`. Hence

```
diam_2(H_j)
 <= 2 sqrt(k) h_j (1+sqrt(kL_+/(2g_0)))
 <= D h_j.                                              (9)
```

The last bound uses `sqrt(k)<=k` and `sqrt(x)<=1+x` for `x>=0`.
The deliberately coarse rational `D` avoids computing any square roots.

For query `q`, take the first level `J` such that

```
2e_J <= 2^(-q),       D 2^(-J) <= 2^(-q).               (10)
```

All quantities in (8) have polynomial base bit length, so
`J=poly_d(I)+O(q)`. Refine to this level subject to the inherited
per-level generated-cell cap. If no cap was hit, compute the actual
hull and test (4). If it passes, return the incumbent and
`[U-2e_J,U]`. These satisfy (1) on every draw. If it fails, invoke the
fixed-selector exact fallback on this same objective.

If `g>=g_0`, (9)--(10) ensure that the hull test passes at every query
precision. Therefore failure at any query implies the single event
`g<g_0`. There is no union over levels or future queries. The algorithm
never assumes that `g>=g_0`: it uses (8) only to choose when to perform
the globally valid hull test or switch to exact fallback.

On the fallback branch, refine the fixed core-first lex optimizer to
coordinate error at most
`min(2^(-q)/(k+1),2^(-q)/(2G))`, with a rational gradient bound
`G>=max(1,sup||grad F_gamma||_1)`, and clip the rational coordinates to
their boxes. Use the latter objective tolerance for every coordinate,
and refine the exact value to width at most `2^(-q)/2`. Clipping preserves
feasibility and cannot increase coordinate error. This yields both the
Euclidean core bound and objective interval in (1), in
`B_0 poly_d(I+b+q)` work. Here `log G=poly_d(I+b)` by elementary monomial
bounds. The ordinary and fallback branches thus approximate the same
fixed core, even though the ordinary residual witnesses may vary with `q`.

## 4. One noise law pays for both exceptional events

Apply the reviewed all-scale count theorem with `L_+`. It supplies an
extended random variable `W>=1`, a base section constant `C_a`, and

```
generated cells at every level <= 16^k W,
Pr(W>s) <= a_k/s + C_a/M,   s>=1,
a_k=(180 k^3)^k (1+L_+/sigma)^k.                        (11)
```

Choose `M` to be the least power of two at least

```
max(2, 2B max(C_a,C_g)).                                (12)
```

Both constants are base-computable and have polynomial logarithms.
Thus this single law still has `log M=poly_d(I)` and works at all query
precisions. Equations (7)--(8) now give

```
Pr(g<g_0) <= 1/B.                                       (13)
```

The inherited cap `16^k B` is checked before generating an oversized
list. A cap at any level implies `W>B`. Ordinary list processing remains
linear, with the `2^k` corner multiplicity absorbed in the parameter
factor. The extra hull computation is one pass through the retained
cells. Adding the terminal depth (10) changes only the polynomial factor.
Consequently one random expression bounding all queries' work and
record length is

```
[f(k) min(B,W) + B_0 1_{W>B or g<g_0}] poly_d(I+q).      (14)
```

The inherited weak-tail integral gives
`E min(B,W)<=1+a_k log B+C_a B/M` and
`B Pr(W>B)<=a_k+C_a B/M`. The additional fallback contribution is
at most `B_0/B<=1` by (13). These estimates prove (2), including expected
proof/output size, with one random work factor for every `q`.

For the reviewed `k<=2` predecessor, replace (11) by its
`512 max(1,L_+/g)^(k/2)` count and truncated moment. The same hull argument
and second fallback event apply, giving the sharper specialized bound
`(1+L/sigma) poly_d(I+q)`. This is a corollary of its existing count proof;
no all-scale conjugacy machinery is needed in those two dimensions.

## 5. What the stronger output does and does not give

The sequence `v_q` is a Cauchy name of one exactly globally optimal
core, and each reported full point is feasible with a certified objective
gap. No claim is made that `z_q` approaches any selected residual optimizer.
The selected exact core may be irrational and is not expanded into a
small polynomial representation. On a rare tied-core draw the ordinary
hulls can remain large, but exact fallback still selects consistently.

This output is stronger than a value interval or a feasible objective
approximation alone. It permits arbitrarily precise core decisions for
one fixed perturbed instance. It remains compatible with the reviewed
[PosSLP point-extraction comparison](posslp-convex-point-extraction.md):
the comparison encodes the difficult coordinate in the unperturbed
residual, whose coordinate accuracy is not promised here. The original
unperturbed objective is not solved by the smoothing statement.

The proof is an output/certificate composition of reviewed count,
growth-tail and fallback interfaces. Its new step is retaining and
checking a hull that contains both every global core and the feasible
incumbent, while paying for failure of that test with a second,
all-precision exceptional event. It makes no separate prior-art claim.

## Verification status

The author reread the actual all-scale count theorem, its fresh review,
and the generic fallback's lexicographic construction and bit bounds.
The fresh independent review passed containment, selector consistency,
terminal diameter, the combined law budget, and precision allocation.
The distinct exact diagnostic
`python3 -B research-20261002/new-direction/check_core_hull_oracle.py`
passed five fixtures and 35 stages, including six stages preserving an
old incumbent, 24 valid hull/value outputs, 116 tests rejecting a hull
as too wide, and 48 exact combined-law budget checks. Tied endpoint
optima, a flat optimal core fiber, and a flat objective were included.
The diagnostic checks the new hull contract, not an implementation of
the exact algebraic fallback. Earlier count and fallback fixtures were
not rerun.
No index edits, project-wide tests, or CI checks were made.
