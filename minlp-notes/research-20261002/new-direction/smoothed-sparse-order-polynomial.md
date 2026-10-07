# Expected exact sparse polynomial optimization on an order polytope

Date: 2026-10-02. Status: complete theorem that passed
[independent completed-text review](order-polytope-independent-review.md).
All variables in this note are continuous. Publication priority and
practical performance are not established.

The sparse polynomial box argument extends to order inequalities when
its curvature parameter is replaced by a full Hessian upper bound.
Common-threshold rounding preserves feasibility, bag order chambers
control conditional value functions, and linear optimization over the
order polytope certifies the active face. The last step avoids assuming
that small coordinate gradients identify active order inequalities.

## 1. Statement

Let

```
P = {x in [0,1]^n : x_i <= x_j for each of m specified edges i -> j},
F_0 = sum_B f_B,
Hess F_0(x) <= H I on [0,1]^n,      H>=1.
```

The factors are explicit rational polynomials of fixed degree at most
`d>=1`. A supplied tree decomposition covers every factor scope and every
order edge, with largest bag size `p`. Directed cycles are permitted.
Evaluate a zero-variable input directly; below assume `n>=1`.
Let `I` include these data, rational `H`, and a rational noise half-width
`sigma>0`. Supply a valid curvature bound; a polynomial-time-verifiable
certificate, or the usual rational monomial bound, is needed if the
bound itself is to form part of an independently checkable proof record.
Include that certificate's length and verification cost in `I`.

There is a base-computable power of two `M`, with
`log M=poly_d(I)`, such that independent uniform coefficients on

```
{-sigma+2sigma k/(M-1) : k=0,...,M-1}
```

admit an algorithm solving `min_P F_gamma`, where
`F_gamma=F_0+gamma'x`, exactly on every draw. Its expected bit work is
at most

```
C_0^p p! (p+1) [2+nH(p+1)/(2sigma)]^p poly_d(I).             (1)
```

Here `C_0` is absolute. For fixed bag size this is polynomial when the
numerical ratio `H/sigma` is polynomially bounded. It is not an FPT bound
in `p`, and it does not preserve the box theorem's dependence on only
coordinatewise diagonal curvature.

The usual output is a polynomial-size rational description of an order
polytope patch on which the restricted objective has a certified positive
Hessian modulus. Its unique constrained minimizer denotes an exact
global optimizer. It supports feasible rational point approximations and
certified objective enclosures in `poly_d(I+q)` bit work for `q` requested
accuracy bits. The rare branch returns an exact real-algebraic optimizer
and value. Its possibly exponential work, output size, and evaluation
cost have polynomial expectations under the same finite law. As in the
[box theorem](smoothed-sparse-polynomial.md), the global pruning proof
record can exceed polynomial size on a particular successful draw; its
expected size and verification work obey (1).

The theorem concerns the sampled objective. Exact recovery of an
unperturbed optimizer is not asserted.

## 2. Feasible rounding and the sparse dynamic program

Use the dyadic coordinate cells of width `h_j=2^(-j)`, nested bag-cell
whitelists, deduplicated corner rows, and separator-key dynamic program
of the box theorem. Assign each order inequality to a containing bag as
a local feasibility constraint. Binarize the decomposition without
increasing its bag size. Start with the single coordinate interval
`[0,1]`; hence the initial lists have size bounded by an absolute
constant to the power `p` per bag.

For a feasible point `x`, draw one common `U` uniformly on `[0,1]` and set

```
Y_i = h_j (floor(x_i/h_j) + 1{U < frac(x_i/h_j)}).
```

For each fixed `U` this is a nondecreasing scalar rounding map. It
therefore preserves every order inequality, including equalities forced
by cycles. It fixes grid nodes and stays in every incident coordinate
cell containing `x`. In particular, it preserves every bag whitelist and
any one specified candidate bag cell.

The rounding is mean preserving, although coordinates are correlated.
Taylor's upper bound from the full Hessian assumption gives

```
E F_gamma(Y) <= F_gamma(x)+E_j,      E_j=nHh_j^2/8.            (2)
```

Indeed `E(Y-x)=0` and `E||Y-x||^2<=nh_j^2/4`. This is why the full
Hessian bound replaces the independent-rounding diagonal bound.

The dynamic program minimizes over exactly the globally consistent
allowed grid assignments satisfying all assigned order inequalities.
Let `m_j` be this minimum, `U_j` the best feasible value seen, and
`m_B(v)` the exact bag-row min-marginal. For a candidate bag cell `C` put

```
q_C=min_{v a corner of C} m_B(v),     LB_C=q_C-E_j,            (3)
```

