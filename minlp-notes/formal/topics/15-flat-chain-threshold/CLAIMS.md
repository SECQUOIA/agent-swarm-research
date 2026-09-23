# Flat-chain threshold: mathematical obligations

This frozen inventory covers the mathematical assertions in
[Section 7 of the manuscript](../../../paper-network-simplex/sections/07-fixed-state-chains.tex),
with the graph definition, balanced-incidence construction, and four-label
example from [Section 6](../../../paper-network-simplex/sections/06-series-parallel.tex),
the local coordinate-section lemma from
[Section 4](../../../paper-network-simplex/sections/04-bounded-rank.tex),
and the state-merger principle from
[Section 1](../../../paper-network-simplex/sections/01-foundations.tex)
as required dependencies. Only those dependencies are included: this package
does not claim the entire network–simplex manuscript, general nested
series–parallel networks, arbitrary block factorization, or the separate
Fibonacci construction. The stronger residual-eliminated manuscript takes
precedence over the earlier fixed-state note.

An obligation is discharged by an actual theorem with the stated hypotheses,
not by a similar calculation or by assuming its difficult conclusion.
`COVERAGE.md` will map each identifier to its declarations and identify reuse.
This inventory itself is not a completion claim. All statements concern the
actual original-coordinate graph hull unless explicitly about an intermediate
profile system or circuit library.

The unit and determinant coefficient bounds concern **flow and observed
product coordinates**. They do not assert the same bound for simplex
coordinates or constants. Coefficient properties require a representation of
the actual affine rows and their original coordinates, not only a feasibility
test on abstract right-hand sides. Include arbitrary observation patterns,
zero simplex weights, ties in minima, zero rows, redundant constraints,
and lower-dimensional feasible profile regions. The manuscript's graph has
`L >= 1`; any `L=0` extension must be distinguished from that graph domain.

## Graph, disaggregation, and exact profiles

| ID | Required assertion | Source and material scope |
|---|---|---|
| FC01 | The stated parallel-pair chain with bypass has the specified unit-capacity source–sink flow semantics, and conservation is equivalent to `x_ai+x_bi+x_h=1` for each gadget. | Section 6 graph definition; existing `Chain` proof may be reused. This is the actual incidence model, not merely a list of assumed balances. |
| FC02 | Sparse graph-hull membership is equivalent to the common-simplex state disaggregation, and a feasible disaggregation gives at most one graph point per positive-weight state. | Section 1 `prop:disaggregation`; used throughout Section 7. Retain zero weights and the original simplex coordinates with residual weight `1-sum y`. |
| FC03 | State-flow conservation gives a shared branch profile `w_j`, its bounds `0<=w_j<=lambda_j`, bypass entries `lambda_j-w_j`, and total `sum w=1-x_h`. | Section 6 equation `chain-profile`. The same profile is used by all serial gadgets. |
| FC04 | The four observation classes partition the states, with the residual state in the neither-observed class; all observed entries and `R_i` have exactly the displayed meanings. | Section 7 complete shared-profile system and equation `chain-R`. A doubly observed state contributes its `a` product to `R_i`, not both products. |
| FC05 | Subject to original flow/simplex and observed-product nonnegativity checks, the full profile equations and inequalities are necessary and sufficient for actual hull membership. | `prop:chain-profile`, equations `chain-profile-bounds` through `chain-endpoints`. Include bypass observations and zero weights. |
| FC06 | Free entries in `[0,w_j]` attain every aggregate between zero and their total capacity; using them independently for each gadget produces all required state flows, capacities, balances, aggregates, and observations. | Constructive sufficiency in `prop:chain-profile`. Existing proportional allocation establishes existence; the particular greedy algorithm is separately required below. |
| FC07 | Eliminating and restoring `w_0=t-sum w_hat` is exact, with both residual inequalities, the two reduced subset endpoint rows, and all singleton equality/bound rows retained. | Equations `chain-residual-reduced` and `chain-endpoints-reduced`. Include empty subset rows as scalar checks. |
| FC08 | Every nonzero reduced normal lies in the specified universe `N_m`; there are at most `2^m+m` distinct nonzero normals. Every individual original right-hand side has flow/product coefficients in `{-1,0,1}`. | Equation `chain-normal-universe` and following paragraph. Distinct geometric normals are counted once; at `m=1` the negative singleton and negative total coincide. |
| FC09 | Grouping original rows by the minimum right-hand side is an exact feasibility equivalence, with an attaining original row available for each present normal and zero rows checked separately. | Section 7 grouping. Existing augmented grouping adds redundant box consequences; it must not be treated as source-only grouping without a proved bridge. |

