# Whole-manuscript review 04, round 01

Reviewer: stage08_review04. Date: September 9, 2026.

## Verdict

**Accept this review gate. No major issues and no valid minor issues identified.**

I read the entire manuscript source: the abstract, all seven sections, all four appendices, every theorem, proof and example, and the complete bibliography. I did not rely on earlier acceptance decisions and did not read other review reports. This is a review of the complete scientific argument and its integration, with additional executable checks of the scalar algorithms and dense screening.

The paper is a coherent, standalone mathematical manuscript. It distinguishes its combined structural guarantees from its classical ingredients, and distinguishes global optimization from stationarity, exact output from accuracy-bit output, and original contacts from convexified responses. The results support a substantial theoretical paper rather than only a report of solver experiments. No theorem repair or further development is needed on the evidence of this review. This is an independent review judgment, not a guarantee of journal acceptance or a proof that no further research is possible.

## Frozen input and build

I verified all 31 file hashes in `process/snapshots/stage08-round01/SHA256.json` and its own SHA256:

`d487e138b70585e03d5affa52a23e03631a30a45165651ddbe9d286162643231`.

I copied the snapshot into `verification/stage08-review04/isolated` and built it with:

```sh
latexmk -pdf -interaction=nonstopmode -halt-on-error -outdir=build main.tex
```

The build exited successfully and produced 78 pages. The final LaTeX log contains no warning, undefined reference or overfull box. I visually inspected the first page, literature comparison table (page 5), contact figure and surrounding mathematical text (page 53), screening table and discussion (page 57), and final bibliography page. The table and figure are legible and have correct labels; no cropped material or layout defect was found. The last page contains the last bibliography entry, an ordinary consequence of this provisional article layout rather than a scientific or submission-blocking issue.

The isolated LaTeX build uses the paper's section, appendix, bibliography, figure and generated table files. It does not need repository research notes or review records. Existing computational scripts have some explicitly documented repository dependencies; I did not misinterpret the standalone mathematical-build claim as a promise that those scripts already form a separately installed software package.

## Complete mathematical reading

### Section 1: model, semantics, encoding and attribution

The distinction between one jointly optimizing follower and independent Nash agents is stated. Fixed shared rows are separated from a growing number of local bounds. The optimistic follower set is not prefiltered by upper constraints; the pessimistic convention imposes universal upper feasibility and maximizes the adverse upper objective for a minimization problem. Infeasible followers are excluded. The switch to revenue maximization in the computational section is explained.

The numerical-degree parameter, explicit monomial input and fixed-total-variable requirements for real algebra are consistently stated. The common-field output is not confused with separate coordinate radicals or a field containing all unrelated adversaries. The substitution lemma correctly expands only in the fixed compressed dimension and clears a positive denominator.

The contributions paragraph and comparison table are adequately qualified. They identify the original combined theorem classes and output guarantees, while crediting multiplier arrangements, real algebra, conic support reduction, polynomial bilevel global comparison, inverse approximation, convex conjugation and the established transferred hardness results. I found no unsupported priority claim.

### Section 2: exact responses

I checked the local normal-cone necessity, conic reduction modulo equality normals, nonsingular KKT system and positive squared-determinant decoding. Local support sizes are bounded by block dimension, not by the total follower constraint rank. The realizable-sign enumeration avoids a Cartesian product of local choices. Multiplying local denominators raises numerical degree polynomially and does not introduce extra variables.

The global predicate compares actual feasible candidate values. A genuine global minimum is present, so comparison against all stationary candidates is sufficient even with a nonconvex aggregate. The upper polynomial relation, separate elimination and infimum predicate retain fixed total dimension. The fixed-normal closed-graph proof uses Hoffman repair into each nonempty nearby polyhedron correctly. Moving-rank enumeration has the necessary determinant guard, and the examples correctly separate optimistic and pessimistic nonattainment. The constant-matrix arithmetic refinement does not use a growing product of variable denominators. The supplied low-rank SPD specialization correctly uses KKT sufficiency even if the small coupling matrix is indefinite.

### Section 3: robustness and screening

The measurement-fiber threshold is sound without making a near-optimal point stationary for the nominal follower. A feasible fiber candidate meeting the true nominal budget suffices; globality remains necessary for the nominal value. Separate elimination per upper criterion is essential and is performed before conjunction. This justifies a fixed measurement count per criterion rather than a fixed rank of their union.

The convex robust-attainment proof handles a budget that vanishes, while the positive-budget nonconvex example actually shows failure of lower continuity of the admissible response set. The Max-Cut transfer distinguishes NP-hard worst-value computation from coNP-complete universal threshold feasibility.

I rederived the two variational inequalities, the completed-square ellipsoid and its coordinate/gradient centers. The strict gradient tests and the weak coordinate tests are sound. The relative-interior refinement has the required strict-somewhere conditions and extends by continuity. Recovery uses the true Hessian, permits zero-gradient bound coordinates and does not incorrectly prune assignments after a failed whole-cell guess. The `M 3^t` count explicitly excludes screening and cover construction. The transition-neighborhood proof uses a polynomial overlapping simplex cover, counts transition coordinates at all relevant vertices and does not infer low ambiguity merely from a small norm error. Signed inner/outer value bounds use the correct enclosure direction and the correct infeasibility implications.

