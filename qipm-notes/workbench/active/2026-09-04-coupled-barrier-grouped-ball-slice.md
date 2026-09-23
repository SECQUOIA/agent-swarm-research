# Coupling cannot lower the barrier parameter of the grouped ball slice

Status: Proved; targeted literature screen complete; independently hostile-audited  
Started: 2026-09-04  
Paper status: Not incorporated  
Confidence: High for the fixed grouped slice; the extension to arbitrary
globally selected small-cap lifts is deliberately left open

## Result

The reduced grouped Lorentz formulation of a product of Euclidean balls has
an intrinsic barrier parameter equal to its number of groups.  This remains
true for an arbitrary self-concordant barrier that couples every group and
every source ball; logarithmic homogeneity and separability are not assumed.

For source ball \(a\in[k]\), partition its \(s_a\) coordinates into
nonempty groups \(G\in\mathcal G_a\).  Put

\[
 L=\sum_{a=1}^k |\mathcal G_a|
\]

and consider the relative-open affine slice

\[
 \Omega=\left\{(s_{aG},w_{aG}):
 q_{aG}:=s_{aG}-\|w_{aG}\|_2^2>0,
 \quad \sum_{G\in\mathcal G_a}s_{aG}=1\quad(a\in[k])
 \right\}.                                                \tag{1}
\]

This is obtained from the Lorentz constraints

\[
 \left({1+s_{aG}\over2},{1-s_{aG}\over2},w_{aG}\right)
 \in Q_{|G|+2}.                                           \tag{2}
\]

Let \(\vartheta_{\rm opt}(\Omega)\) denote the infimum of the parameters
of all self-concordant barriers on \(\Omega\) whose Hessian is positive
definite on \(\operatorname{aff}\Omega\).  Then

\[
                         \boxed{\vartheta_{\rm opt}(\Omega)=L.} \tag{3}
\]

In particular, for \(C=(B_2^s)^k\) and a Lorentz dimension cap \(d\), the
separate grouped construction with

\[
 h=\left\lceil {s\over d-2}\right\rceil
\]

has

\[
             \boxed{\vartheta_{\rm opt}(\Omega)=kh}
             \qquad(3\le d<s+1),                           \tag{4}
\]

while the direct one-group construction has

\[
             \boxed{\vartheta_{\rm opt}(\Omega)=k}
             \qquad(d\ge s+1).                            \tag{5}
\]

Thus a custom coupled barrier cannot improve the exact parameter of the
standard restricted Lorentz barrier on these fixed affine formulations.
For comparison, the projected body \((B_2^s)^k\) itself has exact optimal
barrier parameter \(k\).  Hence the small-cap grouped lift has an intrinsic
barrier tax

\[
                 \vartheta_{\rm opt}(\Omega)
                 -\vartheta_{\rm opt}((B_2^s)^k)=k(h-1).    \tag{5a}
\]

This tax cannot be removed by coupling the barrier while the affine lift is
held fixed.

The generic short-step certificate remains

\[
                    O\!\left(\sqrt{kh}\log{\Delta\over\epsilon}\right) \tag{6}
\]

in the capped branch, where \(\Delta\) denotes the usual initialization or
gap scale for the chosen path-following theorem.  Equation (3) is a
barrier-parameter lower bound, not
a lower bound on the number of iterations taken by every IPM or QIPM.

## 1. The hidden affine cube

For every group choose a number \(\sigma_{aG}>0\) such that

\[
                  \sum_{G\in\mathcal G_a}\sigma_{aG}=1,
\]

and choose a unit vector \(e_{aG}\in\mathbb R^{|G|}\).  Intersect (1)
with the affine subspace

\[
                   s_{aG}=\sigma_{aG},\qquad
                   w_{aG}=t_{aG}e_{aG}.                    \tag{7}
\]

On this subspace the inequalities in (1) are exactly

\[
                   -\sqrt{\sigma_{aG}}<t_{aG}
                   <\sqrt{\sigma_{aG}}.                    \tag{8}
\]

Consequently

\[
       \Omega\cap\mathcal H
       \cong\prod_{a,G}(-\sqrt{\sigma_{aG}},
                         \sqrt{\sigma_{aG}}),               \tag{9}
\]

an open \(L\)-cube.  Every relative-boundary point of (9) has some
\(q_{aG}=0\), hence is also a boundary point of \(\Omega\).  Therefore the
restriction to (9) of any \(\vartheta\)-self-concordant barrier on
\(\Omega\) is a \(\vartheta\)-self-concordant barrier on the cube.

Nesterov and Nemirovskii's Proposition 2.3.6 says that every
self-concordant barrier on an \(L\)-dimensional cube has parameter at least
\(L\): at a cube vertex, \(L\) linearly independent facets are active.
Affine invariance and restriction therefore give

\[
                          \vartheta\ge L.                   \tag{10}
\]

This proof permits arbitrary mixed derivatives across all groups.  In
particular, off-diagonal Hessian blocks cannot evade (10).

## 2. Matching barrier

The restricted standard Lorentz-product barrier is