## General fixed-state circuits and determinant bounds

| ID | Required assertion | Source and material scope |
|---|---|---|
| FC10 | Define the maximum absolute `0/1` determinant over orders at most `m`, including empty determinant one; prove finiteness, the values `Delta_1=Delta_2=1`, `Delta_3=2`, and the Hadamard bound `Delta_m<=max(1,m^(m/2))`. | Definition before `thm:fixed-chain`. Distinguish the integer determinant maximum from real exponent notation in the upper bound. |
| FC11 | Feasibility of the finite grouped real system is equivalent to nonnegative right-hand side for every nonnegative normal-cancellation certificate. | Farkas step in `thm:fixed-chain`. Prove or reuse a theorem with the correct non-strict inequalities and no unexplained feasibility premise. |
| FC12 | The nonnegative cancellation cone is pointed; its extreme rays are exactly minimal positive dependencies, each with support at most `m+1`, and these rays generate the cone. | General circuit argument in `thm:fixed-chain`. A bound on matrix rank alone does not prove cone generation or the feasibility criterion. |
| FC13 | A minimal positive dependence has a unique ray of weights and a primitive positive integer representative obtained from signed minors and division by their common gcd. | Circuit normalization in `thm:fixed-chain`. Show existence of the independent columns and nonzero cofactor kernel vector; handle two-element opposite supports. |
| FC14 | Every primitive circuit weight in the reduced universe is at most `Delta_m`, because whole-row sign changes make the relevant minors `0/1`. | Determinant argument in `thm:fixed-chain`. The bound applies to the actual normalized weights, not an arbitrary scalar multiple. |
| FC15 | Tests for all positive circuits of present normals, together with the zero-row checks, are necessary and sufficient for profile feasibility. Each such circuit belongs to the fixed full-universe library. | Equation `chain-circuit-tests`. Deal correctly with absent normals or prove an exact augmentation that preserves the later coefficient conclusions. |
| FC16 | A positive weighted sum of finite minima equals the minimum over independent row choices. Expanding the tests gives an exact finite affine original-coordinate description. | Paragraph following `chain-circuit-tests`. All branch choices are finite and minima are attained; no empty fiber is used. |
| FC17 | Each expanded circuit inequality has integer flow/product coefficients bounded in absolute value by `(m+1)*Delta_m`; original-domain and scalar zero-row inequalities satisfy that bound too. | `thm:fixed-chain` coefficient statement. Connect coefficient sums to actual rows and count repeated coordinate occurrences. |
| FC18 | At an infeasible query, rows attaining the grouped minima in a violated circuit yield an actual globally valid affine separator with the same violation at the candidate. | `thm:fixed-chain` separation. The selected right-hand sides stay fixed when the tested point changes. |
| FC19 | Enumerating supports of size at most `m+1` and exact elimination produces exactly the fixed-universe primitive positive circuits, in `2^{O(m^2)}` preprocessing depending only on `m`. | Enumeration paragraph in `thm:fixed-chain`. Prove correctness and termination of the specified finite construction and a quantitative parameter bound, not only finiteness. |

## Constructive recovery and complexity

| ID | Required assertion | Source and material scope |
|---|---|---|
| FC20 | A nonempty bounded profile polyhedron has a vertex, and the active normals at a vertex span all `m` profile coordinates, even if the polyhedron is lower dimensional. | Basis-recovery argument in `thm:fixed-chain`. Boundedness follows from explicit profile box rows; do not assume full-dimensionality. |
| FC21 | Precomputing all nonsingular bases of distinct library normals and their inverses, then testing candidates against every present grouped inequality, recovers a feasible profile whenever one exists. | `thm:fixed-chain` recovery. Prove candidate coverage and termination without an online LP oracle; the first feasible candidate may be selected in any fixed order. |
| FC22 | Greedy free-cell filling by repeatedly taking the minimum of remaining demand and the next capacity returns admissible entries with exactly the requested sum. | Recovery paragraph in `thm:fixed-chain`. Cover zero capacities, zero demand, full demand, and an empty free-cell list. |
| FC23 | Restoring the residual coordinate, filling each gadget, and normalizing only positive state weights returns a disaggregation and at most `m+1` actual graph points. | `thm:fixed-chain` constructive decomposition. A zero state contributes no division and is omitted. |
| FC24 | Building and grouping rows uses `O(mL+|Obs|+m)` rational arithmetic operations with preindexed subset masks and cached singleton indices; circuit evaluation and inverse-basis recovery add `2^{O(m^2)}` work. | Runtime statement and mask paragraph. Do not charge only coefficient arithmetic while hiding an `m`-coordinate normal copy per local row; state the arithmetic/indexing model. |
| FC25 | Greedy filling and writing all state-arc entries use `O((m+1)L)` arithmetic/output work; the complete exact separation and recovery satisfy the claimed combined bound and call no online LP. | `thm:fixed-chain`. Distinguish preprocessing, online tests, and output costs. |
| FC26 | Integer basis determinants and cofactors satisfy the stated determinant bounds, and grouped right-hand sides, circuit sums, recovered profiles, greedy entries, and normalized graph points retain polynomial rational encoding length. | Final paragraph of `thm:fixed-chain`. Bounds must cover actual intermediate values, not only a final rational witness; positive-weight division can increase size but remains polynomial. |
| FC27 | For `m=0`, the sparse hull is the original flow polytope and no profile elimination is needed. | `thm:fixed-chain` boundary. There are no explicit observed labels or product coordinates. |

