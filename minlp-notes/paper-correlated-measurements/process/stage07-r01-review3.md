# Final whole-manuscript review 3

**Assessment: no major or minor correction requests.** The frozen manuscript's certificate theory is mathematically consistent under its stated assumptions. I recommend acceptance of this review gate. This is an internal independent review, not external peer review or a guarantee about unknown errors.

## Read scope and integrity

I read the entire manuscript source: the abstract and introduction, all six subsequent main sections, all four appendix source files, `main.tex`, `macros.tex`, and the full bibliography. I also read the paper README, standalone supplement README and source-kinetics README. I considered the overall argument from statistical specification through locality, approximation, certificates, empirical evidence and conclusion. I did not use earlier author/reviewer reports as evidence of correctness.

The built document is 66 pages. Its existing log has no matches for `Warning`, `Overfull`, `Underfull`, `undefined` or `Citation`. A rendered inspection of page 29 confirms legible certificate mathematics, normal margins and unbroken content. This was a targeted visual inspection, not a page-by-page visual audit. All **204** files in `process/stage07-r01-freeze.json` matched their recorded SHA-256 hashes at the end of my checks. No frozen source or result file was changed.

## Certificate theory examined

1. **Local support and rational arithmetic.** I re-derived the prior-aware upper matrix from the residual sandwich, the logdet tangent and efficiency ratio. Inflating only the PSD data term is justified. Real-valued theorems and the rational checker's more restrictive representation are distinguished correctly. Replacing a possibly irrational analytic error by a rational upper enclosure below one preserves the inequality. The logarithm series, remainder, negative binary exponent endpoint reversal, signed interval products, variance denominator powers and the nonnegative clamp are correct. The score increment statement charges the actual maximum number of scored innovations and handles zero selections.

2. **Virtual noise.** The support covariance formula correctly omits zero coordinates. The resolvent is invertible even with a singular PSD split remainder, and the positive-remainder limit preserves matrix concavity. Differentiating the resolvent produces the displayed outer-product derivative, including at zero and one visits. The positive prior gives a neighborhood on which the objective remains differentiable. The continuous support certificate distinguishes query feasibility from lower-bound feasibility and prices a specified convex set contained in the cube.

3. **Dense evaluation.** I checked the tridiagonal congruence and the direction of the first-nonpositive-pivot witness. The covariance innovations describe precisely the same virtual covariance, with no infinity at zero visits. Reverse differentiation gives both recurrence factors and their signs; cancellation of a positive visit and continuity at zero are valid. The `a/q <= 1` argument uses the actual prediction variance and added nonnegative virtual noise. The discussion avoids turning this bounded factor into a complete floating-point stability theorem, and separates the algebraically correct but unstable RTS subtraction from the precision-space conditioning issue.

4. **All-split comparisons.** The Hessian proof for the fixed-point inverse-logdet function is correct for indefinite symmetric perturbations: the Kronecker difference is PSD. With `w = -g >= 0`, the two inequalities `w^T a <= tr(DY) <= tr(RY)` have the correct signs. An inadmissible positive reference is allowed because this proof uses convexity in the positive virtual covariance, rather than concavity of an inadmissible split. The factor repair is a valid rational PSD construction. The same feasible fractional point survives all the specified affine upper supports. The manuscript explicitly excludes branching, extra restrictions and unrelated cuts. The scalar upper spectral witness is evaluated in the positive selected virtual covariance and does not invoke an invalid extension of split concavity.

5. **Robust design.** I checked the common-schedule support, exact simplex normalization, both inequalities for unknown optimal standardizers and the valid zero cap. Individual feasible lower normalizers must refer to the same feasible family, as stated. In the fixed-scenario approximation proof, the block-diagonal cover returns one common schedule, and the two factors of `a` follow respectively from target coverage and normalizer uncertainty. The rational determinant comparison avoids root/log comparison issues. The sharp tie example really attains the stated `a^2` ratio and does not claim impossibility for a better normalization procedure.

