# Why convex Hermitian fibers do not globalize q projective channels

Status: Proved local obstructions; not a global ball-lift counterexample  
Started: 2026-09-04  
Paper status: Not incorporated  
Confidence: High

## Result

The selection-free one-channel argument does not extend formally from
\(q=1\) to \(q>1\).  Two independent mechanisms survive all of the
zero-order consequences normally extracted from a standard-barrier bound
\(\nu_{\rm slice}\leq q\):

1. a compact convex dual certificate fiber can merge two rank-one
   projective tokens into one rank-two support face while retaining total
   rank at most \(q\); and
2. a compact convex primal fiber can join two different kernel lines
   through positive-definite matrices while every point has total
   nullity at most \(q\).

The second mechanism occurs in an explicit affine product-PSD slice whose
restricted standard log-determinant has exact parameter \(q\).  Hence
compactness, convexity, semialgebraicity, Slater, and the actual barrier
bound \(\nu_{\rm slice}=q\) do not by themselves make block supports
constant on fibers or produce a continuous unordered \(q\)-tuple of
projective points.

These examples are not lifts of a Euclidean ball of divisible tangent
dimension.  Ball curvature and the full slack identity could still forbid
the mechanisms.  Thus they identify a precise missing ingredient in the
open divisible Hermitian problem rather than refute its conjectured
barrier lower bound.

## 1. What the barrier bound gives to every dual fiber

Let \(\mathcal P(v)\) be a primal lift fiber over a boundary support
\(v\), and let \(\mathcal D(v)\) be its compact convex normalized dual
certificate fiber.  Suppose the restricted standard product barrier has
parameter at most \(q\).  The determinant-order argument gives

\[
                \sum_i\operatorname{nullity}X_i\leq q
                \qquad(X\in\mathcal P(v)).               \tag{1}
\]

For every \(X\in\mathcal P(v)\) and \(Y\in\mathcal D(v)\), blockwise
positivity and zero total pairing give

\[
                  \operatorname{Ran}Y_i\subseteq\ker X_i.
                                                               \tag{2}
\]

Consequently every certificate has total rank at most \(q\).  More
strongly, define the aggregate support

\[
              E_i(v)=\sum_{Y\in\mathcal D(v)}\operatorname{Ran}Y_i.
                                                               \tag{3}
\]

Then

\[
                         \sum_i\dim E_i(v)\leq q.         \tag{4}
\]

Indeed, finitely many certificates span all spaces in (3), and a positive
average of them has blockwise range equal to their range sum.  If (4)
failed, that average would have rank greater than \(q\), contradicting
(1)--(2).

For \(q=1\), a nonzero compact convex certificate fiber can use only one
rank-one ray.  Strictly feasible normalization fixes its scale, so the
fiber is a singleton and its projective support is intrinsic.  For
\(q>1\), (4) permits the following rank merger.

## 2. Dual obstruction: a rank-two face fills a projective cycle

Let \(\mathbb F\in\{\mathbb R,\mathbb C,\mathbb H\}\), and fix a
two-dimensional \(\mathbb F\)-subspace \(U\) in one Hermitian block.
Consider

\[
 \mathcal D_U={Y\succeq0:\operatorname{Ran}Y\subseteq U,
                              \operatorname{tr}_U Y=1\}. \tag{5}
\]

This is the compact trace-one base of \(H_+^2(\mathbb F)\).  Its
rank-one extreme boundary is

\[
                           \mathbb F P^1\cong S^a,
             \qquad a=\dim_{\mathbb R}\mathbb F,         \tag{6}
\]

while its relative interior consists of rank-two matrices.  In
particular, the convex body (5) fills the entire projective-line orbit;
at its scalar center \(I_U/2\), no eigenline or unordered pair of
eigenlines is intrinsic.

Add \(q-2\) fixed rank-one certificates in distinct blocks.  Every
resulting certificate has total rank at most \(q\), and the aggregate
support dimension is exactly

\[
                              2+(q-2)=q.                 \tag{7}
\]

Every primal tuple complementary to the whole fiber has kernel containing
\(U\) in the first block and the \(q-2\) fixed lines in the others.  This
costs exactly \(q\) forced nullity units.  Choosing the primal blocks
positive definite on the complementary subspaces realizes total nullity
exactly \(q\), not \(q+1\).

Thus two generic rank-one support tokens may coalesce into a rank-two
support face without exceeding either the dual rank budget or the primal
nullity budget.  The rank-two face is a genuine topological cap for the
projective incidence that a proposed unordered-configuration proof would
need to preserve.  This operation is impossible when \(q=1\), because a
rank-two member already exceeds the entire rank budget.

## 3. Primal obstruction with exact standard-barrier parameter q

The dual merger has a complementary primal phenomenon: kernel lines can
disappear inside a convex fiber.  This happens in a complete affine
product-PSD example satisfying the exact barrier bound.

Let

