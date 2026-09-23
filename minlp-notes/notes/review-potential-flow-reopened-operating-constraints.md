# Independent review of reopened operating constraints

Date: 2026-09-06. Reviewer: independent `review_constraints` agent. Verdict: the ordinary-upper-capacity irrational-witness proposition, its smaller equality version, the cactus contrast, the pressure-filter example, and the strict-margin recovery argument pass mathematical review. The stronger linear resistance-perturbation bound was developed during this review and independently checked by the investigating agent; it should additionally be covered by the coordinating agent's independent review before being described as multiply audited.

Reviewed files: [candidate note](potential-flow-reopened-operating-constraints.md), [author's exact checker](../code/potential_flow_mpd/reopened_constraints_exact_checks.py), [global cactus capacity result](../results/potential-flow-global-correlation-arc-validation.md), and the relevant pressure-superlevel representation in [global energy maximization](../results/potential-flow-global-energy-maximization.md). The final candidate reviewed here is the version that leads with ordinary upper capacities and includes the linear perturbation bound. No author files were edited by this reviewer.

## Irrational parameter witness and minimal cycle rank

The saturated-cut step is exact. At u the only outgoing arcs have upper bounds one, there are no incoming arcs, and the injection equals two. Conservation therefore forces both flows to one despite the positive width of every capacity interval. Zero nominations at the branch nodes give equal flow along the two edges of each branch. Both branches have the same drop and strictly positive resistances, so their flows have the same sign; their sum one forces positivity. Thus their quadratic equations may be used without a sign ambiguity.

Eliminating the branch flows gives d=6−4sqrt(2). The connector adds exactly one and the unit target flow forces target resistance theta=1+d=7−4sqrt(2). The indicated rational interval strictly contains this value, and the discriminant of theta²−14theta+17 is 128. Hence no rational resistance profile is feasible. The provided original-node potentials satisfy each individual edge law, including the branch midpoint potentials. All remaining flow bounds hold with room to spare. This verifies feasibility as well as necessity; exhibiting an irrational feasible point alone would not prove the claim.

The graph is simple: a direct edge is parallel to a connector followed by two parallel length-two paths. Series/parallel construction is explicit. Its six edges and five vertices give cycle rank two. The smaller four-vertex example similarly checks and forces theta²−12theta+4=0. The original finite two-point resistance set in that smaller example has neither polynomial root, while its interval hull does; this is a valid filtered-hull obstruction.

For the contrast, the old cactus proof has the necessary stronger contract: fixed rational nominations, rational parameter polytope, rational signed arc capacities, and affine parameter dependence of every coefficient. Cycle circulation bounds are equivalent to inequalities H(a,theta)≤0≤H(b,theta). These are affine rational inequalities even under correlations. A nonempty rational polytope has a rational feasible point, so its returned original resistance scenario satisfies capacities exactly. Every connected simple graph of cycle rank at most one is a cactus. Therefore rank two is the smallest possible *global cycle rank* for the exhibited rational-output obstruction. This does not say every rank-two graph lacks rational witnesses, and it is not a complexity lower bound.

## General perturbation and rational rounding

The flow bound M=(sum|b|)/2 is valid for arbitrary balanced nominations: orient each nonzero physical edge downhill in potential. The resulting flow has no directed cycle and decomposes into source-to-sink paths with total weight M. Each edge therefore has magnitude at most M. This does not require a single source or fixed flow signs across parameter profiles.

The initial square-root estimate passes: h=x'−x is a circulation, so its inner product with a potential gradient is zero. Separate the coefficient change using beta' times the constitutive-function difference and the residual (beta'−beta)f(x). The scalar inequality gives beta_L sum|h|³/2 on the left; the absolute residual is at most delta M² sum|h|. The max-norm estimate and the zero case follow. There is no missing derivative assumption.

During review I found the stronger estimate

    ||x'−x||_infinity <= 2m M delta/beta_L.

The candidate now contains the full proof. Its additional combinatorial fact is valid: a largest edge H of a nonnegative circulation belongs to a directed cycle whose edges all have flow at least H/m. If its head cannot reach its tail through those edges, the reachable cut has incoming flow at least H but total outgoing flow strictly below H, a contradiction. A simple return path gives a simple cycle. Edges are reoriented by h, not by physical x; the latter may have either sign after reorientation, which is why the scalar argument explicitly treats crossing zero.

For h>0, f(x+h)−f(x)≥h|x|/2 holds. When x crosses zero, substituting x=−th gives the nonnegative remainder h²[2t²−(5/2)t+1], whose minimum is 7h²/32. Along the selected cycle the potential increments sum to zero. If H exceeded 2mMdelta/beta_L, each positive-coefficient constitutive increment would strictly dominate the absolute parameter-residual term. For x=0 its increment remains strictly positive while the residual vanishes. Summing is impossible. This establishes global Lipschitz continuity of the flow in resistance on the positive box, including zero or reversing flows. The coefficient is conservative; sharpness is not claimed.

For a common capacity slack gamma, delta≤beta_L gamma/(4mM) changes every flow by at most gamma/2. Coordinatewise dyadic rounding with spacing at most delta, clipped to the original rational interval endpoints, lies in the box and is within delta. Its integer part is controlled by the input resistance bounds; its fractional bit count is controlled by the input and max(0,log(1/gamma)). This is an existence and output-size result conditional on a strictly feasible real design. It neither finds that design nor covers arbitrary non-box parameter restrictions by coordinatewise rounding. Rational nominations should be explicit when stating the rational-input encoding conclusion.

The pressure bound follows by splitting beta'f(x')−beta f(x), using |x|,|x'|≤M and the 2M Lipschitz constant of f on [−M,M], and summing an oriented path. Combined with the linear flow bound it gives k M²delta(1+4m beta_U/beta_L). A finite family of strict pressure-difference margins survives sufficiently fine rational rounding. Absolute potentials need a fixed reference or a separate gauge argument, as the note correctly states. Zero nominations give zero flow for every positive profile and are handled separately.

## Pressure filters and conic representation

For two parallel branches of resistance sums A,B under unit transfer, the equal-drop equations and conservation give D=AB/(sqrt(A)+sqrt(B))². At the two rational profiles (1,9),(9,1), D=9/16; at their midpoint D=5/4. Splitting the A branch into two equal resistances preserves the original triangle model. The restriction D≤1 is therefore nonconvex in the original resistance coordinates. This rules out a rational affine feasible-region description in those coordinates, including a projection of an LP; it does not rule out a nonlinear change of variables.

For the opposite bound, D(beta)=3 min_{Ax=b} sum beta_e|x_e|³/3 is concave because it is an infimum of linear functions of beta. The superlevel set D≥c is convex. Strong energy duality gives exactly the stated extended conic condition, dual objective at least c/3. The factor three and the existential quantifier over dual variables are correct. This does not imply a rational feasible conic point at a degenerate boundary, and the note makes no such claim.

## Independent reproduction

[check_reopened_constraints_review.py](../code/potential_flow_mpd/check_reopened_constraints_review.py) uses only the standard library and imports no investigated implementation. It checks the irrational examples in Q[t]/(t²−12t+4), a different basis from the author's Q(sqrt(2)) arithmetic, and checks interval isolation, every original law, nominations, cut saturation, and shifted irreducibility. It also checks:

- 5,329 exact rational scalar pairs, including sign reversal;
- 350 independently generated rational circulations for the high-edge cycle lemma;
- 441 exact pairs of physical triangle states with fixed nominations (2,−1,−1), including a vanishing and reversing third-edge flow, for both perturbation estimates and pressure bounds;
- the author's exact script under normal and optimized Python.

The independent script passed under both normal and optimized Python. The finite regressions support implementation and algebra; the preceding full arguments establish the universal claims. No mathematical or implementation defect was found in the reviewed author files. Minor wording suggestions about rational nominations and positive accuracy-bit notation were sent to the author.

## Source scope

I directly read the relevant open primary passages of [Aßmann, Liers, Stingl, and Vera (2018), Proposition 4.9, Lemma 4.10, and Proposition 4.11](https://arxiv.org/pdf/1808.10241). They support the note's explicit attribution of affine coefficient restrictions for a cycle. This mechanism is prior work.

I also read [Klimm, Pfetsch, Skutella, and Strubberg (2026), Remark 8 and Corollary 4](https://arxiv.org/html/2604.26882v1). They already discuss irrational arithmetic from rational input and convex continuous conductance design. These facts must not be presented as new. The no-rational-*parameter*-witness example under ordinary capacities is a narrower statement than either passage. The candidate correctly distinguishes resistance from conductance coordinates and numerical state irrationality from unavoidable parameter irrationality.

Independent searches on 2026-09-06 used combinations of rational/irrational resistance design, nonlinear resistive network capacities, potential-based flows and Lipschitz parameter dependence, and coefficient perturbations of graph p-Laplacians. They did not locate the precise rank-two no-rational-parameter-witness construction or the explicit all-graph Lipschitz bound above. This limited search cannot clear priority. The Lipschitz proof uses elementary circulation and scalar monotonicity arguments and should be presented as a useful supporting bound unless a stronger novelty assessment supports more. I did not independently inspect the inaccessible full 2023 reduction article and make no claim about its unseen results.
