# Stage 6, round 1 — independent review 10

**Verdict: PASS.** I found no demonstrable mathematical, scope, attribution, or presentation defect requiring a revision. This is a review of the frozen integrated stage, not a certification of the separate final whole-paper review.

## Coverage

I reviewed the snapshot `process/snapshots/stage06-round01`. I independently confirmed that its `main.pdf` has 111 pages and SHA256 `343b29156e275df970236babbab1077b3a53261317e0995a6a7ea0398b583916`.

I read the frozen `process/review-protocol.md`, `process/stage-06-review-assignment.md`, `process/stage-06-author-assignment.md`, `process/stage-06-author.md`, `process/scope-proposal.md`, and `process/claim-coverage.md`, together with the frozen README. I checked the intended proved/open scope against the integrated text. Prior acceptance labels were not evidence for theorem truth. I did not read any other current-round review or delegate work.

I read all of `main.tex`, `macros.tex`, and `references.bib`, and every manuscript section and appendix in `sections/`:

- `01-foundations.tex`, `02-universal-positive.tex`, `03-cubic-equal-means.tex`, `04-incidence-interiority.tex`, `05-feedback-frequency.tex`, `06-treewidth-two.tex`, `07-positive-boxes.tex`, and `08-exact-complexity.tex`.
- `09-cardinality-spatial.tex`, `10-cardinality-preordering.tex`, `11-coordinate-domains-lifts.tex`, `12-relative-blocks-cuts.tex`, `13-xor-quadratic-hulls.tex`, `14-monomial-reformulations.tex`, `15-finite-certificates-affine.tex`, `16-supporting-comparisons.tex`, and `17-synthesis.tex`.
- `appendix-finite-signings.tex`, `appendix-positive-couplings.tex`, `appendix-cubic-certificates.tex`, `appendix-structural-auxiliary.tex`, `appendix-positive-box-predecessors.tex`, `appendix-point-packing.tex`, `appendix-scaling.tex`, `appendix-p-split.tex`, `appendix-rank-one.tex`, `appendix-fbbt.tex`, and `appendix-integer-comparison.tex`.

This includes the abstract, introduction, roadmap, proofs, computational certificates, open questions, and complete bibliography. Where command output was truncated, I reread the missing ranges. I also read the repository's three rank-one result notes on correlation-face conic bounds, stability, and approximate SDP bounds, and compared their statements with Appendix I.

I inspected rendered PDF pages 1, 2, 93–95, 97, 99, 101–108, and 111, including the rank-one equations, supporting propositions, and bibliography. The source text, rather than visual inspection of every page, supplied the whole-manuscript reading. I found no visible clipping or unreadable mathematical layout on the inspected pages. The manuscript's separation of width ratios, specified spatial certificates, global cone size, integer precision, and primitive update counts is maintained through the abstract and conclusion.

### Primary-source checks

I read `literature/AGENTS.md` before inspecting originals. The following records describe targeted original-source checks, not claims to have independently proved every external theorem.

