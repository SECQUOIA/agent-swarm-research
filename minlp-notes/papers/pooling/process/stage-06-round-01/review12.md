# Stage 6, round 1 — review 12

I reviewed the entire introduction and Section 6, with extra attention to degenerate cases, endpoints, empty feasible sets, lower bounds, and exact arithmetic. I followed `process/reviewer-protocol.md` and the round instructions. The current Section 6 file matched the frozen round snapshot when checked. I did not edit manuscript files, inspect other reviewers' reports, or run builds.

**Findings: none confirmed.** I found no mathematical defect or necessary local correction in the reviewed material. The following records the substantive checks behind that conclusion; these are verification observations, not requests for optional extensions.

## Introduction and theorem dependencies

I checked the abstract, contribution paragraphs, selected-boundaries table, historical comparison, and roadmap in `sections/00-introduction.tex:1–217` against the relevant statements in Sections 1–5. In particular:

- The two existential-real regimes retain their different pool, attribute, bypass, quality-bound, and degree assumptions. The introduction does not infer rational witnesses from rational data or polynomial algorithms from NP membership.
- The degree-two versus degree-three comparison keeps the fixed actual pool interface, total external degrees, and feasibility/threshold distinction. The constant-data hardness theorem uses ordinary source/product economics, whereas the all-degrees-two approximation statement refers to its specified profit.
- The contract algorithms retain exact supplies or exact external contracts where needed, distinguish redundant from restrictive common pool bounds, and retain the zero outlet/common lower-bound assumptions for two-vector feasibility.
- The new physical response and isolated-optimum claims are represented as description and geometry results. The LP-hull entry states the broader linear physical-flow objective scope, while the isolated margin-block entry excludes retained quality and interpool constraints.

I consulted the relevant statements and dependencies in Sections 1–5, including the explicit Hoffman bound at `03-restricted-hardness.tex:807–838`, rather than treating earlier review status as a proof.

## Path certificates and physical response

At `06-synthesis.tex:11–63`, expanding the weighted endpoint products gives the stated linear coefficients and cancels every intermediate square. Strict separation of the two conditional endpoints establishes the vertex characterization, including terminal values zero and one. Inverting the recursion proves distinctness of all terminal values. The exposing inequality has equality only at the selected vertex.

At lines 66–184, I checked the physical capacity and midpoint-quality rows in both directions, the source/reset indexing for the two-quality relay, and the revenue telescoping identity. Only the final revenue varies. The exposing parameters at −1 and 1 still produce nonempty open regimes inside the chosen parameter interval, since uniqueness persists in a neighborhood before restricting that neighborhood to the interval.

The lower-bound removal is uniform over the whole price interval. After retaining the upper halves of the contracts, every contract deficit is nonnegative. The retained rows have zero violation, while a dropped lower-contract row has violation at most the sum of deficits. The Section 3 bound therefore gives the claimed repair distance with `H=N^N`. Base arc revenues are bounded uniformly by three. Rewarding all output throughput accounts for every source contract exactly once, and the additional reset reward accounts for every reset contract exactly once. Consequently `M=3H+1` excludes every positive-deficit optimizer without altering the objective on the exact-contract polytope except by a constant. Its bit length is polynomial even though its numerical magnitude is large.

At lines 186–241, the line-factor argument correctly concerns a formula in price and value alone. Every open boundary segment forces a distinct supporting-line factor in the product of the nonzero defining polynomials. It applies to the epigraph as well as the graph. The state-message count follows from unique exposure of every projected vertex on its upper boundary. The backward recurrence evaluates one support value with polynomial intermediate bit length and does not contradict the explicit-description lower bound. Fourier–Motzkin elimination preserves at most two variables per row, and the three-coordinate simplex counterexample correctly rules out the asserted coordinate-port universality.

## Nonlinear interface and exact hull

At lines 243–389, I checked all interface conservation equations, redundant output specifications, and the physical objective identity. Pool throughput stays exactly one even when the path's terminal flow is zero, so the active quality is uniquely `2−t`; there is no inactive-quality ambiguity. At `t=0,z=0`, the zero-flow product-quality row has its homogeneous interpretation. At `t=1`, all interface capacities and qualities also remain feasible.

The global-optimum characterization fixes the clean flow as well as the path vertex. For the perturbed objective, distinct terminal values differ by at least `4^{−(n−1)}`, which exceeds the perturbation. The outward derivative is strictly negative on every incident edge. The tangent-cone argument controls all nearby feasible directions, and extra clean flow decreases profit. The global optimum is unique among all feasible points, not merely among the constructed local optima.

The integer-dimension proof uses exclusion of every pairwise midpoint, not isolatedness alone. The parity contradiction applies to arbitrary continuous auxiliaries and unbounded integer coordinates. The binary upper construction selects precisely one labeled optimizer at any integral label.

