# Stage 1, round 1 — independent review 14

**Verdict: MINOR.** No major mathematical defect found. The central envelope and bilinear results have complete arguments under their stated conventions. One local qualification is needed in the preliminary spatial-certificate discussion.

## Coverage

Read all frozen text under `process/snapshots/stage01-round01/`: `main.tex`, `macros.tex`, `sections/01-foundations.tex`, and `references.bib`. Read `process/review-protocol.md`, `process/stage-01-review-assignment.md`, `process/stage-01-author.md`, and the scope proposal, with particular attention to the Stage 1 coverage rows. No other report from this round was read.

Read the mathematical arguments in repository-root `results/mccormick-gap-degeneracy-bound.md` and `results/mccormick-hereditary-density-characterization.md`, and the foundational deficiency, independence, and nonnegative-box arguments in `results/positive-multilinear-degree-upper-bound.md`. Historical passing review labels were not treated as evidence of correctness.

After reading `literature/AGENTS.md`, inspected the relevant primary-source passages:

- `[[luedtke2012-some-results-on-the-strength]] p.7-10`: recursive-product limitations, vertex envelope representation, and Theorems 4–5; also the Theorem 8 attribution and the signed four-cycle example in the extracted fulltext.
- `[[boland2017-bounding-the-gap-between-the]] p.4-6`: Lemma 1 and Corollary 1; Theorem 4 and its signed-cycle proof were also checked in the fulltext.
- `[[davidson2007-norms-of-schur-multipliers]] p.3-7`: norm conventions, Theorem 1.2, and the distinction between Theorems 2.3 and 2.4. Rendered and inspected original PDF pages 6–7; the images are in `verification/reviewer14/`. This confirms the continuous bound needed in the manuscript, rather than the rounded integer pattern bound.
- The local inventory did not contain a Szarek original. Independently checked the precise real Rademacher inequality and its attribution in equation (1) of the primary research article [Eskenazis–Nayar–Tkocz, Distributional stability of the Szarek and Ball inequalities](https://arxiv.org/html/2301.09380v2). I have not independently read Szarek's 1976 proof.

McCormick's historical attribution and all bibliography fields were read, but I did not independently verify every publication metadata field or the original McCormick paper.

## Findings

1. **R14-01 — MINOR: qualify the relative-tolerance and best-incumbent conventions.** Location: frozen `sections/01-foundations.tex:180–183`, subsection “What a spatial certificate counts.” The assertion that worse incumbents require weakly higher targets needs `theta <= 1` for the relative target `(1-theta)U`. No range for theta is presently stated. For example, at theta = 2 increasing U from 1 to 2 decreases the target from -1 to -2. Also, the relative convention is expressly defined only for U > 0, so the subsequent unqualified suggestion to grant U = f* is unavailable in that convention when f* <= 0. The absolute-gap argument is unaffected. Repair: state epsilon >= 0 and 0 <= theta <= 1 (or the usual stricter theta < 1), and say that the best-incumbent reduction in the relative convention assumes f* > 0. This is a local clarification; no Stage 1 spatial lower-bound theorem depends on an unstated tolerance range.

## Independent verification

The independent checker is `verification/reviewer14/check_stage1.py`; its recorded output is `verification/reviewer14/result.json`. It imports no manuscript code or existing verification scripts. Reproduction command from the repository root:

```sh
/home/sgusev/miniconda3/envs/minlp-notes/bin/python paper-relaxation-limits/verification/reviewer14/check_stage1.py
```

The run passed. Its exact and numerical parts are deliberately distinguished:

- **Exact exhaustive graph checks:** all 729 coefficient vectors in `{-1,0,1}^6` on the six possible edges of four labeled vertices, including the zero vector and every smaller support. Integer sign enumeration computes Q extrema; an independent enumeration computes each crossing-block bilinear maximum. Their equality verifies the polarization normalization in these cases. Rational arithmetic checks `L^2 <= 16 rho R^2` and `L^2 <= 4 Delta R^2`, avoiding square-root comparisons. Enumerating all row/column subsets verifies `beta = rho` exactly. Enumerating actual cuts verifies that `L = R` holds exactly when both the positive and negative edge sets occur as cuts. The largest observed center ratio is exactly 2.
- **Numerical row check:** the same 729 vectors satisfy `R >= sum_i ||a_i||_2 / 4` with absolute comparison tolerance 1e-12. These square-root evaluations are numerical supporting evidence, not exact certificates.
- **Exact rational envelope checks:** on three variables, enumerate all 58 nonsingular four-column bases of the 4-by-8 vertex-law constraint matrix. For each of the 125 mean vectors in `{0,1/4,1/2,3/4,1}^3`, retain every nonnegative basic law, using exact inverses and rational weights. Minimizing and maximizing the vertex objective over these laws gives exact envelope endpoints. For all 27 coefficient vectors in `{-2,0,3}^3`, the resulting 3,375 comparisons satisfy the induced-cut upper factor, and every half-integral mean satisfies `H = R_W/2` and `T = L_W/2`. This checks boundary fixed-one coordinates as well as fixed-zero coordinates independently of the cut formula.
- **Exact nonnegative-box checks:** at those 125 means on each of two unequal boxes, compute the original trilinear product envelope using the same exact vertex-law LP. Check its upper envelope against the expanded common-threshold formula and its width against the expanded termwise width. All 250 comparisons pass. One box has strictly positive lower endpoints; the other includes zero lower endpoints.

The general proofs were also checked independently, beyond these finite tests:

- Independent endpoint sampling preserves both the mean and multiaffine value, so vertex graph points generate the full scalar graph hull. The lower and upper polytope surfaces yield the claimed envelopes, including the boundary. Consecutive failure arcs have the prescribed marginal measures and attain the single-product lower endpoint.
- The common threshold law is one law for the entire mean vector. Nonnegative coefficients therefore justify common upper attainment and the deficiency optimization identity. The independent-rounding constants follow from `1-exp(-s) >= (1-exp(-1)) min(1,s)`. Affine expansion preserves the full hull, and convexification of a sum makes the original-factor width no larger than the sum of expanded-factor widths.
- In the arrangement argument, connected active equalities or complementations either fix the coordinates, force 1/2 through an odd complementation cycle, or leave a feasible local perturbation. Thus every cell vertex is half-integral. Concavity of H and affinity of T on each cell give precisely the required direction of Jensen's inequality for `T-cH`.
- For the row bound, the locally maximal squared-weight cut guarantees half the squared mass at every vertex; applying both side estimates gives the stated 1/4 factor. The flow cut calculation and fractional weighted Cauchy–Schwarz count each edge once. The direct degeneracy argument, maximum-degree estimate, bipartite estimate, and signed four-cycle sharpness constants agree.
- The random-sign exponential argument uses independence only among edge signs. Global sign reversal reduces the configurations correctly, and Jensen gives the stated finite `sqrt(2mh log 2)` bound. Extending the signing outside the densest induced face does not alter its witness. The full-support perturbation argument uses continuity of the whole-center ratio, without assuming continuity of c* when coefficients disappear.
- The positive coloring probability, exactness cut criterion, arboricity comparison, diluted dense-core example, and scale objection to unnormalized weighted density are consistent. The Schur transfer has factors `2L = <A,M>`, `||A||_(infinity->1) <= 4R`, and `pi(M) <= 2 K_G sqrt(rho)`, yielding `L <= 4 K_G sqrt(rho) R`. The subsequent Sidon comparison and bipartite equality use the correct range conventions.

## Remaining limits

Finite checks do not establish the universal theorems, optimal density constant, or random-sign existence on arbitrary graphs; the manuscript's analytic proofs supply those conclusions. The independent checker does not verify general fractional orientations algorithmically, compute Schur/projective norms, exhaust all real coefficient vectors, or test asymptotically growing graphs. No floating-point optimizer result was accepted as an exact envelope certificate. Existing repository scripts were not relied on or rerun.

The sharp Khinchin theorem, Grothendieck/projective comparison, and max-flow/min-cut remain established external inputs; this review checks their stated forms and uses rather than rebuilding all their proofs. The missing Szarek original and unverified bibliography details are source-verification limits, not evidence that their mathematical statements are false. No future-stage omissions were treated as Stage 1 defects.
