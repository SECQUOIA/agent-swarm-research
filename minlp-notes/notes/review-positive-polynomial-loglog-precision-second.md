# Second review: positive polynomial precision with log-log degree overhead

Date: 2026-09-05. Reviewer: `constant_rank_review`.
Reviewed note: `notes/positive-polynomial-loglog-degree-precision.md`.
Verdict: **PASS** for the supporting scalarization, degree-independent
lower bound, layered rational construction, and stated finite constants.

This audit checks mathematical correctness and polynomial rational
complexity. It does not establish publication priority for the result
or for its classical convex-analysis and formulation ingredients.

## The supporting scalar allocation has exactly the same optimum

The allocation feasible set is compact and contains a strictly positive
point with all coordinate caps strict and image in the interior of `K`.
Its optimal product is positive, so every maximizing allocation is
strictly positive. Maximizing the log product is therefore legitimate.

The same strictly feasible point qualifies the normal-cone sum rule for
the cap and image constraints, and the normal-cone chain rule for the
linear preimage of `K`. The gradient `1/p*` lies in the normal cone of
the feasible set at an optimum. The displayed equation

```
1/p_i*=(C^T lambda)_i+mu_i,
mu_i>=0,       mu_i(p_i*-1)=0
```

has the correct sign for maximization and the upper coordinate caps.
No lower-cap normal is present because `p*>0`. No smoothness of `K`,
full row rank of `C`, or rational multiplier representation is required.

The multiplier sign argument is valid. Since `C>=0` and `p*>0`, its
image `z=Cp*` is nonnegative. If `z_j>0`, unconditionality and convexity
allow a small decrease of coordinate `j` within `K`; the outward normal
inequality then forces `lambda_j>=0`. If `z_j=0`, the corresponding row
of `C` is zero. Setting such normal components to zero leaves `C^T lambda`
and `lambda^T z` unchanged. It preserves normality because unconditional
support functions satisfy `h_K(lambda)=h_K(|lambda|)` and are monotone
in the absolute coordinate magnitudes. The new support value can only
decrease, while it remains at least its value at `z`, which equals the
old support value. Thus equality and the normal condition remain valid.

With `A=C^T lambda>=0` and `b=lambda^T Cp*=h_K(lambda)`, the old
optimum lies on the new scalar constraint. Concavity of the log product
gives, for every positive point feasible for the new capped allocation,

```
sum log p_i-sum log p_i*
 <=A^T(p-p*)+sum mu_i(p_i-p_i*)<=0.
```

The second term is nonpositive because a positive cap multiplier requires
`p_i*=1`. Zero-product points cannot improve a positive optimum. Hence
the scalar allocation optimum is exactly `D_alloc`, rather than just a
relaxation with a comparable value. If `lambda=0`, every cap is active
and `D_alloc=1`, making the lower bound trivial. An index with `A_i=0`
also has `p_i*=1`. All zero-row and zero-weight cases are accounted for.

## The scalarized shape gives a degree-independent lower bound

For `A_i>0`, the coefficients of `phi_i` are nonnegative and sum to one.
Thus it maps `[0,1]` strictly increasingly onto itself, and so does its
square root. The latter is convex: its vector representation has
components `sqrt(d_ik)x^(k/2)`, which are nonnegative convex functions
because `k>=2`. Coordinatewise monotonicity and convexity of the Euclidean
norm on the nonnegative orthant prove convexity of their norm. This
argument includes mixtures of exponents and does not need differentiability
at zero. For `A_i=0`, nonnegative coefficients ensure the scalarized
polynomial has no contribution from that coordinate; choosing the identity
map there is valid.

For a nonnegative convex function, squaring its midpoint convexity
inequality and subtracting from the average of its squared endpoint
values gives exactly the factor `1/4` in inequality (5). Consequently
the same fixed coordinate homeomorphism sends all parity supports into
the unit cube and makes their scalarized Jensen bounds quadratic:

```
(1/4)sum_i A_i(t_i-s_i)^2<=lambda^T J<=b.
```

Compact closures preserve this pairwise inequality. Uniform sampling in
the transformed support gives
`(1/2)sum_i A_i Sigma_ii<=b`. The coordinates of
`p_i=Sigma_ii/2` are at most `1/8`, so this is a feasible scalar
allocation, including zero `A_i`. Equality of allocation optima then
bounds its product by `D_alloc`. Hadamard and the established
volume-covariance inequality give the stated support-volume factor
`2^(r/2)omega_r(r+2)^(r/2)`.

