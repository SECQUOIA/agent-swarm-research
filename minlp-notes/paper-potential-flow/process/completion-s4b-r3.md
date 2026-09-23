# Independent S4b review 3

## Verdict and scope

No major issue found. The section supports its stated algorithmic guarantees, including the new independent directional-coefficient model. I found one minor proof omission in the dual-threshold argument. It has a direct repair and does not invalidate the threshold lemma or the downstream algorithms.

I read all 959 lines of `complexity/sections/07-weighted-cactus.tex`, checked the relevant earlier-section dependencies, and inspected the cited primary-source passages described below. I did not read S4b author, lead, check/build, adjudication, or peer reports. I did not edit the manuscript or bibliography, run a shared build, or spawn agents. This report is the only repository file I wrote; temporary source downloads and extraction files used `/tmp/s4b-r3-*`.

The section SHA-256 matched the assigned freeze both before and after review:

`8b5645a80c0922cda4e57a1948670172268fa0cd4dc9fdc9c6505ec258a10219`

## Issue requiring repair

### R3-1 — Minor: a feasible dual can have no actual breakpoint

**Location:** lines 517–525, proof of `lem:a-wcac-threshold`.

The proof says that a dual minimum exists at a breakpoint and separately treats the case in which every `f_e` vanishes. There is another permitted case: every nonzero `f_e` belongs to a singleton coefficient interval. Then `D` has no actual breakpoints even though some `f_e` are nonzero. Feasibility makes this globally affine dual constant.

For example, take `f=(1,-1)`, `w=(0,1)`, and `L=U=(1,1)`. The equality is feasible and `D(lambda)=-1` for every real `lambda`. There is no breakpoint. This is also a physical coherently oriented two-edge cycle with offsets `(1,-1)`, circulation zero, and unit coefficients; parallel edges are permitted by the preliminaries. Every candidate edge-weight threshold nevertheless works.

**Concrete repair:** after discussing breakpoints, add that if `D` has none, it is affine on the entire real line; feasibility bounds it below, so it is constant, and any edge weight is a minimizing threshold. Alternatively formulate the argument using the partition at all distinct edge weights, allowing redundant breakpoints. Keep the all-zero-flow explanation for recovery. This supplies the missing degenerate case without changing the statement or algorithm.

This is a small mathematical proof omission, not an objection to ordinary LP duality or a request for a different algorithm. I found no other issue requiring correction.

## Mathematical audit

### Structural face theorem, lines 59–233

The two reductions have the required objective-preservation property. Pruning applies to physical subnetworks attached through a single physical vertex and having no support away from that vertex. Interval summation and greedy disaggregation describe their attainable nominations exactly. The zero-induced-source contraction is stronger and needed: with every `gamma_v=0`, the componentwise objective is invariant under independent potential translations. Recovering exterior component flows first, then the balanced effective block injections, justifies the lifting argument. Contracting blocks does not merge distinct vertices of another block because the block–vertex incidence graph is a tree.

The minimal support-spanning incidence tree has at most `p` leaves, and its branching-degree sum is `O(p)`. Thus the counts of special blocks, their retained incidences, and ordinary chains are `O(p)`, even when the physical blocks contain many nonsupport vertices. An ordinary block's induced adjoint vector is `(I,-I)` at its ports; `I=0` would trigger the previous contraction. This verifies the strict terminal ordering used by the first stage.

Smoothing with `g+rho*x` provides positive differential resistance at zero flow for both symmetric and asymmetric laws. The grounded Laplacian argument from Section 2 extends to source vector `c`. The balanced-box normal cone supplies a common multiplier even for lower-dimensional boxes and singleton intervals. Consecutive ordinary block interiors have disjoint adjoint ranges. Leaving shared endpoints free when either neighboring selected/special block contains them avoids inconsistent endpoint assignments.

For the second stage, `sum(deg_B-2)=2r_B-2` bounds marked high-degree vertices, and the suppressed-path count is `r_B+k_B-1`. The retained-port count remains `O(p)`. Path interiors have neither original objective sources nor retained attachments. Adding positive source `delta` there makes successive path currents strictly increase, so adjoint heights increase and then decrease, with at most a two-vertex plateau. A level has at most two interior vertices, giving the stated lower/free/upper/free/lower patterns and `n^{O(rp)}` enumeration. The first coarse face is fixed before the second perturbation, as required.

