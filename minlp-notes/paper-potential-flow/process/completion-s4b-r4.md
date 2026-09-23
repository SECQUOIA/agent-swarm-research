# Independent S4b review 4

Verdict: no major issue found. I found one minor gap in the proof of threshold elimination, concerning a constant dual function with no actual breakpoints. The result is correct and the repair is local. Subject to that repair, the section supports its stated mathematical and output guarantees, including the new independent directional-coefficient model.

The review covers the complete frozen `complexity/sections/07-weighted-cactus.tex`, not only the assigned original-parameter focus. I read the supplied review instructions and applicable literature instructions. I did not read S4b author, lead, build/check, adjudication, or peer reports. Old status assertions in the explicitly permitted source notes were not used as proof or priority evidence. I changed only this report and ran no manuscript build.

The section SHA-256 matched the supplied value before and after the audit:

`8b5645a80c0922cda4e57a1948670172268fa0cd4dc9fdc9c6505ec258a10219`

## Required correction

### R4.1 — Minor: the dual can have no breakpoint

Location: `complexity/sections/07-weighted-cactus.tex`, lines 517–525, proof of `lem:a-wcac-threshold`.

The assertion that a minimum exists at a breakpoint needs a constant-function case. Feasibility prevents an affine tail from decreasing without bound, but does not ensure that the dual has any actual breakpoint. Singleton coefficient intervals are allowed, and the separate all-zero-flow case does not cover all constant duals.

For example, take a two-edge cycle with `f=(1,-1)`, `w=(0,1)`, and `L=U=(1,1)`. The conservation equality holds and the primal objective is `-1`. Nevertheless,

```
D(lambda) = (-lambda)*1 + (1-lambda)*(-1) = -1
```

for every `lambda`. There is no actual breakpoint, despite nonzero flows. Either listed edge weight still supplies a valid threshold, so this is a proof gap in a degenerate case, not a counterexample to the lemma or subsequent theorems.

Concrete repair: state that `D` is affine between consecutive distinct **listed edge weights**, and use those weights as partition boundaries whether or not the slope changes. A minimum can be moved to one of those weights: nonconstant affine pieces attain their minimum at a finite boundary, a flat piece can use a boundary, and a globally constant function can use any listed weight. Alternatively add the globally constant case explicitly before the actual-breakpoint argument. Retain the all-zero-flow case, which also makes recovery immediate.

I found no other required mathematical or scope correction. The following records the substantive checks behind that verdict.

## Structural face theorem

Lines 67–233 establish a structural statement at fixed maximum block rank and fixed objective support. They do not assert that the higher-rank local objectives can already be optimized with the cactus algorithm.

