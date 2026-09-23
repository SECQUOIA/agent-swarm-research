# Unbounded block rank: arc-capacity hardness on series-parallel graphs

Date: 2026-09-05. Status: corollary passed two independent full proof and primary-source audits. The source pressure hardness is due to Thürauf; the added probe transfers it to arc validation. This is a credited consequence, not a new Partition reduction.

## Theorem

For common quadratic passive laws and fixed positive rational resistances, optimizing a signed arc flow over a balanced nomination box is NP-hard even on series-parallel graphs of treewidth two. Robust arc-capacity validation is correspondingly coNP-hard. A polynomial-time high-precision additive algorithm on all such graphs would imply `P=NP`.

Unlike the fixed-block-rank theorem, this class has unbounded cycle rank in one biconnected block. The claim does not imply hardness at any fixed block rank and does not assert NP/coNP membership in the unbounded-rank class.

## 1. Known pressure-hardness input

[Thürauf, Deciding the feasibility of a booking in the European gas market is coNP-hard](https://optimization-online.org/wp-content/uploads/2020/05/7803-1.pdf), Figure 2, constructs a graph with branch vertices `s,t`, intermediate vertices `z_i+`, and pendant exits `z_i-`. The arcs are

```
s->z_i+, z_i+->t, z_i+->z_i-.
```

The main block is `K_{2,n}`, with rank `n-1`. For positive Partition numbers `S_i` and total `K=sum_i S_i`, the resistances on the first two edges of each branch are `1/S_i²`; the pendant resistance is one. Nomination bounds are `K/2` at `s,t` and `S_i` at each paired entry/exit. In signed form, these are entry intervals from zero to the bound and exit intervals from minus the bound to zero, intersected with balance. Their total absolute load bound is `3K`.

Lemma 4.3 and Lemma 4.17 provide the pressure gap: a yes Partition instance has a nomination with `pi_s-pi_t>=1`, whereas a no instance has every nomination satisfying `pi_s-pi_t<T(K)<1`. Equation (3) gives a positive rational `T(K)` with polynomial encoding length. Explicitly, with `n` the number of Partition items,

```
eps0=1-[(K-1/(8K))/K]^2,
M0=max{1-eps0+eps0^2, 1-eps0^2/K^2},
eps1=(1-M0)/5,
T(K)=max{1-eps1^2/(K^2 n^2), M0+4eps1}.
```

Here the source notation `T(K)` also depends on the fixed item count `n`. The quantities are computed by rational arithmetic and maxima only; `0<T(K)<1`. The input assumes `n>=3`, with smaller Partition instances handled directly. These are precisely the pressure subproblem's nomination and physical-law constraints; the source's separate booking potential bounds are not imported into the probe construction. The existing bounded-block-rank novelty audit independently checked this source reduction. Put `gamma=1-T(K)>0`.

## 2. Add a probe arc while preserving series-parallel structure

Add the direct edge `e=(s,t)` with fixed resistance

```
D = ceil(1000*K*(3K+2)/gamma),
H = (1+T(K))/2 = 1-gamma/2,
M = H D².
```

Give the edge the upper flow capacity `c=1/D`. Its addition preserves the series-parallel structure: it is another parallel `s-t` branch. The pendant exits do not change treewidth. The main block now has cycle rank `n`, so no fixed-rank theorem applies.

Fix an original feasible nomination `b`, and write `F_b(t)` for the old-network `s-t` potential difference with nomination perturbed to `b-t e_s+t e_t`. The new physical edge flow `t` satisfies

```
F_b(t)=M t|t|.
```

The same strict energy monotonicity argument as in the reviewed discrete arc reduction shows that `F_b` is strictly decreasing. If its original value `F_b(0)` is nonpositive, then the new flow is nonpositive and cannot violate `c`. If the new flow is positive, then `F_b(t)<=F_b(0)`.

## 3. Preserve the yes-instance gap

For every original nomination, the acyclic bound gives `|x_e|<=3K`. Along an `s-z_i+-t` path the total resistance is `2/S_i²<=2`, so

```
|F_b(0)|<=18K²=:U.
```

For a yes-instance nomination with `F_b(0)>=1`, the new flow is positive and

```
t<=sqrt(U/M)<=6K/D<1.
```

The original and perturbed nominations lie in an enlarged rational box with total absolute load bound at most `3K+2`; only `s,t` need enlargement by one. The same two-edge path gives nomination Lipschitz constant at most `4(3K+2)`. Consequently,

```
0<=F_b(0)-F_b(t)
 <=8(3K+2)t
 <=48K(3K+2)/D
 <=(48/1000)gamma < gamma/4.
```

Thus `F_b(t)>1-gamma/4>H`, and the new flow exceeds `1/D`.

For a no-instance nomination, if the new flow is nonpositive the capacity holds directly. Otherwise strict decrease gives `F_b(t)<=F_b(0)<T(K)<H`, so the new positive flow is strictly less than `1/D`. Therefore a violating nomination exists if and only if the Partition instance is feasible.

## 4. Quantitative arc gap

In a yes-instance witness, the pressure margin above `H` exceeds `gamma/4`; the positive flow is at most `6K/D`. Rationalizing the difference from `c` gives

```
t-c >= gamma/[4(6K+1)D].
```

In a no instance, positive target flows have a pressure margin below `H` of at least `gamma/2` and are at most `2/D`, giving a gap at least `gamma/(6D)`. Nonpositive flows have gap at least `1/D`. Both dominate the displayed yes-case lower bound. This positive rational arc gap has polynomial encoding length because `T(K)`, `D`, and `K` do.

Thus the added probe transfers the known pressure hardness to a high-precision arc-extremum obstruction on series-parallel graphs with unbounded block rank. This is a credited consequence of the old pressure reduction, not a new claim about its original construction.

## Limits and pending checks

All scenarios are unrestricted passive states; the arc capacity is evaluated afterward. No extra potential bound is imposed. If capacities on all other edges are required, use `[-3K,3K]`, which the original full-network nomination bound guarantees. The new arc remains the only potentially restrictive capacity.

Both independent audits checked the precise source lemma scope, perturbed nomination signs, uniform bound, enlarged box, gap conversion, and series-parallel preservation. No exhaustive search for a preexisting direct arc-capacity corollary has been completed. The reduction is from Partition with a potentially small rational gap: it gives weak NP/coNP hardness and a high-precision obstruction, not strong hardness or an impossibility of approximation schemes polynomial in reciprocal error.

## Reproducible full-network yes states

For the explicit yes-instance nominations in Thürauf's Lemma 4.3, the two Partition classes have total `K/2`. At an intermediate branch vertex, the effective nomination after eliminating its pendant is `-S_i` in one class and `+S_i` in the other. With the probe added, the old-network terminal drop and probe flow satisfy exactly

```
F=1-2t/K,
M t^2=F,
t=1/[sqrt(M+1/K^2)+1/K].
```

The branch flow formulas permit direct verification even though some original zero flows change sign. [`unbounded_rank_arc_probe_checks.py`](../code/potential_flow_mpd/unbounded_rank_arc_probe_checks.py) checked 24 such complete network states at 110-digit precision, using the original rational Equation (3) source thresholds. Conservation, every branch pressure, probe pressure, perturbation bound, and strict rational arc gap all passed. The largest probe equation residual was `3.33e-111`. These tests verify explicit yes witnesses and the new probe mechanism; they do not replace the source's proof for all no-instance nominations.

## Independent verification and related positive results

Both full reviews passed: [first audit](../notes/review-potential-flow-unbounded-rank-arc-obstruction.md) and [second audit](../notes/review-potential-flow-unbounded-rank-arc-obstruction-second.md). They directly checked the source's Figure 2, Equation (3), Lemmas 4.3 and 4.17, and the pressure subproblem (2), which excludes potential bounds. They also reproduced the 24 complete yes-witness checks. The auxiliary perturbed source and sink nominations may reverse sign within the enlarged box; this is valid because they only support the unconstrained physical sensitivity argument and need not be original allowed nominations.

The [fixed-nomination envelope theorem](potential-flow-series-parallel-envelope-optimization.md) gives a polynomial-bit additive algorithm on arbitrary series-parallel graphs when nominations are fixed, even with independent resistance uncertainty. The present result explains why allowing continuous nomination boxes changes that scope. The [fixed-block-rank exact arc theorem](potential-flow-exact-arc-capacity.md) still applies to nomination boxes when block rank is fixed. Neither positive theorem is contradicted by the unbounded-rank construction here.
