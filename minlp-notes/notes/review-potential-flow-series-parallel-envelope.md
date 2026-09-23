# Independent review: a single envelope network for arc extrema

Date: 2026-09-05. Reviewer: `potential_flow_review`.

**Verdict: PASS for the stated mathematical and polynomial-bit approximation claims.** Reviewed [the full candidate](potential-flow-series-parallel-envelope-optimization.md), its [adjacent-terminal sign premise](potential-flow-series-parallel-arc-hulls.md), and the cited primary graph and convex-optimization statements. This review does not establish novelty relative to nonlinear circuit tolerance theory.

The hypotheses matter: fixed balanced rational nominations; a connected undirected graph without a `K4` minor; independent positive rational resistance intervals or explicitly listed finite positive rational sets; quadratic passive laws; and no additional scenario constraints on physical flows or potentials. Block cycle rank is unrestricted. The result provides an exact envelope identity and polynomial-bit additive value and endpoint-scenario outputs. It does not provide polynomial exact threshold decisions.

## 1. The electrical signs and homotopy

The target objective is the signed flow on an existing edge `a=(s,t)`. This adjacency permits use of [Eppstein's Lemma 9](https://www.ics.uci.edu/~eppstein/pubs/Epp-IC-92.pdf): the biconnected series-parallel block containing that edge has a two-terminal series-parallel decomposition with terminals `s,t`. Positive-resistance electrical current on a two-terminal decomposition has a fixed direction on every branch, by induction through series and parallel compositions. Off-block currents vanish. A target bridge is covered separately by conservation. This classical premise does not require bounded block rank.

Solving the rational unit-resistance electrical network computes all signs in polynomial bit time. In particular, this uses exact signs of rational currents, not floating-point signs of potentially small currents. The unit-source/sink current on `a`, in the target orientation, belongs to `[0,1]`.

To verify the homotopy derivative, orient the incidence matrix so that `A x=b` and `A^T pi=g(x)`. Under a law perturbation `d`, differentiation gives

```
A dx=0,
A^T d(pi)=R dx+d,
```

where `R` is the positive diagonal matrix of differential resistances. If `j` is the unit electrical flow from `s` to `t`, then

```
d(pi_s-pi_t)=sum_e j_e d_e.
```

Differentiating the target law as well yields

```
dx_a = [sum_(e!=a) j_e d_e - (1-j_a)d_a] / R_a.
```

Thus the candidate's own-edge term has the correct sign and factor. For the simultaneous interpolation toward the maximizing envelope, `d_a<=0`; on other edges `d_e>=0` when the fixed adjoint sign is positive, and `d_e<=0` when it is negative. Every numerator term is nonnegative. This argument permits the physical flow signs to change during the homotopy because the pointwise envelope inequalities hold for every scalar flow value.

Adding `rho*x` to every law gives `R_a=(g_a^t)'(x_a)+rho>0`. The added term is independent of the interpolation parameter and contributes nothing to `d_e`. The asymmetric quadratic envelopes are already C1, so this ordinary linear regularization is sufficient; centered convolution is unnecessary here. The author was asked to make the `+rho` explicit in the displayed denominator while discussing the regularized calculation.

Existence, uniqueness, and convergence as `rho` tends to zero follow from strictly convex energy and the uniform acyclic-flow bound. Therefore the comparison passes to the original laws despite their zero derivatives at zero. Reversing all envelope choices reverses the comparison for the minimum.

## 2. Exact scenario realization

For every envelope flow coordinate, its envelope drop equals the original quadratic drop at one of the two allowed resistance endpoints. At zero either endpoint works. Choosing these endpoints independently reproduces the entire envelope constitutive system at its own physical state, including all conservation and potential equations. Uniqueness identifies that state as the physical state of the selected endpoint scenario.

The envelope upper or lower bound is consequently attained within the original scenario set. Finite positive sets need only contain their extrema; their interior values have no role in the construction. The envelope itself may change coefficient between positive and negative flow, but that is an auxiliary deterministic law, not an assertion that a physical scenario may vary its resistance with flow.

For a zero-adjoint edge, selecting an arbitrary fixed endpoint law does not affect the comparison. Its envelope state is still realized by that same endpoint. For a target bridge the formula gives zero derivative, in agreement with its fixed conservation-determined flow.

## 3. Convex energy and the conic lift

The integral of the asymmetric law is the stated positive piecewise cubic energy. Its minimizer over conservation equations is unique. Splitting flow into nonnegative `p,n` is exact: if both are positive, decreasing both by their minimum preserves conservation and strictly decreases the objective.

For `z>=0`, the proposed lift

```
z^2<=w,
w^2<=u*z,
u,w>=0
```

projects exactly to `u>=z^3`. If `z>0`, combine the two inequalities and divide by `z`; conversely choose `w=z^2`. At `z=0`, the second inequality forces `w=0` and permits every `u>=0`. Both inequalities are rotated second-order cone constraints using rational constants. The objective coefficients `c_e^+/3,c_e^-/3` are positive, so the cubic epigraphs are minimized to equality. The conic representation has linear size.

No general assertion about exact SOCP solvability or conditioning is used for the bit-time theorem. The separate bounded convex-oracle argument supplies that guarantee.

## 4. Polynomial-bit optimization

When `b=0`, all physical flows vanish. Otherwise let `B=sum|b_v|`. The directed support of a passive physical flow is acyclic, so each edge carries at most the total positive nomination `B/2` in absolute value.

In fundamental-cycle coordinates, chord coordinates equal the corresponding physical flows because the particular tree-supported flow is zero on chords and the cycle matrix has an identity chord submatrix. Hence the true minimizer lies in `[-B/2,B/2]^k`, inside the optimization cube `[-B,B]^k`. The spanning-tree construction, cycle matrix, and particular flow all have polynomial rational encoding length. The tree case needs no optimization.

On the larger cube, `|x_e|<=(m+1)B=R` is a valid loose bound. A cycle-gradient coordinate sums at most `m` law values, each bounded by `beta_U R^2`. Thus `G0=m beta_U R^2` bounds every coordinate, and `G=1+m G0` safely bounds the Euclidean gradient norm because `k<=m`.

Function values and gradients at rational inputs use exact rational arithmetic of degree at most three. Both signs and values are computable with polynomial bit cost. The sublevel separation argument is valid: for a point with `E(z)>t`, convexity makes the gradient separate it from `E<=t`. A zero gradient at such a point certifies that the sublevel is empty. The proposed ball of radius `min(B/4,delta/(2G))` about the optimum lies in the cube and within an objective gap `delta`. All radii, objective bounds, and requested accuracy have polynomial binary encoding length.

There is also a direct application of [Dadush's Theorem 2.5.9](https://homepages.cwi.nl/~dadush/papers/dadush-thesis.pdf), printed page 48: the cube is a centered convex body with explicit rational inner and outer radius bounds. Continuing each scalar energy affinely beyond `[-R,R]`, with its endpoint tangent slopes, preserves convexity and C1 matching and produces a globally Lipschitz rational evaluation oracle. This continuation leaves the objective unchanged on the cube. The theorem returns a rational feasible point and an additive objective enclosure in time polynomial in the input encodings. The thesis explicitly defines its polynomial-time convention in terms of input lengths, so this is logarithmic dependence on the reciprocal requested accuracy, rather than dependence on that reciprocal itself.

This route also avoids any ambiguity about ellipsoid feasibility at an irrational exact minimizer. The rational returned cycle coordinates give a flow satisfying conservation exactly. Unbounded cycle rank increases the dimension of an ordinary convex problem; it does not trigger fixed-dimensional real algebraic optimization.

## 5. From energy to a certified flow interval

Subtracting `beta_L*x*abs(x)` from either asymmetric envelope law leaves an increasing function. The scalar inequality

```
(u*abs(u)-v*abs(v))*(u-v) >= |u-v|^3/2
```

therefore gives the claimed strong monotonicity bound. On the segment from the physical minimizer `x*` to a feasible flow `y`, the first-order energy term vanishes because its gradient is a potential vector and `y-x*` is a circulation. Integrating the scalar bound along this segment contributes `integral_0^1 t^2 dt=1/3`, giving

```
E(y)-E(x*) >= (beta_L/6) sum_e |y_e-x*_e|^3.
```

Thus energy tolerance `beta_L*eta^3/6` guarantees coordinate error at most `eta`. The rational interval `[y_a-eta,y_a+eta]` is a certified enclosure. Cubing a rational accuracy parameter and dividing by the positive rational resistance lower bound preserves polynomial encoding length.

## 6. An allowed endpoint witness without exact signs

The endpoint chosen using the approximate flow can disagree with an endpoint agreeing with the envelope state only on an edge with `|x*_e|<=eta`. Its constitutive residual there is at most `(U_e-L_e)eta^2<=beta_U eta^2`. This also covers an approximate coordinate equal to zero and either endpoint convention at zero.

Let `h_e` be the chosen endpoint law, let `x'` be its physical flow, and let `Delta=x'-x*`. Both states have the same nomination, so `Delta` is a circulation. Orthogonality to the two potential vectors gives

```
sum_e [h_e(x'_e)-h_e(x*_e)] Delta_e
 = -sum_e [h_e(x*_e)-g_envelope,e(x*_e)] Delta_e.
```

Strong monotonicity and the residual bound imply

```
(beta_L/2) ||Delta||_infinity^3
 <= m beta_U eta^2 ||Delta||_infinity.
```

The resulting factor `sqrt(2m beta_U/beta_L)` is bounded by the candidate's rational choice `C0=1+2m beta_U/beta_L`. Taking `eta<=epsilon/C0` therefore guarantees an allowed rational endpoint scenario whose actual target flow is within `epsilon` of the exact extremum. Taking `eta<=epsilon/2` simultaneously guarantees the enclosure width. Computing the exact physical state of the witness is unnecessary for this proof or output contract.

## Verification and remaining scope

I reran the supplied checker successfully: 3,840 endpoint scenarios, 24 envelope extrema, 72 approximate-sign recoveries, and 72 energy inequalities passed. The largest envelope discrepancy was `4.05e-15`, and the largest reconstructed endpoint-state discrepancy was `5.47e-15`. These numerical checks supplement the proof audit.

No substantive mathematical correction was needed. The author applied the requested explicit linear regularizer in the homotopy denominator during this review. The candidate's novelty caution should remain: the current-sign theorem and convex-optimization machinery are established, and the envelope consequence still requires comparison with nonlinear circuit tolerance literature before a newness claim.
