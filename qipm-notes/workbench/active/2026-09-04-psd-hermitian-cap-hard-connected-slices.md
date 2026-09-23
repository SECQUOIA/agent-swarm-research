# Exact cap-hard connected slices of PSD and Hermitian products

Status: Proved and independently audited; headline
frontier subsumed by a stronger audited local theorem  
Started: 2026-09-04  
Paper status: Not incorporated  
Confidence: High on the algebraic and barrier frontiers

## Main theorem

Let \(\mathbb K\in\{\mathbb R,\mathbb C,\mathbb H\}\), put
\(\beta=\dim_{\mathbb R}\mathbb K\in\{1,2,4\}\), let \(k,L\geq2\), and
write
\[
 \mathcal P_k(\mathbb K)=\{X=X^*\succeq0\},\qquad
 D_{\mathbb K}(k)=k+{\beta k(k-1)\over2}.                     \tag{1}
\]
Thus \(D_{\mathbb R}(k)=k(k+1)/2\), \(D_{\mathbb C}(k)=k^2\), and
\(D_{\mathbb H}(k)=k(2k-1)\).  Put \(D=D_{\mathbb K}(k)\) and
\[
                         A_k=\mathbf1\mathbf1^*-I_k.             \tag{2}
\]
Thus \(A_k\) has zero diagonal, trace zero, and signature \((1,k-1)\).
All quaternionic trace pairings below mean
\(\operatorname{Re}\operatorname{tr}\), the Euclidean-Jordan trace
pairing; for this real-entry Hermitian \(A_k\), the displayed scalar is
already real.
Consider the codimension-two affine slice
\[
 \boxed{
 Z_{\mathbb K;k,L}=\left\{(X_1,\ldots,X_L)\in
       \mathcal P_k(\mathbb K)^L:
       \sum_i\operatorname{tr}X_i=1,\quad
       \sum_i\operatorname{tr}(A_kX_i)=0\right\}.}             \tag{3}
\]
Identify its affine hull with \(\mathbb R^N\), where
\[
                              N=DL-2.                            \tag{4}
\]
Then:

1. \(Z_{\mathbb K;k,L}\) is compact, has full relative Slater, and has a
   path-connected extreme-point set.
2. For its full slack operator, among factorizations through products of
   arbitrary nonzero proper cones of real dimension at most \(D\),
   \[
       \boxed{L_{\min}=L={N+2\over D},\qquad
              M_{\min}=DL=N+2.}                                \tag{5}
   \]
   This permits arbitrary splitting of slack rows and discontinuous factor
   maps.
3. The optimal barrier parameter on the ambient product cone is \(kL\),
   attained by the standard product log-determinant barrier.  Its
   restriction to (3) has exact parameter \(kL-1\), and this is optimal
   even among arbitrary coupled barriers directly on the slice:
   \[
       \boxed{\nu_{\rm opt,amb}=\nu_{\rm logdet,amb}=kL,\qquad
              \nu_{\rm std,slice}=\nu_{\rm opt}(Z_{\mathbb K;k,L})
                 =kL-1.}                                      \tag{6}
   \]

For \(\mathbb K=\mathbb R,k=2\), this is a linearly transformed version of
the Lorentz family \(Z_{1,L}\subset Q_3^L\).  The cases \(k\geq3\) are
genuinely higher-rank PSD examples.  The complex \(k=2\) cone is the
four-dimensional Lorentz cone, and the quaternionic \(k=2\) cone is the
six-dimensional Lorentz cone.  Complex and quaternionic \(k\geq3\) are
again higher rank.

## 1. Slater, dimension, and compactness

The two affine functionals in (3) are independent.  The point
\[
                         X_i^0={I_k\over kL}                     \tag{7}
\]
is positive definite and satisfies both equations because
\(\operatorname{tr}A_k=0\).  Thus the slice has full relative Slater and
dimension \(DL-2\).  Trace normalization and positivity give
\(0\preceq X_i\preceq I_k\), so the slice is compact.

## 2. Exact extreme points

For a nonzero vector \(v\in\mathbb K^k\), define its moment
\[
                    c([v])={v^*A_kv\over v^*v}.                  \tag{8}
\]
The projective class records the corresponding normalized rank-one ray.
The minimal face of a rank-\(r\) matrix in \(\mathcal P_k(\mathbb K)\) has
real span dimension
\[
                     D_{\mathbb K}(r)=r+{\beta r(r-1)\over2}.
\]
In particular, rank two already costs \(2+\beta>2\).  Apply the elementary
affine-slice criterion
\[
 z\in\operatorname{ext}(K\cap\{\mathcal Az=b\})
 \quad\Longleftrightarrow\quad
 \ker\mathcal A\cap\operatorname{span}F_K(z)=\{0\}.             \tag{9}
\]
Since (3) uses two independent equations, (9) rules out every block of rank
at least two and every point with at least three nonzero blocks.

