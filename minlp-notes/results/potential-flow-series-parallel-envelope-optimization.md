# One envelope network for fixed-nomination arc extrema on series-parallel graphs

Date: 2026-09-05. Status: theorem passed two independent full proof and algorithmic source audits. The electrical current-sign theorem and convex passive-flow formulation are established ingredients. The envelope comparison may overlap classical nonlinear circuit tolerance theory; the precise bit-time algorithm and endpoint recovery are the candidate contribution, with no exhaustive novelty clearance claimed.

## Theorem

Let a connected undirected graph contain no `K4` minor. Orient its edges, fix a rational balanced nomination vector `b`, and prescribe a target edge `a`. Edge laws are `beta_e x_e|x_e|`, with independently chosen positive resistances in rational intervals, or explicitly listed finite positive rational sets. No additional physical flow or potential constraints restrict scenarios. There is no restriction on block cycle rank.

For each target-flow maximum or minimum, one explicitly constructed deterministic network with asymmetric positive quadratic laws has a physical target flow equal to that exact extremum. Its physical flow minimizes a rational convex cubic energy admitting an SOCP formulation of linear size. For every rational tolerance `epsilon>0`, the extremum has a certified rational enclosing interval of width at most `epsilon`, and a resistance vector using only allowed rational endpoints attains flow within `epsilon` of the extremum, computable in polynomial time in input length and `log(1/epsilon)`. The theorem does not claim polynomial exact threshold decision or a rational exact physical state.

Fixed nominations are essential to this statement. The graph's cycle rank can be unbounded; this is a different scope from the reviewed algorithms allowing continuous nomination boxes at fixed block rank.

## 1. Constructing the envelope laws

Use the [reviewed adjacent-terminal electrical sign theorem](../results/potential-flow-series-parallel-arc-validation.md). For a unit electrical injection at the tail of `a` and withdrawal at its head, let `sigma_e` be the graph-determined sign of the current on each other edge. These signs can be computed by one rational electrical solve with all resistances one. They do not depend on the eventual positive differential resistances. Off the target block they are zero. The own-edge unit current always satisfies `0<=j_a<=1`.

Write `L_e,U_e` for the attained resistance endpoints and define the pointwise law bounds

```
g_e^max(x) = max{L_e x|x|, U_e x|x|},
g_e^min(x) = min{L_e x|x|, U_e x|x|}.
```

Both are continuous, strictly increasing, continuously differentiable asymmetric quadratic laws. To maximize target flow, choose

```
g_a^* = g_a^min,
g_e^* = g_e^max   if e!=a and sigma_e>0,
g_e^* = g_e^min   if e!=a and sigma_e<0.
```

For `sigma_e=0`, choose either fixed endpoint law. To minimize target flow, interchange every minimum and maximum above; the zero-current choices remain arbitrary.

## 2. Finite comparison and attainment

Fix any admissible original resistance vector, with physical flow `x`, and let `y` be the physical flow under the envelope laws. Define positive secant resistances and constitutive changes by

```
r_e=[g_e^*(y_e)-g_e^*(x_e)]/(y_e-x_e)  if y_e!=x_e,
r_e=any positive number                         if y_e=x_e,
d_e=g_e^*(x_e)-beta_e x_e|x_e|.
```

Subtract the two physical systems. Their flow difference is a circulation, and the potential difference satisfies the exact linear equation `A^T Delta pi=diag(r)(y-x)+d`. Let `j` be the ordinary unit electrical adjoint between the target endpoints for resistances `r`. Then

```
y_a-x_a = [sum_{e!=a} j_e d_e-(1-j_a)d_a]/r_a.
```

On the series-parallel graph, every other-edge current has its prescribed graph-fixed sign and `0<=j_a<=1`. The maximizing envelope construction makes every numerator term nonnegative. Therefore its target flow is an upper bound for every original resistance scenario. This finite identity uses only strict increase of the laws; it requires no smoothing or derivative assumptions. The [full secant comparison theorem](potential-flow-secant-envelope-comparison.md), including its continuous-law extension, passed two independent audits.

