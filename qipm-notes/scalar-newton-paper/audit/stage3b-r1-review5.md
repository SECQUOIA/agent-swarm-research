# Stage 3b, round 1: independent reviewer 5

Verdict: no major mathematical issues found. One minor audit/source-routing
issue should be corrected. I did not edit the manuscript or read another
reviewer's report. The parent separately raised the source-routing assertion;
I checked the assertion rather than treating it as established.

## Numbered findings

1. **Minor — unsupported description of where excluded notes are already
   covered.** In `audit/stage3b-author.md`, the Source routing paragraph says
   the one-Lorentz counting and simplex/search constructions are independent
   programs “already covered by broader manuscripts.” The corresponding
   `audit/source-map.md` rows 40–41 make similar claims. The manuscript paths
   and exact results establishing that coverage are not supplied. Searches of
   the broader central-path and conic-lift section files find related themes,
   which do not by themselves establish that these particular constructions
   are already incorporated. Their exclusion can reasonably rest on the
   stated scope distinction: separate approximate-counting/search optimization
   constructions versus the inverse-observable and reuse results in this
   paper. **Fix:** remove the unsupported already-covered assertion, or give
   exact manuscript sections and explain which results they contain. Preserve
   the narrower, verifiable statement that the relevant access/output lessons
   are represented here. This does not affect a manuscript theorem.

Major findings: none. Additional minor mathematical findings: none.

## Mathematics and interfaces checked

- **Classical direct sum.** The random target block is independent of the
  assembled product-distribution input, hence of its transcript, even when
  query indices are adaptive. Public nonuniform block-sampling probabilities
  do not invalidate the expected `O(Q/B)` target cost. The minimax threshold
  and truncation constants are consistent: `2/3 - 1/12 = 7/12 > 9/16`.
  Worst-case amplification is used to choose a hard distribution, rather
  than incorrectly amplifying an average distributional success rate.
- **LP increments.** I checked the central equation, telescoping kernel,
  leakage bound, decoding constants, distinct Boolean and numerical coherent
  output contracts, and the strong-convexity approximate-centering transfer.
  The `sqrt(BK tau_ctr)` readout error uses the full product vector and is
  consistent with the Section 7 readout normalization. Fixed-order source
  promises need a smaller numerical error; the text does not extend the
  Boolean representative argument beyond its justified range.
- **SOCP trajectory.** The radial inverse-Hessian calculation gives
  `2 sigma^2 r^2/(1+r^2)`, which equals the displayed `sigma^2 f` term.
  The derivative lower/upper bounds, two geometric tail sums, constants at
  `Gamma >= 256`, and the looser midpoint-output constants at `2^20` are
  consistent. `G = Theta(sqrt(K))` gives the stated accuracy scale. The
  dynamic norm corollary uses a genuine promise gap larger than twice its
  output tolerance, and explicitly charges the stronger iterate interface.
- **Threshold/XOR compiler.** I verified uniqueness in both threshold
  branches, the objective-gap bound at arbitrary feasible points, all eight
  block inequalities, the XOR projection and stability induction, strict
  relative feasibility, and the `12B-4` certified log-barrier parameter.
  The equality lift is linear and keeps sparse incidence. Public readout
  rounding remains below the original upper threshold margin; narrowing the
  half-gap repairs high-branch saturation. The full-SQ mixtures have public
  weights and the coherent parity restriction has constant simulation cost.
- **Parity endpoint and temporal interpretation.** The endpoint, increment,
  objective-gap and unnormalized-sum error bounds agree with the stated
  central path. The text correctly distinguishes a final composition lower
  bound from an unavoidable chronological charge at every path scale.
