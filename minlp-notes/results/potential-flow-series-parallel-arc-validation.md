# Arc-flow uncertainty hulls on series-parallel graphs

Date: 2026-09-05. Status: theorem passed two independent full proof and primary graph-source audits. The electrical sign mechanism is classical confluence theory; no novelty is claimed for it. The computational consequence is a sharp block-rank boundary for discrete arc-capacity validation, subject to the circuit-literature qualifications below.

## Structural theorem

Let a connected graph be series-parallel in the undirected sense, equivalently contain no `K4` minor. Every edge law is continuous, strictly increasing, and zero at zero. Its coefficients vary affinely in independent compact scalar intervals, with each parameter affecting only one edge and every intermediate complete law remaining admissible. Fix balanced nominations and a target edge `a`.

Then its signed physical flow `x_a` is separately monotone in every uncertain scalar parameter. Hence maximum and minimum flow over a product of arbitrary compact scalar parameter sets equal the extrema over the product of their interval hulls, provided the sets attain those endpoints and all hull laws are admissible. The same equality holds after jointly optimizing over any compact nomination set. No extra flow or potential constraints restrict the physical scenario domain.

The law assumptions guarantee a unique physical flow: the energy is strictly convex and coercive. For coercivity, the primitive of a law `g` satisfies `G(x)>=c(|x|-1)` for `|x|>=1`, with `c=min(g(1),-g(-1))>0`. Bounded laws are therefore allowed.

## 1. Electrical sign lemma and primary sources

For an existing edge `a=(u,v)` of a series-parallel graph, inject one unit at `u` and withdraw one unit at `v` in any positive-resistance electrical network. Every edge current has a sign determined by the graph and target orientation, independently of the positive resistance values. Edges off the target block have zero current.

