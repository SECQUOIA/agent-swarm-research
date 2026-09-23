# Stage 1, round 1 — reviewer 06

Primary lens: quadratic-system upper bounds, real/complex descent, symmetric shrinking, coordinate exponents, and compact formulations.

Major findings: 0

Minor findings: 2

I found no major defect in the completed stage. The quadratic-system precision theorem has a coherent standalone proof once its explicitly imported algebraic results are accepted. In particular, the passage from an arbitrary complex shrunk space to real quadratic coordinates is justified; it does not assume that independent row and column operations are permissible input transformations. The smooth and constant-rank extensions also retain the domain and containment conditions their proofs need. This assessment is a mathematical review, not formal verification or a publication-priority certification.

## Snapshot and coverage

I checked all five frozen-file hashes against `snapshot.json`; all matched:

| File relative to `paper-integer-dimension/` | SHA-256 |
| --- | --- |
| `sections/01-foundations.tex` | `075e0e998e9cf3e9bdf0830fde1822876ac272bb336eec5d10374425ace92e03` |
| `references.bib` | `bc7fbcf1dad163b2e1064e787760f7f76b88ba649c3f6657d3a46d9432a433da` |
| `coverage.md` | `a5b675009a1c889bf93105e5b1121f2d5de5fac732d414c4b0b71563e1ce7727` |
| `macros.tex` | `3f613a2cf8ebf1bd4c6c84b531de0e74479e07a19ce7566961f1348384de7a3f` |
| `main.tex` | `cecaea518c089ff3beca3edf14ec879129f947f67ed01af7ef3602fb74ea571e` |

I read `PROCESS.md`, `reviews/PROTOCOL.md`, the task and lens instructions, the entire 1,206-line stage, its bibliography, macros, main file, and coverage inventory. I checked the arguments throughout the stage, including parity closures, finite disjunction, square/product constants, graph allocation, indefinite volume, inertia, covariance/capacity, principal compression, smooth contact volume, constant-rank tubes, and perspective transfer.

I compared the manuscript in depth with `results/quadratic-system-noncommutative-rank-complexity.md`, `results/smooth-map-local-rank-integer-complexity.md`, and `results/constant-hessian-rank-smooth-precision.md`. I read the scope and coordinate-construction portions of `results/quadratic-ncrank-rational-construction.md`, and consulted `notes/quadratic-noncommutative-rank-novelty.md` and `notes/review-quadratic-noncommutative-rank-second.md` only after checking the manuscript's proof chain independently. Earlier audit conclusions were not treated as proof.

