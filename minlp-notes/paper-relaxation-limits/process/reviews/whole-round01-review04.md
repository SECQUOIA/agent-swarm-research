# Independent final whole-paper review 04

## Verdict

**PASS.** I found no major or minor defect requiring a manuscript repair. This is an independent review of the complete frozen manuscript, with additional attention to cardinality pseudoexpectations, full slack-product localizers, coordinate graph lifts, and tensor positivity. It does not adopt earlier acceptance decisions as evidence.

Target: `process/snapshots/whole-round01/main.pdf`, 111 pages, independently verified SHA256:

```text
912de166731f56368a8ee4db21294aa348b85364e85cd444e31265b29828d084
```

The verdict concerns the claims and qualifications actually stated. In particular, the paper distinguishes pointwise envelope widths, scalar envelope evaluation, node relaxation strength, spatial region counts, and global extension complexity. Its restricted lower bounds do not imply impossibility for arbitrary algorithms or arbitrary additional constraints.

## Coverage

I read `main.tex`, `macros.tex`, `references.bib`, and every file below in its entirety, including proofs, appendix code, tables, and qualifications. Paths in this list are relative to the frozen snapshot's `sections/` directory.

```text
01-foundations.tex
02-universal-positive.tex
03-cubic-equal-means.tex
04-incidence-interiority.tex
05-feedback-frequency.tex
06-treewidth-two.tex
07-positive-boxes.tex
08-exact-complexity.tex
09-cardinality-spatial.tex
10-cardinality-preordering.tex
11-coordinate-domains-lifts.tex
12-relative-blocks-cuts.tex
13-xor-quadratic-hulls.tex
14-monomial-reformulations.tex
15-finite-certificates-affine.tex
16-supporting-comparisons.tex
17-synthesis.tex
appendix-finite-signings.tex
appendix-positive-couplings.tex
appendix-cubic-certificates.tex
appendix-structural-auxiliary.tex
appendix-positive-box-predecessors.tex
appendix-point-packing.tex
appendix-scaling.tex
appendix-p-split.tex
appendix-rank-one.tex
appendix-fbbt.tex
appendix-integer-comparison.tex
```

I also read the frozen `README.md` and the complete process files `review-protocol.md`, `whole-paper-review-assignment.md`, `scope-proposal.md`, `claim-coverage.md`, `stage-06-author.md`, `stage06-corrections.md`, and `stage06-reviewer-focus.json`. I checked the scope and coverage ledger against the manuscript, rather than treating the ledger's status labels as verification. I did not read other reports from this final round, delegate work, or edit the manuscript or snapshot.

I read `literature/AGENTS.md` before using local originals. The following are the primary-source passages independently inspected in this review. These are targeted source audits, not claims to have read each cited work in its entirety. Packaged-source locators below use the actual `fulltext.md` page markers; the originals were used to check the important source formulas or statements. Files in `/tmp/minlp-relaxation-limits-sources/` are identified separately by their filenames and PDF page numbers.