\[
                  F_0(s,w)=-\sum_{a,G}\log q_{aG}.          \tag{11}
\]

One summand \(f(s,w)=-\log(s-\|w\|^2)\) is an exact
one-self-concordant barrier on its paraboloid epigraph.  Along an arbitrary
line, put

\[
        A={q'\over q},\qquad C={2\|\dot w\|^2\over q}\ge0.
\]

Then

\[
 f''=A^2+C,\qquad f'''=-2A^3-3AC,
\]

and

\[
 4(A^2+C)^3-(2A^3+3AC)^2=3A^2C^2+4C^3\ge0.               \tag{12}
\]

Moreover, direct Hessian inversion gives

\[
       (\nabla^2f)^{-1}\nabla f=(-q,0),\qquad
       \|\nabla f\|_{(\nabla^2f)^{-1}}^2=1.                \tag{13}
\]

The sum in (11) is therefore an \(L\)-self-concordant barrier, and affine
restriction to the equations in (1) cannot increase its parameter.  With
(10), this proves (3) and also proves that (11) remains exact after all
allocation equalities are imposed.

The base-body comparison in (5a) has the same two-line proof.  The barrier

\[
                    -\sum_{a=1}^k\log(1-\|x_a\|^2)         \tag{13a}
\]

has parameter \(k\).  Fixing all but one coordinate direction in each ball
gives a \(k\)-cube section, so no arbitrary coupled barrier on the product
body can have smaller parameter.

The same theorem applies verbatim to the grouped PSD Schur-complement lift

\[
 \begin{pmatrix}s_{aG}&w_{aG}^T\\
                 w_{aG}&I\end{pmatrix}\succeq0,
 \qquad \sum_Gs_{aG}=1,                                  \tag{13b}
\]

because eliminating the fixed identity block gives exactly (1).  Hence its
reduced parameter \(L\) is also optimal among arbitrary coupled barriers,
not only exact for the displayed log-determinant restriction.  More
generally, any cone compiler whose affine reduction is (1) inherits (3).

The lower-bound half also extends beyond Lorentz geometry.  For
\(1<p<\infty\), the grouped perspective-\(p\) slice

\[
 \Omega_p=\left\{(u_{aG},w_{aG}):
 u_{aG}>\|w_{aG}\|_p^p,\quad
 \sum_Gu_{aG}=1\right\}                                  \tag{13c}
\]

contains the same \(L\)-cube after fixing \(u_{aG}=\sigma_{aG}\) and
varying one coordinate of every \(w_{aG}\).  Hence every arbitrary coupled
self-concordant barrier on \(\Omega_p\) has parameter at least \(L\).
For \(p=2\), (11) matches this lower bound.  For \(p\ne2\), the exact
upper parameter remains open, so (13c) gives only a lower bound.

## 3. Boundary stratification and the Dikin interpretation

The closure of (1) is stratified by the subsets of indices for which
\(q_{aG}=0\).  On the cube section (7), these strata are the ordinary cube
faces.  At a cube vertex all \(L\) constraints are active and their
conormals on \(\mathcal H\) are independent.

The lower bound can be read in Dikin geometry: the unit Dikin ellipsoid of
any self-concordant barrier must stay inside the domain.  Approaching the
cube vertex supplies \(L\) independent boundary directions.  The
Nesterov--Nemirovskii proof combines the corresponding one-dimensional
boundary-gradient inequalities with the barrier gradient bound and obtains
\(L\le\vartheta\).  A coupled Hessian can rotate the Dikin ellipsoid, but it
cannot remove any of those independent walls.

This explains why the cube section is stronger than merely counting
nonzero Lorentz boundary components.  The section certifies independent
affine boundary directions, not just multiple summands in a chosen
logarithmic barrier.

## 4. Why no-sharing factor counts alone do not prove (3) for every lift

The
[analytic no-sharing theorem](2026-09-04-analytic-no-sharing-full-product-balls.md)
gives many productive Lorentz factors and
a contact point at which their selected primal components are simultaneously
nonzero boundary rays.  That is enough to count the logarithmic vanishing
orders of the *standard product barrier*.  It does not by itself show that
the corresponding cone conormals are linearly independent after restriction
to an arbitrary lift affine space.  The stronger
[\(C^1\) top-class no-sharing
theorem](2026-09-04-c1-euler-no-sharing-product-balls.md)
removes analyticity from the minimum total factor count, but likewise does
not create independent restricted conormals.

There is a sharp elementary counterexample to any inference based only on
boundary-ray or productive-factor multiplicity.  Start with the direct ball
slice

\[
                  \Omega_1=\{(1,x)\in Q_{s+1}:\|x\|<1\}.
\]

For an integer \(r\ge2\), replace it by the diagonal slice of
\(Q_{s+1}^r\)

\[
 \Omega_r=\left\{
  ((1/r,x/r),\ldots,(1/r,x/r)):\|x\|<1
 \right\}.                                                \tag{14}
\]

This slice is affinely isomorphic to \(B_2^s\).  If
\(A(x)=(1,x)\) and \(B(y)=(1,-y)\), then

\[
 1-x^Ty=\sum_{j=1}^r\langle A(x)/r,B(y)\rangle.            \tag{15}
\]

All \(r\) selected primal components are nonzero Lorentz boundary rays at
contact, the selections are polynomial, and every copy is productive.
Nevertheless the pullback

\[
                         -\log(1-\|x\|^2)                  \tag{16}
\]

is an exact one-self-concordant barrier on \(\Omega_r\).  By contrast, the
restricted standard product barrier is

\[
                -r\log(1-\|x\|^2)+\text{constant}          \tag{17}
\]

and has exact parameter \(r\).  The \(r\) active conormals are identical on
the diagonal affine slice.

Thus neither simultaneous boundary rays nor productive factor count is a
lower bound for an arbitrary coupled slice barrier.  A valid transfer needs
additional geometry such as the explicit cube section (9), an independent-
conormal/local-corner hypothesis, or an equivalent intrinsic certificate.

The example does **not** refute either capped no-sharing frontier.  Its blocks
have dimension \(s+1\), and duplication only adds redundant factors.  For
the small-cap regime \(d<s+1\), whether every admissible globally bi-\(C^1\)
selected Lorentz lift has intrinsic slice parameter at least \(kh\) remains
open.
What is proved here is the exact arbitrary-barrier value for the grouped
lift that attains the structural frontier.

## 5. Consequences for the QIPM comparison

For the grouped formulation, replacing the separable barrier by an opaque
coupled barrier cannot reduce the parameter below \(kh\).  The separable
barrier also exposes the one-hub forest Newton graph and gives an
\(O(ks)\) exact field-operation solve.  A hypothetical coupled barrier has
no parameter advantage and may destroy that sparse Hessian structure.

This yields a clean formulation-level Pareto statement:

\[
 \begin{array}{c|c|c}
  \text{barrier on the grouped slice}&\text{best possible }\vartheta
      &\text{known exact Newton cost}\\ \hline
  \text{separable restricted Lorentz barrier}&kh&O(ks)\\
  \text{arbitrary coupled barrier}&\ge kh&\text{not automatically sparse}.
 \end{array}                                               \tag{18}
\]

It remains essential not to convert the first column into an iteration
lower bound.  The statement controls the best self-concordant-barrier
certificate on this formulation.  It does not exclude non-self-concordant
methods, long-step behavior better than a worst-case certificate, coherent
quantum outputs, or a different lift.

## Literature and novelty boundary

The cube lower bound is classical: Proposition 2.3.6 of Nesterov and
Nemirovskii, *Interior-Point Polynomial Algorithms in Convex Programming*
(SIAM, 1994), proves that a polytope with \(j\) independent facets active at
one boundary point has barrier parameter at least \(j\), and explicitly
lists the cube.  Lee and Yue, *Universal Barrier Is \(n\)-Self-Concordant*
(2021, arXiv:1809.03011), also cite the cube as a tight example for this
lower bound.  Affine restriction and addition are standard barrier
calculus.

A targeted search found work on optimal barriers for cubes, symmetric
cones, and nonlinear epigraph cones, but no source applying an embedded
cube to establish the exact parameter of the reduced grouped Lorentz ball
lift, or using it to close the arbitrary-coupled-barrier caveat in this
cap-dependent formulation.  The potentially new contribution is this
application and its combination with the exact \(C^1\) and analytic
no-sharing frontiers.  Priority remains subject to specialist review.

## Audit checklist

- [x] Every group is nonempty, so the direction \(e_{aG}\) in (7) exists.
- [x] The allocation constants are positive and sum to one separately for
  every source ball.
- [x] The affine intersection is exactly a full \(L\)-cube, not merely a
  subset of one.
- [x] Every boundary point of the cube section used by the lower-bound
  theorem is a boundary point of the full slice.
- [x] Restriction permits a fully coupled, non-logarithmically-homogeneous
  barrier.
- [x] The upper and lower parameters use the same normalization.
- [x] The diagonal-duplication example is an actual affine Lorentz-product
  lift and preserves the full slack identity.
- [x] Independent hostile audit.

## Independent hostile audit

The auditor checked the affine section directly and confirmed that it is
exactly an \(L\)-cube, that every section-boundary point used in the proof
lies on the boundary of the full slice, and that affine restriction
preserves both self-concordance and the same parameter.  It checked the
normalization against Nesterov--Nemirovskii Proposition 2.3.6 and found no
factor-of-two discrepancy.

The audit independently recomputed the derivatives and inverse-Hessian
identity for \(-\log(s-\|w\|^2)\), so the upper parameter is \(L\), and
verified that the allocation equalities do not invalidate the lower or
upper bound.  It also checked the diagonal duplication example: the slice
is affinely isomorphic to one ball, all duplicated factors are analytic,
nonzero at contact, and productive, yet their restricted conormals coincide.
The only requested correction was to retain the initialization/gap scale
\(\Delta\) in the generic short-step logarithm; this has been incorporated
in (6).
