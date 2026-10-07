# A connected nonconvex obstruction for corrected coordinate grids

This note strengthens the certificate obstruction in
[projection-anchors.md, Section 8](projection-anchors.md#8-an-intrinsic-obstruction-from-optimal-coordinate-projections).
It concerns that specific lower-bound formula and explicit Cartesian grid
tables. It is not an optimization hardness result or a barrier for all
algorithms using tree decompositions.

## 1. A fixed rational example

On \([0,1]^4\), define

\[
 F(x,y,u,v)=(x-y)^2+u^2+v^2-3uv+\frac{u+v}{2}
             +\frac{(x-y)(u-v)}4.
\]

Its minimum is zero, and its optimal set is

\[
 S=\{(t,t,0,0):0\le t\le1\}
   \cup\{(t,t,1,1):0\le t\le1\}.
\]

Every Hessian diagonal is 2, so the coordinate upper-curvature bound is
\(L=2\). Every pair of variables interacts: the interaction graph is
\(K_4\), with treewidth 3 and a four-variable bag. The Hessian is
indefinite, since its quadratic form is negative in direction
\((0,0,1,1)\) and positive in direction \((1,-1,0,0)\).
Each partial derivative takes both signs on the box. Thus no variable can
be eliminated by global coordinate monotonicity.

The global growth inequality is

\[
 F(w)\ge\frac12\operatorname{dist}(w,S)^2,
 \qquad w\in[0,1]^4.
\]

To verify it, write

\[
 a=x-y,\qquad t=\frac{u+v}{2},\qquad d=\frac{u-v}{2},
 \qquad m^2=\min\{t^2,(1-t)^2\}.
\]

Then

\[
 \operatorname{dist}(w,S)^2=\frac{a^2}{2}+2m^2+2d^2,
\]

and

\[
 F(w)-\frac12\operatorname{dist}(w,S)^2
 =\frac34a^2+\frac12ad+4d^2+t(1-t)-m^2.
\]

The quadratic in \((a,d)\) is positive definite, and the final difference
is nonnegative for \(0\le t\le1\). The resulting growth inequality forces
every zero of \(F\) into \(S\), and direct substitution gives zero on
\(S\). The growth constant \(g=1/2\) is sharp: take \(x=y\) and
\(u=v=1/2\). Consequently \(L/g=4\) is fixed.

## 2. Arbitrary coordinate grids

Let \(X,Y,U,V\) be arbitrary finite grids spanning \([0,1]\), including
both endpoints. At a node \(r\) of grid \(i\), let \(\ell_i(r)\) be the
largest length of an adjacent grid interval. Consider precisely the
corrected-grid lower bound

\[
 LB=\min_{w\in X\times Y\times U\times V}G(w),
 \qquad
 G(w)=F(w)-\frac14\sum_i\ell_i(w_i)^2.
\]

If \(\Delta_X\) is the largest gap in \(X\), then

\[
 LB\le-\frac{\Delta_X^2}{4}.
\]

Indeed, choose an endpoint \(x\) of a largest \(X\)-gap, so that
\(\ell_x(x)=\Delta_X\). If \(x\in Y\), choose \(y=x\). Otherwise choose
the closer endpoint \(y\) of the \(Y\)-gap containing \(x\). In either
case,

\[
 (x-y)^2\le\frac14\ell_y(y)^2.
\]

Use the grid assignment \((x,y,0,0)\), where \(F=(x-y)^2\). The
\(y\)-correction cancels this objective value, and the \(x\)-correction
leaves at most \(-\Delta_X^2/4\). The other two corrections are
nonpositive. The same argument with \(X,Y\) exchanged proves

\[
 LB\le-\frac14\max\{\Delta_X^2,\Delta_Y^2\}.
\]

This proof allows arbitrary offsets, nonuniform gaps, and different grids
for the two coordinates. It does not assume matching nodes except for the
required box endpoints. It also follows from the conditional-margin lemma
in the linked note: both optimal coordinate projections equal \([0,1]\).

## 3. Consequences and limits

Every feasible incumbent has value \(UB\ge0\). A certificate
\(UB-LB\le\varepsilon\) therefore requires

\[
 \Delta_X,\Delta_Y\le2\sqrt\varepsilon.
\]

Each of \(X,Y\) must have at least
\(1+\lceil1/(2\sqrt\varepsilon)\rceil\) nodes. Explicit Cartesian bag
tables consequently have at least \(\Omega(\varepsilon^{-1})\) entries,
already from the \(x,y\) coordinates. With \(\varepsilon=2^{-q}\), this
is exponential in the requested accuracy bits \(q\), even though the
dimension, treewidth, coefficient sizes, and growth ratio are constant.

Any coordinate-domain pruning that preserves every global optimizer must
retain all of \([0,1]\) in both \(x\) and \(y\). Taking a coordinate hull
cannot improve this. Separating the two connected components of \(S\)
does not help, since each component has these same full projections.

The conclusion applies to the stated corrected objective on grids covering
the retained coordinate domains. A method may evade it by selecting and
certifying one optimizer, using a stronger joint lower bound, recognizing
algebraic structure, or representing computations implicitly. This note
does not rule out any of those alternatives. In particular, the example's
explicit optimal set makes the optimization problem itself easy.

## 4. Targeted verification

The proof was checked directly in rational arithmetic with
`python3 -B research-20261002/new-direction/check_nonconvex_certificate_barrier.py`.
The script checks the growth identity on a rational mesh and the arbitrary
grid witness on independently generated nonuniform coordinate grids.
No project-wide checks, CI inspection, or external search were performed.
