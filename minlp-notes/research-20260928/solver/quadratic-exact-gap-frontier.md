# Exact finite-order gaps for the fixed quadratic example

Date: 2026-09-28. Status: the order-one and order-two values below are
proved by explicit certificates and witnesses. A separate
[independent review](quadratic-exact-gap-review.md) checks the algebra
and approximation argument. Equality at all higher orders remains a
conjecture, despite close floating-point agreement.

This note concerns only the fixed example in
[quadratic-sharpness.md](quadratic-sharpness.md):

\[
 f=x^2-2xy+y^2+z^2+2yz,
 \qquad x,z\in[0,1],\quad y\in[-1,1].
\]

Write `h(y)=max(y,0)^2`. Let `rho_r^Q` and `rho_r^T` be the sparse
order-`r` bounds with bags `(x,y)` and `(y,z)`, matching separator
moments through degree `2r`. The local quadratic generators are
`x(1-x),1-y^2` and `z(1-z),1-y^2`. The superscripts indicate the
ordinary quadratic module and the preordering, respectively. Total
degrees of all certificate summands are at most `2r`.

The local-measure optimum with separator agreement through degree `n`
is `v_n=-2E_n(h)`, where `E_n` is the best uniform polynomial
approximation error. Therefore

\[
 \rho_r^Q\le\rho_r^T\le v_{2r}=-2E_{2r}(h).
\]

The new exact conclusions are

\[
 \boxed{\rho_1^Q=\rho_1^T=-\frac14
       <-\bigl(3-2\sqrt2\bigr)=v_2}
\]

and

\[
 \boxed{\rho_2^Q=\rho_2^T=v_4
        =\frac83-\frac{14\sqrt3}{9}
        \simeq-0.0276345895.}
\]

Thus local positivity has an additional cost at order one. At order
two, the entire remaining error is caused by finite separator
information, even for the ordinary quadratic module. This is a precise
small-order benchmark and a modest refinement of the sharp-rate result;
it is not by itself a general hierarchy theorem.

## 1. Order one: the local relaxation creates extra error

The identity

\[
 x^2-2xy+\frac{y^2}{2}+\frac y2+\frac18
 =\frac12\left(2x-y-\frac12\right)^2+x(1-x)
                                                        \tag{1}
\]

and its image under `(x,y)->(z,-y)` give a sparse order-one
certificate for `f+1/4>=0`. Hence both bounds are at least `-1/4`.

For the matching upper bound, use the following positive atomic law
to define a truncated functional on the first bag:

\[
 \frac34\delta_{(0,-1/2)}+\frac14\delta_{(1,3/2)}.
                                                        \tag{2}
\]

One atom lies outside the rectangle. This is deliberately a
representation of the truncated functional, not a feasible local law
for the original rectangle. Its order-one moment matrix is positive
semidefinite, and

\[
 L(y)=0,\quad L(y^2)=\frac34,\quad
 L(x(1-x))=0,\quad L(1-y^2)=\frac14.
\]

These are all the order-one generator tests. Reflect this law to the
second bag by `(y,z)=(-Y,X)`. The two separator moments agree. The
local objectives are `-1/2` and `1/4`, so their sum is `-1/4`.
At order one the product of the quadratic generators has degree four
and is absent; the two cones coincide.

For comparison, put `c=sqrt(2)-1`. The polynomial

\[
 S_1(y)=\frac{y^2}{2}+cy
\]

approximates `h` with error `E_2(h)=c^2/2`. On `[0,1]` its error
is `y^2/2-cy`, with its minimum at `c` and its maximum at `1`;
both have absolute value `c^2/2`. The error is odd on `[-1,1]`.
At `-1,-c,c,1` it alternates between the two extreme values. An
improvement by a polynomial of degree at most two would make its
difference from `S_1` change sign at least three times, which is
impossible. Hence `v_2=-c^2`, strictly greater than `-1/4`.

In particular, the implication

> `p>=h` on `[-1,1]`, `deg p<=2r` implies
> `x^2-2xy+p(y)` belongs to the local order-`r` cone

is false. The optimal majorant `p=S_1+c^2/2` at `r=1` already
disproves it. Neither polynomial nonnegativity nor an untruncated
positivity theorem is enough to prove a degree-specific statement.

## 2. The optimal degree-four approximation has an explicit cubic form

Define

\[
 s=\sqrt3,\qquad a=3s-5,\qquad b=s-1,\qquad
 A=\frac{3+2s}{18},\qquad
 E=-\frac43+\frac{7s}{9},
\]

so `0<a<b<1` and `E>0`. Set

\[
 p(y)=A(y+1)(y+a)^2,
 \qquad S(y)=p(y)-E.                                  \tag{3}
\]

Three direct polynomial identities are

\[
 \begin{aligned}
 p(y)-y^2&=A(y+7-4s)(y-b)^2,\\
 p(y)+p(-y)&=y^2+2E,\\
 p(y)&=Ay^3+\frac{y^2}{2}
             +\left(-1+\frac{2s}{3}\right)y+E.
 \end{aligned}                                        \tag{4}
\]

The first identity gives `p>=y^2` on `[0,1]`, because
`7-4s>0`. The factorization in (3) gives `p>=0` on `[-1,0]`.
Thus `p>=h`. The symmetry identity and
`h(y)+h(-y)=y^2` also give `p-h<=2E` everywhere.

At the six ordered points

\[
 -1,-b,-a,a,b,1,
\]

the values of `p-h` are respectively

\[
 0,2E,0,2E,0,2E.
\]

Consequently `h-S` alternates between `E` and `-E` at six
points and has norm `E`. If a polynomial of degree at most four
had smaller error, its difference from `S` would alternate in sign
at those six points and have at least five distinct roots. This is
impossible. We have proved directly that

