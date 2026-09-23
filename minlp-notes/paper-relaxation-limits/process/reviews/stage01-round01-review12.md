# Stage 1, round 1 — independent review 12

**Verdict: MINOR.** No major mathematical defect, hidden circular argument, or unsupported Stage 1 theorem was found. Two boundary conventions should be made explicit.

## Coverage

Read the entire frozen `process/snapshots/stage01-round01/main.tex`, `macros.tex`, `sections/01-foundations.tex`, and `references.bib`; `process/review-protocol.md`; `process/stage-01-review-assignment.md`; `process/stage-01-author.md`; and the scope proposal, including all Stage 1 rows. Reviewed both complete canonical bilinear files, `../results/mccormick-gap-degeneracy-bound.md` and `../results/mccormick-hereditary-density-characterization.md`. Read `../results/positive-multilinear-degree-upper-bound.md`, checking its foundational deficiency and nonnegative-box arguments against the manuscript. Its later dyadic theorem is outside this frozen stage.

Read `../literature/AGENTS.md` before using the literature. Checked relevant primary-source fulltext portions and original PDF pages as follows:

- `[[luedtke2012-some-results-on-the-strength]] p.5`, `p.8-10`, and `p.15-17`: single-product recursive exactness, common upper envelopes, nonnegative affine expansion, positive coloring bound, and the signed four-cycle. Inspected original PDF pages 9 and 15.
- `[[boland2017-bounding-the-gap-between-the]] p.3-6` and `p.10-11`: dimension bound, cut identities and upper implication, and signed-cycle exactness. Inspected original PDF page 6.
- `[[davidson2007-norms-of-schur-multipliers]] p.3-11`: real/complex norm conventions, Theorem 1.2, weighted Theorem 2.4, and its upper-bound proof chain. Inspected original PDF pages 4, 6, and 7, where extraction omits important formulas.
- Confirmed the precise sharp real Khinchin input through equation (1) in [Eskenazis–Nayar–Tkocz, arXiv:2301.09380v2](https://arxiv.org/html/2301.09380v2), which explicitly states the inequality and credits Szarek. I did not obtain or independently reprove Szarek's 1976 original.

No other current-round report was read. Historical audit labels were not used as mathematical evidence. No manuscript files were edited.

## Findings

1. **R12-01 — MINOR — State the tolerance domain and the positivity needed for the best-incumbent relative convention.** Location: frozen `sections/01-foundations.tex`, lines 180–183. The sentence that worse incumbents require weakly higher targets is correct for the relative target `(1-theta)U` only when `theta <= 1`. No range for `theta` is given. For example, at `theta=2`, increasing `U` from 1 to 2 changes the target from -1 to -2. Also, the preceding relative-gap normalization requires `U>0`, so the substitution `U=f*` in that convention requires `f*>0`; the general compact-feasible-set setup allows `f*<=0`. **Repair:** state `epsilon >= 0` and `0 <= theta < 1` (or allow `theta=1` explicitly), and qualify the relative best-incumbent statement by `f*>0`. The absolute-target statement remains valid without positivity. This is local because no spatial lower-bound theorem is asserted in this stage.

2. **R12-02 — MINOR — Carry the edgeless convention into the positive and Sidon statements.** Location: frozen `sections/01-foundations.tex`, lines 494–495 and 575–582. Earlier definitions explicitly set `c*(0)=Gamma(G)=0` for edgeless graphs, but the unqualified sentence that the positive bilinear factor “is one on bipartite graphs” includes an edgeless graph. The definition `S(G)=sup_{a!=0} L_V/||Q||_infinity` likewise has an empty indexing set for an edgeless graph, yet the displayed comparisons are unqualified. **Repair:** say “is one on bipartite graphs with nonempty coefficient support,” and set `S(G)=0` for edgeless graphs, or restrict that final paragraph to graphs with an edge. No positive-support case or asymptotic conclusion is affected.

## Independent verification

### Dependency graph and independence of the arguments

The core proofs form an acyclic chain:

1. Multiaffinity and independent endpoint interpolation identify the scalar graph hull with the convex hull of vertex graph points. Finite-dimensional compactness gives attainment. Polytope surfaces give continuous piecewise-affine envelopes, including at the boundary.
2. Joint-success probability bounds and explicit circle/threshold laws give exact single-product envelopes. A single threshold variable attains every positive upper envelope; positivity is used at precisely this summation step. The deficiency identity then follows by subtracting the common upper value from the minimum expected polynomial value. Both independent-rounding cases use the same full-dimensional independent law.
3. The nonnegative-box transfer uses the affine bijection for the full hull and the general inequality that splitting a factor can only enlarge its termwise width. It does not import a degree theorem or a lower construction. Expansion preserves coefficient nonnegativity and degree, but can change incidence, as the text states.
4. The induced-cut identity uses the vertex-law result plus the symmetric two-point sign law at half-valued coordinates. Coordinates fixed to one contribute only affine terms. The upper implication is separately proved: the arrangement cells have only 0, 1/2, 1 vertices, the termwise gap is affine on each cell, and `T-cH` is convex there. Thus the manuscript does not assume the desired global cut characterization while proving it.
5. Polarization, the explicitly imported Khinchin inequality, a local maximum cut for squared weights, and max-flow/min-cut give the elementary upper bound. The fractional-orientation flow argument proves both existence and minimality; it does not use a gap theorem. Cauchy–Schwarz sums each absolute edge weight exactly once. Degree and bipartite constants follow by separate row estimates. The direct degeneracy proof uses a reverse greedy coloring and remains independent of fractional orientation.
6. The lower construction uses only independent edge signs, the exponential-moment estimate, global sign symmetry, Jensen's inequality, and the already established face identity. It does not use the elementary upper theorem or either Schur input. The estimate is finite and existential on each graph; independence across different vertex sign vectors is never assumed. Extending the signing outside a densest face preserves full support without changing the witness value.
7. The equality of the unrestricted coefficient supremum and the whole-center supremum follows by zero extension of induced coefficients. The full-support approximation uses continuity of the whole-graph ratio on `L=1`, not continuity of `c*` under disappearing edges. Strict positivity follows from orthogonality of distinct degree-two characters, so the compactness argument has no denominator gap.
8. The Schur transfer is a separate upper argument, depending only on its stated external norm inequalities, density counting, elementary projective duality, and polarization. It shares the induced-cut localization with the elementary proof but does not depend on that proof's row bound. The text correctly couples this older upper implication with the independently proved random-sign lower order.

The imported substantive analytic facts are clearly marked: sharp real Khinchin and the Schur/projective norm inequalities. Max-flow/min-cut and basic finite-dimensional convexity are standard additional inputs. Recursive monomial exactness is a cited background fact; it is not needed to prove any comparison for the specified exact termwise model.

### Constants, examples, and scope

I checked the factors of two directly: at a half-valued face `H=R/2` and `T=L/2`; polarization gives `R=max ||A_(S,S^c)||_(infinity->1)`; the locally optimal squared-weight cut gives `R >= (sum_i ||a_i||_2)/4`. Consequently `L <= 4 sqrt(rho)R` and `L <= 2 sqrt(Delta)R`. For a bipartite graph all edges cross the fixed partition, giving `L <= sqrt(2 min(Delta_P,Delta_Q))R`. The unit four-cycle with one negative edge has `L=4`, `R=2`, density 1, and degeneracy 2, validating the finite lower constants and the claimed bipartite sharpness.

The random-sign calculation has `2^h` exponential terms, giving `E Z <= h log(2)/lambda + m lambda/2` and the stated square-root bound after optimization. Densest-face localization therefore proves the fixed-graph lower constant without a hereditary-closure assumption. The positive coloring probability yields both parity cases, and the all-positive complete-graph ratio tends to two. The cycle criterion follows from the two sign classes each being a cut. The arboricity comparison, diluted dense core, scale-invariance obstruction, and planar/series-parallel corollaries have the stated implications. No pointwise gap bound is used as an optimization ratio or a tree-size theorem.

For the Schur transfer, original PDF pages confirm the continuous weighted upper estimate and the projective comparison, including the real constant convention. Counting a symmetric adjacency pattern gives `beta(P)=rho(G)`. Pairing a weighted adjacency matrix with its sign matrix gives `2L <= pi(M)||A||_(infinity->1)`, and the second polarization gives `||A||_(infinity->1) <= 4R`; together these give `L <= 4 K_G sqrt(rho)R`. The Sidon comparison uses mean zero and, in the bipartite case, a sign flip of one part. No claimed upper-bound constant is inferred from the lower-bound construction.

### Finite checker

`verification/reviewer12/check.py` exhausts all 729 vectors in `{-1,0,1}^6` on four labeled vertices, including the zero vector. Exact integer/Fraction arithmetic checks polarization, the squared density and maximum-degree inequalities, the bipartite bound for every valid partition, and `R=L` exactly when both sign classes are cuts. It passes; output is in `verification/reviewer12/check-output.txt`. This checks finitely many weighted graphs and does not prove the universal theorems. The general proof audit above supplies that assessment. Six inspected source-page images are retained in the same verification directory.

## Remaining limits

This review does not settle priority across all earlier literature, the optimal universal density/degeneracy constants, or any future-stage claim. The manuscript appropriately leaves those distinctions open. The historical McCormick citation was not checked against its full original, and Szarek's original proof was not inspected; the exact analytic input was checked in the primary research source identified above. No independent LaTeX rebuild or full PDF layout audit was performed. These limits do not affect the proof-dependency conclusion or warrant a major verdict.