Apply the following fact only to the biconnected block containing `a`; all off-block electrical currents are zero. [Eppstein (1992), Lemma 9](https://www.ics.uci.edu/~eppstein/pubs/Epp-IC-92.pdf), printed page 9, states that a biconnected series-parallel graph becomes two-terminal series-parallel with the endpoints of any existing edge selected as terminals. [Cosme Llópez and Pous (2017)](https://drops.dagstuhl.de/entities/document/10.4230/LIPIcs.MFCS.2017.76) explicitly relate the `K4`-minor-free convention to series-parallel biconnected components. On a two-terminal decomposition, series composition transmits the same positive unit current through each component; parallel composition splits positive current among components. Induction therefore gives a fixed orientation for every current.

A second primary route is [Duffin's confluence theorem](https://sites.math.washington.edu/~reu/papers/current/jim/duffin.pdf), Theorems 0 and 1, printed pages 306–307. Add a positive-resistance source branch parallel to `a`; this creates no `K4` minor. The source-driven original-network currents are a positive multiple of the unit endpoint adjoint and have resistance-independent directions. Both independent reviewers read primary sources supporting these formulations; the electrical sign lemma is established prior theory.

The adjacency of the objective terminals matters. The same statement for every pair of vertices requires the narrower cactus graph class. This distinction explains why the rank-two theta pressure counterexample does not automatically give rank-two arc-flow hardness.

## 2. Parameter sensitivity for another edge

First assume smooth laws with positive derivatives. Let `h` be the electrical adjoint for the target endpoints, and let `j_e` be its signed edge currents. If a parameter `theta` changes the law on a different edge `e` by the affine term `theta f_e(x_e)`, differentiating the target law and potential objective gives

```
partial x_a/partial theta = j_e f_e(x_e)/g'_a(x_a).
```

The denominator is positive. The electrical sign lemma fixes the sign of `j_e`. The sign of `f_e(x_e)` cannot change as this parameter varies with everything else fixed: if it vanishes at any parameter, the entire physical state at that parameter also satisfies every other parameter value, since the only changing constitutive term is zero. Uniqueness makes the state parameter independent. Otherwise continuity prevents a sign change. Therefore the derivative has one weak sign throughout the parameter interval.

## 3. A parameter on the target edge

For a parameter changing the target law itself, differentiation instead gives

```
g'_a(x_a) partial x_a/partial theta + f_a(x_a)
   = partial(pi_u-pi_v)/partial theta
   = j_a f_a(x_a),

partial x_a/partial theta
   = -(1-j_a) f_a(x_a)/g'_a(x_a).
```

The ordinary unit electrical adjoint has `0<=j_a<=1` on its source-to-sink edge. This follows from the electrical maximum principle and the acyclic unit-flow bound. The same zero-basis invariance argument fixes the basis sign. Thus target-edge parameters also yield separate monotonicity. If the target edge is a bridge, `j_a=1` and its flow is independent of every constitutive parameter, as conservation requires.

## 4. Continuity, hull equality, and nomination uncertainty

Use centered convolution of every basis and add a positive linear term to each complete law. This preserves affine dependence, zero at zero, strict increase, and yields positive derivatives. All physical flows have a uniform bound from the nomination magnitude. Centered smoothing converges uniformly on the compact flow interval, and strict convex energy plus uniqueness imply convergence of the physical states.

For each fixed parameter coordinate and fixed setting of the other data, select a smoothing subsequence with a common weak monotonicity direction. The limiting original edge-flow function is monotone in that direction. This establishes the continuous-law statement without differentiating at kinks or zero derivatives.

Starting from a global optimizer, move one parameter at a time to an appropriate interval endpoint, preserving its optimum value. The resulting point lies in the original product of compact scalar sets. Holding an optimal nomination fixed during these moves proves the joint-nomination version.

## 5. Exact polynomial algorithm and rank boundary

Specialize to common quadratic laws and explicitly listed finite positive rational resistance sets. If the graph is series-parallel and its maximum block cycle rank is fixed, the structural equality allows replacing each finite set by its rational endpoint interval. The reviewed [exact continuous-box arc-extremum theorem](../results/potential-flow-exact-arc-capacity.md) computes the exact max/min signed flow over this hull and the nomination box in polynomial bit time. These equal the finite-set extrema, so robust arc-capacity validation is exact polynomial time as well. It is unnecessary to enumerate all endpoint combinations.

An exact maximizing finite resistance vector and an algebraic optimal nomination can also be recovered by self-reduction. Compute the hull optimum `V`. Fix the next resistance to its rational lower endpoint and reoptimize the remaining box and nomination box exactly. If the new optimum equals `V`, keep that endpoint; otherwise fix the upper endpoint. At least one endpoint preserves `V`, because separate monotonicity applies at a nomination attaining the current joint optimum. Repeat for every coordinate. This uses only polynomially many exact fixed-rank arc optimizations and pairwise algebraic comparisons. Once all resistances are fixed, return an exact algebraic nomination optimizer. No common field across optimization calls is formed, and no rational exact physical-state witness is promised.

Every graph with maximum block cycle rank at most two is series-parallel: a `K4` minor would require a biconnected block of cycle rank at least three, since cycle rank cannot increase under deletions or contractions. Therefore discrete arc-capacity validation is polynomial at maximum block rank two.

The separately reviewed [rank-three reduction](potential-flow-discrete-arc-capacity-hardness.md) gives coNP-completeness when the maximum block rank is three. The two independently reviewed statements form an exact graph-parameter boundary: at most two independent cycles per block gives polynomial validation, whereas allowing three gives coNP-completeness. The hardness has fixed nominations; the positive algorithm permits shifted nomination boxes. This does not claim polynomial optimization on all series-parallel graphs when their block cycle rank is unbounded.

## Literature and scope cautions

[The cactus hull source audit](../notes/potential-flow-cactus-hulls-novelty.md) identifies Duffin's classical confluence theory, related linear differential-flow work, and a directly relevant 1993 Hasler–Wang nonlinear tolerance paper that was not openly located. The positive nonlinear tolerance consequence may overlap that unread source. The [focused follow-up source audit](../notes/potential-flow-series-parallel-envelope-novelty.md) found no equivalent rank-two/rank-three discrete arc boundary. The sharper computational rank boundary combines the structural mechanism with the independently developed fixed-rank algorithm and discrete hardness reduction; the exact scope is not claimed to be cleared by an exhaustive circuit-literature search.

## Reproducible mechanism checks

[`series_parallel_arc_hulls_checks.py`](../code/potential_flow_mpd/series_parallel_arc_hulls_checks.py) uses `K_{2,3}` and `K_{2,4}` blocks with dangling branches, covering block ranks two and three. It passed 2,160 comparisons of adjacent-terminal adjoint current signs across independently varied positive electrical resistances. It also passed 60 physical arc-flow parameter finite differences, explicitly including the distinct own-edge factor `j_a-1`; the largest derivative discrepancy was `5.50e-11`. The physical checks use a small positive quadratic-law smoothing term. These tests support the sign and derivative mechanisms, while the graph theorem and exact algorithm require the written proofs and source audit.

Run with `/workspace/local-home/miniconda3/envs/minlp-notes/bin/python code/potential_flow_mpd/series_parallel_arc_hulls_checks.py`.

## Independent verification

Both full audits passed: [first review](../notes/review-potential-flow-series-parallel-arc-hulls.md) and [second review](../notes/review-potential-flow-series-parallel-arc-hulls-second.md). They independently checked the primary graph lemmas, own-edge sensitivity factor, smoothing and bounded-law existence, endpoint hull equality, exact endpoint recovery, and the block-rank boundary.