- Objective-free pruning is valid for an attached physical subnetwork. Aggregating its intervals at the attachment preserves every attainable exterior nomination, and the stated greedy filling gives a rational disaggregation of polynomial bit length. Lines 126–128 correctly retain entire physical blocks: a nonsupport incidence-tree leaf inside a retained block is not deleted as a physical vertex.
- The zero-induced-objective contraction is necessary and justified. Deleting a block's edges partitions the graph into one rooted component per block vertex. When each component's total objective coefficient is zero, translating its potentials does not change its objective. A reduced nomination can be split among the old roots, the remaining balanced effective block injection can be solved, and the exterior components can be translated back. This permits arbitrary allowed coefficients in the removed block and preserves objective values without requiring its state coordinates to be rational.
- A contraction cannot identify two distinct vertices of another surviving block: that would contradict the incidence-tree property. It therefore preserves surviving block ranks. Summing objective coefficients does not increase support, and the surviving induced coefficient sums remain the same sums of original coefficients. Repetition terminates and does not introduce resistance dependence.
- A tree with at most `p` support leaves has `O(p)` branching incidence nodes and total branching degree. Marking support and branching vertex nodes, then including branching blocks and adjacent blocks, yields `O(p)` special blocks and `O(p)` ordinary chains. The ordinary-chain adjoint current is a fixed objective sum. Zero current would make every induced source of that block zero, contradicting completion of the contraction step.
- Positive smoothing makes the grounded derivative Laplacian invertible. The strict two-terminal maximum principle applies to nonbridge biconnected blocks, including the parallel-edge rank-one case. Consequently chain port levels are strictly ordered and open internal ranges are disjoint. The balanced-box normal-cone condition gives the scalar multiplier even on lower-dimensional or singleton boxes. Leaving shared selected/special endpoints free resolves articulation-level equality without inconsistent endpoint assignments.
- Only `O(p)` blocks remain free on each coarse face. In a nonbridge block, `sum(deg-2)=2r_B-2` bounds degree-at-least-three vertices; retained port incidences total `O(p)`. Suppression leaves `r_B+k_B-1` paths, for `O(rp)` paths and marked coordinates overall. Bridges are handled separately.
- The second perturbation is applied only after fixing a coarse face. Interior adjoint sources are exactly positive `delta`, giving `j_i-j_(i-1)=delta`. Edge drops then make the path potential sequence increase and decrease, with at most a two-vertex plateau. A horizontal level meets at most two interior vertices, so the lower/free/upper/free/lower pattern has the claimed count. Empty runs and shared marked coordinates cause no additional free coordinates.
- The two limiting arguments use bounded flows, bounded normalized potentials, energy-minimizer continuity, and a finite family of closed faces. The first limit identifies a coarse face containing an original optimum before any positive interior source is added. The second recovers an optimum on that face. This order avoids corrupting the zero-source chain argument.
- Rational balance elimination and interval disaggregation preserve polynomial encoding. For a joint optimum, freeze its coefficients and apply the same coefficient-independent family. This is valid for the stated independent compact positive coefficient sets as a structural assertion. The full-box corollary uses only interval models already handled by the cactus optimizer.

The explicit unfiltered-domain qualification at lines 124, 711, and 833–837 is essential and correct. This proof is not a capacity-preserving contraction theorem.

## Local formulas, square-root panels, and the common partition

Lines 237–444 correctly reduce a fixed-law cactus objective to independent scalar cycle equations and affine bridge flows. With the tail-positive incidence convention, `Aw=c` gives `c^T pi=sum w_e g_e(x_e)`. Reorientation reverses offsets and weights and swaps asymmetric coefficients and intervals. Edge-disjoint cycle equations ensure global potential compatibility, including cycles joined at articulation vertices.

On a sign cell, the coefficient of `q^2` is constant, the coefficient of `q` is affine, and the constant term is quadratic. At a physical root, `2A_2q+B_1` is the nonnegative sum of differential resistances. Thus the plus-radical selector remains correct for negative `A_2`. The linear branch retains `B_1>0`; no artificial lower bound on that denominator is introduced. On the remaining physical stratum, derivative zero forces every flow to vanish. The affine all-zero chart covers it. Sign-cell closures are harmless because both directional laws vanish at zero.

Bounded-dimensional projection gives exact rational chart eligibility, including lower-dimensional and disconnected domains. In the rational charts the objective can be kept exact even near a vanishing denominator, since the denominator's nonzero condition is retained and the physical objective remains uniformly bounded.

I checked the square-root construction directly. The center `(9/16)4^-j` has the rational square root `(3/4)2^-j`; on its panel the series variable lies between `-5/9` and `7/9`. The displayed geometric-tail bound is valid, and the zero panel has error at most `2^-J`. Rescaling with tolerance `eta/S` gives the stated absolute error on `[0,S^2]`. The panel count, degree, and expanded coefficient lengths are polynomial in the relevant bit lengths; the product `jK` in coefficients is polynomial as claimed. No exponentially fine uniform grid is being used.

