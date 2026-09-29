# Independent review of the first two relaxation orders

Date: 2026-09-28. Status: the order-one obstruction and the proposed
order-two certificate pass this independent algebraic review. This review
does not establish a formula at higher orders or a novelty claim.

The model is

\[
 f=x^2-2xy+y^2+z^2+2yz,
 \qquad x,z\in[0,1],\quad y\in[-1,1],
\]

with bags `(x,y)` and `(y,z)`. Write `h(y)=max(y,0)^2`,
`g_x=x(1-x)`, and `g_y=1-y^2`. The order-`r` quadratic module
uses sums of squares whose products with these generators have degree at
most `2r`. The local preordering also permits the product `g_x g_y`.

## 1. An optimal majorant need not have a certificate at the same order

Set `a=sqrt(2)-1` and

\[
 p_2(y)=\frac12(y+a)^2.
\]

This polynomial majorizes `h`. On the negative half-interval this follows
from its square representation; on the positive half-interval it follows
from

\[
 p_2(y)-y^2=\frac12(1-y)(y+a^2).
\]

Moreover, `p_2(y)+p_2(-y)=y^2+a^2`. Thus
`0<=p_2-h<=a^2`, and its errors at the ordered nodes
`-1,-a,a,1` are `a^2,0,a^2,0`. The polynomial
`p_2-a^2/2` is therefore a best uniform degree-at-most-two approximation
to `h`, by four-point alternation. Equivalently, `p_2` has the smallest
possible uniform majorant width among degree-at-most-two polynomials.

Nevertheless,

\[
 q_2(x,y)=x^2-2xy+p_2(y)
\]

does not belong to the order-one quadratic module. Suppose it had a
representation

\[
 q_2=\sigma_0+c g_x+d g_y,
 \qquad c,d\ge0,
\]

where `sigma_0` is a sum of squares of affine polynomials. At
`(x,y)=(0,-a)`, the left side is zero and `g_y>0`. Consequently `d=0`
and every affine factor of `sigma_0` vanishes there. Write those factors
as `u_i x+v_i(y+a)`. Coefficient comparison gives

\[
 \sum_i v_i^2=\frac12,\qquad
 \sum_i u_i v_i=-1,\qquad
 c=2a,\qquad
 \sum_i u_i^2=1+2a.
\]

Cauchy--Schwarz would require

\[
 1\le\frac12(1+2a)=\sqrt2-\frac12<1,
\]

a contradiction. The order-one preordering is the same module because
`g_x g_y` has degree four. Thus this also disproves membership in that
preordering. In particular, exact polynomial-approximation duality for
actual local measures cannot automatically be transferred to an SOS
relaxation with the same degree budget.

Even degree-one majorants can fail at order one. The optimal linear
majorant is `(y+1)/2`; its maximum error is `9/16`, attained at `y=1/4`.
For the associated `q`, zeros at `(0,-1)` and `(1,1)` force all affine
SOS factors to be multiples of `2x-y-1`. The `xy` coefficient forces
`sigma_0=(2x-y-1)^2/2`; the quadratic coefficients then force
`c=1,d=1/2`, leaving an incorrect coefficient `-1` on `x`.

## 2. The order-one sparse bound is exactly minus one quarter

The identity

\[
 x^2-2xy+\frac12y^2+\frac12y+\frac18
 =\frac12(2x-y-\tfrac12)^2+g_x
\]

and its reflected version for `(z,-y)` certify `f+1/4>=0` in the
order-one sparse quadratic module.

For the reverse inequality, take the first-bag moment sequence from
the atomic probability law

\[
 \frac34\delta_{(0,-1/2)}+\frac14\delta_{(1,3/2)}.
\]

Its moment matrix is positive semidefinite, and

\[
 \mathbb E[y]=0,\quad \mathbb E[y^2]=\frac34,\quad
 \mathbb E[g_x]=0,\quad \mathbb E[g_y]=\frac14.
\]

