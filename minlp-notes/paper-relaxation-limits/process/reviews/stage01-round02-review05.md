# Stage 1, round 2 — independent review 05

**Verdict: PASS.** No major or minor defect identified. The restored finite results are supported by a complete enumeration argument and an independently reproduced exact calculation. The earlier analytic results and the accepted repairs survive this review.

**Coverage.** I read all frozen manuscript text in `process/snapshots/stage01-round02/`: `main.tex`, `macros.tex`, `references.bib`, `sections/01-foundations.tex`, and `sections/appendix-finite-signings.tex`. I also read the frozen `verification/check_complete_signings.py` and `verification/complete_signings.json`, and inspected text extracted from the appendix and references of the frozen PDF. I read the assignment, review protocol, Stage 1 coverage rows and staging rules in `process/scope-proposal.md`, round-1 adjudication, and correction record. I did not read another round-2 review or edit the manuscript.

The canonical dependencies read were `results/mccormick-gap-degeneracy-bound.md`, `results/mccormick-hereditary-density-characterization.md`, and `results/positive-multilinear-degree-upper-bound.md` (including its preliminary envelope and box-transfer arguments). The first two were read in full; I also read the full third note, while treating its later coupling theorem as future-stage material.

After reading `literature/AGENTS.md`, I checked relevant primary-source passages:

- `[[luedtke2012-some-results-on-the-strength]] p.4-9` and `p.15`: recursive relaxation, vertex envelopes, Theorems 4–5 and 8. The original PDF's pages 8–9 and 15 confirm the equations, nonnegative-domain restriction, and theorem numbering.
- `[[boland2017-bounding-the-gap-between-the]] p.1-6`, `p.10-11`: main statements, induced-cut identities, exactness proof, and predecessor attribution. Original PDF pages 3–4 confirm the stated constants, cut normalization, and the explicit attribution to Misener–Smadbeck–Floudas Theorem 3.10.
- `[[davidson2007-norms-of-schur-multipliers]] p.3-7`: Theorems 1.2 and 2.4 and the real/complex distinction. Original PDF pages 4 and 6–7 confirm the projective-norm direction and continuous density bound.

Source-access limits are stated below rather than treating metadata as inspected proofs.

**Findings.** None. No repair requested.

**Independent verification.** I wrote and ran `verification/reviewer05/round02/check_quadratic.py`; its output is `verification/reviewer05/round02/checks.json`. It uses Python's unbounded integers and exact fractions. Its independent search evaluates the quadratic form on all `2^n` spin vectors, updates coefficients in Gray-code order, and derives `R` from half the quadratic oscillation. It does not use the manuscript's cut masks or signed cut-weight formula. It exhausts all normalized signings through K7. As a check on normalization, it also exhausts every unnormalized signing through K5 and verifies that every range-histogram count is multiplied by exactly `2^(n-1)`.

The exact normalized histograms are:

| Graph | R : number of representatives |
| --- | --- |
| K2 | 1 : 1 |
| K3 | 2 : 2 |
| K4 | 4 : 8 |
| K5 | 4 : 12; 6 : 52 |
| K6 | 5 : 12; 7 : 180; 8 : 390; 9 : 442 |
| K7 | 8 : 3240; 10 : 20664; 12 : 8864 |

These agree with the frozen artifacts. I separately extracted and executed the literal program printed in the appendix, obtaining `[1, 2, 4, 4, 5, 8]`. Direct evaluation of every displayed witness, including every induced face, confirms its printed extrema and ratio. In particular, the extended K6 witness on K7 has extrema `(-9,11)`, center ratio `21/10`, and maximum face ratio `3`.

The computation is accompanied by the necessary analytic completeness checks. Switching preserves the entire set of quadratic values by the bijection `s -> t*s`. Making the root star positive gives exactly one labeled representative per switching class; a switching preserving the star has all vertex switches equal and hence is trivial on edges. Complementing a cut does not change its weight. The cut-weight formula `c-2h` is exact, and the initial sentinel `|E|+1` exceeds every possible range because the difference of two cut weights contains at most `|E|` signed unit contributions. Thus the printed loop proves a minimum over all full signings, not only attainment by examples.

Restriction and extension give `F_n=max_{2<=k<=n} M_k`: every induced restriction of a complete full signing is again a complete full signing, and assigning arbitrary signs to new edges preserves the old ratio on the zero-fixed face. This proves the all-point values from the center values without claiming monotonicity of the center problem. The distinction from the arbitrary-real coefficient supremum is explicit and correct.

I also independently checked the full analytic chain:

- Multiaffinity replaces graph points by distributions on vertices; compactness gives attainment. The threshold distribution and circular placement of failure intervals give the product envelopes, including means zero and one. Nonnegative coefficients permit simultaneous upper attainment. Positive affine expansion has the stated direction `T_original <= T_expanded` and preserves the full gap.
- At half-valued coordinates, pairing opposite extremizing spins gives `H=R/2` and `T=L/2`. Integer fixed coordinates add only affine terms. Active equality/complementation relations in a cell either fix values to the three-point grid or leave a feasible local perturbation, so the cell-vertex argument supplies the global induced-cut characterization.
- Polarization gives `R=max_S ||A_(S,V\S)||_(infinity->1)` with the stated normalization. Khinchin on both sides of a partition locally optimal for squared weights gives `R >= (1/4) sum_i ||a_i||_2`. The flow network proves the exact fractional-load bound; summing weighted Cauchy–Schwarz then gives `L <= 4 sqrt(rho) R`. Degree and bipartite constants follow with the stated factors. The frustrated four-cycle has `L=4`, `R=2`, density one, and part degrees two.
- The greedy degeneracy orientation proof, arboricity forest-label argument, and connected leaf-dilution example are sound. In that example there are `2q^2` edges and `q^2+2q` vertices, while the induced K_(q,q) retains density `q/2`. The cycle cut-space criterion correctly handles disconnected graphs and, after the repairs, empty support.
- The random-sign argument uses `2^(h-1)` spin classes and two exponentials, hence exactly `h log 2`; Jensen and optimization yield the printed constant. Zeroing outside coefficients proves the center-supremum identity for arbitrary real coefficients. Compactness and perturbation apply to that continuous ratio without assuming continuity of `c*` across support loss.
- For the symmetric matrix pattern, an edge contributes twice only inside `R intersection C`, yielding the stated density comparison and equality. Projective duality counts each undirected edge twice; the second polarization bound contributes `4R`, leading to `4 K_G sqrt(rho) R` as printed. The Sidon comparison and bipartite equality have the correct directions.
- The repaired certificate conventions make the absolute target have slope one and the relative target slope `1-theta>0` in the incumbent. Positivity of the optimal value is explicitly required when setting the relative incumbent to the optimum. No constrained approximation or unrestricted algorithmic lower bound is inferred from envelope ratios.

**Remaining limits.** These finite enumerations prove only the specified full-signing cases through K7. They do not determine larger-n optima or the optimal universal density constant. The universal results rest on the analytic proofs and the stated external norm inequality, not extrapolation from this checker. I did not rerun the LaTeX build or perform a new rendered-page visual audit.

I did not inspect McCormick's 1976 original or the Misener–Smadbeck–Floudas original; the latter attribution was checked through Boland et al., exactly as disclosed by the manuscript. Szarek's bibliographic details were confirmed on the [publisher page](https://www.impan.pl/en/publishing-house/journals-and-series/studia-mathematica/all/58/2/101277/on-the-best-constants-in-the-khinchin-inequality), but its linked full text returned HTTP 403; the sharp real Khinchin inequality remains an accepted external dependency in this review. No claim of a fresh literature-priority search is made.
