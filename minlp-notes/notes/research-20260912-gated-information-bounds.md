# Bounds for using a gated full inverse in measurement selection

Status: [independently reviewed](research-20260912-gated-bound-independent-review.md),
with the domain clarifications applied. These are consequences and sharp
examples built on the classical operator Kantorovich inequality and block
inversion. They are not claimed as new matrix inequalities. Their use is to
quantify the statistical discrepancy documented in
[the source audit](research-20260912-measurement-source-audit.md), and to give
certificates that remain meaningful when correcting a selection model.

Let a Gaussian mean observation model have sensitivity matrix `F` and known
parameter-independent noise covariance `R>0`. For a selected set `S`, define

```text
M(S) = J0 + F_S^T R_SS^{-1} F_S,
G(S) = J0 + F_S^T (R^{-1})_SS F_S,
```

with a common prior `J0>=0`. Require positive definite information when using
logdet or inverses. The feasible family of selections is finite, nonempty, and
the same in the two optimization problems; its constraints are otherwise
arbitrary. `M` is the actual marginal information; `G` is the gated expression.

## Uniform comparison

If `0<m<=M` and `mI <= R <= MI`, write `kappa=M/m` and

```text
alpha = (M+m)^2/(4Mm) = (kappa+1)^2/(4kappa).
```

For every selection,

```text
M(S) <= G(S) <= alpha M(S).                              (1)
```

The first inequality follows from the Schur complement. For the second,
functional calculus gives

```text
R + Mm R^{-1} <= (M+m) I.
```

Compress to the selected coordinates, writing `A=R_SS` and
`K=(R^{-1})_SS`. Then

```text
K <= ((M+m)I-A)/(Mm) <= alpha A^{-1}.
```

The last inequality follows on each eigenvalue `t>0` of `A` from
`t(M+m-t) <= (M+m)^2/4`. Congruence by `F_S` and `J0<=alpha J0`
prove (1). This is the standard inverse-compression form of the operator
Kantorovich inequality, with an elementary proof included for reproducibility.
A source for attribution is
[New Refinement of the Operator Kantorovich Inequality](https://www.mdpi.com/2227-7390/7/2/139),
which states the underlying inequality and its predecessors.

The certificate can use a diagonally rescaled covariance instead. If `D` is
positive diagonal, replacing `(R,F)` with `(DRD,DF)` leaves both `M(S)` and
`G(S)` unchanged for every coordinate subset. Thus covariance conditioning in
arbitrary physical units need not be used. Normalizing each marginal variance
to one supplies a simple reproducible choice. Seeking a better scaling is a
separate, established diagonal-preconditioning problem.

## Consequences for optimizing a selection

Let `S_G` maximize `logdet G(S)` and let `S_M` maximize `logdet M(S)`.
By (1) and monotonicity,

```text
logdet M(S_G) >= logdet M(S_M) - p log(alpha),             (2)
```

where `p` is the information-matrix dimension. Equivalently, the D-efficiency
`(det M(S_G)/det M(S_M))^(1/p)` is at least `1/alpha`. The same multiplicative
`1/alpha` bound holds for maximizing trace information, using a gated optimizer
of that trace criterion. For minimizing
`trace(M(S)^{-1})`, the gate-optimal design has true objective at most `alpha`
times the true optimum, using a gated optimizer of the trace-inverse criterion.
These statements require a globally optimal gated
selection; an approximate gated optimum incurs its own additional error.

More directly, a *global upper bound* `U_G` on the gated logdet optimum is also
an upper bound on the marginal logdet optimum. Any selected design `S` supplies
the true lower bound `logdet M(S)`. Therefore

```text
logdet M(S) <= optimal marginal logdet <= U_G             (3)
```

is a valid numerical contract when the two supplied bounds are valid. A solver
gap for the gated model alone is not a gap for the marginal model. Re-evaluating
its chosen selection gives the lower side of (3), not equality of the models.

## Sharpness and rank refinement

For `0<rho<1`, take three unit-variance observations with covariance

```text
R = [[1,rho,0],[rho,1,0],[0,0,1]],
F = [1,1/2,b]^T,
```

and select exactly one, with no prior and one parameter. Then
`kappa=(1+rho)/(1-rho)` and `alpha=1/(1-rho^2)`. The marginal information values
are `(1,1/4,b^2)` and the gated values are `(alpha,alpha/4,b^2)`. All
feasible singleton information matrices are positive definite. For
`1<b^2<alpha`, the gated selection is the first observation, while the marginal
selection is the third. Taking `b^2` upwards to `alpha` makes the efficiency
approach `1/alpha`. Hence the constant in (2) is sharp as a supremum already
for three candidates and one parameter. Rational `rho` and rational `b`
can approach the same bound. There is no covariance-independent positive
efficiency guarantee, since `alpha` is unbounded as `rho` approaches one.

For a fixed selection with complement `T`, let
`r_S=rank(R_ST)`. Block inversion shows `rank(G(S)-M(S))<=r_S`. Consequently
at most `min(p,r_S)` generalized eigenvalues of `(G(S),M(S))` differ from one,
and all lie in `[1,alpha]`. Thus

```text
logdet G(S)-logdet M(S) <= min(p,r_S) log(alpha).          (4)
```

If `r_S<=r` uniformly over feasible selections, (2) improves to
`min(p,r) log(alpha)`. There is no analogous rank improvement for
trace-inverse cost: its multiplicative factor `alpha` is already dimension
independent, and rank one can still approach that full factor, because the
error can concentrate in one parameter direction.

## What is and is not established

The information mismatch and its weak-correlation expansion already appear in
Liu et al. (2016); the source audit records the original equations. Block
inversion, inverse-compression inequalities, and diagonal scaling are classical.
The condition-dependent design bounds above are retained as useful explicit
consequences for auditing and repairing the MINLP, with no publication-priority
claim. A useful implementation must still evaluate the correct covariance
submatrices, use genuine global bounds, and state whether its arithmetic is
certified or subject to solver tolerances.