## Exact finite libraries

| ID | Required assertion | Source and material scope |
|---|---|---|
| FC28 | The unreduced signed-subset normal universe in dimension `d` has the same circuit argument, coefficient bound `(d+1)*Delta_d`, and `2^{O(d^2)}` parameter work. | `rem:unreduced-chain`. This is a separate library from the residual-eliminated one. |
| FC29 | The full unreduced signed-subset universes in dimensions `1,2,3` have exactly `1,5,41` primitive positive circuits, with maximum weights `1,1,2`. | `rem:unreduced-chain`. An exhaustive checked enumeration must connect its predicate to mathematical primitive positive circuits; a list of valid circuits alone does not prove the count. |
| FC30 | The reduced universes for `m=1,2,3` have exactly `2,6,11` distinct normals and `1,5,16` primitive positive circuits, with maximum weights `1,1,2`. | `rem:unreduced-chain`. Establish completeness and distinguish full-universe counts from instance-specific present rows. |

## Two-label unit-coefficient theorem

| ID | Required assertion | Source and material scope |
|---|---|---|
| FC31 | The reduced two-label profile system is exactly the three-direction interval hexagon with all six endpoint groups present; its feasibility is equivalent to the five displayed tests. | Equations `chain-hexagon` and `chain-five-tests`; reuse existing interval results with a source-row grouping bridge. |
| FC32 | The displayed max-based formulas for `s_*`, `w_1`, and `w_2` satisfy every grouped bound whenever the five tests pass. | Constructive proof of `thm:two-state-chain`. Include equal interval endpoints and ties. |
| FC33 | The five two-label positive circuits are exactly the three opposite pairs and the two listed triples, all with primitive weights one; the stated forbidden pairs of normals do not co-occur. | Equation `chain-five-circuits` and occurrence proof. Exact classification is stronger than validity of those five tests. |
| FC34 | For every choice of original right-hand-side branches, each observed `a` product has coefficient magnitude at most one in each five-test cut, including singly and doubly observed states. | Occurrence analysis in `thm:two-state-chain`. Track both endpoint rows and both signs of a local equality. |
| FC35 | The corresponding unit bound holds for only-`b`, doubly observed `b`, and bypass products, and for individual zero-row checks. | Same occurrence analysis. The doubly observed `b` product occurs only in the opposite singleton rows because `R_i` uses its `a` counterpart. |
| FC36 | Every `x_ai`, `x_bi`, and shared `x_h` coefficient is unit after each five-test branch is expanded, including the compulsory cancellation from the negative total row. | Final coefficient argument in `thm:two-state-chain`. Unit circuit weights alone do not establish this. |
| FC37 | These branch inequalities and original-domain checks yield a finite exact unit flow/product description for `m<=2`, with separation and constructive decomposition in `O(L+|Obs|+1)` rational arithmetic operations. | `thm:two-state-chain`. Include the direct one-label interval case or a proved zero-label embedding and the zero-label boundary. |

## Three-label classification and coefficient repairs

