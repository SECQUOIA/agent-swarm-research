# Marginal-floor semantic review

Status: semantic review completed. The separate
[verification record](VERIFICATION.md) records the passing build, axiom audit,
import coverage, and kernel replay on 2026-09-17.

The independent review compares the [source result](../../../results/positive-multilinear-marginal-floor-gap.md)
with [CLAIMS.md](CLAIMS.md), the current `Floor*.lean` statements, and their
existing graph-hull and finite-law dependencies. The first pass covered
`FloorDomain`, `FloorDensity`, `FloorCoupling`, `FloorGain`, `FloorExpBound`,
`FloorIntegralBounds`, `FloorAsymptotics`, and `FloorLower`. A second pass covered
the completed `FloorUpper`, `FloorSemantics`, and `FloorResults`, and rechecked
the now-unconditional scalar asymptotic declarations. A final targeted pass
checked the supporting dyadic statements added to `FloorLower` and every row
of the completed [coverage map](COVERAGE.md) against the literal inventory.

## Findings addressed by the current implementation

- `floorRatios` ranges over every finite dimension and degree, requires positive
  included coefficients, and uses actual `weightedTermwiseGap / hullGap` with a
  strictly positive denominator. `CubeFloorBound` is stronger: it admits zero
  coefficients and does not require positive hull gap. This matches the source
  and supports box expansions with zero coefficients.
- The ratio classes have explicit positive-width bilinear witnesses. Real
  supremum inequalities still need boundedness at their call sites; the
  definitions alone do not make unbounded real `sSup` meaningful.
- `floorDensity` uses `max 0 t`, which agrees with the source density on the
  integration interval and is positive for every real parameter when `τ>0`.
  This satisfies the global probability requirements of `integratedBernoulli`.
- Density normalization, the clipped-mass bound, and the correction integral
  are proved, rather than supplied as assumptions. The correction allows
  `p=0` and proves positivity of its denominator from `p<1`.
- `floorLaw` depends only on the requested means and the shift. Its exact mean
  theorem quantifies over all coordinates. The termwise gain is therefore
  simultaneous and independent of objective coefficients.
- `floorUnion_exp_lower` explicitly separates the clipping branch. A clipped
  failure is proved to have corrected probability one, which makes the union
  certain. In the other branch the exponential uses the original failure sum,
  as required by the written proof.
- `floor_integral_gain` is multiplicative and permits zero total failure mass;
  it does not introduce an unjustified division by a zero termwise gap.
- The integral upper estimate splits at `1/L` and uses the reciprocal bound
  only on `[1/L,1]`. This avoids a false pointwise comparison at zero under
  Lean's totalized division.
- The integral lower estimate proves the quadratic exponential inequality and
  the reciprocal-square integral. Its bounds do not assume the desired
  asymptotic equivalence.
- `FloorLower` chooses the natural floor of the real base-two logarithm,
  establishes two-sided feasibility, and proves a normalized limit through
  every positive real floor tending to zero. It uses the existing actual
  dyadic hull-gap upper bound to obtain a sufficient lower ratio. It need not
  reprove the existing exact-family limit to obtain the sharp lower constant.
  The final additions also expose `means_dyadic_strip` for every natural level
  at least one, `tendsto_floorLevels` for divergence of the selected natural
  level, and `tendsto_floorLevels_scale` for the source's unshifted
  `ell/log₂ ell` scale. These account directly for the supporting statements in
  MF-23 and MF-25, beyond the comparison needed by the terminal squeeze.
- `floorBoxParameter` chooses `δ` on fixed coordinates and the usual normalized
  quotient elsewhere. The map back to the original point is proved, including
  degenerate coordinates. Box transfer compares the original, unexpanded
  termwise width with the expanded one in the correct direction and preserves
  the actual polynomial hull width.

## Terminal results and resolution of first-pass checks

`floorMixture` explicitly mixes the two laws with inverse-gain weights.
`floorMixture_deficiency_nonempty` handles the equality threshold `x_i=1/2`
through the easy branch; the unique-low argument handles the remaining hard
case. `floorMixture_deficiency_all` also covers empty terms, and singleton
terms are covered by the nonempty argument with zero failure sum.
`floor_cube_gap_bound` and `floor_finite_bound` require nonnegative coefficients
but no positive-gap hypothesis, so zero polynomial hull width is included.

