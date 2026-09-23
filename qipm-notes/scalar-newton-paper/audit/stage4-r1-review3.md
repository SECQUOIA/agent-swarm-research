# Stage 4, round 1 — independent review 3

Scope: the complete abstract and introduction, rate table, barrier conventions in Section 2, conclusion, bibliography integration, README, Makefile, submission script, and standalone package. I cross-checked the summary claims against the relevant statements in Sections 4–10 and the existing classical estimator. I read the Stage 4 author report and literature ledger, but no other reviewers' reports. No manuscript edits or delegation were made.

**Verdict: no major or minor corrections identified in this integration stage.** This review does not replace the requested final whole-manuscript review.

## Rates and assumptions

- The abstract's classical expression agrees with the constant-confidence specialization of the scalar estimator. It correctly separates the statistical and exponential lower families from the simultaneous bounds, and does not claim their full product.
- The table's two-sparse lower bound includes the finite-population minimum. Its confidence-dependent statement is explicitly restricted to sufficiently large population; the theorem gives the exact required inequality. The clock row matches the theorem's sparsity, conditioning, accuracy dependence, and denominator. The caption correctly explains that the initial reduction requests two forms and therefore lower-bounds a routine supporting arbitrary supplied forms.
- The composition row includes the signal-to-baseline parameter and points to the required oracle-preserving inner family; it does not state an unrestricted product theorem. The prose correctly describes the fixed-coefficient simultaneous exponential/statistical example and confines the separate `kappa^2` factor to the high-accuracy construction.
- The block-access row preserves normalization `alpha`, the accuracy range, and the distinction between system block calls and state preparation. The general sparse-access row leaves the lower and upper bounds unmatched and correctly singles out the canonical two-sparse family as attaining the lower rate. The population restriction remains in the cited theorem and table caption.
- The barrier conventions correctly define local and dual norms, the Newton direction for a maximization barrier subproblem, the squared predictor decrement after a multiplier change, and restriction to an equality tangent space. They do not identify the restricted Hessian condition number with that of a KKT augmentation. The introductory warning that a decrement alone is not a generic global optimality certificate is appropriate.

## Structured systems, reuse, and novelty

- The structured summary retains the sparse full-rank base, the small possibly indefinite correction, source-vector sampling, spectral bounds, and scalar-data promises. It describes the sampler as bounded-cost flagged draws with reusable setup, rather than asserting a full SQ oracle or a finite-bit implementation. The power-cone scalar-acquisition restriction is expressly stated.
- The full-output comparisons remain separate from the scalar query bounds. The conclusion retains the need for hypotheses at the actual iterates and the correct outer residual contract; it does not promote the per-system exact-arithmetic bounds into a general end-to-end IPM theorem.
- The temporal summary distinguishes independent-input constructions from the repeated hard ray. The reuse summary charges residual tests and explicit-output costs instead of equating a refresh count with total runtime. The claim that a single acquisition can serve every checkpoint agrees with the fixed-ray construction.
- The contribution statement is qualified and limited to the stated full-SQ positive-form refinements, single-form composition calculations, parameterized optimization and temporal realizations, and sparse-base correction theorem. The surrounding paragraphs explicitly attribute sparse polynomial evaluation, inverse-form numerical methods, variable-time norm estimation, Forrelation constructions, prior scalar LP value hardness, low-rank SQ methods, cone identities, and recycling. I found no new priority claim for those established ingredients.
- The abstract, introduction, conclusion, and technical sections give a consistent account of the unresolved general parameter regimes. These are identified as limits of the proved classification, not silently assumed results.

## Literature and metadata checks

I independently opened the current primary records for the added comparisons. The [Edenhofer–Hasegawa–Le Gall version 3 text](https://arxiv.org/html/2509.20183v3) supports the sparse polynomial spectral-sum comparison in Theorem 3.1 and the reciprocal application in Section 3.3. The manuscript's arbitrary-vector positive relative-form distinction is stated accurately.

The [Le Gall primary record](https://arxiv.org/abs/2304.04932) explicitly describes approximate length-squared sampling in total variation and extensions of both sparse and low-rank dequantization, supporting the new attribution and the decision not to claim a new general robustness framework. The [Zhao et al. primary record](https://arxiv.org/abs/2604.07639) confirms the authors, title, date, and space/data-sample setting of the adjacent comparison. The manuscript imports no space lower bound into its unrestricted-storage model.

The DOI landing request for Cifuentes et al. failed, but the [direct APS publication page](https://journals.aps.org/prxquantum/abstract/10.1103/g5x4-jcsz) succeeded and independently confirms PRX Quantum **7**, 020364, publication on 18 June 2026, and DOI `10.1103/g5x4-jcsz`. Thus the metadata in the manuscript is verified despite the earlier landing-page failure recorded by the author.

## Standalone verification

The ZIP has 24 files, passes its CRC check, excludes all `audit/` paths, and every archived byte sequence matches the corresponding current repository file. I extracted the archive to a fresh temporary directory and ran `conda run -n qipm --live-stream make -B`. The build exited successfully and generated a 59-page PDF. Its log had no warnings, undefined references/citations, or overfull/underfull boxes.

The README states the actual build and numerical-check dependencies, distinguishes diagnostics from proofs, and explains the intentionally omitted author and venue metadata. The package contains every input required by the independent build. I found no hidden repository-path dependency or placeholder in the manuscript text.