| Source | Passages inspected and purpose |
| --- | --- |
| [[potechin2019-sum-of-squares-lower-bounds]] p.3, p.8, p.18 | Theorem 1, Example 18, Theorem 44 and Corollary 45; degree conventions, fractional-knapsack moments, and the distinction between the sharper moment range and the manuscript's sufficient full-preordering range. Original PDF page 8 also inspected visually. |
| [[grigoriev2001-complexity-of-positivstellensatz-proofs-for]] p.5, p.7-8, p.16 | Main theorem, fractional-cardinality functional, balance and positivity lemmas, and final positivity formula. Original PDF page 7 inspected visually because extraction is poor. The entire spectral proof was not rederived. |
| `schoenebeck-full.pdf` and `.txt` | PDF pages 6–11: random model, Theorems 11–12, Lemma 13 and its signed-character construction, and Remark 1. Pages 16–19: the relevant width lower-bound appendix, including Theorem 21 and Proposition 22. Original page 7 inspected visually; the author's public PDF was also accessible. |
| `cornuejols-packing-covering.pdf` and `.txt` | Theorems 6.5 and 6.13 with their surrounding proofs: the Camion criterion and the balanced mixed-system integrality input. No raster inspection of this source. |
| `hassin-tamir.pdf` | Original PDF page 3, printed page 381, visually inspected because text extraction is empty: Theorem 3.1 and the series-parallel block and recursive definitions relevant to the structural input. |
| [[davidson2007-norms-of-schur-multipliers]] p.4, p.6-7 | Theorem 1.2 and Theorems 2.3–2.4; real Grothendieck convention and the density/row-decomposition norm bounds. Original PDF text extraction checked the equations that the Markdown extraction damages. |
| [[luedtke2012-some-results-on-the-strength]] p.22 | Positive multilinear Conjecture 1 and the conclusion, checked against the original. |
| [[padberg1989-the-boolean-quadric-polytope-some]] p.11 | Lemma 2, clique inequality (17), and its proof; coefficient and sign conversion for the root clique-cut comparison. |
| [[kronqvist2026-p-split-formulations-a-class]] p.4-7, p.15-16 | Retained domain, assumptions, minimal auxiliary convention, formulations, Definition 4, Corollary 3, and Theorem 6 with its proof. Original page 16 also inspected visually; the strict-Jensen step and the retained-domain issue match the manuscript's qualified counterexample discussion. |
| [[fawzi2013-exponential-lower-bounds-on-fixed]] p.3 | Theorem 1, its constants, and the second-order cone interpretation; the full external lower-bound proof was not audited. |
| `lrs-sdpsize.pdf` | Original PDF page 23, Theorem 3.8 and (3.11), including the denominator, exponent and prefactor; pages 32–34, Theorems 5.3–5.4 and the pseudo-density construction and norm calculation. Page 23 also visually inspected. |
| `braun2013-approxlp.pdf` | Original PDF page 18: the hard pair and Theorem 6(i), checked for the stated LP approximation comparison. |
| [[belotti2012-on-feasibility-based-bounds-tightening]] p.14 | Theorem 4.1 and its nonempty-limit hypothesis, checked in the original. |
| `ey-rmc.pdf` | Original PDF pages 26–28: Theorem 5.2 and the PosSLP normalization, detection and amplification construction. |

The bibliography was read in full, but I did not independently open every bibliography item's original. In particular, contextual citations to Khajavirad, Anstreicher, GLS, Karp, Szarek, Sherali, matching and transport literature, Jarre, Coniglio, Ahmadi/Stabbing Planes, Balas/Wu/Starr, Stewart/Esparza, Lubin, and Beach were not separately audited against their originals in this final review. This limits the independent bibliographic and historical clearance; it does not replace the direct examination of the manuscript's proofs. The explicitly unresolved Coniglio version identity remains unresolved by this review.

## Findings

No major or minor findings. No repair requested.

The copied build has three underfull-box diagnostics, but no final unresolved-reference, citation, multiply-defined-label, or overfull-box warning. I do not classify an underfull-box diagnostic by itself as a manuscript defect; the sampled rendered pages were readable. I also do not classify a correctly disclosed external-source or open-problem limit as a defect.

## Independent verification

### Whole-manuscript mathematical audit

I reconstructed the arguments and tested their vulnerable implications, not just their displayed conclusions. The following summarizes that audit across the entire manuscript.

* **Foundations and universal bounds:** checked the vertex-law formulation, the common positive upper envelope, the signed bilinear cut identities, the real row-norm comparison, and the use of full-support marginals in taking the supremum. For the positive coupling, I followed the inactive mass, tangent construction, harmonic quantities, and fixed cutoff through both the upper bound and sharp examples. I checked dyadic/radix attainment and the dimension interpolation rather than identifying a limiting construction with finite attainment.
* **Cubics:** kept scalar envelope complexity distinct from the equal-mean family statements. I followed the reductions to count states, primal and dual certificates, and exact ratio comparisons. I checked the role of unused coordinates and replayed all printed finite integer checks described below.
* **Incidence, feedback, and low treewidth:** checked ownership in the incidence argument, the residual-law gluing after fixing feedback variables, and the cloning argument's uniformity over the required family. I followed the degree-slab decomposition, the odd-cycle baseline, cardinality matching, all seven series-parallel coloring cases, and the total-unimodularity/integrality step. Degenerate residual and empty-support cases did not reveal an omitted assumption.
* **Positive boxes and exact complexity:** checked the coefficient spreading estimates using the global minimum and maximum, the fixed ambient orientation of the bounds, and the distinction between the common-aspect special case and general positive physical boxes. I followed the narrow rational PARTITION reduction and its encoding precision; the claimed exact complexity is not being inferred from an approximate optimization statement.
* **Cardinality, coordinate domains, relative blocks, and quadratic cuts:** the detailed checks are given below. I also checked the root clique-cut escape against the lower bound's stated scope. The paper does not claim its uncoupled construction survives every valid quadratic cut.
* **XOR and monomial reformulations:** checked source-degree versus relaxation-order conversion, the signed-character equivalence classes, and how a positive degree-two Boolean moment matrix with entries in `0,±1` yields the actual finite Boolean law used for the quadratic hull. Product localizers consume the stated source degree; a moment-matrix-only assertion would not suffice. In the random-instance step, I checked the bounded-occurrence deletion calculation, including `48 e^24 / 2^64 < 1/8`, the surviving `m >= 7n`, occurrence bound 64, and the resulting exponent `7n/1024`. The monomial transfer's `4rD` budget, support union bounded by `Dq`, and the order-one degree-three reformulation with `N <= 17n` are consistent. I checked that the quadratic law is claimed on the lifted box, while graph equalities have their separate pullback argument.
* **Finite certificates and supporting comparisons:** followed point packing, tolerance scaling, finite affine realization, positive-box predecessor reductions, the retained-domain P-split example, the rank-one face and affine-section distinction, the FBBT examples and fixed-point hypothesis, and the integer/real comparison with its rational amplification. For the extension-complexity comparisons I checked the imported theorem hypotheses and substitutions at the passages listed above; I did not independently reprove the general external rank lower bounds.

