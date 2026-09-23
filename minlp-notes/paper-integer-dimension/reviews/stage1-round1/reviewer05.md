# Stage 1, round 1 — reviewer 05

Primary lens: quadratic-system lower bounds, covariance, capacity/Hall, and principal restrictions.

Major findings: 0

Minor findings: 2

## Assessment and coverage

I found no major mathematical defect in the stage. In particular, the quadratic-system lower bound survives independent reconstruction: principal compression supplies an actual coordinate slice, the fourth-moment calculation controls covariance energy without a sign assumption on individual Hessians, and both the capacity argument and the Hall/permanent argument yield the required determinant exponent. The finite constant in `eq:ncrank-finite` is consistent with these calculations. This is a review judgment within the limits below, not a claim of certainty.

I read all 1,206 lines of `sections/01-foundations.tex`, the complete coverage inventory, the bibliography, macros and main file, and the process and review instructions. I checked the parity closure argument, finite disjunction, square/product constants, interaction-graph allocation, scalar rank and inertia, quadratic systems, smooth oscillatory lower bound, both smooth upper constructions, constant-rank tubes, and perspective transfer. The later rational construction is explicitly a preview; I did not treat its deferred proof as an omission in this stage.

I read both canonical quadratic-system result files completely, compared the smooth upper construction and constant-rank tube arguments against their corresponding original result sections, and checked the epigraph face-count argument in `notes/mip-binary-lower-bound-extensions.md`. I also inspected the quadratic nc-rank novelty note and relevant portions of the second original nc-rank review after reconstructing the mathematical argument; neither was used as proof.

For primary sources I inspected the cached GGOW published text, especially Theorems 1.4, 1.17 and 2.18 and its discussion of capacity positivity, and the cached Fortin–Reutenauer rank/decomposability theorem. I read `literature/AGENTS.md` before consulting the source inventory. I did not independently retrieve every bibliography item, fully verify the IQS rational algorithm preview, conduct an exhaustive priority search, or compile/render the paper. The supplied analytic proof was checked directly, without independently auditing all the Hörmander, Wolff and Nicola locators.

## Snapshot verification

All five SHA-256 hashes matched `reviews/stage1-round1/snapshot.json` when checked:

| File | SHA-256 |
| --- | --- |
| `coverage.md` | `a5b675009a1c889bf93105e5b1121f2d5de5fac732d414c4b0b71563e1ce7727` |
| `macros.tex` | `3f613a2cf8ebf1bd4c6c84b531de0e74479e07a19ce7566961f1348384de7a3f` |
| `main.tex` | `cecaea518c089ff3beca3edf14ec879129f947f67ed01af7ef3602fb74ea571e` |
| `references.bib` | `bc7fbcf1dad163b2e1064e787760f7f76b88ba649c3f6657d3a46d9432a433da` |
| `sections/01-foundations.tex` | `075e0e998e9cf3e9bdf0830fde1822876ac272bb336eec5d10374425ace92e03` |

## Findings

1. **MINOR — inaccurate collective theorem locator for capacity.** Location: `sections/01-foundations.tex:529–541`, the citation introducing `eq:shrunk`, `eq:evaluation`, and `eq:capacity`. The cited GGOW Theorems 1.4 and 1.17 support the free-field rank, matrix evaluation, shrinking, and zero-rectangle characterizations. They do not themselves state the displayed positive-capacity equivalence. GGOW discusses capacity positivity separately, explicitly crediting Gurvits; see published p. 237, the paragraph immediately before Section 1.6, and p. 280 in its concluding discussion. This is a source-locator/attribution issue, not a false theorem or a gap in the Hall-based qualitative proof. Repair by splitting the citations: retain Theorems 1.4 and 1.17 for shrinking/evaluation and cite the capacity discussion separately, crediting Gurvits as presented by GGOW. Do not substitute Theorem 2.18 for the arbitrary-real-coefficient positivity assertion: that theorem's stated quantitative hypothesis is integral Kraus matrices.

2. **MINOR — repeated multiplication typo in smooth Taylor bounds.** Location: `sections/01-foundations.tex:974`, `:977`, and `:992`, in the proof of `thm:smooth-ranks`. The source writes `C_0,2^{-T}` and `2C_0,2^{-T}` with literal commas. These print as punctuation rather than the intended product and obscure the error-budget inequality. The original smooth-map result has the intended product. Repair all three occurrences to `C_0\,2^{-T}` or `C_0 2^{-T}`, with the corresponding leading factor two at line 977. This is a typesetting defect; the surrounding proof determines the intended estimate unambiguously.

## Detailed verification of the primary lens

- **Principal restrictions:** the two-by-two off-diagonal Hermitian pivot has its inverse factors in the correct order over a division ring. Its Schur complement is Hermitian, rank is additive under block elimination, and selecting principal indices in the complement selects original principal indices in the whole matrix. Applying this to the free-field pencil avoids the unjustified alternative of interpreting independent algebraic row and column changes as a real quadratic coordinate change. Fixing complementary real inputs preserves the common componentwise error and gives the stated positive slice volume.
- **Covariance identity:** expanding `(A+B-2C)^2/4`, where `A=X^TGX`, `B=Y^TGY`, and `C=X^TGY`, gives exactly the three terms in lines 644–647. Centering kills the mixed terms containing one unpaired factor; it does not require a symmetric distribution. Positive volume guarantees positive covariance. Whitening and comparison with a centered ball give the stated factor `omega_s(s+2)^(s/2)`.
- **Capacity and constants:** a real positive definite covariance is allowed in the Hermitian capacity infimum. The AM–GM step acts on the positive matrix `Sigma^(1/2)T(Sigma)Sigma^(1/2)`. Combining energy at most `16m epsilon^2` with volume gives `C_s epsilon^(s/2)` with precisely the power `s/4` in `C_s`. Rearranging the parity cover produces the denominator `4(r+2)omega_r^(2/r)` in `eq:ncrank-finite`.
- **Hall alternative:** a missing perfect matching would exhibit a coordinate column subspace whose joint image lies in fewer coordinate rows, hence a real shrunk subspace and, by complexification, a contradiction. The permanent is continuous and strictly positive at every orthogonal matrix, so compactness legitimately gives a positive uniform minimum. Selecting one of the `s!` permutation products and applying AM–GM uses every covariance eigenvalue twice. No common diagonalization of the Hessians is assumed.
- **Certificate and example:** the squared-Hessian certificate gives both row and column sums equal to `c`, and its weighted AM–GM argument is valid with zero weights omitted. For the cross product, the stated Hessian signs, scalar rank four, squared sum `2I_6`, and lower factor `1/(16 omega_6^(1/3))` agree. Direct sums give the claimed `3k` versus `2k` coefficient gap.
- **Upper/lower compatibility:** real descent by conjugation and supermodularity supplies the maximal deficiency needed by the symmetric shrinking lemma. The orthogonal decomposition has zero `ZZ` and `ZQ` blocks and total exponent `r/2`; translation and diagonal normalization preserve those zero blocks. Consequently the upper construction matches the same invariant that appears in the lower proof.

## Executed checks

I ran the existing exact-arithmetic scripts `code/quadratic_rank/check_vector.py` and `code/quadratic_rank/check_shrunk.py`. They passed the symbolic cross-product Hessian and squared-sum identities, the skew-rank identity, 15 exact positive-definite covariance energy checks, the centered fourth-moment identities for all three outputs, and 20 nonorthogonal-congruence checks of shrinking dimensions, zero blocks, and precision sums. These finite checks supplement the proofs and do not establish their universal claims. No manuscript or source research files were edited.
