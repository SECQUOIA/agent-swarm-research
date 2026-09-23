# Positive perspectives preserve binary precision exponents

Date: 2026-09-05. Status: independently reviewed; see [the proof audit](../notes/review-perspective-integer-precision.md).
This is a useful transfer lemma, not a claim that perspective reformulations
are new. The main quadratic integer-precision theorem is in
[the noncommutative-rank result](quadratic-system-noncommutative-rank-complexity.md).

## A formulation transfer with no additional binaries

Let `F:D -> R^m` have a graph relaxation of componentwise error `delta`
given by an MILP

```
A y + B v + C a + E z <= h,     z in {0,1}^p,
```

where `a` denotes all continuous auxiliary variables. The displayed
constraints include the input-domain restrictions. Equalities may be
represented by paired inequalities. Define the positive perspective

```
G(x,t)=t F(x/t),
D_pers={(x,t): ell<=t<=u, x/t in D},     0<ell<=u<infinity.
```

Introduce continuous scaled auxiliaries `a'` and `v'=t z`, with each
component of `v'` represented exactly by the four linear inequalities

```
ell z_i <= v'_i <= u z_i,
t-u(1-z_i) <= v'_i <= t-ell(1-z_i).
```

Replace the original rows by

```
A x + B w + C a' + E v' <= h t.
```

Keep the same `p` binaries and impose `ell<=t<=u`. Dividing the resulting
rows by positive `t` recovers the original formulation with
`y=x/t`, `v=w/t`, `a=a'/t`, and unchanged binary `z`. Conversely every
original feasible point scales into a feasible point of the new formulation.
Thus it contains every exact perspective graph point and admits only

```
|w_j-G_j(x,t)| <= t delta <= u delta.
```

The transformation adds `p` continuous auxiliaries, the new input `t`, and
`4p+2` inequalities, and no integer variables. When `ell,u` and the original
data are rational, it preserves rational coefficients and polynomial
encoding size. Continuous original auxiliaries need not have finite bounds:
their scaling is imposed through homogenized rows, not product envelopes.
Only the binaries require the bounded-product construction.

This statement concerns binary MILPs. Applying the same four inequalities
to an unbounded general integer variable would not be exact and is not
asserted here.

## Lower transfer by an affine slice

Let `p_conv(F,delta)` and `p_bin(F,delta)` denote least integer dimension
in arbitrary convex lifts and least binary MILP dimension, respectively.
Fix any `t0 in [ell,u]`. Restrict a perspective relaxation to `t=t0`,
then apply the invertible linear change `y=x/t0`, `v=w/t0`. This produces
a relaxation of `F` with error `epsilon/t0`, using the same integer
coordinates. Consequently

```
p_conv(F,epsilon/t0) <= p_conv(G,epsilon),
p_bin(F,epsilon/t0)  <= p_bin(G,epsilon)
                    <= p_bin(F,epsilon/u).
```

Whenever matching lower and binary upper laws for `F` have the form
`c log2(1/delta)+O(1)`, both corresponding laws for `G` have the same
coefficient `c`. The positive lower bound on `t` is essential to the
formulation equivalence as stated; no assertion includes the cone apex.

## Quadratic-over-linear systems

For `F_j(y)=(1/2)y^T H_j y+a_j^T y+b_j` on a full-dimensional bounded
box `D`, the perspective is

```
G_j(x,t)=(x^T H_j x)/(2t)+a_j^T x+b_j t.
```

If the Hessian-space noncommutative rank is `r`, the existing quadratic
theorem and the two transfers give

```
p_conv(G,epsilon)=p_bin(G,epsilon)
                 =(r/2) log2(1/epsilon)+O(1),
```

where the equality means equality of the displayed asymptotic expressions,
not an exact finite-precision equality between the two minima. The binary
upper retains `O(1+log(1/epsilon))` rows and variables for fixed original
quadratic data. The input domain `D_pers` is a bounded polytope described
by `ell<=t<=u` and `D_lower t<=x<=D_upper t`.

An ordinary box domain in `(x,t)` also has the same coefficient when it
has positive width in every `x` coordinate and `0<ell<=t<=u`: obtain the
upper by embedding all ratios `x/t` into one larger bounded box and then
imposing the requested `(x,t)` box; obtain the lower by fixing `t=t0`.

For example `x^2/t` on `x in [0,1], t in [1,2]` has coefficient `1/2`.
Its pointwise Hessian has rank one, while the span of its Hessians contains
an invertible matrix: the Hessian at `x=0` gives the first coordinate
direction, and adding a Hessian at `x>0` produces a positive definite
matrix. Thus half the rank of the global Hessian span would overestimate
the answer. This rational example complements the smooth-map investigation's
norm example and illustrates why a global-span upper bound need not be sharp.

## Attribution and verification

Perspective geometry and convexity preservation are classical; see Boyd
and Vandenberghe, *Convex Optimization*, Sections 2.3.3 and 3.2.6,
[primary book](https://web.stanford.edu/~boyd/cvxbook/bv_cvxbook.pdf).
The bounded binary-product inequalities are standard. The useful consequence
here is transfer of the new sharp integer-precision laws, including compact
formulation size, to nonpolynomial quadratic-over-linear systems.
No standalone priority claim is made for the formulation transformation.

Independent review checked row homogenization with continuous auxiliaries,
binary products, slice accuracy scaling, both domain versions, and the
rank-one/global-span example. Its two minor count and rationality
clarifications are applied. No new algorithm implementation is claimed.
