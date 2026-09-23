# Stage 3 independent review 1

Date: 2026-09-13. Reviewer: `/root/stage03_review1`.

## Verdict

**No MAJOR issue found. Two MINOR wording corrections are requested.** The trace approximation theorem, exact feasibility extension, rational complexity proof, and individual-channel hardness reduction are sound under the stated promises. I also reconstructed the normalization and signed-profile cover proofs and found no theorem-level defect. This is a Stage 3 review, not acceptance of the deliberately unfinished later manuscript stages.

I read `sections/03-approximation.tex`, `appendices/approximation.tex`, the relevant accepted locality definitions and the coverage inventory. I did not read other review reports or edit the manuscript. Independent checks and source excerpts are confined to `verification/stage03-review1/`.

## Findings

### MINOR 1 — Distinguish scalar observations from a scalar parameter in the predecessor reduction

Location: `appendices/approximation.tex:53–67`, especially “Take the scalar class of Theorem...” at line 53; related scope discussion at `sections/03-approximation.tex:174–188`.

Theorem `thm:trace-fptas` deliberately allows input-sized parameter dimension even in its scalar-observation class. The appendix instead uses scalar sensitivities `f_t`, a scalar normalization `h`, and a single Gaussian target. Its reduction is correct for **p = 1**, but that restriction should be explicit before the formulas. The distinction matters because the manuscript correctly explains later that growing target rank is not covered by the bounded-width predecessor argument.

Fix: Begin the appendix construction with “Take the scalar-observation class ... with one parameter (p = 1), cardinality only, ...”. A scalar nonnegative trace weight can be suppressed; if desired, state that zero weight is trivial and positive weight does not change the maximizing schedule. This is a scope clarification, not a defective proof or an invalid main theorem.

### MINOR 2 — Use version-neutral wording for the cited preprint theorem

Location: `appendices/approximation.tex:32`, “not the wording of the published theorem.”

The actual bibliography item `Mahalanabis2012` is the 2012 arXiv preprint, and the inspected source is that original. Avoid an incidental suggestion that this reference was checked in a journal-published version.

Fix: Replace “published theorem” with “stated theorem” or “theorem as printed in the cited preprint.” This does not affect the mathematical comparison.

## Independent proof assessment

- **Uniform envelopes:** The scalar/full-block envelope follows by replacing the gain by one and the final geometric numerator by one. The partial-packet envelope is rational because `sqrt(kappa_0 s_0) <= s_0`. For general decay, invoking the accepted result with larger fixed decay and floor-ratio promises is sufficient; componentwise monotonicity of its derived constants need not be asserted. Zero-contraction/signal and complete-history cases are separately handled.
- **Window and runtime:** If the chosen window is positive, the previous window failed, yielding `beta^L > epsilon/(2 C_0)` and the displayed polynomial bound on `2^L`, including the finite-history cap. The path graph, rational principal solves, and exact path comparisons have polynomial bit cost. Explicit matrix encoding makes the dimension dependence credible, and no algorithmic whitening square root is required.
- **Trace conversion:** Congruence and `W >= 0` preserve the locality sandwich after taking weighted trace. Adding the common PSD prior preserves the same factors. The ratio `(1-delta)/(1+delta) >= 1-epsilon` follows at `delta <= epsilon/2`, including zero optimum without division.
- **Spacing:** The cooldown is measured before each decision. Setting it to `g-1` after selection forbids exactly the next `g-1` calendar times. Clamping an enormous encoded gap to `n+1` preserves the at-most-singleton family. The independent count avoids either relaxing cardinality or requiring information memory `L >= g`. Mandatory/forbidden conflicts are detected by reachability.
- **Hardness:** On maximum-degree-three graphs, the latent/noise split has eigenvalues `P in [1/12,7/12]`, `V=2I/3`, hence `P <= (7/8)V`, and covariance condition number at most `5/3`. The infinity-norm Neumann bound implies every component of `R_SS^{-1}1` is at least `2/3`; a selected edge loses at least `1/9` in scalar information. The claimed FPTAS accuracy allows loss at most `1/18`. This is a valid decision reduction and does not conflict with complete-packet selection.
- **Scalar predecessor:** The dyadic normalization bounds observation noise and sensitivities despite arbitrary initial scales. Adding rational innovation variance yields a Markov SPD latent covariance with the claimed lower and upper spectral bounds. The shear condition estimate and the positive lower bound from one sensitivity-normalized observation give polynomial conditioning and a valid variance-to-information conversion. Keeping the target in all separators until its singleton bag avoids evaluating a nonzero local cost in the source's inverse/principal-block mismatch. The manuscript appropriately distinguishes this adaptation from a fully rational implementation of the predecessor's spectral rounding net.
- **Broader Stage 3:** Maximum-volume factor selection is used only for the coverage proof, not as an algorithmic oracle. Rational dyadic normalization gives a forced floor and exact ranges, and signed floor-profile equality bounds matrix error even for variable-length paths. The rank-preserving matroid contraction, noncancelling squared-minor polynomial, exact interpolation, and deletion recovery provide actual original bases. Growing matrix dimension is correctly excluded from the fixed-p spectral polynomial assertion.

## Primary-source checks

Read `literature/AGENTS.md` before source work.

1. Inspected the actual local Mahalanabis–Stefankovic original PDF, including extracted original pages 12–18 and 37–38, alongside its local full text. Theorem 43 on printed p.37 has the stated condition-number-dependent operation bound and relative conditional-variance guarantee. The message definitions and local cost at pp.16–18 support the adaptation discussion. The source itself also has incidental boundary notation problems, so the appendix's explicit singleton/empty-root construction is preferable to copying the last proof paragraph literally.
2. Verified Mohar's actual author-hosted primary PDF, Theorem 4.1(a), PDF p.10 / printed p.10. It establishes NP-hardness of maximum independent set even for 2-connected cubic planar graphs, which is stronger than the restriction used here. Source: [Mohar, Face Covers and the Genus Problem for Apex Graphs](https://users.fmf.uni-lj.si/mohar/Reprints/2001/BM01_JCT82_Mohar_ApexGraphs.pdf).

## Independent exact checks

Ran:

```text
code/research_20260912/.venv/bin/python paper-correlated-measurements/verification/stage03-review1/check.py
```

All passed. The script is independent of the production and author verification code.

- 76,545 exact dynamic-programming versus exhaustive-enumeration comparisons on a six-time calendar: all ternary mandatory/forbidden/free assignments, every cardinality, history lengths 0/1/2, gaps 1/2/3/7 and `10^30`. The history-dependent objective prevents this from being solely a reachability test.
- Three independently assembled rational covariance fixtures: signed scalar chain, two-channel full packets with rotating transitions, and alternating partial observations of a two-state chain. All 64 schedules were evaluated by direct selected-covariance inversion and separately by local conditional increments. For each fixture, 35 feasible combinations of gap/cardinality/restrictions were checked against exact optimization; the DP maximized the surrogate and met the true trace guarantee. The selected true ratios happened to be one in these small fixtures, so these are correctness checks, not empirical evidence about nonzero approximation error or large-instance runtime.
- All 63 nonempty subsets of a triangular-prism cubic graph, using exact rational inverses, satisfy the independent-set value and `1/9` separation claimed in the hardness proof.

Results: `verification/stage03-review1/results.json`. No historical result was overwritten.