\[
 \Delta_q=\{p=(p_0,\ldots,p_q):p_j\geq0,
                                      \sum_{j=0}^q p_j=1\}             \tag{8}
\]

and project by

\[
                              \sigma=\sum_{j=2}^q p_j.   \tag{9}
\]

Encode this simplex with \(q\) real \(2\times2\) PSD blocks:

\[
 X_0=\begin{pmatrix}p_0&0\\0&p_1\end{pmatrix},
 \qquad
 X_j=\begin{pmatrix}1&0\\0&p_{j+1}\end{pmatrix}
                         \quad(1\leq j\leq q-1).         \tag{10}
\]

Together with the affine equality in (8), positive semidefiniteness of
(10) is exactly \(p\in\Delta_q\).  The slice has full Slater at any
strictly positive \(p\).  Its fibers are compact and convex, and its
projection is the interval \([0,1]\).

The fiber over the boundary point \(\sigma=0\) is

\[
 p_2=\cdots=p_q=0,qquad p_0=t,qquad p_1=1-t,
                              \quad0\leq t\leq1.          \tag{11}
\]

Hence

\[
 X_0(t)=\operatorname{diag}(t,1-t),qquad
 X_j=\operatorname{diag}(1,0).                           \tag{12}
\]

For \(0<t<1\), the first block is positive definite and the other
\(q-1\) blocks each have nullity one, so the total nullity is \(q-1\).
At either endpoint, \(X_0\) acquires one kernel direction and the total
nullity is \(q\).  No point of the fiber has nullity \(q+1\):

\[
 \max_{X\text{ in the fiber }(11)}
               \sum_j\operatorname{nullity}X_j=q.       \tag{13}
\]

Nevertheless, the endpoint kernel of \(X_0\) changes from one coordinate
line to the other, and the line vanishes entirely in the relative
interior.  Thus no block-support map descends through this convex fiber.

The restricted standard product log-determinant in (10) is

\[
                 F(p)=-\sum_{j=0}^q\log p_j.             \tag{14}
\]

This is the standard orthant barrier restricted to its trace-one simplex.
Its exact gradient parameter is \(q\).  For completeness, the orthant
barrier is \((q+1)\)-logarithmically homogeneous.  On the base
\(\sum_jp_j=1\), the radial component removes one unit from the squared
dual gradient norm, giving the upper bound \(q\).  At a simplex vertex,
exactly \(q\) coordinates vanish, so the determinant-order lower bound
gives \(\nu\geq q\).  Therefore

\[
                              \boxed{\nu_F=q}.            \tag{15}
\]

Equations (11)--(15) show that even the actual bound \(\nu_F=q\), not
merely a pointwise rank surrogate, permits a compact boundary fiber that
erases and switches projective kernel data without paying nullity
\(q+1\).

An equivalent radial determinant germ is

\[
                   \sigma^{q-1}(t+\sigma)(1-t+\sigma).   \tag{16}
\]

At \(\sigma=0\), its vanishing order is \(q-1\) for
\(0<t<1\) and \(q\) at the endpoints.  This is exactly the support-switch
pattern in (12).

## 4. Precise consequence for the divisible Hermitian gap

In the divisible ball regime

\[
                         s-1=q\,a(R-1),                  \tag{17}
\]

generic mixed-curvature equality gives \(q\) rank-one projective channels
in full-order blocks.  The examples above prove that certificate-fiber
convexity and a barrier bound do not, by themselves, globalize those
generic channels:

* two channels may merge into one rank-two support face, changing the
  orbit type from two projective points to a two-plane; and
* primal kernel lines may terminate at a positive-dimensional fiber and
  be joined through higher-rank matrices.

Therefore a proof cannot simply replace a selected ordered configuration
by an unordered configuration and invoke sphere-versus-product topology.
It must additionally use the full ball slack identity, its nondegenerate
mixed curvature, or an affine-determinantal integrability condition to
exclude rank mergers and kernel-erasing fibers.  No such exclusion is
proved here.

Conversely, (5) and (10) are not a global affine lift of the ball in
(17).  They do not show that the conjectured divisible Hermitian barrier
bound is false.

## Self-audit checklist

1. In (1), verify determinant order at every boundary tuple, not merely
   along a selected contact sheet.
2. In (4), take a finite spanning subfamily before averaging, and use PSD
   range additivity blockwise.
3. In (5)--(7), distinguish aggregate support dimension from the rank of
   an individual extreme certificate.
4. In (10), check that positive semidefiniteness is exactly coordinate
   nonnegativity and that the slice has a positive-definite point.
5. In (11)--(13), count the first block as nullity zero in the open fiber
   and nullity one only at its endpoints.
6. In (15), distinguish the \((q+1)\)-parameter homogeneous orthant
   barrier from its exact parameter-\(q\) trace-one restriction.
7. Do not cite either obstruction as a counterexample to a Euclidean-ball
   lift theorem; the projected body in Section 3 is only an interval.