On each edge, select the original endpoint resistance whose law agrees with the envelope at `y_e`; either endpoint works when `y_e=0`. The complete envelope state then satisfies that original scenario, and uniqueness makes it its physical state. Thus the bound is attained. Reversing all envelope choices proves the minimum statement.

## 3. Convex formulation and SOCP representation

Write the envelope law as

```
g_e^*(x)= c_e^+ x^2 for x>=0,
g_e^*(x)=-c_e^- x^2 for x<=0,
```

where both coefficients are positive rational resistance endpoints. Its unique physical flow minimizes

```
E(x)= (1/3) sum_e [c_e^+ (x_e^+)^3 + c_e^- (x_e^-)^3],
A x=b.
```

Use nonnegative variables `p_e,n_e` with `x_e=p_e-n_e`. At an energy minimizer, simultaneous positivity of `p_e,n_e` is impossible: subtract their minimum without changing flow or conservation and strictly decrease energy. Thus minimizing the same cubic expression in `p,n` is exact.

For a nonnegative scalar `z`, its cubic epigraph `z^3<=u` has the lift

```
z^2<=w,
w^2<=u z,
u,w,z>=0.
```

Both inequalities are rotated second-order cones, with the first using a constant factor one. If `z>0`, they imply `z^4<=u z`; at zero choose `w=0`. Conversely use `w=z^2`. Hence the complete network needs a constant number of conic variables and constraints per edge. This formulation establishes the computational representation; the bit-time guarantee below does not assume arbitrary SOCPs are automatically well conditioned.

## 4. Explicit polynomial-bit weak optimization

If `b=0`, every physical flow is zero and any endpoint vector is optimal. Otherwise let `B=sum_v |b_v|>0`, `m=|E|`, `beta_L=min L_e`, and `beta_U=max U_e`. Any passive physical flow has absolute value at most `B/2`: direct it by decreasing potential, and use the acyclic flow bound by total positive nomination.

Choose a spanning tree and a rational tree-supported particular flow `x0`, whose coordinates have absolute value at most `B/2`. Let `C` be its fundamental-cycle matrix, with entries in `{0,1,-1}` and an identity submatrix on the chords. Every feasible flow is `x=x0+Cz`. For the physical minimizer, the chord coordinates `z*` have absolute value at most `B/2`.

If there are no chords, the flow is fixed by conservation and can be returned directly. Otherwise minimize the convex piecewise cubic rational function `E(x0+Cz)` on the cube `[-B,B]^k`, where `k` is the cycle rank. This cube contains its global minimizer with margin at least `B/2` from every face. On this cube, every edge flow is bounded by `R=(m+1)B`. An explicit bound on the absolute value of every gradient coordinate is

```
G0=m beta_U R^2,
G=1+m G0.
```

Consequently `G` bounds the Euclidean gradient norm. Function and gradient evaluations at rational points are exact rational arithmetic with polynomial bit cost: the sign of each affine flow selects its cubic piece.

For a rational sublevel threshold `t`, an outside cube coordinate gives a rational separating hyperplane; when `E(z)>t`, its rational gradient gives a separating hyperplane for the convex sublevel set. If `t>=E*+delta`, that sublevel set inside the cube contains a Euclidean ball centered at `z*` of radius

```
r_delta=min{B/4, delta/(2G)}.
```

The whole cube lies in the radius `mB` ball. The logarithm of the ratio of these radii is polynomial in input length and `log(1/delta)`. The rational ellipsoid weak-feasibility procedure, followed by threshold bisection between zero and the rational value `E(x0)`, therefore returns a rational `z` with `E(x0+Cz)<=E*+delta` in polynomial bit time. One can use tolerance `delta/4` inside the feasibility/bisection routine to absorb its numerical objective budget. All returned flows `y=x0+Cz` satisfy conservation exactly. This is a concrete bounded-oracle proof; it does not depend on exact conic feasibility certificates at irrational optima.

