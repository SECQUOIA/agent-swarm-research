# Review of integer polynomial escape increments

Date: 2026-09-27. Status: independent adversarial review of the proposed
strengthening of [the escape-curve note](succinct-unboundedness-curves.md).
This review checks the argument, not publication priority.

**Conclusion.** The strengthened claim is valid. For rational convex
quadratic constraints and objective, a nonempty mixed-integer feasible set
has objective unbounded below if and only if its continuous relaxation
does. Conditional on mixed-integer feasibility, rational linear programming
classifies objective boundedness in polynomial time with no restriction on
the integer dimension or Hessian span. A supplied anchor radius gives a
polynomial-size escape circuit whose increments have integer coefficients
in every coordinate. The proof does not require projected anchors to be
mixed-integer.

## 1. Coordinate sections preserve continuous objective values

At a zero-objective-slope recession direction \(d\), choose any index
\(j\) with \(d_j\ne0\), and let \(A\) insert a zero in coordinate
\(j\). There is a unique decomposition

\[
 w=Ay+ds,\qquad s=w_j/d_j,
 \qquad y=(w-dw_j/d_j)_{-j}.
\]

All coordinates are treated as continuous during this construction. Since
\(Q_i d=0\), each constraint is

\[
 q_i(Ay+ds)=r_i(y)+\alpha_i s,
 \qquad r_i(y)=q_i(Ay),\quad \alpha_i=a_i^Td\le0.
\]

The objective and affine equations have zero slope. Delete the constraints
with negative slope and retain all other constraints. Every retained
feasible point lifts to an original continuous feasible point by making
\(s\) sufficiently large. Thus continuous attainable objective values
are preserved exactly.

The section is especially useful for complexity: every retained polynomial
is obtained by removing the monomials containing the selected coordinate.
Its coefficients are a subset of the previous coefficients, even though
the projection map for anchors involves a rational shear. The shear is not
substituted into the retained problem.

If no negative-objective recession direction appears and the process
reaches zero recession cone, every nonempty continuous objective sublevel
is compact. A feasible sublevel therefore contains a global minimizer.
Consequently continuous objective unboundedness forces a negative direction
to appear after at most the original number of variables in eliminations.

## 2. Integer increments do not require integer projected anchors

Choose positive integers clearing the denominators of each selected
direction. At the terminal negative direction, use
\(p_*(T)=g_*T\), where \(g_*=D_*d_*\in\mathbb Z^r\).
This gives objective change \(-\gamma T\), with
\(\gamma=-a_{0,*}^Tg_*>0\).

For a reverse step, suppose \(p_y\in\mathbb Z[T]^r\),
\(p_y(0)=0\), and an integer polynomial \(B\), with nonnegative
coefficients and \(B\ge1\), bounds every coordinate of
\(y^0+p_y(T)\) for \(T\ge0\). The original anchor at this step is
\(w^0=Ay^0+ds^0\). It is enough to know an integer bound
\(M_s\ge |s^0|\).

For each deleted row let \(H_i\) be its monomial coefficient absolute
sum and \(\beta_i=-\alpha_i>0\). Choose integers

\[
 C\ge1+M_s+\max_i H_i/\beta_i,
 \qquad D\ge1,\qquad g=Dd\in\mathbb Z^{r+1}.
\]

The maximum is zero when there are no deleted rows. Define

\[
 F(T)=C T(1+B(T)^2),\qquad
 P(T)=D F(T),\qquad
 p_w(T)=A p_y(T)+g F(T).
\]

Because \(A\) is a coordinate insertion matrix, this expression proves
directly that \(p_w\in\mathbb Z[T]^{r+1}\), and it has zero
constant term. In particular, the increment circuit can use integer
constants exclusively; the rational directions remain part of the proof
trace.

The reconstructed point is

\[
 w^0+p_w(T)=A(y^0+p_y(T))+d(s^0+P(T)).
\]

For real \(T\ge1\), each deleted row is bounded above by

\[
 H_i B(T)^2+\beta_i M_s
       -\beta_i D C T(1+B(T)^2)\le0.
\]

