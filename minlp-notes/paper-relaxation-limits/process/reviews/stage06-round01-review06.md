# Stage 6, round 1 — independent review 06

**Verdict: PASS.** I found no demonstrated major or minor defect in the frozen manuscript. This verdict concerns the stated theorems and scope; it does not replace the separate final whole-paper review.

## Coverage

I reviewed `process/snapshots/stage06-round01/`. The 111-page `main.pdf` has SHA256 `343b29156e275df970236babbab1077b3a53261317e0995a6a7ea0398b583916`, independently recomputed by my checker. I read the frozen review protocol, Stage 6 review assignment, author assignment and author record, complete scope proposal and claim-coverage ledger. I did not read another current-round review or use historical PASS labels as proof.

I read `main.tex`, `macros.tex`, `references.bib`, and every included section file in full:

- `01-foundations.tex`, `02-universal-positive.tex`, `03-cubic-equal-means.tex`, `04-incidence-interiority.tex`, `05-feedback-frequency.tex`, `06-treewidth-two.tex`, `07-positive-boxes.tex`, `08-exact-complexity.tex`;
- `09-cardinality-spatial.tex`, `10-cardinality-preordering.tex`, `11-coordinate-domains-lifts.tex`, `12-relative-blocks-cuts.tex`, `13-xor-quadratic-hulls.tex`, `14-monomial-reformulations.tex`, `15-finite-certificates-affine.tex`, `16-supporting-comparisons.tex`, `17-synthesis.tex`;
- `appendix-finite-signings.tex`, `appendix-positive-couplings.tex`, `appendix-cubic-certificates.tex`, `appendix-structural-auxiliary.tex`, `appendix-positive-box-predecessors.tex`, `appendix-point-packing.tex`, `appendix-scaling.tex`, `appendix-p-split.tex`, `appendix-rank-one.tex`, `appendix-fbbt.tex`, `appendix-integer-comparison.tex`.

The additional packing focus did not narrow that reading. I checked the roadmap, abstract, introductory attribution and final open-status statements against the mathematics and coverage rows. The ledger preserves the distinction between positive-gap examples, signed spatial examples, global lift size, local propagation and integer precision. I found no missing required development at the specified proved or open status. This is a manuscript-to-ledger audit, not a fresh line-by-line audit of every historical repository note.

I read `literature/AGENTS.md` before originals. Primary-source verification was targeted, not an end-to-end rereading of every cited paper. Important formulas were checked in original PDF extraction or original rendered pages; local synthesis notes were not treated as theorem evidence. The principal locators inspected were:

| Source | Inspected locator and purpose |
| --- | --- |
| Anstreicher | [[anstreicher2009-semidefinite-programming-versus-the-reformulation]] p.12-13: actual packing models, symmetry and Conjecture 4. |
| Khajavirad | [Original arXiv v1 HTML](https://arxiv.org/html/2404.03091v1), Section 1, Remark 1, Proposition 1(i)–(ii), Section 4, equation (44), Proposition 3(i)–(ii): established values and necessary symmetry secants. |
| Kronqvist et al. | [[kronqvist2026-p-split-formulations-a-class]] p.4-7, p.15-16: retained compact convex domain, minimal sharing, assumptions, refinement, Definition 4 and Theorem 6 including its proof. |
| Fawzi–Parrilo | [[fawzi2013-exponential-lower-bounds-on-fixed]] p.3: Theorem 1 constants and SOC decomposition. |
| Lee–Raghavendra–Steurer | Original `lrs-sdpsize.pdf` in `/tmp/minlp-relaxation-limits-sources/`, PDF pp.23, 32–34: Theorems 3.8, 5.3, 5.4, quantitative rank input and the odd-cardinality pseudo-density construction. |
| Braun et al. | Original `braun2013-approxlp.pdf` in the same directory, PDF p.18, Theorem 6(i): the particular fixed-dilation correlation-polytope sandwich. |
| Balas | [[balas1998-disjunctive-programming-properties-of-the]] p.5-7, Section 2, Theorem 2.1: disjunctive hull and recession/closure conventions. |
| Starr | Original `starr1969.pdf` in the same temporary directory, PDF pp.12–13, printed pp.35–36, Appendix 2, Lemma 2 and corollary: exceptional summands. |
| Etessami–Yannakakis | Original `ey-rmc.pdf` in that directory, PDF pp.26–28, Theorem 5.2 and proof: circuit normalization, sign detector and amplifier antecedent. |
| Stewart et al.; Esparza et al. | [[stewart2015-upper-bounds-for-newtons-method]] p.21-22, Section 4.1, equation (18); [[esparza2010-computing-the-least-fixed-point]] p.34, Section 7, Theorem 7.1, equation (14): repeated-squaring/conditioning antecedents and their different algorithmic scope. |
| Lubin et al.; Beach et al. | [[lubin2022-mixed-integer-convex-representability]] p.12, Lemma 4.1 and parity proof; [[beach2024-enhancements-of-discretization-approaches-for]] p.21, combined 2022 preprint Section 5.1.1: midpoint mechanism and sawtooth error, with the version distinction preserved. |
| Wu et al. | [[wu2026-variable-aggregation-based-perspective-reformulation]] p.11-12, Assumption 1, Lemmas 2–3 and Theorem 3: exact attribution and retained assumptions. The referenced supplemental proofs were not audited. |
| Schoenebeck | Original `schoenebeck-full.pdf` and its text extraction in that temporary directory, PDF pp.7–11 and Appendix, printed pp.17–19: Theorems 11–12, Lemma 13, Theorem 21 and Proposition 22, including the relevant expansion proof. |
| Cornuéjols; Hassin–Tamir | Original packing/covering manuscript text in that directory, Theorems 6.5 and 6.13; original `hassin-tamir.pdf`, PDF p.3, printed p.381, Theorem 3.1 and surrounding series-parallel definitions. |
| Davidson–Donsig | [[davidson2007-norms-of-schur-multipliers]] p.6-7, weighted Theorem 2.4 and Lemma 2.5; also projective/Grothendieck input in Theorem 1.2. Continuous weighted density is distinguished from the integer-ceiling pattern result. |
| Luedtke et al.; Boland et al.; Sherali | [[luedtke2012-some-results-on-the-strength]] p.22, Conjecture 1; [[boland2017-bounding-the-gap-between-the]] p.2-4, Theorems 1–4 and Lemma 1; [[sherali1997-convex-envelopes-of-multilinear-functions]] p.7-8, equation (13) and preceding hull distinction. |
| Altschuler–Boix-Adserà | [[altschuler2023-polynomial-time-algorithms-for-multimarginal]] p.55, Theorem 7.4, its precision question and Corollary 7.5: fixed rank versus variable rank, and inverse accuracy versus logarithmic accuracy. |

No source status or library files were changed.

## Findings

None. No repair is requested on the evidence obtained in this review.

## Independent verification

1. **Packing upper bounds, models and attribution.** In `appendix-point-packing.tex`, for a one-coordinate moment block on an interval of length (L), translation reduces the secant to (X_{ii}\le Lx_i). With (s=\sum_i x_i),
   \[
   \sum_{i<j}(X_{ii}+X_{jj}-2X_{ij})
   =k\operatorname{tr}X-\mathbf1^TX\mathbf1
   \le kLs-s^2\le k^2L^2/4.
   \]
   Dividing by the number of pairs gives (kL^2/[2(k-1)]) per coordinate. This yields the unrestricted SDP value (n/(n-1)) and the symmetry value (k/[4(k-1)]) for (k=\lceil n/4\rceil\ge2). The RLT upper bound follows by restricting to a pair in the first quarter. The tightened diagonal secants are essential: adding only mean bounds to the old SDP does not justify this calculation. Reflection relates the manuscript's upper-half convention to Khajavirad's lower-half convention. Also (k-1=\lfloor(n-1)/4\rfloor), so the expressions agree exactly. The manuscript correctly credits Khajavirad's propositions as established results and Anstreicher as the conjectural antecedent.

2. **Attaining covariances and every group pair.** The quarter block covariance is
   \[
   \frac{k}{16(k-1)}(I-J/k),
   \]
   a positive multiple of an orthogonal projection. The remaining covariance blocks are nonnegative diagonal matrices. Thus PSD is analytic, including the singular quarter block. With quarter/half/full groups (Q,H,F), my independent distance calculation gives the following squared distances in order (QQ,QH,QF,HH,HF,FF):

   | Construction | Distances |
   | --- | --- |
   | Symmetry RLT | (1/2,7/8,5/4,5/4,13/8,2) |
   | Symmetry SDP | (k/[4(k-1)],1/2,3/4,5/8,7/8,1) |

   These have the claimed minimum, including the (k=2) tie. On the quarter block the off-diagonal moment (9/16-1/[16(k-1)]) lies in its RLT interval; elsewhere zero covariance or the unrestricted equicorrelation construction supplies the stated products. Empty pair classes cause no difficulty. The dimension-scaled averaging argument also handles zero coordinate length.

3. **Exact finite artifacts.** I authored `verification/reviewer06/stage06-round01/check_packing.py`. Run from the repository root with `python paper-relaxation-limits/verification/reviewer06/stage06-round01/check_packing.py`. It reconstructs all applicable RLT/SDP constructions for (n=2,\ldots,33,40,51,64,81,100), using `Fraction` arithmetic. It passed **612,208 RLT slack-product inequalities across 142 constructions**, all diagonal secant checks and all exact minimum-distance assertions. It checks diagonal/repeated as well as distinct indices, with both coordinate directions. PSD is verified by the preceding analytic projection argument, not by an eigenvalue tolerance. `check_packing.json` records the cases and limits.

   The same executable also extracts and executes the frozen printed signing program and the two concatenated cubic program blocks. Those replays pass: full-signing values are `[1, 2, 4, 4, 5, 8]` for (n=2,\ldots,7); the three larger cubic witnesses and the small two-level witnesses pass their exact dual/attainment assertions. Replaying printed programs is distinct from my independently authored packing check. None of these finite computations proves an arbitrary-size theorem.

4. **Scaling and P-split falsification attempts.** I checked zero scale, retained-domain membership and common-intensive-variable disaggregation. The extensive-cost perspective theorem has the additional hypotheses needed after the explicit counterexamples; the rectangularity claim is restricted to the stated catalogue. In the P-split counterexample both disjuncts together contain all four box vertices, making their hull the retained box; the displayed auxiliary lift satisfies the square epigraphs. The published universal Theorem 6 proof does claim componentwise strict Jensen slack without ensuring differing arguments and does not secure an outward step inside the retained domain. The manuscript's directional repair explicitly fixes both issues. I reconstructed the truncated-square auxiliary hull for translated balls, the transverse maximization in the Hausdorff distance, the rational orthogonal map and its inverse-domain bounds, and the concave auxiliary-image inequalities proving exactness after alignment. These arguments concern epigraph links and auxiliary-only strengthening, as stated.

5. **Rank-one and FBBT transfers.** I rederived the trace face and the rounding chain leading to (136m+10), and checked the outer-section estimate (m(184m+6)). The fixed-dilation LP theorem is used only for LPs. The shifted PSD-rank transfer retains the LRS degree, norm, logarithm and accuracy factors; the (k^{-23/4}) prefactor and choice (k\asymp(m/\log m)^{2/13}) are consistent. Exact fixed-block/SOC exponential bounds and approximate unrestricted-PSD superpolynomial bounds are kept distinct. For FBBT I followed the complement circuit, rational least-root detector and amplifier and reconstructed the update invariant. The lower bound counts the specified primitive updates; acceleration and stronger global contractions are expressly excluded. PosSLP-hardness is not mislabeled NP-hardness.

6. **Whole-paper proof checks.** I checked the half-integral cut reduction and polarization factors; normalized harmonic laws, inactive mass and fixed-point mixture; dyadic and general-radix cutoff ties and digit-reversal realization; coefficient sampling uniformly over all clone vertices; cubic mixture cases, scalar Hessian and finite certificates; feedback-law repair; odd-cycle rounding with its retained baseline; all series/parallel boundary cases; and restriction of one ambient balanced law in the positive-box induction. For the spatial part I checked fractional-cardinality homogenization and Gram degree restrictions, products of slack factors with globally coupled squares, endpoint interpolation for arbitrary coordinate sets, and tensor positivity. The XOR substitution is deterministic substitution rather than conditioning, and the signed-moment realization supplies only the full coordinate-domain quadratic hull. Monomial transfer correctly consumes degree (4rD), uses the support union of a parity basis and preserves the order-one restriction (rD\ge2). The distinct order-one and Bernstein upper certificates are both present. The affine result is a method obstruction, not an affine-tree lower bound. These analytic checks found no failed case.

7. **Presentation and reproducibility.** I independently extracted the whole frozen PDF text and visually inspected rendered manuscript pages 1, 4, 85–87, 93–94, 98, 100, 102, 105, 107 and 111. The packing table, code, supporting proof formulas, roadmap and bibliography fit and remain readable. I found no clipping or unreadable formula on those pages. I did not rerun the LaTeX build or visually inspect all 111 pages.

## Remaining limits

- The finite checks do not establish universal PSD/RLT feasibility, cubic asymptotics or optimal arbitrary-real signing constants; those rely on the analytic proofs identified above. I did not optimize the excluded ORD model or symmetry cases (n<5), or run commercial solvers.
- External theorem hypotheses and relevant proof passages were inspected as listed, but I did not independently reprove the complete conic-rank theorems, sharp Khinchin/Grothendieck constants, matching/oracle-equivalence algorithms, or every classical reference. Wu's supplemental Appendices E–G were not inspected. I did not newly verify the Coniglio publication/version or perform an exhaustive novelty search. These are limits on this review, not claimed access failures or evidence that the manuscript's qualified attributions are false.
- The temporary primary PDFs were read as existing source artifacts; I did not repeat every network retrieval or independently authenticate their entire acquisition history. No paywall or login was bypassed, and no primary source was redistributed.
- Exact cubic constants, a matching second-order lower asymptotic, finite-aspect optima, the stated stronger structural partitions, unequal-aspect frequency-two sharpness and unrestricted affine branching remain open in the manuscript. No finite evidence inspected here settles them.

Only this report and files under the assigned reviewer verification directory were written.