The common partition is built from all local eligibility and panel polynomials in fixed nomination dimension. It avoids selecting a Cartesian product of cycle charts. Multiplying polynomially many bounded-degree rational denominators gives polynomial degree and coefficient length; dense expansion remains polynomial because the variable dimension is fixed. Squared-denominator threshold tests keep the nonzero restrictions.

Open parts are treated with existential strict-threshold tests and suprema. The lower sample threshold ensures existence even when a supremum is unattained. With `a=epsilon/16` and `U-L<=epsilon/8`, `[L-a,U+a]` has width at most `epsilon/4`. A sample above `L-epsilon/16` has physical loss at most

```
(U-L) + epsilon/16 + 2a <= 5 epsilon/16.
```

This budget leaves room for the stated `epsilon/4` rounding loss.

## Nomination and coefficient continuity; original-parameter recovery

The nomination lemma at lines 408–431 is an all-graph result, not a consequence of cycle decomposition. For two states under the same law, each nonzero flow difference has the sign of the corresponding potential-difference drop. Orienting those differences positively gives an acyclic support. Its path decomposition has total weight `||b-b'||_1/2`, which bounds every edge difference. On `[-B_0,B_0]`, each asymmetric law is Lipschitz with constant `2 beta_U B_0`, including across zero. Path integration then gives exactly the displayed `K_b`.

Rational LP recovery at lines 433–440 is valid even if `P` is lower-dimensional. The isolating box contains the algebraic sample, so its intersection with rational `P` is a nonempty rational polytope. The returned rational point remains in the original parameter domain. It need not remain in any selected chart, panel, or denominator stratum because the error estimate compares physical solutions globally.

The new coefficient sensitivity proof at lines 641–686 is sound on every connected graph. In particular:

- The smoothing term is `rho x` with `rho` independent of coefficients. Its parameter derivative therefore contributes no unwanted term to the new directional formula.
- After grounding, the positive derivative resistance matrix gives a differentiable state map. The directional law is jointly continuously differentiable at zero: the flow derivatives from both sides vanish before smoothing, and both coefficient derivatives are zero there.
- The electrical unit adjoint current has an acyclic support and one unit of source-to-sink flow. Hence `|j_e|<=1` on any connected graph, with no cactus assumption.
- At fixed nominations, differentiating `A^T pi=g_theta(x)+rho x` and pairing with that adjoint yields the displayed **positive** pairing with the coefficient forcing term. In the directional model this forcing is `(x_e)_+^2 d beta_e^+ -(x_e)_-^2 d beta_e^-`. Each coordinate derivative has magnitude at most `B_0^2`.
- Integrating along the original coefficient-box segment is allowed. The total-positive-nomination flow bound also holds for the smoothed laws, uniformly in coefficients. Strict-convexity continuity then permits the limit as `rho` decreases to zero, including coefficient-induced sign crossings.
- Normalizing one potential and summing against `|c_v|` gives the coefficient term `||c||_1 B_0^2 ||theta-theta'||_1`. Combining it with the uniform nomination estimate gives the joint bound. No inverse derivative or nonzero-flow hypothesis is hidden here.

Original-coordinate rounding at lines 688–698 respects the distinct models. The directional model rounds up to `2m` original coordinates in their own intervals. The symmetric model rounds one shared coordinate per edge, so its required equality across directions is preserved. Inactive coefficients can be selected rationally during recovery; if a later flow changes sign, the global continuity estimate still compares the two valid original-law scenarios. Singleton intervals are retained exactly. The widths have polynomial bit length because all constants are rational of polynomial bit length.

## Coefficient elimination and local candidate completeness

Lines 461–639 correctly reduce both interval models to the same active-coefficient problem on a sign cell. An inactive directional coefficient does not appear; at zero flow neither coefficient appears. Shared symmetric uncertainty is explicitly treated as a diagonal constraint, not replaced by two independent intervals.

