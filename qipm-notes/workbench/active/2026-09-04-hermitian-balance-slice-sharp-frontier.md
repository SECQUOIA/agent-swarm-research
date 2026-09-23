# Symmetric-cone balance slices: connected extremes, exact barriers, and cap hardness

Status: Fully proved and independently hostile-audited  
Started: 2026-09-04  
Paper status: Not incorporated  
Confidence: High for the audited classical, spin, and Albert statements

## Result

Let \(\mathbb F\in\{\mathbb R,\mathbb C,\mathbb H\}\), put
\(\delta=\dim_{\mathbb R}\mathbb F\), and let
\(\mathbb H_R(\mathbb F)_+\) be the cone of \(R\times R\)
\(\mathbb F\)-Hermitian positive semidefinite matrices. Its real dimension
and symmetric-cone rank are

\[
 d_{\mathbb F}(R)=R+\frac{\delta R(R-1)}2,\qquad
 \rho_{\mathbb F}(R)=R.                                \tag{1}
\]

Fix \(L\geq2\) types \((\mathbb F_i,R_i)\), with \(R_i\geq2\), and write
\[
 K_i=\mathbb H_{R_i}(\mathbb F_i)_+,\qquad
 d_i=d_{\mathbb F_i}(R_i),\qquad
 \rho=\sum_{i=1}^L R_i,\qquad M=\sum_{i=1}^L d_i.
\]
In each factor choose
\[
                 A_i=E_{12}+E_{21},\qquad
                 \ell_i(X)=\operatorname{Re}\operatorname{tr}(A_iX).
\]
Consider the balance cone and its normalized base

\[
\begin{aligned}
 \widehat Z&=\left\{(X_i)\in\prod_iK_i:
                         \sum_i\ell_i(X_i)=0\right\},\\
 Z&=\left\{X\in\widehat Z:\sum_i\operatorname{tr}X_i=1\right\}.
\end{aligned}                                          \tag{2}
\]

Then:

1. \(Z\) is a compact full-dimensional body in its affine hull,
   \(\dim Z=M-2\), and \(\operatorname{ext}Z\) is path-connected.
2. Every cone factor is indecomposable, membership-essential, and
   slack-visible.
3. Among arbitrary, possibly coupled self-concordant barriers,

   \[
      \boxed{\nu_{\rm opt}(\widehat Z)=\rho,\qquad
             \nu_{\rm opt}(Z)=\rho-1.}                 \tag{3}
   \]

   The standard product log-determinant barrier attains both values (with
   the Moore determinant in the quaternionic case).
4. Every bounded-fiber affine extended formulation of \(Z\), equipped
   with any coupled self-concordant barrier, has parameter at least
   \(\rho-1\).
5. In the identical-type case \(d_i=d\), \(R_i=R\), put
   \(N=dL-2\). Among full-slack factorizations through products of
   arbitrary nonzero proper cones of dimension at most \(d\),

   \[
             \boxed{L_{\min}=L,\qquad M_{\min}=N+2=dL.} \tag{4}
   \]

   This permits arbitrary row splitting and requires no continuity of
   factor maps.

The Lorentz family is the rank-two spin-factor version of this theorem.
All conclusions remain valid for a heterogeneous mixture in which any
factor is replaced by a Lorentz cone \(Q_m\), \(m\geq3\): assign it
\(d_i=m\), \(R_i=2\), use one spatial coordinate as \(\ell_i\), and use
the orthogonal spatial coordinate to obtain its diagonal \(Q_2\cong
\mathbb R_+^2\) section. The sphere proof supplies the same zero-level and
opposite-sign paths. Section 5 proves that the same conclusions hold for
arbitrary products of all simple Euclidean Jordan cones, including the
exceptional Albert cone.

## 1. Slater, compactness, and factor resources

Because \(A_i\) is off diagonal, \(\ell_i(I)=0\). Thus
\[
                  X_i^0=\frac{I}{\rho}
\]
gives a positive-definite point of (2), because
\(\sum_i\operatorname{tr}X_i^0=\sum_iR_i/\rho=1\). Hence the two
displayed affine equations are independent and \(N=M-2\).

