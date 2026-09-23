# Candidate radial upper bound for Stage 3

Status: Root derivation, pending author development and five independent reviews.
Date: 2026-09-07

For `F=U-lambda log(c-||x||^2)`, `lambda>=1`, `c-r>=4lambda`, let
`S=c-||x||^2`, `a=2lambda/S`, `D=U''`, and `t=sum_i(1-x_i^2)`.
Then `S>=4lambda+t` and `a<=1/2`.

The radial Hessian is `a I+(a^2/lambda)xx^T`. Since `D>=2I` and
`x^TD^-1x<=t/2`,

```
D <= F'' <= (1+1/4+1/8)D = (11/8)D.
```

Indeed the relative rank-one eigenvalue is at most
`2lambda t/(4lambda+t)^2<=1/8`.

By signed-permutation invariance take positive nonzero objective coordinates;
zero coordinates stay zero. With `s=log eta`, `z_i=e^s w_i`,
`b_i=2/(1-x_i^2)`, central stationarity is `z_i=x_i(b_i+a)`.
Consequently coordinates are positive and ordered with their weights.
Differentiation gives

```
(D_i+a)x_i' + x_i a' = z_i,
a' = (a^2/lambda) K / (1+(a^2/lambda)L),
K = sum x_i^2(b_i+a)/(D_i+a),
L = sum x_i^2/(D_i+a).
```

For `y=x_i^2`, the inequality `y(b_i+a)/(D_i+a)<=1-y`
reduces to `2+a(1-2y)(1-y)>0`, so `K<=t`. Therefore
`0<=a'<=4lambda t/(4lambda+t)^2<=1/4`.

Set `q_i=u'(x_i)=b_ix_i`, `v_i=q_i/sqrt(D_i)`, and
`theta_i=(log q_i)'`. Then

```
theta_i = D_i(b_i+a-a')/((D_i+a)b_i),
7/10 <= theta_i <= 5/4.
```

Here the lower bound is `(4/5)(1-1/8)`; the upper is
`1+a/b_i<=5/4`. In particular every coordinate increases.
The `v_i` are nonnegative and ordered because `x_i` are ordered and
`u'/sqrt(u'')=sqrt(2)x/sqrt(1+x^2)` increases. For the product metric
coordinates `y_i=rho(x_i)`, `y_i'=theta_i v_i`.

The standard prefix inequality with
`alpha_i=sqrt(i)-sqrt(i-1)` and `Gamma_r=||alpha||_2` now gives

```
L_F <= sqrt(11/8) int ||y'||
    <= sqrt(11/8)*(5/4) int ||v||
    <= sqrt(11/8)*(5/4) sum alpha_i int v_i
    <= sqrt(11/8)*(25/14) sum alpha_i Delta y_i
    <= sqrt(11/8)*(25/14) Gamma_r ||Delta y||
    <= sqrt(11/8)*(25/14) Gamma_r d_F(endpoints).
```

The last step uses `F''>=U''` on the whole cube, so off-path shortcuts
cannot invalidate the lower bound on ambient endpoint distance.
All constants are independent of dimension and allowed radial parameters.
Combine with the existing facet-regular lower bound to obtain an actual
`Theta(sqrt(log r))` worst-case same-endpoint distortion for this family.
The upper factor is approximately `2.093935607`, not claimed sharp.

Root numerical diagnostics tested 1200 positive points with dimensions
2, 5, 20, 100 and lambda 1, 3, 100. They confirm the displayed inequalities
but are not a proof. Reproduce meaningful deterministic/randomized diagnostics
in the final verification script if this result is adopted.

## Candidate same-accuracy extension (also requires independent verification)

There is a separate endpoint argument. Let `x_U(eta_U)` be the first
epsilon-accurate standard-box center for the same positive weights.
Since `q_i/z_i=b_i/(b_i+a)>=4/5`, the radial center at
`eta=(5/4)eta_U` has every coordinate at least `x_U(eta_U)` and is accurate.
The first accurate radial center occurs no later because all coordinates
increase as proved above.

Let `h(t)=rho((u')^-1(e^t))`. For the ordinary box profile,
`v=h'` satisfies `v'<=v` (since `u'''>=0` on the positive branch),
and integration from minus infinity gives `v<=h`. Consequently
`h(t+log k)<=k h(t)` for `k>=1`.
Also `q_i<=z_i` implies that the radial metric coordinates at this chosen
parameter are at most `(5/4)` times those of `x_U(eta_U)`.
The ordinary-box scalar dilation theorem gives
`||rho(x_U(eta_U))||<=c_star L_opt,U(epsilon)`.
Finally `L_opt,U(epsilon)<=L_opt,F(epsilon)` by metric domination.
Using the direct product-coordinate upper bound for radial arc length yields

```
L_CP,F(epsilon)
 <= sqrt(11/8)*(125/56)*c_star*Gamma_r*L_opt,F(epsilon).
```

Thus a dimension-uniform same-accuracy upper bound may also be available.
For its matching order use the already proved dyadic radial example, checking
that its central-neighborhood lower bound and geodesic upper bound imply the
corresponding arc-to-target-distance lower bound without extra assumptions.
Neither estimate is proposed for arbitrary facet-regular couplings.
