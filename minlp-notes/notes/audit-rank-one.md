# Independent audit of the row-and-column rank-one results

Audit date: 2026-09-04. Auditor: an independent agent assigned by the coordinating agent.
This is an agent proof review, not external peer review or a guarantee of novelty.
The reviewed file is `results/rank-one-row-column-hardness.md`.

## Verdict

The biclique reduction in Theorem 1 is correct. It proves the exact hardness conjecture stated
by Dey, Kocuk and Santana after their Theorem 4. The fixed-dimension algorithm is correct after
clarifying stationary-point signs, endpoint cases, and bit complexity. Its stated running time
can be strengthened to fixed-parameter tractability in the smaller matrix dimension.
The main mathematical claims survived review; several supporting claims required correction.

Corollary 2, giving NP membership and polynomial-length quadratic encodings of exact optima,
was developed by this auditor during review. The independent reviewer
`review_scaling_characterization` subsequently verified it and Theorem 2, and strengthened
the decision certificate to use only rational numbers. That strengthening was checked in turn
by this auditor. See `notes/review-rank-one-certificates.md` for the second review.

## Proof checks

- **Margin parametrization.** A nonzero nonnegative rank-one matrix has nonnegative factors.
  Summing the factors proves `W=rcᵀ/S`; the converse preserves both margins exactly. Finite
  nonnegative bounds make the matrix set compact. If zero is feasible, the objective tends to
  zero as `S` tends to zero because `|⟨C,W⟩|≤||C||∞ S`.
- **Biclique source problem.** Peeters proves maximum-edge biclique NP-complete for bipartite
  graphs. The size threshold is bounded by the number of graph edges, so the reduction does
  not hide large numerical input. Balanced biclique and maximum-vertex biclique are different
  problems and must not be substituted without justification.
- **Dummies.** For arbitrary `x,y` in their unit boxes, the difference between their sums lies
  in `[-n,n]`. The two dummy blocks realize any correction in this interval. The denominator
  stays positive because of the fixed unit row and column.
- **Rounding.** Sequential minimization in `x`, then `y`, replaces any feasible point by a
  binary one with no larger numerator. This argument applies to the numerator threshold,
  not to minimization of the ratio itself.
- **Penalty and gap.** A binary pair selecting a nonedge has `Q≥n²−(pq−1)≥1`. A biclique gives
  `Q=−|A||B|`. In a no instance every binary numerator is at least one; the sequential rounding
  argument implies the same bound throughout the continuous box. Since `S≤2n+1`, the actual
  ratio has gap at least `1/(2n+1)` from the yes threshold zero.
- **PARTITION alternative.** The claimed expression is correct for the now-explicit cost
  matrix. Vanishing of every `r_i(a_i−c_i)` gives `c_i≥r_i`; equal totals then force equality
  coordinatewise and hence binary choices of the full capacities. This missing step has been
  supplied. The integer-data version now fixes the multiplier to one; arbitrary real positive
  multipliers would not themselves be rational input or become integers after scaling by four.
- **Hull corollary.** The reduction rules out a uniformly polynomial-time construction of an
  exact compact formulation with polynomial-time optimization guarantees. Conic optimization
  requires those guarantees, including whatever conditioning assumptions its solver needs.
  Existence of small nonconstructible formulations is not addressed. The old absolute-error
  choice was half the gap and allowed equality ambiguity; it is now one quarter of the gap.
- **Fixed-dimension algorithm.** Box/hyperplane vertices have at most one free coordinate.
  There are at most `m 2^(m−1)` patterns. Along each pattern the `N` affine weights have
  `O(N²)` crossing points, and each fixed order has `O(N)` greedy filling intervals. This gives
  `O(N³)` intervals per pattern, with exponent independent of `m`.
- **Stationary points.** An interior minimum of `αS+β+γ/S` uses `α,γ>0` and value
  `β+2sqrt(αγ)`. If both coefficients are negative, the stationary point is a maximum and the
  corresponding value has the opposite radical sign. The old blanket formula was inaccurate;
  the algorithm now checks only interior minima and the necessary endpoint/constant cases.
- **Exact bit model.** Breakpoints are ratios of affine coefficients, and greedy breakpoints
  are sums of rational capacities. All have polynomial bit length. The final arithmetic uses
  at most one radical per candidate; comparing two candidates uses sign-aware squaring and
  degree at most four. The output is an exact algebraic encoding, not a promise that the
  optimum is rational. Empty and zero-only feasible intervals are now explicit.

## Scope and claims corrected

The word "refereed" was replaced with independent-agent review. The published Jalilian–Kocuk
article is in Optimization and Engineering 27:317–367 (2026), with online publication in 2025.
The `2×2` hull is not necessarily nonpolyhedral for every bound choice; some degenerate choices
are singletons, so the description now says it need not be polyhedral.

