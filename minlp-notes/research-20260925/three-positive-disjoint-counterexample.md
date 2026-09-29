# Three positive square coefficients can defeat disjoint affine-SOS certificates

## Status and scope

This note gives an exact counterexample to completeness of a specific certificate cone. It does **not** claim that three-variable box quadratic optimization lacks an exact semidefinite formulation. Such a formulation follows from the classical six-tetrahedron representation of Anstreicher and Burer.

The counterexample was found by optimizing over the exact cone of nonnegative quadratics, then simplifying an exposed numerical example into a rational family. Independent calculations confirmed the edge checks and the exclusion proof. Completed [proof and source review](three-positive-counterexample-review.md) verifies the strict gap and its match to the cited relaxation. The [family review](three-positive-family-lmi-review.md) checks the stronger polynomial identity and compact SDP, while the [priority review](three-positive-family-priority-review.md) records what remains unestablished about originality.

## The cone

For disjoint subsets \(A,B\subseteq\{1,2,3\}\), write

\[
w_{A,B}(x)=\prod_{i\in A}x_i\prod_{j\in B}(1-x_j).
\]

Let \(\mathcal D_3\) consist of polynomial identities

\[
p(x)=\sum_{A\cap B=\varnothing}w_{A,B}(x)
       \sum_r L_{A,B,r}(x)^2,
\]

where every \(L_{A,B,r}\) is affine and depends only on coordinates outside \(A\cup B\). We impose no total-degree cutoff. In three variables the largest possible degree of a summand is four. Every summand is nonnegative on the cube.

This is the full disjoint-support, affine-SOS cone for three plus loops. It includes every degree-truncated version with these same support restrictions. Thus exclusion from this full cone also excludes the truncated versions.

## Exact counterexample

**Theorem.** The polynomial

\[
\boxed{p(x,y,z)=x^2+y^2+9z^2+6xy-12xz-12yz-x-y+9z+\tfrac14}
\]

is nonnegative on \([0,1]^3\), has three strictly positive square coefficients, and does not belong to \(\mathcal D_3\).

### Nonnegativity

There is a short certificate in the full degree-four preordering:

\[
\begin{aligned}
p={}&(xy+x+y-3z-\tfrac12)^2
  +6z(1-x)(1-y)\\
 &+3xy(1-x)+2xy(1-y)+x^2y(1-y).
\end{aligned}
\]

Every term is nonnegative on the cube. This proves nonnegativity directly and identifies a concrete stronger certificate system that captures the example. It uses a square of a quadratic polynomial and the factor \(y(1-y)\), which are outside the affine-multiplier and disjoint-factor restrictions defining \(\mathcal D_3\).

### Zero set and independent edge check

The quadratic coefficient matrix is

\[
Q=\begin{pmatrix}1&3&-6\\3&1&-6\\-6&-6&9\end{pmatrix}.
\]

Its two-by-two principal determinants are \(-8,-27,-27\). Therefore no principal submatrix of size at least two is positive semidefinite. A minimizer in the relative interior of a face with at least two free coordinates would require the corresponding principal submatrix to be positive semidefinite, by the second-order necessary condition along that face. Since a global minimizer exists, some global minimizer lies on an edge or vertex.

The following table exhausts the twelve edges; rows involving \(x\) also cover the distinct edge obtained by swapping \(x\) and \(y\).

| Free coordinate and fixed coordinates | Edge polynomial | Minimum on the edge |
|---|---|---:|
| \(x;\ y=0,z=0\), and its swap | \((x-\tfrac12)^2\) | \(0\) |
| \(x;\ y=1,z=0\), and its swap | \(x^2+5x+\tfrac14\) | \(\tfrac14\) |
| \(x;\ y=0,z=1\), and its swap | \(x^2-13x+\tfrac{73}4\) | \(\tfrac{25}4\) |
| \(x;\ y=1,z=1\), and its swap | \(x^2-7x+\tfrac{25}4\) | \(\tfrac14\) |
| \(z;\ x=y=0\) | \(9z^2+9z+\tfrac14\) | \(\tfrac14\) |
| \(z;\ (x,y)=(1,0)\) or \((0,1)\) | \(9(z-\tfrac16)^2\) | \(0\) |
| \(z;\ x=y=1\) | \(9(z-\tfrac56)^2\) | \(0\) |

Every edge is nonnegative. This proves nonnegativity on the entire cube. The zero set is exactly

\[
a=(\tfrac12,0,0),\quad b=(0,\tfrac12,0),\quad
c=(1,0,\tfrac16),\quad d=(0,1,\tfrac16),\quad
e=(1,1,\tfrac56).
\]

The argument excluding higher-dimensional faces also shows that there are no other zeros.

### Exclusion from the certificate cone