### Cardinality positivity and all localizers

Write the squarefree moment as

\[
E_{s,t}[u_S]=(t)_{|S|}/(s)_{|S|}.
\]

I checked the balance recurrence through degree `2d-1`, including the available-moment boundary. Homogenization from degree `a` to degree `d` uses

\[
H_S=\binom{t-a}{d-a}^{-1}
       \sum_{T\supseteq S,\ |T|=d}u_T.
\]

Under the stated sufficient range, its denominator is positive. The difference is a multiple of `sum u - t` modulo the Boolean equations, with the multiplier degree small enough to compare the two squares. This is needed to pass from the homogeneous matrix to arbitrary polynomials.

For the homogeneous matrix, I verified the coefficient identity

\[
N=\sum_{j=0}^d
 \frac{(t)_{2d-j}(s-t)_j}{(s)_{2d}}P_j,
\qquad P_j(I,J)=\binom{|I\cap J|}{j}.
\]

Each `P_j` is an incidence Gram matrix. The coefficients are nonnegative for `t,s-t >= 2d-1`, including endpoint zeros. The Vandermonde identity proving the formula does not require division by a possibly zero falling factorial.

I then reduced an arbitrary repeated slack product to either zero or an assignment indicator `I_{A,B}`. Its mass is

\[
\pi=\frac{(t)_{|A|}(s-t)_{|B|}}{(s)_{|A|+|B|}},
\]

and conditioning gives `pi E_{s-|A|-|B|,t-|A|}` on the remaining variables. I checked the residual inequalities at the exact degree allowed for the squared polynomial, as well as constant polynomials, zero mass, and fully assigned indicators. Thus the proof addresses every admissible slack-product localizer. The manuscript's stronger sufficient range is appropriate here: for example, at `s=6,t=5/2`, a four-one slack product has negative expectation. The sharper source range for a moment matrix cannot simply replace the preordering assumptions.

For the spatial counting step, I checked the three terms in

\[
q_r=\min\{k-2r+2,\ z-2r+2,\ m(1/2-2\varepsilon)\}.
\]

Fewer than `q_r` exclusions leave enough one and zero coordinates for the fractional law, and the retained witness has cost strictly below the target. The probabilistic avoidance bound uses the one and zero witness sets correctly; it does not require an unjustified independence assumption between them.

### Coordinate graph lifts and tensor positivity

For arbitrary coordinate domains, I checked that the proof uses membership of the relevant endpoints and witness values, without assuming compactness or requiring the pseudo-mean itself to belong to the domain. For each coordinate graph map, affine interpolation of its two actual endpoint tuples agrees with the graph on every Boolean assignment. On restricted coordinates the substitution uses the actual witness tuple. Therefore polynomial expressions in lifted variables do not increase degree under this substitution, even if an underlying coordinate map is nonpolynomial or a high-degree polynomial. The separate literal-polynomial `rD` statement has a different degree budget and is not silently used as a substitute. Retaining original coordinates and the stated graph/objective identities is essential and is stated.

