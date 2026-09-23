# A conditioned approximate curvature-capacity theorem

Status: Proved; literature-screened; independently audited  
Started: 2026-09-04  
Paper status: Not incorporated  
Confidence: Medium-high

## Summary

The exact curvature-capacity theorem is quantitatively stable if the cone
factors over one fixed tangent stencil do not move too far relative to their
nearly complementary base factors.  The result below is completely
finite-dimensional and uses no derivatives.  It gives an explicit,
checkable condition under which an additive approximation to the Euclidean
ball slack still forces

\[
        N-1\leq \sum_i (m_i-2)_+.                 \tag{1}
\]

Hausdorff or multiplicative approximation of the projected body alone does
**not** imply the factor-conditioning condition used here.  A sharp
two-point orthant example at the end shows why small slack error and bounded
factor values are insufficient.  Thus this note makes no unconditional
claim for arbitrary nonsmooth or ill-conditioned approximate lifts.

## Finite-stencil theorem

Put \(r=N-1\), choose \(0<h<1\), and define points on the unit sphere by

\[
 v_0=e_N,\qquad
 v_j=h e_j+\sqrt{1-h^2}\,e_N\quad(1\leq j\leq r).
                                                               \tag{2}
\]

Let \(K_i\subset E_i\) be finite-dimensional proper cones,
\(\dim E_i=m_i\), and suppose maps on this finite set satisfy

\[
 A_i(v_j)\in K_i,\qquad B_i(v_j)\in K_i^*,
\]

and

\[
 \left|\sum_i\langle A_i(v_j),B_i(v_\ell)\rangle
             -(1-\langle v_j,v_\ell\rangle)\right|\leq\epsilon
       \quad(0\leq j,\ell\leq r).                 \tag{3}
\]

For each block write

\[
 a_i=A_i(v_0),\quad b_i=B_i(v_0),
\]

and let \(X_i,Y_i:E_i\leftarrow\mathbb R^r\) be the matrices with columns

\[
 X_i e_j=A_i(v_j)-a_i,\qquad
 Y_i e_j=B_i(v_j)-b_i.                              \tag{4}
\]

Set

\[
 \tau_h=1-\sqrt{1-h^2},\qquad H=\tau_h+\epsilon.    \tag{5}
\]

For a block with \(a_i,b_i\ne0\), define

\[
 \begin{split}
 \mathcal E_i={}&
  {\sqrt r H\over\|b_i\|}\,\|Y_i\|_{\rm op}
 +{\sqrt r H\over\|a_i\|}\,\|X_i\|_{\rm op}\\
 &+{\epsilon\over\|a_i\|\|b_i\|}
       \|X_i\|_{\rm op}\|Y_i\|_{\rm op}.
                                                               \tag{6}
 \end{split}
\]

If \(a_i=0\) or \(b_i=0\), instead put

\[
       \mathcal E_i=\|X_i\|_{\rm op}\|Y_i\|_{\rm op}.        \tag{7}
\]

### Theorem

If

\[
       4r\epsilon+\sum_i\mathcal E_i<h^2,            \tag{8}
\]

then (1) holds.  Consequently, if \(d\geq3\) and every non-ray factor has
dimension at most \(d\), then its number \(k_+\) satisfies

\[
       k_+\geq\left\lceil{N-1\over d-2}\right\rceil. \tag{9}
\]

The count in (9) is the number of non-ray factors.  Ray factors can remain
in a formulation, but contribute zero to (1).

## Proof

Suppress the block index.  Let

\[
 \theta=\langle a,b\rangle,qquad
 p=X^Tb,qquad q=Y^Ta.                               \tag{10}
\]

All cone-pairing summands in (3) are nonnegative.  Applying (3) at
\((v_0,v_0)\), \((v_j,v_0)\), and \((v_0,v_j)\) therefore gives, block by
block,

\[
 0\leq\theta\leq\epsilon,qquad
 \|p\|_2\leq\sqrt r H,qquad
 \|q\|_2\leq\sqrt r H.                             \tag{11}
\]

Indeed, both numbers whose difference is a coordinate of \(p\) lie in
\([0,H]\), and similarly for \(q\).

Assume first that \(m\geq2\) and \(a,b\ne0\).  Orthogonally project the
columns of \(X\) to \(b^\perp\), and those of \(Y\) to \(a^\perp\):

\[
 X_0=P_{b^\perp}X,qquad Y_0=P_{a^\perp}Y.           \tag{12}
\]

Then

\[
 \|X-X_0\|_{\rm op}={\|p\|_2\over\|b\|},\qquad
 \|Y-Y_0\|_{\rm op}={\|q\|_2\over\|a\|}.         \tag{13}
\]

The pairing between \(b^\perp\) and \(a^\perp\) has \(m-2\) singular
values equal to one and at most one further nonzero singular value, equal
to

