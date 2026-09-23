# Reviewer 14 — stage 2, round 1

Primary lens: primary-source hypotheses, bibliography, accurate credit, and bounded novelty claims. I also independently reconstructed the mathematical chain across the complete stage.

Major findings: 0
Minor findings: 0

I did not identify a false theorem, material proof gap, source-hypothesis mismatch, or inaccurate priority assertion in the reviewed stage. The rational nc-rank preview now has an explicit upper construction and a uniform capacity-based lower estimate. The finite algorithm distinguishes rational stored iterates from conceptual exact updates, and its oracle reductions state the inner-ball, outer-ball, separation, and precision assumptions needed by the imported results. The error-body reductions retain the actual input domain and account for volume loss.

There are no numbered findings or unresolved questions to report. This assessment is limited to the review described below; it is not a claim of formal verification or established publication priority.

## Frozen files and verification

I checked all six SHA-256 hashes against `reviews/stage2-round1/snapshot.json`; all matched:

| File | SHA-256 |
| --- | --- |
| `coverage.md` | `04faf5b34942a13d79028d42728aeb6443b34c66a575f8293bc546a1ec8fb47e` |
| `macros.tex` | `3f613a2cf8ebf1bd4c6c84b531de0e74479e07a19ce7566961f1348384de7a3f` |
| `main.tex` | `92931390c89c837f079fa63121c50d7fd2ad9b5ff7b4cab8ff88276f2206e177` |
| `references.bib` | `3dcfb568784b51d38f1255ff6135ecefa8be1b9c17b1fef7e8927764022bc900` |
| `sections/01-foundations.tex` | `3108dc02b31b4812fe7fffb444e637a2c846e00268d750262e363dfdb1ded37e` |
| `sections/02-quadratic-finite.tex` | `2d6d05e3f346561242f44ecab130c9b01016b101bb4843eaeb11724eef7a9d2d` |

I read all 1,546 lines of `sections/02-quadratic-finite.tex`, the stage-1 parity, prefix/product, principal-compression, symmetric-shrinking, covariance, capacity-bound, and rational-preview dependencies, the bibliography, the stage-2 coverage and supporting-development entries, `PROCESS.md`, and the review protocol/task/lenses. I had previously read the complete stage-1 draft as reviewer14; for this round I reread the relevant dependencies in the corrected snapshot rather than assuming their previous line numbers or statements were unchanged.

I compared the statements and scope of all thirteen stage-2 canonical results listed in `coverage.md` with the manuscript. I made closer proof comparisons for the weighted rational construction, rational nc-rank construction, general output body, l1 oracle, commuting reduction, and block logdet oracle. This was a targeted source comparison, not a complete reread of all original result files or all 196 supporting notes. The six explicit stage-2 supporting developments are present in the manuscript. Later stages were not reviewed.

## Primary-source interfaces checked

The following checks used the primary papers themselves, including the cached extracted texts. The root audit was read as a checklist, not used in place of those sources or the manuscript proofs.