After normalizing each active rank-one ray to trace one, its column under
the two slice functionals is \((1,c([v]))\).  Hence the extreme points are
exactly:

- one nonzero rank-one block whose projective ray obeys \(c([v])=0\); or
- two nonzero rank-one blocks on rays with moments of opposite signs, with
  their two positive trace weights uniquely chosen to have total trace one
  and weighted moment zero.

Indeed, two columns \((1,c_1),(1,c_2)\) are independent precisely when
\(c_1\ne c_2\), and positive feasibility of a zero weighted mean forces
\(c_1c_2<0\).  This also proves that no listed point is omitted.

## 3. Connectedness without a selection hypothesis

In an eigenbasis of \(A_k\), its quadratic form is
\[
                  (k-1)|a|^2-\|b\|^2,\qquad
                  (a,b)\in\mathbb K\oplus\mathbb K^{k-1}.       \tag{10}
\]
On a zero ray, \(a\ne0\).  Quotienting by right multiplication with a
nonzero scalar and choosing the representative with \(a=1\) identifies
the projective zero-ray set with
\[
                       S^{\beta(k-1)-1}.
\]
Thus it is \(S^{k-2}\), \(S^{2k-3}\), or \(S^{4k-5}\) over
\(\mathbb R,\mathbb C,\mathbb H\), respectively.  It is path connected
except for the real \(k=2\) case, where it consists of two points.

Every positive- or negative-moment ray can be joined within the closure of
its sign region to a zero-moment ray: in (10), scale \(|a|\) relative to
\(\|b\|\) until equality holds (if \(a=0\), first introduce an arbitrarily
small real positive \(a\)-component).  Along such a path, the unique positive
weights of a two-block extreme point vary continuously.  Sending either
moment to zero sends the opposite block weight to zero, so every two-block
extreme point is path connected to a one-block extreme point.

For completeness, this bridge can be written without making any
continuous selection.  A zero ray has a representative
\((1,\sqrt{k-1}\,u)\), with \(\|u\|=1\).  Replacing its second component
by \(\lambda\sqrt{k-1}\,u\) realizes every moment
\(c\in(-1,k-1)\), where
\[
            \lambda^2={k-1-c\over (k-1)(1+c)}.
\]
Given prescribed zero rays in two different blocks, fix
\(0<c_0<1\) and use the moments
\(c_+(t)=tc_0\) and \(c_-(t)=-(1-t)c_0\).  The trace weights
\[
       w_+(t)={-c_-(t)\over c_+(t)-c_-(t)},\qquad
       w_-(t)={c_+(t)\over c_+(t)-c_-(t)}
\]
are exactly \((w_+(t),w_-(t))=(1-t,t)\), so they extend to
\((1,0)\) and \((0,1)\) at the two endpoints.
This is an explicit path of extreme points between the prescribed
one-block points.

For two distinct block labels, one can connect arbitrary one-block zero
rays by perturbing the first ray into the positive region and the second
into the negative region, using the unique zero-mean trace weights, and
letting the two perturbations vanish at opposite endpoints.  When the
zero-ray set is connected, this and within-block motion connect all
one-block points.  In the exceptional real \(k=2\) case, the presence of
\(L\geq2\) blocks connects the two zero rays in one label by going through
any second label.  Thus \(\operatorname{ext}Z_{\mathbb K;k,L}\) is path
connected in every stated case.

This proof concerns the geometry of the displayed slice.  It does not
choose or regularize factors of a later slack factorization.

## 4. Exact arbitrary-dictionary factor-cap frontier

