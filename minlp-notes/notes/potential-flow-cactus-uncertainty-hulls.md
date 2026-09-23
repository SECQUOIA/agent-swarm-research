# Cactus uncertainty sets: an interval-hull candidate

Date: 2026-09-05. Status: the characterization and quantitative restoration passed [independent mathematical review](review-potential-flow-cactus-uncertainty-hulls.md). Retained as a supporting structural result; the [bounded source assessment](potential-flow-cactus-hulls-novelty.md) preserves the unresolved priority comparison with older nonlinear tolerance literature.

## Proposed statement

Consider a connected passive cactus, fixed balanced nominations, and strictly increasing continuous edge laws vanishing at zero. These assumptions guarantee a unique physical state for every balanced nomination. Indeed, the primitive of a law `g` satisfies `G(x)>=c(|x|-1)` for `|x|>=1`, where `c=min(g(1),-g(-1))>0`. The total energy is therefore coercive and strictly convex on the nonempty affine flow-conservation space. The laws need not be unbounded. Potentials are unique modulo a common additive constant. Every uncertain scalar parameter changes only one edge law affinely, and every law throughout the product of parameter intervals is admissible. Then any fixed terminal potential difference is separately monotone in each parameter: with all other parameters held fixed, it is either nondecreasing, nonincreasing, or constant throughout that parameter's interval. The direction may depend on the other parameters and on nominations. All scenarios refer to unrestricted passive physical states; no additional flow or potential bounds restrict the parameter or nomination set.

Consequently, its maximum and minimum over the full parameter box have a box-vertex optimizer. More generally, if each parameter belongs to an arbitrary compact scalar uncertainty set with the same attained minimum and maximum, the extreme values over the product set equal those over the interval hull. The conclusion persists after maximizing or minimizing jointly over any compact nomination set: choose a joint optimizer first, then move its parameter coordinates to endpoints while preserving its value. It does not assert that a maximum over nominations is itself separately monotone in the parameters.

This would make the cactus additive-pressure algorithms applicable to arbitrary independent finite or disconnected compact coefficient uncertainty sets given through their attained endpoints, provided the interval-hull laws remain admissible. It is not a network-design optimization theorem.

## Reasoning for smooth positive-derivative laws

Fix a parameter `theta` on edge `e`, whose law is `g_e(x,theta)=g_base(x)+theta f(x)`. The ordinary pressure adjoint on a cactus is zero off the unique objective-terminal block route. On a bridge of that route, its oriented unit current is fixed. On a cycle block of the route, both paths from the entrance to the exit carry strictly positive adjoint current in that direction. Thus the sign of the adjoint edge current is determined by the graph and objective terminals, independently of physical nominations and parameter values.

The pressure derivative is `dF/dtheta=j_h,e f(x_e)`. The sign of `f(x_e(theta))` cannot change as `theta` varies. Indeed, if it vanishes at any parameter value, the whole physical flow and potential vector at that value satisfy the physical equations for every other value of this parameter: the only changing constitutive term is zero. Uniqueness therefore makes that physical state constant throughout the parameter interval. Otherwise continuity prevents a sign change. It follows that `dF/dtheta` has one sign throughout the interval.

For several parameters on the same edge, this argument holds with the remaining ones fixed. A global optimizer can be moved one coordinate at a time to a suitable endpoint. Each move preserves global optimality; changing subsequent coordinates cannot undo this fact, even though separate monotonicity directions may change.

## Continuous-law extension

Use centered convolution and a positive linear term as in the affine-law investigation. Each smooth surrogate has the same affine one-edge parameter structure and admissible unique physical states. It is separately monotone for each fixed configuration of the other parameters. For a fixed parameter interval, choose a subsequence with the same monotonicity direction (there are only two weak directions); uniform convergence of its pressure objectives gives monotonicity of the original objective. The original constitutive family therefore inherits the statement. Exact derivative statements at nonsmooth points are unnecessary.

## Signed edge-flow extrema

