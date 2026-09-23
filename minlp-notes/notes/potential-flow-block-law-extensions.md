# Potential-flow extensions: constitutive laws and blocks beyond cacti

Date: 2026-09-05. Status: archived derivation superseded by the twice-reviewed [continuous polynomial-law theorem](../results/potential-flow-polynomial-law-uncertainty.md). That theorem includes both candidates below, permits growing dense degrees and piece counts, and replaces the small-block restriction by fixed block cycle rank. The historical derivation is retained for context; it is not an additional pending theorem. They extend the reviewed [quadratic cactus additive-optimization theorem](../results/potential-flow-cactus-additive-optimization.md). Nothing here claims exact threshold decision in polynomial bit time.

## Candidate A: fixed-degree piecewise polynomial edge laws

Fix a constant `d`. On a cactus, replace the quadratic law by edge-specific laws

```
pi_u-pi_v=phi_e(x_e),
```

where every `phi_e` is continuously differentiable, strictly increasing, satisfies `phi_e(0)=0`, and has at most `d` polynomial pieces, each of degree at most `d`, with rational coefficients and rational breakpoints. The outer pieces extend to infinity. All nomination bounds remain rational and finite, with a nonempty balanced box. Then the same polynomial-bit-time additive-optimum interval and rational epsilon-optimal nomination claims should hold. The polynomial's exponent may depend on fixed `d`.

This includes edge-dependent power laws `phi_e(x)=beta_e sign(x)|x|^{r_e}` for integer `1<=r_e<=d`. It does not cover arbitrary irrational or rational exponents merely by analogy: sums of fractional powers can require unbounded algebraic dimension under the present method.

### Proof changes

1. **Passive uniqueness and smoothing.** A strictly increasing continuous piecewise polynomial on the real line with finitely many pieces is unbounded above and below. Its primitive is strictly convex and coercive on the conservation affine space. Add `rho x` to its law. The original derivative is nonnegative everywhere because the law is differentiable and monotone; smoothing makes it positive. The electrical adjoint/KKT threshold proof is unchanged. The flow bound `|x_e|<=B=sum max(|l_v|,|u_v|)` follows from the acyclic physical-flow orientation, since `phi_e(0)=0` preserves the sign of each flow in its potential drop.

2. **Zero-smoothing limit.** The compact flow bound is uniform over all feasible nominations and all positive smoothing parameters, so one can pass to the limit by the same strictly convex-energy comparison argument. The polynomial face enumeration is therefore unchanged: two free aggregated loads at most, in one cycle.

3. **Fixed-block arithmetic.** A fixed-load cycle has one circulation parameter. Every edge flow is affine in it. The inverse images of all constitutive breakpoints give `O(dm)` rational breakpoints. On an interval, the loop equation is a strictly increasing polynomial of degree at most `d`, with rational coefficients. Isolate its unique root; the resulting fixed-block drop is algebraic of degree at most `d`. Algebraic approximation remains polynomial in coefficient size and precision bits for fixed `d`.

4. **Active-cycle arithmetic.** Edge flows are affine in the nomination parameter and circulation. Each constitutive breakpoint gives a line in this plane; there are `O(dm)` lines and polynomially many cells. On each cell the cycle law and objective are polynomials of degree at most `d` in two variables. Fixed-dimensional algebraic decision and sampling apply exactly as in the quadratic theorem.

5. **Rational nomination recovery.** A rational derivative bound on `[-B,B]` is available directly from the polynomial coefficients. For a piece `sum_j c_j x^j`, use `sum_{j>=1} j |c_j| max(1,B)^{j-1}`, and take the maximum over the finitely many pieces. Call the resulting bound `M_e`. The smoothed electrical derivative resistance is at most `M_e+rho`. Testing electrical energy with a unit flow along a fixed objective-terminal path gives

```
|F(b)-F(c)| <= (sum_{e in P} M_e) ||b-c||_1.
```

Its constant is rational and has polynomial bit length. The original rounding proof applies.

6. **Objective bounds.** Polynomial coefficient bounds also provide a rational upper bound on `|phi_e(x)|` for `|x|<=B`. Summing those over a simple path bounds the objective with polynomial encoding length, permitting the value binary search.

