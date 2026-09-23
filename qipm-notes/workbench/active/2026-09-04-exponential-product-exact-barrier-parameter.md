# Exact barrier parameter of a product of exponential cones

Status: Proved; literature-screened; independently audited twice; novelty tentative  
Started: 2026-09-04  
Paper status: Not incorporated  
Confidence: High on the theorem and certificate tensorization; moderate on priority

## Result

Let

\[
 K_{\exp}=\operatorname{cl}\{(u,v,w):v>0,\ w\geq v e^{u/v}\}
 \subset\mathbb R^3.                                      \tag{1}
\]

For every positive integer \(R\), the optimal self-concordant-barrier
parameter of its Cartesian power is

\[
 \boxed{\vartheta_{\rm opt}(K_{\exp}^{R})=3R.}             \tag{2}
\]

The lower bound in (2) applies to an arbitrary barrier that couples all
\(R\) cone factors.  It does not assume logarithmic homogeneity or additive
separability.  In particular, every logarithmically homogeneous
self-concordant (LHSC) barrier on \(K_{\exp}^{R}\) has parameter at least
\(3R\).  The usual sum of the single-cone barriers attains \(3R\), so
coupling the factors cannot improve the parameter.

The dual exponential cone has the same exact result.  In the coordinates
of (1), its interior satisfies

\[
 \operatorname{int}K_{\exp}^*=\left\{(a,b,c):a<0,\
       c>-a\exp(b/a-1)\right\},
\]

and the invertible linear map
\((a,b,c)\mapsto(a-b,-a,c)\) sends it to
\(\operatorname{int}K_{\exp}\).  Optimal barrier parameters are invariant
under invertible linear maps.  On closure, the additional face
\(a=0,\ b,c\geq0\) maps to the usual \(v=0\) exponential-cone face.
Therefore
\(\vartheta_{\rm opt}((K_{\exp}^*)^R)=3R\), and more generally an arbitrary
coupled barrier on
\(K_{\exp}^{R_p}\times(K_{\exp}^*)^{R_d}\) has exact optimal parameter
\(3(R_p+R_d)\).

This sharpens the universal \(2R\) bound for a product of \(R\)
three-dimensional proper cones.  For a direct positive-mixture exponential-
cone formulation with \(R\) atoms, its ambient exponential-cone product
therefore has **exact** optimal parameter \(3R\), rather than merely the
previous interval \([2R,3R]\).

The proof has two independent forms:

1. a tensorization of Nesterov's recession-direction lower-bound
   certificates, which proves (2) even for non-LHSC barriers; and
2. an explicit family of Hildebrand projective cross-ratio configurations
   whose lower bounds tend to three on one exponential cone.  Concatenating
   the configurations by the positive-branch product lemma gives \(3R\).

## Recession-certificate tensorization

For a closed full-dimensional convex set \(C\), a **Nesterov certificate**
consists of

\[
 x_0\in\operatorname{int}C, \quad
 p_1,\ldots,p_s\in\operatorname{rec}C, \quad
 a_i,b_i>0                                             \tag{3}
\]

such that

\[
 x_0-\sum_i a_i p_i\in C,qquad
 x_0-b_i p_i\notin\operatorname{int}C\quad(1\leq i\leq s).
                                                               \tag{4}
\]

Its value is \(\sum_i a_i/b_i\).  Nesterov's lower-bound theorem says that
every self-concordant barrier on \(C\) has parameter at least this value.
Define \(\mathfrak n(C)\) as the supremum of the values of all such
certificates.

> **Tensorization lemma.** For closed full-dimensional convex sets
> \(C_1,\ldots,C_k\),
> \[
>       \mathfrak n(C_1\times\cdots\times C_k)
>       \geq\sum_{j=1}^k\mathfrak n(C_j).             \tag{5}
> \]