For a target edge on a cycle, orient the cycle coherently and write every cycle flow as `q+c_e`, with fixed `c_e` determined by nominations. The scalar cycle equation is strictly increasing in `q`. Changing one parameter on an edge changes its left-hand side affinely by `theta f(q+c_e)`. At any zero of this basis value, the root is independent of the parameter; otherwise the root is monotone because implicit derivative has sign `-f(q+c_e)`. The same centered-smoothing argument covers zero derivatives and kinks. Target bridge flows are fixed by nominations. Thus edge-flow extremes also occur at coefficient-box vertices and agree with extremes over arbitrary product scalar sets having the same attained endpoints. Other cactus blocks do not affect the target block's flow once nominations are fixed.

## Limitations

This argument relies on the graph-fixed adjoint current signs of cactus blocks. More complicated biconnected blocks can change adjoint current signs as parameters vary, so bounded block cycle rank alone does not establish the same hull property. It also relies on one parameter affecting only one edge. A shared uncertain coefficient on several edges can have a derivative equal to a sum of differently signed terms, and the zero-basis preservation argument no longer applies directly. No claim is made for such coupling.

## Exact obstruction already at block cycle rank two

The hull property fails for a theta graph, even for one scalar resistance and fixed rational nominations. Use vertices `0,1,2,3`, oriented edges

```
0->2, 2->1, 0->3, 3->1, 2->3,
```

and quadratic resistances `(1/2,1/6,1/6,1/2,theta)`, respectively. Let nominations be `(4,-4,3,-3)`. For every `theta>0`, the positive cross flow `z` satisfies

```
(12 theta+1) z²+10z-23=0.
```

Its unique positive root lies in `(0,2)`. Set the other four flows, in the stated edge order, to

```
(z+1)/2, (7-z)/2, (7-z)/2, (z+1)/2.
```

These positive flows satisfy all four balances. Their pressure drops are consistent because the two 0-to-1 paths have the same sum, and the 2-to-3 potential difference is

```
[(7-z)²-3(z+1)²]/24 = (23-10z-z²)/12 = theta z².
```

Uniqueness of the passive physical flow therefore proves this explicit solution. Its objective-terminal span is

```
pi_0-pi_1 = [3(z+1)²+(7-z)²]/24
          = 2+(z-1)²/6.
```

The reverse objective `pi_1-pi_0` has its unique maximum `-2` at `theta=1`. For the two-point uncertainty set `{23/108,71/12}`, its cross flow is `3/2` or `1/2`; both give reverse objective `-49/24`. The interval hull includes `theta=1`, so replacing this discrete set by its hull strictly increases the worst pressure objective by `1/24`. The graph has one biconnected block of cycle rank two. This example also shows why a general bounded-rank resistance optimizer must allow interior parameter values; restricting all parameters to box endpoints would be incorrect.

The displayed identities were derived symbolically and checked by direct rational substitution. The [independent proof review](review-potential-flow-cactus-uncertainty-hulls.md) covers this obstruction and the characterization below; the [source assessment](potential-flow-cactus-hulls-novelty.md) retains the qualified priority claim.

## Further candidate: a complete graph characterization

For connected simple graphs, the preceding positive result and obstruction appear to prove the following equivalence:

1. The graph is a cactus.
2. For every positive quadratic-resistance instance with fixed balanced nominations and every pair of objective terminals, the pressure difference is separately monotone in each resistance.
3. For every such instance and every independent product of compact scalar resistance sets, pressure extrema agree with those over the interval hull.

The cactus implications were proved above. To prove the converse, use the elementary graph fact that a connected noncactus simple graph contains a theta subdivision: three internally disjoint paths between the same two branch vertices. At most one path has no internal vertex. Choose objective vertices `0,1` on two of the paths and label the branch vertices `2,3`. These two paths each split into two nonempty segments. Distribute the four gadget resistances `1/2,1/6,1/6,1/2` as positive rational sums across the corresponding segments, putting zero nominations at the extra degree-two vertices.

The third path represents the uncertain cross resistance. If it has more than one edge, assign its fixed edges a positive rational total `d<23/108` and let one remaining edge have resistance `theta` in `{23/108-d,71/12-d}` or its interval hull. Its total path resistance is then exactly one of the gadget values, and the interior choice `theta=1-d` is allowed. If the third path is a single edge, take `d=0`. Quadratic series resistances add because all internal nominations are zero. Thus the theta subgraph reproduces the explicit strict gap `1/24`.

