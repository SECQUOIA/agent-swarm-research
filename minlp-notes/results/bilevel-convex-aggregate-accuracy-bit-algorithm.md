# Accuracy-bit optimization with convex polynomial aggregate coupling

Date: 2026-09-06. Status: two independent full proof audits passed; see the
[first review](../notes/review-bilevel-reopened-nonlinear-aggregate.md) and
[second review](../notes/review-bilevel-reopened-nonlinear-aggregate-second.md).
Publication priority remains qualified by the bounded source search.
This extends the [reviewed fixed-resource theorem](bilevel-fixed-resource-accuracy-bit-algorithm.md), including its signed-marginal extension. It is a bit-complexity result; the real-algebraic global optimizer is not implemented here.

## 1. Model and claim

Fix the leader dimension `r`, aggregate dimension `s`, and resource-row count `k`. Let `X subset [0,1]^r` be a rational polytope. The input contains rational matrices `U in Q^(s by N)` and `C in Q^(k by N)`, independent of the leader, rational affine functions `ell_i(x), b(x)`, and densely encoded rational univariate strictly convex polynomial costs `f_i` on `[0,1]`. Normalize their derivatives as

```
g_i(t)=f_i'(t)-f_i'(0), G_i=g_i(1)>0,
ell_i(x) <- ell_i(x)-f_i'(0),
f_i(t) <- f_i(t)-f_i'(0)t.
```

Write `P=max_i deg(g_i)>=1` and use the normalized costs with derivative `g_i`. Let `R=max(1,max_a sum_i |U_ai|)`, and let `phi(x,w)` be a rational polynomial, densely encoded in its fixed number `r+s` of variables, convex in `w` on `W=[-R,R]^s` for each feasible `x`. Convexity is a promise; it does not require uniform positive curvature. The follower uniquely minimizes

```
F_x(z)=sum_i [f_i(z_i)-ell_i(x) z_i]+phi(x,Uz)
over z in [0,1]^N, Cz<=b(x).
```

The leader minimizes the arbitrary signed affine objective
`H(x)=d_0+d^T x+c^T z*(x)`. No extra upper constraint depends on the response.

**Theorem.** Feasible-leader existence is decidable in polynomial time. If nonempty, an exactly feasible rational leader with objective at most `OPT+2^(-B)` and a rational estimate of `OPT` to absolute error `2^(-B)` are computable in time polynomial in the dense input length, numerical degrees, and `B`, for fixed `r,s,k`. Output bit length is polynomial. No strong-convexity constant, Slater point, positive marginal coefficients, or nonsingular KKT system is required. Resource equalities may be represented by pairs of inequalities.

The quadratic aggregate `phi(w)=w^T H w/2` with rational PSD `H` is an immediate special case. The stronger statement also covers convex quartic congestion penalties and leader-dependent aggregate tariffs. The leader objective may be globally nonconvex despite follower convexity.

If `N=0`, omit the cost-degree constants and solve the affine leader problem subject to `x in X, 0<=b(x)` directly. The proof below assumes `N>=1`.

## 2. Constants inherited and added

The exact feasible-leader polytope `X'` and integer-minor constant `K>=1` are constructed exactly as in Sections 2–3 of the fixed-resource theorem. In particular, `X'` has polynomial-size rational inequalities in fixed `k`, and every `q in [0,1]^N` with `Cq-b(x)<=delta 1`, `x in X'`, admits feasible `y` with `||q-y||inf<=K delta`.

Choose a rational `Gbar>=1` bounding `||gradient_z F_x(z)||inf` on the leader and follower boxes, using absolute coefficient sums after the substitution `w=R(2t-1)`. Set `L=N Gbar` and `Lambda=max(1,K Gbar)`. The same active-normal argument supplies, at every follower optimum, resource multipliers `0<=lambda<=Lambda 1`; the fact that the objective is no longer separable does not change that normal-cone argument.

Choose a rational `L_phi>=0` such that

```
||gradient_w phi(x,w)-gradient_w phi(x,w')||inf
 <=L_phi ||w-w'||inf,  w,w' in W.
```

