# A quadratic obstruction to arc uncertainty hulls on every non-series-parallel graph

Date: 2026-09-05. Status: theorem passed two independent full audits, including the quantitative polynomial-encoding restoration. The positive direction uses classical electrical confluence theory. The candidate contribution is the explicit common-quadratic, one-uncertain-resistance obstruction on every non-series-parallel graph and the resulting universal characterization; broad nonlinear tolerance priority remains qualified below.

## Characterization theorem

For a finite connected simple graph `G`, the following are equivalent:

1. `G` has no `K4` minor.
2. For every fixed balanced nomination, every positive quadratic-resistance interval family, every target edge, and every resistance coordinate, target flow is monotone in that coordinate with all others fixed.
3. For every such fixed nomination and independently chosen compact resistance sets with attained endpoints, the target-flow extrema equal their interval-hull extrema.

The physical scenarios are unconstrained passive states: there are no additional flow or potential side constraints. The negative direction already uses rational data, one uncertain resistance with a two-point set, and the common law `beta x|x|`.

The [reviewed positive theorem](../results/potential-flow-series-parallel-arc-validation.md) proves `1=>2=>3`. It remains to prove `3=>1` by contrapositive.

## 1. Four-node quadratic theta

Take vertices `0,1,2,3`, nominations `(4,-4,3,-3)`, and oriented edges

```
0->2: beta=1/2,
2->1: beta=1/6,
0->3: beta=1/6,
3->1: beta=1/2,
2->3: beta=theta.
```

The cross flow `q` is the unique positive root of

```
(12 theta+1)q^2+10q-23=0.
```

The other flows, in the order above, are `(q+1)/2,(7-q)/2,(7-q)/2,(q+1)/2`. Direct substitution in conservation and pressure equations gives

```
F_theta(0)=pi_1-pi_0=-2-(q-1)^2/6.
```

At `theta=1`, `q=1` and `F=-2`. At the resistance endpoints `theta_L=23/108` and `theta_U=71/12`, the flows are `q=3/2` and `q=1/2`, respectively, and both reverse pressures equal `-49/24`. Thus the original reverse pressure has an interior advantage of `1/24`.

## 2. Probe arc producing exactly K4

Add the target arc `a=(1,0)` with fixed resistance `M=10^8`. The complete graph is now exactly `K4`, and its nominations remain the same four fixed integers.

For a prospective target flow `t`, the flow on the old theta graph has nominations

```
b(t)=b+t e_0-t e_1.
```

Let `F_theta(t)` be its reverse pressure `pi_1-pi_0`. Strict monotonicity of the passive energy gives that `F_theta(t)` is strictly decreasing in `t`. Indeed, for distinct `s,t`, the constitutive monotonicity identity has right side strictly positive and left side

```
(b(t)-b(s)) dot (pi(t)-pi(s))
 = -(t-s)(F_theta(t)-F_theta(s)).
```

The complete physical state satisfies

```
F_theta(t)=M t|t|.
```

For each of the three specified resistance values, `F_theta(0)<0`; hence the unique solution has `t<0`, and

```
F_theta(0)<F_theta(t)<0,
M t^2=-F_theta(t)<-F_theta(0)<=49/24<4.
```

Therefore `|t|<2/sqrt(M)<1`. Throughout this range, use the conservative nomination-box absolute bound `B=18`. A fixed path from `1` to `0` through vertex `2` has resistance sum `2/3`. The reviewed quadratic nomination Lipschitz bound gives

```
|F_theta(t)-F_theta(0)|
 <= [2 B (2/3)] ||b(t)-b||_1
 =48|t|
 <96/sqrt(M)
 =96/10000
 <1/96.
```

At the interior resistance, the new reverse pressure is greater than `-2`. At either endpoint it is less than

```
-49/24+1/96=-65/32.
```

The target constitutive relation has the same fixed `M` in every scenario, and its inverse is strictly increasing. Thus the target flow at `theta=1` is strictly greater than at both interval endpoints. The two-point resistance uncertainty set and its interval hull have different maximum target flows. Separate monotonicity fails as well.

## 3. Subdivision and restoration

