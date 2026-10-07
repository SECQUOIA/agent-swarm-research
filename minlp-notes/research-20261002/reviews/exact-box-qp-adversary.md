# Adversarial review of exact rational mixed-integer box QP corollary

Date: 2026-10-02.

Reviewed `geometric-dp/exact-box-qp.md`, the supporting geometric-grid
theorem, and the rational bit-complexity argument in `extensions.md` §5.
This was a fresh mathematical review, with no external literature search.

**Verdict:** no substantive mathematical gap found. The stated exact
polynomial-time guarantee follows under the global growth promise, at fixed
bag size. Acceptance is valid independently of that promise. The standard
rational-height and reconstruction ingredients are not novelty claims.

## Height and normalization

The minimum-face argument works without growth or uniqueness. A minimizer
exists by compactness, and a minimum face dimension exists because dimensions
are integers between zero and the number of variables. Free coordinates are
strictly interior to their intervals, so free stationarity and positive
semidefiniteness hold. If the free Hessian is singular, its null direction
has zero first-order and quadratic change. The quadratic is constant along
that direction while it stays in the box. The bounded box forces the line
to reach a free-coordinate bound, contradicting the chosen face dimension.
This supplies an invertible free system even when other optimizers form a
continuum.

Equation (3) includes the necessary extra endpoint denominator. With
`x_A=t_A/D`, its right side is integral, and all coordinates have a common
denominator dividing `D det(2H_SS)`. The determinant is positive and obeys
the displayed expansion bound. The empty free set is handled correctly by
determinant one. Substituting a common denominator `q` gives value denominator
dividing `D q^2`; it does not require the optimum's reduced denominator to
divide the numerical upper bound `V`.

The extra `D` is material. For `F=(x-y)^2/5+y` on
`[0,1] × [1/5,2/5]`, the optimizer is `(1/5,1/5)`. Here `D=5` and the
free determinant is two. The free coordinate denominator does not divide
that determinant alone. The draft's normalization covers this example.

## Reconstruction and acceptance

Value isolation is sound because distinct denominator-at-most-`V` rationals
are separated by at least `1/V^2`. The midpoint error is at most
`1/(8V^2)`, strictly below the continued-fraction criterion
`1/(2q^2)` for the desired reduced denominator `q<=V`.

For coordinates, radius `rho=1/(4R^2)` gives interval length
`1/(2R^2)` and midpoint error at most `1/(4R^2)`. This again satisfies
the strict continued-fraction criterion. Signed floor-based continued
fractions handle negative values and intervals crossing zero. Rational
midpoints cause no exceptional case: if a qualifying target exists, it is
a convergent, including the midpoint itself when appropriate. Enumeration
has polynomial bit cost and does not enumerate denominators up to `R` or
`V` numerically.

Independent coordinate reconstructions need not have a common denominator
at most `R`. The draft correctly avoids using such a bound for an arbitrary
candidate. Feasibility and exact equality to the isolated optimum value
are sufficient for unconditional acceptance.

## Trial schedule and bit complexity

Every trial uses grids containing the whole box's endpoints, so its lower
bound stays valid even when its guessed mesh parameter is inadmissible.
The stage cap and gap target are computable by rational comparisons. At
the first admissible trial, the supporting theorem reaches the gap target,
and

```
||y-x*||^2 <= 1/(128R^4) < 1/(16R^4) = rho^2.
```

Thus abandoning a trial after a failed reconstruction cannot prevent the
first admissible trial from succeeding. The argument does not presume that
an arbitrary nearly optimal feasible value has bounded denominator.

For clarity, the supporting arithmetic bound can be substituted explicitly.
Writing `r=m*+1`, admissibility gives `2^r=O(sqrt(kappa))` and
`r=O(1+log kappa)`. Also `J=poly(I)+O(log kappa)`, so the grid denominator
exponent `E=J+O(r 2^r (J+1))` is polynomial in `I,kappa`.
With degree two, the common-denominator bit bound and the number of bag
entries are consequently polynomial in those quantities for fixed `p`.
Earlier trials have smaller stage caps and arithmetic bounds; their
`2^(rp)` table factors sum geometrically. No exponential denominator
bound is being treated as a polynomial numerical quantity.

## Certificate details

The certificate can be checked without the trial history or the growth
constant. A checker verifies endpoint-containing grids, their corrections
from the known diagonal upper curvature, the factorization and finite DP
recurrences, the rational interval, and the feasible candidate's exact
objective. Lemma 1 then isolates the true optimum in that interval.

Two optional clarifications were recommended and are now included in the
corollary, without changing the proof:

- State that the checker verifies the candidate objective lies in the
  displayed isolating interval and has reduced denominator at most `V`.
  Reconstruction already guarantees these properties in the algorithm.
