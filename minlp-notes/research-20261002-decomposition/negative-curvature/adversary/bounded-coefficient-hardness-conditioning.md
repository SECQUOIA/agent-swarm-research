# Conditioning in the bounded-coefficient treewidth-two reduction

Date: 2026-10-02. Status: exact calculation, targeted rational checks, and an
[independent review](bit-serial-independent-review.md) finding no substantive gap.
This analyzes a particular published reduction. It proves no hardness
result for bounded negative-curvature/growth ratio.

The strong treewidth-two hardness result of Del Pia and Khajavirad does
not remove the conditioning question. Their bit-serial construction has
bounded integer coefficients and box endpoints, but its negative-curvature
ratio can still grow exponentially in its number of variables. This holds
even on a family with a unique global optimizer. Increasing the positive
weights on any of its affine square penalties cannot repair that family.

## The construction being analyzed

The reference is [Del Pia–Khajavirad, *Treewidth and the complexity of
box-constrained quadratic programs*, version 1, Theorem 3](https://arxiv.org/html/2609.35595v1#S3).
It encodes SUBSET SUM by copied choice variables, binary-digit recurrences,
running sums, and a target recurrence. Its objective is a sum of affine
squares plus one endpoint penalty per item. The source proves treewidth
two and uniformly bounded integer coefficients; it asserts no positive
uniform growth margin.

Here is the specialization needed for the calculation. Let

\[
 a_1=B,\qquad a_2=B-1,\qquad T=B,\qquad B\geq3,
 \qquad \ell=\lceil\log_2(2B)\rceil,\quad D=2^\ell.
\]

Write `b_ik` and `t_k` for the low-to-high binary digits of `a_i` and `T`.
All variables below are in `[0,1]`, and `z_i0=s_0=w_0=0`. Define

\[
\begin{split}
\Psi={}&\sum_{i=1}^2x_{i1}(1-x_{i1})
 +\sum_{i=1}^2\sum_{k=2}^{\ell}(x_{ik}-x_{i,k-1})^2\\
&+\sum_{i=1}^2\sum_{k=1}^{\ell}
       (2z_{ik}-z_{i,k-1}-b_{ik}x_{ik})^2\\
&+\sum_{i=1}^2(s_i-s_{i-1}-z_{i\ell})^2
 +\sum_{k=1}^{\ell}(2w_k-w_{k-1}-t_k)^2
 +(s_2-w_\ell)^2.                                      \tag{1}
\end{split}
\]

There are `N=5 ell+2` variables. Additive constants do not affect any
curvature or growth claim. The argument below also permits an arbitrary
strictly positive weight on each square, and a common strictly positive
weight `c` on the two endpoint penalties. The source's bounded-coefficient
case uses every weight equal to one.

## A residual-zero witness

For any two numbers `u_1,u_2` in `[0,1]`, set

\[
\begin{split}
x_{ik}(u)&=u_i,\\
z_{ik}(u)&=\frac{u_i}{2^k}\sum_{r=1}^{k}b_{ir}2^{r-1},\\
s_i(u)&=D^{-1}\sum_{j=1}^i a_j u_j,\\
w_k&=2^{-k}\sum_{r=1}^{k}t_r2^{r-1}.                 \tag{2}
\end{split}
\]

Every square in (1) vanishes whenever `B u_1+(B-1)u_2=B`.
The unique binary solution of this equation is `(u_1,u_2)=(1,0)`.
Since every summand in (1) is nonnegative, (2) at this binary solution
is the unique global optimizer `v*`, of value zero. Vanishing square
residuals determine all copied and state variables uniquely.

Take instead

\[
             (u_1,u_2)=(1/B,1),\qquad q=1-1/B,
\]

and let `y` be (2). All its variables belong to the unit box: each digit
prefix divided by `2^k` is less than one, and its running sums are `1/D`
and `B/D`. All square residuals still vanish, but

\[
                   \Psi(y)=c\,q/B.                    \tag{3}
\]

Put `d=y-v*` and `R=||d||^2>0`. Every global point-growth constant
`g>0` for (1) therefore satisfies

\[
                       g\leq cq/(BR).                 \tag{4}
\]

Let `A` contain the linear parts of the square residuals and let `W`
be their positive diagonal weight matrix. If `P` projects onto the two
coordinates `x_11,x_21`, the Hessian is

\[
                  H=2A^TWA-2cP.
\]

Both endpoints defining `d` satisfy all affine residual equations, so
`Ad=0`. Its two penalized choice displacements are `-q,1`. Hence

\[
 d^THd=-2c(q^2+1),\qquad
 \nu:=\max\{0,-\lambda_{\min}(H)\}
       \geq\frac{2c(q^2+1)}{R}.                       \tag{5}
\]

Combining (4) and (5) cancels the possibly large norm of the copied
variables and every square-penalty weight:

\[
             \boxed{\frac{\nu}{g}
                \geq\frac{2B(q^2+1)}q
                =2B(q+q^{-1})\geq4B.}                \tag{6}
\]

For `B=2^m`, `m>=2`, we have `ell=m+1` and `N=5m+7`. The bound is
therefore at least `2^(m+2)`, exponential in `N`, despite the bounded
coefficients of the unweighted source construction.

The positive growth premise is not vacuous. Near `v*`, the two endpoint
penalties control squared displacement of `x_11,x_21`, because the
endpoint distance is at most one half and `u(1-u)` is at least half
that distance. The linear map that takes a displacement to these two
initial choices and all square residuals is injective: zero initial
choices and zero residuals force every copy, digit state, running sum,
and target state to vanish successively. Its least singular value is
positive for each fixed instance. The positive square weights thus give
local quadratic growth. On the compact complement of a neighborhood of
the unique optimizer, positivity gives a positive lower ratio as well.
This proves existence of some `g>0`, without a uniform lower bound.

## Consequence for the open target

The result complements the existing
[four-variable penalty obstruction](../../../research-20261002/new-direction/negative-curvature-penalty-barrier.md)
by addressing the recent bounded-coefficient bit-serial hardness reduction
itself. Moving large input integers into graph structure does not supply
the missing uniform `nu/g` promise.

This calculation does not exclude a different hardness reduction, nor
does it prove the desired `f(p,max(1,nu/g)) poly(I)` algorithm. It closes
one tempting inference from strong width-two hardness. The unresolved
algorithmic task is still to retain large positive energy without a
complete separator value function or an uncontrolled coordinate-grid
curvature bound.

## Verification

Run the scoped check with

```sh
python3 -B research-20261002-decomposition/negative-curvature/adversary/check_bit_serial_conditioning.py
```

The checker passed 106 constructions, 954 weight cases, and 11,332 exact
zero-residual checks. It uses exact `Fraction` arithmetic and verifies all residual
identities for the optimizer and fractional witness, uniqueness of the
binary zero, feasibility, the objective value, squared distance, Hessian
directional curvature, and (6). Powers of two include `B=2^200`; no dense
Hessian or floating-point eigenvalue is used. These finite checks support
the displayed universal argument. No project-wide verification or CI
inspection was run.
