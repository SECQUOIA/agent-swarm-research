# Rational resistance witnesses under arc capacities and uniform perturbation bounds

Date: 2026-09-06. Status: supporting results passed an independent full mathematical and exact-arithmetic review. The uniform Lipschitz strengthening was proposed during review and its full proof checked separately by the investigating agent. Novelty remains qualified by the bounded source comparison below. No general algorithm for constrained series-parallel design is claimed.

## Main result: ordinary upper capacities can require an irrational resistance

**Proposition.** There is a feasible quadratic passive-flow design instance with rational data, fixed nominations, a simple series-parallel graph of global cycle rank two, one uncertain resistance interval, and only ordinary positive-width upper-capacity intervals, such that every feasible resistance design is irrational.

Use five vertices `u,v,r,w,z`. The direct target is `a=(u,v)`. A second u-to-v route begins with the connector `(u,r)` and branches into the paths `r,w,v` and `r,z,v`. Set

```
beta_a = theta in [4/3,11/8],    beta_ur = 1,
beta_rw = beta_wv = 1/2,        beta_rz = beta_zv = 1.
```

Fix `b_u=2`, `b_v=-2`, and zero nominations elsewhere. Impose `0<=x_a<=1` and `0<=x_ur<=1`; all four path edges have capacities `[0,2]`. Every capacity interval has strictly positive width and every lower bound is zero. The graph is simple and series-parallel, with cycle rank `6-5+1=2`.

**Proof.** Conservation at u forces `x_a+x_ur=2`, so both capped flows equal one. The two paths from r to v carry flows q_1 and q_2 summing to one. They share a pressure drop d and have positive resistances, so both flows have the same sign. Their positive sum makes both positive. The path resistance sums are one and two, giving

```
q_1^2 = 2q_2^2 = d,
q_1 = 2-sqrt(2),    q_2 = sqrt(2)-1,
d = 6-4sqrt(2).
```

The connector has unit flow and unit resistance, so adds pressure drop one. Since the target flow equals one, its resistance must equal the entire u-to-v pressure difference:

```
theta = 7-4sqrt(2) in (4/3,11/8),
theta^2-14theta+17=0.
```

For the interval claims, `theta>4/3` is equivalent to `sqrt(2)<17/12`, verified by `2<289/144`, and `theta<11/8` is equivalent to `sqrt(2)>45/32`, verified by `2>2025/1024`. Set `pi_v=0`, `pi_r=d`, `pi_u=1+d`, and `pi_w=pi_z=d/2`. These potentials and the displayed flows satisfy every original equation and capacity. Every feasible scenario must have the displayed theta. Its quadratic polynomial has nonsquare discriminant 128, so no feasible rational resistance scenario exists.

The [exact checker](../code/potential_flow_mpd/reopened_constraints_exact_checks.py) verifies every original physical equation in `Q(sqrt(2))`, rational interval membership, capacity bounds, and the discriminant obstruction. Its checks remain active under `python -O`.

### Smaller version if an exact flow requirement is allowed

Identify r with u and remove the connector. Use target resistance interval `[1/3,3/8]` and impose `1<=x_a<=1` explicitly. The same branch flows force `theta=6-4sqrt(2)`, with minimal polynomial `theta^2-12theta+4=0`. This is a four-vertex, five-edge simple series-parallel graph of cycle rank two. Potentials `pi_v=0`, `pi_u=theta`, and `pi_w=pi_z=theta/2` certify feasibility. The checker verifies this smaller example too; the main result above uses only ordinary upper capacities.

### What this establishes

The [cactus capacity-filter theorem](potential-flow-global-correlation-arc-validation.md) guarantees an exactly feasible rational original parameter scenario whenever one exists over the reals. That output guarantee cannot extend to all series-parallel graphs, even with continuous independent intervals, fixed nominations, and ordinary positive-width upper capacities. Global cycle rank two is the first possible rank for this obstruction, because every connected simple graph of global cycle rank at most one is a cactus.

This is an output-representation obstruction. It is not an NP-hardness proof, does not preclude exact algebraic output, and does not contradict unconstrained rational near-extremal endpoint recovery. A lack of strict feasible margins matters: in the main instance both cut capacities are necessarily saturated. The result does not show that strict capacity feasibility lacks rational witnesses.

There is also an immediate filtered-hull counterexample in the smaller equality-constrained version. Replace its interval by the two-point set `{1/3,3/8}`. No original scenario obeys `x_a=1`, whereas its interval hull has the feasible scenario above. Thus interval-hull replacement does not preserve existence after operating constraints filter scenarios, even on a series-parallel graph. This small example is explanatory; discrete capacity feasibility is already NP-complete on one cycle in the [existing result](potential-flow-discrete-flow-realization.md).

