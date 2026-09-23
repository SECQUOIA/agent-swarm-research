# Stage 6, round 1 — independent review 02

**Verdict: PASS.** I found no demonstrable mathematical, scope, attribution, or presentation defect requiring a revision. This is an independent review of this frozen stage, not a certification of every external theorem or a replacement for the separate final whole-paper loop.

**Frozen target:** `process/snapshots/stage06-round01/main.pdf`, 111 pages, SHA256 `343b29156e275df970236babbab1077b3a53261317e0995a6a7ea0398b583916`.

## Coverage

I read `literature/AGENTS.md` before opening local originals. I read the frozen `process/review-protocol.md`, `process/stage-06-review-assignment.md`, `process/stage-06-author-assignment.md`, `process/stage-06-author.md`, `process/scope-proposal.md`, and `process/claim-coverage.md` completely. I read `main.tex`, `macros.tex`, the complete `references.bib`, and all the following frozen manuscript files completely, including displayed proofs and code:

- `sections/01-foundations.tex`, `02-universal-positive.tex`, `03-cubic-equal-means.tex`, `04-incidence-interiority.tex`, `05-feedback-frequency.tex`, `06-treewidth-two.tex`, `07-positive-boxes.tex`, `08-exact-complexity.tex`.
- `sections/09-cardinality-spatial.tex`, `10-cardinality-preordering.tex`, `11-coordinate-domains-lifts.tex`, `12-relative-blocks-cuts.tex`, `13-xor-quadratic-hulls.tex`, `14-monomial-reformulations.tex`, `15-finite-certificates-affine.tex`, `16-supporting-comparisons.tex`, `17-synthesis.tex`.
- `sections/appendix-finite-signings.tex`, `appendix-positive-couplings.tex`, `appendix-cubic-certificates.tex`, `appendix-structural-auxiliary.tex`, `appendix-positive-box-predecessors.tex`, `appendix-point-packing.tex`, `appendix-scaling.tex`, `appendix-p-split.tex`, `appendix-rank-one.tex`, `appendix-fbbt.tex`, `appendix-integer-comparison.tex`.

Thus the review includes all main sections, Appendices A–K, the abstract, roadmap, synthesis, open questions, and bibliography. I compared the scope and coverage ledgers with these arguments; I found no omitted in-scope development or open result presented as proved. I did not independently reread every historical repository note behind each ledger row.

The reading was primarily of LaTeX source. I additionally rendered and visually inspected PDF pages 1, 16, 20, 23, 85–87, 96–97, 102, 104, 107, and 111. These include the abstract, harmonic inequalities, cubic law and exact table, executable finite certificates, perspective and rectangularity statements, stability and approximate lift transfer, and integer precision. I found no clipped equation, unreadable table/code, missing qualifier, or broken reference on those pages. I did not visually inspect all 111 pages or independently rebuild the PDF.

I used the author validation records as source locators, not as evidence that a theorem or computation is correct. I did not read any other current-round review or spawn an agent. I changed no manuscript or snapshot file.

## Findings

None. There are no major or minor finding IDs and no requested repairs.

## Independent verification

### Universal asymptotics and rounding

For Sections 2–4 and Appendices A–B, I reconstructed the common-law interpretation, the half-grid cut reduction, the row-norm orientation argument, the dyadic hull certificate, and the harmonic proof. Important checks were:

1. The harmonic failure probability integrates to its prescribed marginal, including the zero-failure convention. With an inactive failure mean satisfying `p < t/M`, the aggregate inactive mass is at most `(d-1)t/M`; this is the loss used in Lemma 4.3. The resulting union probability is a lower bound, so it has the direction required for a deficiency guarantee.
2. The convex tangent inequality for `J` at its fixed point gives one mixture working termwise; its weights are global. The Lambert estimate uses `w >= 1`, so `w-1/(2w)` is positive and at least one half. The logarithmic inequality used to prove the finite estimate applies in that range. The tuning `M=(d-1)(1+log(d-1))` gives the stated denominator `log N-log log N+o(1)`. The text correctly calls this an upper certificate and does not infer a matching second-order lower expansion.
3. In the dyadic and radix lower examples, the affine supporting line is valid at every integer count, while the constructed profiles attain its active segment. Mixture weights restore the prescribed means. The dyadic cutoff argument and the simpler `b >= L` radix regime are kept separate. Passing to the largest admissible parameters covers all sufficiently large integer degrees; a subsequence alone is not being used to assert the universal leading limit.
4. The unit-coefficient replacement concentrates uniformly over all clone vertices and also controls the termwise quantity. The union bound has `2^(nm)` vertices and the chosen deviation is of order `m^((d+1)/2)` for fixed `d >= 2`; after dividing by `m^d`, the error vanishes. The compact vertex-law formulation makes this uniform control sufficient for both envelopes. Padding and moving to the interior preserve the asserted limiting supremum, without creating a claim of finite attainment.