Translate the slice by its Slater point and identify its affine hull with
\(\mathbb R^N\).  The full slack operator of any full-dimensional
\(N\)-body has ordinary function rank \(N+1\).  Therefore every conic
factorization through a product \(K'=\prod_{j=1}^{L'}K'_j\) has
\[
                     M':=\sum_j\dim K'_j\geq N+1.               \tag{11}
\]
Suppose equality held.  Minimum-dimension bilinear-factorization rigidity
would identify \(K'\) linearly with the homogenization cone of the body.
The projective extreme-ray space of a product of \(L'\) nonzero proper
cones is the clopen disjoint union of its \(L'\) factor ray spaces, whereas
the projective extreme rays of the homogenization are homeomorphic to the
connected set \(\operatorname{ext}Z_{\mathbb K;k,L}\).  Hence equality in
(11) forces \(L'=1\).

Under the cap \(\dim K'_j\leq D\), however, one factor cannot have dimension
\(N+1=DL-1>D\).  Thus equality in (11) is impossible and integrality gives
\[
                           M'\geq N+2=DL.                        \tag{12}
\]
Since \(M'\leq DL'\), it follows that \(L'\geq L\).  The displayed lift
through \(\mathcal P_k(\mathbb K)^L\) attains both inequalities.  Nothing
in this argument assigns a slack row to one factor, assumes continuous
factor maps, or restricts the competing proper cones beyond their real
dimension cap.

## 5. Exact restricted standard barrier

On the ambient product cone use
\[
                         \Phi(X)=-\sum_{i=1}^L\log\det X_i.      \tag{13}
\]
Here \(\det\) is the determinant of the corresponding Euclidean Jordan
algebra (the Moore determinant over \(\mathbb H\)).  Its
logarithmic-homogeneity degree and barrier parameter are both \(kL\) over
all three division algebras.  Let \(H=\nabla^2\Phi\),
\(g=\nabla\Phi\), and let \(a(X)=\sum_i\operatorname{tr}X_i\).  Blockwise,
\[
 H_i=P(X_i^{-1}),\qquad H^{-1}g=-X,
 \qquad H_i^{-1}[I_k]=P(X_i)[I_k]=X_i^2,                       \tag{14}
\]
where \(P\) is the quadratic representation.  For real and complex
Hermitian matrices, \(P(X)[U]=XUX\); (14) is the standard
Euclidean-Jordan formula and therefore also covers quaternionic Hermitian
matrices without assuming that matrix entries commute.
Consequently, on the trace-one slice,
\[
 a^TH^{-1}g=-1,\qquad
 a^TH^{-1}a=\sum_i\operatorname{tr}X_i^2
       \leq\sum_i(\operatorname{tr}X_i)^2\leq1.                \tag{15}
\]
Projecting the gradient to the tangent space \(\ker a\) gives squared
dual norm
\[
 kL-{1\over\sum_i\operatorname{tr}X_i^2}\leq kL-1.             \tag{16}
\]
Restriction to the second tangent equation can only decrease this norm.
Affine restriction preserves self-concordance and barrier blowup, so
\(\nu_{\rm std,slice}\leq kL-1\).

For the reverse inequality, choose a unit vector \(v\) with
\(v^*A_kv=0\), let \(V\) be the one-block endpoint with block \(vv^*\),
and follow the chord from (7) to \(V\).  As \(\theta\uparrow1\), the endpoint
block determinant has a zero of order \(k-1\), while every other block
determinant has a zero of order \(k\).  Hence
\[
 \Phi((1-\theta)X^0+\theta V)
       =-(kL-1)\log(1-\theta)+O(1).                              \tag{17}
\]
The directional gradient/Hessian quotient tends to \(kL-1\), proving
\[
                         \nu_{\rm std,slice}=kL-1.               \tag{18}
\]

The ambient value is itself intrinsic, not merely the cost of this
particular barrier.  Restrict any self-concordant barrier on
\(\mathcal P_k(\mathbb K)^L\) to the diagonal subspace.  This gives a
barrier on \(\mathbb R_{++}^{kL}\), because every point on the orthant
boundary maps to a singular matrix in at least one block.  The orthant
lower bound is \(kL\).  The product log-determinant barrier attains it, so
\(\nu_{\rm opt,amb}=kL\).

## 6. Exact intrinsic arbitrary-barrier parameter

The zero diagonal of \(A_k\) is the key extra feature.  Restrict (3) to
matrices diagonal in the standard basis:
\[
                X_i=\operatorname{Diag}(p_{i1},\ldots,p_{ik}).   \tag{19}
\]
The moment equation becomes automatic, and the remaining domain is
\[
                  p_{ij}>0,\qquad \sum_{i,j}p_{ij}=1,           \tag{20}
\]
the relative interior of a simplex of dimension \(kL-1\).  Every facet
\(p_{ij}=0\) consists of matrices on the boundary of at least one PSD
factor, and therefore lies in the relative boundary of (3).  The
restriction of every self-concordant barrier on the body is consequently a
barrier on this simplex with no larger parameter.

The Nesterov--Nemirovskii simple-vertex lower bound says that every barrier
on an \(n\)-simplex has parameter at least \(n\).  Taking \(n=kL-1\) gives
\[
                         \nu_{\rm opt}(Z_{\mathbb K;k,L})
                              \geq kL-1.                         \tag{21}
\]
Together with (18), this proves the intrinsic equality in (6).  It is a
statement about barriers directly on the compact affine slice, not about a
different fiber-extended formulation of the same projection.

There is one standard transfer that is safe.  If an affine extended
formulation of this slice has nonempty bounded fibers, exact partial
minimization of any \(\nu\)-self-concordant barrier over each fiber produces
a \(\nu\)-barrier on the slice.  Hence every such bounded-fiber lift also
has \(\nu\geq kL-1\).  This argument does not cover arbitrary unbounded
fibers.

## 7. Interpretation and limits

The family simultaneously saturates three different ledgers:
\[
 \begin{array}{c|c}
 \text{resource}&\text{exact value}\\ \hline
 \text{body dimension}&DL-2\\
 \text{minimum capped factor count}&L\\
 \text{minimum capped total cone dimension}&DL=N+2\\
 \text{optimal ambient (and product-logdet) parameter}&kL\\
 \text{restricted and intrinsic barrier parameter}&kL-1.
 \end{array}                                                     \tag{22}
\]
It shows that the Lorentz cap-hard phenomenon is not rank-two-specific.
Higher PSD rank changes the barrier cost per factor from two to \(k\), but
the same codimension-two connected-extreme mechanism leaves only the sharp
one-unit ambient-dimension gap and removes exactly one unit of barrier
parameter.

### Same storage frontier, different barrier frontier

The distinction is exact at matched real cone dimension.  Fix one of the
Hermitian dimensions \(D=D_{\mathbb K}(k)\), and compare this family with
the Lorentz slice built from \(Q_D^L\).  Both bodies have dimension
\(DL-2\), and under the dimension cap \(D\) both have
\[
                    L_{\min}=L,\qquad M_{\min}=DL.
\]
Nevertheless, their optimal direct-slice barrier parameters are
\[
              kL-1\quad\hbox{and}\quad 2L-1,
\]
respectively.  The exact ratio is \((kL-1)/(2L-1)\), which is
\(\Theta(k)=\Theta_\beta(\sqrt D)\).  Thus the corresponding
\(\sqrt{\nu}\) short-step iteration coefficients differ by
\[
             \sqrt{{kL-1\over2L-1}}=\Theta_\beta(D^{1/4}).
\]
This compares two different cap-hard bodies; it is not evidence that the
Hermitian body itself has a Lorentz lift.  It proves instead that factor
count and total cone dimension alone do not determine even the optimal
direct-body barrier scale.

The factorization lower bound is for the full slack operator.  It does not
follow for a selected finite set of support rows.  The intrinsic barrier
equality applies to the displayed slice; it does not claim that every other
lift realizing its projection has barrier parameter at least \(kL-1\).

## Relation to the stronger local theorem

The resource frontier here is a special equal-type case of
[`2026-09-04-hermitian-balance-slice-sharp-frontier.md`](2026-09-04-hermitian-balance-slice-sharp-frontier.md),
which was developed independently and already proves the heterogeneous
real/complex/quaternionic theorem, bounded-fiber barrier transfer, and the
same exact cap frontier in the identical-type case.  That theorem uses
the balance matrix \(E_{12}+E_{21}\).  The present choice
\(A_k=\mathbf1\mathbf1^*-I\) is worth retaining as a transparent alternate
family: its isotropic projective locus is exactly the sphere
\(S^{\beta(k-1)-1}\), and the cross-factor extreme paths have the explicit
formula above.  No separate frontier or priority claim is attached to
this specialization.

## Audit targets

1. Check the rank-one extreme-point classification from the two-row
   minimal-face criterion over all three division algebras.
2. Check path connectedness, especially real \(k=2\), and the absence of a
   hidden continuous-selection assumption.
3. Check the full-slack equality-rigidity step for arbitrary split rows and
   discontinuous factor maps.
4. Check the cap arithmetic and the cases \(k=L=2\).
5. Check the Euclidean-Jordan inverse-Hessian projection in (14)--(16),
   including the quaternionic case, and determinant orders in (17).
6. Check that the diagonal section is a closed simplex section whose whole
   relative boundary lies in the body's relative boundary.

## Independent audit record

An independent hostile audit passed the quaternionic and
spherical-null-locus extension.  It rederived
\(D_{\mathbb H}(k)=k(2k-1)\), the rank-\(r\) face dimension
\(r(2r-1)\), and the identification of normalized rank-one rays with
\(\mathbb HP^{k-1}\).  It checked that a real orthogonal diagonalization of
\(A_k\) is quaternion-unitary and that right-scaling gives the unique
representative \((1,\sqrt{k-1}u)\), so the isotropic locus is
\(S^{4k-5}\) with no noncommutative quotient ambiguity.  The explicit
moment interpolation, weights \((1-t,t)\), and two-block extreme paths all
passed.  Finally, the Euclidean-Jordan inverse-Hessian identities, Moore
determinant endpoint orders, and diagonal orthant/simplex boundary
inheritance were independently checked and give exactly \(kL\) ambient
and \(kL-1\) normalized parameters.  No substantive defect was found.

## Literature boundary

The abstract extreme-point machinery is classical.  Dubins, [*On Extreme
Points of Convex Sets*](https://doi.org/10.1016/S0022-247X(62)80007-9),
implies, after trace normalization and intersection with the one remaining
balance hyperplane, that an extreme point is a convex combination of at most
two extreme points of the normalized product-cone base.  Pataki,
[*On the Rank of Extreme Matrices in Semidefinite Programs and the
Multiplicity of Optimal Eigenvalues*](https://doi.org/10.1287/moor.23.2.339),
is the standard real-PSD rank antecedent.  More generally, Henrion, Kružík,
and Weis, [*Extreme Points and Faces in the Moment
Problem*](https://arxiv.org/abs/2606.21391), Theorem 2.6, state a
smallest-face injectivity criterion which specializes in finite dimensions
to (9).  These sources cover the support-at-most-two/minimal-face principle,
but not the exact moment-sign classification or its path-connected gluing
over the real, complex, and quaternionic projective spaces.

The ambient barrier statement is also classical Euclidean-Jordan theory.
Güler and Tunçel, [*Characterization of the Barrier Parameter of Homogeneous
Convex Cones*](https://uwaterloo.ca/combinatorics-and-optimization/sites/default/files/uploads/documents/corr95.pdf),
prove that the optimal parameter of a homogeneous cone is its Siegel rank;
Cardoso and Vieira, [*On the Optimal Parameter of a Self-Concordant Barrier
over a Symmetric Cone*](https://doi.org/10.1016/j.ejor.2004.11.027), identify
the Carathéodory number with Euclidean-Jordan rank and treat the standard
generalized log-determinant barrier.  This includes quaternionic Hermitian
cones and gives the classical value \(kL\) on the product cone.  Gouveia,
Ito, and Lourenço, [*Minimal Hyperbolic Polynomials and Ranks of Homogeneous
Cones*](https://www.heldermann-verlag.de/jca/jca33-oa/jca2623-b.pdf), Section
4.2, again use this rank optimum when comparing homogeneous-cone and
hyperbolic barriers.  None of these ambient-cone results states that the
codimension-two compact slice (3) has exact arbitrary-barrier parameter
\(kL-1\).  The lower bound used here is instead the classical simplex bound
of Nesterov--Nemirovskii, *Interior-Point Polynomial Algorithms in Convex
Programming*, Proposition 2.3.6; the new work in the note is the
boundary-inheriting diagonal section and the matching restricted-logdet
calculation.

For lift complexity, Gouveia, Parrilo, and Thomas, [*Lifts of Convex Sets and
Cone Factorizations*](https://arxiv.org/abs/1111.3164), supply the general
slack-factorization framework.  Fawzi and Parrilo, [*Exponential Lower Bounds
on Fixed-Size PSD Rank and Semidefinite Extension
Complexity*](https://arxiv.org/abs/1311.2571), and Saunderson,
[*Limitations on the Expressive Power of Convex Cones without Long Chains of
Faces*](https://arxiv.org/abs/1902.06401), give strong product-cone
obstructions based respectively on fixed PSD block order and face-chain
complexity.  A particularly close PSD comparator is Soh and Chandrasekaran,
[*Fitting Tractable Convex Sets to Support Function
Evaluations*](https://doi.org/10.1007/s00454-020-00258-0), Proposition 2.6:
an order-\(q\) PSD cone cannot be represented by a lift through a product of
strictly smaller PSD cones.  Their result varies PSD order and does not
optimize total real cone dimension or factor count against a dictionary of
all proper cones.

A targeted classical and 2024--2026 primary-source screen did not locate the
combined statement for (3): codimension two, connected extreme-point set,
exact \(M_{\min}=N+2\) and \(L_{\min}=L\) under an arbitrary-proper-cone
dimension cap, and exact coupled-barrier value \(kL-1\).  The safe label is
**candidate explicit sharp synthesis**.  The extremality criterion, ambient
symmetric-cone barrier optimum, simplex lower bound, and general
lift/factorization machinery are not novel; priority for the combined family,
especially the quaternionic topological calculation and the separate local
minimum-dimension rigidity input, still needs specialist review.
