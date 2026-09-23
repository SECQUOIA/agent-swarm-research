# Positive-box multilinear gaps: mathematical obligations

This frozen inventory covers topic 18 of the
[recommended-topic sequence](../../RECOMMENDED-TOPICS-PLAN.md): aspect-ratio
upper and lower bounds for the termwise-to-hull gap ratio on strictly positive
boxes, the finite-dimensional refinement, and the original-box interpretation.

Sources:
[`positive-multilinear-positive-box-sharp.md`](../../../results/positive-multilinear-positive-box-sharp.md)
(the `rho + 2` upper bound),
[`positive-multilinear-positive-box-lower.md`](../../../results/positive-multilinear-positive-box-lower.md)
(the `max{2, rho}` lower bound), the balanced-orientation closure in
[`review-positive-box-balanced-orientation-closure.md`](../../../notes/review-positive-box-balanced-orientation-closure.md)
(the finite-dimensional refinement), and the full derivation in
[`positive-box-rho-plus-two-proof.md`](../../../notes/positive-box-rho-plus-two-proof.md).

## Relation to existing work

The existing `Formal/MultilinearGap` and `Formal/CubicGap` trees already carry
the box layer this topic needs. Reuse is expected and must be identified in
`COVERAGE.md`; nothing may be silently reproved. In particular the following are
available and need only `l i <= u i`, so they apply verbatim to strictly
positive boxes: `coordinateBox`, `boxPoint`, `boxGraph`, `boxEnvelopeValues`,
`boxHullGap`, `boxTermwiseGap`; the affine-rescaling identities
`boxHullGap_eq_of_mem`, `boxEnvelopeValues_eq_of_mem`, `exists_boxPoint`; the
vertex-law semantics `mem_boxGraph_hull_iff`, `boxEnvelopeValues_endpoints`,
`boxEnvelope_endpoints_attained_by_laws`; the envelope identification
`box_convex_envelope`, `box_concave_envelope`; and the coefficient and sandwich
results `boxHullGap_monomial_scale`, `boxTermwiseGap_eq_term_gaps`,
`box_gap_comparison`, `hullGap_sum_le`. The positive affine expansion
(`boxExpansionCoefficient`, `monomial_box_expansion`, `supportPolynomial_box_expansion`,
`boxTermwiseGap_le_expansion`) additionally needs `0 <= l i`, which strict
positivity supplies.

Three things that look reusable are **not**, and must not be assumed:

- `degree_gap_bound_box_transfer` and `degree_gap_bound_on_box` take a premise
  valid at *every* cube point with a degree cap. This topic's cube-level bound
  holds only after normalizing to `[1, rho]^n`, so the constant depends on
  `rho` and the premise shape is wrong. Re-assemble from the pieces instead.
- `positive_polynomial_maximum_general` computes the concave envelope of a
  **cube** monomial `prod Y_i`. This topic needs the physical monomial
  `prod (1 + t Y_i)`, a different objective; the nested-events proof idea
  carries over but the statement must be redone.
- `monomial_minimum` gives the `[0,1]` Frechet envelope `max 0 (sum - (d-1))`.
  The physical convex envelope on `[1, rho]` is
  `rho^floor(S) [1 + (rho-1)(S - floor(S))]`, a different formula.

An obligation is discharged by an actual theorem with the stated hypotheses.
This inventory is not itself a completion claim.

## Conventions fixed for the whole package

- Polynomials are multilinear (squarefree, a `Finset` support) with
  **nonnegative** coefficients; dimension, degree, number of terms, coefficients
  and evaluation points are otherwise unrestricted. Constant and affine terms
  have zero gap and need no exception.
- Boxes are `prod [l i, u i]` with `0 < l i <= u i`. Fixed coordinates
  (`l i = u i`) are permitted and are removed first. `rho > 1` is any real
  bound with `u i <= rho * l i` for every non-fixed `i`; it need not be the
  exact maximum aspect ratio. `rho = 1` is the degenerate zero-gap box.
- `tbtgap` is the sum of the exact concave-minus-convex envelope gaps of the
  individual monomials **including their coefficients**, on the **original**
  box; `chgap` is the envelope gap of the whole polynomial. Both are the
  existing `boxTermwiseGap` and `boxHullGap`.
- Division is total in Lean, and `sSup` of an unbounded or empty set is junk.
  Every supremum statement must be preceded by nonemptiness and boundedness.
- Boundary cases must be included: zero hull gap (the bounds are multiplicative,
  so no division occurs), fixed coordinates, the empty support, dimension zero
  and one, and ties among coordinate means.