| ID | Required assertion | Source and material scope |
|---|---|---|
| FC38 | Every primitive positive circuit in the three-label reduced universe has exactly one of the displayed four forms, with counts `7,5,3,1`, and the only weight two is on the negative total normal in the pair triangle. | Equations `chain3-circuits-a`–`chain3-circuits-d` and their completeness proof. Existing sixteen valid minimal dependencies and sufficient tests do not alone state the full classification. |
| FC39 | The classified circuits have the forbidden co-occurrences used in the proof and all positive-normal weights one; each product and each gadget-flow coefficient is consequently unit in every original-row branch. | Paragraph following classification. Include all observation classes, shared row occurrences, and the absence of products in the doubled negative-total right-hand side. |
| FC40 | The only nonunit bypass-flow cases are the singleton-partition coefficient `-2` and pair-triangle coefficient `+2`, with exactly the stated upper/lower endpoint row origins. | Bypass analysis in `thm:three-state-chain`. Prove exclusivity and that the three contributing rows belong to distinct gadgets. |
| FC41 | In the singleton-partition exception, adding a selected gadget balance changes the three affected flow coefficients to `(-1,0,1)` on `(x_h,x_ai,x_bi)`, leaving every other coefficient unit. | First displayed repair. Show that no other selected row contributes to that chosen gadget coordinate. |
| FC42 | In the pair-triangle exception, subtracting a selected gadget balance changes the three affected flow coefficients to `(1,0,-1)`, leaving every other coefficient unit. | Second repair. The negative-total weight is two but contributes no observed product. |
| FC43 | Both repairs preserve validity on the original flow domain and preserve violation at queries that pass the flow precheck. Every exact branch therefore has a unit flow/product representative. | Repair conclusion. This is equality modulo actual flow equations, not an arbitrary change of an ambient inequality. |
| FC44 | For arbitrary observations and three labels, original-domain/zero-row checks and at most sixteen fixed tests give the exact hull, a unit-coefficient finite description, and linear arithmetic separation/recovery. | `thm:three-state-chain` positive result. Compose coefficient results with actual hull equivalence and constructive recovery, including zero weights and lower-dimensional profiles. |
| FC45 | The first three-gadget example satisfies original flow/simplex and every separate McCormick inequality; its singleton-partition value is `-1/5`, with bypass coefficient `-2`, and the stated repair is a unit violated cut. | First half of `ex:chain3-repairs`. The observed products are zero and residual weight is zero. |
| FC46 | The second example also passes those checks; its three `R_i` equal `3/20`, the pair-triangle value is `-1/20`, bypass coefficient is `+2`, and the repaired cut is unit and violated. | Second half of `ex:chain3-repairs`. Observe exactly the three prescribed state pairs on the `b` arcs. |

## Four-label obstruction and required geometric dependencies

| ID | Required assertion | Source and material scope |
|---|---|---|
| FC47 | A coordinate-plane section locally equal to a nontrivial half-plane forces some inequality in every finite affine description to have the same two-coordinate normal up to positive scaling. Valid affine equations have zero coefficients on those free coordinates. | `lem:section-facet`. Prove a nonconstant active restricted inequality exists, the tangent-direction argument, positivity of scaling, and invariance under adding affine-hull equations. A displayed nonunit valid cut alone cannot establish impossibility of every unit description. |
| FC48 | For a square invertible `0/1` incidence matrix with nonempty proper rows and a positive balancing vector, the displayed flat-chain observation pattern, fixed weights, and fixed flows have the asserted valid original domains and necessary two-coordinate inequality. | `lem:balanced-incidence`, construction and necessity. Exactly two individual observed products remain free; all other original coordinates are fixed. |
| FC49 | The balanced-incidence construction is sufficient on an open neighborhood on the proposed side, by the inverse-matrix profile perturbation and single-row correction. | Equation `balanced-recovery` and the explicit epsilon bound. Prove nonnegative entries, profile/capacity margins, all aggregates and observations, and boundary inclusion. |
| FC50 | The balanced-incidence local section has two-dimensional interior and hence yields the claimed unavoidable coefficient ratio through the coordinate-section result. | Conclusion of `lem:balanced-incidence`. No projection or rescaling of additional free coordinates is allowed. |
| FC51 | The four-state incidence matrix is invertible and has balancing weights `(2,1,1,1)` with beta three; the exact graph, observation count, fixed data, and section inequality `2U+V>=3/32` have the stated values. | `ex:small-sp`: five vertices, nine arcs, cycle rank five, seven observations, specified products `U,V`, flows `13/32` and `5/16`, weights `1/4`. |
| FC52 | That actual four-label hull admits no finite description with all flow/product coefficients in `{-1,0,1}`, even after changing representatives by valid affine equations. Counterexamples extend to larger label counts by adding unused zero-weight labels. | Negative half of `thm:three-state-chain`. Show that no positive multiple of the forced ratio-two normal can have both nonzero coefficients unit. |
| FC53 | The same balanced-incidence family with `N=k+1`, first row `[k]`, and other rows `{i,k+1}` is invertible and realizes ratio `k-1` with the stated graph/state/observation counts, proving no state-independent coefficient-ratio bound on flat chains. | Generalization in `ex:small-sp`, used for Section 7's concluding unbounded-state warning. This can establish that warning without claiming the separate exponential Fibonacci construction. |

