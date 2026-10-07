# Uncertain continuous polynomial flow laws on graphs of bounded block cycle rank

Date: 2026-09-05. Status: two independent proof reviews passed: [first](../notes/review-potential-flow-affine-law-uncertainty.md), [second](../notes/review-potential-flow-affine-law-uncertainty-second.md). This is a computational extension of the [bounded-block-rank nomination theorem](potential-flow-bounded-block-rank.md), [joint resistance theorem](potential-flow-joint-resistance.md), and [fixed-core optimization theorem](fixed-core-block-polyhedral-optimization.md). The novelty claim is limited to this combination and its bit-complexity consequences; general monotone flow laws and uncertain physical parameters are established models.

Only the maximum cycle rank of an individual biconnected block is fixed. Graph size, total cycle count, polynomial degrees, piece counts, and the number of independent uncertain constitutive coefficients may grow with the input. The result gives additive pressure optimization and exact arc-capacity validation, with the output distinctions stated below. It is a parameter-dependent polynomial-time result, not a practical runtime or fixed-parameter tractability claim.

## 1. Model and theorem

Fix the maximum cycle rank of a biconnected block. On a connected graph, orient each edge and impose

```
pi_u-pi_v = g_e(x_e,theta_e)
           = f_e0(x_e) + sum_j theta_ej f_ej(x_e).
```

Every basis function is a rational, densely encoded, continuous piecewise polynomial on the whole real line, with finitely many rational breakpoints. Every basis vanishes at zero. Each uncertain coefficient has an independent finite rational interval. The total number of coefficients, pieces, and degrees may grow with the input; dense encoding is essential to the degree argument below. Require every law in the coefficient box to be strictly increasing on the whole real line. Arbitrarily shifted finite rational nomination boxes, intersected with balance, are nonempty.

**Theorem.** For fixed maximum block cycle rank, one can compute a certified additive optimum-value interval and rational feasible nomination/coefficient inputs within additive `epsilon` of the maximum of any terminal potential difference, in time polynomial in the rational input length and requested precision bits. One can also compute exact maximum and minimum signed flow on any edge as real-algebraic values of polynomial encoding length, and exactly decide robust satisfaction of all rational arc-flow capacities. There are no additional flow or pressure restrictions in the physical-extremum problem. Exact arbitrary pressure-span comparison is not claimed.

An example is a positive uncertain mixture of signed integer powers and monotone hinge functions, including uncertain linear, signed-quadratic, and cubic coefficients. This is broader than multiplying a fixed law by one uncertain resistance. It excludes uncertain exponents and uncertain breakpoints, which would need different analysis.

## 2. Reduction to reviewed mechanisms

For each fixed coefficient vector, strict monotonicity and zero at zero give existence and uniqueness by strictly convex coercive energy and the uniform acyclic-flow bound `|x_e|<=B`, where `B=sum_v max(|l_v|,|u_v|)`. Each individual law is a finite-piece strictly increasing polynomial and is therefore unbounded in both directions. Use the centered analytical smoothing described in Section 6 to obtain smooth laws with derivative at least `rho>0`. The graph-only nomination face theorem for bounded block cycle rank applies without any dependence of its face family on the coefficients.

Take a joint optimum `(b*,theta*)`, whose existence follows from compactness and continuity of the unique physical flow. At fixed `theta*`, replace `b*` by an optimal nomination on the graph-only face family. This preserves the joint optimum. On each face, all but one block have fixed effective nominations. Coefficient intervals are independent across blocks, so block objectives optimize separately.

After a face and cycle coordinates are fixed, flows are affine in a fixed-dimensional core `z`. Use the common refinement of all basis breakpoints. Its inverse images are affine hyperplanes in `z`, and on each cell every basis value is a polynomial in `z`. Each uncertain coefficient is a scalar interval leaf of the fixed-core optimization theorem. Cycle equations have polynomial core coefficients multiplying these leaves; the fixed terms contribute to their polynomial right-hand sides. Potential difference has the same affine-in-leaves form. Thus the number of uncertain coefficients need not be fixed.

For exact edge-flow optimization, its endpoints lie in one block. At fixed coefficients the law is strictly increasing, so its endpoint-potential face family contains an optimal edge-flow nomination. The objective edge flow is affine in the core. Exact algebraic local optimization and pairwise comparison of face optima therefore suffice, with no sum across independent algebraic fields.