The earlier conditional scalar helpers have been replaced by
`tendsto_floorIntegral_normalized` and `tendsto_floorUpper_normalized`, whose
proofs call the actual integral estimates. No density normalization, termwise
gain, asymptotic estimate, or cube floor bound is assumed by the terminal
theorems.

`floorSupremum_antitoneOn`, `floorSupremum_le_half`, and
`floorSupremum_le_upper` establish the finite supremum conclusions with the
proper domains. `floor_suprema_bounds` proves boundedness and inserts the
actual unit-coefficient witness into the strip class before using `le_csSup`.
The two limits in `sharp_marginal_floor_growth` use `𝓝[>] 0` for the real
floor variable. Their normalizing scale is proved positive eventually. The
strip theorem correctly claims only the same leading asymptotic constant.

`marginal_floor_original_box_bound` discharges the cube-bound premise of the
generic transfer theorem. It concerns `boxTermwiseGap` of the original terms,
with nonnegative box endpoints and a floor condition only on nonfixed
coordinates. It also permits `δ=1`; this is a valid stronger boundary statement.

`FloorSemantics` adds the exact minimum-of-anchor-and-failures formula and an
attained maximum weighted-deficiency characterization of the actual hull gap.
The latter has explicit valid minimum-mean anchors, as appropriate after
discarding empty terms; it proves attainment from existing hull compactness
rather than assuming an optimizing law. `floorIntegral_le_one` accounts for
the auxiliary integral bound included in the inventory.

## All-obligation cross-check

This is the semantic cross-check; [COVERAGE.md](COVERAGE.md) is the
declaration-by-declaration map. The final review checked all 32 rows, including
the distinction between positive-coefficient ratio classes and the stronger
nonnegative-coefficient multiplicative bound. Build and trust evidence is
recorded separately in [VERIFICATION.md](VERIFICATION.md).

| Inventory IDs | Review result |
|---|---|
| MF-01–03 | Actual positive-coefficient ratio domains, nonempty witnesses, boundedness, antitonicity and the above-half extension are represented correctly. |
| MF-04–06 | Exact monomial formula, common-threshold maximum, attained maximum deficiency and pointwise nonnegativity are covered by the new semantics module and existing foundations. |
| MF-07–10 | Parameter signs, integral positivity and upper bound, density normalization, clipping, and exact completion including zero failure are proved. |
| MF-11–13 | One explicit law preserves all means; the exponential union bound includes clipping; the actual hard-term deficiency is an integrated union. |
| MF-14–18 | The chord inequality handles zero failure without division; scaling, easy terms, the common mixture, and the finite actual-hull bound fit together. |
| MF-19–22 | The exact logarithmic identity and vanishing shift imply the stated expansion; the two integral estimates imply the unconditional normalized upper limit. |
| MF-23–25 | `means_dyadic_strip` proves the general strip for all levels at least one; existing declarations prove the unit-coefficient identity, exact termwise width, hull-gap positivity and exact-family asymptotic. `tendsto_floorLevels` proves divergence through all positive real floors, and `tendsto_floorLevels_scale` proves the literal unshifted scale limit one. The actual feasible witnesses enter both ratio classes. The terminal proof uses the sufficient comparison ratio, whose separate normalized limit is also proved. |
| MF-26–28 | The two supremum limits follow from proved upper and lower bounds over the correct classes. No fixed-floor equality of the classes or suprema is asserted. |
| MF-29–32 | Existing box hull equivalence and positive expansion are applied to a floor-preserving parameter, including fixed coordinates and zero gaps, in an unconditional original-box theorem. |

No unresolved mathematical defect, missing headline claim, or unmapped literal
inventory obligation was found in the final source-to-statement and coverage
comparison. The separate final verification record supplies the kernel-check
evidence; source inspection alone is not kernel-check evidence.
Literature novelty, publication priority, numerical
experiments, and review history remain outside Lean scope.