The flow bound, spanning-tree correction, energy-minimizer argument, and compactness justify the two separate limiting steps. Endpoint patterns use only graph structure, intervals, and objective sums, so freezing an attained joint coefficient optimizer establishes the structural extension without solving any varying-coefficient higher-rank block problem. The section explicitly preserves that distinction at lines 950–955.

### Fixed-law formulas, panels, and summation, lines 235–444

The identity `Aw=c` makes the weighted objective a sum of edge drops. Coherent reorientation must reverse offsets and weights and swap directional coefficients; the text does all three. Cycle independence follows from edge-disjoint cycles, including cycles meeting at articulation vertices.

On a closed sign cell, the cycle polynomial has constant quadratic coefficient, affine linear coefficient, and quadratic constant term. Its physical derivative is a sum of nonnegative terms. Hence the plus-root selector is correct even when the quadratic coefficient is negative. The linear chart retains its nonzero denominator condition, and a zero derivative forces every flow to vanish, justifying the explicit zero chart. Projection and sampling use fixed dimension, rather than enumeration of exponentially many formal sign choices.

The square-root panel construction uses rational centers whose square roots are rational. The maximum normalized displacement is `7/9`; the geometric tail gives the displayed safe `9/2` bound. Scaling by polynomial-bit `S` adds only `log S` to the accuracy requirement. Dense expansion remains polynomial because nomination dimension is fixed. The common sign partition is formed after collecting local domains, panel boundaries, denominators, and bridge sign hyperplanes. It does not enumerate combinations across cycles.

Multiplication of polynomially many rational denominators has polynomial total degree and coefficient size. Their nonvanishing conditions remain in the formulas. Uniform approximation bounds the surrogate near potentially vanishing denominators. Optimizing strict existential thresholds handles open parts correctly. The error arithmetic checks: surrogate bisection width `eps/8`, approximation error `eps/16` on each side, and the strictly lower sample threshold yield a physical loss below `5 eps/16`; later rounding adds at most `eps/4`.

The nomination-continuity proof is valid on general connected graphs: difference flows follow decreasing difference potentials and form an acyclic directed flow with total source mass `||b-b'||_1/2`. This gives the edgewise flow bound. The asymmetric law is Lipschitz across zero with constant `2 beta_U B_0`. Rational LP rounding inside the original polytope therefore need not preserve chart membership, even for a lower-dimensional polytope.

### Threshold LP and circulation candidates, lines 446–639

Except for R3-1, the threshold proof is complete. Untied endpoints maximize the reduced-cost terms; tied coefficients supply every value in their aggregate interval. At zero flow the endpoint choice is immaterial. Aggregating an arbitrary tied group into two inequalities avoids enumerating its corners, and greedy contribution filling has at most one interior tied coordinate.

For fixed nomination parameters, a threshold circulation domain is compact after the artificial bounds. A boundary must have an active specialized constraint nonconstant in circulation; an identically zero constraint does not supply a boundary. Both roots of every genuine quadratic boundary are needed and included. The selectors `2aq+b >= 0` and `<= 0` remain correct for negative `a` and double roots. Linear boundaries require `b(z)!=0`; coefficient-vanishing strata either exclude the point or leave other constraints to determine boundaries. Nonflat stationary points and feasible flat branches cover the remaining possibilities, including disconnected and singleton feasible domains.

The local maximum must be selected before summing cycles. Pairwise comparisons of rational surrogates within one cycle add polynomially many partition polynomials and avoid exact cross-cycle radical comparisons. The maximum is stable under uniform candidate errors. The actual chosen candidate differs from its own surrogate by at most the same local error, so the subsequent `5 eps/16` witness accounting does not forget the approximate selection loss.

Recovery divides by a flow factor only when nonzero. It works over the common algebraic nomination sample and one local extension at a time. Each circulation is at most quadratic over that common field on nonflat branches; flat branches use fixed-dimensional sampling. The resulting list of separate representations suffices to recover coefficients and round coordinates, without constructing a compositum of all cycle fields.

### New directional-coefficient model and continuity

The strengthening is proved rather than inferred from the older symmetric source notes. On any flow-sign cell exactly one of an edge's directional coefficients enters its drop and the one-row LP. The other coefficient is unconstrained by that local state and can be assigned any allowed rational value. At zero flow neither directional coefficient contributes. Reorientation swaps the two intervals. These observations justify the local extension even when the two directional intervals are different.

The shared symmetric model is correctly treated as one coefficient, not as an independent pair. Recovery and rounding preserve that shared coordinate. Closed sign cells do not enlarge the feasible physical model at zero, because both branches have drop zero there.

