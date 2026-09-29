# Independent check of the three-variable zero obstruction

This note independently checks the explicit quadratic produced during the
three-positive-diagonal investigation. It establishes nonnegativity and
exclusion from the particular cone below. It makes no literature novelty
claim and does not exclude stronger semidefinite formulations.

## Polynomial and certificate cone

On the unit cube, let

\[
p(x,y,z)=x^2+y^2+9z^2+6xy-12xz-12yz-x-y+9z+\tfrac14.
\]

Consider finite sums of terms

\[
w_{S,T}(x)\ell(x_R)^2,\qquad
w_{S,T}(x)=\prod_{i\in S}x_i\prod_{j\in T}(1-x_j),
\]

where \(S,T\) are disjoint, \(R=\{1,2,3\}\setminus(S\cup T)\),
and \(\ell\) is affine in the coordinates in \(R\). Allowing a positive
semidefinite Gram matrix in each block gives the same cone, by decomposing
each matrix into rank-one matrices. Polynomial equality is required; terms
of degree three or four may cancel across blocks.

The polynomial \(p\) is nonnegative on the cube, has strictly positive
square coefficients, and does not belong to this cone.

## Exact nonnegativity check

The quadratic coefficient matrix is

\[
Q=\begin{pmatrix}1&3&-6\\3&1&-6\\-6&-6&9\end{pmatrix}.
\]

Its three principal minors of order two are \(-8,-27,-27\). A minimum
in the relative interior of a cube face of dimension at least two would
require the corresponding principal Hessian to be positive semidefinite.
These minors rule this out. Compactness therefore puts a global minimum on
an edge or vertex.

Symmetry between \(x\) and \(y\) reduces the twelve edge checks to the
following eight restrictions. The first four each stand for two edges.

| Free variable | Fixed variables | Restriction | Minimum on the edge |
|---|---|---|---|
| \(x\) | \(y=z=0\) | \((x-1/2)^2\) | \(0\) |
| \(x\) | \(y=0,z=1\) | \(x^2-13x+73/4\) | \(25/4\) |
| \(x\) | \(y=1,z=0\) | \(x^2+5x+1/4\) | \(1/4\) |
| \(x\) | \(y=z=1\) | \(x^2-7x+25/4\) | \(1/4\) |
| \(z\) | \(x=y=0\) | \(9z^2+9z+1/4\) | \(1/4\) |
| \(z\) | \(x=0,y=1\) | \(9(z-1/6)^2\) | \(0\) |
| \(z\) | \(x=1,y=0\) | \(9(z-1/6)^2\) | \(0\) |
| \(z\) | \(x=y=1\) | \(9(z-5/6)^2\) | \(0\) |

This proves nonnegativity. In particular, the following five points are
zeros:

\[
u_1=(1/2,0,0),\quad u_2=(0,1/2,0),\quad
u_3=(1,0,1/6),\quad u_4=(0,1,1/6),\quad
u_5=(1,1,5/6).
\]

They affinely span three-dimensional space: the determinant of the matrix
with rows \((1,u_i)\), for \(i=1,2,3,5\), is \(-1/12\).

## Exclusion by propagation along zero edges

Call an edge a zero edge when its relative interior contains a zero of
\(p\). Suppose a permitted summand is positive at one endpoint of a zero
edge in direction \(i\). Because all summands are nonnegative on the
cube, this summand vanishes at the interior zero.

Its weight cannot contain coordinate \(i\). Indeed, if it did, the
affine factor would be independent of \(i\). The weight is positive at
the interior zero, so the affine factor would vanish identically along
the edge, contradicting positivity at the endpoint. With coordinate
\(i\) absent from the weight, the weight is a positive constant along
the edge. The affine factor has an interior root and is nonzero at one
endpoint. It must consequently be nonzero at the other endpoint. The
summand is positive at both endpoints.

Now \(p(0,0,0)=1/4\), so a representation would have a summand positive
at the origin. Propagate this summand along the zero edges

\[
(0,0,0)\longleftrightarrow(1,0,0),\qquad
(0,0,0)\longleftrightarrow(0,1,0),\qquad
(1,0,0)\longleftrightarrow(1,0,1).
\]

These edges use all three coordinate directions. The summand's weight
must omit every coordinate, so the summand is an unweighted affine
square. Its affine factor vanishes at all five \(u_i\), because its
weight is everywhere one. Affine spanning forces that factor to be
identically zero, contradicting positivity at the origin.

