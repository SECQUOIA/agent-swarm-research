# Stage 6, round 1, independent review 03

**Verdict: PASS.** I found no demonstrable mathematical, attribution, scope, or local editorial defect requiring repair in the assigned frozen manuscript. This verdict follows a fresh reading and reconstruction; earlier PASS labels were not used as proof.

The additional emphasis was incidence width, frequency, feedback, positive boxes, algorithmic claims, and the boundaries of those results. It did not narrow the full review.

## Coverage

All manuscript paths below are relative to `process/snapshots/stage06-round01/`. I verified that `main.pdf` has SHA256 `343b29156e275df970236babbab1077b3a53261317e0995a6a7ea0398b583916`. The frozen PDF has 111 pages.

I read the entire `main.tex`, `macros.tex`, and `references.bib`, and all of these complete source files, including every proof and appendix:

- `sections/01-foundations.tex`
- `sections/02-universal-positive.tex`
- `sections/03-cubic-equal-means.tex`
- `sections/04-incidence-interiority.tex`
- `sections/05-feedback-frequency.tex`
- `sections/06-treewidth-two.tex`
- `sections/07-positive-boxes.tex`
- `sections/08-exact-complexity.tex`
- `sections/09-cardinality-spatial.tex`
- `sections/10-cardinality-preordering.tex`
- `sections/11-coordinate-domains-lifts.tex`
- `sections/12-relative-blocks-cuts.tex`
- `sections/13-xor-quadratic-hulls.tex`
- `sections/14-monomial-reformulations.tex`
- `sections/15-finite-certificates-affine.tex`
- `sections/16-supporting-comparisons.tex`
- `sections/17-synthesis.tex`
- `sections/appendix-cubic-certificates.tex`
- `sections/appendix-fbbt.tex`
- `sections/appendix-finite-signings.tex`
- `sections/appendix-integer-comparison.tex`
- `sections/appendix-p-split.tex`
- `sections/appendix-point-packing.tex`
- `sections/appendix-positive-box-predecessors.tex`
- `sections/appendix-positive-couplings.tex`
- `sections/appendix-rank-one.tex`
- `sections/appendix-scaling.tex`
- `sections/appendix-structural-auxiliary.tex`

This is a complete source reading of the manuscript, not a complete visual reading of all 111 rendered pages. I separately rendered and inspected PDF pages 1, 4, 36, 43, 93, 96, 99, 102, 105, 107, 110, and 111. The inspected tables, equations, proof endings, and bibliography pages were readable and showed no clipping or unresolved references.

I read the frozen `process/review-protocol.md`, `process/stage-06-review-assignment.md`, `process/stage-06-author-assignment.md`, `process/stage-06-author.md`, `process/scope-proposal.md`, and complete `process/claim-coverage.md`. I read repository `literature/AGENTS.md` before inspecting originals. I did not read another current-round review or modify the manuscript or snapshot.

### Primary-source checks

The following records distinguish checking a relevant original passage from independently proving an entire external theorem. Local originals were inspected directly, using PDF text extraction and, where needed, original-page images. Page numbers marked PDF are file page numbers; printed page numbers are explicitly identified.