For example, sum absolute Hessian coefficient bounds row by row on `X times W` and take their maximum. Put

```
D=L_phi sum_i ||U_i||_1,
mu=min_i G_i/[4(4P)^P],
S=max(1,max_j sum_i |C_ji|),
A=max(1,max_a sum_i |U_ai|).
```

An empty row maximum is zero. The convex aggregate has nonnegative Bregman divergence, so the old local-cost estimate remains valid:

```
F_x(y)-F_x(z)-gradient F_x(z)^T(y-z)
 >=mu ||y-z||inf^(P+1).                                  (1)
```

All these constants have polynomial bit length. Dense degree is essential: powers such as `R^deg(phi)` have polynomial encoding in numerical degree and `log R`, even when numerically large.

## 3. Compressed certificate with aggregate mismatch

Let `h_i` be the true clipped inverse of `g_i`. For `x in X'`, `w in W`, and `lambda in [0,Lambda]^k`, define

```
q_i=h_i(ell_i(x)-U_i^T gradient_w phi(x,w)-C_i^T lambda).
```

This is the box minimizer of the separable cost with the aggregate gradient frozen at `w`. Suppose

```
(Cq-b(x))_j<=delta,
|lambda^T(Cq-b(x))|<=zeta,
||Uq-w||inf<=rho.                                         (2)
```

Then

```
||q-z*(x)||inf
 <=K delta+[(L K delta+zeta+D rho)/mu]^(1/(P+1)).           (3)
```

**Proof.** Set `a=gradient_w phi(x,w)` and `a_q=gradient_w phi(x,Uq)`. The box variational inequality for `q`, tested at `z*`, is

```
[g(q)-ell(x)+U^T a+C^T lambda]^T(z*-q)>=0.
```

Convexity of the actual follower objective therefore implies

```
F_x(z*)>=F_x(q)-lambda^T C(z*-q)
                       +(a_q-a)^T U(z*-q)
          >=F_x(q)+lambda^T(Cq-b(x))-D rho.
```

The last inequality uses follower feasibility, nonnegative multipliers, `|z_i*-q_i|<=1`, and `||a_q-a||inf<=L_phi rho`. Repair `q` to feasible `y` within `K delta`. Consequently `0<=F_x(y)-F_x(z*)<=LK delta+zeta+D rho`. Apply (1) and the nonnegative first-order term at the constrained minimizer, then the triangle inequality. This proves (3).

At an exact response choose `w=Uz*` and a bounded KKT multiplier. All three residuals in (2) vanish, and the clipped inverse formula holds. Conversely vanishing residuals identify the unique true response. Compactness of `W` and the multiplier box, and continuity of clipped inverses, prove that `z*(x)` is continuous on `X'` by the same subsequence argument as in the fixed-resource theorem. Thus `H` attains its minimum.

**Sharper residual bound.** Retain the response-distance factor in
`|(a_q-a)^T U(z*-q)|<=D rho ||z*-q||inf`. For a repaired point `y`, put `t=||y-z*||inf`. The same proof gives

```
mu t^(P+1)<=L K delta+zeta+D rho(K delta+t).
```

It follows that

```
||q-z*||inf <=K delta+max{
 [2(LK delta+zeta+D rho K delta)/mu]^(1/(P+1)),
 [2D rho/mu]^(1/P)}.                                     (3a)
```

Indeed, exceeding both terms inside the maximum would make each of the two terms on the right of the preceding scalar inequality strictly less than half its left side. With no resource residual (`delta=zeta=0`), division by the response distance gives the sharper direct bound `||q-z*||inf<=(D rho/mu)^(1/P)`. This improves the aggregate-mismatch exponent from `1/(P+1)` to `1/P`. The simpler bound (3) is sufficient for the main accuracy-bit proof.

## 4. Fixed-dimensional semialgebraic branch construction

Normalize `w=R(2t-1)`, `lambda=Lambda theta`, so all auxiliary variables
`v=(x,t,theta)` lie in the fixed-dimensional rational polytope
`Q_0=X' times [0,1]^(s+k)`.