## Strict capacity margins restore rational witnesses on every graph

Let a connected graph with `m>=1` edges have fixed nonzero balanced nominations and positive rational resistance bounds `beta_L<=beta_e<=beta_U`. Put `M=(sum_v |b_v|)/2>0`. Every passive physical flow has absolute value at most M. For two profiles `beta,beta'` in the box, let `x,x'` be their physical flows, and suppose `||beta'-beta||_infinity<=delta`. Then

```
||x'-x||_infinity <= 2m M delta/beta_L.             (1)
```

This improvement over the initial square-root perturbation bound was proposed during independent review. It holds even when flows vanish or reverse signs.

**Proof.** Reorient each nonzero edge of the circulation `h=x'-x` so that its new h-coordinate is positive, and let `H=||h||_infinity`. Reorientation preserves the odd quadratic law and all resistance bounds. If H is zero there is nothing to prove. Take a directed edge `u->v` with h-value H. There is a directed path from v to u using only edges with h-value at least `H/m`: otherwise let S be all vertices reachable from v using those edges. Then u is outside S, the incoming cut contains the edge of value H, and every outgoing cut edge has value strictly less than `H/m`. There are at most m such edges, so total outgoing cut flow is strictly below H, contrary to circulation balance. Together with `u->v`, a simple such path forms a directed cycle on which every h-value is at least `H/m`.

Write `f(x)=x|x|`. The scalar inequality needed on this cycle is

```
f(x+h)-f(x) >= h |x|/2   for h>0.                 (2)
```

For `x>=0` and `x<=-h`, expansion even gives the stronger lower bound `h|x|`. For `x=-th`, `0<t<1`, subtracting the right-hand side of (2) and dividing by h squared gives `2t^2-(5/2)t+1`, whose minimum over the reals is `7/32>0`. Also `f(x+h)-f(x)>0` when x is zero.

Sum constitutive differences around the directed cycle. Potential differences telescope, giving

```
sum_cycle beta'_e [f(x_e+h_e)-f(x_e)]
 = -sum_cycle (beta'_e-beta_e) f(x_e)
 <= delta sum_cycle |x_e|^2.
```

If `H>2m M delta/beta_L`, then (2) and `h_e>=H/m` imply that each nonzero-x term on the left strictly exceeds `M delta |x_e|>=delta |x_e|^2`. Each zero-x term is strictly positive while its corresponding right-hand term is zero. This contradicts the summed inequality and proves (1). No positive lower bound on differential resistance `2beta_e|x_e|` was assumed.

The original energy argument remains a valid, weaker alternative: taking the scalar product of the constitutive difference with h gives `(beta_L/2)sum|h_e|^3<=delta M^2 sum|h_e|`, hence `H<=M sqrt(2m delta/beta_L)`. The cycle proof is sharper for sufficiently small perturbations and removes the square-root loss from the precision budget.

Suppose a real design obeys all signed arc bounds with a common strict slack `gamma>0`. Any box-preserving rational rounding with

```
delta <= beta_L gamma/(4m M)
```

changes each physical flow by at most `gamma/2`, so remains exactly feasible, with at least half the original slack. For fixed rational nominations and rational resistance boxes, such a rational profile exists with encoding length polynomial in the problem data and `max(0,log(1/gamma))` when gamma is rational: round each coordinate on a dyadic grid of spacing at most delta and clip to the rational endpoints. This is a witness-size and safe-rounding statement; it does not find the initial strictly feasible real design or prove that doing so is easy.

For completeness, if all nominations are zero, all physical flows are zero for every positive profile and any allowed rational profile suffices whenever the capacity bounds include zero.

Pressure differences also admit a safe bound. Along any fixed path of `k` edges, the two physical terminal pressure differences differ by at most

```
k [delta M^2 + 2 beta_U M ||x'-x||_infinity].       (3)
```

Indeed, compare `beta'_e x'_e|x'_e|` with `beta_e x_e|x_e|` edge by edge, using `|x_e|,|x'_e|<=M` and the `2M` Lipschitz bound for `x|x|` on `[-M,M]`, then sum with path orientation. Combining (1) and (3) gives the linear pressure bound `k M^2 delta (1+4m beta_U/beta_L)`. Thus strict pressure-difference margins also survive sufficiently fine rational rounding. Absolute potential bounds require a stated reference or an explicit treatment of the additive potential gauge.

## Upper pressure filters can already be nonconvex on a triangle

Take a triangle consisting of a two-edge path with total resistance A and a direct edge with resistance B, under unit terminal transfer. The terminal pressure difference is

```
D(A,B)=AB/(sqrt(A)+sqrt(B))^2.
```

