# Stage 6, round 1 — independent review 04

**Verdict: PASS.** I found no demonstrable major or minor defect. This is a review of the frozen integrated stage, not the separate final whole-paper acceptance decision.

## Coverage

I reviewed `process/snapshots/stage06-round01`. I independently checked that its 111-page `main.pdf` has SHA256 `343b29156e275df970236babbab1077b3a53261317e0995a6a7ea0398b583916`.

I read the complete frozen `main.tex`, `macros.tex`, and `references.bib`, and all of these manuscript files, including proofs, examples, computational qualifications, and closing discussion:

- `sections/01-foundations.tex`, `02-universal-positive.tex`, `03-cubic-equal-means.tex`, `04-incidence-interiority.tex`, `05-feedback-frequency.tex`, `06-treewidth-two.tex`, `07-positive-boxes.tex`, and `08-exact-complexity.tex`.
- `sections/09-cardinality-spatial.tex`, `10-cardinality-preordering.tex`, `11-coordinate-domains-lifts.tex`, `12-relative-blocks-cuts.tex`, `13-xor-quadratic-hulls.tex`, `14-monomial-reformulations.tex`, `15-finite-certificates-affine.tex`, `16-supporting-comparisons.tex`, and `17-synthesis.tex`.
- `sections/appendix-finite-signings.tex`, `appendix-positive-couplings.tex`, `appendix-cubic-certificates.tex`, `appendix-structural-auxiliary.tex`, `appendix-positive-box-predecessors.tex`, `appendix-point-packing.tex`, `appendix-scaling.tex`, `appendix-p-split.tex`, `appendix-rank-one.tex`, `appendix-fbbt.tex`, and `appendix-integer-comparison.tex`.

I read the frozen `process/review-protocol.md`, `stage-06-review-assignment.md`, `stage-06-author-assignment.md`, `stage-06-author.md`, `scope-proposal.md`, and `claim-coverage.md`. I compared the coverage statements with the manuscript's proved claims and explicit open boundaries. I read the source-location/validation records needed to locate originals; their PASS labels were not used as mathematical evidence. I did not read another current-round review or spawn an agent.

I inspected rendered PDF pages 1, 4, 55–57, 61–64, 93, 96, 99, 102, 105, 108, and 111. This covers the abstract and roadmap, the main focus proofs, representative new appendices, and the bibliography. Equations, tables, references, and page breaks on these pages were readable. I read the entire manuscript in source form; I did not visually inspect every PDF page.

### Primary-source reading

I read repository `literature/AGENTS.md` before consulting originals. The following are actual passage checks, not claims to have read every page of every cited paper. Unless stated otherwise, page numbers below are PDF page numbers, and the material was extracted directly from the original PDF. Paths beginning `literature/` are relative to `/home/sgusev/repo/minlp-notes`.