These are the required local order-one positivity constraints. The law
does contain an atom outside the rectangle; it is used only to produce
a feasible truncated moment sequence. Its first-bag expected cost is
`-1/2`. For the second bag use the reflected law `(y,z)=(-Y,X)`.
The separator moments through degree two agree and the second-bag cost
is `3/4-1/2=1/4`. The total is `-1/4`. This proves the bound exactly,
and separates it from the actual-local-measure value
`-(3-2sqrt(2))`.

## 3. The proposed order-two certificate is exact

Set

\[
 s=\sqrt3,\quad a=3s-5,\quad b=s-1,\quad
 A=\frac{3+2s}{18},\quad E=-\frac43+\frac{7s}{9},
 \qquad p(y)=A(y+1)(y+a)^2.
\]

Here `0<a<b<1` and `E>0`. Direct factorization gives

\[
 p(y)-y^2=A(y+7-4\sqrt3)(y-b)^2.                 \tag{1}
\]

Since `7-4sqrt(3)>0`, the factorizations of `p` and (1) prove
`p>=h` on the entire interval. The identity

\[
 p(y)+p(-y)=y^2+2E
\]

then proves `0<=p-h<=2E`. At the six ordered nodes
`-1,-b,-a,a,b,1`, the errors `p-h` are
`0,2E,0,2E,0,2E`. Consequently `p-E`, although cubic, is a best
degree-at-most-four uniform approximation to `h`, with error `E`.
The six alternating nodes are necessary for this degree-four claim;
four- or five-point alternation alone would not establish it.

Define

\[
 V=\begin{pmatrix}
 x(x-b)\\
 x(y-b)\\
 (y+1)(y+a)-\frac{(b+1)(b+a)}b x
 \end{pmatrix},\quad
 W=\begin{pmatrix}x-b\\y-b\end{pmatrix},\quad
 Z=(b+a)x-b(y+a),
\]

\[
 Q=\begin{pmatrix}
 2-s&(-7+3s)/4&(s-1)/12\\
 (-7+3s)/4&7/6&-(s+1)/12\\
 (s-1)/12&-(s+1)/12&1/12+s/18
 \end{pmatrix},
\]

\[
 R=\begin{pmatrix}2-s&(-7+3s)/4\\(-7+3s)/4&1\end{pmatrix},
 \qquad k=\frac16+\frac{7s}{72}.
\]

Independent exact symbolic expansion confirms

\[
 x^2-2xy+p(y)=V^TQV+g_xW^TRW+g_y kZ^2.          \tag{2}
\]

The leading principal minors of `Q` are

\[
 2-s,\qquad \frac{35s-58}{24},\qquad
 \frac{38-15s}{864};
\]

those of `R` are `2-s` and `(13s-22)/8`. They are strictly positive:
for the two less immediate comparisons,
`35^2*3=3675>58^2=3364` and `13^2*3=507>22^2=484`.
Also `k>0`. Thus (2) is a genuine order-two quadratic-module
certificate; no product-generator term is needed.

Reflection and `p(y)+p(-y)=y^2+2E` give a sparse certificate for
`f+2E`. The actual-local-measure characterization in
[the sharpness note](quadratic-sharpness.md) gives a feasible value
`-2E` because the shared moments have degree four. Therefore both the
order-two sparse quadratic module and its preordering have exact bound
`-2E` for this example.

## 4. Verification performed and its limits

The reviewer independently derived the order-one obstruction and the
atomic truncated-moment witness by hand. For the order-two result, a
targeted `python3 - <<'PY'` command using SymPy checked:

- exact expansion of (2), obtaining the zero polynomial;
- exact leading principal minors of both matrices;
- all six contact errors;
- factorization (1) and the reflection identity.

A separate exploratory CVXPY calculation, run as
`python3 /tmp/quadratic_strip_check.py`, minimized the added constant
needed for local membership at orders one and two. It suggested
order-two membership and order-one nonmembership before the exact
certificate was supplied. Several numerical runs reported inaccurate
solution status; none is used as proof. The exact certificate and the
explicit moment witness establish the claims above independently of
those numerical statuses.

These checks verify concrete algebra, positivity, and the stated
approximation argument. They do not prove an all-order identity, settle
the behavior at order three or above, establish computational usefulness,
or establish literature priority. No project-wide verification, CI
inspection, or Lean formalization was performed.
