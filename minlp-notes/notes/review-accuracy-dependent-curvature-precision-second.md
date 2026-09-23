# Independent second review: accuracy-dependent scalar curvature precision

Date: 2026-09-05. Reviewer: `constant_rank_review`.
Verdict: **PASS** for the finite mathematical statements reviewed below.

Reviewed notes:

- [Accuracy-dependent curvature precision](accuracy-dependent-curvature-precision.md).
- [Raw curvature arclength obstruction](curvature-arclength-precision-obstruction.md).
- [Scalar convex graph two-bit gap](scalar-convex-graph-two-bit-gap.md).

This review checks the proofs and constants. It does not establish priority,
a polynomial-time integration or quantile algorithm, or a multivariate
extension. The formulation claims allow real coefficients and unrestricted
finite continuous size, as the notes expressly require.

## Density mass and the endpoint Taylor remainder

Write `A=sqrt(f''/epsilon)`, `rho=min(A,(1-x)A²)`, and, on `[a,b]`,
`m=integral rho`, `E=integral (b-t)A(t)² dt`. Continuity makes all these
integrals finite. Nondecreasing curvature implies nondecreasing `A`, even
where curvature vanishes.

The split at `(b-t)A(t)=1` proves `E<=m²+3m/2`. On the lower side the
integrand is bounded by both branches of `rho`. On the upper side,
monotonicity gives

```
m >= integral_t^b min(A(t),(b-s)A(t)²) ds
  = (b-t)A(t)-1/2.
```

The last equality applies because this side has `(b-t)A(t)>=1`.
Here `rho(t)=A(t)`, so the two contributions are respectively bounded
by `m` and `(m+1/2)m`. Thus mass at most `1/2` implies `E<=1`.
The chord gap is at most the left-end tangent remainder `epsilon E`:
the chord minus that tangent increases linearly from zero to this
remainder, while the function lies above its tangent.

The continuous cumulative density admits mass quantiles. Zero-density
pieces can be included in neighboring intervals. If total mass is zero,
continuity forces `A=0` on `[0,1)`, and then also at 1, so the function
is affine. Otherwise at most `ceil(2M)` positive-length pieces suffice.
These observations justify `N_epsilon<=2M+1`, including the affine case.

## The potential estimate and its constants

For an admissible interval of length `ell` and midpoint `c`, the midpoint
Jensen gap satisfies

```
J >= (1/2) integral_c^b (b-t)f''(t) dt
  >= f''(c)ell²/16.
```

The left half of the endpoint tangent remainder is at most
`3f''(c)ell²/8<=6J`; its right half is at most `2J`. Therefore `E<=8`.
The constants use only nonnegative nondecreasing curvature.

For `chi(x)=(1-x)A(x)` and `d=1-b`, the claimed universal estimate is

```
m <= chi(b)-chi(a)+2E+2sqrt(2E).
```

Both cases in the proof are valid. If `ell<=d`, use `m<=ell A(b)` and
subtract the potential difference to obtain
`2ell A(a)-(d-ell)(A(b)-A(a))<=2ell A(a)`.
If `ell>d`, split at `b-d`: on the left, `1-t<=2(b-t)`, while the
right part has mass at most `dA(b)=chi(b)`. After subtracting the
potential difference the bound is `2E+chi(a)`, and
`chi(a)=(d+ell)A(a)<=2ell A(a)`.
Finally `E>=ell² A(a)²/2` proves the displayed estimate in both cases.
The second case includes `b=1`, whose right subinterval has length zero.

On an admissible interval `2E+2sqrt(2E)<=24`. Summing over a partition
telescopes the potential to `chi(1)-chi(0)=-chi(0)<=0`; finiteness at
the endpoint follows from the stated `C²([0,1])` hypothesis. Consequently
`M<=24N_epsilon` with no hidden endpoint or strictly positive curvature
assumption.

## Comparison with arbitrary convex integer lifts

Choose an exact graph witness for each input. Partition them by the parity
of their integer coordinates. For two witnesses of equal parity, their
lifted midpoint has integral integer coordinates and remains feasible by
convexity. Hence their scalar midpoint Jensen gap is at most `epsilon`.
There are at most `2^p` such supports. Closure in the compact input
interval preserves this pairwise inequality by continuity; no boundedness
or closedness of the lifted witnesses is required.