with absent or infeasible rows assigned value `+infinity`. Retain `C`
when `LB_C<=U_j`. Fixed-cell feasible rounding proves the lower bound
on the current allowed physical domain. Inductively all original global
optimizers survive, and

```
f* <= U_j <= m_j <= f*+E_j.
```

Each retained cell has one globally feasible witness corner `y` with

```
F_gamma(y)=q_C <= f*+2E_j.                                  (4)
```

This is the same witness needed by the count below. It is not merely
local feasibility or coordinatewise local optimality. The common random
threshold is only a proof device; no such rounding randomness is used
by the algorithm or conditioned on in the noise analysis.

## 3. Expected bag counts

Condition on all noise outside a bag `B`, whose size is `b<=p`, and put

```
V_B(v)=min_{z:(v,z) in P} [F_0(v,z)+gamma_out'z].
```

The [order-polytope counting lemma](order-polytope-cell-count.md) proves
the needed facts on the original feasible fibers. Their changes are
controlled by at most `b!` closed bag order simplices. On each such
simplex, the fiber is the convex hull of a fixed finite family of affine
maps copying outside coordinates from `0,1,v_1,...,v_b`. Every convex
combination of these maps has squared operator norm at most `n`.
Consequently `V_B` is `nH`-semiconcave on each chamber, independently of
the outside noise and without enumerating the affine maps.

The lemma counts all original feasible bag grid tuples satisfying

```
V_B(v)+gamma_B'v <= f*+eta h_j^2.
```

For `M h_j>=1`, their expected number is at most

```
b! (b+1) [2+(bnH+2eta)/(2sigma)]^b.                         (5)
```

Its proof includes lower-dimensional faces and equal-coordinate tuples.
Within each simplex face, feasible comparison directions have disjoint
coordinate supports. Conditioning on all but one noise coordinate from
each support gives independent scalar interval tests. Thus the chamber
argument preserves the independence needed for the probability product.

Equation (4) permits `eta=nH/4`. Enlarging (5) uniformly over `b<=p`
gives the bracket in (1). A corner belongs to at most `2^p` cells, and
every retained cell has at most `2^p` children and `2^p` corners.
Therefore the expected generated row and cell work per level is bounded
by the right side of (1), times a polynomial factor. This analysis counts
deterministic full-grid tuples; the algorithm generates only sparse
lists. It never conditions the noise law on preceding pruning events.

## 4. A sound active-face certificate

The [face-closure lemma](order-polytope-face-closure.md) supplies the
certificate and its probability bound. Here is the mechanism used by
the algorithm.

Intersect the coordinate projection hulls of all retained incident bags
to obtain a rational box `Q_j` containing every original optimizer. Let
`c` be its midpoint and `r` its largest half-width. Compute rational
monomial bounds

```
M_1 >= max{1,max_i sum_k sup |partial_ik F_0|},
T   >= max{1,max_i sum_kl sup |partial_ikl F_0|}.             (6)
```

Set `g=grad F_gamma(c)` and `delta=M_1 r`. Every optimizer `a` in this
hull satisfies `||grad F_gamma(a)-g||_infinity<=delta`.

Compute `q=min_P g'x`. For each order edge `i->j`, also compute

```
q_e=min{g'x : x in P, x_i=0, x_j=1}.                        (7)
```

An empty restricted face gives `q_e=+infinity`. If
`q_e-q>n delta`, certify `x_i=x_j` at every original optimizer.
For a lower bound `x_i=0`, use the restricted face `x_i=1`; for an upper
bound `x_i=1`, use `x_i=0`. These are rational linear programs of
polynomial encoding length.

For soundness, at any global optimizer `a`, its true gradient exposes a
face of `P` containing `a`. The order polytope and each exposed face have
zero-one vertices. If the proposed equality is not active at `a`, some
vertex of this exposed face belongs to the restricted face in (7).
Its `g`-cost exceeds `q` by at most `n delta`, contradicting the test.
Thus this certificate does not rely on a sampled margin promise.

Substitute every certified bound and identify coordinates connected by
certified equality edges. The remaining coordinates are block values
`y`, with `x=D y+b`; each row of `D` is zero or a coordinate unit vector.
Intersect their coordinate intervals from `Q_j`. Keep all remaining order
inequalities. Propagate lower and upper bounds along these inequalities,
remove singleton coordinates, and contract directed cycles. These exact
operations preserve the patch; they also handle additional equalities
forced by its rational bounds.
Drop tautological self-order rows and constant identities after each
substitution, including before the interior-slack LP used for evaluation.

