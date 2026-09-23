# Rational Jacobi rotations and certified matrix functions

Date: 2026-09-05. Status: supporting algorithmic lemma, independently reviewed twice as
part of the weighted covariance algorithm. This is an explicit implementation of classical Jacobi ideas,
not a proposed new eigenvalue algorithm. It supports the
[weighted covariance construction](quadratic-weighted-covariance-algorithm.md).

A recent direct reference is Alberto Del Pia,
[*Rational Jacobi Rotations and the Complexity of Approximating Mixed Integer Quadratic Programming*](https://arxiv.org/html/2607.29386),
Theorem 2 (July 2026). It proves polynomial Turing computation of an
exactly orthogonal rational near-diagonalizer, using rational rotations
and denominator tracking. The self-contained proof below is retained
for auditability; its spectral guarantee is not claimed as new.

## Rational spectral residuals

**Lemma.** Given rational symmetric `A` and rational `sigma>0`, one can
compute in deterministic polynomial time an exactly orthogonal rational
matrix `V` and rational symmetric `B` such that

```
A=VBV^T,       ||B-diag(B)||_F<=sigma.                    (1)
```

Polynomial time is in the input bit length and `log(1/sigma)` when
`sigma<1`. No separation assumption on distinct eigenvalues is needed.

For `n=1`, take `V=I`. Otherwise let `N=n(n-1)` and choose rational
`M>=max{1,||A||_F}`, for example `max{1,sum_(i,k)|A_ik|}`. Start
with `V=I,B=A`. Choose the current largest off-diagonal entry `B_ik`
in absolute value. An exact orthogonal rotation `C_star` in that
two-coordinate plane annihilates this entry. Writing
`s=||B-diag(B)||_F`, invariance of Frobenius norm and the change in
the two diagonal entries give

```
offnorm(C_star^T B C_star)^2=s^2-2B_ik^2
                          <=(1-2/N)s^2.
```

Approximate the rotation by an exactly orthogonal rational rotation
`C` satisfying `||C-C_star||_2<=sigma/(8NM)`. Use a rational
approximation of its half-angle parameter `t` and the formulas

```
c=(1-t^2)/(1+t^2),       s_angle=2t/(1+t^2).
```

The annihilating angle can be chosen in `[-pi/4,pi/4]`; its half-angle
parameter belongs to `[1-sqrt(2),sqrt(2)-1]`. This parameter can be
computed from the two-by-two block by arithmetic and square roots.
For example, the usual stable quadratic formula gives a tangent of
the annihilating angle of magnitude at most one, and the half-angle
formula is `t=sin(angle)/(1+cos(angle))`. The signs are chosen for
the desired annihilation convention. All denominators of the
half-angle conversion are bounded away from zero. Approximation on
this bounded parameter interval takes polynomially many bits, and
`c^2+s_angle^2=1` holds as an exact rational identity.

Execute `B_next=C^TBC` and `V_next=VC` with exact rational arithmetic.
The reconstruction identity and orthogonality remain exact. Since
`||B||_F=||A||_F<=M`,

```
||C^TBC-C_star^TBC_star||_F<=2M||C-C_star||_2,
offnorm(B_next)<=(1-1/N)s+sigma/(4N).
```

While `s>sigma`, the latter is at most `(1-3/(4N))s`. Hence at most
`ceil(2N log(M/sigma))+1` steps suffice when `M>sigma`; otherwise
no step is needed. An integer upper bound from a dyadic logarithm
avoids a transcendental stopping-count calculation. The actual test
`offnorm(B)^2<=sigma^2` uses exact rational arithmetic.

The rotation precision is `O(log N+log M+log(1/sigma))` bits. Each
rotation has a common denominator of that bit length up to a constant
factor. Each update of `B` multiplies its existing common denominator
by the square of a rotation denominator; each update of `V` multiplies
it once. After polynomially many rotations, all common denominators
still have polynomial bit length. Numerator lengths are controlled by
`||B||_F<=M` and `||V||_2=1`. Computing a subsequent annihilating
rotation from polynomial-bit entries requires polynomial-bit arithmetic
and square roots, including for a very small nonzero pivot. A zero
off-norm terminates the process. This proves the complexity claim.

The maximum-pivot contraction is classical. Gower's author-hosted
numerical analysis notes give the identity and contraction on slides
44--46 ([source](https://gowerrobert.github.io/pdf/teaching/MDI210/NA_slides.pdf)).
The proof above adds explicit rational orthogonal rotations and common
denominator accounting for the required implementation model.

## Matrix functions without eigenvector conditioning assumptions

Put `A_0=V diag(B)V^T`. It satisfies `||A-A_0||_2<=sigma`. If `A`
is positive definite with spectrum in `[a,b]`, the diagonal entries of
`B` belong to `[a,b]`, so `A_0` obeys the same spectral bounds.

The following elementary operator-norm bounds suffice:

```
||log A-log A_0|| <= ||A-A_0||/a,
||sqrt(A)-sqrt(A_0)|| <= ||A-A_0||/(2sqrt(a)),
||A^(-1/2)-A_0^(-1/2)|| <= ||A-A_0||/(2a^(3/2)).         (2)
```

For the logarithm, integrate the resolvent difference and use
`integral_0^infty(a+t)^(-2)dt=1/a`. For the square root, its difference
`X` solves `sqrt(A)X+Xsqrt(A_0)=A-A_0`. The integral solution bounds
its norm by `||A-A_0||/(2sqrt(a))`. For the inverse square root,
combine this with the inverse-difference identity.

For symmetric matrices of operator norm at most `M_0`,

```
||exp(A)-exp(A_0)||<=exp(M_0)||A-A_0||,                 (3)
```

by the Duhamel integral identity. Thus matrix functions reduce to
approximating scalar functions of the rational diagonal entries of `B`
and reconstructing with the exactly rational orthogonal `V`.

Scalar square roots can be approximated by rational bisection. For
logarithms, dyadic range reduction gives an argument in `[1,2]` and
the arctanh series has ratio at most `1/3`. Exponentials use range
reduction and Taylor approximation. If `|log a|,|log b|,M_0` are
polynomially bounded, these computations take polynomial bit complexity
for a prescribed inverse-exponential-polynomial absolute error. Equations
(2)--(3) specify the extra spectral residual precision needed. No
particular exact eigenbasis is ever approximated.

## Rayleigh values and radial projection

Choose a column `v` of `V` corresponding to the largest entry of
`diag(B)`. Its exact Rayleigh quotient is that diagonal entry. Weyl's
elementary spectral perturbation bound gives

```
0<=lambda_max(A)-v^TAv<=sigma.
```

For positive definite `A>=aI`, taking `sigma<=a tau/2` makes the
logarithmic Rayleigh error at most `tau`. This produces the smooth
near-active Rayleigh branch used by the covariance algorithm without
requiring a stable choice of a leading eigenvector.

For the affine-invariant positive definite metric,

```
d(A,A_0)<=2sqrt(n) sigma/a   when sigma<=a/2.
```

Metric projection onto a centered radius-`R` ball is nonexpansive.
Consequently replacing `A` by `A_0` perturbs its projection by at most
this metric error. For `A_0`, projection is the scalar spectral map

```
t=R/max{R,sqrt(sum_i log(B_ii)^2)},
Proj_R(A_0)=V diag(exp(t log B_ii)) V^T.
```

When `R>=1`, its denominator is bounded away from zero. The formulas
and the preceding elementary-function estimates give polynomial-time
evaluation to prescribed inverse-exponential-polynomial matrix error,
and then to the required metric error. This supplies the finite-precision
projection routine used in the inexact subgradient recurrence.
