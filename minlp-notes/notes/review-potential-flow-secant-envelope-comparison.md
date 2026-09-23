# Independent review: finite secant comparison and continuous-law envelopes

Date: 2026-09-05. Reviewer: `potential_flow_review`.

**Verdict: PASS.** This review covers [the finite secant candidate](potential-flow-secant-envelope-comparison.md), its general compact edge-law families, its cactus pressure consequence, and the uniform-in-nomination corollary in [the promoted quadratic envelope theorem](../results/potential-flow-series-parallel-envelope-optimization.md). The finite identity can replace the earlier homotopy and smoothing argument. No new complexity or novelty claim for arbitrary continuous laws is justified or needed.

## 1. The exact identity

Let `x,pi` solve the physical equations under `g`, and let `y,rho` solve them under `G`, with the same balanced nomination. Put `Delta=y-x`. The proposed finite secant resistance is positive whenever its denominator is nonzero, because `G_e` is strictly increasing. If `Delta_e=0`, assigning any positive `r_e` is valid: the corresponding secant equation has zero on both sides. With `d_e=G_e(x_e)-g_e(x_e)`, the two state equations give exactly

```
A Delta=0,
A^T(rho-pi)=R Delta+d,
```

where `R=diag(r)` is positive definite.

For a target pair `u,v`, solve `A R^(-1) A^T h=e_u-e_v` and define `j=R^(-1)A^T h`. Then

```
j^T R Delta=h^T A Delta=0,
j^T A^T(rho-pi)=(e_u-e_v)^T(rho-pi).
```

This proves the finite pressure identity `Delta(pi_u-pi_v)=j^T d`. If `a=(u,v)` is an existing target edge, its own equation is

```
r_a Delta_a+d_a=Delta(pi_u-pi_v),
```

and consequently

```
Delta_a=[sum_(e!=a) j_e d_e-(1-j_a)d_a]/r_a.
```

All signs, the target coefficient `1-j_a`, and the denominator are correct. The first identity holds for any terminal pair and any connected graph; the second requires that its pair be the endpoints of the target edge. Neither requires differentiability. The identity also remains valid when several flow coordinates agree between the states and their auxiliary resistances are chosen arbitrarily.

For the unit electrical current with these positive resistances, the maximum principle gives `j_a>=0`. Its directed support is acyclic and carries one unit, so `j_a<=1`. This property holds on general connected graphs. Resistance-independent signs of the other currents require the separately established topology hypothesis.

## 2. Continuous laws still have unique physical states

The extension does not require constitutive laws to be unbounded. If `g` is continuous, strictly increasing, and zero at zero, then

```
c=min(g(1),-g(-1))>0.
```

Its primitive satisfies a lower bound `c*(|x|-1)` outside `[-1,1]`, and is nonnegative everywhere. Thus the sum of edge primitives is coercive and strictly convex. On the nonempty affine conservation space of a connected graph, it has a unique minimizer. First-order optimality gives a potential vector because the energy is continuously differentiable and the constraint space is affine. The potentials are unique modulo a constant.

This validates existence and uniqueness for both member laws and the proposed envelopes, including continuous bounded member laws. It does not import the stronger polynomial-law assumption used in earlier algorithmic results.

## 3. Compact families and exact realization

For every edge, compactness of its parameter space and joint continuity imply that both pointwise extrema are finite, attained, and continuous in flow. Strict increase of the maximum envelope follows by selecting a member attaining its value at the smaller argument. Strict increase of the minimum envelope follows by selecting a member attaining its value at the larger argument. Both envelopes vanish at zero.

On a `K4`-minor-free graph, the existing-edge electrical sign theorem applies to the finite secant resistances just as it applied to differential resistances. For a maximizing profile, the target uses the minimum envelope, positive-sign other edges use the maximum envelope, and negative-sign other edges use the minimum envelope. In the finite identity, `d_a<=0`, each positive-sign term has `d_e>=0`, and each negative-sign term has `d_e<=0`. Every contribution to the target-flow difference is therefore nonnegative. Edges with identically zero adjoint current can use any fixed member law. Reversing all choices proves the lower bound.

At the envelope physical state, choose on each edge a parameter attaining the envelope value at that particular scalar flow. The entire potential and flow state then satisfies the selected original laws, so uniqueness proves exact realization. Independence is needed **between edges** for these selections to be combined. There is no need for coordinate independence inside one edge's parameter space. The chosen member may depend on the physical flow and hence on the nomination, but it is one legitimate parameter for the entire edge law in the realized scenario.

The envelopes need not themselves be members of their edge families. They serve as auxiliary deterministic laws; only their values at the attained physical state need memberwise realization. This is exactly what compactness supplies.

## 4. Quantifiers in the nomination corollary

For a prescribed target edge and a prescribed maximization or minimization direction, the profile depends only on graph current signs and the fixed edge-law families. Neither the profile nor the auxiliary pointwise envelope definitions depend on nominations. The same profile therefore satisfies

```
x_a^envelope(b)=max_(allowed edge parameters) x_a(b,parameters)
```

for every balanced `b`. A separate profile gives the minimum. Different target edges generally need different profiles.

For a nonempty compact set `U` of balanced nominations, the physical flow of the fixed envelope network is continuous in `b`. To verify this without an inverse derivative bound, use the nomination-dependent acyclic-flow bound, normalize one potential, and take subsequential limits. Bounded law values on the resulting compact flow interval bound normalized potentials. Uniqueness identifies every limit. The envelope target-flow maximum is thus attained on `U`; edgewise realization at a maximizing nomination gives an original scenario attaining the same value. Hence

```
max_(b in U, allowed parameters) x_a(b,parameters)
 = max_(b in U) x_a^envelope(b).
```

There is no exchange of `max` and `min` here and no assertion of a single original scenario working for all nominations. The original realizing parameter vector may depend on `b`. In the quadratic case it can be selected using the resulting flow signs, exactly as in the prior theorem.

The author applied the requested explicit clarification that `U` consists of balanced nominations. This resolves the only presentation issue found. The reduction does not claim that optimizing the remaining deterministic envelope network over arbitrary `U` is polynomial, or that a general compact set has an effective representation.

## 5. Cactus pressure comparisons

The first finite identity applies to an arbitrary pressure objective pair `s,t`. On a cactus, its unit electrical current signs are fixed by the graph for every such pair. Choosing maximum edge laws for positive current signs and minimum edge laws for negative signs makes `j^T d>=0`. There is no separate target-law subtraction for a pressure objective. The same independent edgewise realization proves attainment. Reversed envelope choices give the minimum.

Thus the cactus pressure consequence follows from the same finite identity and the established cactus sign property. It is structurally valid for the stated compact continuous edge-law families. It makes no computational representation claim for those general families.

## Verification and scope

I reran the finite-identity checker: all 240 target-edge identities passed on series-parallel and `K4` networks, with maximum discrepancy `8.03e-15`. This is consistent with the exact identity's graph-independent validity; only the fixed-sign comparison uses the series-parallel hypothesis.

Replacing the quadratic theorem's structural proof does not change its convex cubic energy, SOCP representation, rational oracle algorithm, error bounds, or endpoint recovery. Those require the explicit quadratic data and remain separately reviewed. For arbitrary continuous compact law families the conclusion is an exact structural envelope representation, with no polynomial-time claim. The finite secant identity is an elementary proof device; this audit does not establish its novelty or that of the broader envelope statement relative to circuit comparison literature.