### Section 4: accuracy bits

I checked all three approximation constructions and their error ledgers, including the signed single-resource identity, the resource repair bound, the frozen aggregate residual, and the general nonlinear-branch recovery. The latter rounds in the actual rational base polytope and compares true continuous inverse responses across branch boundaries; it never relies on an invalid old branch after rounding. The absolute complementarity residual control correctly retains large inactive slacks.

The explicitly encoded polynomial upper substitution has both inverse-branch and argument-degree factors. The true-to-surrogate and surrogate-to-recovered-response bounds are enough for the global leader and value guarantee. The empty-follower case is polynomial upper optimization, not incorrectly called an LP. The outer, inner, posterior sandwich and tightening conclusions are different and stated accurately. Convex reduced upper rows, strict anchor and uniform reserve headroom are additional promises. The isolated feasible optimum and irrational-only feasible leaders justify those qualifications.

### Section 5: boundaries

I followed both scalar dense reductions, including the conditional shortfall readout, the ternary witness margin, the near-identity relative-coordinate estimate and the small encoded upper gap. The multiplicative scaling argument preserves binary encoding and does not claim strong hardness. The cost-space scheme freezes saturated coordinates before choosing a maximum-volume row basis; its error and runtime depend on inverse normalized accuracy and conditioning, consistently with the exact hardness result. The rational projected-gradient recovery uses an adequate denominator bound and continued-fraction isolation.

I checked the growing-leader transfer and the independent mixed-radix rounding gap, the bounded-core candidate enumeration, both path-message constructions and their stated output-only limitation. The follower-path reduction needs the nonconvex upper row and retains it. The padding construction preserves original endpoint vertices, uses the required local coefficient alphabet, and does not claim bounded slab weights or rescaled linear costs. The arithmetic propositions correctly distinguish common-field output length and Square Root Sum comparison from NP-hardness. The one-power examples prove precisely the stated rational-output obstruction, without claiming the unsettled affine-upper/no-row subclass.

### Section 6: scalar algorithms and computations

I rederived the convex small system `I + S H` without using `H^{-1}`, the monotone aligned rank-one inversion including negative `h` under SPD, and the quadratic upper interval optimization.

For the nonconvex scalar model, I checked the unique strictly convex fiber allocation with signed and zero loadings and fixed boxes. Its nondegenerate piece count is at most `2N-1`. The endpoint, positive-curvature stationary and flat-piece candidates are complete. On open price cells, identical winning value polynomials have equal derivatives `gamma w`, and the unique fiber minimizer makes their original responses identical. At isolated prices, all original contacts and flat intervals must be retained. The argument for incremental insertion retaining final contacts also covers tangencies and isolated candidate domains.

Optimistic flat-component intersection and pessimistic universal endpoint tests use affine recovery on each fiber piece. The upper solver tracks open price boundaries, isolated admissible leaders, constant-revenue attainment and unattained suprema. Each selected output belongs to its own rational/quadratic field; the entire atlas need not share a quadratic field. Both contact examples and their exact numerical values check out.

The original-coordinate baseline's nonzero-principal-minor restriction is explicit, checked before use and adequate: a global minimizer's minimal free face has a PSD principal Hessian, which becomes PD under that restriction. The baseline compares original objective values and solves both continuous upper tasks independently. Its all-pair crossings are not the same as the older compressed all-pair implementation or the older fixed-price face oracle; the paper distinguishes all three.

The protocol separates fresh-process repetitions, solver time, preprocessing, wall time, profiling, historical data and repeated-type structure. The negative screening result is not hidden. The numerical zero-gap MILP discrepancy is reported accurately and not treated as a rational certificate.

### Section 7 and appendices A–D

The conclusion follows the actual theorem scopes and computational evidence, and makes no empirical claim about the unimplemented general elimination algorithms.

Appendix A has a complete support-membership proof and common-weight recovery from a polynomial list of support tuples. Feasible tuples selected at other core parameters may safely be retained, and the support argument supplies all necessary tuples at the selected parameter. It does not convexify a nonconvex reaction set.

Appendix B controls real parts of complex critical values, pads and merges bad target intervals, covers good gaps with rational analytic panels, establishes the full inverse branch over a critical-value-free disk, and proves polynomial rational Taylor coefficient and intermediate-bit bounds. The positive-coefficient refinement uses that assumption only where needed. I found no dependence on an unproved numerically stable inversion routine.

Appendix C gives explicit denominator-clearing, conic support, repair and multiplier bounds. The Bregman estimate is valid with signed marginal coefficients. For the sharp modulus I checked the common-active-row correction, gradient cancellation and division by the response distance. The semialgebraic component count controls disconnected repeated patterns along a leader segment; merely counting patterns would not have sufficed. The resulting constant can be numerically large but has polynomial encoding. The sharp exponent is attained by the one-dimensional power example.

