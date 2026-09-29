# Prior audit: three ellipsoids and algebraic singleton feasibility

Date: 2026-09-28. Scope: the construction in
[the unbounded-degree note](few-quadratic-unbounded-degree.md), not its proof
review. The question is whether **three rational positive-definite quadratic
inequalities** can force a unique feasible point of arbitrarily large
algebraic degree as the ambient dimension grows. A closely related question
asks for a rational pencil in **two scalar variables** whose spectrahedron
is a singleton at which the matrix has **corank one**.

Arbitrary-degree singleton spectrahedra already follow from classical
finite-variety moment representations. Irrational singleton SOCPs and Gram
spectrahedra also have explicit published predecessors. The inspected
sources do not supply the combination of three native convex quadratics,
unbounded degree, and short rational coefficients. This is a limited
comparison, not a priority claim based on missing search results.

## Closest direct predecessor: finite-variety moment matrices

Monique Laurent, *Semidefinite representations for finite varieties*,
Mathematical Programming 109 (2007), 1–26,
[Theorem 14 and Corollary 15](https://ir.cwi.nl/pub/11663/11663D.pdf),
give a finite moment-matrix representation of the convex hull of evaluation
vectors on a finite real variety. Section 2.2 explicitly handles ideals with
nonreal complex zeros.

Specializing that theorem to the quotient by $T^d-p$, for odd $d$ and a
positive prime $p$, gives the following rational pencil. Use variables
$y_1,\ldots,y_{d-1}$, set $y_0=1$, and index the matrix from zero:

\[
 M(y)_{ij}=
 \begin{cases}
 y_{i+j},&i+j<d,\\
 p\,y_{i+j-d},&i+j\ge d.
 \end{cases}
\]

If $\alpha=p^{1/d}$, Laurent's theorem gives

\[
 \{y:M(y)\succeq0\}
 =\{(\alpha,\ldots,\alpha^{d-1})\}.
\]

This specialization is our application of the theorem, not a separately
named example in the paper. The unique matrix is $v(\alpha)v(\alpha)^{\mathsf
T}$: its rank is one and its corank is $d-1$. The pencil has $d-1$ free
variables. Thus the prior already gives the same power-basis singleton and
unbounded algebraic degree with small rational data. It does not fix the
number of pencil variables at two, give corank one, or express the set by
three native convex quadratic inequalities.

For a concrete check, $d=3,p=2$ gives

\[
 M(y,z)=\begin{pmatrix}1&y&z\\y&z&2\\z&2&2y\end{pmatrix}.
\]

Positive semidefiniteness implies $y,z\ge0$ and
$\det M=6yz-2y^3-z^3-4\ge0$. The arithmetic–geometric mean inequality gives
the reverse inequality, with equality only when $2y^3=z^3=4$. Conversely,
at $(y,z)=(\sqrt[3]2,\sqrt[3]4)$ this matrix is the rank-one outer product
of $(1,y,z)$. Even a planar irrational singleton is therefore covered by
this older representation; retaining the corank distinction is essential.

## Other explicit feasibility predecessors

| Primary source | Exact overlap | Limitation for the present target |
| --- | --- | --- |
| Santiago Laplagne, [*Facial reduction for exact polynomial sum of squares decompositions*](https://arxiv.org/pdf/1810.04215), Theorem 5.1 and its proof, pp. 14–15 | An explicit rational sextic in four polynomial variables has a unique PSD Gram matrix with nonrational entries in $\mathbb Q(\sqrt[3]2)$. The proof explicitly proves uniqueness of the PSD matrix, so this is an isolated feasible point, not just an irrational optimizer. | The Gram matrix is $20\times20$, its affine space has dimension 126, and the displayed sum of three squares gives rank at most three. This is neither a planar pencil nor a corank-one example, and its degree is three. |
| Henrion, Naldi, and Safey El Din, [*SPECTRA — a Maple library for solving linear matrix inequalities in exact arithmetic*](https://homepages.laas.fr/henrion/papers/spectra-more.pdf), Section 4.1 | Displays a classical rational univariate $4\times4$ pencil with feasible set $\{\sqrt2\}$. | Degree two; at the feasible point its two $2\times2$ blocks each have rank one, giving corank two. It does not imply a native convex-QCQP example. |
| Bienstock, Del Pia, and Hildebrand, [*Complexity, exactness, and rationality in polynomial optimization*](https://optimization-online.org/wp-content/uploads/2020/11/8105.pdf), Example 6.3 | The rational SOCP $\sqrt{x_1^2+x_2^2}\le x_0$, $\sqrt{x_0^2+x_3^2}\le3$, $x_1\ge1$, $x_2,x_3\ge2$ forces $(x_0,x_1,x_2,x_3)=(\sqrt5,1,2,2)$. The authors describe this type of example as likely known. | Degree two. Squaring the first SOC row gives $x_1^2+x_2^2-x_0^2\le0$, whose Hessian is indefinite. Convexity of the SOC set does not make that polynomial a native convex quadratic. |

The local exact degree-five example and verifier are in
[the quintic note](span-three-quintic-singleton.md). Its usefulness is as a
small independently checkable instance of the native PSD phenomenon; the
mere existence of an irrational spectrahedral singleton is already old.

## What the output obstruction would establish

The distinctions requiring a precise theorem are fixed three constraints,
positive-definite native Hessians, degree growing with dimension, and a
uniform polynomial input-size bound. The related pencil statement needs
both two scalar variables and corank one. Generic optimizer-degree
formulas do not establish these exact-feasibility properties.

For an FPT output obstruction, fixed-three unbounded degree alone is
insufficient: polynomial growth in the input at a fixed parameter value is
compatible with FPT. Products must yield a degree exponent growing with
the parameter, and the output convention must be explicit. A lower bound
for a dense univariate polynomial representation does not automatically
apply to sparse polynomials, arithmetic circuits, field towers, or radical
expressions. It also does not exclude an FPT **yes/no feasibility**
algorithm. The relevant XP and decision comparisons are recorded in
[the Hessian-span FPT audit](span-fpt-prior-audit.md).

Targeted source verification: inspected Laurent's Theorem 14, Corollary 15,
and Section 2.2; Laplagne's Theorem 5.1 and uniqueness proof; SPECTRA's
displayed irrational singleton; and Bienstock–Del Pia–Hildebrand's
Example 6.3. Searches also covered rational planar singleton spectrahedra,
corank-one singleton pencils, irrational convex quadratic feasibility, and
three-ellipsoid algebraic degree. Those searches do not certify that the
remaining combination is new.