The new all-graph sensitivity proof uses coefficient-independent smoothing. The smoothed law is jointly continuously differentiable, including at zero, and its flow derivative is positive. Pairing the differentiated equations with a unit terminal adjoint gives the stated positive sign in the parameter derivative. The adjoint current has magnitude at most one by acyclic path decomposition. Each original coefficient derivative is thus bounded by `B_0^2`; integrating inside the original product box and taking the uniform smoothing limit gives the terminal estimate. Summing against absolute objective coefficients and combining with nomination sensitivity gives the displayed joint estimate. This argument permits coefficient changes that cross flow signs; it does not assume a fixed active set along the segment.

The inverse-law argument for capacity rounding is also valid across signs. For one fixed asymmetric law, opposite signs give a sum of two positive squares, bounded below by `beta_L*(u-v)^2/2`. Changing coefficients at a fixed flow uses only one active coefficient, so that term is at most `B_0^2 delta`, while the terminal-potential change contributes `B_0^2 k delta`. The stated squared flow bound and sample choices of rounding widths follow. All controlling constants have polynomial bit length, with `k<=2m`.

### Boxes, local filters, and exact profiles, lines 702–901

The fixed-support balanced-box corollary correctly optimizes all reduced faces and lifts nominations rationally. Choosing a face by its greatest certified lower endpoint incurs only the stated local interval error. The unfiltered-domain qualification is necessary and explicit.

With fixed nomination dimension, exact local capacity feasibility reduces to the intersection of cycle eligibility conditions and bridge conditions in nomination space. For fixed laws, bounded-degree local polynomial filters still use only that nomination vector and one circulation. The joint-law result is appropriately restricted to affine arc bounds, which preserve quadratic circulation boundaries. Compactness and closedness give attained physical optima, while the surrogate search can still use open pieces.

The irrational-nomination example checks directly: the two unit capacity bounds force `q=1`, and the cycle equation becomes `t^2=2`; the other flow bounds hold. Thus rational exactly feasible nomination output would be false without slack. The tightened-output guarantee is correctly relative to the tightened optimum only, and does not claim preservation of arbitrary polynomial filters during rounding.

At fixed rational nominations, sign/capacity/artificial endpoints and nonflat stationary circulations are rational. Tied filling at these points uses rational arithmetic of polynomial bit length. An irrational candidate can arise only from an aggregate feasibility boundary. At an attained minimum or maximum of a sum of independent contribution intervals, every nonzero tied contribution must attain its corresponding endpoint. Thus the coefficient profile is rational even though the induced circulation and local value need not be. Zero factors, singleton coefficient intervals, and coincident aggregate bounds cause no recovery problem. A flat objective can select a boundary of its compact feasible circulation set, reducing to the same cases. Choosing inactive directional coefficients rationally completes the extension to original directional profiles.

The quadratic-value comparator is correct. For opposite signs of `U` and `V`, `sign(U+V)=sign(U)*sign(U^2-V^2)` after checking zero cases; the squared difference contains only one radical. This detects equality across distinct stored radicands and does not require factoring or a numerical separation guess. Independent local winners give a global optimizing profile without comparing a growing sum of radicals.

### Interior-resistance example and implementation scope

For `w=(2,-1,-3,0)`, the coherent incidence convention gives `Aw=(2,-3,-2,3)`, as claimed. Every physical circulation is strictly between `-3` and zero. With threshold `-1`, the three untied reduced-cost terms are strictly negative, so their lower coefficient endpoints give the bound `-6(q+1)^2-12`. Equality first fixes `q=-1`, then coefficients 1, 3, and 4 to one, and finally coefficient 2 to two by circulation compatibility. The profile `(1,2,1,1)` is feasible and uniquely maximizing. This proves that endpoint-profile enumeration would miss the optimum in this symmetric example; no uniqueness of inactive directional coordinates is asserted.

I inspected `code/potential_flow_mpd/exact_weighted_cactus.py`, its main check script, and `paper-potential-flow/verification/check_a7_weighted_asymmetric.py`. The manuscript accurately limits the public solver to supplied symmetric blocks. The directional script is a mechanism harness using sign-restricted calls to that solver; it does not implement a graph wrapper or the varying-nomination optimizer.

## Dependencies and source audit

Repository proof dependencies inspected were `01-preliminaries.tex` (network convention, existence/uniqueness, block decomposition, fixed-dimensional elimination and sample representations), `02-cactus.tex` (grounded smoothed adjoint), and `03-block-rank.tex` (symmetric coefficient sensitivity). Their uses in this section are consistent with their hypotheses. In particular, Section 7 supplies its own directional sensitivity derivation rather than citing the symmetric result as though it already covered the new model.

