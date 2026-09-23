# Trees characterize universal weighted-potential uncertainty hulls

Date: 2026-09-05. Status: verified by two independent full mathematical audits; distinct publication priority remains qualified. The graph is finite, connected, and simple. This is a nonlinear passive-flow statement; no analogous boundary is claimed for fixed linear Ohmic laws.

## Characterization

For a finite connected simple graph `G`, the following are equivalent:

1. `G` is a tree.
2. For every fixed balanced nomination, every zero-sum linear potential objective `c^T pi`, and every positive quadratic-resistance box, the objective is separately monotone in every resistance coordinate.
3. For every such nomination and objective, independent nonempty compact positive resistance sets with attained endpoints have the same objective extrema as their interval hulls.

The negative direction already uses three fixed nomination values `(2,-3,1)`, three fixed objective coefficients `(-5,12,-7)`, one uncertain resistance, and positive rational data of polynomial encoding length. There are no additional physical flow or potential constraints on scenarios.

Simplicity is material. A two-vertex multigraph with parallel edges has every zero-sum potential objective proportional to one pairwise difference, so the tree characterization is not asserted for multigraphs with two-edge cycles. The result quantifies over the nonlinear quadratic law, not fixed linear Ohmic laws, for which separate linear-functional monotonicity has a different scope.

## 1. Positive direction on trees

With fixed nominations, conservation determines every tree-edge flow independently of resistance. Normalize one potential and express all other potentials by summing edge drops along the tree. Then every zero-sum weighted potential functional has the form

```
c^T pi=sum_e w_e beta_e x_e|x_e|,
```

where `w_e` is a fixed rational cut sum of objective coefficients when the data are rational. Thus the objective is affine in the independent resistances, with fixed coefficient signs. Separate monotonicity and exact endpoint-hull equality follow. This proves `1=>2=>3`.

## 2. A triangle obstruction

Use [the weighted-potential triangle](potential-flow-weighted-potential-cycle-hardness.md): edges `0->1` and `1->2` have resistance one, while `2->0` has resistance `theta`. The fixed nominations and objective are

```
b=(2,-3,1),
F=-5pi_0+12pi_1-7pi_2.
```

The physical flow is `(q+2,q-1,q)`, where `6q+3-theta q^2=0` and `-1/2<q<0`. Its objective is

```
F=-105/4-12(q+1/4)^2.
```

At `theta=24`, `q=-1/4` and `F=-105/4`. At the two resistance endpoints `theta=16/3` and `theta=144`, the roots are `-3/8` and `-1/8`, and both values equal `-423/16`. Thus the interval hull improves the maximum by exactly `3/16`, and separate monotonicity fails.

## 3. Subdivide onto any simple cycle

If `G` is not a tree, choose a simple cycle and any three distinct vertices on it. Regard the three connecting paths as subdivisions of the triangle edges. Distribute each fixed total resistance one equally over its path edges. On the uncertain path, if it has more than one edge, distribute total `d=8/3` equally over all but one edge and give the remaining edge resistance `theta-d`; if it has one edge, take `d=0`. At both uncertainty endpoints all edge resistances are positive. Assign the three fixed nominations and objective coefficients to the selected branch vertices and zero to the other cycle vertices.

Each internal path vertex has zero nomination, so its path flow is constant. The three effective resistances and objective values are exactly those of the triangle. These rational subdivision data have polynomial encoding length.

## 4. Restore the rest of the graph with an explicit gap

Give every edge outside the selected cycle the same positive integer resistance `R`, and give every additional vertex nomination and objective coefficient zero. Write `m=|E(G)|`.

For each of the three resistance settings, take the conservation-feasible cycle flow `q=-1/4` and zero on all extra edges. Its energy is

```
[(7/4)^3+(5/4)^3+theta(1/4)^3]/3
=(468+theta)/192 <=612/192<4.
```

The full physical minimizer therefore has every extra-edge flow bounded by

```
u=(12/R)^(1/3).
```

The fixed total positive nomination is three, so every full physical flow has magnitude at most three. Restrict the physical state to the selected cycle, inducing a nomination `b'` there. Each cycle vertex has degree two, hence `|b'_v|<=6`. Both `b'` and the original cycle nomination lie in the same balanced box with total absolute coordinate bound at most `6m`. Moreover,

```
||b'-b||_1<=2m u.
```

Use the fixed path of total resistance one for each of `pi_0-pi_1` and `pi_1-pi_2`. The reviewed quadratic nomination Lipschitz bound, together with

```
F=-5(pi_0-pi_1)+7(pi_1-pi_2),
```

gives

```
|F(b')-F(b)|
 <=(5+7)*2*(6m)*||b'-b||_1
 <=288m^2 u.
```

Set

```
R=12(10000m^2)^3.
```

Then the objective perturbation in each scenario is at most `288/10000<3/64`. The restored interior scenario therefore exceeds both endpoint scenarios by more than `3/16-2(3/64)=3/32`. All graph data have polynomial rational encoding length; only one resistance coordinate remains uncertain. Thus every non-tree simple graph violates properties 2 and 3, proving the contrapositive `3=>1`.

## Relation to other objective classes

The result fits the following objective-dependent structural comparison:

- arbitrary zero-sum weighted potential objectives: trees;
- every single pairwise potential difference: cacti, as in the [cactus characterization investigation](../notes/potential-flow-cactus-uncertainty-hulls.md);
- every prescribed arc flow: series-parallel graphs, by the [reviewed characterization](../results/potential-flow-series-parallel-arc-characterization.md).

The [one-cycle weighted-objective hardness candidate](potential-flow-weighted-potential-cycle-hardness.md) gives a separate computational consequence for discrete resistance choices. Its NP-hardness is not part of the present structural proof.

Classical circuit sensitivity and confluence mechanisms require credit. The [weighted-objective source audit](../notes/potential-flow-weighted-potential-cycle-novelty.md), [circuit hull source audit](../notes/potential-flow-cactus-hulls-novelty.md), and completed [focused hierarchy assessment](../notes/potential-flow-weighted-objective-hierarchy-novelty.md) record prior work and inaccessible older sources. The focused assessment found no directly matching full classification in the inspected primary literature; this is not exhaustive priority clearance. The explicit common-quadratic obstruction and quantified restoration are preserved as verified results with that qualification.

## Independent verification

Both [the first full audit](../notes/review-potential-flow-weighted-potential-tree-characterization-independent.md) and [the second full audit](../notes/review-potential-flow-weighted-tree-characterization-second.md) passed. The separate [second-review checker](../code/potential_flow_mpd/check_weighted_tree_characterization_second.py) passed 192 exact subdivided states, 144 subtraction-error controls, and 98 gap-constant checks. The audits checked universal quantifiers, exact triangle values, subdivision, induced nominations, uniform energy and Lipschitz bounds, and polynomial encoding.
