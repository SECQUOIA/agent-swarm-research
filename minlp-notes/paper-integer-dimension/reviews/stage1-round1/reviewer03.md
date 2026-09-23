# Stage 1 review — reviewer 03

Primary lens: exact square/product constants, strong convexity, and finite disjunctions.

Major findings: 0
Minor findings: 3

I found no major mathematical defect in this review. The exact square law, the stated finite product bounds, the strong-convexity bound, and the disjunction construction are sound. The later quadratic and smooth arguments also withstand the checks described below. This is a bounded independent review, not a guarantee of correctness or publication priority.

## Snapshot and coverage

All five hashes were recomputed and matched `reviews/stage1-round1/snapshot.json`:

| File | SHA-256 |
| --- | --- |
| `sections/01-foundations.tex` | `075e0e998e9cf3e9bdf0830fde1822876ac272bb336eec5d10374425ace92e03` |
| `coverage.md` | `a5b675009a1c889bf93105e5b1121f2d5de5fac732d414c4b0b71563e1ce7727` |
| `macros.tex` | `3f613a2cf8ebf1bd4c6c84b531de0e74479e07a19ce7566961f1348384de7a3f` |
| `main.tex` | `cecaea518c089ff3beca3edf14ec879129f947f67ed01af7ef3602fb74ea571e` |
| `references.bib` | `bc7fbcf1dad163b2e1064e787760f7f76b88ba649c3f6657d3a46d9432a433da` |

I read all 1,206 lines of `sections/01-foundations.tex`, the process and review instructions, the bibliography, and the coverage inventory. I compared the relevant proofs in `results/mip-relaxation-binary-lower-bounds.md`, `results/quadratic-inertia-one-sided-integer-complexity.md`, `notes/mip-binary-lower-bound-extensions.md`, and selected corresponding proof sections in the nc-rank, smooth-map, and constant-Hessian-rank result files. I also inspected the original square and one-sided audit notes after independently checking their arguments.

Primary-source checks used the local full text of Lubin–Vielma–Zadik, Beach et al., and Vielma's embedding-formulation paper, and the cached GGOW, Wolff, and Nicola texts. I read `literature/AGENTS.md` first. The source checks cover the specific ingredients and locators discussed here; they are not a comprehensive bibliography or novelty audit. I did not independently prove the imported free-field/algorithmic results, audit all 173 supporting notes, compile the paper, or inspect the rendered PDF. The explicitly deferred rational bit-complexity proof is not counted as a stage-1 omission.

## Findings

1. **MINOR — typographical error in the smooth Taylor estimates.** Location: `thm:smooth-ranks`, lines 974, 977, and 992. The expressions `C_0,2^{-T}` and `2C_0,2^{-T}` contain literal commas, so they do not print the intended products. The proof immediately before and after these expressions supplies the correct estimate; this is not a theorem or proof-gap finding. Replace them by `C_0\,2^{-T}` and `2C_0\,2^{-T}` (or ordinary juxtaposition).

2. **MINOR — the capacity equivalence needs a more accurate source locator.** Location: lines 529–541, especially `eq:capacity`. The introductory citation points collectively to GGOW Theorems 1.4 and 1.17 for three characterizations. Those theorems state the matrix-evaluation, shrinking, and decomposability characterizations, but neither stated theorem includes the displayed positive-capacity equivalence. GGOW does discuss positive capacity for noncommutatively nonsingular pencils on published p.237, and defines capacity in Definition 2.6 on p.244. The imported fact is correct; the issue is the precise attribution of its location. Give the capacity statement its own accurate locator, including the relevant capacity discussion/result, instead of making Theorems 1.4 and 1.17 appear to state it. This does not invalidate the qualitative law, whose independent Hall/permanent proof is also present.

3. **MINOR — add credit for the established disjunction/embedding construction.** Location: `lem:disjunction`, lines 98–118, and `references.bib`. The proof is complete and valid, including inactive recession directions and unused binary codes, but this frequently reused classical ingredient has no citation. The coverage inventory expressly includes credit for disjunctive formulations among the final obligations. A suitable checked primary comparison is Juan Pablo Vielma, *Embedding Formulations and Complexity for Unions of Polyhedra*, Proposition 1 and Corollary 1: the repository primary full text, `literature/papers/vielma2018-embedding-formulations-and-complexity-for/fulltext.md`, pp.6–7, gives distinct binary encodings and exact recovery of the union at integral codes; its preceding Theorem 1 credits the disaggregated formulation to Jeroslow–Lowe and Balas. Add a brief attribution while retaining the paper's own proof, which also makes its real-coefficient and lineality scope transparent. This is a provenance improvement, not a claim that the manuscript falsely asserts novelty.

## Independent mathematical and executable checks

- Re-derived the strong-convexity inequality: contact diameter is at most `sqrt(8 epsilon / mu)`, so one contact has volume at most `omega_d (2 epsilon / mu)^(d/2)`. Summing the compact parity cover gives exactly `eq:strong-lower`, including its factor `mu/2`. Using assignment count instead of parity count is valid by closing the individual contact sets.
- Checked square graph containment, error attainment, and linear size directly from the shared-prefix identity. The depth-zero case and the representation of input 1 are included. The equality for the integer minimum holds at the accuracy thresholds, without an unattained-infimum issue.
- Re-derived the product section integral `4 delta ln 2`, the width bound `5 delta`, substitution `delta=4 epsilon`, and the maximum two-integer gap between the displayed ceiling bounds. The four-point example has all six absolute difference products equal to `sqrt(5)-2`.
- Checked the disjunction proof for `N=1`, unused codes, lower-dimensional members, and common recession cones. An integral binary convex combination forces one code; inactive homogenized members contribute only recession vectors absorbable in the active member.
- Checked the signed-square epigraph construction, the folding-tail Lipschitz argument, the exact one-sided product constant, and the lower-facet/extended-face count. Output unboundedness does not undermine either epigraph containment or the error inequality.
- Checked the scalar determinant constant, covariance expansion and volume inequality, capacity rearrangement, principal compression, real descent, symmetric shrinking, and the shared-monomial upper error budget. Checked the oscillatory proof's mixed-Hessian neighborhood and indicator-function application, the smooth polynomial compiler, the Legendre fibers and whole-tube remainder bound, and the perspective row division by positive `t`.

An independently written inline Python check passed 2,159 exact rational square-prefix cases at depths 0–6, including all prefix cells and exact midpoint attainment; 774 SciPy linear programs optimizing the relaxed folding chain at depths 1–6 and 129 abscissae per depth; the six width-obstruction pairs; and 10,001 samples of the product ceiling gap. The LP optimum agreed with the exact folding sequence within `1e-9`. These finite checks support the analytic review and do not replace its proofs. No manuscript, bibliography, or original research files were edited.