Every graph containing a `K4` minor contains a subdivision of `K4` ([Diestel, Proposition 1.7.2(ii), printed page 18](https://www.prip.tuwien.ac.at/twist/docs/graph_theory_book_diestel.pdf)): because `K4` has maximum degree three, its minor branch sets can be reduced to paths meeting at one branch vertex for each degree-three node. The corresponding subdivision has six internally disjoint branch paths.

Realize the four fixed theta edges and the probe edge by distributing each original positive resistance into positive rational series resistances along its branch path; assign zero nomination to every internal vertex. On the uncertain cross path, distribute a fixed total rational resistance `d` with `0<d<23/108` among all edges except one, and let the remaining edge have resistance `theta-d`. If the cross path has one edge, use `d=0`. All uncertain endpoints remain positive. The effective path resistance is exactly `theta`, so the same three physical states and strict target-flow gap are preserved. Choose any actual edge of the subdivided probe path as the target; its flow equals the original probe flow.

Now place this subdivision inside the full graph. Give every extra edge a common positive integer resistance `R`, give every extra vertex zero nomination, and keep the subdivision resistances fixed. For any of the three resistance scenarios, the old subdivision state extended by zero extra-edge flows is feasible for conservation and has a finite energy bound independent of `R`. The minimizing complete state therefore has every extra-edge flow bounded by `O(R^(-1/3))`. All flows are also bounded by the fixed total positive nomination. Along the connected subdivision, potentials modulo one reference value remain bounded because its fixed resistance coefficients and flows are bounded.

Every subsequential limit restricted to the subdivision consequently satisfies its original conservation and constitutive equations. Uniqueness identifies the limit as the corresponding subdivision physical state. In particular, the chosen target-edge flow converges in each of the three scenarios. Their original gap is strictly positive, so one sufficiently large integer `R` preserves both strict comparisons simultaneously. This constructs rational positive data on every non-series-parallel graph violating properties 2 and 3.

This qualitative restoration establishes existence of a rational counterexample on each fixed graph. It does not claim a uniform polynomial-size construction for the restoration resistance; such an encoding bound is unnecessary for the graph characterization.

## Sources and required verification

The graph-current sign mechanism is classical [Duffin confluence theory](https://sites.math.washington.edu/~reu/papers/current/jim/duffin.pdf). The adjacent-terminal positive theorem uses [Eppstein's Lemma 9](https://www.ics.uci.edu/~eppstein/pubs/Epp-IC-92.pdf). The quadratic theta identities were independently checked in the prior [discrete-resistance hardness result](../results/potential-flow-discrete-resistance-hardness.md). The newly oriented probe comparison and full characterization passed both independent reviews linked below. Broad nonlinear tolerance novelty remains qualified by the [unread Hasler–Wang source](../notes/potential-flow-cactus-hulls-novelty.md).

## Reproducible obstruction check

[`series_parallel_arc_obstruction_checks.py`](../code/potential_flow_mpd/series_parallel_arc_obstruction_checks.py) independently solves the complete four-node `K4` physical equations at 80-digit precision for all three resistance settings. It checks conservation, cycle pressure, probe pressure, monotone perturbation, and the strict endpoint gaps. The interior target flow exceeds both endpoint flows by at least `1.46520940187454e-6`; its pressure advantage is at least `0.0416555988671`. The script uses the original unsmoothed quadratic law and verifies equation residuals below `1e-70`.

## 4. Optional quantitative restoration with polynomially encoded data

The restoration can also be made explicit. The pressure comparison above gives a drop advantage greater than `1/32`. Every probe flow has magnitude less than `2/sqrt(M)`. For the interior probe flow `t_I` and either endpoint flow `t_E`, both negative,

```
F_I-F_E=M(t_I-t_E)(|t_I|+|t_E|),
t_I-t_E > 1/(128 sqrt(M)) =: g = 1/1280000.
```

This gap is preserved exactly under the series subdivisions before extra edges are restored. Let `m` be the total number of edges in the final graph. Distribute fixed branch-path resistances equally among their edges, and take `d=theta_L/2` when the uncertain cross path has more than one edge; these subdivision data have polynomial rational encoding length.

For each of the three cross resistances, the theta feasible flow with `q=1`, zero probe flow, and zero extra-edge flows has energy `(10+theta)/3<6`. This is a conservation-feasible comparison point, not necessarily a physical state. The complete physical minimum therefore has every extra-edge flow bounded by

```
u=(18/R)^(1/3).
```

The original total positive nomination is seven, so every full physical edge flow has magnitude at most seven. Its restriction to the subdivision induces nominations `b'` satisfying `|b'_v|<=7 deg_H(v)`, where `H` is the subdivision. Thus the original and induced nominations belong to the same balanced box with total absolute coordinate bound at most `14m`, and

```
||b'-b||_1<=2m u.
```

For the chosen target edge with fixed resistance `beta_a`, the single-edge path nomination Lipschitz bound controls its endpoint pressure change by `2(14m) beta_a ||b'-b||_1`. Applying the quadratic inverse inequality to its two target flows cancels the resistance:

```
|x'_a-x_a|^2
 <= (2/beta_a)|Delta(pi_tail-pi_head)|
 <= 56m ||b'-b||_1
 <=112m^2 u.
```

Choose the positive integer

```
R=18 (2000 m^2/g^2)^3.
```

Because `1/g=1280000` is an integer, this value is integral. It gives `|x'_a-x_a|<g/4` in each of the three scenarios. The restored interior target flow therefore exceeds both endpoint flows by more than `g/2`. The resistance `R` has polynomial binary encoding length, as do all the other constructed data. This strengthens the qualitative construction to a polynomially encoded counterexample on every non-series-parallel graph, with an explicit rational flow gap.

Both independent full audits checked this quantitative addendum, including the induced subdivision nominations, actual target-edge inverse estimate, and polynomial encoding.

## Independent verification and novelty scope

Both full reviews passed: [first independent audit](../notes/review-potential-flow-series-parallel-arc-characterization-independent.md) and [second audit](../notes/review-potential-flow-series-parallel-arc-characterization-second.md). They checked the complete iff statement, the negative probe orientation, all constants, the subcubic-minor subdivision theorem, state convergence, quantitative restoration, and the 80-digit obstruction checks.

The [focused circuit source audit](../notes/potential-flow-series-parallel-envelope-novelty.md) credits Duffin and related nonlinear tolerance work and records inaccessible directly relevant older papers. Thus the positive sign mechanism is not claimed new, and the broad positive hull property may overlap old circuit theory. The narrower candidate contribution is necessity with a fixed common quadratic law, one uncertain resistance, fixed small integer nominations, and a polynomially encoded positive flow gap on every graph outside the class. This qualified novelty position does not change the mathematical characterization.

The [exact fixed-rank validation theorem](potential-flow-series-parallel-arc-validation.md) and [fixed-nomination arbitrary-rank additive envelope algorithm](potential-flow-series-parallel-envelope-optimization.md) give separate computational consequences. The present graph characterization does not itself establish their complexity claims.
