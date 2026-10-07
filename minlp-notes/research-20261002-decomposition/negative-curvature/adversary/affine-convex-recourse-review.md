# Independent review of affine convex recourse

Date: 2026-10-02. Scope: the actual saved
[affine-convex-recourse.md](../affine-convex-recourse.md).
Verdict: no substantive mathematical gap found in the scoped theorem.

The theorem gives a verifiable sufficient class for eliminating positive
curvature. It does not prove that an arbitrary sparse quadratic admits
the required affine responses, residual width, or positive-diagonal bound.
Those restrictions are stated explicitly and are essential.

## Certificate and elimination

The lower/upper multiplier convention is consistent: stationarity is
`grad_y f=ell-u`. Expanding about the affine feasible response gives a
PSD quadratic plus `(ell-u)'(y-ybar)`. Complementarity changes the latter
exactly into `ell'(y-l)+u'(u_bound-y)`. Thus the displayed identity proves
global conditional optimality throughout the box, including singular PSD
blocks and zero multipliers. It does not need strict complementarity.

The verification method is sufficient. Affine range tests prove signs and
feasibility everywhere on the parameter box; coefficient identities prove
stationarity and complementarity. Fixed parameter coordinates must be
substituted first, as the note requires. A certificate obtained at one
sample parameter cannot pass these tests merely by being valid there.

Direct substitution gives the reduced Hessian
`A+B'CB+B'D+D'B`. Every reduced block is supported on its entire attachment
set, so the supplied residual decomposition must contain that set in a
bag. This guards against unnoticed elimination fill. The polynomial
encoding claim is valid for rational matrix products, sums, and the
proposed rational linear solves; certificate encoding is correctly
included in the input size.

## Conditioning and output

Original point growth restricted to the affine lift gives precisely the
metric `I+sum E_t'B_t'B_tE_t`. No inverse response estimate is needed.
Uniqueness transfers to the retained optimizer, and the assumed original
uniqueness forces the certified lift at that point to be its private
coordinates. The expanded rational optimizer follows by substitution.

The negative-curvature pullback `H_red >= -nu M` is correct but cannot
control a positive diagonal. The additional inequalities (12) or (14)
supply exactly that missing control. In the diagonal variant, `M>=D`
and `1<=r_i^2 D_ii<4` give transformed growth at least `g` and diagonal
curvature at most `4 C0 beta <8 C0 nu`. The graph is preserved, while the
coordinate box changes rationally. The cited filtered-grid result permits
such rational product boxes. These calculations establish the parameter
bound under the stated certificate, not from negative curvature alone.

The endpoint-rounding fallback for nonpositive reduced diagonals is also
correct. Each coordinate section is concave or affine, so an endpoint
choice cannot increase the objective. Successive choices produce a
globally optimal vertex from some optimizer. Standard two-label dynamic
programming on the supplied bags then obtains the optimum without a
growth premise.

The guarantee that growth need not be input is inherited from the cited
filtered-grid theorem. This review checked that the reduced problem meets
the stated inputs, but did not independently re-prove that earlier
algorithm or its full certificate format.

## Separating family

In the ladder family, the scalar inequality
`v(3-t-2v)>=0` holds for `t in [-1/3,2/3]` and `v in [0,1]`, giving
the claimed unique retained optimizer and growth. The lifted squared
distance is bounded by `3||u-a||^2+||v||^2+2||y-u||^2`, which is at most
`3F` when `M0>=1`.

The residual Hessian splits into the two-by-two matrix with eigenvalues
`+sqrt(5),-sqrt(5)` and the common path-Laplacian shift. Since the largest
shift is at most one half, it has exactly `m` negative eigenvalues. Schur
congruence through the positive private block preserves that count in the
original Hessian. A penalty-free lift increases squared norm by at most
a factor two, proving the lower bound `nu>=sqrt(5)/2`. The positive
diagonal bound `L_red<=9/4`, the full growth constant `1/3`, and the
condition `L_red<=3 beta` are consistent. Arbitrarily large `M0` enters
only the original positive curvature and its encoding length.

This is a useful algebraic separation of parameter regimes, not empirical
evidence of solver improvement; the family has the simple certificate
shown in the note.

## Verification scope

This review is an independent read-through and algebraic derivation of
the saved theorem. The reviewer also inspected the exact-arithmetic checker
and ran

```sh
python3 -B research-20261002-decomposition/negative-curvature/check_affine_convex_recourse.py
```

It passed eight valid certificates, 1,518 exact elimination identities,
five invalid-certificate rejections, 1,440 family growth checks, and 18
family matrix cases. The exact Schur PSD routine permits singular pivots;
the complementarity routine checks all affine-product coefficients.
The tests cover sampled rational parameters and finite families; they do
not run global search, prove universal growth by sampling, or implement
the full fixed-parameter algorithm. The rational `9/4` Hessian shift used
by the family checker supports a slightly weaker negative-curvature bound
than the analytic `sqrt(5)` calculation, as the code states.

The review neither asserts publication priority nor changes the open
status of the general negative-curvature target. No project-wide
verification or CI inspection was performed.
