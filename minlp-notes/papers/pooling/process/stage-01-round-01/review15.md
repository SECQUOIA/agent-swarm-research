# Stage 1 review — reviewer 15 — round 1

Focus: interdependencies between the model conventions, reductions, propositions, and corollaries.

## Major finding

### M1. Endpoint disjunction and MILP omit a needed upper-bound-only hypothesis

**Locations:** `sections/01-foundations.tex:641–658`, with downstream consequences at lines 660–672; compare the model at lines 37–47 and the subsection scope at lines 520–523.

The manuscript permits lower quality bounds and general polyhedral product regions. The endpoint paragraph restricts input values to `[0,1]` and product **upper** bounds to `{0,1}`, but does not withdraw lower quality bounds or additional product inequalities. Under the stated restrictions, the asserted equivalence with the support disjunction is false. Consequently the claimed exact MILP is not exact for that stated class.

Concrete counterexample: one scalar quality, one input of quality zero, one pool, and one product; feed and outlet capacities one; all lower flow bounds zero. Let the product quality interval be `[1,1]`. This is a facial specification: with `C={0}`, its intersection with `C` is the empty face. The endpoint paragraph's stated input and upper-bound restrictions hold. The proposed support formulation accepts one unit through the pool: `D=0` and `S=0`, since the product upper bound is one. Physical quality feasibility requires zero delivery because its lower quality bound is one. Assigning cost `-1` to the feed makes the formulation's optimal cost `-1` while the physical optimum is zero. Thus the issue also affects threshold certificates.

**Correction:** explicitly restrict this paragraph and all its consequences to coordinatewise upper quality specifications only, with no nonredundant lower quality bounds and no additional cross-quality constraints. Equivalently, say the regions are exactly the coordinate upper-bound regions (nonnegativity already follows from input qualities). No theorem extension is required to repair the intended result.

This is a missing essential hypothesis rather than a failure of the intended upper-bound-only argument. The same omission is present in the supporting result's informal endpoint paragraph, so that note is not an independent justification for the broader wording.

## Minor finding

### m1. State finite flow boundedness explicitly where optimal values are defined

**Locations:** lines 49–50, 125–127, the opening of `s1:triviality`, and lines 520–532.

The global model says arcs and totals “may have finite rational lower and upper bounds.” This can permit absent upper bounds. The sign subsection then calls `z*` a minimum and its proof decomposes an optimal flow; the facial theorem calls every branch a polytope and promises an integral optimum for every rational objective. These claims require bounded flow variables (or suitable separate attainment and bounded-objective hypotheses). The intended assumption is clear from the source results, both of which expressly impose finite arc/node capacities. However, the manuscript should carry it into the theorem scopes. A sole unbounded bypass of cost `-1` illustrates why absence of finite flow bounds cannot be silently allowed in the optimization assertions.

**Correction:** state that all instances in these capacitated optimization subsections have finite upper flow bounds sufficient to bound every arc; explicitly identify the later definition of `S` as removing that assumption. In the compactness paragraph, write “with finite flow bounds, imposing this box…” so the bounding conclusion has its hypothesis before it.

## Checked and found consistent

- Destination disaggregation evaluates the multiplier at the arc head; its conservation and quality identities then agree, and coordinatewise domination preserves precisely the zero-lower-bound capacity model.
- Single-product projection correctly relies on aggregate quality conservation and topological reconstruction. The sign test, averaging bounds, and destination-flow LP inequalities have the correct directions.
- The shortest-path reduction preserves quality ratios under common scaling, and its support and rational encoding arguments are sound under finite rational input data.
- The conic-hull statement uses positive-capacity support and correctly distinguishes a cone from the convex hull after reinstating capacities. The two-product counterexample is valid.
- The cyclic reconstruction properly separates isolated positive circulations from components with external inflow. The substochastic argument, absorption decomposition, and negative-cycle versus path-mixture criterion are consistent under the explicitly algebraic steady-state semantics. Merging isolated circulation into one product component preserves physical feasibility and domination.
- The facial sufficiency and necessity arguments, recognition LP, fixed-dimension face enumeration, and node-splitting integrality argument are coherent. In particular, positive lower bounds on omitted arcs must make a branch infeasible, as the manuscript correctly says.
- Affine rank reduction preserves the arc-flow projection, accounting for inactive pools. Rank-one matrix costs are correctly distinguished from physical arc costs.

## Verdict and verification limits

**Verdict: major findings present**, namely M1; m1 is an assumption-clarity issue with a straightforward repair. The intended upper-bound-only endpoint theorem appears sound once its scope is stated.

I read the complete assigned LaTeX section and independently checked the mathematical implications and edge cases described above. I also consulted the substantive proof text in `results/pooling-triviality-polynomial.md` and `results/pooling-facial-quality-integrality.md`. I did not inspect other reviewers' reports. This review does not establish priority claims from the external literature, audit bibliography metadata, review later paper sections, or certify compilation or journal acceptance.
