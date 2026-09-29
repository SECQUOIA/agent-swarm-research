# Extreme cube quadratics when every two-coordinate Hessian is indefinite

Date: 2026-09-27. Status: theorem with an exact finite graph check and
[independent adversarial proof review](cube-strict-extreme-review.md); publication
priority remains unestablished. This is a partial classification. It does
not establish completeness of the disjoint-support SDP plus the previously
constructed family blocks.

The five-contact family from the [earlier note](../research-20260925/three-positive-disjoint-counterexample.md)
accounts for every extreme ray in the strict regime studied here. The remaining
five-edge contact pattern that can occur gives a six-cycle of contacts and a
sum of an affine square and a triangle polynomial. That pattern is nonextreme;
it must not be excluded as infeasible.

## 1. Statement and scope

Let \(\mathcal P_3\) be the cone of quadratic polynomials nonnegative on
\([0,1]^3\). Write

\[
p(x)=c+\ell^Tx+x^TQx,\qquad Q=Q^T.
\]

Assume

\[
Q_{ii}>0,\qquad Q_{ii}Q_{jj}-Q_{ij}^2<0\quad(i\ne j),
\qquad p(v)>0\quad(v\in\{0,1\}^3). \tag{S}
\]

**Theorem.** If \(p\in\mathcal P_3\) satisfies (S) and generates an extreme
ray of \(\mathcal P_3\), then a permutation and complements of its coordinates
put it in the form

\[
\begin{aligned}
p={}&(h-d_1x-d_2y+d_3z)^2
 +2d_3kz(1-x-y)+k(2D+k)xy,\\
&D=d_1+d_2-h,
\end{aligned} \tag{1}
\]

where

\[
0<h<\min(d_1,d_2),\qquad k>0,\qquad d_3>D+k.
\]

Conversely every polynomial (1) under these restrictions satisfies (S) and
generates an exposed extreme ray, as proved in the earlier note.

The conclusion concerns extreme rays, not every polynomial satisfying (S).
The proof does not cover polynomials that vanish at a vertex or have a positive
semidefinite two-coordinate principal Hessian. Those excluded regimes remain
necessary for any claim of completeness of a relaxation for the entire cube
quadratic hull. This theorem also does not assert that every polynomial in the
strict regime decomposes using only extreme rays that remain in that regime.

## 2. Edge contacts and the need for five of them

A minimizer in the relative interior of a face with at least two free
coordinates would require the corresponding principal Hessian to be positive
semidefinite. This contradicts (S). Every minimizer therefore lies on an edge
or vertex. In particular all zeros are in edge interiors, since vertices are
strictly positive. Each edge has at most one zero, because its quadratic
coefficient is positive.

Put \(d_i=\sqrt{Q_{ii}}>0\), and \(s_v=\sqrt{p(v)}>0\). If an edge with
endpoints \(a,b\) has direction \(i\), its restriction, parameterized from
\(a\) to \(b\), is

\[
(1-t)s_a^2+ts_b^2-d_i^2t(1-t)
 =((1-t)s_a-ts_b)^2+\big((s_a+s_b)^2-d_i^2\big)t(1-t).
\]

Consequently nonnegativity on that edge is equivalent to

\[
\lambda_e:=s_a+s_b-d_i\ge0,
\]

and an interior zero exists exactly when \(\lambda_e=0\). Its parameter is
\(t=s_a/d_i\in(0,1)\).

An extreme ray satisfying (S) has at least five contact edges. To see this,
suppose it has \(m\le4\). The vector space of quadratics has dimension ten.
For each contact impose the two homogeneous linear conditions that a
perturbation vanish there and have zero derivative in its edge direction.
The solution space has dimension at least \(10-2m\ge2\) and contains \(p\).
Choose an independent solution \(r\).

For sufficiently small \(\varepsilon>0\), both \(p\pm\varepsilon r\) retain
positive edge curvatures, positive vertex values and the strict principal-minor
conditions. On every contact edge their restrictions remain a positive
multiple of the same squared linear factor. On every other edge the original
minimum is strictly positive, so compactness and the finiteness of the twelve
edges preserve nonnegativity for small \(\varepsilon\). Their minima still
occur on edges or vertices, by the Hessian argument. Thus
\(p\pm\varepsilon r\in\mathcal P_3\), contradicting extremality.

This perturbation argument is local and uses all strict assumptions. It does
not silently extend to singular Hessians or vertex contacts.

## 3. Two elementary contact exclusions

**Three contacts on one face are impossible.** Complement the face coordinates
so that two of the contacts meet at its vertex \(00\), and the third joins
\(10\) to \(11\). Write \(h=s_{00}\). The three contact equalities give