The transformed compact supports cover the entire cube because the map
is a homeomorphism, so the lower bound follows without a Jacobian or
volume-preservation assertion. Multipliers and the coordinate transform
are proof devices only; their possible irrationality does not enter the
construction. The bound `A_r<7r/2` is the same checked Gaussian estimate
as in the pure-power theorem.

## Every layer has uniformly bounded local curvature

The `J+1` displayed intervals cover `[0,1]`, overlap only at endpoints,
and have positive dyadic lengths. On the final interval the normalized
second derivative is at most `D^2*2^(-2J)<=1`. On earlier intervals,
the upper endpoint is `1-s`, with `s<=1/2`.

For `k=2`, curvature is at most `1/2`. For `k>=3`, putting
`v=(k-2)s` gives

```
k(k-1)s^2(1-s)^(k-2)
 <=(v+1)^2 exp(-v)<=4/e<2.
```

The first inequality uses `ks=v+2s<=v+1` and
`(1-s)^(k-2)<=exp(-v)`. The second follows by maximizing the scalar
function on `v>=0`. Thus summing with nonnegative coefficients gives
local normalized curvature at most `2C_ji`, with no degree-dependent
constant left in the approximation error.

## Layer selectors add no hidden integer variables

At an integer assignment of the `S` layer bits, every selector assigned
to a different string has an upper bound of zero. If a string is used,
the sum equation forces its unique matching selector to one. An unused
string forces all selectors to zero and is infeasible. Thus all selectors
are exactly binary at integer-feasible points, despite being continuous
variables in the model.

Their four-inequality product formulations are therefore exact at every
integer-feasible point. Fractional selector values may occur in the LP
relaxation, which does not affect the graph guarantee for the mixed-integer
projection. The product bounds needed in the recurrences are valid.
For `v` bounded by one or by `h_i`, the intermediate `a_0 v` has the
same safe bound because `a_0 in [0,1]`; it can be used as a bounded
continuous argument in the subsequent selector products.

For the selected layer, the equations reduce exactly to
`a=ell+s a_0`, `rho=s eta`, and `x=a+rho`. Prefix and residual bounds
give `a_0+eta<=1`, so the whole segment from `a` to `x` stays within
that layer. Expanding multiplication by `a` as displayed makes both
power recurrences exact by induction. Bounds `0<=v_k<=1` and
`0<=t_k<=h_i` follow from `a<=1` and `rho<=h_i`.

When `L_i=0`, the prefix is zero and there are no precision bits; the
remaining multiplications use only the implied-binary selectors and still
give the exact powers of the selected layer's left endpoint. Thus the
zero-depth case is included without introducing any extra integer.

The claimed per-coordinate row and variable count follows: each power
recurrence requires `O(L_i)` prefix products and `O(J_i+1)` selector
products, while selector activation requires `O(J_i S_i)` inequalities.
The independent coordinate constructions share outputs through linear
equations and do not enumerate the Cartesian product of their layers.

## Error, constants, and rational complexity

The prefix Taylor expression has the correct first-order term
`k a_i^(k-1)rho_i`. Applying the local normalized curvature bound over
residual length at most `h_i` gives remainder at most `C_ji h_i^2`.
Hence `0<=f-T<=Cp`. The rectangle with endpoints `T` and `T+Cp`
contains the exact graph and permits only errors with coordinate
magnitudes at most `Cp`. Unconditionality supplies the whole-body
guarantee, without a finite exact linear description of `K`.

The allocation optimum gives the finite count `Phi+r+sum_i S_i`.
The reviewed rational allocation oracle adds at most `1/(2 ln 2)`.
Combining this with `A_r<7r/2` gives exactly

```
p_out<=p_conv+(9r/2)+sum_i S_i+1.
```

All layer endpoints are dyadic with `O(log D_i)` bits, and `J_i,S_i`
are computed by integer comparisons. Positive rational allocation bounds
make every `L_i` polynomial in the full encoding. Recurrence coefficients,
product bounds, and output sums retain polynomial bit length. Numerical
degree enters continuous size and construction time through the exact
power recurrences, consistent with dense input. There is no hidden
requirement to compute the scalarizing multipliers or shape functions.

I inspected and reran `code/quadratic_rank/check_positive_polynomial_loglog.py`.
All 276 convex-square-root checks, 1,021 exact layer curvature bounds,
1,021 exact prefix/Taylor checks, and 30 scalarization KKT cases passed.
The checks include zero-depth prefixes. They supplement the universal
proofs above. No unresolved mathematical or encoding defect was found.