All nonlinear complexity remains at fixed degree and dimension. Increasing the number of polynomial pieces while keeping it polynomially encoded would still yield a polynomial arrangement size, but a precise more general statement is unnecessary here.

## Candidate B: a mixture of cycles and uniformly small non-cycle blocks

Fix positive integers `d,k`. Consider a connected graph in which every biconnected block is either a cycle of arbitrary length or has at most `k` edges. Use the laws of Candidate A and the same balanced interval-nomination model. The graph need not be a cactus. Then additive MPD optimization and rational nomination recovery should remain polynomial in input bit length and requested precision bits, with a polynomial exponent depending on `d,k`.

The bound is on the number of edges in a non-cycle block; merely bounding vertices would not bound a multigraph's algebraic dimension if it had unbounded parallel edges.

### Global one-block structure is not specific to cacti

After aggregating off-path components, the block-cut structure is still a series chain. In the smoothed electrical derivative network, the unit `s-t` current passes through every block. For a non-bridge block with entrance `a` and exit `c`, every internal harmonic potential lies strictly between `h_a` and `h_c`. The weak maximum principle gives the bounds. Equality at an internal node would propagate through its neighbors of the same extremal value; two-vertex-connectivity supplies a path to the opposite terminal avoiding the extremal terminal, giving a contradiction. The bridge case is immediate.

Thus consecutive blocks have ordered, nonoverlapping open ranges of `h`. The common multiplier leaves free loads in only one block, with all preceding core loads upper-saturated and all following loads lower-saturated. Smoothing and compactness preserve one of these finitely many closed faces. There are linearly many choices of the active block. This one-block lemma holds for every connected graph, although it is algorithmically useful only when each possible active block admits a tractable local reduction.

### Local algorithms

If the active block is a cycle, use Candidate A's two-pivot refinement and two-variable optimization.

If it has at most `k` edges, it has at most `k+1` vertices. Leave every nomination in the block free, except for its fixed total balance. Keep local flows and normalized local potentials as explicit variables. There are `O(k)` real variables. Enumerating the constitutive pieces gives at most `d^k` cases, a constant for fixed `d,k`. In each case, conservation, nomination bounds, potential laws, and the objective threshold form a constant-dimensional polynomial system of degree at most `d`, with polynomial-size rational coefficients. Fixed-dimensional real algebraic decision and sampling yield the required local optimum interval and algebraic nomination.

Every inactive block has fixed effective nominations. A cycle is handled as in Candidate A; a block with at most `k` edges is a constant-dimensional polynomial physical-flow system, with a unique normalized solution. Real algebraic sampling produces that solution with bounded degree (depending on `d,k`) and polynomial coefficient bit length. Approximate its objective-terminal drop to the required precision before summation. No exact sum comparison is needed.

### Rational recovery for several free loads

The selected small-block face is a rational box intersected with a single rational balance equation. Suppose the algebraic sampler returns nominations `b*`. Refine an isolating interval for each coordinate to a rational interval of width at most `eta`. Intersect these intervals with the original rational box and the exact balance hyperplane. The resulting rational polytope is nonempty because it contains `b*`; linear programming produces a rational point inside it with polynomial bit length. Its l1 distance from `b*` is at most `(k+1)eta`. Choosing `eta` from the rational global Lipschitz bound controls objective loss. Original-group interval disaggregation remains rational and exact.

## Fixed cycle rank: initial obstruction and later candidate resolution

Bounding the cycle rank rather than the number of edges would be a stronger extension. Suppressing degree-two vertices gives a small topological core, but their internal nominations cannot simply be suppressed: they remain optimization variables. Along a maximal degree-two path, the electrical sensitivity is monotone when its endpoint sensitivity values differ. If both endpoints equal the common multiplier, however, the whole path can have the same sensitivity, leaving many free nominations. A proof must deal with these flat sensitivity paths without assuming generic resistances or generic optimizers. This note does not claim a fixed-cycle-rank theorem. A subsequent [separate candidate](potential-flow-block-cycle-rank-investigation.md) resolves the flat-path obstruction by adding small positive adjoint sources through an objective perturbation; its own proof reviews and novelty assessment determine its status.