For each listed threshold, the reduced-cost endpoint choices and tied aggregate interval give a feasible optimal LP profile exactly when `S+l_T<=0<=S+u_T`. The value formula subtracts `lambda` times the conservation equality and has the correct sign. Ties require only two aggregate inequalities, not enumeration of all tied endpoint assignments. The only correction needed in the converse is R4.1 above.

The circulation candidate list is complete. After specializing `z`, the feasible set is compact because of the artificial circulation bounds. Every boundary has an active constraint nonconstant in `q`; otherwise it would have a feasible neighborhood. Both roots of a nonzero quadratic coefficient are included, with selectors valid for either sign of that coefficient. A vanishing linear coefficient is not divided by; the remaining constraints decide whether its specialization excludes the parameter or is irrelevant to the boundary. Nonflat stationary points and flat-objective strata cover interior maximizers. Arc bounds add only affine constraints and do not change these degree claims.

Surrogate comparisons are performed within each cycle before summation. Pairwise comparison numerators and denominator signs belong to the common partition. The maximum of approximate candidates differs from the true maximum by at most the local uniform error. The actual selected candidate also lies within that error of its own surrogate. Thus the `5 epsilon/16` sampled-scenario bound includes approximate candidate selection without requiring a new radical-sum comparison or an omitted extra error charge.

The tied-coordinate fill starts at the minimum contribution of each interval, raises contributions until the desired aggregate is met, and divides only by nonzero `f_e`. It recovers original coefficients, with at most one tied active coefficient interior. The algebraic sample `z_*` has a common polynomial-size representation; each cycle adds only its own local extension. Subsequent local arithmetic and isolation have polynomial degree and size. A global primitive element containing every cycle root is unnecessary. Sharing the same `z_*` ensures that independently represented local outputs assemble to a physical scenario.

## Exact filters, irrational feasibility, and slack recovery

Lines 731–815 keep three different conclusions separate:

1. Fixed-dimensional affine nomination models with rational arc bounds admit exact feasibility decisions and exactly feasible algebraic approximate optimizers, in both coefficient models.
2. Fixed laws additionally admit a polynomial-size list of bounded-degree local polynomial filters defining a closed set. Substituting cycle flows leaves only `(z,q)`, so long cycles do not raise the local variable dimension. This broader filter class is not claimed for joint coefficient optimization, where new higher-degree boundaries would require a different candidate analysis.
3. A supplied nonempty tightening gives rational output feasible for the original arc bounds, with the objective guarantee measured against the tightened optimum only.

The algebraic output proof imposes all local restrictions before projection and samples surviving parts exactly. It does not apply rational LP rounding to a possibly irrational-only feasible set. Closed filters and compact original boxes give attained physical extrema even though individual partition parts may be open.

The four-cycle irrational witness at lines 817–831 checks out under the manuscript's incidence convention. Successive differences of `x=(q+t-1,q-2,q,q-2)` give `b=(t+1,-t-1,2,-2)`. The two unit capacities force `q=1`; the cycle equation is `t^2-2=0`; and `t` in `[1,2]` leaves only `sqrt(2)`. The other two capacities hold. Rational nominations themselves, not just the state, are impossible on that filtered family.

For resistance rounding, the edge-endpoint potential estimate gives a drop change bounded by `B_0^2 k delta`. The fixed-law inverse estimate

```
|g(u)-g(v)| >= beta_L |u-v|^2 / 2
```

is valid at equal signs and opposite signs. Evaluating the two laws at the same `y_e` changes the drop by at most `B_0^2 delta`, because only one directional coefficient is active there. Combining these estimates proves the displayed squared flow bound with `2B_0^2(k+1)/beta_L`; it remains valid when `x_e` and `y_e` have opposite signs.

The final flow error is bounded by `H_1 h/2 + B_0 sqrt(2(k+1)delta/beta_L)`. The supplied choices make each term at most `sigma/4`, leaving total error at most `sigma/2`. Simultaneously imposing the objective rounding budget is possible with polynomial-bit widths, including polynomial dependence on the encoding of `sigma` and the smallest coefficient endpoint. The text correctly disclaims any comparison between tightened and original optima and any preservation of arbitrary polynomial filters by this rounding.

