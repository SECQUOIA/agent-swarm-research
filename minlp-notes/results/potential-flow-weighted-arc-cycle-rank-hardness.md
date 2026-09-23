# Two cycles suffice for discrete hardness of a fixed linear arc-flow objective

Date: 2026-09-05. Status: verified by two independent full mathematical audits; the bounded source search found no matching fixed-rank theorem. This concerns a linear functional of two arc flows, distinct from a weighted potential functional and from one designated arc flow.

## Theorem

Under the common quadratic laws `pi_u-pi_v=beta_e x_e|x_e|`, maximizing a fixed linear arc-flow objective is NP-hard on connected simple graphs of global cycle rank two and maximum degree three, with fixed small balanced nominations and independent two-point positive resistance choices on each uncertain edge. The four outer resistances in the construction are fixed. The nominations and two objective coefficients are always

```
b=(4,-4,3,-3),   F=-9 x_02+5 x_23,
```

with zeros at subdivision vertices. Positive integer resistances suffice. Exact threshold attainment is NP-complete, and robust satisfaction of a rational upper limit is coNP-complete on the fixed-global-rank-two class with fixed rational nominations and explicitly listed resistance options.

There is a positive no-instance gap of polynomial binary length, ruling out polynomial-time dependence on input size and accuracy bits unless `P=NP`. A separate nomination scaling gives absolute-error-one hardness on an unnormalized class; it no longer keeps the nomination values small. No strong or relative-approximation hardness is claimed.

For fixed nominations and global rank at most one, any linear arc-flow objective admits exact polynomial-time optimization over independent finite resistance sets. Thus rank two is the first possible hardness rank for this objective class. At any fixed global rank, independent continuous resistance intervals give exact algebraic optimization for fixed nominations by the fixed-core theorem. All physical scenarios are unconstrained passive states; no operating bounds filter them.

## 1. A theta network with a concave arc-flow performance curve

Take edges

```
0->2: beta=1,   2->1: beta=1,
0->3: beta=1,   3->1: beta=2,
2->3: beta=theta>0.
```

Write `x_02=a`, `x_23=q`. Conservation at the four vertices gives the other flows

```
x_21=a+3-q,   x_03=4-a,   x_31=1-a+q.
```

Equality of the two outer source-to-sink pressure drops is

```
a^2+(a+3-q)^2=(4-a)^2+2(1-a+q)^2,
```

whose relevant branch is

```
a(q)=q+9-2 sqrt(2q+18).                          (1)
```

For every `0<=q<=3`, all four outer flows in (1) are strictly positive. Indeed, `a` increases from `9-6sqrt(2)>0` to `12-4sqrt(6)<4`, while `a+3-q=12-2sqrt(2q+18)>0` and `1-a+q=2sqrt(2q+18)-8>0` throughout that interval.

The cross-edge pressure law is

```
theta q^2=pi_2-pi_3=(4-a)^2-a^2=16-8a(q).       (2)
```

The left side minus the right side is strictly increasing on `[0,3]`, since `a'(q)=1-2/sqrt(2q+18)>0`. It is negative at zero and positive at three. Thus (2) has exactly one root with `0<q<3`. The associated positive flows satisfy all balances and both independent cycle equations, so they are the unique passive physical state.

Let `u=sqrt(2q+18)`. The fixed linear flow objective becomes

```
F=-9a+5q=18u-4q-81
 =-9/2-2(u-9/2)^2.                              (3)
```

Therefore `F<=-9/2`, with equality exactly at

```
u*=9/2,   q*=a*=9/8,   theta*=448/81.            (4)
```

A useful rational endpoint pair is

```
theta_L=1792/5329: q=73/32, a=57/32, u=19/4,
theta_U=12032:    q=1/32,  a=17/32, u=17/4.
```

Both endpoint objective values equal `-37/8`; the interior value at (4) is `-9/2`, an advantage of `1/8`.

## 2. Subset-Sum on the cross path

Take positive binary integers `a_1,...,a_n,K` and let `S=sum a_i`. Preprocess trivial `K>S` instances. Replace edge `2->3` by an `n`-edge path with zero internal nominations. On its edge `i`, allow

```
beta_i in {224/(81n), 224/(81n)+224 a_i/(81K)}.
```

All path flows are equal to `q`; use its first edge as the second arc in the objective. The effective cross resistance is

```
theta=(224/81)(1+sum_i a_i sigma_i/K).
```

It equals `theta*=448/81` exactly when the selected subset sums to `K`. Thus

