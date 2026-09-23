# Positive-box multilinear gaps: aspect-ratio bounds and original-box transfer

Status: complete and independently reviewed. Verified 2026-09-20.
The initial three-review assignment omitted PB27-PB31. A subsequent review
covered that tier; [REVIEW.md](REVIEW.md) records the initial omission and the
follow-up separately.

This is topic 18 of the [recommended-topic sequence](../../RECOMMENDED-TOPICS-PLAN.md).
It verifies the two-sided aspect-ratio bound on the termwise-to-hull gap ratio
over strictly positive boxes — the `rho + 2` upper bound of
[`positive-multilinear-positive-box-sharp.md`](../../../results/positive-multilinear-positive-box-sharp.md)
with its full derivation in
[`positive-box-rho-plus-two-proof.md`](../../../notes/positive-box-rho-plus-two-proof.md),
the `max{2, rho}` lower bound of
[`positive-multilinear-positive-box-lower.md`](../../../results/positive-multilinear-positive-box-lower.md),
and the finite-dimensional refinement `rho + beta_N` of
[`review-positive-box-balanced-orientation-closure.md`](../../../notes/review-positive-box-balanced-orientation-closure.md).

All forty-six obligations are covered with the source corrections recorded in
`COVERAGE.md`, including PB44's even-dimension and common-box qualifications.
The earlier gaps in PB07, PB10, PB32, and PB37 are now closed: Lean proves the
fair-law equivalence, slab integrality, partition nesting, and incidence-bound
attainment. Independent reviews and their resolutions are recorded below.

- [Mathematical obligations](CLAIMS.md), frozen before the proofs.
- [Claim-to-declaration coverage](COVERAGE.md), one row per obligation PB01-PB46.
- [Independent review](REVIEW.md).
- [Verification record](VERIFICATION.md).
- Proof sources: the nineteen new modules under
  [`Formal/MultilinearGap`](../../Formal/MultilinearGap).

## What the package proves

`C_box(rho)` is the supremum, over every dimension, every multilinear support
with nonnegative coefficients and every strictly positive box whose coordinate
aspect ratios are at most `rho`, of the ratio of the termwise gap to the hull
gap. The headline is

> `max {2, rho} ≤ C_box(rho) ≤ rho + 2` for every `rho > 1`,

with `C_box(2) ≤ 4` and `0 ≤ C_box(rho) - rho ≤ 2`. **No exact value is claimed
at any fixed `rho`.** In fixed dimension `N ≥ 2` the upper constant improves to
`rho + beta_N` with `beta_N < 2`, degrading to `rho + 2` as `N` grows.

## Why it reuses the existing box layer rather than rebuilding it

Unlike [topic 17](../17-grid-switching/README.md), which needed a new model,
this topic lives inside the existing `MultilinearGap` and `CubicGap` trees. The
box semantics (`coordinateBox`, `boxPoint`, `boxHullGap`, `boxTermwiseGap`), the
affine-rescaling identities and the law and moment machinery all apply verbatim
to strictly positive boxes, and are used unchanged. `CLAIMS.md` requires each
reuse to be identified and forbids silently reproving anything; the reuse
inventory at the end of [COVERAGE.md](COVERAGE.md) is that record, including the
seven listed assets that turned out not to be needed and the three places where
new work deliberately overlaps existing material — one of them a duplicated
private helper that the inventory did not record until now, while claiming that
nothing was silently reproved.

`CLAIMS.md` also names three results that *look* reusable and are not — the
degree-capped cube bounds, the cube-monomial concave envelope, and the `[0,1]`
Fréchet convex envelope. None is used in the forbidden role. The physical
monomial `∏ (1 + t Y_i)` has different envelopes from the cube monomial
`∏ Y_i`, and both of its envelopes are redone from scratch.

## The load-bearing step, and how it is proved

Everything on the upper side reduces to one inequality: the coefficient
`F_{n,j} = 2 C_j + V_j - P_j - 2 O_j + C_{j-1} - P_{j-1}` is nonnegative for
every dimension, every order and every point of the cube, where `C`, `V`, `P`
and `O` are the binomial moments of common-threshold, adjacent-count,
independent-Bernoulli and endpoint-orientation rounding. Nonnegativity is proved
by induction on the support, using a **spreading step at a global minimum and a
global maximum**. The hypothesis cannot be weakened: `F` is not Schur-concave,
and the sources' four-variable counterexample was reproduced independently
during review. This is source-review evidence; no Lean declaration establishes
the failure of Schur-concavity, and `CoefficientInequality.lean` mentions it in
its docstring. The orientation moments' Lipschitz bound is proved by coupling,
**not** by differentiation — the partial derivatives need not exist at an
orientation breakpoint.

The finite-dimensional refinement replaces the constant `2` by `beta_N = 1/p_N`,
where `p_N` is the probability that a given pair of coordinates receives
opposite orientations under a **balanced ambient** law. The delicate point is
that restricting to a smaller support must not resample the law in the smaller
dimension. The moment's law argument is the ambient law on the whole index
type, and the support only selects which coordinates are counted. These
definitions and proofs retain the ambient constant as the support shrinks;
substituting the support-size constant is invalid in general. The type system
does not prohibit writing that constant or defining a different law.

## The identified risk, and what it cost

The lower bound imports a unit-box incidence maximum from topic 19, made an
obligation here as PB37. Both directions are proved: `RadixIncidence.lean`
provides the upper bound and `RadixAttainment.lean` constructs an attaining law.
The upper bound needs only `1 ≤ b` and `1 ≤ L` — an earlier version of this
paragraph said `1 ≤ b` alone, but `1 ≤ L` is in both upper-direction signatures;
attainment holds for `b ≥ 2` and `2 ≤ L ≤ b + 2`, which includes the source's
regime `2 ≤ L ≤ b`.

`SlabIntegrality.lean` proves the geometric statement required by PB10, in
addition to the original direct adjacent-count construction.
`FairOrientationFolding.lean` identifies the unfolded fair-orientation law with
the folded law used in the upper bound. `Radix.block_subset_unique` proves
PB32's nested partitions on the actual leaf blocks. The coverage map links each
result to its obligation.
