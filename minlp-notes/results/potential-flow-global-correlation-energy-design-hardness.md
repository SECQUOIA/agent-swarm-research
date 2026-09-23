# Strong hardness of minimum pressure-drop and dissipation design on a cactus

Date: 2026-09-05. Status: verified by two independent full mathematical audits, with a completed bounded source assessment. The Max-Cut and concave energy mechanisms are classical; the restricted passive-network realization remains a qualified contribution.

## Theorem

Under fixed unit source/sink nominations and the common quadratic passive law, minimizing the source-to-sink potential difference over a globally correlated rational resistance polytope is strongly NP-hard on a connected simple cactus of maximum degree three. All resistances lie in [1,3], the orientation is a DAG, and all physical flows are strictly positive. The same objective is total constitutive dissipation sum_e beta_e |x_e|^3.

An explicit restricted family has NP-complete weak upper-threshold design feasibility. Absolute-error 1/256 approximation of the minimum value, or a rational design with objective at most OPT+1/256, is NP-hard with these bounded physical data. No extra numerical scaling is needed.

## 1. Remove the variable bridge-energy bias

Start from the [reviewed paired-triangle total-flow construction](../results/potential-flow-global-correlation-total-flow-hardness.md), based on an unweighted comparison graph with n vertices, m>=1 edges, and theta_i in [0,1]. Replace its initial n bridges by 2n bridges in series: for each i use a pair with resistances

    r_i=1+theta_i,  s_i=2-theta_i,
    r_i+s_i=3.

These are actual edge-resistance coordinates with rational linear constraints. They both lie in [1,2]. The plus and minus triangle path resistances remain 2+r_i-r_j and 2-r_i+r_j, respectively; both edges of each two-edge path share that value. Their alternate single edge and every joining bridge have fixed resistance two.

The resulting global resistance polytope is still the injective affine image of the theta cube, described by bounded integer coefficients and fixed-alphabet constants. All bridges carry unit flow, so each initial pair contributes constant dissipation three. This correction is essential: an unpaired bridge would add r_i and bias the objective by a linear function of theta.

The graph has |V|=6m+2n, |E|=8m-1+2n and cycle rank 2m. It remains a simple degree-three cactus with a DAG orientation and strictly positive physical flows. Put the fixed nominations +1 and -1 at its first and last vertices.

## 2. The triangle pressure drop is strictly concave in its resistance parameter

A triangle with path resistance s on each of its two path edges and resistance two on its alternate edge has path flow f(s)=1/(1+sqrt(s)). Its source-to-sink potential drop and its total dissipation under unit through-flow equal

    e(s)=2s/(1+sqrt(s))^2.

Indeed, the two path edges have total drop 2s f(s)^2, the alternate edge has drop 2(1-f(s))^2, and both agree. Summing beta x^3 over the two paths gives that common drop times the total through-flow one.

Differentiation gives

    e'(s)=2/(1+sqrt(s))^3,
    e''(s)=-3/[sqrt(s)(1+sqrt(s))^4]<0.

Thus e(2+delta)+e(2-delta) is concave and even in delta. At binary theta its value is

    A_E=2e(2)=24-16sqrt(2)     for an uncut comparison edge,
    B_E=e(1)+e(3)=13/2-3sqrt(3)  for a cut comparison edge.

The decrease kappa_E=A_E-B_E is positive. The exact rational bounds sqrt(2)<283/200 and sqrt(3)>173/100 give

    kappa_E=35/2-16sqrt(2)+3sqrt(3)>1/20>1/32.

## 3. Exact Max-Cut identity

Total dissipation is a concave function of theta, since it is a sum of the preceding concave affine compositions plus constant bridge contributions. A concave function on a cube has a minimizing vertex, by successively moving each coordinate to a nonincreasing endpoint. At a binary theta the value is

    E(theta)=C_E-kappa_E cut(theta),
    C_E=3n+4m-2+m A_E.

Therefore

    min E=C_E-kappa_E MaxCut(H).

For any conserved passive state, sum_e beta_e |x_e|^3=pi^T b. Here only unit source/sink nominations are nonzero, so this quantity equals pi_source-pi_sink. Consequently the same identity proves hardness of minimizing that prescribed potential difference. It is not an arbitrary weighted-potential objective.

## 4. Thresholds, encoding, and approximate designs

For a target 1<=K<=m choose a rational tau satisfying

    |tau-[C_E-kappa_E(K-1/2)]|<=1/512.

Dyadic approximations to sqrt(2),sqrt(3) of width at most 1/[65536(m+1)] suffice. The resulting denominator is O(m+1), and the numerator is polynomial in m+n. Every other network or uncertainty coefficient has bounded magnitude, so numerical data remain polynomially bounded under unary encoding.

If MaxCut(H)>=K, the minimum is below tau-7/512. If MaxCut(H)<=K-1, it is above tau+7/512. Hence weak design feasibility E<=tau is strongly NP-hard, and absolute-error 1/256 minimum-value approximation is NP-hard. On this explicit family, a minimizing binary theta is a polynomial certificate, and its value belongs to the fixed field Q(sqrt(2),sqrt(3)); exact comparison is polynomial. Thus weak-threshold feasibility is NP-complete on the stated family. The same fixed yes/no comparison graphs used in the reviewed total-flow reduction handle trivial source inputs.

A rational near-optimal design with loss at most 1/256 also decides the source. In a yes instance its energy is below tau-5/512; in a no instance every design is above tau+7/512. Approximate its physical energy to error 1/512 by separately enclosing the rational-profile triangle roots and summing the rational bridge energies. This uses polynomial precision and avoids exact comparison of an arbitrary radical sum.

The result gives no fixed relative-error or normalized-objective hardness claim. General concavity of energy and the use of convex/concave cube vertices are classical; the contribution under consideration is the precise bounded passive-network realization and objective scope.

The term dissipation denotes the mathematical quantity `sum_e beta_e |x_e|^3=b^T pi`. If a gas model uses squared pressure as its potential, the potential difference is a squared-pressure difference; this identity does not identify the quantity with literal compressor power.

## Verification and source scope

Both [the first full audit](../notes/review-potential-flow-global-correlation-energy-design-hardness.md) and [the second full audit](../notes/review-potential-flow-global-correlation-energy-design-hardness-second.md) passed. They checked the bridge-bias cancellation, exact energy and potential identities, strong numerical bounds, threshold directions, and rational near-optimal design semantics.

The [focused source assessment](../notes/potential-flow-global-correlation-energy-novelty.md) compares classical resistance-energy concavity, earlier effective-resistance design hardness, and the April 2026 potential-flow network-design paper. It found no matching restriction to this bounded positive cactus with an explicit global resistance polytope. Quadratic nonlinearity is not essential to the general hardness mechanism: the same paired-triangle strategy also works with linear resistor laws. The result is retained for its precise quadratic passive-network and optimization scope, without claiming a new concavity principle or exhaustive publication priority.

## Reproducible checks

[`global_correlation_energy_checks.py`](../code/potential_flow_mpd/global_correlation_energy_checks.py) passed 1,197 energy and source-to-sink drop scenarios across all 63 nonempty four-vertex comparison graphs. It checked the actual paired-bridge topology, resistance bounds, constant prefix dissipation, triangle energy/drop identity, the binary cut formula, and concave endpoint domination for additional fractional profiles. It also checked 192 rational threshold gaps. The largest local energy/drop discrepancy at 90-digit precision was below `3.69e-91`. Threshold construction and bridge cancellation were checked with exact rational arithmetic.
