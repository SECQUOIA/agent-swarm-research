# Stage 6, round 1 — independent review 09

**Verdict: MINOR.** No major defect found. Findings R09-1 and R09-2 are local clarifications. The P-split rational-coordinate comparison, its quantification over auxiliary-only convexifications, and the aligned exact-image repair withstand the checks below.

## Coverage

I reviewed the frozen `process/snapshots/stage06-round01` manuscript, not the live working copy. The 111-page frozen `main.pdf` has SHA-256 `343b29156e275df970236babbab1077b3a53261317e0995a6a7ea0398b583916`, which I checked. I read the complete TeX manuscript, including `main.tex`, `macros.tex`, `references.bib`, and every included section:

- `01-foundations.tex`, `02-universal-positive.tex`, `03-cubic-equal-means.tex`, `04-incidence-interiority.tex`, `05-feedback-frequency.tex`, `06-treewidth-two.tex`;
- `07-positive-boxes.tex`, `08-exact-complexity.tex`, `09-cardinality-spatial.tex`, `10-cardinality-preordering.tex`, `11-coordinate-domains-lifts.tex`, `12-relative-blocks-cuts.tex`;
- `13-xor-quadratic-hulls.tex`, `14-monomial-reformulations.tex`, `15-finite-certificates-affine.tex`, `16-supporting-comparisons.tex`, `17-synthesis.tex`;
- `appendix-finite-signings.tex`, `appendix-positive-couplings.tex`, `appendix-cubic-certificates.tex`, `appendix-structural-auxiliary.tex`, `appendix-positive-box-predecessors.tex`, `appendix-point-packing.tex`, `appendix-scaling.tex`, `appendix-p-split.tex`, `appendix-rank-one.tex`, `appendix-fbbt.tex`, `appendix-integer-comparison.tex`.

I read the frozen review protocol, Stage 6 reviewer and author assignments, author record, scope proposal, and claim-coverage ledger. I also read the three canonical P-split notes `notes/common-factor-p-split-correction.md`, `notes/common-factor-p-split-balls.md`, and `notes/common-factor-p-split-rotation-gap.md`. Existing status labels were not used as mathematical evidence. I did not read another current-round report or modify the manuscript or snapshot.

The source reading below followed `literature/AGENTS.md`. For the central P-split attribution, I checked the original published PDF as well as the available transcription: [[kronqvist2026-p-split-formulations-a-class]] PDF pp. 4–7 and 15–16, including the assumptions, retained-domain formulation and bounds, minimal sharing, Definition 4, Theorem 6 and its proof, and the refinement discussion. I visually inspected original PDF p. 16. The live DOI page did not open successfully; the local published original was accessible.

Additional direct primary-source checks were:

| Source | Passage inspected and use checked |
| --- | --- |
| [[anstreicher2009-semidefinite-programming-versus-the-reformulation]] | Original PDF pp. 12–13, point-packing model and Conjecture 4; separate coordinate blocks, symmetry, and conjectural numerical status. |
| Khajavirad, arXiv:2404.03091v1 | Definitions and Propositions 1 and 3 in the [primary HTML version](https://arxiv.org/html/2404.03091v1); the four comparison values and RLT statement. The inspected proofs support the manuscript's attribution to subsequent proofs of the conjectures. |
| [[balas1998-disjunctive-programming-properties-of-the]] | Original PDF pp. 5–7, printed pp. 7–9, Theorem 2.1 and its proof; bounded versus unbounded disjunctive hulls and zero weights. |
| [[wu2026-variable-aggregation-based-perspective-reformulation]] | Original PDF pp. 11–12, Assumption 1, Lemmas 2–3 and Theorem 3. The supplementary proofs cited there were not present in this inspected passage. |
| Starr, `starr1969.pdf` | PDF pp. 12–13, printed pp. 35–36, Appendix 2, especially Lemma 2 and its corollary. |
| [[fawzi2013-exponential-lower-bounds-on-fixed]] | Original PDF p. 3, Theorem 1 and Lorentz-cone decomposition discussion; constants, fixed block size, and $m\ge d$. |
| Lee–Raghavendra–Steurer, `lrs-sdpsize.pdf` | PDF p. 23, Theorem 3.8 and (3.11), and pp. 32–34, Theorems 5.3–5.4 and the pseudo-density argument used for the inherited exponent. |
| Braun et al., `braun2013-approxlp.pdf` | PDF p. 18, Theorem 6(i) and the start of the hard-pair application. |
| Schoenebeck, `schoenebeck-full.pdf` | PDF pp. 7–11, Definition 10, Theorems 11–12, Lemma 13, and the signed-vector construction. |
| [[belotti2012-on-feasibility-based-bounds-tightening]] | Original PDF pp. 1–2; continuous linear limit computation versus primitive FBBT iteration. |
| Etessami–Yannakakis, `ey-rmc.pdf` | PDF pp. 26–28, Theorem 5.2 and the gate-normalization/sign/amplification proof. |
| [[esparza2010-computing-the-least-fixed-point]] | Original PDF p. 34, Section 7, Theorem 7.1 and proof. |
| [[stewart2015-upper-bounds-for-newtons-method]] | Original PDF pp. 21–22, Section 4.1, equation (18) and repeated-squaring discussion. |
| [[lubin2022-mixed-integer-convex-representability]] | Original PDF p. 12, Lemma 4.1 and parity proof. |
| [[beach2024-enhancements-of-discretization-approaches-for]] | Original PDF p. 21, Section 5.1.1; the distinct upper and lower piecewise-square errors. |

The short PDF filenames above identify files in `/tmp/minlp-relaxation-limits-sources/`. This table records selected original passages, not complete readings of those entire external papers. In particular, I did not independently re-audit every external theorem cited in the earlier stages; those limits are recorded below.

## Findings

1. **R09-1 — MINOR: state the three catalogue members explicitly.** Location: Proposition G.4, PDF p. 96; `sections/appendix-scaling.tex:143–146`; associated coverage-ledger entry at line 194. The phrase “the finite catalogue contains $0<s<M=\max\Lambda$” should explicitly say that **zero, $s$, and $M$** are catalogue members. The appendix's general convention only requires a nonnegative compact scale set; it does not globally require zero membership. The proof on p. 97 uses the zero slice and the $M$ slice to obtain $(s,s\xi,(s/M)T_1+(1-s/M)T_0)$, and its converse describes the full mean-scale interval as $[0,M]$.

   This is a consequential distinction in interpreting the wording: if “contains” were read as asserting only $s\in\Lambda$ and $0<s<M$, then $\Lambda=\{1,2\}$, $s=1$, and the nonrectangular $E=\{(\xi,T):\xi=T\in[0,1]\}$ contradict the criterion. With two scales, the mean fixes their weights and every scale-only cost separates. The intended three-member assumption is clear from the proof and the following discussion; I therefore classify this as a local statement clarification rather than a defect in the intended result. **Repair:** write “let $\Lambda\subset[0,M]$ be finite, with $\{0,s,M\}\subseteq\Lambda$ and $0<s<M=\max\Lambda$.” Apply the same explicit membership wording in the coverage ledger.

2. **R09-2 — MINOR: reverse one word in the coverage ledger.** Location: frozen `process/claim-coverage.md:67`, row for `results/positive-multilinear-incidence-sparsity-gap.md`. It says “ownership of incoming low coordinates.” The incidence proof assigns ownership to incoming **high** coordinates; low events are placed in the common anchor. The manuscript proof uses the correct convention. **Repair:** replace “low” by “high” in that ledger cell.

## Independent verification

### P-split counterexample, projection, and coordinate effects

For Example H.1 I checked all four box vertices individually: the two with $t=0$ satisfy the first ball inequality, and those with $t=3$ satisfy the second. Thus the retained box equals the true hull. The explicit auxiliary segment between $(0,9,1)$ and $(9,0,1)$ dominates the three square functions throughout the box. The higher-dimensional construction has positive diagonal quadratic coefficients and contains every box vertex. This also prevents the source's informal “few constraints” setting from rescuing its universal statement.

The original Theorem 6 proof has both failures identified in the manuscript: strict convexity gives strict Jensen slack only in a component whose arguments differ, and an outward movement from a retained-domain facet need not remain in the domain. Proposition H.2 supplies the missing directional conditions. Its common positive step follows from finitely many links; convexity of the relaxation and containment of the entire feasible set justify the asserted strict containment of its hull.

For Proposition H.3, fixing $c\ge0$ with $\sum c_i\le r^2$ gives $h=r^2-\sum c_i$. The auxiliary cross-section is the union of two rectangles, whose hull is exactly the truncated square $0\le a,b\le U, a+b\le U+h$. This establishes sufficiency, including $h=0$, without an unsupported interchange of slicing and convexification. Downward closure then permits substitution of the true squares. I checked the completed-square ellipsoid, its implication of the retained bounds, and the two-group case where the original transverse upper bound is reduced to $r^2$ by either disjunct.

For the Hausdorff calculation, on the left of the capsule the farthest admissible point at transverse radius $\rho$ has $t=-e(\rho)$. The derivative of its squared center distance with respect to $\rho^2$ is

\[
\frac12+\frac{d}{4\sqrt{(d/2+r)^2-\rho^2/2}}>0.
\]

Thus the extremum is at $\rho=r$, and subtracting $r$ gives the claimed distance. At $\rho=0$ the excess is zero; no omitted positive-part operation changes the maximum. The ratio limit is $\sqrt2-1$. The additive refinement claim is restricted to the original box, as it must be.

For Proposition H.4, the rational matrix is orthogonal and equals its inverse. At $p=(2D,4D/3)$ it gives $t=34D/15\in(0,5D)$ and $w=4D/5$. Each original square is at most $4v_i^2/9$, and twice that value is below its global bound $(v_i+1)^2$. The half-weight lift therefore works. Orthogonality makes the distance to the capsule exactly $4D/5-1>0$. At the aligned left end, the inverse map and $|w|\le1$ give $-1\le x_1\le4/5$, $-1\le x_2\le3/5$, hence squared center distance at most two. Reflection gives the other end. This proof uses the actual transformed domain, not its bounding box. Rational $D\ge2$, the endpoint value $D=2$, determinant $-1$, and the optional sign flip of $w$ are all consistent.

### Every auxiliary-only convexification and the exact-image repair

Proposition H.5's strongest quantifier is justified directly. Any convex $Q$ containing the two feasible center images contains their midpoint. Every midpoint entry is $v_i^2/2$, whereas each witness square is at most $4v_i^2/9$. There is slack $v_i^2/18$ in every such comparison. No description of $Q$, closure assumption on it, or ability to compute it is needed. This covers the exact feasible auxiliary image hull. It does not cover cuts involving original coordinates or replacement of the epigraph map; the final paragraph correctly states that boundary.

In aligned coordinates, $f(c)=d^2+1-c+2d\sqrt{1-c}$ is decreasing and concave on $[0,1]$. At every feasible image both $a,b\le f(c)$; the two hypographs therefore contain the convex image hull. Since $c\ge w^2$, monotonicity gives $t^2,(t-d)^2\le f(w^2)$. The two resulting intervals intersect in exactly

\[
-\sqrt{1-w^2}\le t\le d+\sqrt{1-w^2},\qquad |w|\le1.
\]

This is the capsule. The reverse containment follows from convexity and inclusion of both balls, with the retained domain containing their hull. I also checked the claimed conic representation: an $s\ge0$ with $s^2+c\le1$ and $a+c-d^2-1\le2ds$ exists exactly when $a\le f(c)$; choosing $s=\sqrt{1-c}$ proves sufficiency, including $c=1$. The second inequality is identical with $b$. Thus the exact-image repair is not merely an appeal to convexifying the full graph.

### Remaining manuscript

I reconstructed the principal transitions while reading the full paper: common vertex laws and induced-cell vertices; the harmonic normalization and cubic dual certificates; ownership and compatible global laws in the incidence construction; residual gluing for feedback deletion; the degree-slab odd-cycle argument; and the active/blocking invariant in the series-parallel proof. I checked the dyadic/radix limiting profiles, coefficient-spread reduction at global extrema, balanced fixed-ambient construction, and the rational error estimates in the PARTITION reduction. These checks found no additional defect.

For the spatial and hierarchy material I checked the endpoint-witness counting, PSD covariance, homogeneous reduction of the fractional Gram calculation, indicator localizers, coordinate-wise endpoint pullback, and tensor treatment of globally nonnegative squares. For the XOR material I checked degree $4r$, the substituted degree $4rD$, inclusion of the constant in the signed Gram realization, and the distinction between the actual box distribution used for the order-one upper construction and the graph identities imposed in moments. I did not infer a spatial-node bound from a bound on another resource.

For the new supporting appendices I checked the point-packing covariance witnesses; scaling endpoint interpolation, multiplicities and the zero-weight conic argument; the extensive-cost size-biased/product-weight proof; the stated Shapley–Folkman consequence; the explicit correlation-face inverse and exposure; the stability constants and section transfer; the FBBT detector/amplifier recurrences; and the parity, width and area arguments in the integer comparison. Except for R09-1's membership wording, these checks found no defect. The manuscript appropriately distinguishes inherited lower bounds, self-contained transfers, and examples that do not support a general algorithmic claim.

### Exact computational and production checks

- I wrote `verification/reviewer09/stage06-round01/check_psplit.py` independently, using Python `Fraction` and exact active-set enumeration. It checks every vertex of the proposed auxiliary polytope for one through four transverse variables and the three $(r,d)$ pairs $(1,3),(2/3,7/4),(5/2,9)$. Every vertex belongs to an original auxiliary disjunct; the respective vertex counts are 8, 11, 14, and 17. It also checks the rational map and witness arithmetic for $D=2,7/3,10,1000$. Results are in `check_psplit.json`. These are finite exact checks, not certificates of the universal or asymptotic statements.
- I ran the frozen finite cubic checker in an isolated copy; all six printed finite certificates passed. I separately extracted and executed the complete integer program printed in `appendix-finite-signings.tex`; its output was `[1, 2, 4, 4, 5, 8]`. I reviewed its switching normalization and enumeration coverage. These executions verify the stated finite claims only.
- I copied the frozen build inputs into `verification/reviewer09/stage06-round01/build/` and ran its build/check script. It returned compile exit 0, no warnings, no duplicate labels, a matching printed cubic checker, and 111 pages. Evidence is `build/verification/build-report.json` and `build/verification/build-output.txt`. The rebuilt PDF hash differs from the frozen PDF; the build records a new creation time, and I do not claim byte identity.
- I visually inspected frozen PDF pages 96–100 and the published P-split source p. 16. Those pages are readable and unclipped. Full manuscript coverage above refers to complete TeX reading; it does not mean every rendered page received a separate visual inspection.

## Remaining limits

I did not reprove the external extension-complexity theorems, the external random-XOR width lower bound, or every classical optimization and multilinear-hull result cited in the earlier stages. The original-source table identifies the passages actually checked. In particular, the Schoenebeck width result's complete external proof, Wu's supplemental proofs, and all earlier-stage bibliographic dependencies were not independently audited end to end. I found no conflict between the checked source scopes and the manuscript's uses. These limits should not be replaced by earlier PASS labels.

The exact computations cover their explicitly listed finite instances. I did not run a numerical solver, enumerate arbitrary dimensions, or conduct an exhaustive novelty search. The complete manuscript proof reading and the detailed P-split derivations are the basis of this verdict; the successful build and finite checks provide additional, narrower evidence. This review is for the present stage and does not replace the planned final whole-paper loop.