The span of each nonempty closed support has endpoint midpoint gap at
most `epsilon`. Its chord gap is nonnegative and concave, vanishes at
the endpoints, and has maximum at most twice its midpoint value.
Therefore every span has chord error at most `2epsilon`. Degenerate
spans cause no difficulty. A finite cover by closed intervals can be
trimmed to a partition with at most as many pieces, each contained in
one covering interval. For example, greedily choose a covering interval
that reaches farthest to the right from the current endpoint; a finite
cover of an interval ensures progress until 1. Chord error cannot increase
on a subinterval of a convex function's domain.

Thus `N_(2epsilon)<=2^p`. Pointwise `rho_epsilon<=2rho_(2epsilon)`
because the two branches scale respectively by `sqrt(2)` and 2.
It follows that `M_epsilon<=48*2^p`. Since `p>=0`, this implies
`1+M_epsilon<=49*2^p` and proves the stated lower bound.

For the upper bound, a cell band between its chord minus `epsilon` and
its chord contains the exact graph and lies inside the permitted tube.
Each cell includes its input interval constraints. A finite union of
these bounded polyhedra admits a Hamming-distance encoding with
`ceil(log2 N_epsilon)` binaries; unused codes can be forbidden. Global
input/output bounds supply finite valid deactivation constants. Together
with `N_epsilon<=2M_epsilon+1`, this proves the upper bound
`p_bin<=log2(1+M_epsilon)+2`. The proof is about finite existence, not
the size or arithmetic complexity of constructing the partition.

## Raw arclength obstruction

For `f_M=(1/M)sum_j x^(2^j)`, let `k=2^j`. The intervals
`[1-1/k,1-1/(2k)]` have disjoint interiors and length `1/(2k)`.
On each, the selected monomial contributes at least `k²/(8M)` to
curvature: `k(k-1)>=k²/2` and `(1-1/k)^(k-2)>=1/4` for `k>=2`.
Its contribution to the integral of square-root curvature is therefore
at least `1/(4sqrt(2M))`. Summing gives the claimed `sqrt(M)/(4sqrt(2))`.

The function is continuous, strictly increasing, convex, and has range
`[0,1]`. Inverse images of 16 equal height intervals give chords of
error at most `1/16`, since the chord and graph lie between the same
endpoint heights. Four binary cell-index variables suffice for their
finite union. This proves the unbounded overestimate by raw arclength
at fixed tolerance across the family. The note correctly distinguishes
this from fixed-function asymptotics as tolerance tends to zero.

## Two-bit gap for every continuous convex scalar graph

This supporting result does not require differentiability or monotone
curvature. Uniform continuity gives a finite admissible chord partition;
the preceding parity-span proof still gives `N_(2epsilon)<=2^p_conv`.

Take any interval whose chord gap `g` is at most `2epsilon`. If its
maximum exceeds `epsilon`, the concave gap's superlevel set is a
nondegenerate closed interior interval `[u,v]`, and both boundary values
equal `epsilon`. On each outside interval, the new chord error is
`g` minus its chord there, and lies between zero and `g<=epsilon`.
On the middle interval, that chord of `g` is the constant `epsilon`,
so its new error is `g-epsilon<=epsilon`. At most three pieces suffice.

Consequently `N_epsilon<=3N_(2epsilon)` and
`p_bin<=ceil(log2(3*2^p_conv))=p_conv+2`. All endpoint, flat-segment,
and nondifferentiable cases follow from continuity and concavity. This
comparison makes no claim that the finite partition can be computed
in time polynomial in the accuracy encoding.

## Supporting computation

The repository checker `code/quadratic_rank/check_accuracy_dependent_curvature.py`
was rerun successfully: 140 exact rational Taylor/midpoint inequalities
for nondecreasing polynomial curvature, and 420 branch-split numerical
interval-mass and potential checks. The numerical integrations are
supporting evidence only. The proofs above supply the certificates.

No mathematical correction is required by this independent review.
