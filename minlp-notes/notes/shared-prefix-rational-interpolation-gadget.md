# Rational endpoint interpolation using only existing prefix bits

Date: 2026-09-05. Status: independently reviewed supporting lemma.

This elementary extension of binary disaggregation evaluates a rational
function at a binary grid prefix and multiplies it by a continuous
interpolation weight without adding integers. It may be useful beyond the
Stieltjes inverse-power construction. It is not claimed as a new general
binary-product linearization principle.

Let `h=2^(-L)` and `a=sum_(ell=1)^L 2^(-ell)z_ell`, with `z_ell` binary.
Let `lambda in [0,1]`. Suppose rational polynomials `P,Q` satisfy the
certified denominator bound `Q(t)>=q_min>0` on `[0,1]`, where `q_min` is
positive rational. Set `R=P/Q`. Degrees, coefficient encodings, and the
encoding of `q_min` are part of the input bounds.

For either endpoint `t=a` or `t=a+h`, and either weight
`theta=lambda` or `theta=1-lambda`, introduce variables

```
v_k=t^k theta/Q(t),          k=0,...,d,
d=max(deg P,deg Q).
```

They can be imposed exactly using linear equations and the existing bits:

```
0<=v_k<=1/q_min,
v_k=a v_(k-1)+s h v_(k-1),       k=1,...,d,
sum_k Q_k v_k=theta,
```

where `s=0` for the left endpoint and `s=1` for the right endpoint.
Expand `a` in each recurrence and replace every product
`z_ell v_(k-1)` by its exact binary-times-bounded-continuous hull.
The denominator equation forces `v_0=theta/Q(t)`, because the recurrences
force `v_k=t^k v_0` and `Q(t)>0`. Conversely, the displayed true values
respect all bounds since `0<=t<=1`.

The rational endpoint contribution is then the linear expression

```
theta R(t)=sum_k P_k v_k.
```

Using a left family with weight `1-lambda` and a right family with weight
`lambda` therefore imposes

```
x=(1-lambda)R(a)+lambda R(a+h)
```

with `O((d+1)(L+1))` continuous variables and rows, no additional integers, and
polynomial coefficient length under the stated input bounds. Signs of
coefficients in `P,Q` are unrestricted; positivity is needed only for the
certified denominator on the real interval. The Stieltjes special case
can instead exploit separate degree-one denominators for a simpler bound.

Exact endpoints `R(0)=0,R(1)=1` ensure that the union of these interpolated
segments covers `[0,1]`, even if `R` is not monotone: the piecewise-linear
function joining the successive values is continuous and joins zero to
one. Retain the original bound `0<=x<=1` to remove any segment portions
outside that interval. If `|R-g|<=delta` on `[0,1]`, then every retained
interpolated value differs by at most `delta` from the corresponding
interpolation of the exact endpoint values of `g`.

This statement does not supply a rational approximation to an arbitrary
inverse function, a denominator certificate algorithm for unrestricted
input, or a polynomial-degree representation after arbitrary rational
circuit composition. Those are separate analytic and encoding questions.
It only gives an exact MILP implementation once the indicated polynomial
representation and positive denominator bound are available.

The [first compact-power audit](review-compact-pure-power-interpolation.md)
and [second compact-power audit](review-compact-pure-power-interpolation-second.md)
both checked this broader gadget, including its constant-degree and
zero-bit size convention.