## Tier A: classes and semantics

| ID | Required assertion | Source |
|---|---|---|
| PB01 | Define the strictly positive aspect-ratio class and its ratio set: dimension, support, nonnegative coefficients, a box with `0 < l i <= u i` and `u i <= rho * l i`, a point of the box, and a positive hull gap. Prove it nonempty and bounded above before defining `C_box(rho)` as its supremum. | sharp note, definition of `C_box` |
| PB02 | Reconcile the two source definitions: the sharp note's `C_box(rho)` ranges over **all** strictly positive boxes of aspect ratio at most `rho`, while the lower note's ranges over `[1, rho]^n`. Prove the inclusion of the common-aspect class in the general class, so the lower bound transfers. | sharp note; second review, which records this transfer explicitly |
| PB03 | The normalization `x_i = 1 + t u_i` with `t = rho - 1` maps `[0,1]^n` onto `[1, rho]^n`; a physical monomial at a vertex is `(1 + t)^K` where `K` is the success count. | sharp note, normalization |
| PB04 | On a strictly positive box, `0 <= chgap <= tbtgap`, so every ratio is well defined and at least one. Reuse `box_gap_comparison`. | sharp note |

## Tier B: the four rounding laws and their moments

| ID | Required assertion | Source |
|---|---|---|
| PB05 | Common-threshold rounding has the prescribed means and **simultaneously attains the concave envelope of every positive physical monomial**, with the sorted moment formula `C_j(u) = sum_i u_(i) * binom(n-i, j-1)`. | sharp note, envelope facts |
| PB06 | Independent Bernoulli rounding gives `P_j = e_j(u)`, the elementary symmetric polynomial. Reuse `bernoulliLaw_expect_prod`. | proof note |
| PB07 | The **fair endpoint-orientation law** — one uniform variable plus `n` independent fair coins — has the prescribed means, and its moments `O_j` are well defined. The law `orientationLaw` exists; its general-cardinality moments do not. | proof note |
| PB08 | `2 O_2 = C_2 + L_2` where `L_2 = sum_{a<b} max(0, u_a + u_b - 1)`. | proof note, order two |
| PB09 | `O_j` is coordinatewise nondecreasing with coordinate Lipschitz constant `binom(n-1, j-1)`, proved by coupling with the same uniform variable and the same orientation coins. **A derivative argument is not admissible**: the sources record twice that the partial derivatives need not exist on an orientation breakpoint. | proof note; first review |
| PB10 | Slab integrality: the polytope `{y in [0,1]^n : floor S <= sum y_i <= ceil S}` is integral and contains `u`, so an adjacent-count law with means `u` exists. | proof note |
| PB11 | Discrete convexity of `k |-> binom(k, j)` for `j >= 2` and of `k |-> (1+t)^k` for `t > 0`, hence `V_j = (1-theta) binom(k,j) + theta binom(k+1,j)` is the **minimum** moment and `V(t) = sum_j V_j t^j` is the **exact** convex envelope `rho^floor(S) [1 + (rho-1)(S - floor(S))]` of the physical product. Exactness is essential; a mere lower bound collapses the theorem. | proof note; first review |
| PB12 | Uniform moment conventions across all four families: order zero is one, negative orders are zero, orders above the dimension vanish. | proof note |

## Tier C: the coefficient inequality

| ID | Required assertion | Source |
|---|---|---|
| PB13 | Define `F_{n,j} = 2 C_j + V_j - P_j - 2 O_j + C_{j-1} - P_{j-1}` and prove `F_{n,0} = F_{n,1} = 0`. | proof note, equation (1) |
| PB14 | `F_{n,n+1} = C_n - P_n >= 0`, and orders above `n+1` vanish. | proof note |
| PB15 | `F_{n,2} = (C_2 - P_2) + (V_2 - L_2) >= 0`, from PB08, the pairwise Frechet upper bound, and the pairwise Frechet lower bound. | proof note, equation (2) |
| PB16 | Boundary recursions `F_{n,j}(u, 0) = F_{n-1,j}(u)` and `F_{n,j}(u, 1) = F_{n-1,j}(u) + F_{n-1,j-1}(u)`, for all four moment families under the PB12 conventions. | proof note, (3) and (4) |
| PB17 | The spreading step for `3 <= j <= n` at interior `u`: moving a **global minimum** `x` and a **global maximum** `y` to `x - h`, `y + h` with `0 <= h <= min(x, 1-y)` does not increase `F_{n,j}`, via the exact changes in `2C_j + C_{j-1}` and `P_j + P_{j-1}` and the Lipschitz bound of PB09. The hypothesis cannot be weakened to arbitrary mean-preserving spreading: `F` is **not** Schur-concave, and the sources give an explicit four-variable counterexample. Ties must be handled. | proof note, (5) and (6); the counterexample is recorded there |
| PB18 | **`F_{n,j} >= 0` for every `n`, `j` and `u`**, by induction using PB14-PB17. | proof note |