\[
          {\langle a,b\rangle\over\|a\|\|b\|}.      \tag{14}
\]

This follows by restricting the orthogonal projection
\(P_{b^\perp}\) to \(a^\perp\): it is the identity on
\(a^\perp\cap b^\perp\), while its remaining singular value is the cosine
of the angle between \(a\) and \(b\).  It follows from (11)--(14) that
\(X^TY\) is within operator norm \(\mathcal E_i\) of a matrix of rank at
most \((m-2)_+\).  One may see this directly from

\[
 \|X^TY-X_0^TY_0\|_{\rm op}
 \leq {\|p\|_2\over\|b\|}\|Y\|_{\rm op}
      +\|X\|_{\rm op}{\|q\|_2\over\|a\|},          \tag{15}
\]

followed by deleting the last singular direction in (14).  If \(m=1\) and
\(a,b\ne0\), then \(a^\perp=b^\perp=\{0\}\), so \(X_0=Y_0=0\) and (15)
directly gives the required rank-zero approximant with the first two terms
of (6).  When \(a=0\) or \(b=0\), the zero matrix is again a rank-zero
approximant and (7) is the trivial product bound.  Thus ray and zero blocks
contribute no rank.

Let \(\widetilde D\) be the mixed-difference matrix of the left side of
(3):

\[
 \widetilde D_{j\ell}=widetilde s(v_j,v_\ell)
 -\widetilde s(v_j,v_0)-\widetilde s(v_0,v_\ell)
 +\widetilde s(v_0,v_0).
\]

By bilinearity,

\[
             \widetilde D=\sum_iX_i^TY_i.           \tag{16}
\]

For the Euclidean-ball slack its exact value is

\[
 D_*=-h^2I_r-\tau_h^2\mathbf1\mathbf1^T.            \tag{17}
\]

All singular values of \(D_*\) are at least \(h^2\).  Four uses of (3)
per entry give

\[
       \|\widetilde D-D_*\|_{\rm op}\leq4r\epsilon. \tag{18}
\]

The sum of the blockwise low-rank approximants has rank at most
\(c=\sum_i(m_i-2)_+\), and (6)--(7), (15), and (18) put it within distance
at most \(4r\epsilon+\sum_i\mathcal E_i\) of \(D_*\).  If \(c<r\), the
Eckart--Young theorem says that every rank-\(c\) matrix is at operator-norm
distance at least \(\sigma_{c+1}(D_*)\geq h^2\) from \(D_*\), contrary to
(8).  This proves the theorem.

## A simpler sufficient conditioning hypothesis

Suppose all blocks have nonzero base factors and, for constants \(\rho,L>0\),

\[
 \|a_i\|,\|b_i\|\geq\rho,qquad
 \|X_i\|_{\rm op},\|Y_i\|_{\rm op}\leq Lh.          \tag{19}
\]

If \(\epsilon\leq h^2\), then \(\tau_h\leq h^2\) and (8) follows from

\[
 {4r\epsilon\over h^2}
 +{4k\sqrt r Lh\over\rho}
 +{k\epsilon L^2\over\rho^2}<1.                    \tag{20}
\]

Thus a uniformly conditioned family has the exact curvature-capacity lower
bound for every sufficiently accurate approximation, provided (19) holds
uniformly on the corresponding shrinking stencils.  Balancing the first
two terms suggests the cubic-root scale
\(h\asymp(\sqrt r\,\epsilon\rho/(kL))^{1/3}\), up to absolute constants,
provided the resulting stencil lies inside the region on which (19) holds.

## From a multiplicative ball approximation to (3)

Let \(C_\eta\) be a full-dimensional convex body with

\[
 (1-\eta)B_2^N\subseteq C_\eta\subseteq(1+\eta)B_2^N,
\qquad 0<\eta<1.                                   \tag{21}
\]

The same sandwich follows from the centered Hausdorff bound
\(d_H(C_\eta,B_2^N)\leq\eta\), because Hausdorff distance between compact
convex bodies is the uniform distance between their support functions.

Its polar satisfies

\[
 (1+\eta)^{-1}B_2^N\subseteq C_\eta^\circ
 \subseteq(1-\eta)^{-1}B_2^N.                       \tag{22}
\]

Choose radial boundary points \(x(v)=\rho_C(v)v\) and
\(y(v)=\rho_{C^\circ}(v)v\).  Their slack obeys

\[
 \left|1-\langle x(v),y(w)\rangle
       -(1-\langle v,w\rangle)\right|
 \leq {2\eta\over1-\eta}.                          \tag{23}
\]

After minimal-face reduction, any exact proper-cone lift of \(C_\eta\)
gives a cone factorization on all the radial boundary points needed here.
Concretely, for each \(x(v)\), choose a primal lift (for example, the
minimum-norm lift).  For each supporting functional \(y(v)\), conic dual
attainment after minimal-face reduction supplies a dual factor, and the
pairing of these factors is exactly \(1-\langle x(v),y(w)\rangle\).
This lift-derived selection is important because radial boundary points
need not be extreme, whereas some standard formulations index the slack
operator only by extreme points.  Hence (3) holds with