Now restore every edge of the original graph outside this chosen theta subgraph, assigning it a common resistance `M>0`. Give every other vertex zero nomination. Fix one of the two endpoint parameter values or the interior parameter value. A feasible flow supported on the theta subgraph has an energy bounded independently of `M`. The unique minimum-energy physical flow consequently satisfies

```
(M/3)*sum_(outside theta) |x_e|^3 <= C,
```

so every extra-edge flow tends to zero as `M` tends to infinity. All physical flows are uniformly bounded by the total nomination magnitude. After normalizing a theta potential, its other theta potentials stay bounded because every theta edge has bounded positive resistance and bounded flow. Any convergent subsequence of theta flows and potentials satisfies, in the limit, the original theta balances and constitutive equations. Passive uniqueness identifies the limit with the explicit gadget state. Hence the three relevant terminal objective values converge to their gadget values.

For sufficiently large finite rational `M`, each objective discrepancy is less than `1/96`, preserving a strictly positive interior-versus-endpoint gap. The objective is therefore not monotone in its single uncertain resistance, and its two-point uncertainty set has a strictly smaller worst value than its interval hull. This proves failure of both (2) and (3) whenever the graph is not a cactus.

This is a structural existence proof. It does not give or need a polynomial bit bound on the chosen large resistance `M`. All constructed data can be chosen rational. The characterization has passed independent proof review; its source assessment retains the comparison limits noted above.

## Reproducible checks

[`cactus_uncertainty_hulls_checks.py`](../code/potential_flow_mpd/cactus_uncertainty_hulls_checks.py) verifies all three theta states with exact rational arithmetic. It also checks 18 cactus coefficient grids and 18 one-coordinate sweeps, with zero observed excess over corner extrema and zero monotonicity violations. Adding the missing edge of the theta graph with resistances `100`, `10000`, and `1000000` gives positive interior gaps approximately `0.03095`, `0.04056`, and `0.04156`, approaching the exact theta gap `1/24`. The numerical solves use the smooth law `beta*(x|x|+10^(-9)x)` to avoid a singular initial Newton Hessian; the exact rational identity checks use the original quadratic law. These tests support the mechanisms, while the original-law topology characterization rests on the proof.

Run with `/home/sgusev/miniconda3/envs/minlp-notes/bin/python code/potential_flow_mpd/cactus_uncertainty_hulls_checks.py`.

## Quantitative strengthening of the restoration step

The large-resistance construction can in fact use polynomially encoded integers. This additional bound passed the quantitative follow-up in the [independent review](review-potential-flow-cactus-uncertainty-hulls.md); the qualitative restoration proof above already proves the characterization.

Let `m` be the number of edges of the original graph. On the theta subdivision, the feasible flow corresponding to `z=1` has outer branch flows `1,3,3,1` and cross flow `1`. Its energy is `(10+tau)/3<6` for every one of the three relevant total cross resistances `tau in {23/108,1,71/12}`. Extend it by zero on all other edges. Hence every restored-network physical extra-edge flow satisfies

```
|x_e| <= (18/M)^(1/3).
```

The original nominations have total absolute magnitude `14`, so every physical edge flow is at most `14` in absolute value. Restrict a restored physical flow to the theta subgraph and call its induced theta nomination `b'`. At every theta vertex,

```
|b'_v| <= 14 deg_theta(v),
||b'-b||_1 <= 2 m_extra (18/M)^(1/3).
```

Both `b` and `b'` are balanced: outside vertices have zero nomination, so their aggregate conservation cancels the total extra-edge exchange with the theta vertices. The box `|b_v|<=14 deg_theta(v)` has total load bound `28 m_theta`. The quadratic nomination Lipschitz theorem applies on this box. Choose the 0-to-1 path through branch vertex 2, whose total theta resistance is `1/2+1/6=2/3`. Its pressure sensitivity constant is

```
C = 2*(28 m_theta)*(2/3) = (112/3) m_theta.
```