Let `C` be the resulting coordinate box, with midpoint `c_C` and largest
half-width `r_C`. Check by exact rational linear algebra that

```
Hess_y F_gamma(D c_C+b) - (nT r_C+g_0) I is positive definite. (8)
```

Since `||D||^2<=n`, (6) bounds the restricted Hessian variation by
`nT r_C` throughout `C`. Hence (8) certifies Hessian at least `g_0 I`
on the whole box. The retained order-polytope patch inside `C` contains
every original global optimizer. Its unique constrained minimizer is
therefore an exact global optimizer. With no variables remaining, verify
and return the fixed rational point. No strict slack of an inactive order
inequality is required by this certificate.

## 5. Why closure occurs at polynomial precision

Write `g_*` for the global point-growth modulus, set to zero on nonunique
draws. The [finite-noise growth proof](polynomial-finite-noise-tails.md)
applies after replacing its mixed-box membership formula by

```
0<=x_i<=1,       x_i<=x_j for each specified edge.
```

There are still two quantified blocks, one free noise scalar, fixed
degree, and polynomially many atoms. Its block-sensitive elimination
bound gives a base-computable `C_tail=2^{poly_d(I)}` and, for every
`epsilon>0` under the same finite law,

```
Pr{g_*<epsilon} <= n epsilon/sigma+2n C_tail/M.              (9)
```

This also follows directly from the compact-domain continuous growth
tail plus the uniform scalar-section count. Adding the order inequalities
does not add a quantifier block.

For an optimizer `a` and an active constraint, define its linear exposure
gap using the true gradient in (7), with the analogous opposite-bound
face for a bound constraint. The face-closure lemma gives, with

```
D_0=max(1,d-1),
K=max{1,(m+2n) 2^(m+2n) D_0^n},
```

the unconditional bound

```
Pr{g_*>0 and some active finite exposure gap <=tau}
   <= K(tau/sigma+2/M).                                    (10)
```

The proof counts at most `2^(m+2n)` minimal faces and `D_0^n`
nonsingular stationary roots on each face. Positive point growth makes
the relevant restricted Hessian positive definite. For an active order
edge, vary its two noise coefficients while fixing their sum. The face
stationary equations do not change. On the opposite zero-one face in
(7), the linear exposure gap for a fixed root changes with slope one in
absolute value. Counting directly on the at most `2M-1` sum fibers gives
`tau/sigma+2/M`; no lower bound on a conditional fiber's probability is
assumed. Active bound constraints need only a single noise coordinate.
Infinite gaps are harmless and are omitted from the event.

Suppose `g_*>=g_0` and every active finite gap exceeds `tau`. Put

```
A=2+nH/g_0.
```

By (4), witnesses have distance at most
`h_j sqrt(nH/g_0)/2` from the unique optimizer. Hence each retained
coordinate hull lies within `A h_j` of it, and `r<=A h_j`. If

```
h_j <= min{1/A, tau/(4nM_1 A), g_0/(4nT A)},                (11)
```

then (7) certifies every active order equality and bound: its computed
gap is at least the true gap minus `n delta`, which exceeds `n delta`.
The resulting affine space is contained in the affine hull of the
optimizer's minimal face. Two-sided Taylor expansion of point growth
on that face gives restricted Hessian at least `2g_0 I`. The Hessian
variation estimate then makes (8) positive definite. Closure therefore
succeeds by (11), without a lower bound on inactive primal slacks.

## 6. One finite law and the same-draw fallback

The [canonical exact fallback](polynomial-exact-fallback.md) extends to
`P` by the same replacement of its domain membership formula. Its
lexicographically selected optimizer and each scalar output still have
two-block singleton formulas. Thus a base-computable budget
`B=2^{poly_d(I)}`, enlarged also to cover evaluation work, bounds the
fallback by

```
B (I+b+q+1)^c_d,       b=log_2 M,                           (12)
```

for a fixed exponent `c_d`. Additional sampled coefficient and requested
accuracy bits enter only the polynomial factor. Ties and positive-
dimensional minimizer sets are permitted.

Choose before drawing the coefficients

```
rho=1/(4B),       g_0=rho sigma/(2n),       tau=rho sigma/(2K).
```

Let `J` be the least nonnegative integer satisfying (11) with
`h_J=2^(-J)`. Take the least power of two

```
M >= max{2,2^J,4n C_tail/rho,4K/rho}.                       (13)
```

All these quantities have polynomial binary length. There is no precision
circle: `B,C_tail,K,g_0,tau,J` are fixed from the base instance before
choosing `M`. Equations (9) and (10) each contribute at most `rho` to
the bad probability. If closure has not succeeded by level `J`, run
(12) on that same sampled objective. Its probability is at most
`2rho=1/(2B)`, so its expected work and output cost are polynomial.
There is no resampling.

