# Independent review of coupled order-polytope optimization

Date: 2026-10-02. Verdict: **passed after the recorded clarifications**.
This review reads the actual
[composition theorem](smoothed-sparse-order-polynomial.md),
[conditional count](order-polytope-cell-count.md), and
[face-closure lemma](order-polytope-face-closure.md).

The coupled mechanism is sound. It substantially exceeds the product-block
extension in its feasible-set scope: order edges can connect the entire
problem, and no disjoint-block factorization or independent outside domain
is assumed. The price is the full ambient Hessian upper bound and the
factorial bag-order chamber count. The statement remains continuous,
fixed-width expected polynomial optimization under the specified finite
noise law. It is not a mixed-integer order theorem or an FPT-width result.

## 1. Feasible rounding and sparse witnesses

For fixed threshold `U`, the scalar dyadic rounding map is nondecreasing.
It preserves every original order inequality and every equality implied
by a directed cycle. It fixes grid coordinates exactly. A coordinate
strictly between grid nodes belongs to one interval at that level; a
coordinate on a shared boundary never moves. Consequently every rounding
outcome stays in every incident candidate bag cell containing the starting
point, and in all preceding whitelist cells. This validates fixed-cell
rounding even though the same threshold correlates coordinates across
many bags.

The full Hessian bound, mean preservation, and the sum of marginal
variances give `E=nHh^2/8`. Independent-coordinate diagonal curvature
would not justify this step. Local feasibility rows must cover every
original order edge, as the supplied decomposition requires. Then a
globally consistent DP assignment is genuinely feasible, and every
retained cell has one full feasible witness of gap at most `2E`.
No inconsistent collection of local witnesses is used in the count.

## 2. Conditional fibers and the chamber count

The projection onto a bag is the order polytope induced by reachability.
The proposed maximum-of-bag-predecessors construction proves sufficiency,
including cyclic equalities. Intersecting an induced order inequality
with a total-order simplex either leaves it unchanged or forces a chain
of equalities. Thus its intersection is a face, and the at most `b!`
closed faces cover the bag projection, including lower-dimensional cases.

At a recourse-fiber vertex, each tight outside equality component must
touch a bag coordinate or a zero/one bound; otherwise it admits a small
two-sided translation. Therefore the proposed copy maps contain every
fiber vertex. Their feasibility is constant on the relative interior of
one bag-order face. The interpolation-and-limit argument correctly extends
the convex-hull representation to its boundary; additional boundary-only
maps need not be enumerated.

For a fixed convex combination of copy maps, each row of its linear part
has nonnegative entries summing to at most one. Its squared Frobenius norm,
and hence squared operator norm, is at most `n`. The full Hessian upper
bound yields upper curvature `nH` for every such pullback. The outside
linear noise remains affine and changes no curvature. Taking the infimum
over the fixed weight simplex preserves semiconcavity on the chamber.
This proves the recourse sensitivity needed here; it is not the invalid
claim that arbitrary parameter-dependent feasible fibers preserve upper
curvature.

On a face with `k+1` nested zero-one vertices, successive differences
have disjoint supports. Grid barycentric weights are positive multiples
of `h`, so both comparison moves stay in the face. Conditioning on all
but one coefficient in each support leaves exactly `k` independent
uniform coefficients. The comparison intervals do not depend on these
remaining coefficients. Multiplying their probabilities by
`binom(1/h-1,k)` proves the stated cancellation of grid density.
Outside copy-map count never enters the algorithm; `b!` explicitly does.

## 3. LP face forcing and the finite-law exposure gap

The forcing rule uses the original order polytope, whose vertices are
zero-one. At a global optimizer, the true gradient minimizes a linear
objective over that polytope. If a proposed equality is violated there,
some vertex in its exposed linear face lies in the corresponding opposite
zero-one face. Comparing that vertex with a minimizer of the midpoint
gradient objective bounds the computed gap by `n delta`. Thus the test
cannot remove an optimizer, without any growth or probability premise.

The gap is `n`-Lipschitz in coefficient infinity norm, rather than merely
the looser `2n` estimate: compare the two relevant zero-one minimizers,
whose difference has one-norm at most `n`. Empty opposite faces mean an
equality already holds throughout the polytope. This handles self edges,
cycles, and redundant order relations without assigning a multiplier to
each redundant row.

For a fixed minimal face, positive point growth makes the tangential
stationary root nonsingular. For an active edge, holding the two noise
coefficients' sum fixed changes only their normal difference. The face
stationary roots therefore stay fixed on that fiber. A violating vertex
always has coordinate pattern `(0,1)`, while a face vertex has equal
coordinates. On values where the root is optimal, its exposure gap has
constant slope of magnitude one, even if the unrestricted linear program
has multiple minimizers. The small-gap event lies in an interval of
length `tau`.