The LP hull contains exactly the claimed vertical segments. Its lower and upper affine boundaries never meet, and any hull vertex projects to a path vertex. Thus returning an optimal LP vertex yields a physical optimizer with polynomial rational bit length. Returning an arbitrary point of the optimal LP face would not suffice; the manuscript explicitly makes that distinction.

At lines 391–438, the relay economics put the nonzero coefficient on the correct equal-flow duplicate. For general supply sequences, `s_{j+1}>2s_j` separates the lower and upper terminal ranges strictly, and `s_1>0` prevents coincident initial endpoints. The physical telescoping identity gives the same equality and hull arguments. The general-supply statement does not reuse the geometric sequence's particular perturbation size. The counterexample obtained by deleting the pool lower bound satisfies the other displayed constraints and earns `3/16`, so retaining nonlinear contracts is material.

## Dense slab, cost rank, and arithmetic

At lines 450–504, the SUBSET SUM reduction handles targets zero and total weight, including its nonempty-domain promise. Rounding error is at most `1/8`; adding the slab half-width still leaves a strict error below one. The padding coordinates cannot choose their upper branch at a zero of the certificate. The construction has polynomial bit length, and its endpoint bits give rational NP certificates. The manuscript does not infer physical degree-two hardness or strong hardness from this reduction.

At lines 506–651, I checked the interaction-rank identity and its additive-cost invariance; projected-box enumeration with repeated, zero, and dependent generators; and the hyperplane-slice argument for lower-dimensional polytopes. A zero-dimensional projected box is a singleton. Equal-total edges add no missing slice vertices. Segments between nonadjacent projected vertices remain feasible and therefore cannot introduce spurious objective values; interpolating stored corners supplies valid margins.

The total interval detects infeasibility. Zero-only feasibility is handled without division. On a candidate interval approaching zero, nonnegativity and total mass imply `|<C,W>|≤||C||∞ S`, so the zero extension loses no infimum. Singleton positive totals are evaluated directly. For `αS+β+γ/S`, all sign and zero cases are covered by endpoints, the positive minimum stationary point, or a constant value. Rational coefficients, bounded-degree candidate comparisons, and interpolation at a single selected square root support the claimed exact output field and bit complexity. The rank-one specialization allows signed factors and zero residual capacities; tied greedy coefficients do not invalidate endpoint attainment. The example with optimal total `sqrt(2)` verifies the need for quadratic output.

At lines 653–737, upper and lower Lagrangian quality multipliers combine in the same attribute span, while terminal specification terms are additive column costs. The perturbation estimate follows from total nonnegative mass. The rank-one constraint perturbation disjunction handles both signs and `z=0`; a nonempty singleton parameter interval also causes no problem. Even if an LP branch has no vertex, a finite rational LP optimum still has a polynomial-size rational feasible solution, which is all the text requires. The Square-Root Sum leaves are convex singletons despite their nonconvex-looking equality representation, and the conclusion is correctly an arithmetic implication rather than an NP-hardness assertion.

## Adjacent results and sources

I checked the scoped summaries at lines 739–857 against the corresponding canonical notes for rank-one margins, the correlation face, stability and approximate SDP lower bounds, common-factor optimization and reciprocal anchors, integer anchors, network universality, cycle/theta/parallel-path hulls, and power-flow transfer. The face selection correctly excludes the zero generator and selects one member of each pair. The text distinguishes LP nonpolyhedrality, total SOC size, fixed-order PSD block count, and unrestricted PSD order; it also retains the accuracy and objective-uniformity conditions on approximate lifts. The common-factor and network summaries preserve their restrictions on additional linking/product constraints and network balance/topology.

I read `literature/AGENTS.md` before using literature. Primary checks included Gärtner et al.'s Section 4, Lubin–Vielma–Zadik's midpoint lemma, the relevant projected-box precedent in Punnen et al., and the cited Boveroux et al. construction and one-column discussion. I also checked the LRS full manuscript's exact correlation-polytope lower bound against the stated source. In particular, Gärtner et al.'s displayed direction has the geometric sum bound giving `|λ|<1/15` at `ε=1/4`. The Boveroux construction's two parameter-dependent columns have disjoint nonzero row supports, confirming rank two. Source versions are identified in the manuscript bibliography.

The open-question discussion at lines 859–927 does not silently combine algorithms with incompatible contract or objective assumptions. Its private-supply/helper-pool example correctly distinguishes a global total from the missing separate source equations.

## Verdict and limits

**Verdict: no findings.** All new proofs in the introduction/Section 6 review scope were examined, including the degenerate cases described above. I did not run builds or new numerical tests, and no computational result is used as a theorem certificate. I checked adjacent summaries and their canonical arguments, but did not independently reproduce every long proof in the separate conic, network, or power-flow programs, or every earlier-stage reduction. This review is not an exhaustive priority search or a guarantee of external-review acceptance.
