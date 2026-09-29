# Every stationary rational quartic at the quintic tower is a quadratic form in its relations

Date: 2026-09-28. Status: complete uniform proof and exact checks;
[fresh adversarial review](tower-quartic-stationary-space-review.md) passed
without a substantive correction. Publication priority is unestablished.

The [complete quadratic-space theorem](tower-quadratic-vanishing-space.md)
gives five rational quadratic relations per gate and proves independence
of all their pairwise products. This note identifies their full span:
it is exactly the space of rational quartics whose value and gradient
vanish at the supplied tower point. Thus every rational quartic having
that point as a zero-valued unconstrained minimizer has a unique rational
symmetric Gram matrix on those relations. The
[least-field construction](exponential-least-sos-field.md) shows that
this matrix may be indefinite even when the quartic is strongly convex
and SOS over the reals.

## Statement

Use the point \(p_k=(a_i,a_i^2,a_i^3)_{i=1}^k\), with
\(a_i=2^{1/5^i}\), and the vector \(q\) of \(5k\) quadratic
relations from the companion note. Define
\[
 J_{d,k}=\{F\in\mathbb Q[X]_{\leq d}:
                     F(p_k)=0,\ \nabla F(p_k)=0\}.
\]

**Theorem.** For every \(k\geq1\),
\[
 J_{3,k}=\{0\},\qquad
 J_{4,k}=\{q^{\mathsf T}Aq:A\in\operatorname{Sym}_{5k}(\mathbb Q)\}.
                                                               \tag{1}
\]
The representing matrix \(A\) is unique. In particular,
\[
                  \dim J_{4,k}=\binom{5k+1}{2}.                 \tag{2}
\]
The definition includes all polynomials of degree at most four, without
assuming nonnegativity or convexity.

## 1. A local first-derivative interpolation calculation

Let \(L\) be a characteristic-zero field, let \(b\in L\setminus\{0\}\),
and suppose \(T^5-b\) is irreducible over \(L\). In
\(K=L(a)\), where \(a^5=b\), consider the linear map
\[
 \mathcal H:L[x,y,z]_{\leq3}\longrightarrow K^4,
 \quad P\longmapsto(P,P_x,P_y,P_z)(a,a^2,a^3).
                                                               \tag{3}
\]
Both spaces have dimension twenty over \(L\).

**Lemma.** The map \(\mathcal H\) is invertible.

**Proof.** Give \(x,y,z\) weights \(1,2,3\). Group the twenty
monomials by their weight modulo five. The five groups, each of size
four, are shown below. For the value row and each derivative row, keep
the coefficient of the corresponding power of \(a\), reducing powers
by \(a^5=b\). The resulting map is block diagonal up to row and
column permutations. Its five blocks, with rows in the order value,
\(x\)-derivative, \(y\)-derivative, \(z\)-derivative, are:
\[
\begin{array}{c|c|c}
\text{residue}&\text{ordered monomials}&\text{block}\\ \hline
0&(1,yz,x^2z,xy^2)&
 \begin{pmatrix}1&b&b&b\\0&0&2&1\\0&1&0&2\\0&1&1&0\end{pmatrix}\\[3pt]
1&(x,z^2,xyz,y^3)&
 \begin{pmatrix}1&b&b&b\\1&0&b&0\\0&0&1&3\\0&2&1&0\end{pmatrix}\\[3pt]
2&(y,x^2,xz^2,y^2z)&
 \begin{pmatrix}1&1&b&b\\0&2&b&0\\1&0&0&2b\\0&0&2&1\end{pmatrix}\\[3pt]
3&(z,xy,x^3,yz^2)&
 \begin{pmatrix}1&1&1&b\\0&1&3&0\\0&1&0&b\\1&0&0&2b\end{pmatrix}\\[3pt]
4&(xz,y^2,x^2y,z^3)&
 \begin{pmatrix}1&1&1&b\\1&0&2&0\\0&2&1&0\\1&0&0&3b\end{pmatrix}.
\end{array}                                                     \tag{4}
\]
Their determinants are, respectively,
\[
                         5,\quad5b,\quad-5b,\quad-5b,\quad-5b.
\]
All are nonzero. Hence the map is invertible. \(\square\)

Only the independence of \(1,a,a^2,a^3,a^4\) and \(b\ne0\) are
used. In the tower induction, take \(L=\mathbb Q(a_{k-1})\),
\(b=a_{k-1}\), and \(a=a_k\). The degree-five extension follows
from the degrees \([\mathbb Q(a_j):\mathbb Q]=5^j\). For the first
gate use \(L=\mathbb Q\) and \(b=2\).

## 2. No nonzero stationary rational cubic

First, there is no nonzero rational affine polynomial vanishing at
\(p_k\), by the retained-monomial proof in the companion note.
Consequently,
\[
                            J_{2,k}=\{0\}.                       \tag{5}
\]
Indeed every partial derivative of a member of \(J_{2,k}\) is a
rational affine polynomial vanishing at \(p_k\); all derivatives
are therefore identically zero, and the remaining constant is zero.

We prove \(J_{3,k}=0\) by induction. The first gate follows directly
from the local lemma. For the induction step write \(U\) for the
earlier variables and \(V=(x_k,y_k,z_k)\) for the last triple.
If \(F\in J_{3,k}\), then \(F(p_{k-1},V)\) is a polynomial of
degree at most three over \(L=\mathbb Q(a_{k-1})\), with zero value
and zero \(V\)-gradient at the last-gate point. The local lemma
makes this entire polynomial zero. Thus each coefficient of \(F\),
viewed as a polynomial in \(V\), vanishes at \(p_{k-1}\).