## 3. Dense-degree complexity

The fixed-core theorem states a fixed-degree version, but its proof already accommodates degree growth from common denominators; the following dense-degree strengthening was checked in both independent reviews. With maximum densely encoded degree `D`, fixed-size minors and comparison polynomials have degree `O(D)`; the common denominator products have degree `O(ND)`. At fixed total variable dimension their expanded coefficient count is polynomial in `N,D`. Their coefficient bit lengths are polynomial as well. Fixed-dimensional sign enumeration, quantifier elimination, sampling, and algebraic LP reconstruction have polynomial bit complexity in formula size, degree, and coefficient length. Since dense degree is bounded by the input length, this establishes the required strengthening. Sparse binary exponents do not satisfy this argument and are excluded.

## 4. Uniform continuity and rational input recovery

Let `N_ej` and `M_ej` be rational coefficient-sum bounds on the absolute value and derivative of basis `f_ej` on `[-B-1,B+1]`. For each polynomial piece, use coefficient-sum bounds at `T=max(1,B+1)`: `N=sum_j |a_j|T^j` and `M=sum_{j>=1} j|a_j|T^(j-1)`, taking maxima over all pieces. Put `U_ej=max(abs(theta_lower_ej),abs(theta_upper_ej))` and

```
M_e = M_e0 + sum_j U_ej M_ej,
C_b = sum_{e in a fixed terminal path} M_e.
```

The smoothed derivative resistance is at most `M_e+rho`. The ordinary unit-source/sink electrical adjoint has edge current of absolute value at most one. For the centered smooth surrogate, the coefficient derivative of the pressure objective is exactly

```
partial F_rho / partial theta_ej = j_h,e S_rho f_ej(x_e).
```

Consequently, integrating and passing to the zero-smoothing limit gives

```
|F(b,theta)-F(c,eta)|
 <= C_b ||b-c||_1 + 2 sum_ej N_ej |theta_ej-eta_ej|.
```

If the graph has no edges or all nomination bounds force zero loads, return the constant zero objective directly. Vanishing sensitivity coefficients need no rounding budget and are never used as divisors. The feasible coefficient box is convex and every intermediate law is admissible by hypothesis. Isolate algebraic input coordinates to rational intervals, recover balanced nominations by rational LP, and round coefficients within their own intervals. The displayed bound gives polynomial precision for a rational near-optimal pressure input. Recompute its unique physical flow; no exact rational physical-state output is claimed. Exact edge-flow algebraic values do not require a quantitative inverse-law modulus, and no optional rational near-edgeflow witness is presently claimed.

## 5. Polynomial-time validation of admissible law families

The law hypotheses can be checked in polynomial time in the dense model. Continuity matching and values at zero are exact rational polynomial evaluations. On each common original piece, the pointwise minimum derivative over the coefficient box is

```
f_e0'(x) + sum_j min(theta_lower_ej f_ej'(x), theta_upper_ej f_ej'(x)).
```

Discard identically zero basis derivative polynomials before root partitioning. Partition the real line further at roots of the remaining individual basis derivatives. The roots may be represented through the product of these rational polynomials, whose degree and coefficient length are polynomial in the dense input; no common algebraic field of separately represented roots is required. On every resulting interval the minimizing coefficient endpoint is fixed, so nonnegativity reduces to univariate polynomial sign tests over algebraic intervals. There are polynomially many derivative roots, and all root isolation/sign tests have polynomial bit complexity for dense univariate polynomials.

Nonnegative derivative gives monotonicity. To ensure strict monotonicity for every coefficient vector, exclude a coefficient vector whose complete derivative vanishes identically on any nonempty common original piece. For each such piece, derivative-coefficient matching is a rational linear system in the coefficients; intersect it with their boxes and test feasibility by LP. If no such vector exists, no allowed finite-piece polynomial law is constant on a nonempty open interval, which together with nonnegative derivative is equivalent to strict increase. Conversely, any failure of strict increase has such a constant subinterval and hence an identically zero derivative on one original polynomial piece. Zero-length pieces are omitted.

Both independent reviews checked this validation argument, including zero derivative polynomials and flat-interval detection.

## Literature context and limits