```
max_sigma F>=-9/2  iff  sum_i a_i sigma_i=K for some sigma.
```

The graph remains simple, has global cycle rank two and maximum degree three, and has only the original four nonzero nominations. Fixed trivial yes/no outputs can use the original theta with `theta=448/81` or `theta=224/81`; integer scaling is described below.

## 3. A rational no-instance gap

When no target subset exists,

```
|theta-theta*|>=224/(81K)>2/K,
theta<=3(1+S/K).
```

Subtract equation (2) at the physical point and at (4):

```
(theta-theta*) (q*)^2
 =-(q-q*)[theta(q+q*)+8(a(q)-a*)/(q-q*)].        (5)
```

At `q=q*`, equation (5) implies `theta=theta*`, so this case does not occur in a no instance. On `[0,3]`, `0<a'(q)<1`; hence the secant slope in (5) lies in `(0,1)`. Also `q+q*<5` and `(q*)^2>1`. Writing `H=23K+15S`, we obtain

```
|q-q*| > (2/K)/(5theta+8) >= 2/H.
```

Both `u=sqrt(2q+18)` and `u*=9/2` sum to less than ten, so

```
|u-u*|=2|q-q*|/(u+u*) > |q-q*|/5 > 2/(5H).
```

Consequently every no-instance choice satisfies

```
F<-9/2-8/(25H^2) <= -9/2-Delta,
Delta=1/(4H^2).                                 (6)
```

The threshold `J=-9/2-Delta/2` has a strict violation exactly for yes Subset-Sum instances. An additive value estimate with error less than `Delta/4` separates the cases. A sufficiently accurate discrete resistance witness also reveals a target subset on yes instances, which can be verified by integer arithmetic.

Multiply every resistance by `81nK`. The four outer resistances become `(81nK,81nK,81nK,162nK)`, and path options become

```
{224K,224K+224n a_i}.
```

These are positive integers of polynomial binary length. Common resistance scaling changes potentials but leaves every flow, the objective threshold, and gap (6) unchanged. The literal trivial yes/no outputs can similarly be scaled by 81 to obtain integer data.

For a separate absolute-error statement, multiply all nominations by `N=16H^2`. Quadratic homogeneity makes every flow and this linear flow objective scale by `N`, with resistances unchanged. The gap becomes at least four. An estimate with absolute error at most one separates the cases by comparison with the scaled peak minus two. The objective coefficients remain `(-9,5)`, but nominations now grow with the instance. This is unnormalized weak hardness, not a fixed-small-nomination constant-error claim.

## 4. Exact membership and the positive boundary

For any fixed global cycle rank `r`, fixed rational nominations, and fixed rational resistances, all flows can be expressed by `r` circulation coordinates. On a polynomial number of sign cells, cycle equations and any linear flow objective have rational polynomial descriptions in these fixed variables. Exact real-algebraic optimization therefore evaluates the physical weighted flow objective in polynomial bit time. Equivalently, apply the [reviewed fixed-core theorem](../results/fixed-core-block-polyhedral-optimization.md) with point resistance intervals. This gives a deterministic verifier after guessing one explicitly listed resistance option per edge. Thus existential weak-threshold attainment and strict upper-limit violation belong to NP, and robust upper limits belong to coNP on the fixed-global-rank class. The reduction proves the stated rank-two completeness results.

For global rank one, all nonzero cycle freedom is one scalar circulation `q`; bridge flows are fixed. Every weighted arc-flow objective is therefore `Aq+C` for rational constants `A,C`. If `A=0`, it is constant. Otherwise its maximization or minimization is exactly a single cycle-arc flow extremum, possibly with reversed orientation. There is also a direct scalar algorithm. Define `H_min(q)=sum_e min_{beta_e in options} beta_e(q+d_e)|q+d_e|`. Each summand is continuous and strictly increasing, so the unique zero of `H_min` is the largest attainable circulation: every original cycle function lies above it, and edgewise endpoint choices attaining its terms at that zero realize equality. Using pointwise maxima instead gives the smallest circulation. Sorting the rational breakpoints `-d_e` leaves rational quadratic equations on every interval; solve the unique relevant root exactly. This yields polynomial bit complexity and an exact endpoint scenario. It agrees with the [reviewed finite-resistance arc theorem](../results/potential-flow-series-parallel-arc-validation.md). Rank zero is immediate.

This single-cycle argument does not claim exact polynomial comparison for sums of independent cycle extrema on arbitrarily many cycles. Independent algebraic fields can introduce a square-root-sum arithmetic issue there.