## Observed-label reduction

| ID | Required assertion | Source and material scope |
|---|---|---|
| FC54 | For a nonempty convex common state domain, the Minkowski sum of nonnegative scalar copies is the copy scaled by their total; include zero total and the empty family. | Equation `homothetic-merger`, the needed mathematical state-merger dependency. The flat-chain application need not formalize the unrelated full block-factorization theorem. |
| FC55 | Retaining every structurally observed label and merging unused labels with the residual state preserves the exact original hull; the merged weight is `1-sum_{j in J} y_j`. | `cor:chain-observed-labels`. Structural observation membership does not disappear when a label weight is zero. Keep the full original simplex constraints. |
| FC56 | A merged feasible state flow can be refined proportionally into every constituent global state, with an explicit zero-total case, preserving observations, capacities, balances, and aggregates. | Equation `proportional-refinement`, specialized to the common flat-chain domain. Dividing only by a positive merged weight is essential. |
| FC57 | Substituting the merged weight changes no flow/product coefficient, so all fixed-state conclusions hold with observed count `a` replacing ambient `m`; in particular `a<=3` is unit and `a<=2` admits five tests. | `cor:chain-observed-labels`. This substitution may change simplex coefficients, which are not claimed unit. |
| FC58 | Separation and compact recovery use `O((a+1)L+|Obs|+m)+2^{O(a^2)}` arithmetic operations; storing one normalized merged flow and constituent weights requires only `O(m)` additional bookkeeping. | Corollary runtime. Explicitly describe and prove the compact output representation and its refinement semantics. |
| FC59 | Writing every global state-arc entry can instead require `Theta((m+1)|E|)` output operations; compact recovery must not be claimed to materialize that larger output within its smaller bound. | Corollary output qualification. Account for output size separately from arithmetic on the compressed representation. |
| FC60 | With no observed labels the hull is exactly `Flow × Delta_m`; no profile elimination is needed. | Final corollary boundary. This includes arbitrarily many unobserved explicit labels and no products. |

## Reuse and semantic hazards

The existing [topic 06 coverage](../06-network-simplex/COVERAGE.md) establishes
FC01–FC07's core hull/profile semantics, much of FC09's feasibility grouping,
and the real feasibility/recovery criteria underlying FC31–FC32 and FC44.
Its `Circuits` module proves the sixteen displayed dependencies are distinct,
positive, minimal, and sufficient for all right-hand sides. It explicitly
does not prove the complete circuit classification, general determinant or
count bounds, unit-coefficient repairs, four-label obstruction, state merging,
or complexity. Existing proportional cell allocation proves existence but
does not verify the stated greedy filling algorithm and operation count.

Existing `GroupedProfile` adds a box consequence for every normal so that all
minimum fibers are nonempty. In particular it adds a negative-total row with
right-hand side zero. The source coefficient proof instead uses the original
negative-total right-hand side `lambda_0-t`, whose bypass coefficient is
necessarily `+1`. The augmented zero row cannot be fed into that occurrence
argument as though it had the same coefficient. Source-only branch grouping,
or a proved elimination/replacement of artificial branches, is required for
the claimed unit description. This does not invalidate existing feasibility
theorems; it limits their direct reuse for coefficient analysis.

The fixed-dimensional determinant maximum, basis inverse, and rational
arithmetic claims are mathematical algorithms. Their declarations must make
the chosen operation and bit-size models explicit. A mathematical charge
model does not verify the compiled arithmetic backend, Python implementation,
or parser unless a separate refinement connection is proved.

## Separate software, history, and scope

| ID | Assertion outside the mathematical completion claim | Boundary |
|---|---|---|
| FS01 | Repository scripts implement grouping, circuit generation, repaired cuts, and recovery correctly. | Proved Lean reference algorithms do not verify those Python executables without a refinement theorem. Focused tests may support current behavior. |
| FS02 | Historical finite enumeration outputs, regression counts, timings, LP comparisons, and benchmark results have the reported values. | Measurements and execution evidence are separate from the exact mathematical circuit-count obligations FC29–FC30. |
| FS03 | Literature attribution, priority, novelty, and external review history are accurate. | Formal proofs do not establish historical or bibliographic claims. |

The theorem's flat-chain restriction is substantive. This package makes no
claim that one shared profile, the five/sixteen tests, or the same determinant
bound describes arbitrary nested series–parallel networks. It also does not
assert that all state flows must be integral; the hull results and recoveries
here use real or rational flows.

Local checks are targeted to this topic. Project-wide verification belongs to
CI and is neither run locally nor inspected.
