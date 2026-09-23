# Cone-meet compilers and a fixed-rank Lorentz obstruction

Status: Proved; independently audited  
Started: 2026-09-04  
Paper status: Not incorporated  
Confidence: High on mathematics; moderate on QIPM novelty  

## Exact one-translate compression is a lattice property

Let \(K\subset V\) be a finite-dimensional closed, pointed, generating cone,
write \(x\leq_Ky\) when \(y-x\in K\), and put
\(\downarrow a=a-K\).  The following are equivalent:

\[
 \begin{split}
 &\text{for every }a,b\in V\text{ there is }c\in V\text{ with }
 (\downarrow a)\cap(\downarrow b)=\downarrow c;\\
 &(V,\leq_K)\text{ is a vector lattice};\\
 &K\text{ is simplicial: }K=T\mathbb R_+^d
 \text{ for some invertible }T.
 \end{split}                                                  \tag{1}
\]

Indeed, equality of lower sets says exactly that \(c=a\wedge b\).  Meets
give joins by negation.  Closedness makes the finite-dimensional ordered
space Archimedean, and the finite-dimensional vector-lattice representation
theorem identifies its positive cone with a linear image of
\(\mathbb R_+^d\).  Conversely, coordinatewise minima prove the last
implication directly.

Thus a compiler allowed to synthesize a new apex can summarize arbitrary
translated-cone intersections by one translate exactly for simplicial cones.
If it must retain one of the two input constraints, universal compilation
requires a total order and hence dimension one.  Every genuine
nonsimplicial cone already has a two-offset obstruction, including Lorentz
cones of dimension at least three and PSD cones of matrix size at least two.
The finite-dimensional hypothesis is essential.

## A rank rather than poset-width compiler

For \(K=T\mathbb R_+^d\) and arbitrary apices \(a_1,\ldots,a_N\),

\[
 \bigcap_{i=1}^N(a_i-K)=c-K,\qquad
 c=Tm,\qquad
 m_j=\min_i(T^{-1}a_i)_j.                                   \tag{2}
\]

The apices may form an antichain of width \(N\); only the \(d\) coordinate
minima matter.  With coherent access to transformed entries
\((T^{-1}a_i)_j\), all coordinates of \(m\) can be found in

\[
 \widetilde O(d\sqrt N)
\]

queries.  This is tight for explicit classical output:

\[
 Q=\Theta(d\sqrt N),\qquad R=\Theta(dN),
\]

by putting an independent unique-search instance in every coordinate and
using the direct-sum adversary.

The natural scenario-product logarithmic barrier has parameter \(Nd\),
whereas the compiled translate has the optimal simplicial parameter \(d\).
On an all-equal radial instance, their metric lengths between slack scales
\(\alpha_0,\alpha_1\) are exactly

\[
 \sqrt{Nd}\left|\log\frac{\alpha_0}{\alpha_1}\right|,
 \qquad
 \sqrt d\left|\log\frac{\alpha_0}{\alpha_1}\right|.
\]

These are statements about the explicit barriers, not lower bounds on all
IPMs.  If only physical coordinates of \(a_i\) are available and \(T^{-1}\)
is dense, one transformed entry can itself cost \(d\) queries and forming
\(Tm\) costs \(O(d^2)\) arithmetic.

## Product-ray extension beyond symmetric cones

Let

\[
 K=\prod_{j=1}^B K_j,\qquad
 a_i=(r_{i1}e_1,\ldots,r_{iB}e_B),
\]

with \(e_j\in\operatorname{int}K_j\).  Even if the scenario vectors \(r_i\)
are pairwise incomparable,

\[
 \bigcap_i(a_i-K)
 =\prod_{j=1}^B(r_{*j}e_j-K_j),\qquad
 r_{*j}=\min_i r_{ij}.                                      \tag{3}
\]

Hence product power-cone, exponential-cone, nonsymmetric homogeneous-cone,
or quantum-relative-entropy models with one ordered radial uncertainty in
each factor compile using

\[
 \widetilde\Theta(B\sqrt N)
\]

scalar-radius queries.  The compiled barrier parameter is at most
\(\sum_j\nu_j\), instead of the natural scenario-product value
\(N\sum_j\nu_j\).  Formula (3) is the maximal obviously safe factorwise
extension of the chain compiler: arbitrary motion within a nonsimplicial
factor is blocked by (1).

## \(N\) indispensable factors in rank-two Lorentz geometry

The failure is stronger than a two-set counterexample.  Let

\[
 L_3=\{(t,z)\in\mathbb R\times\mathbb R^2:t\geq\|z\|_2\},
\]

choose distinct unit vectors \(v_1,\ldots,v_N\) and \(0<\rho<R\), and define

\[
 a_i=(0,\rho v_i),\qquad
 C_N=\bigcap_{i=1}^N(a_i-L_3).
\]

Every exact finite same-space representation with the same cone orientation,

\[
 C_N=\bigcap_{\ell=1}^m(c_\ell-L_3),
\]

has

\[
 \boxed{m\geq N.}                                           \tag{4}
\]

On the slice \(t=-R\), the body is the intersection of disks

\[
 C_N\cap\{t=-R\}=\bigcap_i B(\rho v_i,R).
\]

The point \(z_i=-(R-\rho)v_i\) lies on the \(i\)-th circle and strictly
inside every other disk, because for \(j\ne i\)

\[
 \|z_i-\rho v_j\|^2
 =(R-\rho)^2+\rho^2+
 2\rho(R-\rho)\langle v_i,v_j\rangle<R^2.
\]

Thus every original circle contributes a distinct open boundary arc.  A
different circle intersects such an arc in at most two points, so a finite
alternative disk intersection must contain a circle coinciding with each
original one.  This proves (4).

A path-consensus lift of this family has constant block incidence and block
treewidth one.  Therefore fixed cone rank and treewidth do not bound the
number of surviving translated factors; ordering or lattice structure is
genuinely doing work.

The scope of (4) is exact and narrow.  It does not exclude auxiliary-variable
SOC or SDP lifts, projections, affine images, nonlocal barriers, or arbitrary
extended formulations.  It proves only that a compiler restricted to
same-oriented translated-\(L_3\) factors retains at least \(N\) factors and
therefore the canonical product parameter \(2N\).

## Novelty boundary

Finite-dimensional vector-lattice representation and coordinatewise
compilation for simplicial cones are classical.  A targeted search found no
source connecting them to the rank-versus-poset-width quantum query law,
product-cone radial compilation, or the fixed-rank Lorentz factor lower bound
in a QIPM setting.  Those connections are the apparent novelty; priority is
not guaranteed.