With continuous independent resistance intervals and fixed nominations at any fixed global rank, the circulation variables are the fixed core, cycle equations are fixed aggregate constraints, and resistance coefficients are scalar interval leaves. A linear flow objective depends affinely on the core. The same fixed-core theorem gives exact algebraic joint optimization. This is the continuous-versus-discrete companion at rank two; it does not assert the result for arbitrary nomination boxes and weighted flow objectives.

## Independent verification and novelty limits

Both [the first independent audit](../notes/review-potential-flow-weighted-arc-cycle-rank-hardness.md) and [the second independent audit](../notes/review-potential-flow-weighted-arc-cycle-rank-hardness-second.md) passed. They checked physical signs, the performance identity, gap constants, both scaling arguments, exact membership, and the direct rank-one algorithm.

The [focused source audit](../notes/potential-flow-weighted-arc-cycle-rank-hardness-novelty.md) found no matching theorem with fixed global rank two, four fixed nominations, two fixed objective coefficients, and two-point choices. General circuit-extremum hardness and nonlinear tolerance analysis are prior topics, and older inaccessible sources leave residual uncertainty. The plausible contribution is this precise rank-one/rank-two boundary; no exhaustive novelty clearance is asserted.

## Reproducible checks

[`weighted_arc_cycle_rank_hardness_checks.py`](../code/potential_flow_mpd/weighted_arc_cycle_rank_hardness_checks.py) passed three symbolic identities, three exact rational theta states, and 1,778 resistance scenarios across 40 instances at 90-digit precision. It checked every balance and edge law on the full subdivided theta, target equality, strict robust-limit direction, no-case gap, integer resistance scaling, and nomination amplification. The largest full physical residual was below `9.61e-83`. These checks support the formulas and encoding; they do not replace the complexity proof or source audit.

## Positive weighted-throughput corollary

The hardness also holds with two fixed positive objective coefficients. Conservation at vertex 0 gives `x_02+x_03=4`, hence

```
F_positive=9x_03+5x_23=F+36.
```

The maximum target becomes `63/2`, and every gap above is unchanged. Both selected flows are strictly positive throughout the construction, so this is a nonnegative weighted inflow objective at vertex 3. Under the separate nomination scaling by `N`, the shift is `36N` and the target is `63N/2`. Both independent reviewers confirmed this corollary; it does not alter the fixed nominations, graph rank, or resistance encoding.

## Unit total-flow objective on a directed acyclic graph

The reduction can use coefficient one on every arc. For an instance with `n` items, subdivide path `0->3` into `9n+1` edges of total resistance one. Keep the other three outer paths as single edges. Replace the cross path by `5n` edges: `4n` fixed edges of resistance `28/(81n)`, and `n` uncertain edges with options

```
{112/(81n), 112/(81n)+224a_i/(81K)}.
```

The effective cross resistance remains `theta=(224/81)(1+subset/K)`. Internal nominations are zero. Every edge flow is strictly positive for every positive `theta`, by the physical bounds proved above; subdivision preserves this. The orientation is acyclic. Therefore the sum of all oriented flows equals the sum of their absolute values, and it is

```
(9n+1)(4-a)+a+(a+3-q)+(1-a+q)+5nq
 = nF+36n+8.
```

Its peak is `(63n+16)/2`, and its no-instance gap is at least `n Delta`. The graph has `14n+4` edges and `14n+3` vertices, so global rank remains two and maximum degree remains three. All original small nominations remain fixed. The objective support grows, but every coefficient is one.

Common resistance scaling by `81nK(9n+1)` makes every coefficient integral. The subdivided `0->3` edges become `81nK`; fixed cross edges become `28K(9n+1)`; uncertain cross options become

```
{112K(9n+1), 112K(9n+1)+224n(9n+1)a_i}.
```

The three remaining outer resistances are the common scale times `(1,1,2)`. Both independent reviewers checked the path counts, objective identity, positivity, and encoding. Thus the precision hardness also holds for maximizing total absolute flow with unit arc costs on this directed acyclic construction. No constant-gap or strong-hardness claim is inferred while retaining the small nominations; the separate nomination-amplification argument remains available on an unnormalized class.

The separate [`weighted_arc_unit_cost_checks.py`](../code/potential_flow_mpd/weighted_arc_unit_cost_checks.py) passed 62 complete subdivided scenarios, checking acyclic orientation, graph counts, positive flows, every conservation equation, the all-unit objective identity, and integer resistance data.