On the rational resistance segment joining `(A,B)=(1,9)` and `(9,1)`, implement the path edges with resistances `A/2` each. At either endpoint `D=9/16`; at the midpoint `(5,5)`, `D=5/4`. Hence the upper-pressure restriction `D<=1` accepts both rational endpoint profiles and rejects their midpoint. The accepted resistance set is not convex, although all physical flows may remain within `[0,1]`.

This explains why arbitrary pressure filters cannot be appended as affine constraints to the cactus capacity LP. It is consistent with the [existing correlated-resistance energy-minimum hardness](potential-flow-global-correlation-energy-design-hardness.md), and is retained as a small exact diagnostic rather than an additional complexity theorem. The opposite one-terminal-transfer restriction `D>=c` is a convex resistance condition because D is concave in the resistance vector. The [existing energy-maximization SOCP](potential-flow-global-energy-maximization.md) gives its exact extended conic representation by requiring the dual objective to be at least `c/3`. No unconditional rational exact-feasibility output is asserted at a degenerate conic boundary.

## Literature comparison and novelty limits

[Raber's 2022 doctoral thesis](https://d-nb.info/1258349914/34), Theorem 3.12 on printed pages 34–35, already proves continuity of physical flows and potentials with respect to all positive arc resistances by parametric convex optimization. Section 3.7 proves differentiability in nominations subject to a condition on zero-flow cycles; it is a distinct parameter question. The thesis was downloaded openly and these passages were read directly; the [PDF](../literature/external-potential-flow-reopened/raber-2022.pdf) and [extracted text](../literature/external-potential-flow-reopened/raber-2022.txt) are retained. Continuity and qualitative strict-margin recovery are therefore established antecedents. The retained quantitative refinement is the explicit all-graph resistance Lipschitz constant `2mM/beta_L`, valid through zero flows, and its rational encoding and capacity-rounding consequences. This bounded search did not locate that precise quantitative statement.

[Aßmann, Liers, Stingl, and Vera (2018)](https://arxiv.org/pdf/1808.10241), Proposition 4.9, Lemma 4.10, and Proposition 4.11, express single-cycle circulation restrictions as affine inequalities in pressure-loss coefficients. These are the prior basis for the cactus contrast; affine capacity linearization is not a new claim. Their general robust feasibility model explicitly includes operating inequalities and uses polynomial optimization when no such reduction applies.

[Klimm, Pfetsch, Raber, and Skutella (2023)](https://doi.org/10.1287/moor.2022.1338) develop nonlinear effective resistance and series/parallel reduction. The small examples above use those established network calculations. Only the publisher abstract was accessed during this reopened search; no unseen theorem from that paper is being claimed as checked.

[Klimm, Pfetsch, Skutella, and Strubberg (2026)](https://arxiv.org/pdf/2604.26882), Remark 8 in Section 3.2, explicitly discusses irrational calculations arising even from rational or integral input in potential-flow network design. Its Corollary 4 also gives convex continuous conductance-cost design. Both passages were read in the repository's full-text copy and the open preprint. Thus neither the general existence of irrational quantities nor conductance convexification is a novelty claim here. The precise scoped observation retained above is a feasible rational-input, rank-two series-parallel **capacity-filtered resistance design with no rational parameter witness**, opposed to the rational-witness theorem on cacti.

Searches of openly accessible literature on 2026-09-06 for rational resistance design, irrational capacity-feasible parameters, continuous pipe design, and resistance sensitivity did not locate the precise no-rational-witness example or the stated uniform Lipschitz estimate. This was a bounded source search, not exhaustive priority clearance. The estimates use elementary circulation and scalar-law inequalities, and are retained as practical supporting results with qualified novelty.

## Independent review and reproducible evidence

The [independent full audit](../notes/review-potential-flow-reopened-operating-constraints.md) passed the ordinary-upper-capacity obstruction, smaller equality example, cycle-rank contrast, perturbation bounds, rounding consequences, and source framing. Its [independent checker](../code/potential_flow_mpd/check_reopened_constraints_review.py) verified both original network constructions, 350 high-flow circulation instances, 441 exact physical perturbation pairs including zero and reversing flows, and 5,329 scalar pairs. All checks passed under normal and optimized Python. The investigating agent independently checked the reviewer-proposed Lipschitz cycle proof, including its zero-flow and sign-reversal cases.

The [investigation record](../notes/potential-flow-reopened-operating-constraints.md) records the development sequence and scope decisions.

## Reproduction

Run `python code/potential_flow_mpd/reopened_constraints_exact_checks.py` and repeat with `python -O`. Both use only the standard library. They verify the exact examples and scalar ingredients; they do not substitute for a mathematical review of the general perturbation bound.

The separate audit is reproduced with `python code/potential_flow_mpd/check_reopened_constraints_review.py`, also with `python -O`.