\[
             \epsilon={2\eta\over1-\eta}.           \tag{24}
\]

Therefore (8), or the transparent sufficient condition (20), turns a
multiplicative body approximation into the block-count lower bound (9).
The substantive extra hypothesis is conditioning of the selected primal
and dual cone factors; (21) by itself does not supply it.

## Rigorous obstruction to an unconditioned discrete argument

Even bounded factor values and vanishing additive slack error do not force
a two-dimensional proper-cone factor to have approximately zero mixed
curvature.

Take the two sphere points \(v_0,v_1\) from (2) with \(r=1\), and put
\(\tau=1-\sqrt{1-h^2}\).  For \(\alpha>0\), set
\(\beta=\tau/\alpha\).  In the self-dual cone \(K=\mathbb R_+^2\), define

\[
\begin{array}{c|cc}
 &v_0&v_1\\ \hline
A_1&(\alpha,\alpha)&(0,\alpha+\beta)\\
B_1&(\alpha,\alpha)&(\alpha+\beta,0).
\end{array}                                          \tag{25}
\]

The resulting nonnegative kernel has values

\[
 \widetilde s_{00}=2\alpha^2,qquad
 \widetilde s_{10}=\widetilde s_{01}=\tau+\alpha^2,
 \qquad \widetilde s_{11}=0.                        \tag{26}
\]

The true ball-slack values are \(0,\tau,\tau,0\), so the uniform error
tends to zero with \(\alpha\).  Nevertheless the mixed difference is
exactly

\[
 \widetilde s_{11}-\widetilde s_{10}-\widetilde s_{01}
 +\widetilde s_{00}=-2\tau=-h^2-\tau^2,             \tag{27}
\]

the full ball value.  Yet \((m-2)_+=0\).

This is not merely an artifact of unbounded coordinates.  Apply the
orthant automorphism

\[
 D=\operatorname{diag}\!\left(\sqrt{\beta/\alpha},
                               \sqrt{\alpha/\beta}\right)
\]

to primal factors and \(D^{-1}\) to dual factors.  Pairings are unchanged,
and every displayed factor remains bounded as \(\alpha\downarrow0\)
(indeed, the largest coordinates tend to \(\sqrt\tau\)).  What degenerates
is relative conditioning: the base primal and dual factors become nearly
complementary while the increments remain comparable to their nonvanishing
coordinates.  Correspondingly, the left side of (20) does not become
small.

The example proves that a proposed finite-difference proof cannot replace
(6) by additive slack accuracy plus absolute boundedness alone. It does not
itself construct a global low-block lift approximating \(B_2^N\). The
companion [approximate-ball note](2026-09-04-approximate-ball-curvature-stability.md)
records the global boundary: arbitrarily accurate circumscribed polytopes
have ray-only lifts, but their number of rays grows with accuracy. Thus no
unconditional metric theorem can preserve the non-ray curvature sum;
meaningful remaining variants must also control total factor complexity or
exclude singular switching. Nonsmooth approximants show the mechanism:
curvature can concentrate at singular contacts while the active factor
stratum changes on a shrinking scale.

## Novelty boundary and next questions

The proof is an elementary quantitative version of the tangent-pairing
argument, based on orthogonal projections and Eckart--Young.  No claim is
made that this exact inequality or its constants are new pending specialist
review.  The closest targeted source found was Gouveia--Parrilo--Thomas,
“Approximate cone factorizations and lifts of polytopes,” *Mathematical
Programming* 151 (2015), DOI
[10.1007/s10107-014-0848-z](https://doi.org/10.1007/s10107-014-0848-z).
That paper rigorously transfers approximate slack factorizations to inner
and outer approximations (and conversely in its polyhedral setting), but it
does not give a local curvature-capacity or dimension-minus-two stability
bound.  Basu--Dinitz--Li, “Computing Approximate PSD Factorizations,”
APPROX/RANDOM 2016, DOI
[10.4230/LIPIcs.APPROX-RANDOM.2016.2](https://doi.org/10.4230/LIPIcs.APPROX-RANDOM.2016.2),
studies algorithms for approximate PSD matrix factorization under bounded
factor regions, not curvature loss at near-complementary cone factors.

The useful content here is the explicit separation between:

1. multiplicative approximation, which gives a uniformly accurate slack
   kernel;
2. relative factor conditioning, which is what preserves the loss of two
   curvature directions per proper cone block.

The main open question left by this note is whether a global argument can
replace factor conditioning after imposing a uniform bound on total factor
count and dimension, or whether genuinely ill-conditioned products of a
fixed number of bounded-dimensional blocks can converge to a Euclidean ball.