Positive semidefiniteness and fixed total trace make \(Z\) compact. To see
factor essentiality, relax \(K_i\) to its full Hermitian span, choose
\(j\ne i\), and set
\[
          X_i=-\frac{T}{R_i}I,\qquad
          X_j=\frac{T+1}{R_j}I,\qquad X_k=0\ (k\ne i,j).
\]
Both balance functionals vanish on scalar matrices and the total trace is
one. Letting \(T\to\infty\) gives an unbounded family in the relaxed slice.
Each \(K_i\) is an irreducible classical symmetric
cone. At a rank-one point in factor \(i\), a nonzero complementary
rank-one dual matrix supplies a supporting slack row using that factor,
so no factor is slack-invisible.

## 2. Exact extreme points and connectedness

For an affine section \(\{X\in\prod_iK_i:\mathcal A X=b\}\), a point is
extreme exactly when
\[
 \ker\mathcal A\cap
 \bigoplus_i\operatorname{span}F_i(X_i)=\{0\},         \tag{5}
\]
where \(F_i(X_i)\) is the minimal cone face containing \(X_i\). Here
\(\operatorname{rank}\mathcal A=2\). A rank-\(r\) Hermitian PSD point has
minimal-face dimension
\[
                 r+\frac{\delta_i r(r-1)}2.            \tag{6}
\]
This is at least three for \(r\geq2\). Therefore every extreme point of
\(Z\) has either one or two nonzero blocks, all of rank one.

Normalize a rank-one ray as \(P=uu^*\), \(\|u\|=1\), so its projective
parameter lies in \(\mathbb FP^{R-1}\). A real orthogonal change in the
first two coordinates diagonalizes \(A_i\), after which
\[
                 \ell_i(uu^*)=|u_1|^2-|u_2|^2.         \tag{7}
\]
Consequently the exact alternatives are:

- one nonzero rank-one block with \(\ell_i(P)=0\);
- two nonzero rank-one blocks whose \(\ell\)-values have strict opposite
  signs, with their positive weights uniquely determined by trace one and
  balance.

No other point is extreme by (5)--(6).

The zero set
\[
 E_i=\{[u]\in\mathbb F_iP^{R_i-1}:|u_1|=|u_2|\}        \tag{8}
\]
is path-connected except when \((\mathbb F_i,R_i)=(\mathbb R,2)\), where
it has two points. For \(R_i\geq3\), scale the first two coordinates
together while introducing a nonzero third coordinate; this joins every
point of (8) to \([e_3]\). For \(R_i=2\), (8) is \(S^{\delta_i-1}\), hence
is connected for \(\mathbb C,\mathbb H\). The positive and negative
regions of (7) are path-connected: in the chart \(u_1\ne0\), respectively
\(u_2\ne0\), they are a unit ball in one projective coordinate times an
affine space.

Every two-block extreme deforms to a one-block point by moving one
nonzero \(\ell\)-value to zero and using the unique balance weights. Given
zero-level points in two different factors, choose paths entering the
positive region in the first and the negative region in the second. Their
unique balance-weighted sums form an extreme path joining the two
one-block points. This also joins the two components of the exceptional
\(\mathbb RP^1\) zero set through any other factor. Since \(L\geq2\),
\(\operatorname{ext}Z\) is path-connected.

## 3. Exact arbitrary barrier parameters

Use the matrix basis in which every \(A_i\) is off diagonal. Diagonal
matrices satisfy every balance equation automatically. Their intersection
with \(\widehat Z\) is the orthant
\[
                          \mathbb R_+^\rho.             \tag{9}
\]
Its boundary is contained in \(\partial\widehat Z\). Restricting any
self-concordant barrier on \(\widehat Z\) to (9), the independent-facet
lower bound gives \(\nu\geq\rho\). The standard barrier
\[
                     \Phi(X)=-\sum_i\log\det X_i        \tag{10}
\]
has parameter \(\rho\), proving the first equality in (3).

On the normalized slice, the diagonal section of (9) is a simplex of
dimension \(\rho-1\), and every simplex facet remains in \(\partial Z\).
Thus every, possibly coupled, barrier on \(Z\) has parameter at least
\(\rho-1\).

For the matching upper bound, let \(H=\nabla^2\Phi\), \(g=\nabla\Phi\),
and let \(a(X)=\sum_i\operatorname{tr}X_i\). Logarithmic homogeneity gives
\[
             H^{-1}g=-X,\qquad g^\mathsf TH^{-1}g=\rho.
\]
The inverse Hessian in the trace direction gives
\[
             a^\mathsf TH^{-1}a=\sum_i\operatorname{tr}(X_i^2)
                  \leq\left(\sum_i\operatorname{tr}X_i\right)^2=1. \tag{11}
\]
Projecting \(g\) off the normalization covector therefore yields squared
dual norm
\[
        \rho-\frac{(a^\mathsf TH^{-1}g)^2}
                         {a^\mathsf TH^{-1}a}
        =\rho-\frac1{a^\mathsf TH^{-1}a}\leq\rho-1.    \tag{12}
\]
Restriction to the additional balance tangent can only decrease the norm.
Affine restriction preserves self-concordance and the barrier property,
so (10) restricted to \(Z\) is a \((\rho-1)\)-barrier. This proves (3).