I wrote an independent checker, `verification/reviewer02/stage06-round01/independent_checks.py`, without importing an author checker. Its exact radix tests check means, active lines, and intercepts for 48 pairs `b=2,...,7`, `L=2,...,9`. These finite tests do not verify every radix or substitute for the countwise proof.

The same checker uses SciPy quadrature and scalar root solving for 18 harmonic parameter choices: `d` in `{2,3,10,1000,10^6,10^12}` and three allowed values of `M`. Every applicable Lambert lower bound lay below the computed fixed point. These are numerical falsification probes, not rigorous interval certificates or an asymptotic proof.

### All finite cubic certificates and attainment distinctions

I reconstructed the three-law case split in Theorem 5.2. Low/low cases, exactly one low coordinate, and all-high cases have the claimed lower bounds, including the boundary means. The fixed mixture's optimality is expressly limited to mixtures of those three laws. An independent exact integration of the orientation, independent, and Bernoulli conditional laws passed on all 2,002 sorted quadratic/cubic mean vectors with denominator 20, including boundaries. The finite grid does not prove the continuous theorem.

For the analytic cubic lower certificate, I independently checked the reduction to the boundary minimizer and the Hessian-based exclusion argument, then expanded all five Bernstein representations in exact symbolic arithmetic. Their minimum coefficient is `901/120000`, giving the reduced lower bound `1610000/743033`. Neither the minorant nor its expectation is assumed attained. The explicit sentence on PDF page 23 correctly prevents interpreting this lower bound on `R_3` as convergence of the actual family ratios.

For Proposition 5.5 and Appendix C, I independently enumerated every count state and checked each affine minorant, all atom probabilities and means, primal/dual objective equality, upper envelopes, individual lower envelopes, and final fractions:

| Group size | Count states | Exact convex envelope | Exact concave envelope | Sum of individual lower envelopes | Exact ratio |
|---|---:|---:|---:|---:|---:|
| 6 | 343 | `2750/13` | `1647/4` | 10 | `20891/10411` |
| 8 | 729 | `3572/7` | 971 | 28 | `6601/3225` |
| 64 | 274625 | `34172072/105` | 587944 | 20832 | `7443345/3445256` |

There are 275,697 states in this three-group check. The uniformly chosen subsets conditional on each count law recover every coordinate marginal, so the count certificates really are envelope certificates in the original variables.

For the two-level family I checked both displayed square-factor identities symbolically. The finite grids at `m=4,8,12,16` give convex envelope values `11,120,441,1088` and ratios `27/16,21/11,99/50,135/67`. In particular the smaller displayed cases remain below two and the 32-variable case exceeds two. I checked the interior padding arithmetic `165025/80947` and `2700/1343`, including the loss `12/5` for the 52-variable example. The two-level asymptotic argument has a matching feasible expectation and minorant after normalization; it therefore proves convergence of actual ratios to `243/115`, unlike the earlier analytic lower certificate.

The checker completed successfully under Python with SymPy 1.14.0 and SciPy 1.18.1. Results are in `verification/reviewer02/stage06-round01/independent_checks.json`. Its SHA256 is `7d209e9aebb5e2366ee95ec05fc27b22abe4b832c69c4662b7457a1be882f2f6`. It also checks the frozen PDF hash. Exact arithmetic means rational/symbolic equality and finite exhaustive inequality checks here, not automated verification of the surrounding universal proofs.

### Structural, spatial, and reformulation arguments

I checked that the common-law arguments survive arbitrary allowed boxes and shared variables. The feedback-variable domination estimate and conditional gluing give the asserted multiplicative bound. The frequency-two rounding proof preserves the baseline terms; its polynomial-time convex-envelope argument uses the correctly convex piecewise-linear cardinality interpolation and a matching reduction, rather than treating an arbitrary degree cost as already convex. I followed the full two-terminal invariant through the series and parallel steps of the incidence-treewidth-two proof. I found no missing orientation, disconnected-component, or zero-gap case.

