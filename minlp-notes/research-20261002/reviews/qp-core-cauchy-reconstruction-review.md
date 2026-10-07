# Independent review of QP reconstruction from core Cauchy output

Date: 2026-10-02.

**Verdict: the completed box corollary and its general height lemma pass.**
This review freshly checks
[qp-core-cauchy-reconstruction.md](../new-direction/qp-core-cauchy-reconstruction.md),
including the revised rational fallback paragraph, against the actual
[core Cauchy interface](../new-direction/core-only-noise-core-oracle.md).
It does not assert the separately pending coupled-polytope oracle premise.

## Stationary-face argument

Independent active rows can be chosen to define the affine hull of the
minimal face, including when the ambient polytope is lower-dimensional.
Its relative-interior point admits both signs of every sufficiently small
tangent displacement. Tangent stationarity and positive semidefiniteness
of the restricted Hessian follow.

For two points `x,y` of the stationary-face polytope, put `w=x-y`.
Their common face equations give `w in ker R`. Stationarity at both
points gives

`w'(Ay+c)=0` and `w'A(x-y)=0`.

The quadratic difference is therefore zero. Every point of that rational
polytope is globally optimal, without an equation involving the unknown
optimal value. Neither an inverse Hessian nor positive definiteness is
used in this constancy step.

The full lexicographic optimizer is the lexicographic minimum of this
polytope and is a vertex: any nontrivial segment through it has an
endpoint smaller in the first differing coordinate. The full selector,
with core coordinates first and residual coordinates afterward, is
essential to this vertex assertion. It agrees with the source Cauchy
theorem. Arbitrary other optimizers can have irrational coordinates.

## Exact denominator constants

The constants in (6) are valid as stated. Work with the active rows after
scaling by `D`. A rank-`r` pivot minor and the corresponding adjugate
construction give an integer nullspace basis whose entries are at most
`r! C^r <= n! C^n` in absolute value. Rank zero uses the identity;
rank `n` has no tangent equations.

Each coefficient and right-hand side of a scaled stationary equation is
a sum of at most `n` products of a basis entry and a scaled input entry.
It is consequently bounded by

`C_1 = n n! C^(n+1)`.

The scaled original constraints satisfy the same bound. A vertex has
`n` independent active equations; the determinant bound by permutation
expansion gives a common nonzero integer denominator and coordinate
numerators bounded by

`U = n! C_1^n`.

Because `DA/2`, `Dc`, and `Dc_0` are integral, substituting a common
coordinate denominator `Delta` gives an objective denominator dividing
`D Delta^2`. Thus `Q=D U^2` bounds the reduced denominators of both
the selected coordinates and the value. No extra factor of two is
missing. Objective numerators also have polynomial length, directly from
the same quadratic substitution. All logarithms of these bounds are
polynomial in the full sampled rational input length.

## Fixed law and continued fractions

After the grid size is fixed, twice the product of the base denominators,
the denominator of `sigma`, and `M-1` clears every possible sampled
linear coefficient and keeps `DA` even. Repeated factors cause no
problem. An integer bound on scaled data using
`|c_i+gamma_i| <= |c_i|+sigma` for core coordinates gives one valid `C`
for every atom. These choices have polynomial length in `I+log M` and
do not require knowing the sampled indices.

The precision condition `2^(-t)<=1/(8Q^2)` gives core intervals of
width at most `1/(4Q^2)`, and a still narrower value interval. Two
different reduced rationals with denominators at most `Q` are separated
by at least `1/Q^2`, so the rational in each interval is unique.

Its distance from the rational midpoint is at most `1/(8Q^2)`, strictly
below `1/(2b^2)` for its own denominator `b<=Q`. The continued-fraction
criterion therefore includes it among the midpoint's convergents.
Checking interval membership identifies it. The argument covers signed
values, zero, and exact rational midpoints with the usual signed
continued-fraction convention. It needs polynomial work in the interval
and denominator-bound encodings.

The source evaluator supports every accuracy for one fixed law. Therefore
choosing `t=poly(I+log M)` after `M` introduces no precision loop. For the
reviewed box law, `log M=poly(I)`, so one polynomial-precision query
suffices.

## Rational fallback and expected postprocessing cost

At the full lexicographic optimizer, a nonzero null direction of the
positive semidefinite tangent Hessian would preserve the quadratic value
along both small signs. One sign would be lexicographically smaller.
Hence this selected point has positive definite tangent Hessian on its
minimal face, with zero-dimensional faces included.