If \(\widehat Z_{\rm ext}\) is any affine lift of \(Z\) with bounded
nonempty fibers and \(\widehat\Phi\) is a \(\nu\)-barrier on it, exact
partial minimization over each fiber produces a \(\nu\)-barrier on \(Z\).
Equation (3) then gives \(\nu\geq\rho-1\).

## 4. Exact cap hardness

In the identical-type case, ordinary slack rank gives total factor
dimension \(M'\geq N+1\) for every full-slack factorization. The cap
\(d<N+1\) excludes a one-factor equality realization. If a multifactor
realization had \(M'=N+1\), minimum-dimension cone rigidity would identify
its product cone with the homogenization cone of \(Z\). But the
projectivized extreme rays of a nontrivial cone product form a clopen
disjoint union, whereas those of the homogenization are
\(\operatorname{ext}Z\), which is connected. Hence \(M'\geq N+2=dL\).
Since \(M'\leq dL'\), one has \(L'\geq L\). The original product slice
attains both bounds, proving (4).

## 5. Extension to every simple symmetric cone

The exact barrier calculation needs neither matrix coordinates nor the
topology of the extreme-ray manifold. Let \(V_i\) be arbitrary simple
Euclidean Jordan algebras, including copies of the Albert algebra
\(H_3(\mathbb O)\), and write \(r_i\) for their ranks. Choose a Jordan
frame \(c_{i1},\ldots,c_{ir_i}\) and a nonzero element
\(A_i\in V_i(c_{i1},c_{i2})\) in the off-diagonal Peirce space. Put
\[
       \ell_i(x)=\langle A_i,x\rangle,\qquad
       \rho=\sum_i r_i,
\]
and define the balance cone and trace-one body exactly as in (2).

Every frame-diagonal element is orthogonal to \(A_i\). Consequently the
frame-diagonal section of the balance cone is exactly
\(\mathbb R_+^\rho\), and its trace-one section is a
\((\rho-1)\)-simplex. Their relative boundaries remain in the boundaries
of the balance cone and body. The orthant and simple-vertex lower bounds
therefore apply to arbitrary coupled barriers.

The product standard Jordan barrier has logarithmic-homogeneity degree
\(\rho\). For its Hessian \(H\), gradient \(g\), and the total-trace
covector \(a\), the Euclidean Jordan identities give
\[
 H^{-1}g=-x,\qquad g^TH^{-1}g=\rho,\qquad
 a^TH^{-1}a=\sum_i\operatorname{tr}(x_i^2)
       \leq\left(\sum_i\operatorname{tr}x_i\right)^2.
\]
The same metric projection as in (12) removes at least one unit on the
trace-one slice, and the balance equation can only decrease the restricted
dual norm. Hence, for arbitrary products of simple symmetric cones,
\[
       \boxed{\nu_{\rm opt}(\widehat Z)=\rho,\qquad
              \nu_{\rm opt}(Z)=\rho-1.}                 \tag{13}
\]
Exact partial minimization transfers the \(\rho-1\) lower bound to every
bounded-fiber affine lift of \(Z\).

The extreme-point and cap arguments extend as well. For every simple EJA,
a rank-\(k\geq2\) point has minimal-face dimension
\(k+a_i k(k-1)/2\geq3\). Thus the two-row activation argument again leaves
only one or two nonzero rank-one blocks, with zero or opposite strict
\(\ell\)-signs. The classical and spin primitive-ray manifolds were handled
above. It remains only to check the Albert primitive-ray manifold
\(\mathbb OP^2\).

By the spectral theorem, an automorphism and a positive rescaling take a
nonzero \(A_i\in V_i(c_{i1},c_{i2})\) to
\(c_{i1}-c_{i2}\). In the standard reduced-homogeneous-coordinate chart
of \(\mathbb OP^2\) where the first diagonal coordinate is positive, write
a point as \((x,y)\in\mathbb O^2\). (See Held, Stavrov, and VanKoten,
[*Semi-Riemannian geometry of (para-)octonionic projective
planes*](https://arxiv.org/abs/math/0702631), Section 3.) Its three diagonal
coordinates are
\[
 \frac{(1,\|x\|^2,\|y\|^2)}{1+\|x\|^2+\|y\|^2},
\]
so the height is
\[
 h(x,y)=\frac{1-\|x\|^2}{1+\|x\|^2+\|y\|^2}.            \tag{14}
\]
The positive region is \(B^8\times\mathbb R^8\), hence path-connected.
Swapping the first two frame idempotents is an Albert-algebra automorphism
that sends \(h\) to \(-h\), so the negative region is path-connected too.
The zero set in this chart is \(S^7\times\mathbb R^8\). Outside the chart,
zero height forces the unique point \(c_{i3}\).  Connect an arbitrary
\((x,y)\in S^7\times\mathbb R^8\) inside that product to \((x,0)\), then,
for a fixed unit \(y_0\), let \((x,ty_0)\) tend to infinity; its projective
limit is \(c_{i3}\).  Hence the full zero set is
path-connected. The same paths with \(\|x\|<1\) or \(\|x\|>1\) show that
every zero point is approachable from the required sign region.

The cross-factor opposite-sign paths from Section 2 therefore prove that
the extreme set is path-connected even with Albert factors. Factor
essentiality and slack visibility use only scalar interior points and
complementary primitive idempotents, so they also persist. Consequently
all five headline conclusions extend to arbitrary heterogeneous products
of simple symmetric cones. In particular, for \(L\) identical Albert
factors, \(d=27\), \(R=3\), and \(N=27L-2\), the exact arbitrary-proper-
cone dimension-cap frontier is
\[
                    L_{\min}=L,\qquad M_{\min}=N+2=27L.  \tag{15}
\]

## 6. An explicit maximal-exposed-rank objective and central path

The same family has a canonical objective whose exposed Jordan rank equals
the optimal body-barrier parameter.  Choose one frame idempotent, say
\(c=c_{11}\), and put

\[
                 S=(e_1-c,e_2,\ldots,e_L),\qquad
                 Q=\operatorname {rank}_J S=\rho-1.       \tag{16}
\]

On \(Z\), minimizing \(\langle S,X\rangle\) uniquely exposes the feasible
point \((c,0,\ldots,0)\), and its optimum is zero.  Indeed,
\(\langle S,X\rangle=1-\langle c,X_1\rangle\geq0\), with equality only
at that point.  Thus \(S\) is a genuine conic exposing slack of rank
\(Q=\nu_{\rm opt}(Z)\).

The analytic center is \(X^c_i=e_i/\rho\).  For the objective-scaled
standard central path, parameterized by \(\tau\geq0\), strict convexity
and the first-order equations give

\[
 X_1(\tau)=a(\tau)c+b(\tau)(e_1-c),\qquad
 X_i(\tau)=b(\tau)e_i\quad(i>1),                         \tag{17}
\]

where

\[
 a+Qb=1,\qquad {1\over b}=\tau+{1\over a}.              \tag{18}
\]

All balance functionals vanish on this frame-diagonal path.  Conversely,
the gradient of \(\tau\langle S,\cdot\rangle+\Phi\) at (17) lies in the
span of the trace-normal covector, so (17)--(18) are the full affine-slice
first-order conditions, not merely those of the diagonal restriction.

Let \(g(\tau)=\langle S,X(\tau)\rangle=Qb(\tau)\).  Then

\[
 \tau={Q-(Q+1)g\over g(1-g)},\qquad
 g(0)={Q\over Q+1}={\rho-1\over\rho},\qquad
 g(\tau)\sim{Q\over\tau}.                              \tag{19}
\]

The exact standard-barrier length of the central-path segment between
gaps \(g_0=(\rho-1)/\rho\) and \(\epsilon\in(0,g_0)\) is

\[
 \mathcal L_{\rm CP}(\epsilon)
   =\int_{\epsilon}^{g_0}
       \sqrt{{Q\over g^2}+{1\over(1-g)^2}}\,dg.          \tag{20}
\]

In particular,

\[
 \sqrt{\rho-1}\log{g_0\over\epsilon}
 \leq \mathcal L_{\rm CP}(\epsilon)
 \leq \sqrt{\rho-1}\log{g_0\over\epsilon}
       +\log\!\bigl(\rho(1-\epsilon)\bigr).             \tag{21}
\]

The lower coefficient is path-independent.  In the exposed-minor theorem,
\(\det_S S=1\), while the exposed principal minor of \(X^c\) has
determinant \(\rho^{-Q}\).  Hence its scale is exactly
\(\Delta_c=Q/\rho=g_0\), and every piecewise-\(C^1\) interior feasible path
in the displayed product variables from \(X^c\) to gap at most
\(\epsilon\) has standard-barrier metric length at least the left side of
(21).  Consequently any method whose counted rounds have
intrinsic movement at most \(D\) needs at least

\[
             {\sqrt{\rho-1}\log(g_0/\epsilon)\over D}    \tag{22}
\]

rounds from the analytic center.  This is a geometric bounded-movement
statement for the displayed standard barrier.  It is not a quantum-query
or runtime lower bound, and it does not assert the same metric bound for
an arbitrary optimal coupled barrier.

## Literature and novelty boundary

The minimal-face criterion (5) is not new.  Dubins, [*On Extreme Points of
Convex Sets*](https://doi.org/10.1016/S0022-247X(62)80007-9), already gives
the support-at-most-two conclusion after trace normalization and one further
hyperplane cut.  Pataki, [*On the Rank of Extreme Matrices in Semidefinite
Programs and the Multiplicity of Optimal
Eigenvalues*](https://doi.org/10.1287/moor.23.2.339), is the standard
real-PSD rank specialization, while Henrion, Kružík, and Weis, [*Extreme
Points and Faces in the Moment Problem*](https://arxiv.org/abs/2606.21391),
Theorem 2.6, state the general smallest-face injectivity criterion underlying
(5).  What these results do not provide is the exact one-/two-block sign
classification for (2), the projective zero-level topology, or the
cross-factor paths proving that all extreme points form one path component.

Optimal barrier parameter \(R\) for a rank-\(R\) classical Hermitian cone is
standard Euclidean-Jordan theory, including the quaternionic case.  The
precise primary antecedents are Güler and Tunçel, [*Characterization of the
Barrier Parameter of Homogeneous Convex
Cones*](https://uwaterloo.ca/combinatorics-and-optimization/sites/default/files/uploads/documents/corr95.pdf),
and Cardoso and Vieira, [*On the Optimal Parameter of a Self-Concordant
Barrier over a Symmetric
Cone*](https://doi.org/10.1016/j.ejor.2004.11.027).  The latter identifies
Euclidean-Jordan rank with the Carathéodory number and analyzes the generalized
log-determinant.  The 2026 paper of Gouveia, Ito, and Lourenço, [*Minimal
Hyperbolic Polynomials and Ranks of Homogeneous
Cones*](https://www.heldermann-verlag.de/jca/jca33-oa/jca2623-b.pdf), Section
4.2, uses the same classical equality while showing that optimal homogeneous
barriers and minimal hyperbolic barriers can differ outside symmetric cones.
These are ambient-cone results; they do not imply the one-unit normalized
slice identity \(\nu_{\rm opt}(Z)=\rho-1\).

The lower-bound ingredients for (3) are classical.  The local
independent-halfspace lower is Nesterov--Nemirovskii,
*Interior-Point Polynomial Algorithms in Convex Programming*, Section 2.3.4;
its simplex specialization is Proposition 2.3.6.  He, Saunderson, and Fawzi,
[*Exploiting Structure in Quantum Relative Entropy
Programs*](https://arxiv.org/abs/2407.00241), give a recent, distinct example
in which working directly with structured Hermitian-matrix cones removes
redundant log-determinant terms and proves a smaller optimal parameter.  Their
cones are nonlinear quantum-relative-entropy epigraphs, and their result does
not cover product-Hermitian balance sections or the exact \(\rho-1\) formula
here.

Bounded-fiber exact partial minimization is Chares, [*Cones and Interior-Point
Algorithms for Structured Convex Optimization Involving Powers and
Exponentials*](https://dial.uclouvain.be/pr/boreal/en/object/boreal%3A28538),
Assumption 4 and Theorem 5.2.1.  Thus barrier-parameter preservation under
that hypothesis is known, and item 4 is best described as a **family-specific
corollary** of Chares plus the exact intrinsic lower bound.  The screen gives
no basis for dropping boundedness of the fibers.

For item 5, Gouveia, Parrilo, and Thomas, [*Lifts of Convex Sets and Cone
Factorizations*](https://arxiv.org/abs/1111.3164), establish the general
lift--slack-factorization correspondence.  Fawzi--Parrilo's
[*Exponential Lower Bounds on Fixed-Size PSD Rank and Semidefinite Extension
Complexity*](https://arxiv.org/abs/1311.2571) and Saunderson's
[*Limitations on the Expressive Power of Convex Cones without Long Chains of
Faces*](https://arxiv.org/abs/1902.06401) give product-cone lower bounds in
fixed-PSD-block and bounded-face-chain models.  Soh and Chandrasekaran,
[*Fitting Tractable Convex Sets to Support Function
Evaluations*](https://doi.org/10.1007/s00454-020-00258-0), Proposition 2.6,
show that a PSD cone of order \(q\) cannot be lifted through a product of
smaller PSD cones.  None of these statements gives the exact total-real-
dimension/factor-count frontier against **all** nonzero proper cones of
dimension at most \(d\).

A targeted classical and 2024--2026 primary-source screen found no exact
statement combining the connected-extreme balance construction, exact
arbitrary-coupled values \(\rho\) and \(\rho-1\), the bounded-fiber corollary,
and the identical-factor cap frontier \(M_{\min}=N+2,\ L_{\min}=L\).  The
conservative label is **candidate explicit sharp synthesis**, not a new
general extremality, symmetric-cone barrier, partial-minimization, or
lift-factorization theorem.  This is evidence from a targeted search, not an
exhaustive priority determination; quaternionic and mixed-spin-factor cases
deserve specialist review.

## Audit targets

1. Check quaternionic real dimensions, trace pairing, face dimensions,
   and the standard barrier calculation.
2. Check the two-equation extreme classification (5)--(7).
3. Check path-connectedness of (8) and the cross-factor paths, especially
   real order two.
4. Check the orthant/simplex restrictions and boundary inheritance for
   arbitrary coupled barriers.
5. Check bounded-fiber partial minimization and the arbitrary-dictionary
   cap proof.
6. Check the all-EJA orthant/simplex sections and trace-Hessian calculation
   in (13), including the Albert algebra.
7. Check the octonionic chart formula (14), the zero/sign-region
   connectivity, and the Albert cap consequence (15).
8. Check the exposed slack, full-slice central-path equations, exact length,
   and exposed-minor scale in (16)--(22).

## Independent audit record

An independent hostile audit checked the real-dimension and minimal-face
formulas over \(\mathbb R,\mathbb C,\mathbb H\), including the Moore
determinant and real-trace Hessian calculation in the quaternionic case.
It verified that the two affine rows give columns \((1,c_i)\), so an
extreme point has exactly one zero-level rank-one block or two rank-one
blocks with strict opposite signs and uniquely determined weights. The
projective zero sets, sign charts, and cross-factor paths give a
path-connected extreme set, including the exceptional two-point zero set
of \(\mathbb RP^1\). The diagonal orthant and simplex sections inherit the
ambient and body boundaries and therefore prove the lower bounds for
arbitrary coupled barriers; the restricted product barrier attains them.
Finally, factor essentiality, slack visibility, bounded-fiber partial
minimization, minimum-dimension cone rigidity, and the cap arithmetic were
checked independently. The same arguments pass for heterogeneous spin
factors with the resource convention stated above. No defect was found.

The all-EJA extension received a separate hostile audit.  It verified
\(H=P(x^{-1})\), \(H^{-1}=P(x)\), the trace-covector projection in (13),
and the inherited orthant/simplex boundary lower bounds.  For Albert it
checked the \(\mathbb OP^2\) big-cell coordinates, the unique zero-height
point \(c_3\) outside that chart, connectivity and two-sided accessibility
of all three sign strata, and the transfer of the connected-extreme cap
argument.  The rank-two Albert face dimension and the exact
\(L_{\min}=L, M_{\min}=27L\) arithmetic also pass.  The audit returned
**PASS**; its only requested change was the explicit chart path to \(c_3\),
now included above.

The QIPM-facing central-path corollary received a further hostile audit.
It verified that \(S=e-c\) uniquely exposes the selected frame vertex,
that the full affine-slice first-order equations have zero balance
multiplier, and that they reduce over every simple EJA to (18).  Direct
recalculation gives the gap inversion (19), the Hessian line element
\((da/a)^2+Q(db/b)^2\), and therefore the exact integral and both bounds
in (20)--(21).  Finally, the exposed support determinant is one and the
compressed analytic-center determinant is \(\rho^{-Q}\), so
\(\Delta_c=Q/\rho\).  The bounded-movement consequence (22) has the stated
standard-barrier, non-query scope.  No mathematical correction was
required.