The restricted theta state is exactly the unique theta physical state for `b'`. Its terminal pressure discrepancy from the original theta state is therefore at most

```
(224/3) m_theta m_extra (18/M)^(1/3)
 <= 75 m² (18/M)^(1/3).
```

The explicit integer choice

```
M = 18*(10000*m²)^3
```

makes the discrepancy at most `75/10000<1/96`. Thus all added resistances have polynomial binary encoding length, and the theta-path resistance splits can be chosen rational with polynomial encoding as well. The topological obstruction can be constructed with polynomially many arithmetic operations and polynomially encoded data from a theta subdivision.

## Close literature distinction: linear differential-flow nondegeneracy

[Brandenberg and Stursberg (2025), Extremal Solutions for Network Flow with Differential Constraints](https://link.springer.com/article/10.1007/s10957-025-02792-4), Definitions 1.1–1.2, study linear DC constitutive equations with fixed elasticities and variable nomination/capacity bounds. Their Theorem 3.1 characterizes cactus graphs by universal nondegeneracy of an alpha-tree description of that polytope. Example 3.1 uses the balanced Wheatstone ratio, and Proposition 3.1 records the known cactus/diamond graph characterization. These graph and electrical ingredients must be credited. Their optimization property is different from fixed-nomination resistance uncertainty.

In fact, for linear laws the pressure hull property holds on **every** connected graph. Fix a positive conductance vector, vary one conductance from `t0` to `t`, and ground one vertex. If `a` is that edge's incidence column, `L(t)=L(t0)+(t-t0)aa^T`. Writing `u=e_s-e_t` in grounded coordinates, `r=a^T L(t0)^(-1)a`, and `U=u^T L(t0)^(-1)a`, `V=a^T L(t0)^(-1)b`, the rank-one inverse identity gives

```
F(t)=F(t0)-(t-t0)UV/[1+(t-t0)r].
```

The denominator is positive for all positive conductances in the interval, because the grounded Laplacian stays positive definite. Hence the derivative has the constant sign of `-UV`. Resistance is the reciprocal of conductance and preserves monotonicity up to reversing its direction. Repeating the endpoint argument gives the hull property on every graph for linear laws. This familiar rank-one sensitivity calculation therefore distinguishes the present nonlinear characterization from the 2025 linear-polytope characterization; it is not claimed as a new result itself.

## Constructive endpoint recovery for additive optimization

When the compact scalar uncertainty sets have rational attained endpoints, the existing cactus box algorithms also yield near-optimal inputs belonging to the original sets. Their first output may have interior parameters, so a recovery step is needed. Hold its rational nomination fixed, and move parameters to endpoints one at a time. For a maximization objective, separate monotonicity ensures that at least one of the two endpoint choices has value at least the current value. Evaluate those endpoint objectives within absolute error `delta` and select the larger estimate. The selected true value loses at most `2delta` relative to the better endpoint. With `N` parameters, total loss is at most `2N delta`. Set `delta` to an appropriate fraction of the requested tolerance divided by `N`.

Fixed-scenario objective evaluation to this precision is polynomial by the reviewed polynomial-law or fixed-fractional-law algorithms, and there are only `2N` evaluations. Every final parameter is one of the rational endpoints and thus belongs to its original compact set. The nomination remains feasible. The same argument minimizes an objective by selecting the smaller endpoint estimate. For exact polynomial-law edge-flow values, one may use exact algebraic comparisons instead. No efficient common-field pressure comparison is assumed.

A source audit also identified the classical origin of the adjoint sign topology: [Duffin, Topology of Series-Parallel Networks](https://sites.math.washington.edu/~reu/papers/current/jim/duffin.pdf), Theorem 0 (printed pages 306–307), characterizes resistance-independent current direction for confluent branches; Theorem 1 uses a Wheatstone obstruction. Adding the objective source branch relates this established result to graph-fixed adjoint current signs. The present candidate must not claim that sign topology as new. Its potential contribution is the nonlinear one-edge coefficient monotonicity, the uncertainty-set hull consequence, and the explicit fixed-quadratic converse construction.