## Tier D: the common-aspect bound

| ID | Required assertion | Source |
|---|---|---|
| PB19 | The coefficient of `t^j` in `(2+t) C + V - (1+t) P - 2 O` is exactly `F_{n,j}`, with no lost top-degree term. | proof note |
| PB20 | `C - V <= rho (C - P) + 2 (C - O)` for every physical monomial and every `u`. | proof note, (7) |
| PB21 | The mixture of independent rounding with weight `rho/(rho+2)` and orientation rounding with weight `2/(rho+2)` is **one law on all coordinates**, independent of the support and the coefficients, capturing at least `1/(rho+2)` of every physical monomial's gap simultaneously. | sharp note |
| PB22 | `tbtgap <= (rho + 2) chgap` on `[1, rho]^n`, and the specialization to `4` on `[1,2]^n`. | sharp note, (8) |

## Tier E: original-box transfer and interpretation

| ID | Required assertion | Source |
|---|---|---|
| PB23 | With `s_i = (u_i/l_i - 1)/(rho - 1)` in `(0,1]` and `z_i = l_i[(1 - s_i) + s_i x_i]`, the map is an affine bijection `[1,rho]^n -> prod [l_i, u_i]`, and each original monomial expands with nonnegative coefficients. | sharp note, transfer |
| PB24 | `chgap` is invariant under that bijection, and `tbtgap_original <= tbtgap_expanded`, since a concave envelope of a sum is at most the sum of concave envelopes and dually. | sharp note |
| PB25 | `tbtgap_B f <= (rho + 2) chgap_B f` on every strictly positive box with aspect ratios at most `rho`, after removing fixed coordinates. | sharp note |
| PB26 | **The interpretation.** The expansion is a proof device only. The pulled-back laws are the same endpoint laws in the original coordinates; common-threshold rounding attains all expanded positive monomials simultaneously, so each **original** monomial's deficiency **equals** the sum of its expanded deficiencies, and the per-monomial guarantee holds in the original coordinates without forming the expansion. This is explicitly **not** an argument by box inclusion. | sharp note, interpretation paragraph; first review |

## Tier F: the finite-dimensional refinement

| ID | Required assertion | Source |
|---|---|---|
| PB27 | Define `p_N = 2 floor(N/2) ceil(N/2) / (N(N-1))` and `beta_N = 1/p_N`, and prove the closed form `beta_N = 2 - 2/N` for even `N` and `2 - 2/(N+1)` for odd `N`. | closure note |
| PB28 | The **balanced ambient orientation law** — a uniform subset `H` of size `floor(N/2)`, independent of one uniform variable — has the prescribed means, and every distinct pair has opposite orientations with probability exactly `p_N`. That probability is **unchanged under restriction to any subset of coordinates**. Fairness of individual orientations is not required and fails for odd `N`. | closure note |
| PB29 | `O_2 = (1 - p_N) C_2 + p_N L_2`, and `beta_N p_N = 1` gives the same base case as PB15. | closure note |
| PB30 | `F_{S,j} = beta_N C_j + V_j - P_j - beta_N O_j + C_{j-1} - P_{j-1} >= 0` for every support `S`, with the **same** `beta_N`, under restrictions of the **same ambient law** — never resampled in the smaller dimension. Deleting a deterministic coordinate must not condition on its orientation coin. | closure note |
| PB31 | `tbtgap f <= (rho + beta_N) chgap f` on `N`-dimensional strictly positive boxes, including the unequal-box transfer, with mixture weights `rho/(rho + beta_N)` and `beta_N/(rho + beta_N)`. Dimensions zero and one have zero gaps. | closure note |

## Tier G: the lower bound