A 2026-09-05 open-web search for uncertain constitutive polynomial coefficients, monotone potential flow, and cycle-rank complexity returned the already-audited resistance-uncertainty papers, rather than a matching bounded-block-rank coefficient-family theorem. This is a limited search, not a novelty certificate. [Aßmann, Liers, Stingl, and Vera (2018)](https://arxiv.org/abs/1808.10241) already study polynomial robust feasibility and uncertain passive gas networks using set containment and SOS methods; their tree result is an LP and their single-cycle method reduces to linearly many polynomial subproblems. [Thürauf (2025)](https://link.springer.com/article/10.1007/s10107-025-02207-2) gives general worst-case nonlinear subproblems for robust design, rather than polynomial-time algorithms for each such subproblem. This result is presented as a computational corollary of the new graph/core theorems, while crediting these existing uncertainty models and reductions.

## 6. Why continuity suffices

No derivative matching is required at the polynomial breakpoints. Let every basis be continuous piecewise polynomial. Choose a nonnegative C-infinity mollifier `eta` supported on `[-1,1]` with integral one, and define the centered smoothing operator

```
S_rho f(x) = integral eta(t) f(x-rho t) dt
            - integral eta(t) f(-rho t) dt.
g_rho(x,theta) = S_rho g(x,theta) + rho x.
```

For each strictly increasing complete law `g`, convolution preserves increase, subtracting a constant preserves it, and adding `rho x` makes the derivative at least `rho`. Also `g_rho(0,theta)=0`. Centered convolution is linear, so coefficient dependence remains affine. All allowed flows remain bounded by `B` through acyclicity. On any compact interval, continuous finite-piece polynomials are Lipschitz; derivative bounds on `[-B-1,B+1]` give uniform convergence to the original laws as `rho` decreases to zero, uniformly over the compact coefficient box. The strictly convex energies then give uniform physical-flow convergence by compactness and uniqueness. This is sufficient for the finite-family limiting proof of nomination faces. The smooth laws need not have an algorithmically constructed polynomial representation: they are used only in the existence proof; exact local optimization uses the original piecewise polynomials.

For quantitative pressure sensitivity, convolution derivatives are bounded by the supremum of the original piecewise derivatives on the enlarged interval. Thus use coefficient-sum constants computed at `T=max(1,B+1)`; centered basis values satisfy `|S_rho f_ej(x)|<=2N_ej`. A safe uniform bound is consequently

```
|F(b,theta)-F(c,eta)|
 <= C_b ||b-c||_1 + 2 sum_ej N_ej |theta_ej-eta_ej|,
```

where `C_b` uses full-law derivative bounds on the enlarged interval. This suffices for polynomial rational recovery. The direct original limit also recovers sharper constants, but they are unnecessary. Uniform strict monotonicity validation retains the same derivative-root and per-piece LP argument; matching values, instead of derivatives, at breakpoints now verifies continuity. No fractional exponents, uncertain breakpoints, or variable-dimensional algebraic inversion are thereby admitted.

## 7. Reproducible mechanism checks

[`affine_law_checks.py`](../code/potential_flow_mpd/affine_law_checks.py) uses independent uncertain coefficients for linear, signed-quadratic, cubic, and nonsmooth monotone hinge bases. Its deterministic rank-two/rank-three graph experiments passed 40 exact rational cycle identities and 64 independent coefficient-sensitivity finite differences. The maximum derivative error was `1.50e-9`; the physical residual was `1.55e-13`. The numerical states include edges on both sides of the hinge breakpoint. These checks support the affine-leaf representation and adjoint mechanism, but do not replace the existence, global optimization, or bit-complexity proofs.

Run with `/workspace/local-home/miniconda3/envs/minlp-notes/bin/python code/potential_flow_mpd/affine_law_checks.py`.

The [exact arc-capacity result](potential-flow-exact-arc-capacity.md) supplies the one-block objective reduction and precise algebraic-output convention. Scalar resistance uncertainty is a special case of this theorem, with one basis per edge and its positive resistance interval. A fixed law is the zero-uncertainty special case. Multiple coefficients affecting one edge are allowed; a coefficient shared across different edges is outside the independent scalar model stated here. The [fractional-power arithmetic investigation](../notes/potential-flow-fractional-power-arc-barrier.md) explains why replacing polynomial pieces by arbitrary algebraic fractional powers does not automatically preserve the exact-flow conclusion.