For positive physical boxes, the random orientation is sampled once for the ambient variable and retained across normalized terms. The extremal spreading argument and coefficient-regularity sum have the required monotonicity and normalization. The narrow unequal-box reduction uses exact rational arithmetic and polynomial encoding length. It establishes exact scalar-envelope hardness, with no claim of fixed-error approximation hardness.

For the spatial sections, I reconstructed the fractional-cardinality Gram decomposition, homogenization degree bound, and conditioning identity for arbitrary repeated slack products. The nonnegative falling-factorial coefficients have the required range; zero coefficients require no cancellation. Tensoring functionals restricts a PSD tensor product to the total-degree principal submatrix. The coordinatewise graph-lift argument uses the full graph box, endpoint interpolation, and full objective agreement. The more general monomial lift pays the declared degree loss. Neither conclusion silently assumes consistency that is unavailable at the oracle's order.

For the XOR construction, I checked the source-to-polynomial width budget, signed quadratic realization, witness counting, and the `rD >= 2` qualification. The independent finite upper certificates use precisely the agreements their oracle supplies. Cardinality and XOR obstructions concern certified region counts under the named node oracles; the text does not transfer them to unrestricted integer linear disjunctions or unrestricted global convex lifts.

### Stage 6 additions and precision

I reconstructed the supporting examples in the supporting comparisons and Appendices F–K:

- The point-packing SDP and RLT values use the specified diagonal secants and symmetry bounds. The manuscript gives published credit, including the earlier conjectural status in Anstreicher and the later proof by Khajavirad.
- The scale-cost counterexample distinguishes an extensive-only perspective from a model with an unscaled intensive coordinate. The rectangularity proof uses attained minimum-cost representations and the intermediate scale; the zero-scale fibre is stated explicitly. The integral-count hull argument needs integrality of the count polytope, not a stronger integer-decomposition property. The Shapley–Folkman comparison includes diameter, Lipschitz, and normalization qualifications.
- The P-split counterexample retains the original domain and sharing equations. The flaw in the inspected source proof is the direction of Jensen's inequality in constructing its auxiliary upper value. The corrected condition and translated-ball hulls respect that domain. The projected ellipsoid/cylinder and Hausdorff-distance calculations use the physical rotation; rational perturbation estimates support the finite rational instance.
- The correlation-polytope face is exact. In the stability proof the separate errors give `136m+10` for the face and `184m+6` for the perturbed section. The quantitative SDP transfer retains the shifted slack, the power `k^(-23/4)`, the inverse-quadratic precision scale, and the positive-pseudodensity parameter range. Fixed-size PSD block counts, total SOC dimension, unrestricted PSD order, and approximate LP size remain different resources.
- The FBBT transfer preserves every fixed point under sound contractions and attains the least fixed point under fair forward propagation. The normalized sign detector and amplifier have the required rational roots and separation. The every-schedule primitive bound follows from `l_z <= 1-(1-b)^K <= Kb`; this is a primitive-update result, not a lower bound for symbolic elimination, accelerated iteration, or arbitrary contractors. PosSLP hardness is not mislabeled NP-hardness.
- The square precision bound uses the correct midpoint error and has a matching secant/tangent construction. The product area argument and simultaneous-product coordinate-width estimate have their declared constants. The fractional vertex-cover coefficient comes from simultaneous edge constraints. Positive errors are explicitly required for logarithmic formulas, and closures handle nonmeasurable parity classes without granting extra lift assumptions.

## Primary-source audit and remaining limits

The following are direct original-source checks, not citations to prior reviews. Page numbers below are PDF pages unless explicitly marked printed. Local copies were read in place. This table specifies the material actually inspected; it does not claim a complete reading of each external paper.

