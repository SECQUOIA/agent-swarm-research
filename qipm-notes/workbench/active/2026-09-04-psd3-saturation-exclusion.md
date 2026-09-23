# The apparent \(\mathbb S_+^3\) saturation exception is impossible

Status: Proved; independently hostile-audited  
Started: 2026-09-04  
Paper status: Not incorporated  
Confidence: High

## Result

Let \(S^2\) carry the full three-ball slack

\[
                         s(x,y)=1-x\mathbin\cdot y.
\]

There is no globally labelled bi-\(C^1\) factorization

\[
  1-x\mathbin\cdot y
    =\operatorname {tr}(X(x)Y(y))
       +\sum_{j=1}^q a_j(x)b_j(y),                         \tag{1}
\]

where \(X,Y:S^2\to\mathbb S_+^3\), the scalar factors are
nonnegative, and the PSD block saturates the two tangent channels at every
diagonal contact.  Equivalently, the unique positive-capacity block has
complementary ranks \(1,2\), and its rank-one support map

\[
                           S^2\longrightarrow\mathbb {RP}^2             \tag{2}
\]

is a submersion (hence the universal double cover).  The number \(q\) of
ray factors may be any finite number.

Consequently the \(n=2\), \(H_3(\mathbb R)_+=\mathbb S_+^3\) alternative in
the saturated symmetric-cone support-orbit theorem is not realizable by the
full three-ball slack.  Combined with the support-orbit classification, a
globally bi-\(C^1\) saturated factorization of a Euclidean-ball full slack
through a finite product of irreducible symmetric cones has a unique
positive-capacity rank-two spin-factor block in every dimension, including
\(n=2\).  This last exclusion uses the quadratic ball boundary and is not
claimed for an arbitrary smooth strictly convex body.

The proof has two parts.  Finitely many nonnegative ray terms force the
rank-two PSD sheet to be one affine pencil globally.  Positivity of that
pencil on the whole sphere would give a real symmetric \(3\)-by-\(3\)
linear determinantal representation of \(t(t^2-\lVert x\rVert^2)\), and
an elementary normal-form calculation rules this out.

## 1. Deleting all ray terms on finitely many open cells

Every diagonal summand in (1) is nonnegative and their sum is zero.  Thus

\[
  \operatorname {tr}(X(x)Y(x))=0,
  \qquad a_j(x)b_j(x)=0                                   \tag{3}
\]

for every \(x\) and \(j\).  For any nonnegative continuous function \(f\),

\[
                 \{f>0\}\ \cup\ \operatorname {int}\{f=0\}             \tag{4}
\]

is open and dense.  Intersect (4) for the finitely many functions
\(a_j,b_j\), and partition the resulting open dense set \(\Omega\) by
their finitely many positive/zero-interior status patterns.  Denote the
nonempty open pattern sets by \(\Omega_\sigma\).  On each such set and for
each \(j\), (3) says that at least one of \(a_j,b_j\) vanishes identically.
Hence

\[
       \sum_j a_j(x)b_j(y)=0
       \quad(x,y\in\Omega_\sigma),                         \tag{5}
\]

including when \(x,y\) lie in different connected components of the same
pattern set.

Suppose first that \(Y\) has rank one and \(X\) rank two.  The support map
of \(Y\) is a submersion to \(\mathbb {RP}^2\), so it maps every nonempty
open subset to an open subset.  Therefore

\[
             \operatorname {span}\{Y(y):y\in\Omega_\sigma\}
                       =\mathbb S^3.                       \tag{6}
\]

Indeed, a symmetric matrix orthogonal to the left side would have its
quadratic form vanish on a projective open set, and hence vanish
identically.  Choose six \(y_\ell\in\Omega_\sigma\) for which
\(Y(y_\ell)\) form a basis.  Equations (1) and (5) determine \(X(x)\), for
all \(x\in\Omega_\sigma\), from

\[
             \operatorname {tr}(X(x)Y(y_\ell))=1-x\cdot y_\ell .        \tag{7}
\]

Thus there is an ambient affine matrix pencil

\[
                         L_\sigma(x)=C_{\sigma0}+\sum_{i=1}^3x_iC_{\sigma i}
                                                                    \tag{8}
\]