## Exact profiles and implementation scope

Lines 841–901 establish exact rational optimizing coefficients at fixed rational nominations without claiming rational flows or a single rational objective value. Rational sign/capacity boundaries and quadratic stationary points give rational `q` and rational tied recovery. An irrational boundary can arise only from a tied-aggregate quadratic. At an extreme aggregate, every nonzero tied contribution must use its corresponding endpoint, so the original coefficients are rational even though the resulting circulation is irrational. Inactive directional coefficients can be chosen rationally. Flat objectives can use a boundary of their nonempty compact feasible circulation set and therefore reduce to the same two cases.

Pairwise local quadratic-value comparison is correct. For opposite nonzero signs of `U` and `V`, `sign(U+V)=sign(U) sign(U^2-V^2)`, and the squared difference has only one radical. Zero cases must be handled first, as stated. Independent local winners yield an exact global optimum without comparing any growing sum of radicals. The separate sum output and subsequent interval enclosure are consistent with the preliminary output conventions.

The interior-resistance example at lines 903–926 is correct. `Aw=c` for the displayed edge weights. Every physical circulation lies strictly in `(-3,0)`. Threshold `lambda=-1` produces strictly negative untied reduced costs and the upper bound `-6(q+1)^2-12`. Equality forces `q=-1`, the first, third, and fourth coefficients equal to one, and the second coefficient equal to two. This is a unique symmetric-model optimum and defeats endpoint-only profile enumeration.

I inspected `code/potential_flow_mpd/exact_weighted_cactus.py`, including `Quadratic.compare`, `solve_cycle`, witness reconstruction, and `solve_cactus`. Its supplied-block interface, symmetric coefficient arrays, optional local capacities, exact rational recovery, and separate local radical output match lines 929–948. It neither derives nor verifies graph-to-block mapping and does not implement the varying-nomination semialgebraic optimizer or independent directional intervals. The new directional script is a mechanism harness that calls the symmetric solver on sign-restricted subproblems; it does not silently expand the public solver's scope.

## Dependencies and source audit

I checked the relevant earlier-section contracts in `complexity/sections/01-preliminaries.tex`: tail-positive incidence, asymmetric reorientation, existence and uniqueness, block incidence/decomposition, cycle equation, compact-domain continuity, the fixed-dimensional quantifier-elimination and sample-point contracts, and exact versus additive output encodings. I also read the adjoint and physical path-decomposition passages in `complexity/sections/02-cactus.tex` and the symmetric all-graph resistance estimate in `complexity/sections/03-block-rank.tex`. The new section supplies its own directional derivative argument; it does not obtain that strengthening merely by citing the symmetric lemma.

I consulted the explicitly permitted source investigations/results:

- `results/potential-flow-weighted-cactus-accuracy-bits.md`;
- `results/potential-flow-joint-weighted-cactus-accuracy-bits.md`;
- `notes/potential-flow-reopened-weighted-face-reduction.md`;
- `notes/potential-flow-reopened-weighted-investigation.md`;
- `notes/potential-flow-exact-weighted-cactus-solver.md`.

I inspected the four bibliography entries directly used for the section's literature positioning in `complexity/references.bib`, the local source metadata, and the following primary-source passages. Here `p.N` follows the local `fulltext.md` page marker; printed manuscript page numbers are separately identified when they differ.