For a product of independent block laws, I reconstructed the global localizer matrix from the block matrices indexed by monomials up to the allowed square degree. Their tensor product is positive semidefinite; the matrix for all global monomials of total degree at most that bound is a principal submatrix. This covers squares coupling several blocks. Some entries of the auxiliary tensor matrix refer to larger total degrees, but they are used only to construct a Gram matrix, not asserted as additional moments of the truncated global functional.

In the relative-gap construction, the light/heavy-block division and the penalty bound give `sum_b |R_b| >= 2 q_0 G tau` with `q_0=t-2r+2`. I checked the consequent product-measure exponent and the explicit `r=1,t=2` specialization: `tau=17/128` and exponent `17n/384`. The perturbations distinguish the blocks under the stated translated coefficient symmetries; the proof does not depend on a nonexistent blockwise independence inside one globally coupled square.

### Exact executable checks

I wrote and ran `verification/reviewer04/whole-round01/check_focus.py` using Python standard-library rational arithmetic. It does not read prior check results. The resulting `checks.json` records:

| Check | Result |
| --- | --- |
| Homogeneous Gram entry/coefficient identities | 568 exact checks |
| Cardinality balance recurrences | 492 exact checks |
| Indicator finite-difference and conditioning identities | 3,681 exact checks |
| Conditioned degree/parameter inequalities | 662 exact checks |
| Global two-block localizer | Exact rational PSD verification of a 15-by-15 matrix |
| Graph endpoint substitutions | 16 Boolean assignments |
| Printed appendix integer programs replayed | Both passed |

The moment checks cover orders 1 through 3, sizes up to 12, and half-integer values throughout the stated sampled sufficient ranges. The two-block test uses seven variables per block, `t=7/2`, order 2, localizer `u_0(1-u_7)`, and basis consisting of the constant and all 14 original variables. Both blocks satisfy the full-preordering parameter assumptions. Rational Schur elimination, including zero-pivot handling, verifies positivity of the entire matrix, and hence all coupled linear squares in this test.

The graph test uses endpoint values of `x(1-x)` and `x^17+2x`; it is a finite sanity check of endpoint interpolation, not a proof for every possible coordinate map.

I extracted and executed the code printed in the frozen finite-signing and cubic appendices. The signing enumeration returns `[1,2,4,4,5,8]` for orders 2 through 7. The cubic program checks its count-state and pair-state grids and reports that all finite cubic certificates passed. Outputs are retained as `appendix-finite-signings.tex.replay.txt` and `appendix-cubic-certificates.tex.replay.txt`. Replaying these programs independently verifies the published finite arithmetic, while the universal statements rely on the separately reviewed reductions and proofs. No floating-point numerical experiment is being used as proof.

### Build and visual checks

I copied the frozen build inputs into `verification/reviewer04/whole-round01/build/` and ran a fresh `latexmk -pdf -interaction=nonstopmode -halt-on-error main.tex` there. It completed successfully with 111 pages. A complete `pdftotext -layout` extraction of the rebuilt PDF is byte-for-byte equal to the same extraction of the frozen PDF. I do not claim equality of PDF binaries, whose build metadata can differ.

The final `main.log` has three underfull-box messages and no unresolved-reference/citation, multiply-defined-label, or overfull-box warning. First-pass undefined-reference messages in the multi-pass build transcript are not final build failures.

I visually inspected frozen PDF pages 1, 23, 56, 61, 64, 86, 96, and 110, and copied-build page 58. These samples cover the opening, mathematical displays, the focus sections, appendix code, and references. I found no clipping or unreadable content in these samples. Source and manuscript renders are retained under `verification/reviewer04/whole-round01/renders/`.

## Remaining limits

* This review includes complete manuscript-source reading and complete extracted-PDF equality checking, but only nine manuscript pages were inspected as rendered images. It is not an every-page raster proofread.
* The exact computations are finite checks. They neither establish universal positivity nor enumerate all dimensions, graph families, coordinate maps, reformulations, or theorem parameters.
* The primary-source audit is limited to the passages recorded above. General external results, including the deeper rank lower bounds, are accepted at their cited theorem level after checking the applications. Bibliographic priority and all contextual citations have not received an exhaustive original-source audit.
* The manuscript's stated open problems and scope restrictions remain. In particular, the spatial bounds do not settle arbitrary-region complexity, arbitrary reformulations, or the effect of unrestricted extra constraints. I found no place where those unresolved questions were needed to complete a proof of a claimed theorem.

Within those limits, I found the complete frozen manuscript mathematically coherent, reproducible in its printed finite computations, and consistent with its stated coverage and qualifications.