such that \(X=L_\sigma\) on \(\Omega_\sigma\).  If \(X\) is the rank-one
sheet, the identical argument with the variables exchanged makes the
rank-two sheet \(Y\) affine on every pattern set.

## 2. A finite \(C^1\) selection of affine sphere maps is one pencil

We use the following elementary gluing lemma.

**Lemma 1 (finite affine selection).**  Let \(F:S^2\to W\) be \(C^1\),
where \(W\) is finite dimensional.  Suppose a dense open subset is the
union of finitely many open sets \(U_i\), and on \(U_i\), \(F\) is the
restriction of an ambient affine map \(L_i:\mathbb R^3\to W\).  Then all
nonempty pieces use the same affine map, and \(F=L\) on all of \(S^2\).

*Proof.*  Combine pieces carrying identical pencils and put
\(E_i=\overline {U_i}\).  The finite union of the \(E_i\) is \(S^2\).  On
\(E_i\), continuity of the value and derivative gives

\[
                             j^1F=j^1(L_i|_{S^2}).                         \tag{9}
\]

If two distinct ambient affine maps \(L_i,L_j\) have the same value and
tangential derivative at \(z\in S^2\), their difference has the form

\[
                         (L_i-L_j)(x)=M(z\cdot x-1)                        \tag{10}
\]

for a nonzero \(M\in W\).  Hence their restricted first jets can agree at
at most that one point.  All pairwise intersections \(E_i\cap E_j\) of
distinct pieces therefore lie in a finite set \(Z\).  On the connected
surface \(S^2\setminus Z\), the sets \(E_i\setminus Z\) form a disjoint
clopen partition.  Only one can be nonempty.  The closure of a nonempty
open \(U_i\) cannot lie in the finite set \(Z\), so there was only one
distinct pencil.  Density and continuity finish the proof. \(\square\)

Applying Lemma 1 to (8) shows that the rank-two sheet, call it \(X\), is
one affine pencil on the whole sphere:

\[
                  X(x)=C_0+\sum_{i=1}^3x_iC_i\succeq0,
                  \qquad \operatorname {rank}X(x)=2.       \tag{11}
\]

This globalization is the step missed by a merely local analysis of the
ray-free patch.

## 3. Homogenization leaves the genuine \(q\ell\) case

Homogenize (11):

\[
                   \mathcal L(t,x)=tC_0+\sum_{i=1}^3x_iC_i.               \tag{12}
\]

The cubic \(p=\det\mathcal L\) vanishes on \(t=1,\lVert x\rVert=1\).
The real sphere is Zariski dense in the irreducible quadric
\(Q(t,x)=t^2-\lVert x\rVert^2\), so

\[
                         \det\mathcal L(t,x)=Q(t,x)\ell(t,x)              \tag{13}
\]

for a real linear form \(\ell\).  This is the essential correction to the
invalid inference that the entire four-dimensional pencil is singular.

The kernel lines in (11) vary over all of \(\mathbb {RP}^2\) by (2).  Since
\(C_0\) is the spherical average of \(X(x)\), it is positive definite: a
vector in its kernel would be in the kernel of every positive semidefinite
\(X(x)\).  Moreover, at every upper-boundary point,

\[
 \partial_t\det\mathcal L(1,x)
    =\operatorname {tr}(\operatorname {adj}(X(x))C_0)>0
    =2\ell(1,x).                                           \tag{14}
\]

Thus \(\ell(t,x)=at+b\cdot x\) satisfies \(a>|b|\): it is future timelike.
A Lorentz change of homogeneous variables sends \(\ell\) to a positive
multiple of \(t\), while preserving \(Q\) and its upper cone.  The pencil
maps that whole cone into \(\mathbb S_+^3\), because the cone is generated
by its boundary rays and (11) is PSD there.  Its value at \((1,0)\) is
positive definite as well: after the Lorentz reparametrization the boundary
kernel map is still onto \(\mathbb {RP}^2\), so the spherical average of
the boundary pencil has no common kernel.  That average is its value at
\((1,0)\).  After a congruence and scalar normalization, (13) would become

\[
              M(t,x)=tI+A(x),\qquad
              \det(tI+A(x))=t(t^2-\lVert x\rVert^2).        \tag{15}
\]

It remains to show that no such real symmetric pencil exists.

For contrast, the local \(q\ell\) case is real and cannot be discarded:

\[
 \begin{pmatrix}
 t+x_3&x_1&x_2\\ x_1&t-x_3&0\\ x_2&0&t-x_3
 \end{pmatrix},
 \qquad
 \det=(t-x_3)(t^2-\lVert x\rVert^2).                       \tag{16}
\]

At \(t=1\) it is PSD of rank two away from one pole and its kernel map is
the stereographic chart into \(\mathbb {RP}^2\).  The finite-selection
argument, not local determinantal algebra, is what forces the timelike
linear factor in (13).

## 4. No symmetric \(3\)-by-\(3\) pencil represents \(tQ\)

**Lemma 2.**  There is no linear map
\(A:\mathbb R^3\to\mathbb S^3\) satisfying (15).

*Proof.*  Coefficient comparison in (15) says that every nonzero \(A(x)\)
has eigenvalues \(0,\lVert x\rVert,-\lVert x\rVert\).  In particular

\[
 \operatorname {tr}A_i=0,\quad
 \operatorname {tr}(A_iA_j)=2\delta_{ij},\quad
 \det A(x)=0,                                               \tag{17}
\]

where \(A_i=A(e_i)\).  Orthogonally diagonalize
\(A_1=D=\operatorname {diag}(1,-1,0)\).

Write a symmetric matrix \(B\), satisfying (17) and orthogonal to \(D\),
as

\[
 B=\begin{pmatrix}a&d&e\\d&a&f\\e&f&-2a\end{pmatrix}.
\]

The identity \(\det(D+sB)=0\) first forces \(a=0\), and then gives

\[
                  e^2=f^2,\qquad def=0,qquad d^2+e^2+f^2=1.              \tag{18}
\]

Thus its off-diagonal triple \((d,e,f)\) has one of the two forms

\[
                 (\pm1,0,0),qquad
                 (0,\pm2^{-1/2},\pm2^{-1/2}).              \tag{19}
\]

Apply this classification to both \(A_2\) and \(A_3\).  If one has the
first form, trace orthogonality forces the other to have the second; then
the zero-diagonal determinant
\(2(\text{off}_{12})(\text{off}_{13})(\text{off}_{23})\) of a combination
of \(A_2,A_3\) has a nonzero \(x_2x_3^2\) or \(x_2^2x_3\) coefficient.  If
both have the second form, orthogonality forces their two sign vectors to
differ in exactly one coordinate, up to overall signs.  The determinant of
\(x_1D+x_2A_2+x_3A_3\) then has a nonzero \(x_1x_2x_3\) coefficient.
Every case contradicts \(\det A(x)\equiv0\). \(\square\)

Lemmas 1 and 2 contradict (11)--(15), proving the result.

## Independent hostile audit

The auditor checked the finite open status-cell deletion, including ray
terms evaluated at two different points of the same possibly disconnected
cell.  It verified that the rank-one support image of every nonempty open
cell spans all of \(\mathbb S^3\), so the opposite rank-two sheet is an
ambient affine pencil there.  It then checked the first-jet gluing lemma:
two distinct affine sphere maps can have the same restricted first jet at
only one point, and deleting the resulting finite collision set leaves a
connected sphere.

The determinant audit retained the genuine local \(Q\ell\) possibility.
It verified instead that global positivity and the surjective kernel map
make the linear factor future timelike; after a Lorentz reparametrization,
the new central matrix is positive definite because it is the average of
boundary matrices with no common kernel.  Finally, direct coefficient and
case checks confirmed Lemma 2, with the sign-pattern wording corrected as
above.  No mathematical gap remained after these clarifications.

## Assumptions and scope

* Finiteness of the ray product is essential to the finite-selection
  argument.  The proof makes no claim about infinite products or integral
  factorizations.
* The PSD maps need \(C^1\) regularity.  Continuity suffices for deleting
  ray terms, but the first-jet gluing in Lemma 1 uses \(C^1\).  The scalar
  ray maps themselves only need to be continuous and nonnegative.
* The proof uses saturation only through the fixed complementary ranks and
  the rank-one support submersion (2).  Those conclusions follow from the
  general bi-\(C^1\) saturated support theorem.
* Ray blocks have zero tangent-channel capacity, but they were not assumed
  useless a priori; Section 1 is what removes them on a dense finite family
  of open cells.