\[
 E_4(h)=E=-\frac43+\frac{7\sqrt3}{9}.                  \tag{5}
\]

No numerical Remez calculation or quoted approximation formula is
needed. The same argument also proves `E_3(h)=E_4(h)`.

## 3. An exact order-two local certificate

Write `gx=x(1-x)` and `gy=1-y^2`, and define

\[
 V=\begin{pmatrix}
 x(x-b)\\
 x(y-b)\\
 (y+1)(y+a)-\dfrac{(b+1)(b+a)}b x
 \end{pmatrix},\quad
 W=\begin{pmatrix}x-b\\y-b\end{pmatrix},\quad
 Z=(b+a)x-b(y+a).
\]

Let

\[
 Q=\begin{pmatrix}
 2-s&(-7+3s)/4&(s-1)/12\\
 (-7+3s)/4&7/6&-(s+1)/12\\
 (s-1)/12&-(s+1)/12&1/12+s/18
 \end{pmatrix},
\]

\[
 R=\begin{pmatrix}
 2-s&(-7+3s)/4\\
 (-7+3s)/4&1
 \end{pmatrix},
 \qquad k=\frac16+\frac{7s}{72}.
\]

An exact identity is

\[
 \boxed{x^2-2xy+p(y)=V^TQV+g_xW^TRW+g_y kZ^2.}        \tag{6}
\]

The leading principal minors of `Q` are

\[
 2-s,\qquad \frac{35s-58}{24},\qquad
 \frac{38-15s}{864};
\]

those of `R` are `2-s` and `(13s-22)/8`. They are strictly
positive. For example, `35^2*3>58^2` and `13^2*3>22^2` prove
the two less immediate comparisons. Also `k>0`.

Thus `Q,R` are positive definite and their quadratic forms are sums
of squares. Every summand in (6) has total degree at most four.
This is an ordinary quadratic-module certificate, with no product
of generators needed.

Apply (6) again to `(z,-y)`. By (4), the left sides add to `f+2E`.
Therefore `rho_2^Q>=-2E`. The local-measure upper bound gives
`rho_2^T<=-2E`, proving equality for both cones.

For a completely explicit primal witness, let the first separator
law put the following masses on `-1,-a,b`:

\[
 w_1=\frac{8-4s}{9},\qquad
 w_a=\frac5{18}+\frac s6,\qquad
 w_b=-\frac16+\frac{5s}{18}.
\]

These masses are positive and sum to one. Their first and third
moments are zero. The reflected law therefore matches all moments
through degree four. Use `x=max(y,0)` with the first law and
`z=max(-y,0)` with the reflected law. Both local laws are on their
rectangles, and their total objective is

\[
 w_1+w_a a^2-w_b b^2=-2E.
\]

This certificate-and-witness proof does not need SDP strong duality,
nor does it rely on the general measure-approximation duality.

## 4. Higher-order frontier and literature limits

[The numerical data](numerical-rate-results.json) are consistent with

\[
 \rho_r^Q=\rho_r^T=-2E_{2r}(h)\qquad(r\ge2).            \tag{7}
\]

Only `r=2` is proved here. The checks at `r=3,4,5,6` use
floating-point SDPs and finite-grid approximation LPs; several SDP
runs report `optimal_inaccurate`. Their agreement cannot prove (7)
or exclude a small strict gap. A useful next target is a certificate
for the optimal separator with a uniform degree bound. A theorem
that only guarantees some finite certificate degree will not resolve
(7).

The symmetry of `h` allows its best degree-`2r` approximant, for
`r>=2`, to have the form `y^2/2` plus an odd polynomial of degree at
most `2r-1`. To see this, subtract `y^2/2` and take the odd part
of an approximant; this cannot increase uniform error. This degree
slack is a possible aid to a certificate construction, not a proof
of one.

Sources examined for the degree question:

- [Nguyen and Powers, *Polynomials non-negative on strips and
  half-strips*](https://arxiv.org/abs/1009.3588), full open preprint,
  especially Theorem 4 and its proof. Their half-strip preordering
  is saturated. Our local polynomial is nonnegative even on
  `[-1,1] x [0,infinity)` after reversing the variable order, so
  this theorem is relevant to existence of an untruncated
  certificate. It does not provide the total-degree bound `2r`
  required here or establish membership in the specified ordinary
  box quadratic module at order `r`.
- [Ahmadi, Dibek and Hall, *Sums of Separable and Quadratic
  Polynomials*](https://arxiv.org/abs/2105.04766), abstract examined.
  Their globally nonnegative univariate-plus-quadratic setting is
  related in algebraic form. Our polynomial is only required to
  be nonnegative on a rectangle or half-strip; global
  nonnegativity is unavailable. The abstract does not settle the
  degree-constrained rectangle problem, and no claim is made
  here about every theorem in that paper.

These searches do not establish novelty. In particular, the explicit
best cubic approximation is not claimed to be a new approximation
theorem. The contribution of this note is the exact small-order
analysis for this particular sparse quadratic benchmark. The
broader novelty assessment remains the one in
[the sharpness prior audit](sharpness-prior.md).

## Verification record

The targeted command

```
python3 -B research-20260928/solver/check_quadratic_exact_gap.py
```

checks both local certificate identities, the factorizations and
six approximation contact values, the exact principal minors,
the order-one truncated witness, and the order-two local-measure
witness. It uses exact rational arithmetic and `sqrt(2),sqrt(3)`
symbolically. The independent reviewer separately expanded (6),
factored `p-y^2`, checked the minors, and reconstructed the
approximation and order-one arguments. These checks support the
displayed finite-order proofs. They establish neither (7) at
higher orders nor any publication-priority claim. No Lean,
project-wide checks, or CI inspection was used.