| Source | Passages actually checked and purpose |
| --- | --- |
| Potechin, `literature/papers/potechin2019-sum-of-squares-lower-bounds/original.pdf` | Pages 3, 8–9, and 18: Theorem 1, Example 18, Theorem 44/proof and Corollary 45. Checked the fractional-cardinality moments and classical attribution. |
| Grigoriev, `literature/papers/grigoriev2001-complexity-of-positivstellensatz-proofs-for/original.pdf` | Pages 1–2 and the construction/Lemmas 1.3–1.4 on pages 5–8, supplemented by the package text. Extraction is partly degraded; this was not a complete audit of Grigoriev's positivity proof. The manuscript supplies its own proof of the sufficient range it needs. |
| Schoenebeck, `/tmp/minlp-relaxation-limits-sources/schoenebeck-full.pdf` | Pages 6–12, especially Definition 10, Theorems 11–12, Lemma 13, and the signed closure/Gram construction. Checked the random-model parameters, width-to-degree conversion, and signed-character construction. |
| Padberg, `literature/papers/padberg1989-the-boolean-quadric-polytope-some/original.pdf` | Page 11, printed page 149: Lemma 2, inequality (17), and its integer-cardinality proof. |
| Davidson–Donsig, `literature/papers/davidson2007-norms-of-schur-multipliers/original.pdf` | Pages 2–4, 6–7, and the relevant proof passage on page 11: factorization, Theorems 1.2/2.4, and the row estimates. Checked the real/complex convention and the density comparison. |
| Luedtke–Namazifar–Linderoth, `literature/papers/luedtke2012-some-results-on-the-strength/original.pdf` | Pages 8–10: vertex-law formulas, Theorems 4–5 and positive-box extension; page 22: Conjecture 1 and its surrounding qualification. |
| Sherali, `literature/papers/sherali1997-convex-envelopes-of-multilinear-functions/original.pdf` | Pages 8–9, printed pages 252–253: equation (13) and Theorem 3. Checked the symmetric-envelope attribution and formula. |
| Cornuéjols, `/tmp/minlp-relaxation-limits-sources/cornuejols-packing-covering.pdf` | Pages 78 and 84: Theorems 6.5 and 6.13. Checked the rectangular Eulerian-submatrix condition and the separate mixed unit-right-hand-side balanced-matrix statement. |
| Hassin–Tamir, `/tmp/minlp-relaxation-limits-sources/hassin-tamir.pdf` | Rendered pages 3–4, printed pages 381–382: Theorems 3.1–3.2, their augmentation proof, and Remark 3.4. The scan has no useful text extraction. |
| Khajavirad, [arXiv:2404.03091v1](https://arxiv.org/html/2404.03091v1) | Original HTML model definitions, Remarks 1–2, Proposition 1 and proof, and Proposition 3 with the SDP definitions/proof. Checked the four reported packing values and the strengthened-bound convention. |
| Balas, `literature/papers/balas1998-disjunctive-programming-properties-of-the/original.pdf` | Pages 5–7, printed pages 7–9: Section 2, Theorem 2.1, proof and corollaries. Checked disaggregation and closure/boundedness distinctions. |
| Wu et al., `literature/papers/wu2026-variable-aggregation-based-perspective-reformulation/original.pdf` | Page 12: Lemma 3/Theorem 3 statements; Assumption 1 and the surrounding setup also checked in the package text. The separately referenced supplementary proofs were not inspected. The manuscript's scaling claims have their own proofs. |
| Starr, `/tmp/minlp-relaxation-limits-sources/starr1969.pdf` | Pages 12–13, printed pages 35–36: Appendix 2, Lemma 2/corollary and proof. |
| Kronqvist et al., `literature/papers/kronqvist2026-p-split-formulations-a-class/original.pdf` | Pages 4–7 and 15–16: assumptions, retained domain, shared auxiliary convention, Definition 4, Theorem 6 and its complete proof. These passages support the precise counterexample target and the directional repair discussion. |
| Lee–Raghavendra–Steurer, `/tmp/minlp-relaxation-limits-sources/lrs-sdpsize.pdf` | Page 23: Theorem 3.8/(3.11); pages 31–34: correlation slack construction, Theorem 5.3 pseudo-density and Theorem 5.4. Checked the quantitative inputs and normalization used in the approximate transfer. |
| Fawzi–Parrilo, `literature/papers/fawzi2013-exponential-lower-bounds-on-fixed/original.pdf` | Page 3: Theorem 1 and the Lorentz-cone decomposition discussion. Checked fixed block order versus total SOC dimension. |
| Braun et al., `/tmp/minlp-relaxation-limits-sources/braun2013-approxlp.pdf` | Page 18: hard pair and Theorem 6(i). Checked that the invoked fixed-dilation LP bound has the required form. |
| Altschuler–Boix-Adserà, `literature/papers/altschuler2023-polynomial-time-algorithms-for-multimarginal/original.pdf` | Page 55: Theorem 7.4, the subsequent inverse-accuracy question, and Corollary 7.5; Definition 7.2 checked in package text. Verified the distinction between polynomial and logarithmic inverse-accuracy dependence. |
| Etessami–Yannakakis, `/tmp/minlp-relaxation-limits-sources/ey-rmc.pdf` | Pages 26–28: Theorem 5.2 and its circuit-normalization, detector, and amplification proof. |
| Stewart–Etessami–Yannakakis, `literature/papers/stewart2015-upper-bounds-for-newtons-method/original.pdf` | Pages 21–22: Section 4.1, equation (18), amplification and repeated-squaring discussion. |
| Esparza et al., `literature/papers/esparza2010-computing-the-least-fixed-point/original.pdf` | Page 34: Section 7, equation (14), Theorem 7.1 and proof. |
| Belotti et al., `literature/papers/belotti2012-on-feasibility-based-bounds-tightening/original.pdf` | Pages 1–2: continuous linear FBBT limit and iterative antecedents; used for context, not as a replacement for the new primitive-update proof. |
| Lubin et al., `literature/papers/lubin2022-mixed-integer-convex-representability/original.pdf` | Page 12: Lemma 4.1 and complete parity argument. |
| Beach et al., `literature/papers/beach2024-enhancements-of-discretization-approaches-for/original.pdf` | Page 21 of the combined preprint: Section 5.1.1 and the sawtooth error. Checked the manuscript's explicit version/numbering qualification. |

I also used the Boland and Adams package text to locate the cut criterion and common-ratio envelope antecedents, but did not perform a fresh full original-PDF proof audit of these two papers. Other bibliography entries were read as manuscript citations, not silently promoted to independently audited sources.

## Findings

None. There are no major or minor finding IDs and no required repairs from this review.

## Independent verification

### Fractional-cardinality positivity and all localizers

For `lem:fractional-positive` in `sections/10-cardinality-preordering.tex` (PDF pages 55–56), I reconstructed the balance recursion directly:

\[
a\frac{$t$_a}{(s)_a}+(s-a)\frac{$t$_{a+1}}{(s)_{a+1}}
=t\frac{$t$_a}{(s)_a}.
\]

The condition on its multiplier gives $a\le 2d-1\le s-1$, so the last moment exists. Homogenization uses a positive denominator under $t\ge2d-1$; the difference from a degree-$d$ homogeneous representative is the balance times a polynomial of degree at most $d-1$. Consequently the multiplier in the square comparison has degree at most $2d-1$, within the stated equality system.

I independently expanded the Gram entry with overlap $h$:

\[
\frac{$t$_{2d-h}}{(s)_{2d-h}}
=\sum_{j=0}^{h}\binom hj
\frac{$t$_{2d-j}(s-t)_j}{(s)_{2d}}.
\]

The incidence matrices attached to the binomial coefficients are Gram matrices. Every scalar coefficient is nonnegative in the claimed range. The Vandermonde verification does not divide by a possibly zero falling factorial of $t$; this matters at the integer boundary.

For `lem:assignment-localizer` (PDF pages 56–57), repeated factors either reduce to zero or to a disjoint assignment indicator. The direct inclusion-exclusion calculation gives indicator weight

\[
\pi=$t$_a(s-t)_b/(s)_{a+b}.
\]

When the square polynomial is nonconstant, $a+b\le2r-2$, so the weight is strictly positive and the conditional parameters satisfy all three remaining-variable/degree inequalities. Constant polynomials and the zero-remaining-variable case are handled separately and require no undefined conditional functional. Thus the proof supplies every allowed product localizer with every global square, rather than only separate coordinate localizers.

I tried the natural boundary counterexample just outside this range. At $s=8,t=5/2,r=2$, the product of four lower slacks has expectation $-1/1792$. This confirms the manuscript's stated obstruction for the full preordering and does not contradict its deliberately stronger sufficient range.

For `thm:preordering-cover`, I checked the strict restriction threshold, surviving one/zero counts, moment objective, and endpoint count together. Fewer than $q_r$ exclusions leave the needed $2r-1$ counts on both sides; the penalty remains strictly below the certification target. The integer/noninteger and $q_r\le0$ qualifications are consistent with this argument.

### Coordinate graph lifts and total-degree tensors

For `thm:local-graph-lift` in `sections/11-coordinate-domains-lifts.tex` (PDF pages 61–62), I checked the affine endpoint substitution without assuming it equals the nonlinear graph on the continuous cube. Restricted coordinates use actual witness tuples; unrestricted coordinates use the two actual endpoint tuples. A locally valid polynomial therefore reduces to a nonnegative combination of endpoint indicators, and a local identity reduces to zero. The substitution cannot increase lifted degree. This proves all localizer and equality products in the stated degree range, even for finite nonpolynomial maps.

The objective argument also survives globally coupled written polynomials: agreement on the full product graph implies equality on every Boolean assignment after substitution, hence identical multilinear reductions. Agreement merely on the balance-feasible graph would not establish that step, and the theorem explicitly excludes that weaker assumption. Retaining original coordinates keeps balance degrees correct.

For `lem:tensor-preordering` in `sections/12-relative-blocks-cuts.tex` (PDF pages 63–64), I checked that the auxiliary tensor matrix does not presume unavailable global moments. For a test $gP^2$, each block matrix indexed by monomials of degree at most $d=\deg P$ is defined and PSD because $\deg g_b+2d\le2r$. The tensor is PSD. Restricting to tuples with total degree at most $d$ gives the required global matrix. Its entries have available global degree; larger unused tensor entries are only a Gram construction. Equality products factor correctly even when other block moments are signed.

In `thm:relative-cover`, I recalculated the light-block pseudoexpectation and heavy-block actual evaluation bounds, the sum-of-exclusions threshold $2q_0G\tau$, and the witness fraction. These yield exponent $q_0G\tau$. The explicit $r=1,t=2,\theta=\eta=1/32$ example gives $\tau=17/128$ and exponent $17n/384$. The text requires a positive-τ fixed-parameter regime and does not assert a uniform positive relative tolerance for arbitrarily growing order. I also checked the clique escape cut by its integer-cardinality polynomial and its continuous multiaffine extension.

### The remaining core arguments

I checked the proof chains beyond my additional focus, including these possible failure points:

- The vertex-law model preserves the full mean vector; the positive common upper law and signed cut conversion use the specified decomposition. The induced half-grid argument, fractional orientation, and row estimate give the asserted graph-density order. I did not infer sharp numerical Grothendieck constants from the order comparison.
- The harmonic coupling has the required normalization and inactive-mass bound. Dyadic and variable-radix count laws are distinct regimes. The cubic scalar inequality and certificate arguments do not use finite numerical searches as universal proofs.
- The frequency-two rank argument treats dummy and parallel edges; odd-cycle rounding retains the baseline. The width-two series/parallel proof keeps its full boundary invariant. Its TU step uses the stated Camion criterion, not an implication from balancedness alone.
- Positive-box orientation is sampled in a fixed ambient space and then restricted. The finite minimum/maximum spreading and coefficient comparison produce the claimed $L+1+\beta_N$ expression without a general Schur-concavity assertion.
- The single-product PARTITION reduction keeps rational separation and certificate bit length under control. Its rank-one MOT consequence is about exact/high-precision computation, not fixed-error hardness.
- The XOR transfer consumes degree $4r$, and monomial pullback consumes $4rD$. A signed PSD degree-two matrix has an actual sign law, with the constant vector's class included. Restriction uses deterministic substitution and marginalization. Quadratic realization is on the full coordinate domain and need not satisfy the lifted graph pointwise. The parity-rank count uses the union of supports of basis rows, not the number of repeated auxiliary names.
- The bounded-occurrence deletion, random-sign tail, and source event intersection give the stated size/objective regime. The order-one upper certificate uses the available quadratic distribution plus expected graph identities; it does not assume graph support. The finite exponential upper certificates and arbitrary affine branching boundary remain distinguished.

### Stage 6 supporting additions

I reconstructed each new appendix's argument, with these explicit cross-checks:

- `prop:packing-values`: averaging pairwise variance gives $k\operatorname{tr}X-\mathbf1^{\mathsf T}X\mathbf1$, and the interval secants bound it by $k^2L^2/4$. The displayed covariance constructions and cross-group means attain the four values, including RLT feasibility. The half-box symmetry uses recomputed secants and $n\ge5$.
- `prop:scale-hull`, `prop:scale-perspective`, and `prop:scale-rectangularity`: endpoint disaggregation keeps the shared operating variable. Zero weights use compactness. Product weights attain the extensive-only operating-cost and scale-cost bounds simultaneously. The separating cost in the rectangularity necessity argument forces the indicated contracted fibre. No independent scalar perspective is applied to an unscaled intensive coordinate.
- `ex:psplit-exact-box` and `prop:psplit-repair`: the retained domain and shared auxiliary really matter in the published model. The box example has all four vertices in the disjunctive union; the repair preserves zero-slack links and the domain. For `prop:psplit-balls`, I eliminated the auxiliary hull at fixed transverse square sum and differentiated the squared distance in $\rho^2$, obtaining the maximum at $\rho=r$ and the limit $\sqrt2-1$. I checked the rational orthogonal map and why an exact auxiliary-image hull alone still leaves the stated witness feasible.
- `prop:correlation-face` and `prop:correlation-stability`: the atom face, exposure, and inverse projection are consistent. The rounding steps give $4SB+58SD+5|m-S|$; convex-mixture control yields $184m+6$, followed by the additional factor $m$ in the projection. Exact fixed-block PSD/SOC bounds and unrestricted PSD order are kept separate. In `prop:rank-one-approximation`, the shifted pseudo-density input gives the stated prefactor exponent $-23/4$; the residual scalar block accounts for the $q+1$ factorization size.
- `lem:fbbt-fixed-point`: fair forward updates dominate every finite Kleene iterate while sound contraction preserves the least fixed point. In `prop:fbbt-hardness`, the detector roots, amplifier, rational cube feasibility, variable names, and four-vertex SCC bound check out. In `prop:fbbt-iterations`, the primitive-update invariant limits progress under every permitted schedule, and the input bit-length qualification is stated. This is neither an arithmetic lower bound for stronger solvers nor a Newton-method claim.
- Appendix K: square midpoint error, the product area estimate, closed parity classes, coordinate-width control, and the shared binary expansion upper bound give the stated precision counts. These counts concern integer assignments/parity classes and are not relabeled as spatially certified regions.

### Computation performed

I wrote and ran `verification/reviewer04/stage06-round01/check_cardinality.py`. Its output is `check_cardinality.json` in the same directory. It uses rational arithmetic for identities and localizer entries, and floating point only for the final eigenvalue diagnostics:

- 350 exact homogeneous Gram-entry identities.
- 500 exact balance identities.
- 7,350 exact conditional-moment identities, including boundary parameters.
- 170 two-block localizer PSD diagnostics at orders one and two; the largest matrix has 137 rows. The minimum computed eigenvalue was approximately $-1.81\times10^{-15}$, consistent with rounding at zero and above the check tolerance $-10^{-10}$.
- The exact negative four-slack example $-1/1792$.

These checks cover finite selected parameters and squarefree Boolean bases. The analytic quotient and degree arguments above, not numerical PSD tests, establish treatment of arbitrary repeated powers and universal orders.

I also replayed the frozen exact cubic certificate script and the frozen complete-signing enumeration routines for $K_2,\ldots,K_7$. The cubic checks passed; the minimum cut ranges were $1,2,4,4,5,8$. Outputs are `cubic-replay.txt` and `signing-replay.json` under my verification directory. These are replays of author routines, not independent algorithm implementations. I invoked the signing routines without their frozen-output writer. No manuscript or frozen artifact was changed.

## Remaining limits

This review is not a formal proof verification or an exhaustive search for counterexamples. I did not rerun every historical repository experiment, every solver-dependent check, or the complete build pipeline. The new exact arithmetic tests and selected PDF inspection supplement the proof reading.

External theorems remain external inputs. In particular, I checked Schoenebeck's width statement and the relevant signed construction but did not independently reprove the random-resolution-width theorem in its appendix. I checked the needed LRS, Braun, and Fawzi statements/parameters rather than redoing their complete extension-complexity proofs. Grigoriev's degraded extraction and Wu's uninspected supplementary proof are explicit source-reading limits. I did not freshly audit every contextual predecessor in the bibliography, including Jarre/Coniglio, or the complete classical matching, Khinchin, and optimization–separation literature. None of these limits is being represented as a completed source audit.

The manuscript correctly leaves exact cubic and higher-width constants, finer asymptotics, unequal-aspect structural extensions, and unrestricted affine/coupled-oracle branching outside its proved conclusions. I found no claim in the reviewed stage that requires those open questions to have been solved.