I also inspected the relevant proof material in the five explicitly allowed source leads: the two promoted accuracy-bit result files, `notes/potential-flow-reopened-weighted-face-reduction.md`, `notes/potential-flow-reopened-weighted-investigation.md`, and `notes/potential-flow-exact-weighted-cactus-solver.md`. Their prior review statuses were not used as evidence, and linked reviews were not opened.

I read `literature/AGENTS.md`. The following source checks used actual full-text passages, not just metadata or abstracts:

- **Gotzes–Heitsch–Henrion–Schultz:** downloaded the [WIAS author manuscript](https://www.wias-berlin.de/people/heitsch/GHHS16_Preprint.pdf) to `/tmp/s4b-r3-ghhs.pdf` and inspected its extracted text. Theorem 6 and equation (44), printed p.18 (PDF p.20), give the affine-ray radical/rational formulas. Printed p.24 (PDF p.26) explicitly states the extension to node-disjoint cycles with attached trees. These support lines 42–48 without supplying the section's stronger combined theorem. The web tool initially timed out; direct retrieval succeeded.
- **Vigneron:** inspected `literature/papers/vigneron2014-geometric-optimization-and-sums-of/fulltext.md`, especially local page markers p.7–10, and re-extracted the same passages from `original.pdf`. Section 2.3 explicitly discusses a bit model; Theorem 6 and Section 3.2 give the common-arrangement and approximate-summation ingredients with polynomial dependence on `1/eps`. The section correctly avoids describing that predecessor as real-RAM-only or as an accuracy-bit algorithm. The bibliography's publication record is used with explicit author-manuscript locators in the text.
- **Aßmann–Liers–Stingl–Vera:** inspected the local full text and re-extracted `original.pdf`, Sections 4.2 and 4.3.3, especially Lemma 4.10 on PDF/printed pp.20–21. The cycle interval equivalence is linear in the loss coefficients at fixed circulation endpoints; tree robustness is reduced to polyhedral containment/LP. The bibliography identifies the arXiv version used for the locators. These are appropriate predecessors, not a source for the present weighted joint optimizer.
- **González Grandón–Heitsch–Henrion:** inspected the [WIAS 2401 manuscript](https://www.wias-berlin.de/preprint/2401/wias_preprints_2401.pdf), downloaded as `/tmp/s4b-r3-gg.pdf`. Section 2 restricts the network model to trees; Section 3.2 and Lemmas 2–3, printed pp.7–8 (PDF pp.9–10), explicitly solve the ellipsoidal and rectangular roughness inner optimizations. The manuscript's description of random loads combined with robust roughness uncertainty is supported.

The novelty qualification is appropriately narrow. These sources establish several ingredients; none of this review is an exhaustive priority search. I did not independently reprove the cited general real-algebraic algorithms or verify all bibliographic publication metadata against publisher records.

## Validation actually performed and limits

I ran the following with `PYTHONDONTWRITEBYTECODE=1`, without writing shared build products:

1. `paper-potential-flow/verification/check_a7_weighted_asymmetric.py`: passed 120 exact original-directional LP cases (29 feasible), 32 exact directional cycle cases, 32 interval-swap reorientations, 1,280 independent physical profiles, 1,280 sensitivity cases, and the explicit coefficient-induced sign crossing.
2. `code/potential_flow_mpd/exact_weighted_cactus_checks.py`: passed 1,200 quadratic comparison/interval cases; 45 cycle cases, including 15 capacity cases; 1,531 independently solved physical profiles; the interior-resistance, all-zero, fixed-coefficient irrational, flat-objective, and singleton-capacity regressions; and an 80-bit multiblock interval check.
3. A small independent exact Python control verified R3-1's constant dual and its valid rational optimizing profile, and checked exact cancellation between differently stored radicals and an opposite-sign value comparison.

The supplied tests are regression evidence. Finite numerical coefficient/profile samples do not establish global optimality or universal continuity. The directional exact-cycle harness shares the public solver's candidate implementation, so its agreement is not an independent proof of candidate completeness. No full varying-nomination semialgebraic implementation, asymptotic performance experiment, shared build, or exhaustive literature search was performed. A first attempt to inspect PDFs through Python `fitz` failed because that module was unavailable; inspection proceeded successfully using `pdftotext` on the actual PDFs.

Final frozen section hash: `8b5645a80c0922cda4e57a1948670172268fa0cd4dc9fdc9c6505ec258a10219`.