The practical implication is about exact general-cost block optimization and hull construction.
It does not say all cutting-plane or SOC methods are necessarily incomplete: exponential-size
exact SOC formulations already exist, and a cutting-plane method can perform exponential work.
Nor does it justify removing or declining to jointly convexify valid flow bounds.

For additive path costs `C_ij=a_i+b_j`, the objective reduces to `aᵀr+bᵀc`; the quality-free
single-pool block is then an LP. Hardness requires the richer objective class used by the
reduction. This is relevant to convexification subproblems, but not a proof that the usual
quality-free pooling model with arc-additive operating costs is hard. Existing bounded-input
pooling algorithms are credited explicitly.

## Literature check

Primary sources inspected or located:

1. [Dey, Kocuk and Santana author manuscript](https://www2.isye.gatech.edu/~sdey30/RankonePool.pdf),
   Section 3.1, immediately after Theorem 4: the precise intersection-of-row-and-column-bounds
   optimization conjecture. The corresponding [arXiv record](https://arxiv.org/abs/1902.00739)
   describes the general rank-one framework.
2. [Jalilian and Kocuk, published article](https://doi.org/10.1007/s11081-025-09997-6): Section 2
   states SOC representability with exponential size and motivates compact outer approximations.
   The [arXiv record](https://arxiv.org/abs/2306.10810) confirms the row, column, and total-sum scope.
3. [Peeters (2003)](https://doi.org/10.1016/S0166-218X(03)00333-0): NP-completeness of maximum-edge
   biclique in bipartite graphs.
4. [Boland, Kalinowski and Rigterink](https://arxiv.org/abs/1508.03181): polynomial-time
   single-pool optimization with bounded inputs in their pooling model.
5. [Haugland and Hendrix](https://doi.org/10.1007/s10957-016-0890-5): established polynomial-time
   pooling cases, including bounded source count for a single pool.

Targeted searches included:

- `Dey Kocuk Santana rank one row column bounds conjecture NP hard resolved`
- `"rank-one" "row" "column" "NP-hard" Kocuk`
- `"rank-one" "conjecture" "Santana"`
- `"rank-one" "row and column" "hardness"`
- `"rank-one" "row sums" "NP-hard"`
- `"rank-one" "column sums" conjecture complexity`
- `"A study of rank-one sets" hardness conjecture resolved`

No prior resolution of the exact conjecture appeared in the inspected results. This is
provisional evidence of novelty, not exhaustive coverage of unpublished work, inaccessible
articles, or differently phrased equivalent results. The bilinear biclique encoding is an
established type of reduction; its novelty claim is specifically the transfer to this set.

## Computational evidence limitation

The existing Gurobi script is a numerical sanity check, not a proof certificate. In particular,
it accepts a time-limit status and then compares the incumbent objective with a threshold.
An incumbent above a threshold does not certify a no instance without a corresponding lower
bound. The recorded small examples are useful for catching construction mistakes, but the
mathematical proof, not solver status or tolerance, establishes the result. The PARTITION
threshold has no proved uniform gap in the existing note. No new numerical claim is made by
this audit.

## Independent check of the coordinating agent's zero-lower-bound draft

The draft at `/tmp/zero_lower_draft.txt` was checked independently during this audit. For the
unit-upper-bound rank-one set `K` and its subset `F` with `r_0=c_0=1`, the draft proves
`dist_1(W,F)≤2(2−r_0−c_0)`. The proof is correct:

- For `S≥1`, raise the distinguished margins to one and decrease the other entries by the
  same amounts. Donor totals suffice because `S−r_0≥1−r_0` and similarly for columns. The
  rank-one product difference is bounded by the sum of the two margin differences in entrywise
  one-norm, which is twice the total distinguished-margin deficit.
- For `0<S<1`, use `E_00`. Since `(S−r_0)(S−c_0)≥0`, one has
  `W_00=r_0c_0/S≥r_0+c_0−S`, and
  `||W−E_00||_1=1+S−2W_00≤1+3S−2r_0−2c_0≤2(2−r_0−c_0)`.
  The zero matrix is immediate.

Consequently any `L>2||C||∞` strictly improves every point outside `F` when minimizing
`⟨C,W⟩−L(r_0+c_0)`, by at least `(L−2||C||∞)(2−r_0−c_0)` after repair. This transfers the
existing hardness reduction to zero lower bounds and unit upper bounds, with integer penalty
`L=2||C||∞+1` and shifted threshold `−2L`. The coordinating agent owns the resulting theorem
and its final presentation; this paragraph records the independently verified argument.