For primary-source checks, I read the relevant GGOW text in `build/source-cache/ggow2020.txt`, including Theorems 1.4, 1.17, and 2.18 and the discussion of capacity on printed page 237. I also checked the actual statements of [IQS, Theorem 1.5 and Lemma 5.3](https://arxiv.org/html/1512.03531), and the involution convention in [Volčič, Section 2.1](https://www.cambridge.org/core/journals/forum-of-mathematics-sigma/article/hilberts-17th-problem-in-free-skew-fields/1DC74DC3E0E011210C826FF4DCA24DE1). IQS explicitly supplies polynomial rational data sizes and invariance under field extension. Volčič supplies the involution used for Hermitian principal elimination.

Limits: I did not conduct an exhaustive novelty search, recheck every bibliography item's publication metadata, inspect the compiled PDF, or audit every one of the 173 supporting notes. The deferred stages and the full quantitative bit proof of the rational preview are outside this round's completed mathematical stage. The preview's use of rational bases and its imported algorithmic scope are consistent with the sources inspected.

## Findings

1. **MINOR — malformed products in the smooth upper-bound proof.** Location: `sections/01-foundations.tex`, lines 974, 977, and 992, proof of `thm:smooth-ranks`. The expressions `C_0,2^{-T}` and `2C_0,2^{-T}` contain literal commas where multiplication is intended. These render as punctuation inside the inequality and obscure the actual Taylor-error budget. This is a typesetting defect, not a false estimate: the preceding coefficient argument proves a constant times `2^{-T}`. Replace them by `C_0\,2^{-T}` and `2C_0\,2^{-T}` consistently.

2. **MINOR — the capacity equivalence needs its own source locator.** Location: `sections/01-foundations.tex`, lines 529–541, especially the citation to GGOW Theorems 1.4 and 1.17 before `eq:capacity`. Those two theorem statements give the matrix-evaluation, shrinking/rank-decrease, and zero-rectangle characterizations; neither theorem statement itself gives the capacity equivalence. The same primary paper does discuss positive capacity for noncommutatively nonsingular pencils on printed page 237 and develops capacity in Section 2. See [GGOW's published paper](https://www.math.ias.edu/~avi/PUBLICATIONS/GargGOW20.pdf). Add a separate accurate capacity locator and credit Gurvits for this established equivalence. This is an incomplete pinpoint citation, not a mathematical gap: the source supports the claim elsewhere, and the subsequent Hall/permanent argument independently supplies the qualitative energy constant used in the rate proof.

## Detailed verification of the primary lens

- **Complex-to-real descent, lines 590–601:** The deficiency is supermodular because the image of an intersection is contained in the intersection of images. A maximizing space and its conjugate both have deficiency `d`; the maximum bound forces their sum and intersection to have deficiency `d`. The sum is conjugation invariant and is therefore the complexification of its real part. Its image has the same property. This proves existence of a real maximizing pair without a genericity or rationality assumption.
- **Symmetric coordinate construction, lines 603–612:** The two restricted orthogonal projections are adjoints, so their equal ranks give `dim Z - dim W = d`. Symmetry sends each `z` in `Z` into both `V` and `U`'s orthogonal complement, hence into `W`. Orthogonality and the dimension of the remaining complement give exactly `2 dim W + dim Q = r`. This also handles empty blocks and deficiency zero.
- **Exponent assignment, lines 615–620:** The possible blocks have endpoint weights `1` for `ZW`, `2` for `WW`, `3/2` for `WQ`, and `1` for `QQ`. Square coefficients are correctly counted twice. Thus leaving `Z` undiscretized does not omit any low-weight nonlinear term, and the total weight is `r/2`.
- **Quadratic upper formulation, lines 727–745:** The enclosing box has positive finite widths because the original box is full dimensional and the coordinate transformation is invertible. Diagonal normalization preserves zero blocks; translation contributes only affine terms. The original domain constraints remain in the lift. An empty prefix has zero affine prefix and the entire bounded coordinate as residual, so the mixed `ZW` terms remain covered by the same construction. The residual McCormick/square error and the absolute coefficient sum give `C 2^{-T}/4`, including signed coefficients. Exact residual products retain every graph point. Each needed monomial uses a number of rows linear in its endpoint depths, so the fixed-data size assertion follows.
- **Rational bases, lines 802–810:** Orthonormal bases are unnecessary: a congruence whose columns lie in mutually orthogonal subspaces preserves the required zero blocks even when the bases within those subspaces are not normalized. Rational nullspaces and inverses therefore suffice. The manuscript correctly separates this fact from the later uniform height and running-time proof.
- **Smooth extension, lines 963–1007:** Taylor segments for the general smooth upper remain inside the transformed original domain. In the polynomial compiler the forbidden Hessian entries vanish identically, which justifies moving Taylor base points to prefixes in the larger enclosing box. Products of existing integral bits force the auxiliary product variables to be binary-valued without a new integrality declaration. The stated fixed-degree term count is valid.
- **Compactness elsewhere:** The Hall/permanent argument takes a continuous positive function on the compact orthogonal group, so its minimum is positive. The constant-rank construction controls the whole polyhedral tube through transverse Taylor displacement, then takes finitely many charts covering boundary points as well. Neither argument assumes a uniform aspect ratio for contact sets.

Executed checks, both successful:

1. `python code/quadratic_rank/check_shrunk.py` — 20 exact rational examples after nonorthogonal congruence verified the shrinking dimensions, zero blocks, and precision sums. I inspected this checker before running it.
2. `python code/quadratic_rank/check_smooth_polynomial.py` — verified the quartic example's Hessian rank, forbidden zero blocks, and precision weights of all 12 Taylor residual terms.

These finite checks corroborate the calculations; the universal claims were assessed through their proofs. No manuscript or research-source files were edited.
