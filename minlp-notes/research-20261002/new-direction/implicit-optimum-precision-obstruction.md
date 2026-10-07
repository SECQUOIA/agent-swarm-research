# Uniform conditioning does not bound rectangular certification precision

Date: 2026-10-02. Status: elementary proofs with fresh independent review.
No literature priority claim.

Fixed polynomial degree, fixed interaction width, and uniform quadratic
growth do not bound the size of every rational enclosure used to certify an
exact optimizer. The examples below are globally strongly convex. The first
requires exponentially many endpoint bits if an enclosing box must lie
strictly inside the feasible domain. The second requires exponentially many
endpoint bits if a box must certify even the weak active KKT sign throughout
its free-coordinate rectangle. Its width is two and its curvature-to-growth
ratio is the constant \(112/27\).

These are limitations of specified certificate formats, not an impossibility
result for compact implicit exact optimization. Both optimizers have short
recurrences and short symbolic optimality proofs. In particular, proofs that
retain the equations' correlations need not certify signs throughout an
independent-coordinate rectangle.

The construction adapts the small-state recurrence in the
[nonlinear dynamics note](nonlinear-dynamics.md#7-counts-and-exact-real-scope).
It complements the [expanded algebraic output obstruction](../geometric-dp/algebraic-output.md):
here every optimizer coordinate is rational, and endpoint precision is the
issue rather than algebraic degree.

## 1. A path with a tiny interior coordinate

For \(n\ge1\), take \(X=[0,1/2]^{n+1}\), and define

\[
r_0(x)=x_0-\tfrac14,\qquad
r_i(x)=x_i-\tfrac14x_{i-1}^2\quad(1\le i\le n),\qquad
F(x)=\sum_{i=0}^n r_i(x)^2.
\tag{1}
\]

There are \(n+1\) constant-size rational factors, each of degree at most
four. The interaction graph is a path of width one. Coefficients and interval
endpoints have constant bit length. An indexed factor list has total input
length \(I=O(n\log(n+1))\).

The recurrence

\[
a_0=\tfrac14,\qquad a_i=\tfrac14a_{i-1}^2
      =2^{-(4\cdot2^i-2)}
\tag{2}
\]

defines a point strictly inside \(X\). All residuals vanish there, so
\(F(a)=0\). Conversely, vanishing residuals force (2). Thus \(a\) is the
unique global optimizer.

## 2. Growth, curvature, and global positive definiteness

For \(e=x-a\), the residuals satisfy

\[
r_0=e_0,\qquad
r_i=e_i-\frac{x_{i-1}+a_{i-1}}4e_{i-1}.
\]

Consequently \(r=(I-P)e\), where \(P\) is a weighted lower shift with
weights at most \(1/4\). Since \(\|P\|_2\le1/4\),

\[
F(x)=\|r\|_2^2\ge\tfrac9{16}\|x-a\|_2^2.
\tag{3}
\]

For each \(i<n\), direct differentiation gives

\[
\partial_{ii}F=2+\tfrac34x_i^2-x_{i+1}\le\tfrac{35}{16},
\qquad \partial_{nn}F=2.
\tag{4}
\]

Hence the upper coordinate curvature and global quadratic growth constants
can be chosen as \(L=35/16\) and \(g=9/16\), with
\(\kappa=L/g=35/9\).

There is also a uniform global Hessian bound. Write \(J=Dr\). Its diagonal
entries are one and its subdiagonal entries are \(-x_{i-1}/2\), so
\(\|I-J\|_2\le1/4\). The exact Hessian identity is

\[
\nabla^2F=2J^\top J-\operatorname{diag}(r_1,\ldots,r_n,0).
\]

Every \(r_i\le1/2\) on \(X\). Therefore

\[
\nabla^2F(x)\succeq
\left(2(3/4)^2-1/2\right)I=\tfrac58 I\qquad(x\in X).
\tag{5}
\]

The tiny coordinate is thus compatible with global strong convexity, not
merely local Hessian positive definiteness.

## 3. A strict-interior box can require exponentially many bits

Use the ordinary binary rational format: an endpoint is written as an
integer numerator and a positive integer denominator in binary, without a
compressed exponent or arithmetic circuit. Let a closed rational rectangle
\(B=\prod_{i=0}^n[\ell_i,u_i]\) satisfy

\[
a\in B\subset(0,1/2)^{n+1}.
\]

Put \(m=4\cdot2^n-2\). Its terminal lower endpoint obeys
\(0<\ell_n\le a_n=2^{-m}\). Writing \(\ell_n=p/q\) with integers
\(p\ge1\) and \(q\ge1\) yields

\[
q\ge p2^m\ge2^m.
\tag{6}
\]

The denominator alone needs at least \(m+1=4\cdot2^n-1\) bits. Reduction
to lowest terms cannot evade this argument. The bound is exponential in
\(n\) and superpolynomial in the indexed input length. Fixed width and
fixed \(\kappa\) therefore cannot give an
\(\operatorname{FPT}(p,\kappa)\operatorname{poly}(I)\) total runtime for
this mandatory output format, where \(p\) denotes maximum bag size.

Containment in the open feasible domain is essential. Merely requiring the
optimizer to be an interior point of the enclosing rectangle does not imply
this containment. A rectangle can touch a feasible boundary, or extend
outside the feasible domain, while still containing the optimizer in its
interior. Equation (6) does not apply when its lower endpoint is zero or
negative.

Indeed, define \(T_0(x)=1/4\) and \(T_i(x)=x_{i-1}^2/4\). This map
preserves the closed box \(X\) and has Euclidean Lipschitz constant at most
\(1/4\). The contraction theorem proves existence and uniqueness of its
fixed point using that closed box with constant-size endpoints. Together
with \(F=\|x-T(x)\|^2\), this gives a short exact optimality certificate.
No strictly interior rational enclosure is needed for that proof.

## 4. A tiny active derivative with the same conditioning properties

Add \(y\in[0,1/2]\), and define

\[
h(x)=x_n-\tfrac18x_{n-1}^2=\tfrac12(x_n+r_n),\qquad
\widetilde F(x,y)=F(x)+y^2+\tfrac14yh(x).
\tag{7}
\]

The original path together with the terminal bag \(\{x_{n-1},x_n,y\}\)
gives width two and maximum bag size three. Degree, coefficient sizes, and
the number of factors incident to a coordinate remain uniformly bounded.

Since \(x_n,y\ge0\),

\[
\tfrac14yh=\tfrac18yx_n+\tfrac18yr_n
\ge-\tfrac1{16}(y^2+r_n^2).
\]

Using (3) gives the global bound

\[
\widetilde F(x,y)\ge\tfrac{15}{16}(F(x)+y^2)
\ge\tfrac{135}{256}\bigl(\|x-a\|^2+y^2\bigr).
\tag{8}
\]

Thus \((a,0)\) is the unique optimizer, with value zero. Its active-bound
derivative is strictly positive but doubly exponentially small:

\[
\partial_y\widetilde F(a,0)=\tfrac14h(a)=a_n/8.
\tag{9}
\]

The added term changes only one free-coordinate diagonal second derivative,
by \(-y/16\), and \(\partial_{yy}\widetilde F=2\). Thus
\(L=35/16\) remains valid. With \(g=135/256\) from (8),

\[
\kappa=\frac{L}{g}=\frac{112}{27}.
\tag{10}
\]

For completeness, global strong convexity also persists. Relative to
\(\operatorname{diag}(\nabla^2F,2)\), the nonzero Hessian perturbation
entries are

\[
E_{n-1,n-1}=-y/16,\quad
E_{n-1,y}=E_{y,n-1}=-x_{n-1}/16,\quad
E_{n,y}=E_{y,n}=1/4.
\]

The maximum absolute row sum is at most \(9/32\). Since \(E\) is
symmetric, \(\|E\|_2\le9/32\), and (5) gives

\[
\nabla^2\widetilde F\succeq(5/8-9/32)I=\tfrac{11}{32}I.
\tag{11}
\]

## 5. Uniform weak KKT signs on rectangles force long endpoints

Let \(B=\prod_i[\ell_i,u_i]\subseteq X\) be any rational rectangle
containing \(a\). Suppose a certificate proves the active KKT inequality
by establishing

\[
\partial_y\widetilde F(x,0)\ge0\quad\text{for every }x\in B.
\tag{12}
\]

This includes the usual check that a certified interval range has a
nonnegative lower endpoint. On the nonnegative rectangle, the exact range
minimum is

\[
\min_{x\in B}\partial_y\widetilde F(x,0)
=\tfrac14\left(\ell_n-u_{n-1}^2/8\right).
\tag{13}
\]

Because \(u_{n-1}\ge a_{n-1}\), (12) forces

\[
0<a_n/2=a_{n-1}^2/8\le\ell_n\le a_n=2^{-m}.
\tag{14}
\]

The denominator bound (6) follows again. Even allowing the enclosing box to
touch the original feasible boundary cannot avoid it: the uniform sign
requirement itself forces a positive terminal lower endpoint. Requiring a
strictly positive derivative range would only strengthen the requirement.

This is an exact-range obstruction. It is not caused by repeated-variable
overestimation in a particular implementation of interval arithmetic. At the
corner \(x_n=\ell_n\), \(x_{n-1}=u_{n-1}\), the lower bound (13) is
attained. Sound range computation on the entire rectangle cannot discard
that corner simply because it fails the residual equations.

Consequently, even at fixed degree, width two, and \(\kappa=112/27\),
there is no polynomial bound on the ordinary rational endpoint size of
rectangles that enclose the optimum and certify its active derivative sign
uniformly on the free-coordinate rectangle.

## 6. What remains possible

Both families admit compact exact representations and certificates:

- Recurrence (2), with shared intermediate values, represents the optimizer
  using \(O(n)\) arithmetic operations. Its expanded rational denominators
  need not be written.
- The closed-box contraction proof above isolates the first family's root.
  Nonnegativity of the squares proves its optimality.
- In the second family, \(r_n(a)=0\) proves
  \(h(a)=a_n/2>0\) using (2). Inequality (8) certifies global optimality and
  uniqueness without a rectangular derivative-sign bound. Positivity follows
  inductively from positive initial state and squaring.
- A signed mantissa with a binary exponent can express the particular dyadic
  coordinates compactly. The lower bounds concern explicitly written integer
  numerators and denominators, not all encodings of rational numbers.

In particular, an implicit root representation with a rational isolating
box, a Hessian certificate, and an interval-Newton or Krawczyk argument is
not ruled out as a whole. A proposed complexity proof must specify whether
it requires a box inside the open feasible domain, and whether active signs
are certified on the whole rectangle or only at the correlated implicit
root. The two size lower bounds apply to the respective stronger
requirements. Methods preserving residual equations, allowing suitable
boundary-touching boxes, or using other compact proofs need separate
analysis.

The examples show that the stated growth and curvature parameters do not
control interior slack or nonzero active derivative magnitudes. They do not
prove a lower bound for all exact algorithms, exact optimal values, or all
implicit certificates. Both exact optimal values here are zero.

## 7. Verification

The arguments above are algebraic proofs for every \(n\), rather than
claims inferred from numerical sampling. The targeted checker
`check_implicit_optimum_precision.py` supplements them with exact rational
checks of the recurrence, denominator lengths, residual and Hessian
identities, growth inequalities, perturbation bounds, and rectangular sign
minimum. Its finite checks are not a substitute for the proofs.

The targeted command actually run was

```text
python3 research-20261002/new-direction/check_implicit_optimum_precision.py
```

It passed 120 exact-rational configurations at horizons \(n=1,2,3,5,8\),
45 rectangular sign checks, recurrence and denominator-length checks at
those five horizons, and both conditioning-ratio checks. The Hessian checks
include exact elimination certificates for the stated shifted matrices at
the tested configurations. No project-wide verification or CI inspection
was run. A [fresh independent actual-file review](../reviews/implicit-optimum-precision-review.md)
checked all constants, the endpoint encoding argument, and the precise scope
of rectangular sign certification, and found no blocking issue. This is an
internal mathematical review, not external peer review.
