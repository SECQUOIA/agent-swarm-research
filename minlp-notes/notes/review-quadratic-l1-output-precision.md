# Independent audit: quadratic precision with a sum of absolute errors

Date: 2026-09-05. Reviewer: `graph_precision_second_review`.

**PASS after one explicit zero-energy convention was added.** I independently reviewed [the specialized l1 precision note](quadratic-l1-output-precision.md), including its primary analytic and optimization imports. Its semidefinite covariance surrogate gives the stated finite dimension-only constants and a polynomial rational construction. This review is separate from the general symmetric-body theorem.

## Finite bounds

The matrix `Gamma(P)` is positive semidefinite because it is the Frobenius Gram matrix of the scaled symmetric Hessians. I checked equation (1) in the primary [Briët, de Oliveira Filho and Vallentin paper](https://arxiv.org/pdf/0910.5765): for positive semidefinite objective matrices, the correlation SDP lies between the sign optimum and `pi/2` times that optimum. The note correctly treats this as an established inequality.

A parity support's quadratic midpoint vector has l1 norm at most `4 epsilon`. Every sign combination therefore satisfies the scalar pairwise discrepancy bound. Its fourth-moment inequality yields `s^T Gamma(Sigma)s<=16 epsilon^2`. The imported ratio gives `S(Sigma)<=8 pi epsilon^2<36 epsilon^2`. Scaling covariance by `c_n=max(6,n/4)` enforces both the energy constraint and the identity cap. The previously reviewed covariance-volume and parity-cover argument then gives exactly the stated lower constant.

For the upper bound, all outputs share one residual-error matrix `Z`. Its Frobenius norm is at most one quarter, and each output error equals one half of its Frobenius pairing with the corresponding scaled Hessian. Applying Cauchy--Schwarz to any signed sum bounds it by `sqrt(s^T Gamma(P)s)/8<=epsilon/8`. The maximum over signs is the l1 norm. Thus the same binary count works, without a factor depending on the number of outputs.

Compactness of the covariance feasible set and positive determinant attainment hold as before: `S` is a continuous maximum over a compact elliptope, homogeneous of degree two, and a sufficiently small positive scalar multiple of the identity is feasible. The all-affine case is handled separately.

## Geodesic oracle and zero energies

For fixed correlation matrix `X`, the energy is a positive semidefinite output-budget energy. After excluding identically zero energies, its half logarithm is geodesically convex and its normalized gradient is positive semidefinite with trace one. The exclusion matters: if `H_1=H_2` and `X=[[1,-1],[-1,1]]`, then this energy vanishes even though the Hessians do not. The author added the explicit convention after this review raised it. Every nonzero energy is positive at every positive definite covariance, by the transformed-Hessian square-sum representation.

The supremum of the nonzero log-energy branches is the half logarithm of `S`, hence is globally one-Lipschitz. A nearly optimal feasible correlation matrix supplies a near-active branch, rather than requiring differentiability of `S` or a unique SDP optimizer. The repaired oracle point has energy at least half the positive trace of `Gamma`, so the branch actually used never has zero energy. The exact penalty, feasibility scaling, and earlier inexact subgradient proof therefore apply.

## Primary weak-optimization theorem and exact repair

I read Definition (5), the encoding discussion on printed page 172, and Theorem (3.1) on page 177 of [Grötschel, Lovász and Schrijver (1981)](https://ir.cwi.nl/pub/10046/10046D.pdf). The weak optimizer is within the requested distance of the body and its objective is within the requested additive error of the optimum over the original body. It is not restricted to comparison with an eroded body. The stated binary complexity includes logarithmic accuracy dependence. I also inspected the page image to verify the source's weak-separation normalization `||c||>=1`; division by the nonzero infinity norm meets that convention.

For `m>=3`, the off-diagonal elliptope parameterization has dimension at least two, a known inner Euclidean radius one quarter, and outer radius `m`. The `sqrt(2)` relation between off-diagonal matrix Frobenius norm and coordinate norm proves the inner inclusion; entry magnitudes at most one prove the outer inclusion. The small cases `m=1,2` are elementary. Exact rational symmetric congruence elimination supplies a polynomial-bit negative quadratic-form witness when a queried correlation matrix is not positive semidefinite. It therefore gives the required rational strong separator and, by the stated normalization, a weak separator.

Normalize `Gamma` to trace one. Its optimum `s` lies in `[1,m]`. The weak optimizer at accuracy `rho` has objective `a>=s-rho`, and its matrix has least eigenvalue at least `-sqrt(2)rho`. Therefore

```
X_f=(X(v)+2rho I)/(1+2rho)
```

is exactly positive semidefinite with exact unit diagonal. Its objective is `(a+2rho)/(1+2rho)`. Feasibility and the weak objective guarantee give

```
0<=s-a_f<=rho[1+2(s-1)]/(1+2rho)<=(2m+1)rho.
```

With `rho=nu/[4(m+1)]`, the proposed unnormalized bounds satisfy `L<=S<=U=L+nu tr Gamma`, `L>=tr Gamma/2`, and `U/L<=1+2nu`. All constants are conservative. The upper value is a mathematical certificate supplied by the weak-optimization theorem; producing an explicit dual optimum is unnecessary. The half-log branch gap is at most `nu`, and inverse-polynomial choices fit the earlier oracle and final repair budgets.

The trace lower bound `tr Gamma(P)>=lambda_min(P)^2 tr Gamma(I)` and positive rationality of the latter trace prove the required polynomial-bit conditioning. The dyadic initial covariance from `delta^2 m tr Gamma(I)<=epsilon^2` gives the same polynomial-radius bound. Rational sums and matrix-function approximations suffice; neither a factorization of `X` nor an exact SDP optimizer is assumed.

## Checks and scope

I ran the provided `code/quadratic_rank/check_l1_errors.py`. All 24 exact shared-residual inequalities and 30 exact rational elliptope feasibility/upper-bound repairs passed. This checks the new algebra, not an implementation of the imported weak optimizer.

Rationally transformed l1 budgets and finitely many groups follow by taking maxima of the corresponding penalty branches, with zero energies omitted. The group and output counts affect polynomial running time but not the additive dimension-only guarantee. The note correctly avoids transferring the separate-output hardness reduction to a single l1 budget without a new reduction.
