# Independent final whole-paper review 11

**Verdict: PASS.** No major or minor findings. No repair is required for this frozen version.

Reviewed target: `process/snapshots/whole-round01`, including the 111-page `main.pdf`, SHA256 `912de166731f56368a8ee4db21294aa348b85364e85cd444e31265b29828d084`. This is an independent final gate, with additional emphasis on FBBT complexity and iteration proofs. Earlier PASS labels were not used as evidence of correctness. I did not read other reports from this final round, delegate, or edit manuscript or snapshot files.

## Coverage

I read the frozen review protocol, whole-paper review assignment, reviewer-focus record, scope proposal, claim-coverage ledger, Stage 6 author record, and Stage 6 correction log. I read `main.tex`, `macros.tex`, the complete bibliography (`references.bib`, 41 entries), and every section and appendix, including every displayed proof and both complete printed certificate programs:

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
- `sections/appendix-positive-couplings.tex`
- `sections/appendix-cubic-certificates.tex`
- `sections/appendix-finite-signings.tex`
- `sections/appendix-structural-auxiliary.tex`
- `sections/appendix-positive-box-predecessors.tex`
- `sections/appendix-scaling.tex`
- `sections/appendix-point-packing.tex`
- `sections/appendix-p-split.tex`
- `sections/appendix-fbbt.tex`
- `sections/appendix-rank-one.tex`
- `sections/appendix-integer-comparison.tex`

The coverage ledger's distinctions are preserved in the manuscript: pointwise scalar widths, exact envelope computation, local polynomial relaxation strength, spatial certificate size, and global extension size are different resources. The later coordinatewise graph and order-one monomial refinements are present, with their objective and degree hypotheses. Earlier weaker bounds, auxiliary structural results, finite certificates, counterexamples, and open cases are not silently promoted into stronger universal conclusions.

I read `literature/AGENTS.md` before consulting local originals. The principal source checks were against original PDFs or direct text extracted from them, with the following locators. These are targeted dependency checks, not claims to have read all these external works in full.