Suppose \(p\in\mathcal D_3\). At the origin, \(p(0,0,0)=1/4\). Consequently, at least one individual summand \(w_{A,B}L^2\) is strictly positive there. Such a summand has \(A=\varnothing\), and if

\[
L(x,y,z)=\alpha+\beta x+\gamma y+\delta z,
\]

then \(\alpha\ne0\). Because every summand is nonnegative, this summand vanishes at each zero of \(p\).

Its weight is strictly positive at \(a\) and \(b\), regardless of \(B\). Hence

\[
\beta=-2\alpha,\qquad \gamma=-2\alpha.
\]

In particular, \(x\) and \(y\) occur in \(L\), so disjoint support forbids either coordinate from belonging to \(B\). Therefore \(B\subseteq\{z\}\). The weight is consequently strictly positive at both \(c\) and \(e\). Vanishing at \(c\) gives \(\delta=6\alpha\), while vanishing at \(e\) then gives

\[
0=\alpha-2\alpha-2\alpha+\tfrac56(6\alpha)=2\alpha,
\]

contradicting \(\alpha\ne0\). Thus \(p\notin\mathcal D_3\). This proof does not rely on floating-point optimization, duality, or closure of the cone.

## Structural interpretation

For any such disjoint certificate, an interior zero on a cube edge constrains every summand that is positive at one endpoint. The edge coordinate must occur among the multiplier's free coordinates: if it were fixed by the weight, the affine factor would remain nonzero along the edge and the weight would be positive at the interior zero. Once that coordinate is free, the affine factor has an interior root and is nonzero at the opposite endpoint. Its weight is unchanged along the edge, so the summand is positive there too.

Thus positivity propagates along a connected graph of edges containing interior zeros, forcing every direction used by that graph to remain free. Here the zero edges through \(a,b,c,d\) form a path using all three directions. A summand positive at the origin must therefore be an unweighted global affine square. But the five zeros affinely span \(\mathbb R^3\): the determinant of the augmented rows \((1,a),(1,b),(1,c),(1,e)\) is \(-1/12\). No nonzero affine polynomial vanishes at all these points. The direct proof above is the shortest specialization of this argument.

## An exact rational separation certificate

The following linear functional \(\Lambda\) is defined on the twenty monomials that can occur in the cone. All tabulated entries have denominator \(10000\).

| Exponent | Numerator | Exponent | Numerator |
|---|---:|---|---:|
| 000 | 10000 | 100 | 4041 |
| 001 | 1377 | 101 | 1025 |
| 002 | 681 | 102 | 629 |
| 010 | 4041 | 110 | 771 |
| 011 | 1025 | 111 | 674 |
| 012 | 629 | 112 | 590 |
| 020 | 3392 | 120 | 770 |
| 021 | 1222 | 121 | 598 |
| 200 | 3392 | 210 | 770 |
| 201 | 1222 | 211 | 598 |

For each disjoint pair \((A,B)\), let \(b\) list the constant monomial and the coordinates outside \(A\cup B\). The matrix

\[
M_{A,B}=\Lambda\bigl(w_{A,B}bb^T\bigr)
\]

is positive definite. There are eight blocks of size one, twelve of size two, six of size three, and one of size four. Exact computation gives these minimum leading principal determinants, grouped by determinant order:

\[
\frac1{10000},\qquad
\frac{307}{50000000},\qquad
\frac{154171}{40000000000},\qquad
\frac{45063248771}{10^{16}}.
\]

Sylvester's criterion therefore proves \(\Lambda(w_{A,B}L^2)\ge0\) for every permitted generator. On the other hand,

\[
\Lambda(1)=1,\qquad \Lambda(p)=-\frac1{40}.
\]

This independently proves exclusion and gives an explicit gap. In the certificate optimization \(\sup\{\gamma:p-\gamma\in\mathcal D_3\}\), every feasible \(\gamma\) satisfies \(\gamma\le-1/40\), although \(\min_{[0,1]^3}p=0\).

The same rational moment point also satisfies the SOC strengthening in equations (15) and (16) of Anstreicher and Puges, under every permutation and all eight coordinate switches. Writing \(t=\Lambda(xyz)\), the unswitched inequalities have the forms

\[
t^2\le Y_{ii}Y_{jk},\qquad
(Y_{ij}+t)^2\le Y_{ii}(Y_{jj}+3Y_{jk}),
\]

for distinct indices. The exact checker verifies all 24 switched instances of (15), with minimum slack \(2831/4000000\), and all 48 switched instances of (16), with minimum slack \(124813/12500000\). The accompanying trilinear RLT inequalities are the eight scalar blocks already checked, and the diagonal upper bounds hold as well. Consequently, \(p\ge0\) is not implied by their PSD, RLT, triangle, ETRI1/2/3 and stated SOC strengthening. This is a comparison with those particular systems; the known exact tetrahedral formulation already implies the cut.