Coefficients of \(V\)-monomials of degree at least two have degree
at most one in \(U\); they are zero by affine independence. Therefore
\[
 F(U,V)=h_0(U)+x_k h_1(U)+y_k h_2(U)+z_k h_3(U),                 \tag{6}
\]
where all \(h_j(p_{k-1})=0\), \(\deg h_0\le3\), and
\(\deg h_j\le2\) for \(j>0\). Taking a partial derivative in
any earlier variable and evaluating at \(p_k\) gives a linear
combination of \(1,a_k,a_k^2,a_k^3\) over \(L\) equal to zero.
Their independence shows that every \(h_j\) has zero gradient at
\(p_{k-1}\). Equation (5) kills \(h_1,h_2,h_3\), and the
induction hypothesis kills \(h_0\).

## 3. Every stationary quartic is a sum of relation products

All products of two relations belong to \(J_{4,k}\). We prove the
reverse inclusion by induction; uniqueness then follows from the
companion product-independence theorem.

Let \(F\in J_{4,k}\). Its part of degree four in the last triple
\(V\) has constant rational coefficients, since the total degree is
at most four. The fifteen products of the last gate's leading
quadratics
\[
                   x_k^2,\ x_ky_k,\ y_k^2-x_kz_k,\ y_kz_k,\ z_k^2
\]
span every quartic in that triple. Subtract a rational linear
combination of products of two last-gate relations to remove this
part. The remainder remains in \(J_{4,k}\) and has degree at most
three in \(V\).

By the local lemma, specializing \(U=p_{k-1}\) makes this remainder
identically zero as a polynomial in \(V\). Its degree-three
coefficients have degree at most one in \(U\), so affine
independence makes them zero. We are left with degree at most two
in \(V\), and every coefficient vanishes at \(p_{k-1}\).
Write \(c_{y^2}(U)\) and \(c_{xz}(U)\) for the coefficients of
\(y_k^2\) and \(x_kz_k\). All coefficients of quadratic
\(V\)-monomials belong to the earlier rational space \(I_2\).

We claim
\[
                         c_{y^2}+c_{xz}=0.                       \tag{7}
\]
Differentiate the remainder in an earlier variable and specialize
\(U=p_{k-1}\). The resulting last-gate quadratic vanishes at
\((a_k,a_k^2,a_k^3)\). For any such quadratic over \(L\), the
sum of its \(y_k^2\) and \(x_kz_k\) coefficients is zero: these
are the only degree-at-most-two monomials evaluating to \(a_k^4\),
whereas \(y_kz_k=b\) and \(z_k^2=bx_k\) under evaluation.
It follows that the gradient of \(c_{y^2}+c_{xz}\) vanishes at
\(p_{k-1}\). Its value also vanishes there, so (5) proves (7).

Equation (7) lets us express the entire degree-two part in \(V\)
as \(\sum_{j=1}^5 L_j(V)P_j(U)\), where \(L_j\) are the five
displayed leading quadratics and every \(P_j\) belongs to the
earlier \(I_2\). Subtract \(\sum_j q_{k,j}(U,V)P_j(U)\).
These are products of last-gate and earlier rational quadratic
relations; they have total degree at most four and zero value and
gradient at \(p_k\). The new remainder has the form (6), now with
\(\deg h_0\le4\) and \(\deg h_j\le3\) for \(j>0\).

The same coefficient and gradient argument as in Section 2 makes
every \(h_j\) stationary at the earlier point. The already proved
vanishing of \(J_{3,k-1}\) kills \(h_1,h_2,h_3\). By induction,
\(h_0\) is a combination of products of earlier relations. The
first-gate case simply subtracts the fifteen local products and
applies the local cubic lemma. This completes the proof of (1).

## 4. Consequences and limits

Every rational quartic with value zero and gradient zero at the
supplied tower point has a unique rational symmetric matrix \(A\)
of order \(5k\). It is a rational polynomial SOS precisely when
\(A\succeq0\), by the companion recognition theorem. In this
stationary subclass, membership in the product span is automatic.
All this computation is polynomial in \(k\) and the explicit
rational input length.

For an arbitrary rational quartic merely satisfying \(F(p_k)=0\),
the span-membership test remains necessary. For a differentiable
polynomial with an unconstrained minimum at \(p_k\), stationarity
does hold, so (1) applies. Constraints in an MINLP do not in general
imply zero ambient gradient; the theorem must not be applied to
arbitrary constrained optima on that basis.

The theorem also shows that a rational stationary quartic at this
point is determined by its homogeneous degree-four part: the difference
of two such polynomials with the same leading part lies in \(J_{3,k}\).
It does not imply that every homogeneous quartic has such a completion.

First-derivative interpolation, polynomial vanishing ideals, and Gram
representations are classical tools. The contribution here is the
explicit uniform stationary-space identity for the supplied tower.
The [companion literature comparison](tower-quadratic-vanishing-space.md)
covers the earlier binomial and rational SOS mechanisms examined.
No search establishes that this particular identity is new, and no
general interpolation or ideal-membership theorem is claimed.

## 5. Targeted exact checks

The author ran:

```text
python3 research-20260927/check_tower_quartic_stationary_space.py
```

It verifies the five symbolic determinants in (4) and computes the
complete rational value-and-gradient evaluation ranks on all monomials
of total degree at most three and at most four for \(k=1,\ldots,5\).
The cubic kernels are zero, and the quartic kernel dimensions are
\(15,55,120,210,325\). These finite checks support the displayed
uniform proof; they do not replace its induction or establish novelty.
No numerical roots, Lean proof, project-wide verification, or CI
inspection is used.
