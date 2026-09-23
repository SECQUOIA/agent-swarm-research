# One-cycle discrete resistance hardness for a fixed weighted potential objective

Date: 2026-09-05. Status: mathematically verified by two independent full audits; the bounded source audit found no matching restricted theorem. Novelty remains qualified below. This concerns a weighted linear potential functional, not a single pairwise pressure difference or an arc flow. Classical circuit optimization and confluence results require explicit credit.

## Computational theorem

Under the common quadratic passive law `pi_u-pi_v=beta_e x_e|x_e|`, optimizing a fixed weighted potential functional is NP-hard even on a single simple cycle, with fixed small integer nominations and independent two-point resistance choices. Only three distinguished vertices have nonzero nomination and objective coefficients; these are always

```
b=(2,-3,1),   c=(-5,12,-7),   F=c^T pi.
```

All other coefficients are zero. The objective is well defined modulo a potential constant because `sum c=0`. The exact threshold problem on this fixed-nomination one-cycle class is NP-complete, and robust satisfaction of a rational weighted-performance upper bound is coNP-complete. Positive integer resistances suffice after common scaling.

There is a positive rational gap of polynomial binary length. Thus a polynomial algorithm in input size and requested accuracy bits for the discrete weighted-potential maximum would imply `P=NP`. A further common resistance scaling also makes absolute-error-one value approximation NP-hard on the unnormalized integer-data class. This does not imply strong hardness or a relative-error approximation obstruction.

For comparison, independent positive resistance intervals admit exact polynomial-bit optimization of any rational weighted potential functional with fixed nominations and fixed global cycle rank. On trees, finite resistance choices also give exact polynomial optimization. These positive statements do not assert analogous tractability for uncertain nomination boxes.

All scenarios are unconstrained passive physical states. No separate physical pressure or flow feasibility constraints filter the uncertainty domain.

## 1. A triangle with an interior maximum

Orient a triangle as `0->1`, `1->2`, `2->0`. The first two resistances equal one; the last is `theta>0`. With nominations `(2,-3,1)`, every conserved flow has the form

```
x_01=q+2,   x_12=q-1,   x_20=q.
```

Its physical circulation is the unique root with `-1/2<q<0` of

```
6q+3-theta q^2=0,
q=-6/[6+sqrt(36+12theta)].
```

Indeed, in this interval the first edge flow is positive and the other two are negative. The sum of directed pressure drops is `(q+2)^2-(q-1)^2-theta q^2`. At `q=-1/2` it is negative, and at zero it is positive; strict increase of all scalar laws gives the unique physical root.

For the fixed coefficients `c=(-5,12,-7)`,

```
F=-5(pi_0-pi_1)+7(pi_1-pi_2)
 =-5(q+2)^2-7(q-1)^2
 =-105/4-12(q+1/4)^2.                       (1)
```

Thus `F<=-105/4`, with equality exactly at `q=-1/4`, equivalently `theta=24`. The interval endpoints

```
theta_L=16/3,   theta_U=144
```

give `q=-3/8,-1/8`, respectively, and both values are `-423/16`. The interior advantage is exactly `3/16`. This single-coordinate example already shows that pairwise-pressure hull results on cacti do not extend to arbitrary linear potential functionals.

## 2. Subset-Sum encoded by a series path

Take positive binary integers `a_1,...,a_n,K`, write `S=sum a_i`, and preprocess trivial `K>S` instances. Replace the uncertain edge `2->0` by a path of `n` edges. Its internal vertices have nomination and objective coefficient zero. Give edge `i` the independent options

```
beta_i in {12/n, 12/n+12a_i/K}.
```

Its effective resistance is

```
theta=12+(12/K)sum_i a_i sigma_i,
sigma_i in {0,1}.
```

All flows on the path equal `q`, and the resulting graph is still one simple cycle of maximum degree two. Formula (1) is unchanged. Therefore

```
max_sigma F>=-105/4
 iff some sigma has theta=24
 iff sum_i a_i sigma_i=K.
```

The graph and all rational data have polynomial binary encoding length. Fixed trivial yes/no outputs can use the original triangle with `theta=24` or `theta=12`, respectively, and the same objective threshold; both already have integer resistances.

## 3. Explicit no-instance gap and integer scaling

If no target subset exists, then `|theta-24|>=12/K`. Subtract the circulation equation evaluated at `q` and `q_0=-1/4` to obtain

```
|q+1/4|=|theta-24|/[16(6+theta(1/4-q))].
```

Since `-1/2<q<0` and `theta<=12+12S/K`,

```
16(6+theta(1/4-q))<240+144S/K,
|q+1/4|>=1/(20K+12S).
```

Consequently every no-instance resistance choice satisfies

```
F<=-105/4-Delta,
Delta=12/(20K+12S)^2=3/[4(5K+3S)^2].         (2)
```

Take a rational weighted-performance limit `J=-105/4-Delta/2`. A scenario with `F>J` exists exactly in the yes case. Robust satisfaction `F<=J` for every choice therefore corresponds to a no Subset-Sum instance. An additive maximum-value estimate with error less than `Delta/4` separates these cases. A sufficiently accurate discrete resistance witness also reveals an exact target subset in yes instances, which can be checked with integer arithmetic.

Multiplying every resistance by `4nK` makes the first two resistances `4nK` and path options

```
{48K, 48K+48n a_i}.
```

All potentials and objective values scale by `4nK`, while flows and nominations do not change. The equality threshold becomes the integer `-105nK`. The scaled gap and robust threshold are rational of polynomial binary encoding length. This proves the integer-resistance version without changing the graph class or the fixed objective coefficients.