- **IQS, Theorem 1.5 and Lemma 5.3.** The cached February 2018 manuscript explicitly constructs an `(n-r)`-shrunk subspace over the base field and states polynomial size for intermediate and final rational data. Lemma 5.3 gives invariance under field extension. The manuscript supplies a rational linear basis and works over the infinite field of rationals, satisfying the stated field-size hypothesis. The bibliography deliberately identifies the revised full manuscript whose theorem numbering is used. [Primary manuscript](https://arxiv.org/pdf/1512.03531).
- **GGOW, Theorem 2.18.** The source applies to rank-nondecreasing completely positive operators with integral Kraus matrices and gives capacity at least `n^(-2n)`. Clearing the denominator of the principal compressed Hessians supplies exactly these hypotheses. Scaling capacity by `D_H^(-2r)` is consistent with the determinant-ratio definition. The stage-1 full-rank and capacity interface supplies rank nondecrease. [Primary published paper](https://www.math.ias.edu/~avi/PUBLICATIONS/GargGOW20.pdf).
- **Zhang–Sra, Corollary 8 and its proof, printed pages 8–9.** The source gives the one-step squared-distance comparison with curvature factor evaluated at the distance to the comparison point. Its proof separates the unprojected triangle estimate from nonexpansive projection. This supports the manuscript's use when the rational stored iterate lies in the slightly enlarged ball and projection is onto the original ball. The manuscript derives its own local rounding and telescoping terms rather than importing a theorem for exact iterates unchanged. [Primary proceedings paper](https://proceedings.mlr.press/v49/zhang16b.pdf).
- **Criscitiello–Boumal, Appendix I, printed pages 70–71.** The cached arXiv v2 uses precisely `tr(P^-1 X P^-1 Y)` and states that this cone is Hadamard; Proposition I.1 gives curvature lower bound `-1/2`. The weaker `-1` used here is valid. The source treats order at least two; order one is flat and causes no exception to the manuscript's weaker bound. The bibliography's note identifies the version containing this appendix. [Primary manuscript](https://arxiv.org/abs/2008.02252).
- **GLS1981, Definition (5), printed page 172, and Theorem (3.1), printed page 177.** The actual weak-optimization definition promises both distance at most epsilon from the body and objective loss at most epsilon against every point of the original body. It does not restrict the comparison to an eroded body. The manuscript supplies known balls for both correlation-matrix and logdet-hypograph applications. The strong spectral separators, tangent separators, normalization, and exact central-ball/correlation repairs are compatible with this interface. The correlation dimension-one cases are handled separately; the logdet hypograph has dimension at least two. [Primary paper](https://ir.cwi.nl/pub/10046/10046D.pdf).
- **Dadush–Peikert–Vempala, Definition B.2 and Theorem B.5, printed pages 37–38.** The source requires polynomial-height rational strong separation and explicit outer bounds; it returns a rational positive definite shape matrix, a potentially real center, and factor `(d+1)sqrt(d)` with the stated small-volume alternative. The manuscript's rational lower-volume threshold excludes that alternative, and symmetry removes the center by convex averaging. No rational center or exact matrix square root is assumed. [Primary full manuscript](https://sites.cc.gatech.edu/fac/cpeikert/pubs/svp-anynorm.pdf).
- **Del Pia, Theorem 2.** The cached July 31, 2026 primary manuscript states rational orthogonal near-diagonalization and polynomial Turing complexity for rational input. Its title, author, year, and arXiv identifier match the bibliography. The citation is limited to this spectral ingredient; the manuscript proves its own needed residual lemma and does not attribute a graph-formulation theorem to Del Pia. [Primary manuscript](https://arxiv.org/abs/2607.29386).
- **Briët–de Oliveira Filho–Vallentin.** The primary manuscript's introduction states the PSD `2/pi` ratio and the Rietz/Nesterov attribution, and its publication record matches ICALP 2010, LNCS 6198, pages 31–42. The manuscript uses only the inequality, for which it also gives the Gaussian-sign/Schur-power proof; it does not mistake randomized rounding for its deterministic correlation-SDP oracle. [Primary manuscript](https://arxiv.org/html/0910.5765v3).
- **Sra–Hosseini and MAXDET.** The primary NIPS2013 proceedings paper discusses positive definite geodesic geometry and geodesic convexity; the broad contextual citation is appropriate because the specific quadratic energy expansion is proved here. Vandenberghe–Boyd–Wu's author-hosted page confirms the stated title, journal, volume, pages, and determinant-maximization context. The manuscript explicitly separates these classical objectives and algorithms from its formulation consequences. [Sra–Hosseini](https://proceedings.neurips.cc/paper_files/paper/2013/file/3948ead63a9f2944218de038d8934305-Paper.pdf), [MAXDET primary page](https://web.stanford.edu/~boyd/papers/maxdet.html).
- **Cao and Max-Cut context.** Cao's publisher page confirms the 2007 metadata and the derivative-based ellipsoid/anisotropic-interpolation connection; no specific unverified Cao theorem is required by the proof. I opened the cited Garey–Johnson–Stockmeyer scan and inspected its title/first page, which identifies Simple MAX CUT among its completeness results. The manuscript's zero-recognition coNP statement is expressly restricted to its graph family. [Cao publisher page](https://epubs.siam.org/doi/10.1137/060667992), [Garey–Johnson–Stockmeyer primary scan](https://www.math.ucdavis.edu/~deloera/MISC/LA-BIBLIO/trunk/JohnsonDavid2.pdf).

## Independent mathematical reconstruction

I checked the covariance scaling constants and the shared symmetric-monomial error calculation, including the factor-eight slack and endpoint representation. I checked the Lagrangian determinant certificate, the geometric-mean sign symmetrization, the scalar allocation formula, and the distinction between the Frobenius benchmark's dimension gap and a universal algorithmic lower bound.

For the rational algorithm I checked the Jacobi off-norm contraction, exact common-denominator bookkeeping, gap-free matrix-function reduction, trace-one branch gradients, polynomial-radius bound, local inexact recurrence, feasibility repair, and determinant loss of the final rational grid. I recomputed the displayed inexact-oracle budget `3n/(512n)+D/[128(D+1)] < 1/32` and checked that the iteration/rounding constants leave the stated objective margin.

For output budgets I checked the PSD factorization used only in the proof, rational grouped gradients, zero-energy detection, l1 correlation repair, nonlinear-output-image equivalence, and body-radius pullbacks. For the input quotient I checked affine terms varying along fibers, the rational zonotope separator, LDL scaling, and the normalized domain-volume bound. For the positive structures I checked unconditional domination, expected Jensen vectors, block determinant comparison, blockwise quotient domains, the direct logdet interior ball and exact repair, the diagonal constants, independent integer minors, and forest face tiling. I also checked the thin-domain example and the Max-Cut replication/positive-optimum gadget, including the distinction between power-sublinear hardness and the unexcluded `N/log N` scale.

## Executed checks and limitations

- Executed a Python SHA-256 comparison for every frozen file; all six matched.
- Read cached primary-source theorem statements and retrieved additional primary proceedings/author/publisher pages for bibliography and contextual claims.
- Downloaded and rendered the cited scanned Garey–Johnson–Stockmeyer first page to inspect the otherwise non-searchable source. I did not reread its entire NP-completeness reduction.
- No full numerical solver or classical oracle algorithm was implemented or executed for this review. The validation of the universal construction is by the mathematical proof and the checked imported interfaces, not by the root's passing script labels.
- No complete visual layout audit or fresh LaTeX build was performed. I did not perform an exhaustive novelty search or verify every legacy stage-1 bibliography field anew.
- No manuscript, bibliography, original result, or other review was edited; no subagents were used.