| Source | Directly checked locator and purpose |
|---|---|
| Luedtke–Namazifar–Linderoth | Author PDF 5–9, 13, 22: recursive/termwise scope, vertex LP and common upper envelope, half-grid transfer, Conjecture 1. |
| Boland et al., gap paper | PDF 3–4, 6–7, 10–11: induced-cut gap identity, transfer corollary, asymptotic and exactness context. I did not completely audit their discrepancy proof. |
| Davidson–Donsig | PDF 4, 6–7, 11: Theorems 1.2 and 2.4, row/column characterization and finite weighted interpretation. |
| Sherali | PDF 8–9, printed 252–253: equation (13), Theorem 3 and the stated symmetric-box formula. |
| Adams et al. | PDF 22–23: Proposition 4.1 and its derivation for common-ratio boxes. |
| Cornuéjols | PDF 78–79, printed 76–77, and PDF 84, printed 82: Camion criterion and mixed balanced-system integrality. |
| Hassin–Tamir | Original scanned PDF 3, printed 381, visually inspected: Theorem 3.1 and SPM/block characterization. |
| Grötschel–Lovász–Schrijver | Original PDF 191, printed 179: Theorem 6.4.9, including rational exact optimization and polyhedral oracle scope. |
| Potechin | PDF 3, 8, 18: Theorem 1, Example 18, Theorem 44 and classical fractional-cardinality provenance. The manuscript supplies its own positivity proof. |
| Schoenebeck | Author full PDF 6–11, 16–19: random model, Theorems 11–12, Lemma 13's vector construction, and the expansion/width input. |
| Jarre | PDF 3–6: binary-knapsack and max-cut SDP obstruction with the stated branching model. |
| Ahmadi et al. | PDF 4 and 8: algebraic-disjunction/SOS definitions and Theorem 1. I did not audit the numerical experiments or complete Section 6. |
| Beame et al.; Fleming et al. | Stabbing Planes author PDF 3–4, printed 2–3; branch-and-cut author PDF 5, printed 4: the comparison models and finite-field refutation distinction. |
| Anstreicher; Khajavirad | Anstreicher PDF 12–13, Conjecture 4. Khajavirad's [primary HTML version](https://arxiv.org/html/2404.03091v1), model, Remark 1, Propositions 1 and 3 and the relevant proof calculations. |
| Balas; Wu et al.; Starr | Balas PDF 5–7, printed 7–9, Theorem 2.1 and bounded corollary; Wu PDF 12, Lemma 3 and Theorem 3; Starr PDF 12–13, printed 35–36, Appendix 2 including Lemma 2 and its corollary. |
| Kronqvist–Misener–Tsay | Original PDF 4–7 and 15–16: Assumptions 1–4, minimal sharing, retained-domain models, Definition 4, Theorem 6/Corollary 3 and the full problematic Jensen step. |
| Fawzi–Parrilo | Original PDF 3: Theorem 1, constants and SOC decomposition. |
| Lee–Raghavendra–Steurer | Author PDF 23, 32–34: Theorem 3.8/equation (3.11), Theorem 5.3 pseudodensity and Theorem 5.4. I checked the imported statements and the manuscript's transfer, not the complete external rank proof. |
| Braun et al. | Author PDF 18: Section 4.3 hard pair and Theorem 6, including dilation 2. I did not reprove the external nonnegative-rank lower bound. |
| Belotti et al.; Etessami–Yannakakis | Belotti PDF 1–2: linear FBBT scope. Etessami–Yannakakis PDF 26–28: Theorem 5.2 and normalization/detector/amplification proof. |
| Stewart–Etessami–Yannakakis; Esparza et al. | Stewart PDF 21–22, equation (18); Esparza PDF 34, Theorem 7.1 and equation (14), including proof. |
| Lubin–Vielma–Zadik; Beach et al. | Lubin PDF 12, Midpoint Lemma 4.1 and proof. Beach combined 2022 preprint PDF 21, Section 5.1.1 and Table 1: square maximum-error benchmark and version numbering. |

There are explicit external limits. The Coniglio anonymous review PDF redirected to an OpenReview browser-verification challenge; I could not independently inspect it. The bibliography already discloses that identity with the published version has not been verified, and the cited comparison is not a premise of a manuscript proof. Szarek's publisher record verified the bibliographic data, but its original download returned HTTP 403. I used the standard sharp real Khinchin theorem as an external input and did not independently reprove it. I did not open the original Edmonds matching-algorithm paper, the original Grigoriev paper, or every foundational citation such as McCormick, Padberg, or Karp; I checked the manuscript's uses against their stated standard contracts and, where noted above, directly inspected the later source supplying the needed theorem. No exhaustive literature-priority search was performed.

The universal results remain supported by mathematical argument rather than sampled numerical checks. Exact `R_3`, matching second-order universal asymptotics, and unrestricted extensions outside the named oracle/formulation models remain open or outside scope as the manuscript states. These limits do not supply a finding against the claims actually made.