\[
s_{10}=d_1-h,\quad s_{01}=d_2-h,\quad
s_{11}=d_2-d_1+h.
\]

The mixed coefficient on that face is therefore

\[
Q_{12}=\tfrac12(s_{11}^2-s_{10}^2-s_{01}^2+s_{00}^2)
       =d_2(2h-d_1).
\]

Since \(0<h<d_1\), this gives \(|Q_{12}|<d_1d_2\), contrary to (S).

**A three-edge star cannot have any additional contact edge.** Put its common
vertex at the origin. The three edge contacts force

\[
p=(h-d_1x-d_2y-d_3z)^2+2\sum_{i<j}r_{ij}x_ix_j,
\qquad h>0.
\]

On the line segment joining the contacts on axes \(i\) and \(j\), the square
vanishes and both involved coordinates are positive away from the endpoints.
Nonnegativity therefore gives \(r_{ij}\ge0\). Since
\(Q_{ij}=d_id_j+r_{ij}\), condition (S) strengthens this to \(r_{ij}>0\).
Hence a zero cannot have two positive coordinates. Every edge other than the
three incident to the origin has two positive coordinates at any interior
point. No additional contact is possible.

## 4. Complete enumeration of five-edge patterns

Use these edge labels, with coordinates ordered \(x,y,z\):

| Label | Endpoints | Label | Endpoints |
|---:|---|---:|---|
| 0 | 000–100 | 6 | 010–011 |
| 1 | 000–010 | 7 | 011–111 |
| 2 | 000–001 | 8 | 100–110 |
| 3 | 001–101 | 9 | 100–101 |
| 4 | 001–011 | 10 | 101–111 |
| 5 | 010–110 | 11 | 110–111 |

There are 792 five-element subsets of the twelve edges. The 48 cube symmetries
partition them into 24 orbits. The following table gives the lexicographically
least representative of every orbit and its disposition. “Face” means at
least three contacts on a face; “star” means the preceding star exclusion.
The forced-face rows use the identities below. The enumeration is reproduced
using integer arithmetic by the linked checker; it is small enough that the
entire list is also recorded here.

| Orbit | Representative | Disposition |
|---:|---|---|
| 0 | 0,1,2,3,4 | Face |
| 1 | 0,1,2,3,5 | Face |
| 2 | 0,1,2,3,6 | Face |
| 3 | 0,1,2,3,7 | Face |
| 4 | 0,1,2,3,9 | Face |
| 5 | 0,1,2,3,10 | Face |
| 6 | 0,1,2,3,11 | Face |
| 7 | 0,1,2,7,10 | Star |
| 8 | 0,1,3,4,5 | Face |
| 9 | 0,1,3,4,6 | Face |
| 10 | 0,1,3,4,11 | Forced face by A |
| 11 | 0,1,3,5,7 | Face |
| 12 | 0,1,3,5,8 | Face |
| 13 | 0,1,3,5,9 | Face |
| 14 | 0,1,3,5,10 | Face |
| 15 | 0,1,3,5,11 | Face |
| 16 | 0,1,3,6,7 | Family (1) |
| 17 | 0,1,3,6,8 | Face |
| 18 | 0,1,3,6,9 | Face |
| 19 | 0,1,3,6,10 | Forced face by B |
| 20 | 0,1,3,6,11 | Forced face by A |
| 21 | 0,1,3,7,8 | Face |
| 22 | 0,1,3,7,11 | Forced face by A |
| 23 | 0,1,6,7,9 | Six-cycle; nonextreme |

The slack definition implies these identities without using quadratic
compatibility of the vertex values:

\[
\begin{array}{ll}
\mathrm A:&-\lambda_1+\lambda_2-\lambda_3+\lambda_5+\lambda_{10}-\lambda_{11}=0,\\
\mathrm B:&-\lambda_0+\lambda_1-\lambda_6+\lambda_7+\lambda_9-\lambda_{10}=0,\\
\mathrm C:&\lambda_0-\lambda_1+\lambda_6-\lambda_7-\lambda_9+\lambda_{10}=0.
\end{array}
\]

For each indicated representative the negative terms vanish. Nonnegative
slacks force the remaining positive terms to vanish. In rows 10, 20 and 22,
identity A forces edges 2, 5 and 10. Row 19 uses B to force edges 7 and 9.
Each enlarged set has three contacts on a face. In row 23, identity C forces
edge 10, giving the six-cycle \(\{0,1,6,7,9,10\}\); that case needs a different
argument.