An open primary reference is [Dadush (2012), Theorem 2.5.9](https://homepages.cwi.nl/~dadush/papers/dadush-thesis.pdf), printed page 48 (PDF page 61), with the encoding convention in Section 2.5.1 and immediately before Section 2.5.2: polynomial time is polynomial in the lengths of the rational data and oracle parameters. This states weak convex optimization on a centered bounded convex body with a rational evaluation oracle, producing a feasible point and an additive objective enclosure. For its globally Lipschitz formulation, replace each scalar energy outside `[-R,R]` by its tangent affine continuation. This gives a convex continuously differentiable globally Lipschitz function, unchanged throughout the optimization cube, with the same rational oracle and gradient bound. Dadush credits the classical weak membership/optimization equivalence; the algorithmic theorem is prior work.

## 5. Converting energy accuracy to flow accuracy

The function `g_e^*(x)-beta_L x|x|` is increasing. The quadratic scalar monotonicity inequality therefore gives

```
(g_e^*(u)-g_e^*(v))(u-v) >= (beta_L/2)|u-v|^3.
```

Integrating on the segment from `x*` to any feasible `y`, and using that the physical gradient is a potential difference orthogonal to circulations, gives

```
E(y)-E(x*) >= (beta_L/6) sum_e |y_e-x*_e|^3.
```

Thus an energy gap at most `delta=beta_L eta^3/6` guarantees `||y-x*||_infinity<=eta`. The rational interval `[y_a-eta,y_a+eta]` encloses the exact extremum. Take `eta<=epsilon/2` to ensure width at most `epsilon`.

## 6. Recovering an allowed endpoint scenario without exact sign tests

Select each resistance endpoint according to the sign of the approximate flow `y_e` and the envelope rule. This is an exact rational endpoint selection. If this selection differs from one agreeing with the true envelope flow, then `|x*_e|<=eta`. Therefore the constitutive residual of the selected original law at `x*` obeys

```
|beta_e x*_e|x*_e| - g_e^*(x*_e)| <= beta_U eta^2.
```

Let `x'` be the physical flow for these chosen resistances and the fixed nomination. The difference `x'-x*` is a circulation. Subtracting the two constitutive systems, taking their product with this circulation, and using scalar strong monotonicity yields, for `D=||x'-x*||_infinity`,

```
(beta_L/2) D^3 <= m beta_U eta^2 D.
```

For `D>0`, this gives `D<=sqrt(2m beta_U/beta_L) eta`; the zero case is immediate. Set the rational factor `C0=1+2m beta_U/beta_L` and take

```
eta=min{epsilon/2, epsilon/C0}.
```

The output endpoint scenario has target flow within `epsilon` of its exact extremum, while the certified value interval has width at most `epsilon`. All requested internal precision has polynomial binary length. This avoids the need to decide whether an algebraic envelope flow is exactly zero.

## Boundaries and novelty audit needed

The single-envelope identity is exact as a mathematical statement. The algorithmic output is additive: no exact algebraic encoding or polynomial exact threshold decision is asserted when cycle rank is unbounded. Fixed nominations are used throughout. There are no flow or potential side constraints on the uncertainty scenarios.

The adjacent-terminal current-sign lemma is classical [Duffin confluence theory](https://sites.math.washington.edu/~reu/papers/current/jim/duffin.pdf), with a direct series-parallel formulation in [Eppstein, Lemma 9](https://www.ics.uci.edu/~eppstein/pubs/Epp-IC-92.pdf). The [existing circuit novelty audit](../notes/potential-flow-cactus-hulls-novelty.md) flags the unread Hasler–Wang 1993 nonlinear tolerance paper. Another possibly relevant source is the IEEE article [“Does a series-parallel network of monotone resistors make sense? Yes or no?”](https://ieeexplore.ieee.org/document/558441/). Its actual contents have not yet been read. The [focused envelope source audit](../notes/potential-flow-series-parallel-envelope-novelty.md) did not establish an equivalent envelope theorem, but the inaccessible older nonlinear tolerance sources remain a material novelty limitation. The proof and algorithmic guarantees do not depend on a claim that those circuit ingredients are new.

## Reproducible mechanism checks

[`series_parallel_envelope_checks.py`](../code/potential_flow_mpd/series_parallel_envelope_checks.py) compared 24 envelope maxima/minima on `K_{2,3}` and `K_{2,4}` blocks with dangling branches against exhaustive enumeration of 3,840 endpoint scenarios. These networks include block ranks two and three, and the tests include a target bridge. The largest extremum mismatch was `4.05e-15`; selecting endpoints from the envelope flow reproduced its full state within `5.47e-15`. Another 72 approximate-sign endpoint recoveries satisfied the stated perturbation bound, and 72 feasible-flow perturbations satisfied the energy-gap inequality. These checks use unsmoothed quadratic laws and independently solve the circulation equations; they do not certify the general theorem or its bit complexity.

Run `/workspace/local-home/miniconda3/envs/minlp-notes/bin/python code/potential_flow_mpd/series_parallel_envelope_checks.py`.

## Independent verification and exact-arithmetic boundary

Both full algorithm audits passed: [first review](../notes/review-potential-flow-series-parallel-envelope.md) and [second review](../notes/review-potential-flow-series-parallel-envelope-second.md). They checked simultaneous homotopy, the distinct target-edge factor, exact endpoint realization, the cubic SOCP lift, the rational ellipsoid oracle and its input-length guarantees, the energy-to-flow constant, and approximate-sign recovery. Both directly read the primary graph and bounded-ellipsoid statements. The second reviewer also checked 10,000 rational scalar monotonicity instances exactly. The finite comparison proof now used in Section 2 has two additional full audits linked in the secant support result.

The separately [reviewed exact arc comparison corollary](potential-flow-series-parallel-exact-arc-barrier.md) adds a probe to the cactus arithmetic encoder and proves Square-Root-Sum hardness of exact thresholds even with fixed unit nominations and no uncertainty. It has its own two independent audits and remains a distinct exact-arithmetic statement. The present result intentionally gives certified additive values and rational near-extremal resistance selections.

## Parametric consequence: eliminate resistance uncertainty before nomination optimization

The envelope law profile depends only on the graph, prescribed target edge, and resistance endpoints. Different target edges generally require different envelope profiles; this is not one network simultaneously maximizing every arc. It does not depend on the fixed nomination used to prove the comparison. Consequently the same envelope network represents the entire value function

```
x_a^envelope(b)=max_beta x_a(b,beta)
```

for every balanced nomination `b` simultaneously, with the corresponding minimum profile for lower extrema. For any nonempty compact set `U` of balanced nominations, it follows immediately that

```
max_{b in U, beta allowed} x_a(b,beta)
 = max_{b in U} x_a^envelope(b).
```

Thus a robust arc-extremum model on a series-parallel graph can remove all independent resistance choices before optimizing nominations: it replaces them by one deterministic asymmetric quadratic law per edge. Endpoint resistances realizing the resulting optimum are recovered from its flow signs. That original resistance vector can depend on the nomination; the statement does not promise one resistance vector simultaneously attaining the envelope at every nomination. This is an exact model reduction, including when the resistance sets are discrete. It does not claim polynomial optimization of the remaining nomination problem on graphs with unbounded block cycle rank, and it does not add side constraints to the scenario domain.

## Direct conic formulation check

[`envelope_socp_checks.py`](../code/potential_flow_mpd/envelope_socp_checks.py) implemented the two explicit rotated-SOC inequalities for each positive and negative cubic term and solved eight envelope networks on `K_{2,k}` blocks with cycle ranks 2, 4, 8, and 14. Compared with independently solved physical circulation equations, the largest flow discrepancy was `4.39e-7`, conservation residual `1.72e-15`, and energy discrepancy `2.44e-11`. The installed CVXPY 1.9.2/Clarabel solver reported `optimal_inaccurate` in two of eight runs at the requested `1e-10` solver tolerance; the independently checked residuals above describe the observed accuracy. This is numerical formulation evidence, not a certified implementation of the theorem's rational ellipsoid algorithm.

## Verifiable numerical output

The separately reviewed [rational energy certificate](potential-flow-envelope-rational-certificates.md) supplies exact, solver-independent posterior flow and pressure intervals for a deterministic envelope solve. Its saved JSON example verifies with ordinary Python using only rational arithmetic and integer roots. The uncertainty interpretation additionally requires the envelope instance to have been constructed correctly for the original graph, target, and resistance bounds; the JSON itself certifies only the deterministic energy instance.