Moreover, \(p+1/80\) is at least \(1/80\) everywhere on the cube but has negative \(\Lambda\)-value. Thus failure is not limited to polynomials with zeros. The exact moment checks were independently repeated using SymPy, separately from the standard-library rational checker.

The durable verification command for these moment data is

```sh
python research-20260925/checks/three_positive_gap_certificate.py
```

## A family that explains the example

Let \(h,d_1,d_2,d_3,k>0\), put \(D=d_1+d_2-h\), and consider

\[
p_{h,d,k}=(h-d_1x-d_2y+d_3z)^2
 +2d_3kz(1-x-y)+k(2D+k)xy.
\]

If \(0<h<\min(d_1,d_2)\) and \(D+k<d_3\), this polynomial has the five interior edge contacts

\[
(h/d_1,0,0),\quad (0,h/d_2,0),\quad
(1,0,(d_1-h)/d_3),\quad (0,1,(d_2-h)/d_3),\quad
(1,1,(D+k)/d_3).
\]

**Proposition.** Every member of this family under the displayed strict inequalities is nonnegative on the cube and lies outside \(\mathcal D_3\).

In fact, putting \(L=h-d_1x-d_2y+d_3z\), one has the identity

\[
\begin{aligned}
p_{h,d,k}={}&(L-kxy)^2+2d_3kz(1-x)(1-y)\\
 &+k(2d_1+k)xy(1-x)+2kd_2xy(1-y)
   +k^2x^2y(1-y).
\end{aligned}
\]

It proves nonnegativity whenever \(d_1,d_2,d_3,k\ge0\), for arbitrary real \(h\). The stricter restrictions ensure that the five contacts used in the exclusion proof lie in edge interiors. This larger parameter domain permits all these valid quadratic inequalities to be imposed by a compact semidefinite extension; that construction is developed separately in [the family SDP note](three-positive-family-sdp.md).

For completeness, the edge geometry can also be verified directly. The quadratic coefficient matrix has diagonal \((d_1^2,d_2^2,d_3^2)\) and off-diagonal entries

\[
Q_{12}=d_1d_2+kD+k^2/2,\quad
Q_{13}=-d_3(d_1+k),\quad
Q_{23}=-d_3(d_2+k).
\]

All two-by-two principal determinants are strictly negative. Again it suffices to check the edges. Put \(A=2d_3k\), \(B=k(2D+k)\), and \(t=d_3-D-k>0\). On the bottom face, the edges with \(x=0\) or \(y=0\) are squares, and those with \(x=1\) or \(y=1\) are a square plus \(By\) or \(Bx\). On the top face, the edges with \(x=0\) or \(y=0\) are a square plus \(A(1-y)\) or \(A(1-x)\). For the top edge with \(x=1\), put \(r=1-y\); the restriction is

\[
t^2+\bigl[2d_2(k+t)+k(k+2t)\bigr]r+d_2^2r^2\ge0.
\]

The other top edge follows by swapping the first two coordinates and parameters. The vertical edge with \(x=y=0\) is \((h+d_3z)^2+Az\); the other three vertical edges are the squares

\[
\bigl(d_3z-(d_1-h)\bigr)^2,\quad
\bigl(d_3z-(d_2-h)\bigr)^2,\quad
\bigl(d_3z-(D+k)\bigr)^2.
\]

All twelve edges are nonnegative.

For exclusion, repeat the direct proof with a summand positive at the origin and affine constant \(\alpha\ne0\). The first two contacts force its \(x\)- and \(y\)-coefficients to be \(-\alpha d_1/h\) and \(-\alpha d_2/h\), so these coordinates are free. The third contact forces its \(z\)-coefficient to be \(\alpha d_3/h\). Its affine factor consequently equals \(\alpha k/h\ne0\) at the fifth contact, where its weight is positive. This contradiction proves exclusion.

The displayed rational counterexample is the choice \((h,d_1,d_2,d_3,k)=(1/2,1,1,3,1)\). The family shows that the contact obstruction persists across a range of coefficient ratios; it does not by itself quantify each member's relaxation gap.

## Every member of the family generates an exposed extreme ray

Let \(\mathcal P_3\) denote the cone of quadratic polynomials nonnegative on the cube. Under the family's strict parameter assumptions, define \(F(q)\) to be the sum of the values of \(q\) at its five displayed contacts. Then

\[
\{q\in\mathcal P_3:F(q)=0\}=\{\lambda p_{h,d,k}:\lambda\ge0\}.
\]

Thus each member generates an exposed extreme ray of the full nonnegative-quadratic cone. In particular, the missing valid inequality cannot be obtained by adding nonproportional nonnegative quadratic inequalities.