There is also a fixed absolute-accuracy consequence. Multiply all these integer resistances once more by `T=(5K+3S)^2`. The peak becomes the integer `-105nK T`, and the no-instance gap becomes

```
(4nK) T Delta=3nK>=3.
```

An estimate with absolute error at most one separates yes and no maxima by comparison with the peak minus `3/2`. The added scaling has polynomial binary encoding length and preserves the same fixed nominations, fixed objective coefficients, and simple cycle. Thus absolute-error-one value approximation is NP-hard on this unnormalized input class. The numerical resistance magnitudes can be large; this does not prove strong hardness, hardness under normalized coefficients or objective ranges, or relative-error hardness.

## 4. NP/coNP membership on the one-cycle class

For a fixed positive rational resistance choice and fixed rational nominations on a cycle, choose a rational particular conserved flow and parameterize every edge flow by one scalar circulation `q`. Cycle conservation of potential is a strictly increasing scalar equation

```
sum_e beta_e (q+d_e)|q+d_e|=0,
```

after orienting the cycle consistently. Its breakpoints `-d_e` are rational. On every interval between consecutive breakpoints, the left side is a rational polynomial of degree at most two. The unique root can therefore be found and encoded exactly in polynomial bit time by sorting breakpoints, rational endpoint comparisons, and at most one quadratic root computation. A linear piece or a root at a breakpoint is handled directly. Potentials along cycle paths and any rational weighted potential objective then belong to that same degree-at-most-two algebraic field and can be compared with a rational threshold exactly in polynomial time.

Guessing one explicitly listed resistance option per edge is a polynomial-size certificate. The preceding exact evaluation verifies either a weak target threshold or a strict upper-bound violation in polynomial time. This proves NP membership for the existential versions and coNP membership for robust upper-bound satisfaction. Combined with the reduction, the stated restricted problems are NP/coNP-complete.

## 5. Positive continuous-box companion

Fix rational nominations and a rational zero-sum objective vector `c`, and let the global cycle rank be a fixed integer `r`. A spanning-tree parameterization expresses every flow as a rational affine function of `r` circulations `z`. On each of the polynomially many flow-sign cells, all edge pressure drops are `beta_e` times a quadratic polynomial in `z`.

There are `r` cycle equations. Expressing potentials along a fixed spanning tree writes the objective as another sum

```
F(z,beta)=sum_e w_e beta_e p_e(z),
```

with rational weights `w_e` and quadratic `p_e`. Thus the physical equations and objective are a fixed number of polynomial aggregate constraints in the fixed-dimensional circulation core, with each independent resistance interval a scalar polyhedral leaf. The reviewed [fixed-core block-polyhedral theorem](../results/fixed-core-block-polyhedral-optimization.md) computes the exact optimum and an algebraic witness in polynomial bit time. Add one core objective coordinate if required by that theorem's formulation. All candidates share only a fixed number of core variables; interval resistances are the permitted scalar leaves.

For compact bounds in the fixed-core formulation, restrict circulation coordinates to the passive flow bound `B=sum |b_v|` and bound the objective by a rational path estimate such as `B^2 ||c||_1 sum_e beta_e^upper`. Every physical state satisfies these polynomially encoded bounds; handle `B=0` directly.

In particular, the single-cycle continuous-interval version is exact polynomial time, whereas its independent two-point version is NP-hard. On a tree, fixed nominations determine every edge flow, so `c^T pi` is a linear function of the independent resistance coefficients. Choosing the appropriate endpoint on every edge solves the finite-set version exactly. Hence one cycle is the first possible cycle rank for the discrete weighted-potential obstruction.

This argument uses fixed nominations. It does not import the nomination-face theorem for a pairwise potential objective into an arbitrary weighted objective.

## Sources and novelty limits

The positive continuous-box argument applies the existing [fixed-core theorem](../results/fixed-core-block-polyhedral-optimization.md); the passive energy and series-law reduction are established ingredients. General circuit-extremum hardness and nonlinear tolerance analysis are prior topics; [the circuit source audit](../notes/potential-flow-series-parallel-envelope-novelty.md) records directly relevant inaccessible older sources. The proposed narrower contribution is the single simple cycle, fixed coefficients `b=(2,-3,1)` and `c=(-5,12,-7)`, independent two-point choices, and precise interval-versus-discrete boundary. The [focused weighted-objective source audit](../notes/potential-flow-weighted-potential-cycle-novelty.md) found no equivalent precise one-cycle theorem, while retaining the older circuit-literature caveats. This bounded search does not establish exhaustive novelty.

## Reproducible reduction checks

[`weighted_potential_cycle_hardness_checks.py`](../code/potential_flow_mpd/weighted_potential_cycle_hardness_checks.py) verified three symbolic identities, the three exact rational triangle states, and 1,776 resistance scenarios across 44 single-cycle instances at 90-digit precision. The checks covered 68 exact target subsets, every conservation equation, cycle pressure, weak target equality, strict robust-limit direction, the rational no-case gap, degree-two cycle topology, and integer scaling. All passed; the largest cycle pressure residual was `1.77e-90`. These are reduction checks, not an exhaustive literature comparison or a replacement for the complexity proof.

## Independent verification

Both [the first full audit](../notes/review-potential-flow-weighted-potential-cycle-hardness-independent.md) and [the second full audit](../notes/review-potential-flow-weighted-potential-cycle-hardness-second.md) passed. They checked the reduction, strict and weak thresholds, gap and integer scaling, exact one-cycle membership, and the continuous-box companion. Both identified and verified the fixed absolute-error scaling consequence now included above.