For feasible rational fallback approximants, refine the canonical point
to coordinate error `epsilon`, clip to `[0,1]`, and replace coordinate
`i` by the maximum of the clipped values over all predecessors of `i`,
including itself. This is feasible and stays within `epsilon` in the
infinity norm of the exact feasible point. A rational gradient bound and
the separate exact value enclosure give the certified objective gap.
Thus the stronger approximation contract also has cost (12).
For Euclidean point error `2^(-q)`, refine coordinates to error at most
`2^(-q)/n` before repair; this adds only `O(log n)` precision bits.

## 7. Patch evaluation and total work

The usual descriptor contains its substitutions, rational coordinate
box, remaining order inequalities, objective, modulus, and matrix test.
The unique minimizer of this explicitly described convex patch denotes
the exact output. Its KKT system is an equivalent exact description.

The [convex-patch evaluation argument](convex-patch-evaluation.md)
extends from a box to this rational order-polytope patch. After bound
propagation, singleton elimination, and cycle contraction, a nontrivial
patch has relative dimension equal to its remaining number of variables.
A rational linear program finds an interior point and a positive common
slack for its inequalities. Half that slack is a valid Euclidean ball
radius since every remaining row has norm at most two. The point and
radius have polynomial encoding length. An equivalent general procedure
first computes the rational affine hull by linear programming.

The capped epigraph has the same rational value/gradient separator as
in the evaluation note, together with order and bound separators. Its
inner and outer ball bounds have polynomial encoding length. The cited
bit-model weak-optimization theorem therefore applies unchanged.

For its near-feasible rational output, first propagate the box bounds:
replace each lower bound by the largest predecessor lower bound and each
upper bound by the smallest successor upper bound. Clip coordinates to
these intervals and take predecessor maxima. This gives an exactly
feasible rational point. Relative to any feasible point, the repair does
not increase infinity-norm error. A bound on the gradient's one-norm
therefore gives the same objective-gap repair as in the box argument.
Strong convexity then converts an objective gap
`min{2^(-q),(g_0/(2n))2^(-2q)}` into the required point accuracy
in the original coordinates. The factor `n` accounts for copying a block
value into up to `n` original coordinates.

All grid coordinates, polynomial evaluations, dynamic-programming sums,
LP data, hulls, gradient enclosures, and matrices have polynomial bit
length for `j<=J`. There are polynomially many levels, bags, and LP calls
per level. Summing (5), including the absolute per-bag branching factors,
and adding the expected fallback proves (1).

## 8. Scope and verification

This is a continuous order-polytope extension. It does not cover arbitrary
TU or affine constraints, mixed integer order systems, or a bound using
only diagonal curvature. The [affine-feasibility barrier](constrained-smoothing-barrier.md)
therefore does not apply to its stated input class. The full Hessian
parameter may be numerically large even when its binary encoding is
short.

Independent checks established the common-threshold fixed-cell rounding
and sparse witness argument. The counting theorem has a separate
completed-text review. The [fresh composition review](order-polytope-independent-review.md)
passed the actual count, face-closure, and composition proofs after the
recorded clarifications. A separate root review independently checked
the substantive interfaces. These mathematical reviews do not establish
publication priority. No full numerical solver, external literature
search, project-wide verification, or CI inspection was used in this
composition.

A targeted inline `python3 - <<'PY'` command checked local links, paired
code fences, and trailing whitespace in this note and the face-closure
note. The same command used exact fractions to check 151 common-threshold
roundings and nine LP-gap/Hessian closures for
`F_0(x_1,x_2)=4x_1 x_2-4x_1+1` on `0<=x_1<=x_2<=1`, with small linear
noise. This objective has an indefinite ambient Hessian and a positive
Hessian on its active diagonal face. All checks passed. These finite
checks do not implement the full expected-work algorithm, sampling
budget, algebraic fallback, or convex evaluator.

The independent reviewer separately ran

```
python3 -B research-20261002/new-direction/check_order_polytope_review.py
```

That [checker](check_order_polytope_review.py) passed 297 finite-noise
draws on chain, fork, and cyclic order systems, including 969 sound forced
equalities, 494 active-gap checks, 213 zero-gap incidences, 6,831
gap-Lipschitz checks, 275 fixed-face/proposal probability comparisons,
and 1,754 rounding atoms. The [results](order-polytope-review-check-results.json)
are separate from the author's inline checks. They support the new
interfaces and do not establish asymptotic expectation experimentally.