To prove this, choose one certificate in each factor and take the product
base point.  Embed each recession direction of \(C_j\) in the \(j\)-th
direct summand, with all other components zero.  The joint subtraction
point in the first condition of (4) is the product of the local joint
subtraction points and hence is feasible.
Subtracting the local threshold \(b_i p_i\) makes the \(j\)-th component
noninterior, so the product point is noninterior.  The certificate value is
the sum of all local values.  Taking independent suprema proves (5).

Consequently, whenever cones \(K_j\) have parameter-sharp Nesterov
certificates of values \(\vartheta_j\), every possibly coupled barrier on
their product has parameter at least \(\sum_j\vartheta_j\).  If the factors
also possess barriers of those parameters, their sum supplies the matching
upper bound.  Thus this certificate-sharp class has an exactly additive
optimal barrier parameter even though arbitrary barriers on the product are
allowed to couple the factors.

## An explicit parameter-three certificate for the exponential cone

Put

\[
 h(v,w)=v\log(w/v),\qquad (v,w)\in\mathbb R_{++}^2.   \tag{6}
\]

After permuting coordinates, (1) is exactly

\[
 K_{\exp}=\operatorname{cl}\{(v,w,u):u\leq h(v,w)\}, \tag{7}
\]

the closed hypograph cone of the concave one-homogeneous function \(h\).
Its interior is \(v,w>0\) and \(u<h(v,w)\).  Its nontrivial closure face
is \(v=0,w\geq0,u\leq0\); there are no finite closure points with
\(v>0,w=0\).  Thus (7) is exactly the usual exponential-cone closure.
Fawzi and Saunderson's Proposition 3.11, specialized to a scalar output,
already implies a lower bound of three.  The following specialization of
their proof records the actual certificate.

Fix \(0<\epsilon<1\), and write \(L=\log(1/\epsilon)\).  Set

\[
 x_1=(1,\epsilon),\qquad x_2=(\epsilon,1),\qquad
 x_0=x_1+x_2=(1+\epsilon,1+\epsilon),                \tag{8}
\]

so that

\[
 h(x_0)=0,\quad h(x_1)=-L,\quad h(x_2)=\epsilon L,\quad
 \Delta:=h(x_0)-h(x_1)-h(x_2)=(1-\epsilon)L>0.       \tag{9}
\]

Choose \(\tau'>\Delta\) and \(\tau>\tau'\).  In the coordinates of (7),
take the interior base point and three recession directions

\[
 \begin{aligned}
 y_0&=(x_0,h(x_0)-\tau),\\
 p_1&=(x_1,h(x_1)),\qquad
 p_2=(x_2,h(x_2)),\qquad
 p_3=(0,0,-\tau).
 \end{aligned}                                      \tag{10}
\]

Use coefficients and thresholds

\[
 a_1=a_2=1,\quad a_3=1-\tau'/\tau,\qquad
 b_1=b_2=1+\epsilon,\quad b_3=1.                    \tag{11}
\]

All \(p_i\) belong to the cone and hence are recession directions.  The
first component pair of \(y_0-b_i p_i\) leaves the open orthant for
\(i=1,2\), while \(y_0-p_3=(x_0,h(x_0))\) lies on the hypograph boundary.
Moreover,