This proves nonmembership without numerical separation or a closure
assumption. The argument also disproves the tentative claim that all
zeros of a cube-nonnegative quadratic with strictly positive square
coefficients must lie in one affine hyperplane.

## Closedness and the meaning of the obstruction

The same fixed finite-block cone is closed. For each weight and its
affine monomial vector \(b_R\), the matrix

\[
M_{S,T}=\int_{[0,1]^3}w_{S,T}(x)b_R(x)b_R(x)^\top\,dx
\]

is positive definite: the weight is positive in the cube interior, and
a nonzero affine polynomial cannot vanish there identically. In a
convergent sequence of represented polynomials, integration bounds the
sum of traces of the positive semidefinite Gram matrices by the reciprocal
of the smallest eigenvalue among the finitely many \(M_{S,T}\). Thus a
subsequence of all Gram matrices converges and represents the limit.

Consequently some strictly positive perturbations \(p+\varepsilon\),
\(\varepsilon>0\), also lie outside the cone. This argument does not
give a numerical value of \(\varepsilon\). The result concerns these
disjoint affine-square blocks only; higher-degree factors and other
semidefinite lifts are outside its scope.

## Checks performed

The targeted command actually run was `python -`, with an inline SymPy
program. This independent calculation enumerated all twelve edge
restrictions, evaluated their exact minima, and computed the augmented
zero matrix rank and the determinant above. The calculation used exact
rational arithmetic. It checks the displayed arithmetic; the
face-minimum and propagation arguments are mathematical proofs and are
not supplied by the computation. No project-wide checks or CI checks were
run.

Exploratory calculations preceding the exact example optimized random
linear functionals over the six-tetrahedron copositive description and
then tested the resulting polynomial against the finite-block cone.
They identified the contact pattern. Random strictly positive-diagonal
quadratics had failed to reveal a gap, so those random tests did not
support a universal exactness conclusion. The exact example and proof
above supersede that numerical impression.

## Independent check of the parameter family

The obstruction extends to the following family, checked independently
after the explicit example. Assume

\[
h,d_1,d_2,k>0,\qquad h<\min(d_1,d_2),\qquad
D=d_1+d_2-h,\qquad d_3>D+k,
\]

and put \(t=d_3-D-k>0\). Define

\[
p=(h-d_1x-d_2y+d_3z)^2
  +2d_3kz(1-x-y)+k(2D+k)xy.
\]

The three principal minors of order two of its quadratic coefficient
matrix are

\[
-\frac{k(2D+k)(4d_1d_2+2Dk+k^2)}4,\qquad
-d_3^2k(2d_1+k),\qquad -d_3^2k(2d_2+k).
\]

All are strictly negative, so the earlier reduction to edges applies.
On the bottom edges with \(x=0\) or \(y=0\), the restrictions are
squares. On the remaining bottom edges, they have the form
\((h-d_1-d_2y)^2+k(2D+k)y\), or the expression obtained by exchanging
the first two coordinates, and are strictly positive. The vertical
restrictions at \((x,y)=(1,0),(0,1),(1,1)\) are respectively

\[
[d_3z-(d_1-h)]^2,\quad
[d_3z-(d_2-h)]^2,\quad
[d_3z-(D+k)]^2.
\]

The remaining vertical restriction is
\((h+d_3z)^2+2d_3kz>0\). On a top edge with \(x=0\), the restriction
is \((h-d_2y+d_3)^2+2d_3k(1-y)>0\), and likewise after exchanging
coordinates. On the top edge with \(x=1\), substitution \(r=1-y\)
gives the exact identity

\[
p(1,1-r,1)=t^2+
 [2d_2(k+t)+k(k+2t)]r+d_2^2r^2>0.
\]

Exchanging the coordinates checks the last edge. Thus the polynomial is
nonnegative, and its zero set consists exactly of the five points

\[
A=(h/d_1,0,0),\quad B=(0,h/d_2,0),\quad
C=(1,0,(d_1-h)/d_3),\quad
F=(0,1,(d_2-h)/d_3),\quad
E=(1,1,(D+k)/d_3).
\]

All five lie in edge relative interiors. The determinant of the
augmented matrix with rows \((1,A),(1,B),(1,C),(1,E)\) is

\[
-\frac{hk(d_1-h)}{d_1d_2d_3}\ne0.
\]