- **Fixed KKT ray and signed-tree witness.** I checked the differentiated
  KKT equations, the public diagonal radial Hessian, constant-probability
  extraction of the inverse state, the norm/condition estimates for the
  signed tree, and the width-three bags. The bounded-Dikin chord estimate
  follows from the two affine logarithmic factors along a ball chord. Its
  iteration conclusion is properly limited to the stated movement model.
  A stored inverse vector or one fixed scalar estimate supplies the entire
  subsequent ray family without further input queries.
- **Approximate checkpoint volume.** Rejection implies exact distance greater
  than `eta/(2B0)` and approximate-column distance greater than `Delta`.
  Normalized columns give the first QR diagonal exactly one and the remaining
  diagonals greater than `Delta`. The upper singular-value product is at
  most `(2r)^r (d_r+xi+epsilon)^r`; this contradicts the lower volume under
  the exact displayed width hypothesis. Normalization is essential and is
  included. The acceptance and rejection inequalities are both valid with
  the two `eta/8` errors.
- **Stable adaptive refinement.** The coefficient bound is imposed on exact
  versions of the checkpoints actually selected, not an unrelated final
  basis. Replacing those vectors gives residual at most `B0 Lambda xi`, so
  dependent rays cannot trigger a rejection at the stated threshold. The
  resulting at-most-r argument is valid despite approximate stored rays.
- **Analytic width and strict-complementarity boundary.** Summing the vector
  Chebyshev coefficient tail gives the displayed exponent and denominator.
  Distinct QP branch points prove linear independence. For `c2=2c1`, the
  normalized predictor coordinate squared has a nonremovable pole at
  `-(c1^2+c2^2)/8`, so strict complementarity cannot give a uniform ellipse
  for this family. The conclusion does not assert that every such family has
  large numerical rank at every fixed accuracy.
- **Certification and explicit output.** The unique-search residual is
  exactly zero or `1/sqrt(2)` under the stated coefficient interface. Free
  RHS norms would destroy that reduction and are explicitly excluded. The
  canonical-bit-oracle dense-output proof works for approximate recovery:
  coordinate rounding gives at most `D/16` mistakes; the multilinear state
  expansion has span dimension at most `sum_{j<=Q} binom(D,j)`; the POVM
  trace bound multiplies this dimension by the Hamming-ball volume. A
  sufficiently small constant fraction of D queries gives exponentially
  small success, establishing the claimed Omega(D) quantum lower bound.

## Literature and validation

Primary sources checked online:

- [Brody et al., A Strong XOR Lemma for Randomized Query Complexity](https://theoryofcomputing.org/articles/v019a011/):
  the theorem covers partial Boolean functions and expected randomized query
  cost, matching the application. The manuscript's truncation comparison
  supplies the worst-case bounded-error lower bound it needs.
- [Buhrman et al., Robust Polynomials and Quantum Algorithms](https://homepages.cwi.nl/~rdewolf/publ/qc/robust_journal.pdf):
  the coherent subroutine model and Corollary 3 support joint recovery using
  linear total source queries. They do not give arbitrary real estimates;
  the manuscript respects that distinction.
- [Beals et al., Quantum Lower Bounds by Polynomials](https://arxiv.org/abs/quant-ph/9802049):
  polynomial-method input dependence supports both parity and the stated
  multilinear-span argument.
- [Parks et al., Recycling Krylov Subspaces for Sequences of Linear Systems](https://vtechworks.lib.vt.edu/items/590c07fe-a0c8-49b2-9494-be5061f5fbf7):
  attribution of the underlying subspace-recycling idea is appropriate.

The manuscript also attributes reduced-basis ideas to Binev et al. rather
than claiming recycling or greedy approximation itself as new. Its qualified
Section 8 contribution statement isolates sparse realizations, quantitative
kernels and output contracts from the prior query-complexity ingredients.

I ran
`/home/sgusev/miniconda3/envs/qipm/bin/python notes/scalar-newton-paper/checks/check_temporal_identities.py`.
It passed all kernel, threshold/XOR, sparse-KKT and rank/volume diagnostics.
These checks supplement the analytic verification above.