For an error `eta>0`, the [reviewed inverse approximation lemma](../notes/certified-monotone-polynomial-inverse-approximation.md) gives polynomially many rational polynomial branches approximating each `h_i` uniformly within `eta`. Pull their rational breakpoints back through the polynomial arguments

```
a_i(v)=ell_i(x)-U_i^T gradient_w phi(x,R(2t-1))
                     -Lambda C_i^T theta.
```

These breakpoint loci are polynomial hypersurfaces, usually not hyperplanes. Compute their realizable sign conditions on `Q_0` by fixed-dimensional real algebraic algorithms. The number of sign conditions and the cost of producing samples are polynomial in the number and degrees of these polynomials, since the dimension is fixed. At each sampled sign condition choose a valid branch for every inverse, using either adjacent branch at a breakpoint. Define `Q` by `Q_0` and the closed branch-interval inequalities for all chosen branches. Every point of `Q` satisfies the corresponding branch validity conditions, even if `Q` is larger than the sampled sign condition. The resulting polynomially many compact sets `Q` cover `Q_0`, and on each set the chosen `p_i(v)` obey `|p_i-q_i|<=eta`.

This avoids enumerating exponentially many arbitrary branch combinations. It also avoids requiring closure computations for connected algebraic cells. Branch vectors arising from realizable signs suffice, and adding points whose chosen branches remain valid is harmless.

On each `Q`, form

```
E=Cp-b(x), J=lambda^T E, T=w-Up,
H_Q=d_0+d^T x+c^T p.
```

Minimize `H_Q` on the compact set

```
v in Q, E_j<=S eta, |J|<=k Lambda S eta,
|T_a|<=A eta.                                             (4)
```

A true globally optimal leader, its true aggregate, and a bounded multiplier give a point satisfying (4). Hence the winning value `V` and a winning algebraic minimizer `v*` satisfy

```
V=H_Q(v*)<=OPT+||c||_1 eta.                               (5)
```

Exact optimization and sampling need only a fixed number of real variables, including the duplicated variables in the optimality formula. Polynomial compositions and expansions have polynomial encoding in fixed dimension. No common algebraic field for the `N` exact inverse values is constructed.

## 5. Rational recovery across nonlinear branch boundaries

It is generally impossible to recover a rational point preserving a nonlinear cell: even a rational polynomial equality can require an irrational coordinate. Accordingly, preserve only membership in the rational polytope `Q_0`. Approximate the winning algebraic point `v*` by a rational `vhat in Q_0` using a containing simplex of rational vertices and rounded barycentric coordinates. Fixed dimension permits enumeration of vertices and simplices, including on lower-dimensional faces.

The approximation need not retain the branch chosen at `v*`. All subsequent error estimates use the continuous **true** clipped response `q`, not that branch polynomial evaluated outside its validity interval.

Here is an explicit sufficient modulus. Put

```
alpha=min_i (G_i/2)(eta/(2P))^P.
```

For `eta<=1/2`, changing the argument of any clipped inverse by less than `alpha` changes its value by less than `eta`. Indeed a response displacement at least `eta` would require an argument displacement at least `(G_i/2)(eta/(2 deg g_i))^(deg g_i)>=alpha`, by the reviewed inverse modulus. Clipping preserves this implication. Let `M>=1` bound the infinity-norm Lipschitz constants of all polynomial arguments `a_i` on the normalized unit cube; absolute coefficient sums give such a rational polynomial-bit bound.

Write `Ebar=S+max_{x in [0,1]^r}||b(x)||inf`, using an absolute affine-coefficient bound, and `B_b=max(1,max_j ||linear coefficients of b_j||_1)`. Choose rational recovery distance `h` strictly smaller than

```
min{alpha/(2M), S eta/(B_b+1), A eta/(2R+1),
    S eta/(Ebar+1), epsilon/[16(1+||d||_1)]}.              (6)
```