| Source | Passage checked and purpose |
| --- | --- |
| Belotti et al., *On feasibility based bounds tightening* | PDF pp. 13–15, especially Theorem 4.1 and the following infeasibility discussion; verified the nonempty-limiting-box qualification. Original PDF p. 14 also inspected visually. Publication metadata cross-checked at the [Optimization Online record](https://optimization-online.org/2012/01/3325/). |
| Etessami–Yannakakis | Theorem 5.2, original PDF pp. 26–28; checked circuit splitting, normalization, detector, and amplification against the manuscript's explicit attribution. PDF p. 27 inspected visually. |
| Stewart et al. | Section 4.1, equation (18), original PDF pp. 21–22; checked the chain underlying the stated inference about ordinary Kleene iteration. PDF p. 21 inspected visually. |
| Esparza et al. | The long source's Section 7, Theorem 7.1 and equation (14), PDF pp. 34–35, including the displayed proof; distinguished its Newton statement from the manuscript's Kleene inference. |
| Schoenebeck | Theorems 11–12, Lemma 13 and the signed-character construction, original full-paper PDF pp. 6–11; also consulted the appendix expansion argument. Checked the parameter substitution and signed Gram mechanism. |
| Cornuéjols | Theorem 6.5 (Camion) and Theorem 6.13 (balanced mixed packing/covering); checked the actual hypotheses rather than conflating balancedness with total unimodularity. |
| Hassin–Tamir | Theorem 3.1 and surrounding terminal/series-parallel definitions, visually in original PDF p. 3, printed p. 381. The scanned PDF's empty text extraction was not treated as evidence. |
| Lee–Raghavendra–Steurer | Theorem 3.8/equation (3.11), PDF p. 23, and the pseudo-density construction and consequences in Theorem 5.3/Corollary 5.4, PDF pp. 32–34; checked the quantitative substitution in the approximate PSD bound. |
| Braun et al. | Hard pair and Theorem 6(i), original PDF p. 18; checked the fixed-dilation LP input. |
| Fawzi–Parrilo | Theorem 1, original PDF p. 3; checked the fixed-block conic resource and constants. |
| Kronqvist et al. | Original PDF pp. 4–7 and 15–16: retained compact domain, assumptions, minimal-sharing remark, Definition 4, Theorem 6 and its proof. The retained-box counterexample addresses the stated theorem's scope. |
| Davidson–Donsig | Theorems 1.2 and 2.4 and the distinction between weighted and pattern Schur multipliers; checked the real norm comparison used in the paper. |
| Luedtke et al. | Original PDF p. 22, Conjecture 1; checked the nonnegative-box/positive-coefficient antecedent. |
| Sherali | Original PDF pp. 8–9, printed pp. 252–253, equation (13) and Theorem 3; checked the monomial-envelope formula and its attribution. |
| Lubin et al. | Original PDF p. 12, midpoint lemma and proof; checked the parity mechanism in the integer comparison. |
| Boland et al. | Original PDF pp. 4–6, Lemma 1, its full primal/dual proof and Corollary 1; also the cycle characterization proof in the local source text at pp. 10–11. Checked the cut-width normalization and sign conditions. |

The frozen author-validation record was used to locate sources, not as independent validation of their claims.

## Findings

None. I found no demonstrable error in a theorem, proof, constant, necessary hypothesis, central attribution, or required scope item, and no local editorial defect warranting a MINOR finding.

## Independent verification

### FBBT: limiting bounds, encoding, and every-schedule iteration

I reconstructed the three arguments in `appendix-fbbt.tex` separately.

For Lemma `lem:fbbt-fixed-point`, the assumed cube fixed point bounds the monotone Kleene sequence from zero. Continuity gives its least nonnegative fixed point. Sound contractions cannot discard that point. Once the lower vector dominates one synchronous Kleene iterate, fairness ensures that all finitely many defining coordinates receive forward propagation at some finite later time. Thus the next synchronous iterate is eventually dominated. This uses no bounded-delay assumption and gives convergence of the lower vector, not an algorithmic running time. The same reasoning applies to the augmented nonnegative expression graph.

For Proposition `prop:fbbt-hardness`, I checked that the positive/negative circuit split, alternating layers and paired complements implement the intended normalized circuit in polynomial size. The multiplication complement is `r = r_j + p_j r_k`, so subtraction is not smuggled into the defining equations. Copy variables remove repeated names in products. The detector has four vertices in its directed strongly connected component; the final amplifier has two. Its least root is one for `U <= V`, and `(1-c)/c` otherwise, including the endpoint cases `c = 0, 1/2, 1`. For positive integer difference, `1-a_* >= 1/M`. The repeatedly squared small number is encoded by equations, not by writing its enormous rational denominator in binary. Consequently the two output ranges `[0,1/8]` and `{1}` are separated under additive error `1/4`. Every feasible root is rational and determines the remaining coordinates, so the asserted two-point bound is valid. The optional inequality `ca <= 1/2` retains the least root and removes only the unwanted root. PosSLP-hardness is not represented as NP-hardness.

For Proposition `prop:fbbt-iterations`, I checked the comparison with exact upstream initialization using monotonicity of interval-hull contractors. With `c = 1-b`, the invariant `0 <= l_w <= c l_z <= c` makes the inverse product update ineffective on `l_z`. One affine hull update can raise `l_z` only to `max(l_z,b+l_w) <= b+c l_z`; its simultaneous update of `l_w` preserves the invariant. The feasible solution forces the upper endpoints to stay at `u_z=1` and `u_w` in `{1,c}`, so upper-bound propagation supplies no faster lower update. After `K` affine applications, `l_z <= 1-c^K <= Kb`, yielding `K >= 2^(2^n-1)` to reach one half. This bound does not rely on inserting idle steps into a schedule. It holds for every finite ordering of the specified primitives; fairness supplies eventual convergence. Global contractors and equation aggregation are explicitly outside this claim. The statement also correctly distinguishes parameter `n` from ordinary input length `O(n log n)`.

Finally, I derived the claimed Kleene consequence of the Stewart chain: monotonicity gives `e_i(k)^2 >= e_{i-1}(k)`; the bottom recurrence gives `e_0(k) >= 1/(k+1)`; hence `e_n(k) >= (k+1)^(-1/2^n)`. The manuscript credits this as an inference from the source's displayed system, not a source theorem about Kleene iteration.

The independent standard-library checker `verification/reviewer11/whole-round01/check_independent.py` uses exact rational arithmetic. Its saved result is `independent-results.json`. It verified:

- 3,016 reachable primitive-contractor transitions, enumerating both contractor choices through 13 steps for each `n=1,...,4`, with the stated invariant and `1-c^K <= Kb` bound.
- 12,528 rational detector cases with `M=1,...,32` and `U,V` ranging from zero through `M`, including all detector endpoint cases and the optional root-selection inequality. For this separate algebraic check, `b=1/(16M^2)` supplies the needed smallness; this is not presented as the circuit construction.
- Four Stewart chain lengths and nine synchronous exact iterates for each, checking the error inequalities.

These finite checks try to expose errors; the general proofs are the analytic arguments above.

### Other proof families

I reconstructed the vertex-law interpretation and the distinction between the factorwise lift and scalar graph hull, including zero-width conventions. The positive coupling arguments maintain marginal laws; the harmonic cutoff, inactive mass bound, and Lambert parameter constraints have the stated ranges. The dyadic argument uses nested partitions, and the radix argument is a different regime. The equal-mean cubic upper bound's cases and finite scalar dual inequalities have the right factors.

For the structural results, I checked ownership of incoming variables, the distinction between summed and termwise degree estimates, the series/parallel terminal invariant, the separate uses of balancedness and Camion's criterion, and the rank calculation in the frequency-two slab argument. The positive-box proof restricts the fixed ambient balanced law when deleting coordinates; it does not assume unrestricted Schur concavity. The unequal-aspect obstruction and the larger open interval for its supremum remain correctly distinguished.

For envelope complexity, the narrow-box PARTITION reduction has rational input and an exact threshold; it is not a claim of hardness at fixed absolute tolerance. The finite-type algorithm is scoped to a fixed number of aspect-ratio types. The precision assumptions for the transport consequence are explicit.

For the cardinality lower bounds, I checked positivity, equality identities, repeated slack products and degree accounting. Tensor products support global squares, not merely separate block squares. Coordinatewise graph transfer uses affine interpolation on the two retained endpoints; it does not identify the original nonlinear function with that affine map on its entire domain. The lifted objective must agree on the full graph at the stated available degree.

For XOR and monomial lifts, substitutions are deterministic rather than pseudoexpectation conditioning. The signed moment construction, full-box quadratic moment realization, degree factors `4r` and `4rD`, bounded occurrence deletion, parity-rank count, and constants in the exponential bounds are consistent. The order-one quadratic formulation uses identities in expectation at the permitted degree; it does not assume unsupported samplewise graph equations. The affine-branching section states an obstruction to this proof method, not a general tree upper bound.

In the supporting appendices I checked the scale disaggregation, zero slices, extensive-only perspective and rectangularity hypotheses; the point-packing covariance; the retained-box P-split counterexample and directional repair; and the rank-one face and stability estimates. Exact lift bounds, approximate lift bounds and fixed-block conic bounds retain their distinct resources. The LRS substitution yields the stated logarithmic loss in the approximate exponent. The integer comparison retains the midpoint/parity limitations.

### Exact certificates and PDF checks

I extracted and executed both complete printed appendix programs in my own verification directory. The signing program returned `[1,2,4,4,5,8]`. The cubic program verified the exact finite primal/dual certificates, including ratios `20891/10411`, `6601/3225`, `7443345/3445256`, `27/16`, `21/11`, and `99/50`, and its `m=16` two-level checks. Both passed. Code hashes and complete standard output are saved in `independent-results.json`. These programs verify their specified finite instances, not the universal cubic or signing claims.

I copied the frozen TeX inputs into `verification/reviewer11/whole-round01/build/` and ran `latexmk -pdf -interaction=nonstopmode -halt-on-error main.tex` with that directory as the explicit working directory. The build completed successfully at 111 pages, without undefined-reference or overfull-box warnings. Three underfull-box messages are harmless in the inspected output. The full extracted text of the independent PDF is byte-for-byte identical to the frozen PDF's full extracted text; this is a text-equivalence check, not a claim of identical PDF bytes.

I visually inspected frozen PDF pages 1, 4, 30, 55, 85–87, and 104–111, including the FBBT material and bibliography. The selected pages are readable without clipping or layout defects. The rendered page images and contact sheets are in the assigned verification directory. Visual inspection of four source pages is identified in the source table above.

## Remaining limits

This is a mathematical referee review, not a formal proof-assistant verification. Every manuscript proof was read and assessed, but only the specifically listed finite programs and rational checks were executed. There were no floating-point optimization experiments in this review. The universal claims rest on their analytic proofs and cited external theorems, not on the finite samples.

I checked the principal source statements and the passages listed above; I did not independently reprove every classical external result or audit all 41 references in full. In particular, external rank lower-bound theorems, the random expansion theorem behind the XOR input, and classical integrality, norm, optimization/separation and SOS results remain external dependencies. Source passages not listed in the table were not freshly verified in their entirety. No central source needed for the additional FBBT focus was inaccessible.

All 111 pages were covered through the complete TeX and extracted PDF text, but visual page inspection was selective rather than page-by-page. Full text equality with the fresh build does not establish equality of every graphic or layout detail.

The open extremal and structural questions explicitly retained in the synthesis and coverage record remain open. Their presence does not undermine the scoped results proved here.