There is also a direct exclusion proof. A summand positive at the origin
has an affine factor \(L=\alpha+\beta x+\gamma y+\delta z\), where
\(\alpha\ne0\), and its weight uses only factors \(1-x_i\). Its
weight is positive at \(A,B\). Vanishing there forces
\(\beta=-\alpha d_1/h\) and \(\gamma=-\alpha d_2/h\), so neither
\(x\) nor \(y\) can occur in the weight. Its weight is consequently
positive at \(C\). Vanishing at \(C\) forces
\(\delta=\alpha d_3/h\ne0\), excluding \(z\) from the weight as
well. But then \(L(E)=\alpha k/h\ne0\), contradicting the zero at
\(E\). Every strict assumption used here has been retained.

A second targeted `python -` command used an inline SymPy program to
verify both top-edge identities, the three vertical square identities,
all five zero substitutions, the principal minors, the determinant, and
the final affine-factor value. These were symbolic rational identities
in the parameters. They do not replace the sign and cone arguments.

## Quartic certificate and exposed-ray check

Let \(L=h-d_1x-d_2y+d_3z\). The following polynomial identity was
independently checked by symbolic expansion:

\[
\begin{aligned}
p={}&(L-kxy)^2+2d_3kz(1-x)(1-y)\\
 &+k(2d_1+k)xy(1-x)+2kd_2xy(1-y)
   +k^2x^2y(1-y).
\end{aligned}
\]

Every term is nonnegative on the cube. This is a certificate of degree
at most four in the preordering generated by the six individual box
inequalities. It supplies another proof of nonnegativity. For this
identity's positivity conclusion alone, the weaker assumptions
\(d_1,d_2,d_3,k\ge0\) and arbitrary real \(h\) suffice. The strict
assumptions above place the contacts in the required edge interiors.

This certificate lies outside the restricted certificate format examined
earlier: its first square has a bilinear factor, and other terms use both
\(x\) and \(1-x\), or both \(y\) and \(1-y\), in a weight. Thus
there is no conflict with the separation proof.

Under the strict family assumptions, \(p\) generates an exposed extreme
ray of the cone of all quadratics nonnegative on the cube. To check this,
write another such quadratic as

\[
q=q_0+\ell_x x+\ell_y y+\ell_z z+
Q_{xx}x^2+Q_{yy}y^2+Q_{zz}z^2+
2Q_{xy}xy+2Q_{xz}xz+2Q_{yz}yz,
\]

and suppose it vanishes at the five contacts. Each contact is a local
minimum along its edge, so the tangential derivative vanishes too. Set
\(\lambda=Q_{xx}/d_1^2\). The contact at \(A\) forces

\[
q_0=\lambda h^2,\qquad \ell_x=-2\lambda hd_1,
\qquad \lambda\ge0.
\]

The contact at \(B\) then gives \(Q_{yy}=\lambda d_2^2\) and
\(\ell_y=-2\lambda hd_2\). Comparing the value at \((1,0,0)\)
along its bottom edge and its vertical edge through \(C\) gives
\(Q_{zz}=\lambda d_3^2\); division is valid because \(d_1-h>0\).
The tangential derivative equations at \(C,F,E\) give

\[
\ell_z=2\lambda d_3(h+k),\qquad
Q_{xz}=-\lambda d_3(d_1+k),\qquad
Q_{yz}=-\lambda d_3(d_2+k).
\]

Finally the vertical-edge contact at \(E\) determines

\[
Q_{xy}=\lambda\left(d_1d_2+kD+\frac{k^2}{2}\right).
\]

Thus \(q=\lambda p\), including the degenerate case \(\lambda=0\).
The nonnegative linear functional
\(q\mapsto q(A)+q(B)+q(C)+q(F)+q(E)\) therefore exposes precisely
the ray \(\{\lambda p:\lambda\ge0\}\).

Two further targeted `python -` commands supplied exact symbolic checks.
The first expanded the quartic identity and checked that the derived
coefficient vector equals \(\lambda p\). The second formed nine linear
contact equations: values and tangential derivatives at \(A,B,C,E\),
and the tangential derivative at \(F\). In the coefficient order
\((1,x,y,z,x^2,y^2,z^2,xy,xz,yz)\), deleting the \(x^2\) column
gives a square matrix with determinant

\[
-\frac{h^2(d_1-h)^2}{d_2^2d_3^2}\ne0.
\]

This independently confirms uniqueness after fixing the square
coefficient. The proof uses only those nine equations; adding the
remaining contact value cannot enlarge the solution space.