- `literature/papers/schultz2016-on-the-quantification-of-nomination/`: [[schultz2016-on-the-quantification-of-nomination]] p.20-22, especially Theorem 6 and equation (44), establish the affine-ray piecewise quadratic-radical/rational formulas. Theorem 6 is on printed p.18, matching the section's locator. [[schultz2016-on-the-quantification-of-nomination]] p.26, printed p.24, explicitly discusses node-disjoint cycles and attached trees. I checked Theorem 6 and the final extension passage against text extracted directly from `original.pdf`, because the stored Markdown omits some displayed formulas. This supports the stated predecessor credit, not the complete new weighted cactus theorem.
- `literature/papers/vigneron2014-geometric-optimization-and-sums-of/`: [[vigneron2014-geometric-optimization-and-sums-of]] p.7-10, Section 2.3, Theorem 6, and Section 3.2. Section 2.3 explicitly permits a bit model and adds polynomial dependence on input bit length, problem size, and `1/epsilon`. Theorem 6 uses a common arrangement; Section 3.2 replaces exact algebraic-sum selection with approximate summation. I checked these passages against `original.pdf` using `pdftotext`. The manuscript correctly distinguishes this `1/epsilon` dependence from an accuracy-bit bound; it does not misdescribe Vigneron as exclusively real-RAM or claim approximate summation as a new principle.
- `literature/papers/amann2018-deciding-robust-feasibility-and-infeasibility/`: [[amann2018-deciding-robust-feasibility-and-infeasibility]] p.16-17, Section 4.2 and Corollary 4.5, support the exact tree LP reduction. [[amann2018-deciding-robust-feasibility-and-infeasibility]] p.20-21, Section 4.3.3 and Lemma 4.10, give the coefficient conditions for a single-cycle circulation interval and explain their linear/polyhedral character. I checked the original PDF's Lemma 4.10 and subsequent explanation directly. These are correctly presented as related reductions, not as the present weighted multi-cycle theorem.
- `literature/papers/henrion2017-a-joint-model-of-probabilistic/`: [[henrion2017-a-joint-model-of-probabilistic]] p.6-10, Sections 2–3. Section 2 specifies a tree with a single entry, stochastic loads, and nonstochastic roughness uncertainty. Section 3.2, Lemmas 2–3, gives ellipsoidal and rectangular inner optimizations; I checked their formulas in `original.pdf` on PDF pp.9–10, printed pp.7–8. The current section appropriately separates that probabilistic/robust uncertainty model from deterministic weighted optimization.

All four cited sources had accessible full text in the local collection. I inspected the relevant passages, not every page of every paper. I did not perform a new exhaustive literature search or independently authenticate all publisher metadata. The section's narrow combination claim and explicit refusal to claim exhaustive priority are justified by this evidence. No novelty should be inferred for LP duality, elementary approximation, sign decomposition, root isolation, or fixed-dimensional real-algebraic computation.

## Executed validation and limits

I ran:

```
PYTHONDONTWRITEBYTECODE=1 python paper-potential-flow/verification/check_a7_weighted_asymmetric.py
```

It passed and reported 120 original `2m`-coordinate LP cases, including 29 feasible cases; 32 exact directional cycle cases; 32 interval-swap reorientations; 1,280 independently solved physical profiles; 1,280 coefficient-sensitivity cases; and an explicit coefficient-induced sign crossing. I read the harness before running it. Its original-box LP enumeration is distinct from its active-threshold calculation. The exact directional optimum path reuses the symmetric solver on sign-restricted panels, so this is not an independent complete implementation of candidate optimization. The sensitivity checks use floating-point cycle states and tolerances; they do not prove the all-graph theorem.

I checked the irrational nomination example, the interior coefficient example, the error budgets, and the inverse-law inequalities symbolically in the audit above. I did not run shared builds, the full varying-nomination algorithm, an independent all-graph numerical sensitivity suite, or all historical solver regressions. The proof review relies on the stated and cited preliminary real-algebraic primitives; it is not a fresh audit of the complete Basu–Pollack–Roy or Renegar sources. A failed attempt to use the unavailable `fitz` module was replaced by successful direct `pdftotext` inspection and did not affect source access.

Final frozen-section SHA-256:

`8b5645a80c0922cda4e57a1948670172268fa0cd4dc9fdc9c6505ec258a10219`
