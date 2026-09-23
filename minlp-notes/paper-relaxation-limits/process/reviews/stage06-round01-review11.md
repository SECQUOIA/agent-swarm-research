# Stage 6, round 1, independent review 11

**Verdict: MINOR.** I found one local missing qualification in the description of prior FBBT results. I found no major defect in the integrated manuscript. The hardness, fairness and primitive-update arguments survive the falsification attempts below. This verdict is for this frozen integration stage, not the separate final whole-paper review.

## Coverage

I reviewed `process/snapshots/stage06-round01`. My checker confirms that its 111-page `main.pdf` has SHA256 `343b29156e275df970236babbab1077b3a53261317e0995a6a7ea0398b583916`.

I read `main.tex`, `macros.tex`, `references.bib`, and every section file in full:

- `01-foundations.tex`, `02-universal-positive.tex`, `03-cubic-equal-means.tex`, `04-incidence-interiority.tex`, `05-feedback-frequency.tex`, `06-treewidth-two.tex`, `07-positive-boxes.tex`, `08-exact-complexity.tex`;
- `09-cardinality-spatial.tex`, `10-cardinality-preordering.tex`, `11-coordinate-domains-lifts.tex`, `12-relative-blocks-cuts.tex`, `13-xor-quadratic-hulls.tex`, `14-monomial-reformulations.tex`, `15-finite-certificates-affine.tex`, `16-supporting-comparisons.tex`, `17-synthesis.tex`;
- `appendix-finite-signings.tex`, `appendix-positive-couplings.tex`, `appendix-cubic-certificates.tex`, `appendix-structural-auxiliary.tex`, `appendix-positive-box-predecessors.tex`, `appendix-point-packing.tex`, `appendix-scaling.tex`, `appendix-p-split.tex`, `appendix-rank-one.tex`, `appendix-fbbt.tex`, `appendix-integer-comparison.tex`.

I read the frozen `README.md`, `process/review-protocol.md`, `process/stage-06-review-assignment.md`, `process/stage-06-author-assignment.md`, `process/stage-06-author.md`, `process/scope-proposal.md`, and `process/claim-coverage.md`, including the complete scope and coverage rows. I also inspected the frozen author-validation record, the preparation note `verification/stage06-additional-primary-checks.md`, and the Schoenebeck source record. These records supplied locators, not proof. I did not read another current-round review or use a prior PASS as evidence.

The complete manuscript reading was from source, including its displayed mathematics and executable appendices. I additionally rendered and visually inspected PDF pages 1, 4, 86, 99, 105–108. This checks representative introduction, roadmap, code, geometric, FBBT and bibliography rendering; it is not a visual inspection of all 111 pages. No new full LaTeX build was performed.

I read `literature/AGENTS.md` before the local originals. The following lists direct primary-source checks, with the limits of each check. For local literature packages, page locators refer to the inspected original PDF; extractions were used where equations remained readable.