| ID | Required assertion | Source |
|---|---|---|
| PB32 | Define the variable-radix family: `eps = 1/rho`, `L >= 2`, `b = L^2`, `m = b^L`, nested partitions of the leaves into `b^j` equal blocks, `p(a,z) = sum_j sum_{B in P_j} a_j prod_{i in B} z_i`, variables in `[eps, 1]`, normalized means `u_j = b^{-j}` for anchors and `1 - 1/m` for leaves, all strictly interior. | lower note |
| PB33 | Each term's exact convex-envelope value is `eps`, by Jensen (`E eps^R >= eps` when `E R = 1`) together with the attaining one-failed-coordinate categorical law. | lower note |
| PB34 | Each term's exact concave value is `eps + (1-eps) u_j - (eps/m)(1 - eps^k)`. | lower note |
| PB35 | The exact termwise gap `T_L = (1-eps) L - D_L` with `D_L = eps sum_t (1 - eps^{b^t})/b^t`, and `0 <= D_L <= eps b/(b-1)`. | lower note, (2) and (3) |
| PB36 | The exact hull-gap identity as a maximum over binary laws with the stated marginals. | lower note, (4) |
| PB37 | **The imported unit-box bound.** `max E sum_j A_j N_j = 1 + (L-1)/b` for `b >= L`, of which only the upper direction is needed. This result belongs to the still-deferred topic 19 and has **no Lean coverage**; the lower bound is not a theorem without it, so it is an obligation of this package. Its proof is a rearrangement argument over joint laws with prescribed marginals. | `positive-multilinear-incidence-sharp-growth.md`, imported by the lower note |
| PB38 | The hull-gap upper bound `H_L <= eps(1-eps) L + (1-eps)[1 + (L-1)/b] - D_L`, using `1 - eps^{R_B} <= 1` on a nonempty block and `1 - eps^r <= (1-eps) r`. | lower note, (5) |
| PB39 | The hull-gap lower bound `H_L >= eps(1-eps) L + (1-eps)^2 sum_j b^{-j} - D_L`, from the law choosing exactly one uniformly random failed leaf, under which each level contributes `1 - eps` deterministically. | lower note, (6) |
| PB40 | Finite positivity `H_L > 0` for every finite `L`, needed before any ratio is formed. | lower note |
| PB41 | The limits `H_L/L -> eps(1-eps)` and `T_L/H_L -> rho` for each fixed `eps` in `(0,1)`, with no interchange of the `L` and `rho` limits. | lower note, (7) |
| PB42 | Scaling by `rho` maps `[1/rho, 1]` to `[1, rho]`, giving a degree-`d` term the positive coefficient `rho^{-d}` and preserving both gaps exactly. | lower note |
| PB43 | `C_box(rho) >= rho` for every `rho > 1`. | lower note, (1) |
| PB44 | `C_box(rho) >= 2`: the complete positive bilinear graph at normalized means one half has ratio `2(n-1)/n`, tending to two, and positive affine scaling to any nondegenerate box leaves the ratio unchanged. | lower note |

## Tier H: the headline

| ID | Required assertion | Source |
|---|---|---|
| PB45 | `max{2, rho} <= C_box(rho) <= rho + 2` for every `rho > 1`, using the class reconciliation of PB02. | sharp note |
| PB46 | `C_box(rho) = rho + O(1)` as `rho -> infinity`, and `C_box(2) <= 4`. **Explicitly not claimed:** that either endpoint is the exact value at any fixed `rho`. | sharp note |

## Explicit exclusions

- The superseded predecessor bound `4R + 6 + 2/R` of
  [`positive-multilinear-positive-box.md`](../../../results/positive-multilinear-positive-box.md),
  together with its `K(rho)` constant, its `g_rho` variant, its low/high split
  and its two high-group estimates. Every one of its conclusions is strictly
  weaker than `rho + 2` — it gives `45/2` on `[1,2]^n` where the sharp theorem
  gives `4` — and the sharp theorem covers every `rho > 1`, so nothing depends
  on it. Its retention in the sources is documentary. The one ingredient that
  **is** carried forward is the physical convex-envelope formula, which appears
  here as PB11.
- The asymmetric predecessor of
  [`positive-box-asymmetric-upper-predecessor.md`](../../../notes/positive-box-asymmetric-upper-predecessor.md),
  which the sharp note explicitly replaces.
- Optimality of the constant `1/(rho+2)` beyond what the sources prove: it is
  optimal only among fixed mixtures of these two laws with a uniform
  per-monomial guarantee, and neither obstruction gives a matching lower bound
  for the true polynomial ratio. No exact value of `C_box(rho)` is claimed.
- Machine-level bit-complexity claims. As in topics 3, 16 and 17, the verified
  content of a constructive claim is its correctness and its exact size
  recursions; no counted bit-cost model is claimed. Every such assertion must be
  mapped in `COVERAGE.md` to a Lean statement or to this exclusion, with reason.
- Novelty and bibliographic priority. The sources credit the physical
  convex-envelope formula and the elementary-symmetric envelope as classical,
  and seek novelty only in the coefficient inequality and its
  dimension-independent comparison.