\[
 y_0-p_1-p_2-a_3p_3=(0,0,\Delta-\tau')\in K_{\exp}. \tag{12}
\]

Thus (10)--(11) form a certificate of value

\[
 \frac{2}{1+\epsilon}+1-\frac{\tau'}{\tau}.         \tag{13}
\]

For each fixed \(\epsilon\), choose any fixed \(\tau'>\Delta\), first let
\(\tau\to\infty\), and then let \(\epsilon\downarrow0\).  The values in
(13) tend to three.  Therefore

\[
                         \mathfrak n(K_{\exp})\geq3. \tag{14}
\]

Tensorization gives \(\mathfrak n(K_{\exp}^R)\geq3R\).  On the other hand,

\[
 -\log\!\bigl(v\log(w/v)-u\bigr)-\log v-\log w     \tag{15}
\]

is the standard parameter-three LHSC barrier on (7), and summing (15) over
the factors gives a parameter-\(3R\) barrier.  This proves (2).

## A master theorem for one-sided perspective cones

The exponential cone is one instance of a broader exact product theorem.
For \(j=1,\ldots,k\), let

\[
 h_j:\mathbb R_{++}^{n_j}\longrightarrow\mathbb R
\]

be concave and positively homogeneous of degree one, and assume its closed
hypograph

\[
 {\cal H}_j=\operatorname{cl}\{(x,z):x\in\mathbb R_{++}^{n_j},
                                      \ z\leq h_j(x)\}          \tag{14a}
\]

is full-dimensional.  Fawzi--Saunderson's Proposition 3.11 gives
\(\mathfrak n({\cal H}_j)\geq n_j+1\).  Certificate tensorization therefore
gives, for every possibly coupled self-concordant barrier on the product,

\[
 \boxed{\vartheta\geq\sum_{j=1}^k(n_j+1).}                     \tag{14b}
\]

Whenever each \(h_j\) is compatible with the orthant logarithmic barrier so
that

\[
 -\log(h_j(x)-z)-\sum_{\ell=1}^{n_j}\log x_\ell               \tag{14c}
\]

is an \((n_j+1)\)-barrier, (14b) is attained and the product optimum is
exactly additive.  Besides the exponential cone
\(h(v,w)=v\log(w/v)\), this includes the one-sided weighted-geometric-mean
 hypograph cones (sometimes called one-sided generalized-power cones)

\[
 h(x)=\prod_{\ell=1}^{n}
       (x_\ell/\alpha_\ell)^{\alpha_\ell},
 \qquad \alpha_\ell>0,\quad\sum_\ell\alpha_\ell=1.             \tag{14d}
\]

Thus a product of these one-sided cones with \(n_j\) positive coordinates
has exact optimal coupled-barrier parameter \(\sum_j(n_j+1)\), not merely
the universal \(2k\).  The one-sided hypothesis matters: the usual absolute
generalized-power cone
\(\{(x,z):\prod x_\ell^{\alpha_\ell}\geq\|z\|_2\}\) has no output recession
ray, and this certificate does not prove that its known
\((n+1)\)-barrier is optimal.  Already for a three-dimensional absolute
power cone, the exact optimal parameter remains open.

## Projective interpretation for the exponential cone

The same family makes Hildebrand's cross-ratio lower bound sharp.  Define
the three linearly independent boundary vectors

\[
 e_1=(x_1,h(x_1)),\qquad
 e_2=(x_2,h(x_2)),\qquad
 e_3=(0,0,-1),                                      \tag{16}
\]

Their determinant is \(-(1-\epsilon^2)\), so they are indeed independent.

Take

\[
 x^*=e_1+e_2+(\tau-\Delta)e_3
     =(x_0,h(x_0)-\tau)\in\operatorname{int}K_{\exp},
 \qquad \tau>\Delta.                                \tag{17}
\]

Choose any functional in \(\operatorname{int}K_{\exp}^*\) and normalize
the three boundary rays in (16) and the ray through \(x^*\) onto its common
compact affine base before applying Hildebrand's theorem.  These projective
rescalings do not change the cross-ratios or the calculation below.

If \(\beta_i>0\) is the first opposite boundary time on the ray
\(x^*-t e_i\), Hildebrand's positive cross-ratio is the coefficient of
\(e_i\) in (17) divided by \(\beta_i\).  The domain-coordinate boundary
tests give

\[
 \beta_1,\beta_2\leq1+\epsilon,qquad \beta_3=\tau. \tag{18}
\]

At \(t=1+\epsilon\), the first two domain-coordinate pairs are,
respectively, \((0,1-\epsilon^2)\) and
\((1-\epsilon^2,0)\), so their first boundary contacts occur no later.
The third ray is \((x_0,-\tau+t)\), whose first boundary contact is exactly
at \(t=\tau\).  Consequently \(q_1=1/\beta_1\),
\(q_2=1/\beta_2\), and \(q_3=(\tau-\Delta)/\tau\).

Subtracting the coefficient displayed in (17) leaves the sum of the other
two boundary vectors.  For \(i=1,2\), the \(e_3\) term lowers the hypograph
coordinate strictly because \(\tau>\Delta\); for \(i=3\), strict concavity
is exactly the positive gap \(\Delta\) in (9).  Thus each remaining sum is
interior.  Hence \(\beta_i\) is strictly larger than that coefficient, so
all three cross-ratios lie in \((0,1)\).  Their sum satisfies

\[
 S_{\epsilon,\tau}
 \geq \frac{2}{1+\epsilon}+1-\frac{\Delta}{\tau}.   \tag{19}
\]

For all sufficiently small \(\epsilon\) and sufficiently large \(\tau\),
(19) ensures \(S_{\epsilon,\tau}>2\).  Hildebrand's positive branch then
gives \(\nu\geq S_{\epsilon,\tau}\).
Taking \(\tau\to\infty\) and \(\epsilon\downarrow0\) proves that the
supremal Hildebrand lower bound for \(K_{\exp}\) is three.  It cannot exceed
three because the explicit barrier (15) has parameter three.  Applying the
positive-branch product construction to \(R\) copies gives the LHSC lower
bound \(3R\) directly.

## Mixed products and matrix relative-entropy cones

The tensorization lemma is not specific to (1).  Fawzi and Saunderson prove
that for a matrix-valued concave one-homogeneous map

\[
 h:\mathbb H_{++}^{n_1}\times\mathbb H_{++}^{n_2}
       \longrightarrow\mathbb H^m,                 \tag{20}
\]

every barrier on the closed matrix hypograph has parameter at least
\(n_1+n_2+m\).  Their proof restricts the input matrices to diagonal
subspaces and constructs precisely the Nesterov certificates used above.
It follows from (5), or by first taking the product of those diagonal
sections, that a product of such cones has the coupled-barrier lower bound

\[
              \vartheta\geq\sum_j(n_{1j}+n_{2j}+m_j). \tag{21}
\]

Whenever the compatible natural barriers of their Theorems 1.1 or 1.5
apply, (21) is attained and hence is exact.  In particular, for a product
of quantum-relative-entropy epigraph cones with matrix sizes \(n_j\) and
scalar epigraph coordinates,

\[
              \vartheta_{\rm opt}=\sum_j(2n_j+1).   \tag{22}
\]

More generally, certificate-sharp orthant, Lorentz, PSD, exponential,
product-ball homogenization, and these matrix-perspective factors may be
mixed: the exact optimal parameter of the ambient product is the sum of
their individual optimal parameters, even against a globally coupled
barrier.  For the product-ball homogenization cone
\(\mathcal H_{q,s}=\{(t,y_1,\ldots,y_q):\|y_a\|_2\leq t\}\), the explicit
parameter-sharp certificate and optimal parameter \(q+1\) are proved in
[the bounded-face sharing note](2026-09-04-bounded-face-sharing-sharp-models.md#6-exact-barriers-sharing-factors-does-not-share-the-ipm-parameter).

### Exact loss under aggregation and projection

There is a useful contrast between coupling a barrier on a fixed product
and changing the ambient cone.  Define the \(d\)-coordinate relative-entropy
epigraph cone

\[
 {\cal R}_d=\operatorname{cl}\left\{(t,x,y):
 x,y\in\mathbb R_{++}^d,\quad
 t\geq\sum_{\ell=1}^d x_\ell\log(x_\ell/y_\ell)\right\}.
                                                               \tag{23}
\]

Fawzi--Saunderson's scalar-output lower bound (their Remark 3.12), together
with the standard compatible relative-entropy barrier, gives

\[
             \vartheta_{\rm opt}({\cal R}_d)=2d+1.             \tag{24}
\]

The matching intrinsic barrier is
\[
 -\log\!\left(t-\sum_{\ell=1}^d
 x_\ell\log(x_\ell/y_\ell)\right)
 -\sum_{\ell=1}^d\log x_\ell-\sum_{\ell=1}^d\log y_\ell .
                                                               \tag{24a}
\]

On the other hand, introducing local epigraph variables \(t_\ell\) and
applying the linear map that retains \(x,y\) and sends
\((t_1,\ldots,t_d)\) to \(t=\sum_\ell t_\ell\),

\[
 t_\ell\geq x_\ell\log(x_\ell/y_\ell),\qquad
 t=\sum_\ell t_\ell                                      \tag{25}
\]

realizes \({\cal R}_d\) directly as a linear image of \(K_{\exp}^d\):
under the coordinate convention (7), the local epigraph coordinate is
\(t_\ell=-u_\ell\).
The ambient product in (25) has exact optimal parameter
\(3d\), whereas its projected aggregate cone has exact optimal parameter
\(2d+1\).  Thus projection lowers the optimal parameter by exactly
\(d-1\), a ratio tending to \(2/3\).  No coupled barrier on the unchanged
ambient product can realize this reduction; it requires passing to the
aggregate cone and its intrinsic barrier.

More generally, partition \(N\) scalar relative-entropy terms into \(B\)
blocks of sizes \(d_1,\ldots,d_B\).  Modeling each block by one cone
\({\cal R}_{d_j}\) gives a product whose exact coupled-barrier optimum is

\[
          \sum_{j=1}^B(2d_j+1)=2N+B,                         \tag{26}
\]

compared with the exact value \(3N\) for the coordinatewise exponential-
cone product.  This is an exact barrier-parameter compression theorem for
block aggregation.  It does not by itself say that the larger block Hessian
or its Newton system is cheaper to evaluate.

### Exact positive-output aggregation law

The block formula is a special case of a more general output-dimension law.
Let \(N,B\geq1\), let \(A\in\mathbb R_+^{B\times N}\), and put

\[
 \phi_i(x_i,y_i)=x_i\log(x_i/y_i),
\]

and define the positive-output aggregation cone

\[
 {\cal C}_A=\operatorname{cl}\left\{(x,y,z):x,y\in\mathbb R_{++}^N,
       \ z-A\phi(x,y)\in\mathbb R_+^B\right\}.              \tag{27}
\]

Then

\[
 \boxed{\vartheta_{\rm opt}({\cal C}_A)=2N+B.}              \tag{28}
\]

Indeed, the vector map
\(h(x,y)=-A\phi(x,y)\) is concave with respect to
\(\mathbb R_+^B\), one-homogeneous, and one-compatible with the orthant
barrier \(-\sum_i\log x_i-\sum_i\log y_i\).  Compatibility follows first
coordinatewise for the logarithmic perspective and is preserved by the
positive map \(A\).  The natural barrier

\[
 F_A(x,y,z)=
 -\sum_{b=1}^B\log\left(z_b-\sum_{i=1}^N A_{bi}\phi_i(x_i,y_i)\right)
 -\sum_{i=1}^N(\log x_i+\log y_i)                            \tag{29}
\]

therefore has parameter \(2N+B\).  Conversely, Proposition 3.11 and its
orthant-output proof give the matching lower bound: the input orthant has
\(2N\) independent boundary directions and the output orthant has \(B\).
Equivalently, (29) follows by restricting Fawzi--Saunderson's positive-map
perspective barrier to diagonal input and output matrix subspaces.

There is an exact coordinatewise lift.  Introduce \(q_i\geq\phi_i(x_i,y_i)\)
with \(N\) exponential cones, an output slack \(r\in\mathbb R_+^B\), and

\[
                         z=Aq+r.                             \tag{30}
\]

Because \(A\geq0\), projection of (30) is exactly (27).  Certificate
tensorization shows that the full ambient product in (30) has exact optimal
parameter \(3N+B\), even against coupled barriers.  Passing to the intrinsic
aggregate cone saves exactly \(N\), but no more.  Consequently, if all
\(N\) input pairs and \(B\) outputs are retained, positive epigraph
aggregation can improve the usual parameter-driven short-step iteration
factor by at most

\[
 \sqrt{\frac{3N+B}{2N+B}}<\sqrt{\frac32}.                   \tag{31}
\]

Thus an asymptotic iteration-count improvement must also compress input
degrees of freedom or exploit a different complexity mechanism; merely
sharing or aggregating output epigraphs cannot provide one.  Formula (31)
compares standard \(\sqrt\vartheta\)-based upper bounds, not realized
iteration counts or an oracle lower bound.

The intrinsic barrier does not require a dense unstructured Hessian.  Write
\(s=z-A\phi(x,y)>0\), let \(R=\operatorname{Diag}(s_b^{-1})\), and let
\(J\in\mathbb R^{B\times2N}\) be the Jacobian of \(A\phi\), with the
\(i\)-th two-coordinate block of row \(b\) equal to
\(A_{bi}\nabla\phi_i^T\).  If \(p=(x_1,y_1,\ldots,x_N,y_N)\), then

\[
 \nabla^2F_A=
 \begin{bmatrix}G+J^TR^2J&-J^TR^2\\-R^2J&R^2\end{bmatrix}
 =
 \begin{bmatrix}I&-J^T\\0&I\end{bmatrix}
 \begin{bmatrix}G&0\\0&R^2\end{bmatrix}
 \begin{bmatrix}I&0\\-J&I\end{bmatrix},                  \tag{32}
\]

where \(G\) is block diagonal with positive-definite \(2\times2\) blocks

\[
 G_i=\operatorname{Diag}(x_i^{-2},y_i^{-2})+
       \left(\sum_{b=1}^B\frac{A_{bi}}{s_b}\right)
       \begin{bmatrix}x_i^{-1}&-y_i^{-1}\\
                       -y_i^{-1}&x_i/y_i^2\end{bmatrix}.     \tag{33}
\]

Hence a cone-Hessian solve uses two multiplications by \(A\) or \(A^T\),
\(N\) independent \(2\times2\) solves, and diagonal scaling: exact
unit-cost exact-arithmetic complexity
\(O(N+B+\operatorname{nnz}A)\).  This factorization does
not itself solve a surrounding constrained Newton system, but it shows that
the optimal parameter reduction in (28) need not destroy sparse Hessian
access.

## Sparse-QIPM implication and scope

If a sparse compiler outputs \(R\) independent exponential-cone factors,
then no choice of a nonseparable ambient barrier can reduce their parameter
contribution below \(3R\).  In particular, any separate geometric or
information-theoretic argument that forces \(R=\Omega(g)\) factors forces
\(\vartheta=\Omega(3g)\) with the sharp factor-three accounting.  Standard
short-step upper bounds therefore use the unavoidable ambient quantity
\(\sqrt{3R}\), rather than a potentially improvable value between
\(\sqrt{2R}\) and \(\sqrt{3R}\).

This is a barrier-parameter theorem, not an iteration lower bound for all
interior-point algorithms.  It also concerns the displayed ambient product.
It does not rule out replacing that product by a different cone lift or by a
single compiled cone, nor does it include source-query, derivative-
evaluation, conditioning, or output costs.

## Literature boundary

- [Fawzi and Saunderson, *Optimal Self-Concordant Barriers for Quantum
  Relative Entropies*](https://doi.org/10.1137/22M1500216), Section 3.3,
  reproduce Nesterov's recession-direction theorem, prove the hypograph
  lower bound, and thereby prove optimal parameter three for the scalar
  relative-entropy/exponential cone.  Their main matrix cones have optimal
  parameters \(2n+m\) or \(n_1+n_2+m\), as appropriate.  The \(3R\)
  exponential-product certificate can also be obtained directly from
  their general Theorem 3.10 by taking input cone
  \(\mathbb R_{++}^{2R}\), output cone \(\mathbb R_+^R\), and the
  coordinatewise map
  \((v_j,w_j)_j\mapsto(v_j\log(w_j/v_j))_j\).  Tensorization is therefore
  a reusable reformulation of the published certificate method, not a new
  lower-bound technique.
- [Coey, Kapelevich, and Vielma, *Performance Enhancements for a Generic
  Conic Interior Point Algorithm*](https://doi.org/10.1007/s12532-022-00226-0)
  record the \(2d+1\) relative-entropy-cone barrier used in (24a).
- [Chen and Goulart, *An Efficient Implementation of Interior-Point Methods
  for a Class of Nonsymmetric Cones*](https://doi.org/10.1007/s10957-024-02573-5)
  exploit sparse and low-rank Hessian representations for ordinary relative-
  entropy cones.  Their work is the closest implementation precedent for
  (32), but it uses the one-output cone and does not state the arbitrary
  positive-output law (28) or the iteration-compression ceiling (31).
- [He, Saunderson, and Fawzi, *Interior Point Methods for Structured Quantum
  Relative Entropy Optimization Problems*](https://doi.org/10.1007/s12532-025-00296-w)
  absorb positive input-side maps into tailored QRE cones, prove optimal
  parameters even for singular maps, and exploit the resulting Hessian
  structure.  This is close conceptual precedent for combining cone
  aggregation with structured linear algebra, though it does not state the
  classical multi-output law (28)--(33).
- [Nesterov, *Constructing Self-Concordant Barriers for Convex
  Cones*](https://optimization-online.org/2006/04/1358/) gives the
  compatible parameter-\((n+1)\) barrier (14c) for weighted geometric-mean
  hypographs, as well as the parameter-three exponential-cone barrier.
- [Hildebrand, *A Lower Bound on the Barrier Parameter of Barriers for
  Convex Cones*](https://doi.org/10.1007/s10107-012-0576-1) gives the
  projective cross-ratio theorem used in (16)--(19).  His Section 6 explains
  how classical Nesterov--Nemirovskii boundary lower bounds arise as special
  cases, but does not give the exponential-product calculation above.
- The standard Cartesian-product rule says that **sums** of barriers have
  additive parameters.  That is only the upper bound in (2).  Targeted
  searches for optimal-parameter additivity under arbitrary coupled
  barriers, tensorization of the recession certificate, and an exact
  \(3R\) lower bound for products of exponential cones found no explicit
  statement.  Since the result is nevertheless an immediate specialization
  of the published general certificate theorem, only the explicit product
  formulation and mixed-product packaging are plausible novelty; priority
  requires specialist review.  The mathematical novelty of the bare
  \(3R\) formula is low; its value here is the exact coupled-barrier
  accounting and the fixed-product-versus-aggregate separation.
  Targeted searches also found no explicit statement of (28)--(31), but
  these formulas are short consequences of the same published compatibility
  and lower-bound machinery, so their priority likewise requires specialist
  review.

## Independent audit record

Two hostile audits verified the coordinate permutation and closure face, all
certificate feasibility and noninteriority conditions, the order of the
limits, and the parameter convention in Nesterov's theorem.  They also
verified the product-interior argument for arbitrary coupled barriers, the
cross-ratio coefficient calculation, and the matrix/QRE restriction and
product extensions.  No mathematical defect was found in (2).  The audits
did weaken the priority claim: Theorem 3.10 of Fawzi--Saunderson already
contains the product certificate after a direct choice of product input and
output cones, although no explicit statement of (2) was found in the
targeted literature search.

A further hostile audit checked (27)--(33), including zero or duplicate rows
and zero columns of \(A\), the closed projection, the exact ambient-product
parameter, and every Hessian sign and block.  It found no defect.  It also
identified He--Saunderson--Fawzi as close conceptual precedent and confirmed
that (28)--(33) should be presented as an apparently unstated specialization
and formulation consequence, not as a new barrier construction.