| Source and locator | What was checked |
| --- | --- |
| Cornuéjols, *Combinatorial Optimization: Packing and Covering*, Theorem 6.5, printed p. 76; adjacent context p. 77; Theorem 6.13, printed p. 82 | Camion's Eulerian-submatrix criterion and the balanced-matrix integrality statement used by the width argument. The Camion page was also inspected visually. |
| Hassin–Tamir, *Efficient Algorithms for Optimization and Selection on Series-Parallel Graphs*, Theorem 3.1, printed p. 381/PDF p. 3 | Original scanned page: the block characterization and the surrounding series-parallel definition. The manuscript's additional coloring invariant was reconstructed independently. |
| Edmonds, *Maximum Matching and a Polyhedron with 0,1-Vertices*, printed pp. 125–126 | Original NIST PDF, introductory weighted-matching algorithm and polyhedral statements. I did not reprove the blossom algorithm. |
| Deza–Onn, *Optimization over Degree Sequences*, arXiv:1908.09278, Theorem 1.2 and Section 3, PDF pp. 1–6 | Original PDF, including the matching-gadget reduction. The manuscript's mandatory-slot gadget was checked separately. |
| Grötschel–Lovász–Schrijver, *Geometric Algorithms and Combinatorial Optimization*, Theorem 6.4.9, printed p. 179 | Strong separation/violation/optimization equivalence for well-described polyhedra and the beginning of its proof. |
| Davidson–Donsig, *Norms of Schur Multipliers*, Theorem 2.3, PDF pp. 7–8; proof opening p. 13 | Pattern density parameter and square-root bounds in the [authors' original PDF](https://www.math.uwaterloo.ca/~krdavids/Preprints/DavDon_schur.pdf). This was an attribution/statement check, not a full reconstruction of the operator-theoretic proof. |
| Boland et al., *Bounding the Gap between the McCormick Relaxation and the Convex Hull for Bilinear Functions*, PDF pp. 2–3 | Definitions, Theorems 1–4, square-root order, and signed-cycle exactness scope. |
| Luedtke–Namazifar–Linderoth, *Some Results on the Strength of Relaxations of Multilinear Functions*, author manuscript PDF p. 22 | Original Conjecture 1 and its stated setting. |
| Sherali, *Convex Envelopes of Multilinear Functions over a Unit Hypercube and over Special Discrete Sets*, printed pp. 252–253/PDF pp. 8–9 | Equation (13), Theorem 3, and the beginning of its proof. |
| Adams et al., *Error Bounds for Monomial Convexification in Polynomial Optimization*, Proposition 4.1, printed p. 22 | Original-page image: both common-ratio envelope formulas and their proof. |
| Schoenebeck, author full version of *Linear Level Lasserre Lower Bounds for Certain k-CSPs*, Theorems 11–12, Lemma 13, Appendix Theorem 21/Proposition 22 | The signed Gram construction and closure argument; the expansion and unsatisfiability proof, including the final union bound. The manuscript's repaired normalized construction was checked on its own terms. |
| Anstreicher, *Semidefinite Programming versus the Reformulation-Linearization Technique for Nonconvex Quadratically Constrained Quadratic Programming*, Section 4, PDF pp. 12–13 | The point-packing formulations and four conjectured values. |
| Khajavirad, *The Circle Packing Problem: A Theoretical Comparison of Convexification Techniques*, Remark 1 and Propositions 1 and 3 | RLT, interval-dependent symmetry/secant conventions, values and size ranges in the [original arXiv version](https://arxiv.org/html/2404.03091v1). |
| Balas, *Disjunctive Programming: Properties of the Convex Hull of Feasible Points*, Theorem 2.1, printed pp. 7–9/PDF pp. 5–7 | Disaggregated hull statement and proof; comparison with the manuscript's bounded, self-contained specialization. |
| Wu et al., *Variable Aggregation-Based Perspective Reformulation for Mixed-Integer Convex Optimization with Symmetry*, PDF pp. 11–12 | Assumption 1, Lemma 3, Theorem 3, and surrounding formulation. Supplemental proofs were not available in the inspected main PDF and were not checked. |
| Kronqvist–Misener–Tsay, published *P-Split Formulations: A Class of Intermediate Formulations between Big-M and Convex Hull for Disjunctive Constraints*, PDF pp. 4–7 and 15–16 | Retained domain, sharing convention, assumptions, and Theorem 6 with its proof. The manuscript's counterexample correctly addresses the strict-convexity inference in that proof. |
| Starr, *Quasi-Equilibria in Markets with Non-Convex Preferences*, printed pp. 35–36/PDF pp. 12–13 | Lemma 2, its proof, and corollary. |
| Fawzi–Parrilo, *Exponential Lower Bounds on Fixed-Size PSD Rank and Semidefinite Extension Complexity*, PDF p. 3, Theorem 1 | Exact fixed-block constants and Lorentz-cone decomposition discussion. |
| Lee–Raghavendra–Steurer, author version, Theorem 3.8/(3.11), PDF p. 23; Theorems 5.3–5.4, PDF pp. 32–34 | Quantitative rank statement, pseudo-density normalization/interpolation, norm bound, and stated exact correlation-polytope consequence. The full proof of Theorem 3.8 remains an inherited input. |
| Braun et al., *Approximation Limits of Linear Programs (Beyond Hierarchies)*, PDF p. 18, Theorem 6(i) and surrounding hard pair | Fixed-dilation LP obstruction used after the manuscript's stability transfer. The full communication lower-bound proof was not reconstructed. |
| Etessami–Yannakakis, *Recursive Markov Chains, Stochastic Grammars, and Monotone Systems of Nonlinear Equations*, Theorem 5.2, PDF pp. 26–28 | Circuit normalization, sign detector, and amplification proof. |
| Belotti et al., *On Feasibility-Based Bounds Tightening*, PDF pp. 1–2 | Scope of continuous linear FBBT limit computation and nonfinite iteration. |
| Stewart–Etessami–Yannakakis, *Upper Bounds for Newton's Method on Monotone Polynomial Systems*, Section 4.1/(18), PDF pp. 21–22 | Recurrence and its iteration context. |
| Esparza et al., *Computing the Least Fixed Point of Positive Polynomial Systems*, Section 7, Theorem 7.1/(14), PDF p. 34 | Original slow-convergence construction and proof. |
| Lubin–Vielma–Zadik, *Mixed-Integer Convex Representability*, Lemma 4.1, PDF p. 12 of the cited arXiv version | Parity-midpoint argument and its scope. |
| Beach et al., combined 2022 preprint, Section 5.1.1, PDF p. 21 | Upper and lower square-approximation errors and the version-specific locator used in the manuscript. |

Some source passages were obtained from already-present original PDF files under `/tmp/minlp-relaxation-limits-sources/`; I did not independently authenticate their original download transport. I rejected an unrelated file encountered while locating Edmonds and instead inspected the original NIST article. The Deza–Onn HTML request failed, but its actual arXiv PDF was accessible and inspected.

## Findings

None. There are no major or minor finding IDs and no required repairs from this review.

## Independent verification

### Structural theorems and algorithms

1. **Feedback gluing.** I reconstructed the domination/residual argument, including endpoint and zero-mass cases. For each desired state, one orientation pattern of probability `2^(-f_F)` aligns the relevant events at an endpoint. Thus the reference marginal satisfies `Q_i(s,b) >= (P_e)_(F,i)(s,b)/2^(f_F)`. Subtracting the scaled local marginal leaves consistent nonnegative residual masses. One gluing on the resulting incidence forest gives the global law. The proof does not multiply the loss again along a path. For physical products the local affine upper majorant is used on the original factor scopes, so the feedback parameter is not silently computed after expansion.

2. **Frequency two.** I reconstructed the degree-slab vertex argument. After integral coordinates are removed, a fractional full-rank component is an odd cycle with values one half; dummy vertices and parallel edges do not create an omitted exceptional component. Matching/complement rounding on a cycle of length `l` supplies the stated `1 - 1/(2l)` coverage. The baseline `b = max p` must remain in the calculation, and it does. Its convexity has the correct Jensen direction. The cardinality lower envelope is affine on each slab and the upper envelope is concave, giving the claimed averaged bound. The positive-box corollary is restricted to a common aspect ratio on a factor and does not assert the same theorem for arbitrary unequal ratios.

3. **Polynomial bit complexity.** I checked the edge-cover reduction, including negative edge costs, uncovered-vertex penalties, the added hub/mate, and the matching completion argument. For convex degree tables, each mandatory pair is either matched internally or both vertices consume endpoint slots. Reassigning the used slots to the cheapest slots gives the telescoping table increments. The bonus `2W + 1` forces mandatory coverage without changing the intended optimum. The gadget has polynomial size in the explicitly listed tables. In the marginal-envelope LP, affine majorants and full-rank rational vertex systems give polynomial encoding bounds; rational boundary means do not invalidate the oracle claim.

4. **Incidence width two.** I reconstructed the active/blocking terminal invariant through every series and parallel case. In a parallel composition, a new simple cycle consists of two terminal paths. The terminal-factor correction is one for mixed terminal types and zero for equal types. This gives the required prohibition of monochromatic odd-factor cycles. The subsequent Eulerian-submatrix decomposition really needs Camion's full criterion, not merely an induced-cycle assertion; the manuscript uses the full criterion. Decomposing into cycles of length divisible by four establishes its hypothesis. I also checked the complete-pair construction and fixed-aspect asymptotic sharpness.

5. **Positive-box coefficients.** For the global-minimum/global-maximum move, I recalculated `ΔC_j = -binom(d-1,j-1) h` and `ΔC_(j-1) = -binom(d-1,j-2) h`. The adjacent-cardinality term is constant because the mean sum is fixed. The product change is bounded by the second binomial coefficient times `h`; the orientation change is bounded below by minus the first coefficient times `h`, even when orientation coins are dependent. These inequalities give the stated nonpositive change of the coefficient. Restricting to a boundary retains the ambient orientation law, so induction does not incorrectly replace it by a newly balanced lower-dimensional law. The unequal-box expansion has nonnegative coefficients and the termwise-gap inequality has the correct direction. It is used for the aspect-ratio result, with no unsupported preservation of the original incidence structure.

### Independent exact falsification checks

I wrote and ran `verification/reviewer03/stage06-round01/check_structural.py`; results are in the adjacent `check_structural.json`. It is independent of the author's checkers and uses exact `Fraction` arithmetic and integer graph enumeration.

- For ambient dimensions 2 through 5, every support size, and all sorted quarter-grid means including 0 and 1, I integrated the full ambient balanced-orientation law exactly and independently enumerated the product law. All **2,547 coefficient inequalities** passed. Exchangeability justifies sorting the means for these particular moment expressions. This includes ambient/support-size mismatches and boundary restrictions.
- I enumerated all connected bipartite graphs with at most seven vertices in the NetworkX graph atlas, tested width at most two by recursive degree-at-most-two elimination with fill, enumerated all simple cycles, and searched every factor coloring for both bipartition choices. All **62 graphs / 124 factor-side choices** admitted the required coloring.

Run command:

```text
/home/sgusev/miniconda3/envs/minlp-notes/bin/python paper-relaxation-limits/verification/reviewer03/stage06-round01/check_structural.py
```

These finite checks are attempts to falsify the universal statements; they do not prove them. No numerical optimization solver was used in these checks.

### Full-paper checks beyond the additional focus

I reconstructed the signed-cut normalization, half-integral cell argument, and polarization; the harmonic cutoff and inactive-mass accounting; the dyadic/radix profiles; the cubic finite and scalar-envelope calculations; and cloning's simultaneous concentration requirement. The interiority statement keeps its joint dimension restrictions. The PARTITION reduction concerns exact rational comparison and does not establish a fixed-additive-error hardness result.

For the cardinality family, I checked the falling-factorial moment formulas, positivity argument, reduction of products of assignment factors, and all displayed degree budgets. Endpoint affine substitution makes the graph-lift transfer degree-loss-free. Full-graph objective agreement is used where needed. For XOR, I checked signed closure/Gram consistency, the `4r` and `4rD` budgets, endpoint quadratic realizability on the whole box, and parity-rank counting using original basis rows. A full-box quadratic law is correctly distinguished from a graph-supported law. The order-one quadratic certificate and order-two Bernstein certificate have separate justifications. The spatial claims quantify their oracle and region families; arbitrary global acceleration is not smuggled into the lower-bound model.

In the supporting comparisons, I recalculated the point-packing covariance and group-distance certificates; checked the scaled common-intensive hull, extensive-only cost perspective and zero slice; and reconstructed the scale-cost counterexample and rectangularity argument. For P-split I checked the exact auxiliary hull, the ball/capsule distance calculation, retained-domain witnesses, and the distinction between actual quadratic images and unrestricted auxiliaries. For the rank-one appendix I recalculated the exposed correlation face, stability constants `136m + 10` and `184m + 6`, and the induced error scale; the LRS prefactor and logarithmic qualifications remain explicit. For FBBT I checked the least-fixed-point lower-limit argument, normalized circuit construction, small strongly connected components, and the schedule-independent primitive-contractor invariant. The doubly exponential claim excludes equation aggregation and global contractors. Finally, I reconstructed the parity-class closures, square midpoint error, bilinear area bound, and graph fractional-cover precision calculation.

These are mathematical reconstructions and adversarial boundary checks, not machine-checked proofs. I did not rerun the author's entire verification suite or independently enumerate every printed finite-signing table.

## Remaining limits

- I have not independently proved every inherited external theorem. In particular, sharp Khinchin, weighted blossom optimization, the general oracle-equivalence theorem, and the general communication/PSD-rank lower bounds remain external inputs. The source statements inspected above support their manuscript uses; the report does not claim complete source-proof verification.
- I did not freshly inspect every bibliography entry's original. Examples include the original Szarek proof, original Grigoriev proof, and all ancillary branch-and-cut comparison papers. The manuscript's local cardinality positivity proof was checked directly. This is not an exhaustive priority or historical-attribution clearance.
- The Wu supplemental proof was not checked. No manuscript conclusion was accepted solely by inferring that absent proof.
- PDF inspection was limited to the twelve listed pages. The whole mathematical text was read in source form; this is not a full typographic audit or an independent clean rebuild.
- The exact finite-aspect positive-box constant, extensions beyond the stated width/frequency/domain assumptions, and stronger spatial or global algorithm models remain separate questions. The manuscript marks those boundaries and does not need to solve them to justify the results stated here.

This is the assigned Stage 6 review and does not replace the separate final whole-paper review loop.