Counting at most `2M-1` sum fibers gives the stated
`D^n(tau/sigma+2/M)` bound. This is tuple counting, not a false uniform
conditional-density assertion on short fibers. Coordinate bounds use a
single noise coefficient. The crude `q 2^q D^n` union factor is used only
inside logarithmic precision budgets; it is not an enumerated family of
algorithmic states. Finite atoms at zero gaps are explicitly covered.

## 4. Closure, degeneracies, and exact evaluation

On the good event, witness proximity bounds the hull radius by `Ah`.
The specified cutoff identifies every active original equality and bound.
Point growth then gives a positive Hessian in every direction of the
minimal face. Extra valid singleton substitutions only restrict those
directions. No numerical lower bound on an inactive order slack is needed.
Keeping all remaining order inequalities is essential to that conclusion.

The composition uses a conservative unweighted block-coordinate test.
Since its copy matrix satisfies `||D||^2<=n`, the `nT` variation term is
necessary and sufficient for the stated argument. The face-closure note's
weighted test is a different, also valid, version. They should not be
combined by dropping one version's metric factors. The composition now
uses objective tolerance `g_0 2^(-2q)/(2n)` when it requests Euclidean
accuracy in the original copied coordinates.

Bound propagation, singleton removal, and cycle contraction retain exactly
the rational patch. Tautological self-order rows must be removed before
maximizing common interior slack. Equivalently, rational LP identifies
the affine hull first. Rational LP and determinant bounds supply a
polynomial-bit relative interior point and inradius; their numerical
values may be exponentially small. Neither an optimizer slack bound nor
an input-only positive inradius is being assumed.

The final feasible repair is particularly suitable for this polytope.
After propagating interval bounds, clip a rational approximate point and
take predecessor maxima. The result obeys every order inequality. It
stays within the same infinity-norm error of any feasible comparison
point: a predecessor's exact value is at most the target coordinate's
exact value, and the coordinate itself supplies the opposite bound.
Propagated upper bounds ensure no repaired value exceeds its interval.

Consequently an epsilon-near epigraph point can be made exactly feasible
at objective cost at most `(G+1)epsilon`, using a one-norm gradient bound.
The known interior-ball homothety also bounds the difference between the
original and eroded-body optima. These are the two explicit repairs needed
for the GLS weak-optimization guarantee. The current closure and
composition notes contain both; no exact epigraph feasibility is inferred
directly from GLS. The same predecessor repair makes fallback algebraic
approximants feasible, with an additional logarithmic dimension margin
when Euclidean point accuracy is requested.

## 5. Bit composition and requested clarifications

Replacing box membership by polynomially many linear order inequalities
keeps the growth and canonical fallback formulas at two quantified blocks.
The established degree/count/height separation therefore still supplies
base-only exponential budgets. The growth and exposure-gap probabilities
are each at most `rho` under the displayed finite-law schedule, and the
fallback's exponential factor is fixed before sampling precision is chosen.
No face enumeration, real-number sampling oracle, or coefficient-height
exponent depending on dimension is hidden in the expected bound.

These clarifications were requested and are now applied:

- Direct evaluation when no variable remains, before dividing by `n`.
- Curvature proof data and its polynomial-time verification charged to the
  input/work model, with extra verifier cost stated separately if needed.
- Tautological rows removed before the interior-slack LP.
- The copy-matrix factor in physical Euclidean accuracy, including a
  logarithmic refinement margin on the fallback branch.
- Explicit near-feasible/eroded-body GLS repair in the supporting closure
  note as well as the composition.

## 6. Independent exact checks

I wrote and ran

```
python3 -B research-20261002/new-direction/check_order_polytope_review.py
```

The [checker](check_order_polytope_review.py) uses chain, fork, and cyclic
order systems, with exact isotonic quadratic optima obtained by active-face
enumeration and exact LP values obtained from all feasible zero-one
vertices. It passed 297 finite-noise draws, 969 sound forced equalities,
494 active-gap checks, 213 zero-gap incidences, 6,831 gap-Lipschitz checks,
and 275 fixed-face/proposal probability comparisons. It also passed 1,754
common-threshold rounding atoms, checking feasibility, exact means, and
the Hessian rounding error. Results are saved in
[order-polytope-review-check-results.json](order-polytope-review-check-results.json).

These finite exact checks target the new LP/rounding interfaces. They do
not prove the asymptotic probability theorem experimentally, implement the
full sparse solver, or replace the analytical chamber review. The author's
separate tests have not been rerun. No external search, project-wide checks,
CI inspection, or index edits were performed. This mathematical review
does not establish publication priority.