- Mention the separate certificate for the `L0<=0` branch: endpoint DP
  optimality plus coordinatewise concavity. That branch does not need an
  isolating interval or a positive-curvature correction.

## Follow-up: uniqueness implies qualitative quadratic growth

The proposed additional lemma is correct for a quadratic on a compact box.
Consequently the exact algorithm terminates on every such rational problem
with a unique optimizer, even without a quantitative conditioning promise.
Its polynomial-time bound still depends on the numerical value of `kappa`.

Here are the details needed for the contradiction argument. If no positive
global growth constant exists, choose feasible `x_k != x*` with
`[F(x_k)-F(x*)]/||x_k-x*||^2 -> 0`. Compactness bounds the squared
distances, so the objective gaps tend to zero. Uniqueness and compactness
then imply `x_k -> x*`. Put `t_k=||x_k-x*||` and, after taking a
subsequence, `u_k=(x_k-x*)/t_k -> u`, where `||u||=1`.

For `ell=2Qx*+d`, first-order optimality along every feasible chord gives
`ell^T u_k>=0`. The exact expansion is

```
[F(x_k)-F(x*)]/t_k^2 = ell^T u_k/t_k + u_k^T Q u_k.
```

The quadratic terms are bounded, so `ell^T u_k=O(t_k)` and
`ell^T u=0`. Nonnegativity of the first term also implies
`u^T Q u<=0`. The limit direction has the required signs at each active
box bound. Thus `x*+tau u` is feasible for every sufficiently small
positive `tau`; this feasible-ray property is essential. Optimality on
that ray gives `u^T Q u>=0`. Equality makes the whole short ray optimal,
contradicting uniqueness. The proof supplies existence, not a useful
numerical lower bound on the growth constant. No new executable checks
were needed for this follow-up.

## Follow-up: mixed integer and continuous boxes

The extension to a product of rational continuous intervals and
integer intervals is valid. Integer bounds must first be rounded inward;
empty domains are rejected and fixed coordinates can be eliminated. No
integer-domain enumeration is needed for the proof or the algorithm.

For the height lemma, fix the integer coordinates of one global optimizer
and minimize face dimension only in its continuous slice. The same null
direction argument applies to free continuous coordinates. The complementary
set `A` now contains both active continuous coordinates and all integer
coordinates, including integers strictly between their bounds. Each still
has the representation `t_i/D`: use `t_i=D x_i` for an integer coordinate.
The same integer linear system, determinant bound, `R`, and `V` therefore
apply. Selecting this slice is an existence argument, not an algorithmic
search through assignments. The magnitudes of its integers, and hence the
binary lengths of the right-hand side and reconstructed numerators, are
bounded by the input endpoints. Large domain cardinalities introduce no
unaccounted factor in the running time.

The qualitative growth proof also extends. Compactness and uniqueness
first force the putative sequence `x_j` to converge to `x*`. Integer
coordinates must then equal their optimizer coordinates for all sufficiently
large `j`. Only after this observation may one use first-order optimality
along the remaining chords; a chord that changes an integer coordinate
would not justify that step. The normalized limit direction has zero
integer components and admits a short feasible ray in the continuous
slice. The existing contradiction follows. In a purely integer box,
convergence alone already contradicts `x_j != x*` eventually.

The mixed-grid theorem supplies exactly the required lower bounds and
contraction estimate, and the rational bit bound already covers integer
steps and mixed grids. In particular, ignoring unit grid intervals in an
integer coordinate's correction is valid because they contain no omitted
feasible integer. Reconstruction keeps the same thresholds: integers are
rationals of denominator one. The final acceptance check must include
integrality, and the certificate checker must use the integer grid
corrections and verify integer feasibility. Its validity then remains
unconditional. For `L0<=0`, sequential endpoint minimization on the
continuous enclosing box attains integer endpoints as well, so the endpoint
DP branch remains valid. Polynomial time still requires a bound on
`kappa`, even though every unique mixed optimum has some positive growth
constant.

The final revised mixed-domain note was reread after these edits. Its
height lemma, qualitative growth proof, acceptance checks, and complexity
scope agree with this review. No stale continuous-only restriction or
substantive logical mismatch remains. The purely continuous example is
properly identified as also valid with its third variable restricted to
`{0,1}`. This follow-up was a proof review; no new executable tests were
run.

## Targeted verification performed

Ran one inline `python3 - <<'PY'` check using exact `fractions.Fraction`
arithmetic. It passed 11,376 continued-fraction reconstruction cases with
denominator bounds one through twenty, positive and negative targets, exact
midpoints, and both maximal signed coordinate errors. It also checked the
rational active-bound normalization example, 121 feasible objective
comparisons for that example, and the strict stopping-constant inequality.
These finite checks supplement the proof review; they do not establish the
general theorem. No project-wide checks or CI inspection were performed.