| Source and precise locator | What I checked |
| --- | --- |
| Fawzi–Parrilo, local `literature/papers/fawzi2013-exponential-lower-bounds-on-fixed/original.pdf`, PDF p. 3, Theorem 1 and Lorentz-cone discussion | Fixed block-size constants, stronger order-two bound, and the distinction between number of fixed blocks and dimension of unrestricted Lorentz cones. |
| Lee–Raghavendra–Steurer, `/tmp/minlp-relaxation-limits-sources/lrs-sdpsize.pdf`, PDF p. 23, Theorem 3.8 and (3.11), and pp. 32–34, Theorems 5.3–5.4 | Quantitative PSD-rank inequality, pseudo-density normalization and norm, odd parameter, strict negativity hypothesis, and exact correlation-polytope order bound. I also inspected the rendered page 23 formula. |
| Braun et al., `/tmp/minlp-relaxation-limits-sources/braun2013-approxlp.pdf`, PDF p. 18, Theorem 6(i) and preceding hard pair | Fixed dilation of the Boolean correlation inequalities and the LP resource being bounded. |
| Kronqvist–Misener–Tsay, local `literature/papers/kronqvist2026-p-split-formulations-a-class/original.pdf`, PDF pp. 4–7 and 15–16 | Assumptions 1–4, retained global domain, allowed minimum sharing, defining formulation, Corollary 3, Definition 4, and Theorem 6 with its proof. These support the manuscript's specific counterexample to universal nonexactness. |
| Anstreicher, local `literature/papers/anstreicher2009-semidefinite-programming-versus-the-reformulation/original.pdf`, PDF pp. 12–13 | Four point-packing values were stated as Conjecture 4, with numerical evidence and the stated symmetry restrictions. |
| Khajavirad, [arXiv:2404.03091v1 original HTML](https://arxiv.org/html/2404.03091v1), model/Remark 1 and Propositions 1 and 3 | Matching RLT/SDP values and symmetry-adjusted models; appropriate later proof credit. |
| Balas, local `literature/papers/balas1998-disjunctive-programming-properties-of-the/original.pdf`, PDF pp. 5–7, Section 2/Theorem 2.1 | Disaggregated convex-hull representation, including the zero-weight issue. |
| Wu et al., local `literature/papers/wu2026-variable-aggregation-based-perspective-reformulation/original.pdf`, PDF p. 12, Lemma 3/Theorem 3 | Aggregation hull statement and the explicit reference of its proof to supplementary material. |
| Starr, `/tmp/minlp-relaxation-limits-sources/starr1969.pdf`, PDF pp. 12–13, printed pp. 35–36, Appendix 2/Lemma 2 and corollary | Dimension bound on exceptional summands used for the aggregate rounding comparison. |
| Etessami–Yannakakis, `/tmp/minlp-relaxation-limits-sources/ey-rmc.pdf`, PDF pp. 26–28, Theorem 5.2 proof | Normalized arithmetic-circuit encoding, rational-root detector, and constant-gap amplification. |
| Belotti et al., local `literature/papers/belotti2012-on-feasibility-based-bounds-tightening/original.pdf`, PDF pp. 1–2 | Classical nonfinite/slow FBBT and polynomial solvability of the linear limiting-bound problem; no confusion with primitive iteration count. |
| Esparza–Kiefer–Luttenberger, local `literature/papers/esparza2010-computing-the-least-fixed-point/original.pdf`, PDF p. 34, Section 7/Theorem 7.1 and system (14) | Published slow-Newton example and its distinct iteration model. |
| Stewart–Etessami–Yannakakis, local `literature/papers/stewart2015-upper-bounds-for-newtons-method/original.pdf`, PDF pp. 21–22, Section 4.1/(18) | Chain used in the manuscript's explicitly labelled inference about ordinary Kleene iteration. |
| Lubin–Vielma–Zadik, local `literature/papers/lubin2022-mixed-integer-convex-representability/original.pdf`, PDF p. 12, Lemma 4.1 | Midpoint parity obstruction and its hypotheses. |
| Beach et al., local `literature/papers/beach2024-enhancements-of-discretization-approaches-for/original.pdf`, PDF p. 21, combined 2022 version, Section 5.1.1 | Scalar upper and lower approximation-error constants and the need to distinguish version numbering. |
| Schoenebeck, `/tmp/minlp-relaxation-limits-sources/schoenebeck-full.txt`, source PDF pp. 7–11 and 16–19 | Definition 10, Theorems 11–12, Lemma 13, and the expansion/counting proof around Theorem 21/Proposition 22 underlying the local sign laws. |
| Cornuéjols, `/tmp/minlp-relaxation-limits-sources/cornuejols-packing-covering.txt`, Theorems 6.5 and 6.13 with surrounding proof | Camion's criterion and the balanced-matrix connection used in the structural proof. |
| Hassin–Tamir, source images `/tmp/minlp-relaxation-limits-sources/hassin-02.png` and `hassin-03.png`, printed pp. 380–381, Theorem 3.1 | Biconnected series-parallel characterization; read the scanned original because its text extraction was empty. |
| Davidson–Donsig, local `literature/papers/davidson2007-norms-of-schur-multipliers/fulltext.md` and original PDF pp. 4–7, Theorems 1.2 and 2.4 | Support-pattern norm statements, weighted constants, and the manuscript's prior-art comparison. |
| Luedtke–Namazifar–Linderoth, local `literature/papers/luedtke2012-some-results-on-the-strength/fulltext.md`, Theorems 4–5 and Conjecture 1; original PDF p. 22 | Earlier common upper law and positive-coefficient question, with author-version locators. |

## Findings

None. No major or minor finding IDs are assigned, and no repair is requested.

## Independent verification

### Correlation-face geometry and stability

I reconstructed the proof of Proposition I.1 from the marginal parametrization, without assuming a symmetric generator. For nonzero `W`, `W=rc^T/S` with both marginals in `[0,1]`. Trace equality implies both sums `sum r_i(1-c_i)` and `sum c_i(1-r_i)` vanish, forcing `r=c=1_A`. On that trace face, `B=0` allows at most one member per paired index, and maximizing the total at `m` selects precisely `(x,e-x)(x,e-x)^T/m`. This proves the displayed affine inverse, including its off-diagonal blocks. Successive faces are legitimate here; the explicit exposing functional additionally avoids relying on that observation alone.

For the exposure estimate I recovered `||r-c||_1 <= 2SD` and `S <= m+SB+||r-c||_1 <= m+2mB+4mD`, giving `g >= B+D`. For Proposition I.2 I checked the successive constants `u<=6SD`, `v<=8SD`, `h<=SB+8SD`, and `||a-b||_1<=2SB+22SD+|m-S|`. Comparing outer products through `(S/m)b` gives the claimed `4SB+58SD+5|S-m|`. Substitution yields `(18m+5)B+(136m+5)D+5g`, hence `(136m+10)g`. The zero generator is handled separately and satisfies the claimed estimates.

The stronger transfer is not obtained by multiplying the crude exposure Lipschitz constant. I checked its separate averaging argument: the positive part of `S-m` is at most `2mB+4mD`, so the average absolute deviation is at most `4mB+8mD+m-T`. This gives `28mB+156mD+5(m-T)`, and then `(184m+6)epsilon` after the section and triangle inequality. Both output maps have entrywise norm at most `m`, yielding exactly `A_m=m(184m+6)`. The strict penalty threshold is sufficient to force every minimizer into the face; replacing it by a non-strict inequality would require a separate argument, and the manuscript does not do that.

I also checked the nonpolyhedral `K_2` slice. Fixing its first row and column sums to one yields the displayed curve with lower-right entry `q+1/q-2`, whose strict convexity exposes infinitely many extreme graph points. Thus exact finite LP nonrepresentability and the quantitative positive-error LP lower bound are logically distinct.

### Exact and approximate conic resources

The exact face restriction preserves the cone even if the original lift is not strictly feasible. The fixed-order PSD inequalities agree with Fawzi–Parrilo. Decomposing a Lorentz cone counts dimension, not merely one unrestricted cone, so the exact SOC assertion is the stated exponential total-dimension bound. Several unrestricted PSD blocks combine by total order. The LRS exact PSD bound is superpolynomial, not the fixed-block exponential bound.

For Proposition I.3 the Boolean LP inequalities have coefficient norm one and become right-side-two inequalities under unit entrywise error. This is the fixed-dilation hard pair from Braun et al. The proof does not reuse that LP hard pair to infer a PSD bound.

I independently substituted the shifted sign-correlation slack into LRS (3.11). The coefficient norm is `1/(4k^2)` because the entrywise norm sums the full matrix. For `eta<=1/2`, shifting by `eta/(4k^2)` leaves pseudo-expectation at most `-1/(8k^2)`. The choice `delta=1/(16k^2)` meets the strict source inequality. The prefactor is `k^(-23/4)`, and the bracket is proportional to `m/(k^(13/2) log m)`. An odd `k` of a sufficiently small constant times `(m/log m)^(2/13)` gives the claimed exponential of that quantity. Its eventual `m>=2k` requirement is satisfied.

I checked the `q+1` slack-factorization justification: restrict to the smallest PSD face containing feasible matrices, obtain relative strict feasibility from a finite combination spanning their ranges, and use conic duality for each nonnegative affine slack. Its nonnegative constant remainder is one extra scalar PSD coordinate. This also explains why a closed projected set or a pre-existing proper lift is not being silently assumed. The final SOC approximate consequence transfers only the superpolynomial total-dimension bound through PSD order at most twice that dimension. The theorem needs uniform error for all normalized costs, or the displayed set sandwich, rather than one favorable objective.

### Whole-manuscript proof checks

- For signed envelopes I checked the induced-face reduction, polarization, density orientation, and union-bound signing argument. For positive envelopes I followed the common upper law, universal rounding, harmonic and radix capacity constraints, asymptotic normalization, coefficient removal, and the separation of cubic finite certificates from the equal-means mixture optimum. I found no interchange of an upper certificate with an exact optimum claim.
- For incidence and width two I reconstructed the terminal-type invariant in the series/parallel proof and checked why Camion's condition, rather than balancedness alone, is needed. I checked the odd-cycle lower examples, frequency-two matching reduction, rational interior radius, and preservation of the structural baseline under dummy variables. For positive boxes I checked the physical-coordinate coefficient expansion, the fixed-ambient common coins, and the unequal-aspect failure of bipartite exactness.
- For exact scalar complexity I checked the PARTITION product comparison, the remainder versus variance gap, and rational basic certificates. For cardinality spatial bounds I followed the fractional-cardinality Gram construction, endpoint restrictions, conditional indicators, full preordering products, tensorization, witness counting, and finite upper certificates. The claims retain their stated oracle and branching restrictions.
- For coordinate graph lifts I checked endpoint interpolation and the role of objective agreement on the full graph. For XOR and bounded monomials I followed the degree losses `4r` and `4rD`, the low-degree sign-class laws, deterministic substitution rather than conditioning, and the separate order-one upper construction. In particular, the restrictions `r>=1`, `rD>=2`, and the unlifted cubic restriction `r>=2` are not silently dropped.
- For point packing I checked the two covariance projections, the special singleton groups, the group-pair RLT bounds, and symmetry-adjusted diagonal secants. For scaling I checked the zero-weight disaggregation, retained intensive variable, failure of general cost separation, rectangularity criterion, and aggregate rounding. These statements do not claim exactness for unrestricted costs.
- For P-split I checked that the four box corners in the retained-domain example already lie in the disjunction, making its hull the retained box. I also checked the directional repair's additional hypothesis, the downward-closed auxiliary hull, the translated-ball projected formula, the transverse point attaining the Hausdorff gap, the rational coordinate transformation, and exactness after convexifying the exact aligned auxiliary image. The comparison remains about the stated formulation and domain.
- For FBBT I checked the normalized arithmetic circuit, the rational detector roots, amplification gap, constant coefficients and bounded feedback components. In the slow primitive example the invariant `l_w<=c l_z` prevents inverse product propagation from accelerating the lower bound; every affine update obeys `l_z(new)<=b+c l_z`. Thus `l_z<=Kb` for every stated primitive ordering. Stronger initialization is justified by contractor monotonicity. The cited slow-Newton systems are distinguished from the manuscript's inference about ordinary Kleene iteration.
- For integer precision I checked the parity midpoint obstruction, scalar midpoint gap, compact closure of parity classes, the product-area estimate `16 epsilon log 2`, binary expansion upper construction, and fixed-count special case. None of these arguments is substituted for a spatial region lower bound.

### Exact computational evidence

The reproducible checker is `verification/reviewer10/stage06-round01/check_independent.py`; its output is `verification/reviewer10/stage06-round01/result.json`. It completed successfully using exact Python integers and `Fraction`, with no optimization solver or floating-point arithmetic:

- Exhausted all nonzero equal-total half-grid marginal pairs for `m=1,2`: 18 and 1,106 generator pairs. Also checked 959 seeded rational generator pairs for `m=1,...,8`. All satisfied the exposure, rounded-distance, `136m+10`, and stronger affine bounds.
- Checked all 510 paired atoms for `m=1,...,8`, including the affine inverse and zero exposure.
- Independently constructed the symmetric Lagrange densities for every odd `k=3,...,31`; verified normalization, the claimed infinity-norm bound, unshifted negative moment, shifted negative moment at error `1/2`, range, and mean bound.
- Executed exact alternating primitive FBBT for `n=1,2,3`. The first lower bound at least `1/2` occurred after 3, 11, and 178 affine applications, consistent with the every-schedule lower bound.
- Replayed the complete finite-signing program printed in the frozen appendix, obtaining `[1,2,4,4,5,8]`. Replayed the frozen exact cubic finite-certificate script, including all three large asymmetric grid certificates and the smaller witnesses; all assertions passed. These two computations are explicitly author-code replays, not independently coded enumerations.

## Remaining limits

The finite computations are falsification checks, not proofs of the universal stability inequalities, the every-schedule FBBT statement, or PSD rank asymptotics. The Lagrange computation verifies density moments and norm, not positivity on every low-degree square; that positivity is a cited external theorem whose use I checked. I did not rerun the full repository validation suite or rebuild the frozen PDF, and I did not visually inspect all 111 pages.

I did not reproduce from first principles the deep external PSD-rank theorems, Schoenebeck's complete lower-bound machinery, Schur-multiplier theory, or the standard matching/optimization complexity results. The source checks above identify the original portions actually inspected. Other bibliography entries were read as bibliography and manuscript context, not freshly audited in full. I did not inspect Wu et al.'s supplementary proofs, establish identity of Coniglio's anonymous review version with its published version, or independently verify every publisher bibliographic field. The manuscript explicitly records the relevant source-version limitations rather than concealing them. These are limits of this review and do not provide a demonstrated defect.

The paper's stated open quantitative gaps and stronger-oracle questions remain open; neither this PASS nor the finite checks resolves them.