Rows of zero slope and all equations follow from the reduced problem.
Choosing an integer \(L\ge\max\{1,\|d\|_\infty\}\) gives the
next valid coordinate majorant

\[
 B_w(T)=L\bigl(B(T)+M_s+P(T)\bigr),\qquad T\ge0.
\]

This closes the induction. At an integer parameter, adding the final
integer vector to an original mixed-integer anchor preserves every
designated integer coordinate. No projected anchor needs to be integral.
All objective changes except the terminal one are zero.

## 3. Size and classifier scope

The following bounds are sufficient and do not use fixed parameters.

- Reduced coefficients only disappear. Every recession LP therefore has
  encoding length polynomial in the original input length \(N\).
- Polynomially many rational LP calls find polynomial-bit directions or
  detect zero recession cone. Negative slope is tested by normalizing it
  to at most \(-1\); nonzero cone membership is tested by the coordinate
  normalizations \(d_j\ge1\) and \(d_j\le-1\).
- Products of polynomially many polynomial-bit rational projection
  matrices have polynomial bit length. One can see this by clearing each
  matrix's denominators before multiplying: denominator bit lengths add,
  and numerator bit lengths add with the logarithms of the intermediate
  dimensions.
- A supplied rational radius \(R\) thus gives polynomial-bit bounds on
  all projected anchors and removed anchor scalars. The terminal majorant
  must bound the *scaled* direction \(g_*\), not only \(d_*\).
- Denominator-clearing integers, row coefficient sums, slope ratios, and
  the constants \(C,L,M_s\) all have polynomial bit length in
  \(N+\operatorname{bits}(R)\). Expanded polynomial coefficients need
  not have polynomial bit length and are never generated.
- Each reverse step changes the degree bound from \(b\) to at most
  \(2b+1\). Starting at degree one gives
  \(\deg p\le2^{\ell+1}-1\) after \(\ell\) eliminations. The
  arithmetic circuit shares previous expressions, so it has polynomial
  size.

The classification algorithm needs neither an anchor nor its radius.
Under the feasibility promise, an anchor exists and has some finite
radius; the construction then proves that continuous objective
unboundedness implies mixed-integer objective unboundedness. The reverse
implication follows by inclusion. If the terminal recession cone is zero,
continuous boundedness also implies mixed-integer boundedness.

This is a promise classification, not a polynomial-time mixed-integer
feasibility algorithm. The trace by itself is not an unconditional
certificate that a mixed-integer feasible point exists. Producing a small
encoded feasible anchor is a separate issue; fixed-parameter common-field
anchor results may still be used for that issue. The construction also
does not justify preserving mixed-integer *attainable values* at the
intermediate projections. Only continuous attainable values are preserved
there. Integer increments restore the property needed for the final
unboundedness conclusion.

## 4. Exact check with a fractional projected anchor

Consider two integer variables, constraint
\((z_1-2z_2)^2-z_1\le0\), objective \(-z_1+2z_2\), and anchor
\(a=(1,0)\). The direction \(d=(2/3,1/3)\) has zero objective
slope. Eliminating coordinate one gives
\(y=z_2-z_1/2\), so the projected anchor is \(-1/2\).
The only constraint is deleted and the terminal increment is \(-T\).

For the original radius \(R=1\), valid choices are
\(B=2(1+T)\), \(M_s=2\), \(C=9\), and \(D=3\). The resulting
increment is

\[
 p(T)=\left(18T(1+4(1+T)^2),
            -T+9T(1+4(1+T)^2)\right).
\]

Both entries have integer coefficients and zero constant terms. Exact
symbolic substitution gives the constraint value
\(-72T^3-140T^2-86T\) and objective \(-1-2T\). This explicitly
checks an elimination that destroys anchor integrality while preserving
the required final integrality.

Targeted verification run: an inline `python` program using SymPy expanded
these expressions, checked both polynomial coefficient domains were
`ZZ`, checked zero constant terms, and asserted the displayed constraint
and objective identities. Result: passed. No project-wide checks or CI
inspection were performed.