| Primary source | Direct reading and checked dependency |
| --- | --- |
| Belotti et al., `[[belotti2012-on-feasibility-based-bounds-tightening]]` | Pages 1–7 and 10–14: operator model, fixed-point discussion, linear FBBT LP, Theorem 4.1 and its nonempty-limit hypothesis. Page 14 was also rendered from the original and inspected visually. |
| Etessami–Yannakakis, `/tmp/minlp-relaxation-limits-sources/ey-rmc.pdf` | PDF 26–28, complete Theorem 5.2 reduction: positive/negative parts, normalization, detector and amplification. The detector page was also inspected visually. |
| Stewart et al., `[[stewart2015-upper-bounds-for-newtons-method]]` | PDF 21–22, equation (18), Newton-chain behavior and repeated squaring; equation (18) page also inspected visually. |
| Esparza et al., `[[esparza2010-computing-the-least-fixed-point]]` | Original author PDF 34, equation (14), Theorem 7.1 and its proof, inspected visually. I also read the corresponding published-version extraction, where the numbering differs. |
| Luedtke et al., `[[luedtke2012-some-results-on-the-strength]]` | Author Theorems 4–5, Theorem 8 statement and initial reduction, Conjecture 1 on p.22. Positivity, nonnegative lower bounds and the coloring constants match the manuscript. |
| Boland et al., `[[boland2017-bounding-the-gap-between-the]]` | Theorems 2 and 4; Lemma 1 and Corollary 1; signed-cycle characterization and proof. The scalar vertical-gap interpretation is retained. |
| Davidson–Donsig, `[[davidson2007-norms-of-schur-multipliers]]` | Theorems 1.2 and 2.4 and the displayed proof of the latter. The continuous weighted-matrix bound permits the manuscript's unrounded density parameter. |
| Cornuéjols, `/tmp/minlp-relaxation-limits-sources/cornuejols-packing-covering.txt` | Theorems 6.5 and 6.13, with surrounding proofs, supporting the TU and balanced-matrix inputs. This was a source text extraction, not a fresh page rendering. |
| Hassin–Tamir, `/tmp/minlp-relaxation-limits-sources/hassin-tamir.pdf` | Original PDF 3, printed p.381, rendered independently: series-parallel definition, Theorem 3.1 and the augmentation argument. |
| Schoenebeck, `/tmp/minlp-relaxation-limits-sources/schoenebeck-full.pdf` | PDF 7–12: random model, width definition and Theorems 11–12, signed-character construction and Gram calculation. The full probabilistic width proof in its dependency literature was not rederived. |
| Khajavirad | [Original arXiv HTML](https://arxiv.org/html/2404.03091v1): RLT/SDP/SYM conventions, Proposition 1 and its proof, Proposition 3 statement and initial proof. These support the published credit and the exact point-packing values. |
| Anstreicher, `[[anstreicher2009-semidefinite-programming-versus-the-reformulation]]` | Author PDF 12–13, Conjecture 4 and its numerical status. The manuscript correctly distinguishes this predecessor conjecture from Khajavirad's later proofs. |
| Kronqvist et al., `[[kronqvist2026-p-split-formulations-a-class]]` | PDF 4–7 and 15–16: assumptions, retained domain, epigraph remark, independent bounds, Corollary 3, Definition 4 and Theorem 6 with proof. |
| Balas, `[[balas1998-disjunctive-programming-properties-of-the]]` | PDF 5–7: Theorem 2.1, disaggregation proof and bounded-domain corollary. Some scanned mathematical symbols in the extraction are poor; the manuscript's bounded-slice proof was checked independently. |
| Wu et al., `[[wu2026-variable-aggregation-based-perspective-reformulation]]` | PDF 12, Lemma 3 and Theorem 3 statements. Supplementary proofs and all of Assumption 1 were not independently audited; no broader source theorem is treated as established by this check. |
| Fawzi–Parrilo, `[[fawzi2013-exponential-lower-bounds-on-fixed]]` | PDF 3, Theorem 1, fixed-block-size lower bound and Lorentz-cone interpretation. |
| Braun et al., `/tmp/minlp-relaxation-limits-sources/braun2013-approxlp.pdf` | PDF 18, hard pair and Theorem 6(i–ii). I checked the applicable pair and approximation factor, not the entire corruption-bound proof. |
| Lee–Raghavendra–Steurer, `/tmp/minlp-relaxation-limits-sources/lrs-sdpsize.pdf` | PDF 23 and 32–34, Theorem 3.8/equation (3.11), pseudo-density construction, Theorems 5.3–5.4 and their specialization. Earlier analytic machinery remains an external input. |
| Lubin et al., `[[lubin2022-mixed-integer-convex-representability]]` | PDF 12, complete Lemma 4.1 parity argument. |
| Beach et al., `[[beach2024-enhancements-of-discretization-approaches-for]]` | PDF 21, Table 1 and initial maximum-error discussion. This confirms the stated discretization precedent, not every source formulation. |

## Findings

1. **R11-1 — MINOR: qualify the prior linear-FBBT LP statement.** Location: `sections/appendix-fbbt.tex:5–6`, opening paragraph of Appendix J, PDF p.104. The sentence says that linear continuous FBBT limits can be obtained by an LP without stating a nonemptiness condition. The cited source's Theorem 4.1 explicitly assumes the limiting box is nonempty. Its following Section 4.1 also reports a case where FBBT detected emptiness but FBBT-LP was not infeasible. Thus the cited theorem does not support the unqualified statement for empty limits. Source: `[[belotti2012-on-feasibility-based-bounds-tightening]]` p.14, Theorem 4.1 and Section 4.1; independently rendered as `verification/reviewer11/stage06-round01/belotti-14.png`. Repair the sentence to begin: “When the limiting box is nonempty, continuous linear FBBT limits can be obtained by an LP,” and preferably give the theorem locator. This is local: the manuscript's own constructed FBBT systems are feasible, and their proofs do not depend on this LP result.

## Independent verification

### FBBT and prior fixed-point constructions

**Fairness needs no bounded delay.** For the nonnegative polynomial system, the increasing Kleene sequence starts at zero and is bounded by every nonnegative fixed point. Continuity gives its least fixed point (q). Because (q) is a feasible point, sound contractors preserve it and give (l\leq q). For each fixed Kleene depth, after the previous depth has been reached, finitely many defining forward updates suffice to reach the next one. Fairness supplies a finite epoch containing all these updates even when delays grow without bound. This proves the lower-limit sandwich. I checked that the same argument applies to the augmented arithmetic-node system, rather than silently eliminating graph variables.

**Restricted reduction and amplification.** I reconstructed the normalized complementary circuit. Addition is an average; a product uses (p=p_jp_k), (v=p_jr_k), (r=r_j+v), preserving (p+r=1). Layer identities keep the arithmetic description polynomial in size. The huge normalizer (M\leq2^{2^L}) is used in the proof, not inserted as a binary-encoded input constant. Copy variables remove repeated names in products.

For (c=1/2+(U-V)/(2M)), (d=1-c), the detector (a=d+ca^2) has least root 1 when (c\leq1/2), and (d/c) otherwise. In the positive case, with integer \(\Delta=U-V\geq1\),

\[
1-a=\frac{2\Delta}{M+\Delta}\geq\frac1M.
\]

For the repeated-square value (b=2^{-2^{L+2}}\leq1/(8M)), the amplifier is (z=b/[1-(1-b)a]). It equals 1 for (U\leq V), and is at most (bM\leq1/8) otherwise. Additive error (1/4) therefore separates the cases at (1/2). I checked (c=0,1/2,1), the orientation of the decision, rationality of all solutions, and the at-most-two-solutions assertion. The inequality (ca\leq1/2) selects the least detector root. PosSLP-hardness is not presented as an NP-hardness theorem. The small strongly connected components refer to the directed defining-equation graph, not a different interaction graph.

**Every-order primitive-update count.** Fixing the acyclic constants exactly is a stronger initialization. Monotonicity of each interval-hull contractor permits comparison under the same update sequence, so a lower bound from that initialization also applies to the stated one. For (c=1-b), the two feedback equations are (z=b+w) and (w=cz). Their exact coordinate hulls preserve (0\leq l_w\leq c l_z). Consequently a product update cannot increase (l_z), while an affine update can increase it at most to (b+c l_z). After (K) affine calls,

\[
l_z\leq1-c^K\leq Kb.
\]

Reaching (l_z\geq1/2) requires (K\geq2^{2^n-1}). I checked simultaneous old-endpoint formulas in both directions, not only forward updates. The feasible point forces (u_z=1); upper tightening therefore does not defeat the invariant. Fairness establishes the eventual limit; the finite lower bound holds for every order. Counting primitive calls, exact arithmetic and literal binary input size remain distinct. Eliminating the feedback equations globally would be a different operation and is expressly excluded.

**Earlier double-exponential examples.** For Stewart's chain, writing (e_i=1-x_i) gives (e_0(k+1)=e_0(k)-e_0(k)^2/2) and (e_i(k)^2\geq e_{i-1}(k)). Hence (e_0(k)\geq1/(k+1)) and (e_n(k)\geq(k+1)^{-1/2^n}). The claimed double-exponential first-bit Kleene consequence follows. The Esparza chain yields the corresponding square-root propagation through a slightly different polynomial. The manuscript distinguishes these derived Kleene consequences from the sources' Newton iteration statements and credits the earlier mechanisms. It does not use an inherited synchronous recurrence as proof of the new every-order contractor bound.

### Checks across the rest of the manuscript

- I recalculated the factor-of-two relation between full-center envelope widths and cut ranges, checked the induced-face boundary reduction, and followed the polarization/density argument. Switching preserves the quadratic range; normalized signings and cuts are exhaustively covered by the printed finite program.
- I checked the positive coupling constructions, the marginal normalization and cutoff mixture in the degree bound, and the distinction between its second-order upper estimate and a sharp leading asymptotic. For cubics, the finite minorants and attaining laws certify their advertised lower examples. Optimization within the chosen mixture family does not become an assertion that the true cubic constant is known.
- I followed the frequency-two extreme-point argument and every series/parallel case of the treewidth-two invariant. The balanced-matrix and TU inputs are used on the appropriate incidence systems. The positive-box restriction argument uses the same ambient law when coefficients or supports are restricted.
- For cardinality, I checked the Gram/Vandermonde positivity argument, conditional degrees and full preordering rather than only square terms. Endpoint interpolation transfers coordinatewise graph lifts. Tensor products preserve PSD on the principal submatrix of permitted total degree. The stronger block and clique oracles are explicitly outside the lower-bound oracle.
- For XOR, I checked signed-character consistency and Gram PSD, deletion/width accounting, substitution instead of conditioning, and the degree (4rD) requirement. The moment statement concerns the full-box quadratic hull. It does not assert that arbitrary additional graph identities or stronger relative oracles leave the certificate lower bound intact.
- I reconstructed the point-packing averaging inequality and projection covariance witnesses, including all group-pair types and the tightened diagonal secants. The (n\geq5) symmetry range and the published attribution are retained.
- For scaling, I checked the common-(T) disaggregation and zero slices; the cost-separation counterexample forces a nonzero second component. The perspective proof is restricted to extensive variables, and its size-biased/product-weight construction does not silently preserve unrelated intensive variables.
- For P-split, the box counterexample has all box vertices in the disjunctive union, so its convex hull is the box. The translated-ball auxiliary hull is downward closed and yields the stated cylinder/ellipsoid intersection. The squared distance increases with the transverse radius squared, giving the displayed Hausdorff distance. The rotated example retains the transformed domain, and exact-image constraints are distinguished from epigraph inequalities.
- For rank one, I checked the trace-one atoms, correlation face and paired indicators, the constants (136m+10) and (184m+6), and the resulting (A_m). The robust LP reduction uses its own right-hand side; the SDP reduction uses the shifted slack and keeps the (k^{-23/4}) prefactor. Fixed block order, unrestricted matrix order and spatial region counts remain separate resources.
- For integer precision, I checked the parity-class midpoint argument, the area integral (16\varepsilon\log2), the width constant (20\varepsilon), and the shared binary expansion with only residual-residual products relaxed. The conclusions count integer/parity resources, not spatial certificates.

### Executed exact checks

`verification/reviewer11/stage06-round01/check.py` uses standard-library exact rational arithmetic. Its recorded `check.json` reports 66,363 normalized detector/amplifier cases (layers 1–3, all integer outputs from 0 to the corresponding (M)); 2,384 exact primitive-hull transitions (all binary update words through length 12, deduplicating states, for four repeated-square depths); and 36 finite Kleene-chain cases. It also verifies the frozen PDF hash. These are finite regression/falsification checks; the universal statements rely on the derivations above.

I separately extracted and executed the verbatim Python blocks from the frozen finite-signing and cubic appendices without modifying those files. The signing program returned `[1, 2, 4, 4, 5, 8]`. Both cubic blocks completed and printed `All finite cubic certificates passed.` The enumeration is an exact proof for those finite tables only.

## Remaining limits

No cited source needed for the FBBT focus was inaccessible. This was not a complete independent audit of every external theorem or every bibliography entry: in particular the earlier analytic machinery behind the SDP-size result, the probabilistic width lower bound, the full Wu supplement, and all predecessor envelope/transport proofs remain external inputs. I checked their relevant scope where indicated above and reconstructed the manuscript's applications. Starr's original proof was not independently read in this review. Poor scanned text in Balas limits my source-level symbol check there, although the bounded disaggregation used here has its own verified proof.

I did not exhaust arbitrary circuits, arbitrary update sequences or large hierarchy matrices computationally. The finite experiments cannot establish those universal claims. Likewise I did not perform a full-page visual audit or a fresh build. I found no mismatch between the stated proved/open scope and the mathematical claims I read; the unresolved exact cubic constant, broader structural bounds and stronger-oracle questions remain explicitly open rather than being filled by finite evidence.
