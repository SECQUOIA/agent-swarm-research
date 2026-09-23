# Finite secant comparison and continuous-law envelopes

Date: 2026-09-05. Status: finite comparison identity and full continuous-family structural theorem passed two independent audits. The electrical sign theorem is classical, and related nonlinear circuit comparison results may already exist. This is a reviewed proof simplification and structural support result, with no new bit-time claim for arbitrary continuous laws.

## Exact finite comparison identity

Let a connected oriented graph have incidence matrix `A`, fixed balanced nominations `b`, and two sets of continuous strictly increasing edge laws `g_e,G_e`, each zero at zero. Let `x,y` be their unique physical flows, with potentials `pi,rho`, respectively. For each edge define

```
r_e = [G_e(y_e)-G_e(x_e)]/(y_e-x_e)  if y_e!=x_e,
r_e = any positive number                    if y_e=x_e,
d_e = G_e(x_e)-g_e(x_e).
```

Strict increase makes every secant resistance positive. The zero-difference definition is harmless because its coefficient multiplies zero. Subtraction of the two physical systems gives the exact linear identities

```
A(y-x)=0,
A^T(rho-pi)=diag(r)(y-x)+d.
```

For a target edge `a=(u,v)`, let `h` solve the ordinary positive-resistance electrical adjoint

```
A diag(1/r) A^T h = e_u-e_v,
j=diag(1/r) A^T h.
```

Applying the adjoint to the difference equations yields

```
(rho_u-rho_v)-(pi_u-pi_v)=j^T d,
y_a-x_a = [sum_{e!=a} j_e d_e-(1-j_a)d_a]/r_a.    (1)
```

These are finite identities, not derivatives. No smoothing, positive law derivative, inverse function theorem, or path integration is needed. For any connected graph, `0<=j_a<=1` by the electrical maximum principle and unit-flow bound.

## Continuous-law envelope theorem on series-parallel graphs

Suppose the graph has no `K4` minor. For each edge let `Theta_e` be a nonempty compact parameter space and let `g_e(x,theta)` be jointly continuous. Each member is strictly increasing in `x` and zero at zero. Choices are independent between edges; coordinates within one edge's parameter space may be coupled arbitrarily.

Define the pointwise extremal laws

```
g_e^max(x)=max_{theta in Theta_e} g_e(x,theta),
g_e^min(x)=min_{theta in Theta_e} g_e(x,theta).
```

Compactness and joint continuity guarantee attainment and continuity of both envelopes. They are strictly increasing: for the maximum, use a member attaining the old maximum at the smaller argument; for the minimum, use a member attaining the new minimum at the larger argument. Both envelopes vanish at zero. Their primitives are strictly convex and coercive, so their network has a unique physical flow for every balanced nomination.

For one prescribed target edge, its adjacent-terminal unit electrical currents have graph-fixed signs `sigma_e` independent of positive resistances. Select a maximizing law profile as follows:

- on the target edge, use `g_a^min`;
- on another edge with positive adjoint sign, use `g_e^max`;
- on another edge with negative adjoint sign, use `g_e^min`;
- on zero-adjoint edges, use any member law.

Compare any original scenario with this profile using (1). Every term on the right is nonnegative, proving that the envelope target flow is an upper bound for every scenario.

At the envelope physical flow, compactness provides for each edge a parameter member attaining the required envelope value at that scalar flow. Select these parameters independently across edges. The resulting original scenario has exactly the same entire physical state, by uniqueness. Therefore the envelope upper bound is attained. Interchanging every maximum and minimum gives the lower extremum.

The same envelope profile works for every balanced nomination simultaneously. Hence resistance/law uncertainty can be removed before optimization over any nonempty compact set of balanced nominations, although the remaining nomination optimization is not claimed easy. The original parameter choice realizing the envelope generally depends on the nomination; no single original scenario is claimed to realize it for all nominations. Different target edges generally require different envelope profiles.

## Relation to the reviewed quadratic algorithm

For quadratic resistance intervals or finite sets, the pointwise envelopes are the asymmetric quadratic laws in the [reviewed one-SOCP theorem](../results/potential-flow-series-parallel-envelope-optimization.md). Identity (1) now supplies its finite comparison proof, without changing any algorithm, accuracy constant, output claim, or graph scope.

The broader continuous-law statement is structural only. Arbitrary compact parameter spaces need not have a computable representation or an efficient envelope oracle, and no polynomial algorithm is claimed for them. The fixed quadratic result retains its explicit rational convex cubic formulation and endpoint-recovery algorithm.

## Further direct consequence for pressure comparisons

For an arbitrary objective pair `s,t`, the first identity holds with its corresponding unit adjoint: `Delta(pi_s-pi_t)=j^T d`. On a cactus, these current signs are graph-fixed for every terminal pair. Choosing a pointwise maximum law on positive-sign edges and a pointwise minimum on negative-sign edges therefore maximizes that pressure difference over independent compact edge-law families; reversing choices minimizes it. The same edgewise attainment argument applies. This is a structural extension of the [cactus uncertainty investigation](../notes/potential-flow-cactus-uncertainty-hulls.md), not a new assertion that the classical circuit comparison mechanism is novel.

## Source and review boundaries

The graph-fixed sign property is established [Duffin confluence theory](https://sites.math.washington.edu/~reu/papers/current/jim/duffin.pdf), with the target-edge series-parallel formulation supported by [Eppstein, Lemma 9](https://www.ics.uci.edu/~eppstein/pubs/Epp-IC-92.pdf). The [focused nonlinear tolerance audit](../notes/potential-flow-series-parallel-envelope-novelty.md) records unresolved older-paper access. The finite comparison identity is an elementary secant linearization and should be credited as a proof device rather than assigned novelty without a source comparison.

## Reproducible finite-identity checks

[`secant_comparison_checks.py`](../code/potential_flow_mpd/secant_comparison_checks.py) solved pairs of distinct asymmetric quadratic physical networks with the same nominations, formed their finite secant resistances, and checked (1) for every target edge. It passed 240 identities on both series-parallel and `K4` graphs with branches, with maximum discrepancy `8.03e-15`. The exact identity applies to both graph classes; only the resistance-independent sign conclusion uses series-parallel structure.

## Independent verification

Both full reviews passed: [first audit](../notes/review-potential-flow-secant-envelope-comparison.md) and [second audit](../notes/review-potential-flow-secant-envelope-comparison-second.md). They checked the exact finite identity, compact continuous-family envelopes, strict monotonicity and coercivity, edgewise attainment, the cactus pressure consequence, and the simultaneous-in-nomination quantifiers. The realizing original parameters may depend on the nomination even though the envelope profile is fixed. These reviews assess correctness, not publication priority.