Its independent active rows consequently give a nonsingular stationary
KKT system. Enumerating such row sets, solving nonsingular systems,
discarding infeasible candidates, and comparing objective then full lex
order includes and selects the desired point. Singular systems may be
skipped. Other retained candidates need not be local minima: feasibility
ensures that none has value below the true global minimum.

There are base-exponentially many row sets and polynomial-bit rational
solves. Their whole cost can be included in the fallback budget before
choosing the law; sampled coefficient bits remain in its fixed-exponent
polynomial factor. On fallback, the exact rational answer is returned
directly. Ordinary-branch primal and interval outputs have polynomial
length at the selected polynomial precision. Thus the subsequent
continued-fraction computation has deterministic polynomial cost on the
data it actually receives. No nonlinear postprocessing bound is inferred
from the expected length of a potentially large algebraic record or
proof trace.

## Convex completion and scope

The reconstructed core defines a nonempty rational fiber of polynomial
encoding length. Exact rational convex QP on that fiber supplies a
globally optimal residual completion in polynomial bit work. A rational
affine-hull reduction handles lower-dimensional fibers if needed. The
completion may choose any residual optimizer; it need not reproduce the
lexicographic residual coordinates used for the height proof. Its exact
value agrees with the separately reconstructed optimum value.

For the box corollary, the PSD residual block supplies fiber convexity,
and the reviewed Cauchy theorem supplies the same full lexicographic
core. Substituting the polynomial reconstruction precision into its
one-query bound preserves the fixed input exponent and the claimed
parameter factor, including the stated specialization for `k<=2`.
The separate coupled-polytope application remains conditional, as the
draft explicitly states.

## Verification scope

This was a document and mathematical review. No new agents, literature
search, executable tests, project-wide verification, or CI inspection
were used. The final saved fallback paragraph was reread after it added
explicit infeasible-candidate rejection.

Targeted document check:

```sh
git diff --no-index --check /dev/null research-20261002/reviews/qp-core-cauchy-reconstruction-review.md
```

It reported no whitespace errors. Exit status `1` denotes the new-file
comparison.

## Addendum: coupled-polytope application, 2026-10-02

**The new Section 5 passes a fresh interface and arithmetic check.**
This addendum supersedes the earlier references to a pending coupled
application. I read the saved Section 5, the actual
[coupled value theorem](../new-direction/coupled-polytope-core-value-oracle.md)
and [selected-core oracle](../new-direction/coupled-polytope-core-oracle.md),
and their completed
[value](coupled-polytope-core-value-review.md) and
[selected-core](coupled-polytope-core-oracle-review.md) reviews.
The source algorithms' separate proof reviews remain their own records;
this addendum checks the new exact-QP transfer against their interfaces.

For any residual interval of positive width, write
`z_i=ell_i+(u_i-ell_i)y_i`. After substituting fixed residual coordinates,
this is an affine bijection between the original feasible polytope and
its normalized image. Convexity of the supplied corrected objective is
preserved by this substitution. The core coordinates are unchanged, so
both `alpha ||v||^2/2` and the sampled linear term `gamma'v` are exactly
unchanged. No residual width factor multiplies `alpha` or changes the
noise scale. Quadratic and linear constraint substitution has polynomial
rational encoding cost, with all supplied bounds counted in the input.

Positive coordinate widths also preserve the full lexicographic order:
the first differing residual coordinate has the same order before and
after normalization. Inserting fixed coordinates changes no comparison.
Thus the oracle's selected core is the core of the same full lexicographic
optimizer used in the height proof, even if the oracle is implemented
after residual normalization.

The reviewed coupled oracle supplies exactly the same-law value interval
and selected-core error contract needed by Section 3, with
`log M=poly(I)` and expected work
`f(k)(1+alpha/sigma)^k poly(I+t)`. Its compact-domain argument permits
lower-dimensional polytopes and projected core sets without assuming
continuity of a partially minimized value function. The general rational
height proof applies directly to the original polytope. The same rational
QP fallback may be included in the base budget before selecting the law;
it preserves the full lex selector and directly returns an exact rational
answer. Ordinary outputs undergo only polynomial-size rational
reconstruction.

Finally, on a fixed reconstructed core, the supplied correction is
constant. Convexity of the corrected objective on the polytope therefore
implies convexity of the original quadratic on that fiber. Exact convex
completion applies, including after rational affine-hull reduction. This
establishes the claimed exact expected bound with the supplied `alpha`.
When `alpha=0` (or there are no core coordinates), direct exact convex
QP suffices. No replacement of `alpha` by the box curvature bound is
justified or claimed.

No mathematical correction was needed. This fresh addendum used no
delegation, external research, or executable tests. The targeted whitespace
command recorded above was rerun on the updated review and reported no
errors; no project-wide or CI checks were run.