Appendix D gives the sparse-shadow edge exposure and backward value recurrence, the unextended epigraph boundary-factor lower bound, telescoping/parabolic exposure, fixed-alphabet padding and exact equal-gain projection. Zero-gain rows are added at their original heads. Multiple bounds, reverse edge orientations, fixed total cycle rank and same-field witness recovery are handled. The projection's objective restriction and lack of automatic parameter compactness are stated.

## Independent executable checks

All new logs and scripts are in `verification/stage08-review04/`; original experiment records were not overwritten, and no timing campaign was run.

1. `check_independent.py` ran the existing 18 distinct complete-task cases against the independent original-coordinate solver, then **12 new cases** from seed `80904`, including signed/zero loadings, negative boxes, both tariff-coefficient signs, varying curvature and affine upper rows. All passed. Each comparison includes the full response set at every independently generated baseline cut and an interior point of each baseline cell, both upper values/attainment flags, and attained-witness checks.
2. The same script independently derived the singular two-coordinate model with `d=(1,1)`, `u=(1,-1)`, box `[-1,1]^2`, `h=1/2`. At price zero every aggregate in `[-2,2]` has response `(w/2,-w/2)` and zero follower cost. Upper equality `z_1=1/4` admits the attained optimistic pair `x=0,w=1/2,z=(1/4,-1/4)` and no universally feasible pessimistic leader. The compressed solver returns exactly that behavior with a one-shot iterator of the two upper rows. This exercises a continuum that the baseline deliberately rejects.
3. `check_screen_convex.py` compares exact screening against full status enumeration on three new dense rational families (seeds `809041`–`809043`). At cell endpoints and midpoints it checks the variational inequality and two independently chosen signed directional ellipsoid inequalities, and every certified coordinate status. All pass.
4. That script also compares the fused convex aligned sweep with exhaustive certified paths for negative, zero and positive rank-one coefficients, signed/zero loadings, gamma 2, an affine upper row and quadratic upper data. All exact objectives agree.
5. All three table inputs were regenerated in the isolated copy from the raw fresh records and historical screening JSON, with only the historical-data path adapted. Their bytes match the frozen table files exactly. There are 60 successful raw workers.
6. All **11 measured input hashes** in the raw result file match either the live file or its explicitly preserved measured version. The measured compressed source differs from the reviewed live source by exactly the documented `constraints = tuple(constraints)` line. The measured driver and test versions also match their recorded hashes. This independently confirms that the later correction was not silently relabeled as measured code.

## Primary-literature checks

I consulted actual primary sources, not other review reports:

- [Hladík, Černý and Rada, arXiv:1911.10877](https://arxiv.org/html/1911.10877v1), especially Section 2, Observations 1–2 and the following face-enumeration discussion. This directly supports the attribution of stationary-face enumeration and the distinction between fixed rank of the whole quadratic form and a full-rank diagonal-plus-low-rank model.
- Local original PDF of Gardiner–Lucet (2010), pages 470–471 and 478, including Propositions 3.1 and 4.3 and their arguments. The stated quadratic-time and linear-time envelope constructions are correctly credited. The publisher DOI request failed in this session; the authoritative local original was accessible.
- Local original PDF of Moehle et al. (2023), Section 6.3 and Appendix B. The paper cites its constructive envelope account without relying on the external tangent formulas for its own correctness.
- Local original PDF of Gritzmann–Sturmfels (1993), Algorithm 2.3.6, Theorem 2.3.7 and Corollary 2.3.10. The shared support-direction arrangement and binary polynomial-time antecedent are accurately described; parameter-uniform core elimination and common-field recovery are separately proved here.
- [Liu et al., PMLR 2014 primary proceedings page](https://proceedings.mlr.press/v32/liuc14.html) confirms the stated variational-inequality screening lineage. I did not infer a bilevel recovery theorem from that source.
- [Wu et al., arXiv:2603.00027v1, Lemma 4.2](https://arxiv.org/html/2603.00027v1) explicitly supplies the unconstrained uniform-convexity response exponent `1/(p-1)`. The manuscript correctly credits this and narrows its own claim to moving affine resources and an effective polynomial-encoding constant.

Additional online searches on fixed shared constraints with many separable quadratic followers, and on accuracy-bit optimization for strictly convex polynomial followers, found related work already discussed or classes with materially different assumptions. These bounded searches do not prove absence of all earlier work. The manuscript's “To the best of our knowledge” claim concerns the combined theorem classes and outputs and is appropriately qualified on this evidence.

## Remaining issues and limits

Major issues: **none identified**.

Minor issues requiring correction: **none identified**.

The general quantifier-elimination algorithms have mathematical proofs rather than executable implementations. The manuscript says so. The computational diagnostics are finite checks, not formal verification; the comparison baseline deliberately excludes singular principal minors; the general approximation theorem does not decide exact response-dependent upper feasibility without additional conditions. These are correctly stated scopes, not unresolved gaps.