Here is a direct proof, including the possible zero polynomial. Suppose \(q\in\mathcal P_3\) vanishes at the five contacts, and write its quadratic coefficients as \(a_x,a_y,a_z,b_{xy},b_{xz},b_{yz}\), with the convention that the mixed terms are \(2b_{ij}x_ix_j\). Write its linear coefficients as \(\ell_x,\ell_y,\ell_z\), and its constant as \(c_0\).

The restriction to the bottom \(x\)-edge has an interior zero at \(h/d_1\), so it equals \(a_x(x-h/d_1)^2\), with \(a_x\ge0\). The bottom \(y\)-edge similarly equals \(a_y(y-h/d_2)^2\). Comparing the common constant gives

\[
\lambda:=a_x/d_1^2=a_y/d_2^2\ge0,
\quad c_0=\lambda h^2,
\quad \ell_x=-2\lambda hd_1,
\quad \ell_y=-2\lambda hd_2.
\]

Compare the value of \(q(1,0,0)\) from the bottom \(x\)-edge with the vertical edge through the third contact. Their values are \(\lambda(d_1-h)^2\) and \(a_z(d_1-h)^2/d_3^2\), respectively. Since \(d_1-h>0\), it follows that \(a_z=\lambda d_3^2\).

The three vertical edge contacts make the derivative in \(z\) vanish. Consequently,

\[
\begin{aligned}
\ell_z+2b_{xz}&=-2\lambda d_3(d_1-h),\\
\ell_z+2b_{yz}&=-2\lambda d_3(d_2-h),\\
\ell_z+2b_{xz}+2b_{yz}&=-2\lambda d_3(D+k).
\end{aligned}
\]

These equations give

\[
\ell_z=2\lambda d_3(h+k),\quad
b_{xz}=-\lambda d_3(d_1+k),\quad
b_{yz}=-\lambda d_3(d_2+k).
\]

Finally, the vertical edge at \(x=y=1\) gives \(q(1,1,0)=\lambda(D+k)^2\), which determines

\[
b_{xy}=\lambda(d_1d_2+kD+k^2/2).
\]

Every coefficient of \(q\) now equals \(\lambda\) times the corresponding coefficient of \(p_{h,d,k}\). Since each evaluation is nonnegative on \(\mathcal P_3\), their sum exposes precisely this ray.

## Literature comparison and limitations

- [Khajavirad, *Tight semidefinite programming relaxations for sparse box-constrained quadratic programs*, arXiv:2601.18545v2](https://arxiv.org/abs/2601.18545v2), Section 3, equation (17), gives exactly the 27 matrices checked here when all three vertices have positive loops. The independent source review establishes this match, so the example answers that section's three-variable exactness question negatively. Section 6 describes the corresponding disjoint affine-SOS multipliers, but its degree conventions are inconsistent: a fully conditioned one-variable-square block can have degree four. The comparison uses the explicit matrices, not that degree label.
- [Anstreicher and Puges, *Extended Triangle Inequalities for Nonconvex Box-Constrained Quadratic Programming*, arXiv:2501.09150](https://arxiv.org/abs/2501.09150), equation (3), explicitly recalls the exact six-tetrahedron DNN representation of the full three-variable quadratic hull, attributed there to Anstreicher and Burer. The present result separates the disjoint certificate cone from that exact hull; it does not establish a new general SDP representation or an impossibility of one.
- [Hildebrand, *Minimal zeros of copositive matrices*, arXiv:1401.0134](https://arxiv.org/abs/1401.0134), Lemma 4.3 and Theorem 4.5, provide the established relation between affine-square subtraction and the span of zeros after homogenization. The counterexample refutes the exploratory conjecture that a nonnegative three-variable quadratic with positive square coefficients must have its zeros in an affine hyperplane.

These sources were inspected during this investigation. The completed
[publication assessment](publication-quadratic-assessment.md) links the fresh
proof and priority audits, including current versions of the two recent
comparators. The candidate contribution is the three-variable obstruction to
these disjoint certificates, its exposed family, and compact family enforcement.
Incompleteness of weaker PSD, RLT, and triangle systems was already known.
The source-specific gap is proved; an exhaustive absence of equivalent prior
formulations is not claimed.

## Verification record

Run the targeted command

```sh
python research-20260925/check_three_positive_disjoint_counterexample.py
```

The checker uses exact rational arithmetic to verify all principal two-by-two determinants, all twelve edge minima, the five zeros, the nonzero affine-span determinant, the coefficient equations in the exclusion proof, the quartic identity on a determining interpolation grid, and the rank-nine contact system proving extremality for the rational example. It does not mechanically formalize the calculus argument reducing minimizers to edges or the general interpretation of SOS identities. Both displayed verification commands were run and passed. The family identities and extremality equations were also checked symbolically with SymPy by the independent `zero_obstructions` agent. No project-wide checks or CI checks were run for this note.