6. **Separators and changing anchors.** The augmented matrix is SPD because both the parameter prior and latent anchor prior are SPD. All cross terms of the anchor prior are retained in the cross-representation elimination. Substituting the conditional latent residual is a bijection in the eliminated variables, and Woodbury gives precisely the coarser conditional covariance. Schur concavity, monotonicity and successive elimination imply the asserted hierarchy direction. Empty anchors, an empty schedule, a remaining integrality gap and nonnested partitions are handled explicitly. Arbitrary nuisance witnesses yield the upper quadratic, so numerical stationarity is unnecessary. Singleton patterns recover the actual residual diagonal split; the last unanchored endpoint is correctly distinguished from anchoring every time. The signed bridge formulas and deterministic anchor reset have the appropriate domain restrictions.

## Independent exact checks

I wrote `verification/stage07-review3/exact_certificate_checks.py`, which imports SymPy but imports no manuscript or archived implementation. Its output is `exact_certificate_checks.json`. It passed **767 exact checks**, grouped as follows:

| Check | Count | Distinct scope |
|---|---:|---|
| Selected-information Schur identity | 64 | All 16 subsets at four anchor levels for a dense rational latent covariance, not restricted to a Markov chain |
| Arbitrary nuisance quadratic identity and PSD excess | 64 | Signed two-parameter loadings, nonstationary latent variances and nonoptimal rational nuisance coefficients |
| Cross-anchor Schur identity | 48 | Three nested changes, explicitly permuting retained and removed nuisance coordinates |
| Nested mixture PSD ordering | 24 | Unequal rational mixtures; both intermediate and parameter Schur order |
| VN zero/boundary identity | 81 | Every visit vector in `{0, 1/2, 1}^4`, unequal positive diagonal split and rank-deficient PSD remainder |
| VN matrix gradient identity and PSD | 324 | All four partial derivatives at every preceding query |
| Signed dense reverse-adjoint identity | 162 | Both positive and negative AR correlation, all boundary visit patterns and an admissible split strictly above the nugget |

PSD conclusions in these fixtures are checked using exact principal minors, not floating eigenvalue tolerances. The dense checks independently form and invert the full resolvent and compare every row and information entry with the derived recurrences. These finite checks support implementation-independent algebraic confidence; the general conclusions still rely on the manuscript proofs.

## Whole-paper coherence and contribution boundaries

The introduction accurately distinguishes classical selected-covariance information, virtual-noise equivalence, Vecchia conditionals, PSD profile machinery and subsystem design from the specific guarantees developed here. The practical computations do not purport to implement the large theoretical spectral sets. Local sensitivity consistency, encoded rational optimization, physical noise assumptions and global nonlinear identifiability remain separate throughout. The public-source and temporal kinetic models are also clearly distinguished.

The scalar/noisy-block, general-decay and partial-packet assumptions align with their later complexity uses; the calendar feasibility graph retains a cooldown for long spacing. The spectral normalization accounts for exact singular ranges and forced owners. The represented-matroid argument keeps the original rank when restricting or deleting, and explicitly addresses cancellation and finite-field limitations. The examples of failed dominance, capped solves, nonnested separator comparisons, and fixed-physical-grid difficulties agree with the conclusion's qualified practical claims. I found no unsupported inference that a closed mixture gap certifies a single design.

The manuscript is substantial, but its progression is coherent and the assumptions needed for the individual results are stated locally. The contribution table and result roadmap make the different strands navigable. I do not regard its length, the explicit counterexamples, or the retained negative results as defects requiring changes under the user's comprehensive-coverage request.

## Literature checks and limits

I independently inspected the local primary full text of Kim and Kim (2006), confirming that inverse-logdet convexity is already identified there as established. I inspected Hainy et al.'s Proposition 3 and its zero-weight extension, and Sagnol and Harman's subsystem criterion and Theorem 4.3/Corollaries 4.4–4.5. Those antecedents are accurately credited in the manuscript. I also checked the current official arXiv records for [Hainy et al.](https://arxiv.org/abs/2504.17651) and [Chowdhary et al.](https://arxiv.org/abs/2409.09137), confirming the cited versions and their stated subject matter. I did not infer novelty from an unavailable publisher text.

I did not repeat all 46 archived certificate replays, the public-source enumeration or a fully isolated dependency installation in this review; those are separate whole-manuscript review responsibilities. I read their described contracts and the empirical conclusions, without treating archived solver status as mathematical evidence. I did not inspect every cited work's full text, conduct an exhaustive worldwide priority search, or perform proof-assistant verification. The qualified novelty wording is appropriate to these limits.