## 5. The six-cycle is feasible but not extreme

For the six-cycle in row 23, put \(h=s_{000}\) and use the positive diagonal
roots \(d_i\). Contacts 0 and 1 give \(c=h^2\),
\(\ell_x=-2hd_1\), \(\ell_y=-2hd_2\). The contact slack equalities give

\[
\begin{aligned}
s_{100}&=d_1-h,&s_{010}&=d_2-h,\\
s_{101}&=d_3-d_1+h,&s_{011}&=d_3-d_2+h,\\
s_{111}&=d_1+d_2-d_3-h.
\end{aligned}
\]

Vanishing derivatives on edges 7 and 10 give

\[
Q_{12}+Q_{13}=d_1(d_2-d_3),\qquad
Q_{12}+Q_{23}=d_2(d_1-d_3).
\]

Writing \(K=Q_{12}-d_1d_2\), and then using a vertical contact to determine
\(\ell_z\), determines every coefficient:

\[
\boxed{
p=(h-d_1x-d_2y+d_3z)^2+2K\,[z+xy-xz-yz].
} \tag{2}
\]

The chord between the two axis contacts forces \(K\ge0\). Condition (S)
then forces \(K>0\). The bracket is the nonnegative quadratic

\[
z+xy-xz-yz=z(1-x)(1-y)+xy(1-z).
\]

The two summands in (2) are nonzero and nonproportional: the square has positive
constant \(h^2\), whereas the bracket has zero constant. Thus (2) does not
generate an extreme ray.

The six-cycle is an informative limitation of a simpler graph argument. A
five-edge pattern of direction counts \((2,2,1)\) is not automatically
impossible under (S); it can force an additional contact and a decomposition.

## 6. Recovery of the family from the surviving orbit

Orbit 16 has the equivalent representative \(\{0,1,6,9,11\}\): two contacts
at the bottom origin in the \(x,y\) directions and three vertical contacts at
\((x,y)=(1,0),(0,1),(1,1)\).

Put \(h=s_{000}>0\), \(d_i=\sqrt{Q_{ii}}\), and \(D=d_1+d_2-h\).
The first two contacts give

\[
0<h<\min(d_1,d_2),\quad c=h^2,\quad
\ell_x=-2hd_1,\quad\ell_y=-2hd_2.
\]

The first two vertical roots are \((d_1-h)/d_3\) and
\((d_2-h)/d_3\). Write the third as \((D+k)/d_3\), so that
\(0<D+k<d_3\). Vanishing derivatives at the three vertical roots yields

\[
\ell_z=2d_3(h+k),\qquad
Q_{13}=-d_3(d_1+k),\qquad Q_{23}=-d_3(d_2+k).
\]

Finally, comparing \(p(1,1,0)=(D+k)^2\) gives

\[
Q_{12}=d_1d_2+kD+k^2/2.
\]

These are exactly the coefficients of (1). The chord between the two bottom
axis contacts implies \(Q_{12}\ge d_1d_2\), and (S) makes this inequality
strict. Hence \(k(2D+k)>0\). Since \(D>0\) and \(D+k>0\), the alternative
\(k<-2D\) is impossible. Thus \(k>0\), completing the classification.

Every extreme ray in the stated regime has at least five contact edges.
Choose any five. The complete table either rules the pattern out, proves the
polynomial nonextreme, or recovers (1). This proves the theorem without assuming
that there are exactly five contacts in advance.

## 7. Verification, significance and unresolved scope

The targeted command actually run was

```sh
python research-20260927/check_cube_strict_extreme_classification.py
```

It passed. It checks all 792 five-edge subsets, their 24 orbits, the three
integer slack identities, the forced-face exclusions, the forced six-cycle,
and the equivalence of the surviving orbit to the family's contact pattern.
It does not mechanically verify the calculus reduction, local perturbation
argument, coefficient recovery, or exposed-ray statement. No project-wide
verification or CI checks were run.

The calculation explains why searching for another five-contact family with
strictly indefinite two-coordinate Hessians repeatedly recovers the existing
family. It directs further completeness research toward vertex contacts,
positive semidefinite face Hessians, and their singular boundaries. It provides
no solver-speedup guarantee and no full quadratic-hull formulation.

This note adds a restricted extreme-ray classification to the earlier family's
construction. Classical exact cube moment lifts already enforce every
nonnegative quadratic; the present result does not improve on their exactness.
The earlier note and [family SDP note](../research-20260925/three-positive-family-sdp.md)
record those comparisons. A targeted literature audit of this classification
itself is still required before making a publication-priority claim.