Then `||q(vhat)-q(v*)||inf<=eta`, `||b(xhat)-b(x*)||inf<=S eta`, `||what-w*||inf<=A eta`, and `||lambdahat-lambda*||inf<=Lambda S eta/(Ebar+1)`. At `v*`, (4) and inverse approximation imply true residual bounds `2S eta`, `2k Lambda S eta`, `2A eta`. Transferring these to `vhat` gives

```
delta=4S eta,
zeta=5k Lambda S eta,
rho=4A eta.                                              (7)
```

For complementarity, use
`lambda_hat^T Ehat-lambda*^T E*=lambda_hat^T(Ehat-E*)+(lambda_hat-lambda*)^T E*`,
where the two additional terms have magnitude at most `2k Lambda S eta` and `k Lambda S eta`, respectively. Here `E*` denotes the true residual, with absolute value bounded by `Ebar`. This also handles inactive constraints with large negative residuals. All logarithmic precision requirements in (6) are polynomial in input and accuracy bits.

## 6. Error ledger and output

If `c=0`, solve the leader LP over `X'`. Otherwise set

```
epsilon=2^(-B), tau=epsilon/[64(1+||c||_1)],
eta=min{1/4,tau,tau/(8KS),
        mu (tau/2)^(P+1)/(1+4LKS+5k Lambda S+4DA)}.
```

Equations (3) and (7) imply `||q(vhat)-z*(xhat)||inf<=tau`. As `p(v*)` is within `eta` of `q(v*)`, and the true clipped response changes by at most `eta`,

```
|H(xhat)-V| <=epsilon/16+||c||_1(2eta+tau)
              <=7epsilon/64 <epsilon/8.                  (8)
```

Together with (5), this gives `H(xhat)<=OPT+epsilon`. Exact membership of `xhat` in `X'` ensures follower feasibility. Equation (8) also implies `V>=OPT-epsilon/8`. Return any rational approximation of the algebraic `V` within `epsilon/16`; its absolute error from `OPT` is less than `epsilon`. Rational approximation of a fixed-dimensional algebraic output has polynomial cost here.

Only the recovered leader and optimum estimate are promised rational. The true follower response can be irrational. The algorithm does not require a rational auxiliary vector to be an exact follower optimizer.

## 7. Practical meaning and limits

The extension permits many local polynomial response laws coupled by a fixed number of aggregate congestion, production, or risk measures, plus fixed shared resource rows. For example, `phi(x,w)=a(x)w^2+b(x)w^4` with nonnegative coefficients on `X'` couples all units while allowing vanishing local curvature. A quadratic aggregate is relevant to correlated demand penalties; a quartic term models sharply rising congestion costs. These are structural examples, not validated application models.

The result is stronger than solving one convex follower quickly: it globally optimizes an independently signed leader objective, with polynomial dependence on requested accuracy bits and exactly feasible rational leader output. The theorem's dimension-dependent exponents and coarse constants do not establish a practical solver. Useful implementation work should first target quadratic or rank-one aggregates with simpler inverse laws.

Nonconvex aggregate costs are excluded from this proof. The old exact theorem for quadratic local costs can handle some nonconvex aggregate costs through an explicit global-optimality check, but approximate stationarity is insufficient here. Leader-dependent `C`, growing aggregate/resource dimensions, sparse binary degree, and arbitrary exact response-dependent upper constraints are also outside the claim.

## 8. Focused source comparison

The prior [resource accuracy-bit source assessment](../notes/bilevel-resource-accuracy-bit-novelty.md) already credits clipped inverse resource allocation, Hoffman bounds, active-normal compression, algebraic-sum approximation, and fixed-dimensional real algebraic optimization. None of these ingredients is claimed new here.

Additional open-source searches on 2026-09-06 used “bilevel optimization separable convex polynomial low rank coupling aggregate fixed dimension approximation logarithmic accuracy” and “convex separable optimization nonlinear aggregate coupling resource allocation polynomial inverse bilevel.” They located the following adjacent work:

- Jeyakumar, Lasserre, Li and Pham, [Convergent Semidefinite Programming Relaxations for Global Bilevel Polynomial Optimization Problems](https://arxiv.org/html/1506.02099), give globally convergent SDP schemes for polynomial bilevel problems, including convex followers. Their Theorem 3.5 assumes nondegeneracy and Slater conditions and establishes convergence as the relaxation order grows. Such general convergence is an antecedent for global polynomial bilevel optimization; it is not the fixed-aggregate, accuracy-bit complexity claim here.
- Ouattara and Aswani, [Duality Approach to Bilevel Programs with a Convex Lower Level](https://arxiv.org/html/1608.03260), use convex duality for bilevel reformulation. Their Sections II–IV explicitly study regularity and consistent regularization; assumption R1 is strict follower feasibility. Dual optimality compression is established; the claimed distinction here is the fixed-dimensional inverse approximation and rational-recovery complexity combination, including degenerate follower polyhedra.
- Vidal, Gribel and Jaillet, [Separable Convex Optimization with Nested Lower and Upper Constraints](https://arxiv.org/abs/1703.01484), develop efficient resource-allocation algorithms. Their primary optimization problem is the convex allocation objective rather than the signed upper response objective considered here.

No matching combined theorem was found in this bounded search. This is not a publication-priority certificate. The main technical addition relative to the repository's existing result is the aggregate-mismatch certificate (3), together with nonlinear branch construction and rational recovery that deliberately crosses branch boundaries. Both full independent audits checked these steps and passed.

## 9. Verification record

Both full proof reviews passed, including the refined residual bound, nonlinear
branch cover, rational recovery crossing branch boundaries, and response modulus.
The first reviewer also audited the existing resource and monotone-inverse
dependencies afresh. Its [independent checker](../code/bilevel_reopened/nonlinear_aggregate_review.py)
passed five irrational branch-boundary certificates, ten rational recoveries on
opposite sides of these boundaries, twenty complementarity-transfer terms, and
twenty zero-curvature aggregate cases. The second reviewer independently checked
all proof sections and the companion polynomial-upper-data interface, then reran
the author's diagnostics. Minor empty-follower and normalization clarifications
were incorporated; no substantive theorem defect was found.

The exact-arithmetic diagnostic is [nonlinear_aggregate_checks.py](../code/bilevel_reopened/nonlinear_aggregate_checks.py). It constructs instances with known rational KKT optimizers, signed aggregate/resource coefficients, a resource equality encoded by two rows, box saturation, quartic convex aggregate costs, and strictly convex local costs with zero curvature at an interior point. It checks the convexity certificate and its response consequence without a numerical optimizer. These checks supplement, and do not replace, the general proof or independent audit.

Run on 2026-09-06: 240 quadratic-local/quartic-aggregate cases, 561 zero-curvature signed-resource-equality cases, and 72 complementarity-transfer cases passed using exact rational arithmetic.

## 10. Explicit leader-response modulus

This supporting bound is useful for later constraints on the upper response. Let `B_b` bound the infinity-norm Lipschitz constant of `b`, and let `T_x` satisfy
`|F_x(z)-F_x'(z)|<=T_x ||x-x'||inf` on the unit follower cube. Absolute coefficient sums after aggregate normalization supply `T_x` with polynomial encoding. For any `x,x' in X'`, put `Delta=||x-x'||inf`. Then

```
||z*(x)-z*(x')||inf
 <=K B_b Delta+
   [2(T_x+L K B_b)Delta/mu]^(1/(P+1)).                    (9)
```

To prove this, repair `z*(x)` to a point `y` feasible at `x'`, and `z*(x')` to `y'` feasible at `x`, each within `K B_b Delta`. Optimality of `z*(x)` and the two Lipschitz estimates give

```
F_x'(y) <=F_x(z*(x))+T_x Delta+L K B_b Delta
        <=F_x(y')+T_x Delta+L K B_b Delta
        <=F_x'(z*(x'))+2(T_x+L K B_b)Delta.
```

Apply (1) to `y,z*(x')` and then the triangle inequality. This is a quantitative stability consequence of the existing Hoffman and polynomial-convexity bounds, not a separate claim of a new general sensitivity theorem.
