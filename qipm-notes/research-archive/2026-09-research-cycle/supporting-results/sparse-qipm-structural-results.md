# Structural lower bounds and oracle embeddings for sparse quantum interior-point methods

**Research note — 2026-09-02**  
**Status:** theorem candidates with complete internal proofs, adversarial proof review,
and targeted open-literature checks. No claim of priority is unconditional;
“apparently new” means that no matching statement was found in the searches recorded
in Section 9.

## Abstract

This note develops five groups of results about quantum interior-point methods (QIPMs)
for sparse linear optimization.

1. The complementarity equation itself imposes a support barrier. At an exactly
   centered point, any inexact short-step direction whose complementarity residual is
   at most \(\eta\mu\) must change a linear number of primal/slack coordinate pairs.
   More generally, a \(k\)-sparse latent Newton state reconstructed through a
   column-local map of locality \(g\) must satisfy \(gk=\Omega(n)\). Thus their
   sparsity and scatter locality cannot have sublinear product in the usual short-step
   formulation.
2. There is a fixed-pattern, two-sparse box-LP family for which the reduced barrier
   Hessian and the primal-dual normal matrix are scalar diagonal matrices, with
   condition number one at every point on the central path, yet estimating the optimal
   value or returning a sufficiently accurate classical solution requires
   \(\Omega(n)\) quantum coefficient queries. The lower bound remains
   \(\Omega(\sqrt{nk})\) when the reduced box-variable optimum is promised to be
   \(k\)-sparse.
3. A balanced standard-form LP embeds a sparse linear system in a strictly feasible
   short-step OSS while preserving sparsity and condition number. The step reduces
   complementarity, stays in the central neighborhood, and exposes the hard solution
   block with constant probability. This makes established sparse-QLS lower bounds
   genuine lower bounds for that QIPM subroutine.
4. The \(\Omega(\kappa\log(1/\epsilon))\) sparse-QLS precision lower bound of Mori et
   al. remains valid for real symmetric, indefinite, two-sparse KKT matrices whose
   support graphs have treewidth at most two. Bounded treewidth therefore does not
   remove condition/precision dependence from a QLSA-based KKT solve.
5. As a supplementary algorithm-design result, projective centering of established
   lazy diagonal maintenance yields a reset ledger bounded by projective log variation.
   This is a modest refinement of classical inverse-maintenance ideas, not a new
   preconditioning method or a quantum speedup: event discovery, block-encoding
   normalization, inverse-update stability, and classical readout remain separate costs.

Together these results give a rigorous phase boundary for sparse QIPMs: sparse input,
a sparse reduced optimum, good conditioning, or bounded treewidth can each coexist
with a hard subproblem or output contract. Slow projective operator variation remains
a possible design opportunity, but no quantum runtime improvement is claimed for it.

## 1. Models and notation

For standard-form linear optimization,

\[
  \min c^T x \quad\text{subject to}\quad Ax=b,\qquad x\ge 0,
\]

the dual slack is \(s=c-A^Ty>0\), and
\(X=\operatorname{Diag}(x)\), \(S=\operatorname{Diag}(s)\). A centering
direction with target factor \(\sigma\) and complementarity residual \(r\) satisfies

\[
  S\Delta x+X\Delta s=-(1-\sigma)\mu e+r                 \tag{1}
\]

at an exactly centered point \(XSe=\mu e\). The residual contract is
\(\lVert r\rVert_2\le\eta\mu\). This is the same form used in inexact feasible
short-step methods; the feasibility equations and the stationarity block are not needed
for the first theorem.

For a vector pair, define its complementarity-pair support by

\[
  \operatorname{psupp}(\Delta x,\Delta s)
  =\{i:\Delta x_i\ne0\ \text{or}\ \Delta s_i\ne0\}.
\]

For a matrix, its support graph has one vertex per row/column and an undirected edge for
each structurally nonzero off-diagonal entry. Query lower bounds below are black-box
bounds. They do not imply the same lower bound when the entire input is already
available classically or when only a quantum-state output is requested.

## 2. A complementarity sparsity barrier

### Theorem 1 (support barrier at the center)

Let \((x,s)>0\) satisfy \(XSe=\mu e\), and let \(0\le\sigma<1\). If a direction satisfies (1) and
\(\lVert r\rVert_2\le\eta\mu\), then

\[
 \left|\operatorname{psupp}(\Delta x,\Delta s)\right|
 \ge n-\frac{\eta^2}{(1-\sigma)^2}.                       \tag{2}
\]

In particular, for a short step \(1-\sigma=a/\sqrt n\), with \(0\le\eta<a\),

\[
 \left|\operatorname{psupp}(\Delta x,\Delta s)\right|
 \ge \left(1-\frac{\eta^2}{a^2}\right)n.                 \tag{3}
\]

For an exact direction, every complementarity pair changes.

#### Proof

Let \(Z\) be the set of indices at which both direction coordinates vanish. For each
\(i\in Z\), the left side of (1) is zero, hence
\(r_i=(1-\sigma)\mu\). Therefore

\[
 |Z|(1-\sigma)^2\mu^2
 \le \sum_{i\in Z}r_i^2
 \le \lVert r\rVert_2^2
 \le \eta^2\mu^2.
\]

Thus \(|Z|\le\eta^2/(1-\sigma)^2\), which proves (2). Substitution of
\(1-\sigma=a/\sqrt n\) gives (3). ∎

The theorem is unchanged for linearly constrained convex quadratic programs, or any
primal-dual method with the same coordinatewise nonnegative complementarity equation.
The objective Hessian and stationarity equation are irrelevant to the proof.

### Corollary 1 (latent sparsity versus reconstruction locality)

Suppose a QIPM solves for latent coefficients \(z\) and reconstructs the actual update
as \((\Delta x,\Delta s)=Bz\). Let \(g\) be the maximum number of complementarity
pairs touched by one column of \(B\). If the latent coefficient vector is
\(k\)-sparse, then at an exactly centered point

\[
  gk\ge n-\frac{\eta^2}{(1-\sigma)^2}.                    \tag{4}
\]

For a short step, \(gk\ge[1-(\eta/a)^2]n\).

#### Proof

The union of the pair supports of the \(k\) selected columns contains at most \(gk\)
indices, while it must contain the support of the reconstructed direction. Apply
Theorem 1. ∎

This gives a precise dichotomy. If the reconstruction columns are local, the latent
QLSA solution cannot be sublinearly sparse. If the latent solution is sparse, the
reconstruction map must have nonlocal columns, and explicitly scattering those columns
still touches \(\Omega(n)\) output coordinates. For the orthogonal-subspaces system
(OSS), the map contains the null-space basis \(V\) and \(-A^T\), so (4) also exposes
where basis-inverse densification moves the cost.

If every row of \(A\) has at most \(r_A\) nonzeros and
\(\Delta s=-A^T\Delta y\), then
\(|\operatorname{supp}\Delta s|\le r_A|\operatorname{supp}\Delta y|\). Hence

\[
 |\operatorname{supp}\Delta x|+r_A|\operatorname{supp}\Delta y|
 \ge n-\frac{\eta^2}{(1-\sigma)^2}.                       \tag{5}
\]

Sparse reduced dual output therefore forces a dense primal update unless the dual
support times row locality is already linear.

### Proposition 1 (away from exact centering)

At any positive point, write the inexact centering equation as

\[
 S\Delta x+X\Delta s=\sigma\mu e-XSe+r,
 \qquad\lVert r\rVert_2\le\eta\mu.
\]

For \(\rho>0\), let
\(J_\rho=\{i:|x_is_i-\sigma\mu|\ge\rho\mu\}\). Then

\[
 |\operatorname{psupp}(\Delta x,\Delta s)|
 \ge |J_\rho|-(\eta/\rho)^2.                              \tag{6}
\]

The proof repeats Theorem 1 on the zero-update indices inside \(J_\rho\).

### Proposition 2 (a sparse LP with a one-sparse optimum and an incompressible step)

For \(n\ge3\), consider

\[
 \min x_2
\]

subject to

\[
 x_1+x_2=1,\qquad x_{i-1}-x_i=0\quad(i=3,\ldots,n),
 \qquad x\ge0.                                             \tag{7}
\]

The constraint matrix has full row rank, \(2(n-1)\) nonzeros, maximum row sparsity
two, and maximum column sparsity two. Its feasible segment is
\(x(t)=(1-t,t,\ldots,t)\), \(0\le t\le1\), and its unique optimum is the
one-sparse vector \(e_1\).

On the central-path branch, \(0<t<(n-1)/n\), the exact logarithmic-barrier path is
determined by

\[
 \mu(t)=\frac{t(1-t)}{n-1-nt}.                             \tag{8}
\]

At \(t=1/2\), where \(\mu=1/[2(n-2)]\), the primal component of the exact Newton
direction for any nonzero infinitesimal change of \(\mu\) is proportional to

\[
 (-1,1,\ldots,1).                                         \tag{9}
\]

Consequently, the normalized primal direction has best \(k\)-sparse approximation
error exactly

\[
  \sqrt{1-k/n}.                                            \tag{10}
\]

Constant relative \(\ell_2\) error requires \(k=\Omega(n)\).

#### Proof

Substitution of the equality constraints gives the one-dimensional barrier objective

\[
 f_\mu(t)=t-\mu\bigl[\log(1-t)+(n-1)\log t\bigr].
\]

The stationarity equation rearranges to (8). Differentiating the exact KKT system shows
that the Newton tangent is a nonzero scalar multiple of
\(x'(t)=(-1,1,\ldots,1)\). All normalized coordinates therefore have magnitude
\(1/\sqrt n\), and deleting \(n-k\) of them leaves squared error
\((n-k)/n\). ∎

The example rules out a common shortcut: sparsity of the optimal solution does not
imply sparsity or compressibility of central-path directions, even when both row and
column sparsities of \(A\) are constant.

### Theorem 1A (universality of positive sparse-QP central-direction profiles)

Sparse optimal support in fact imposes essentially no geometry on a primal central-path
direction. Let \(u\in\mathbb R_{++}^n\) be any positive unit vector, and choose
\(\mu_0>0\) such that \(u_i^{-2}>4\mu_0\) for every \(i\). Define

\[
 c_1=-\sqrt{u_1^{-2}-4\mu_0},
 \qquad
 c_i=+\sqrt{u_i^{-2}-4\mu_0}\quad(i\ge2),                 \tag{10a}
\]

and consider the strongly convex, bound-constrained QP

\[
 \min_{x\ge0}\ {1\over2}\lVert x\rVert_2^2+c^Tx.         \tag{10b}
\]

Its objective Hessian is \(I\), its unique optimum is the one-sparse vector
\(x^*=(-c_1)e_1\), and strict complementarity holds. Nevertheless, its exact central
path has

\[
 x_i(\mu)={-c_i+\sqrt{c_i^2+4\mu}\over2},
 \qquad
 x_i'(\mu)={1\over\sqrt{c_i^2+4\mu}},                     \tag{10c}
\]

and therefore

\[
 x'(\mu_0)=u,
 \qquad
 \operatorname{Diag}(2x(\mu_0)+c)=\operatorname{Diag}(1/u_i). \tag{10d}
\]

The diagonal matrix in (10d) is the Jacobian of the row-scaled complementarity
equation used to compute the central tangent, and is one-sparse. It has constant
condition number for every near-uniform family with
\(\max_i u_i/\min_i u_i=O(1)\).

This conditioning statement is formulation dependent. The canonical primal-barrier
Hessian is \(I+\mu X^{-2}=X^{-1}(X+S)\), whose condition can differ; (10d) does not
claim that every scaling of the QP Newton equations is well conditioned.

#### Proof

Stationarity gives \(s=x+c\), so centrality is
\(x_i(x_i+c_i)=\mu\). Its positive root and derivative are (10c). Substitution of
(10a) proves (10d). At \(\mu=0\), the first cost is negative and all others are
positive, giving the stated unique optimum and positive inactive slacks. ∎

Restrict \(u\) to the nonnegative, near-uniform hard family used in the coherent
tomography lower bound of van Apeldoorn et al. The theorem embeds every such state as
the normalized Newton direction of a one-sparse, constant-conditioned system with
identity objective Hessian and a one-sparse strictly complementary optimum. Therefore,
in the modular controlled solution-unitary model, classical \(\epsilon\)-\(\ell_2\)
direction recovery needs

\[
 \widetilde\Omega(n/\epsilon)                             \tag{10e}
\]

solution-unitary calls. This bound is on the QLSA/readout interface. An algorithm also
allowed to inspect the exact classical coefficients in (10a) can read information about
\(u\) directly, so (10e) is not a stronger combined-oracle lower bound.

## 3. Perfect conditioning does not remove sparse-LP query hardness

### Theorem 2 (fixed sparse box LP with condition-one central systems)

For a hidden string \(b\in\{0,1\}^N\), let \(c_i=1-2b_i\), and consider

\[
 \begin{aligned}
   \min_{x,t\ge0}\quad &c^Tx\\
   \text{subject to}\quad &x+t=e.
 \end{aligned}                                             \tag{11}
\]

The equality matrix \(A=[I\ I]\) is input-independent, has \(2N\) nonzeros,
maximum row sparsity two, and maximum column sparsity one. The following all hold.

1. The unique optimum is \((x^*,t^*)=(b,e-b)\), with
   \(\operatorname{OPT}_b=-|b|\), and every feasible \(x\) obeys
   \[
     c^Tx-\operatorname{OPT}_b=\lVert x-b\rVert_1.         \tag{12}
   \]
2. For every barrier parameter \(\mu>0\), both the reduced logarithmic-barrier
   Hessian and the primal-dual normal matrix on the exact central path are positive
   scalar multiples of \(I\). Their row/column sparsity is one and their spectral
   condition number is exactly one.
3. With bit-or-controlled-phase oracle access to \(b\), any bounded-error quantum algorithm that
   estimates the optimal value to additive error below \(1/2\), or returns a feasible
   classical point of objective gap below \(1/2\), makes at least \(N/2\) coefficient
   queries.
4. For \(1\le k\le N\), under the promise \(|b|\in\{k-1,k\}\), scalar-value estimation below error
   \(1/2\) needs
   \[
      \Omega\!\left(\sqrt{k(N-k+1)}\right)                \tag{13}
   \]
   queries. Under the promise \(|b|=k\) with \(1\le k\le N/2\), returning the weight-\(k\) reduced
   box-variable optimum \(x^*=b\), or a
   feasible point of gap below \(1/2\), needs
   \(\Omega(\sqrt{k(N-k)})=\Omega(\sqrt{Nk})\) queries.

#### Proof

The optimization is coordinate-separable. A positive cost chooses \(x_i=0\), and a
negative cost chooses \(x_i=1\), proving the optimum and (12).

Eliminate \(t=e-x\). The barrier objective is

\[
 \Phi_{b,\mu}(x)=c^Tx-\mu\sum_i[\log x_i+\log(1-x_i)].     \tag{14}
\]

For \(c_i=1\), stationarity gives the central coordinate

\[
 p_\mu=\frac{1+2\mu-\sqrt{1+4\mu^2}}{2}\in(0,1/2),       \tag{15}
\]

and for \(c_i=-1\) it gives \(1-p_\mu\). Therefore

\[
 \nabla^2\Phi_{b,\mu}(x_\mu)
 =\mu\bigl[p_\mu^{-2}+(1-p_\mu)^{-2}\bigr]I.             \tag{16}
\]

On the primal-dual path, the slacks are \(s_x=\mu/x\) and
\(s_t=\mu/t\). Hence

\[
 AX S^{-1}A^T
 =\frac{p_\mu^2+(1-p_\mu)^2}{\mu}I.                      \tag{17}
\]

This proves item 2.

An optimal-value estimate below \(1/2\) can be rounded to recover the integer
\(|b|\), hence its parity. Bounded-error quantum parity requires \(N/2\) queries.
Likewise, (12) and gap below \(1/2\) imply that thresholding each coordinate at
\(1/2\) recovers every bit of \(b\).

For the adjacent-weight promise, use the adversary matrix given by the bipartite
inclusion graph between \((k-1)\)- and \(k\)-subsets. Its norm is
\(\sqrt{k(N-k+1)}\), while the matrix remaining after fixing one queried index has
norm one. For fixed weight \(k\), the Johnson-graph/all-marked-item adversary gives
\(\Omega(\sqrt{k(N-k)})\). The full standard-form vector \((b,e-b)\) always has
support size \(N\); “sparse optimum” here refers only to the reduced box variable
\(x=b\). ∎

The linear lower bound is not only an artifact of asking for subconstant average
coordinate error. Restricting \(b\) to an exponential constant-weight code of relative
distance \(\delta\), a feasible point with gap at most \(\gamma N\),
\(\gamma<\delta/4\), can be thresholded and uniquely decoded. The polynomial/Fourier
span of a \(T\)-query bit- or controlled-phase-oracle algorithm has dimension at most
\(\sum_{j=0}^T\binom Nj\); Holevo and Fano bounds then give \(T=\Omega(N)\).

### Corollary 2 (a QIPM-native sign-state readout instance)

At the strictly feasible point \(x=t=e/2\),

\[
 \nabla\Phi_{b,\mu}=c,\qquad
 \nabla^2\Phi_{b,\mu}=8\mu I,qquad
 \Delta=-\frac{c}{8\mu}.                                  \tag{18}
\]

Thus the normalized Newton state is, up to global phase,

\[
 |\Delta_b\rangle=\frac1{\sqrt N}\sum_i(-1)^{b_i}|i\rangle. \tag{19}
\]

Choosing \(\mu=4N\) makes the squared decrement of the scaled function \(\Phi\) equal
to \(1/32\); for the conventional self-concordant normalization \(\Phi/\mu\), it is
\(1/(128N)\). A matching primal-dual witness is

\[
 y_i=-8N+c_i/2,\qquad s_{x,i}=8N+c_i/2,\qquad
 s_{t,i}=8N-c_i/2.
\]

It is strictly feasible, has complementarity average \(4N\), and its relative
\(N_\infty\) deviation is \(1/(16N)\). Thus the instance is well inside a standard
central neighborhood rather than being a boundary artifact. Choose an
exponential code whose projective Hamming distance satisfies
\(\min\{d_H(b,b'),N-d_H(b,b')\}\ge\delta N\) for distinct codewords. A greedy
packing supplies such a code for sufficiently small constant \(\delta>0\), and the
rays (19) are then separated by a constant.
Any modular recovery procedure that returns the normalized direction ray to a
sufficiently small constant \(\ell_2\) error, using
\(U_b=D_bW\) and its inverse with known uniform-state preparation \(W\), needs
\(\Omega(N)\) calls. This is a
readout-interface bound, not a lower bound for quantum-only observable output.

The construction is stronger than merely observing that writing \(N\) numbers takes
\(N\) operations: even the scalar optimal value is query-hard, while the constraint
matrix and every central Newton sparsity pattern are fixed.

## 4. Sparse-QLS lower bounds survive a feasible QIPM short step

The preceding LP family gives an end-to-end optimization lower bound with perfect
conditioning. The next result answers a different question: do the established
condition-, sparsity-, and precision-dependent QLS lower bounds actually occur in a
legitimate QIPM Newton system? The answer is yes for the feasible OSS formulation,
including a progress step that reduces complementarity.

### Theorem 3 (query-preserving feasible OSS short-step embedding)

Let \(H\in\mathbb R^{n\times n}\) be real symmetric, invertible,
\(d\)-sparse by rows and columns, and normalized so \(\lVert H\rVert_2=1\), with
bidirectional sparse access. Let \(q\in\mathbb R^n\), \(\lVert q\rVert_2=1\), be the
known right-hand side of a hard QLS instance, with coherent coordinate-value access.
For any fixed neighborhood radius \(\theta\in(0,1)\), choose constants
\(0<\delta\le\min\{\theta,1/2\}\) and \(0\le\alpha\le\delta/4\), and put

\[
 a={\delta q\over\sqrt2},
 \qquad D=\operatorname{Diag}(a),
 \qquad \sigma=1-{\alpha\over\sqrt n}.                  \tag{20}
\]

Define the standard-form LP

\[
 \min c^Tx\quad\text{subject to}\quad
 A x=0,\quad x\ge0,
 \qquad
 A=[H\ -H],\quad c=(e+a,e-a).                             \tag{21}
\]

At the strictly feasible point
\(x^0=e_{2n}\), \(y^0=0\), \(s^0=c\), the following hold.

1. The complementarity average is \(\mu^0=1\), and the point belongs to both the
   standard \(N_2(\theta)\) and \(N_\infty(\theta)\) neighborhoods.
2. With null-space basis \(V=(I,I)^T\) and \(r=1-\sigma=\alpha/\sqrt n\), the feasible
   short-step OSS is
   \[
   M_{\rm OSS}
   =\begin{bmatrix}-H&I+D\\H&I-D\end{bmatrix},
   \qquad
   M_{\rm OSS}\binom{\Delta y}{\lambda}
   =\binom{-r e-a}{-r e+a}.                              \tag{22}
   \]
   Its row sparsity is at most \(d+1\), its column sparsity is at most \(2d\), and
   \[
      \kappa_2(M_{\rm OSS})=\Theta_\delta(\kappa_2(H)).    \tag{23}
   \]
3. Its exact solution has \(\lambda=-r e\) and
   \(\Delta y=\sigma H^{-1}a\). The normalized solution state's \(\Delta y\) block
   has probability at least
   \[
     p_0:={\sigma^2\delta^2/2\over \sigma^2\delta^2/2+\alpha^2},
   \]
   which is at least \(2/3\). Measuring that block extracts
   \(|H^{-1}q\rangle\) with constant overhead. When \(\alpha=0\), the probability is
   one.
4. The recovered step has \(\Delta x=(-r e,-r e)\) and
   \(\Delta s=(-\sigma a,\sigma a)\). Its endpoint satisfies
   \[
     x^1=\sigma e,\qquad s^1=(e+r a,e-r a),\qquad \mu^1=\sigma.
   \]
   It is strictly feasible and has centrality residual norm \(\sigma r\delta\), so it
   remains in both stated neighborhoods. For \(\alpha>0\), this is a genuine progress
   step; for \(\alpha=0\), it lands exactly at \(x^1=s^1=e\).
5. Every sparse query to the full LP data, the OSS, or its right-hand side is simulated
   with \(O(1)\) queries to \(H\) and \(O(1)\) evaluations of the fixed known vector
   \(q\); the equality right-hand side is zero and does not leak the hard input.

Consequently, after the standard symmetric dilation when needed, Mori et al.'s bounds
transfer to genuine feasible QIPM short-step systems with only constant-factor changes:

\[
 \Omega(\kappa_{\rm OSS}\sqrt{d_{\rm OSS}})               \tag{24}
\]

queries at a sufficiently small universal fixed state error, and

\[
 \Omega\!\left(\kappa_{\rm OSS}\log(1/\epsilon)\right)    \tag{25}
\]

for constant sparsity and \(0<\epsilon\le\epsilon_0\), subject in both cases to the
dimension and condition promises of the underlying QLS theorems. Here
\(\epsilon_0>0\) is a universal constant after the constant-error extraction below,
and \(d_{\rm OSS}\) is the
declared sparse-oracle slot bound; the sparsity lower-bound construction may use padded
candidate slots rather than that many actual nonzeros.

#### Proof

Primal feasibility follows from \(H e-H e=0\), and dual feasibility holds by the
definition of \(s^0=c\). Since \(\lVert a\rVert_\infty<1\), the point is strictly
positive. The two slack blocks sum to \(2e\), so \(\mu^0=1\), while

\[
 X^0s^0-\mu^0e=(a,-a),
 \qquad \lVert(a,-a)\rVert_2=\delta.
\]

This proves the neighborhood claim. Because \(H\) is invertible,
\(\operatorname{null}(A)=\operatorname{range}(V)\). Substituting
\(\Delta x=V\lambda\) and \(\Delta s=-A^T\Delta y\) into the feasible centering
equation with target \(\sigma\mu^0e\) gives (22).

Apply the orthogonal row transformation

\[
 Q={1\over\sqrt2}\begin{bmatrix}-I&I\\I&I\end{bmatrix}.
\]

Then

\[
 Q M_{\rm OSS}
 =\sqrt2\begin{bmatrix}H&-D\\0&I\end{bmatrix}.           \tag{26}
\]

The triangular factor has constant norm, and its inverse is

\[
 \begin{bmatrix}H^{-1}&H^{-1}D\\0&I\end{bmatrix}.
\]

Because \(\lVert D\rVert\le\delta/\sqrt2\), its inverse norm is
\(\Theta_\delta(\lVert H^{-1}\rVert)\), proving (23). Applying \(Q\) to the right-hand
side and dividing by \(\sqrt2\) gives

\[
 H\Delta y-D\lambda=a,\qquad \lambda=-r e.
\]

Since \(De=a\), direct substitution gives
\(\Delta y=\sigma H^{-1}a\) and the stated physical step. At the endpoint,

\[
 A^Ty^1+s^1=(\sigma a,-\sigma a)+(e+r a,e-r a)=c,
 \qquad \mu^1={1\over2n}(x^1)^Ts^1=\sigma,
\]

so the step is feasible. Moreover,
\(X^1s^1-\mu^1e=\sigma r(a,-a)\), whose 2-norm is \(\sigma r\delta\) and whose infinity
norm is no larger. Relative to \(\mu^1\), both neighborhood residuals are at most
\(r\delta\le\theta\).

Finally, \(\lVert H^{-1}q\rVert\ge1\) because \(\lVert H\rVert=1\). Hence
\(\lVert\Delta y\rVert^2\ge\sigma^2\delta^2/2\), whereas
\(\lVert\lambda\rVert^2=r^2n=\alpha^2\), proving the block-probability bound. Because
\(\alpha\le\delta/4\) and \(\sigma\ge7/8\), in fact \(p_0\ge49/57>2/3\).

For completeness, let \(P_y\) project onto the \(\Delta y\) block. If normalized
states \(\lVert\phi-\psi\rVert\le\epsilon\),
\(\lVert P_y\psi\rVert\ge\sqrt{p_0}\), and
\(\epsilon\le\sqrt{p_0}/2\), the triangle inequality and normalization give

\[
 \left\lVert{P_y\phi\over\lVert P_y\phi\rVert}
       -{P_y\psi\over\lVert P_y\psi\rVert}\right\rVert
 \le {4\epsilon\over\sqrt{p_0}}.
\]

Thus projection changes all error thresholds by only a universal constant, and the
\(\log(1/\epsilon)\) asymptotics are unchanged. For \(\alpha=0\), there is no
conditioning loss.

All nontrivial matrix entries in (21)–(22) are entries of \(H\), plus known diagonal
terms. The vector \(q\) is explicit in the QLS hard families being transferred. In
Mori et al.'s clock construction, the possible positions are the identity and known
clock successor/predecessor positions; the hidden Boolean update is reversible, so both
row and column slot queries use \(O(1)\) source queries. Its operator norm also has a
known analytic scaling, so imposing \(\lVert H\rVert=1\) costs no query. This proves the
oracle claim for the transferred families. A general real QLS matrix \(J\), under
row-and-column sparse access, can first be replaced by
\(H=\left[\begin{smallmatrix}0&J\\J^T&0\end{smallmatrix}\right]\), which preserves
norm, condition number, and maximum row/column sparsity and embeds
\(J^{-1}q\) in the second flagged block when the dilated right-hand side is
\((q,0)\). Composing with Mori et al.'s reductions proves
(24)–(25). ∎

This is a lower bound for QLSA-based preparation of the OSS solution state to the stated
error. It does not lower-bound Apers–Gribling's spectral-sampling IPM, the quantum
central-path method, an inexact feasible move that bypasses accurate OSS-state
preparation, or an LP algorithm that bypasses the OSS. In this constructed LP the
physical \((\Delta x,\Delta s)\) is explicit; the hard component is \(\Delta y\).

An instructive formulation gap also appears in the unbalanced version of the
construction: its OSS has condition \(\kappa(H)\), while the unreduced three-block
primal-dual Jacobian has condition \(\Theta(\kappa(H)^2)\). Thus a lower bound must name
the actual Newton formulation; KKT and reduced-system conditions are not interchangeable.

## 5. Treewidth does not remove QLS condition/precision hardness

### Theorem 4 (treewidth-two KKT precision lower bound)

For a constant \(\epsilon_0>0\), there is a family of real symmetric, indefinite,
two-sparse matrices \(K\) such that

\[
 \operatorname{tw}(G_K)\le2
\]

and preparing an \(\epsilon\)-approximation to the normalized solution state of
\(Kz=\widehat b\), for \(0<\epsilon\le1/11\), requires

\[
  \Omega\!\left(\kappa(K)\log(1/\epsilon)\right)           \tag{27}
\]

sparse-matrix oracle queries in the parameter range of Mori et al.'s QLS lower bound.
Each \(K\) is a standard equality-KKT matrix.

#### Proof

Mori et al. construct a real matrix

\[
 A=I-\delta^{1/q}B,                                       \tag{28}
\]

where \(B\) is a clock permutation on basis states
\((u,t)\in\{0,1\}\times\mathbb Z_{3q}\). Each row and column of \(A\) contains an
identity entry and one permutation entry. Their reduction proves the
\(\Omega(\kappa(A)\log(1/\epsilon))\) QLS lower bound.

Form the symmetric dilation

\[
 K_A=\begin{bmatrix}0&A^T\\A&0\end{bmatrix},
 \qquad \widehat b=\binom0b.                              \tag{29}
\]

Then

\[
 K_A^{-1}\widehat b=\binom{A^{-1}b}{0},                  \tag{30}
\]

so the desired solution state is a flagged isometric embedding of Mori et al.'s hard
state. The singular values of \(K_A\) are those of \(A\), each repeated; hence
\(\kappa(K_A)=\kappa(A)\).

The support graph of \(K_A\) is bipartite. The identity entries of \(A\) give one
perfect matching and the permutation entries give a second. Their union has maximum
degree two and is a disjoint union of paths and even cycles, so its treewidth is at most
two. A row query to \(K_A\) requires the identity neighbor and either the known clock
successor or predecessor. Because the hidden update is an involution, this uses only a
constant number of queries to Mori et al.'s Boolean oracle. Their decision measurement
extends by the block flag, preserving the approximation gap up to a constant rescaling
of \(\epsilon\). This proves (27).

Finally, (29) is the KKT matrix of the equality-constrained convex program
\(\min 0\) subject to \(Ax=b\), in the variable order \((x,y)\). ∎

The theorem is intentionally about a QLS/KKT subproblem. It does not show that every LP
solver must use this KKT formulation, and it does not multiply the QLS lower bound by a
separate tomography lower bound.

### Theorem 4A (LP value hardness at exact treewidth)

For integers \(a,b,c\ge1\), let
\(\tau=c\), \(q=c+a\), and \(p=c+a(b+1)\). There are LPs with \(p\) nonnegative
variables and \(q\) inequality constraints whose constraint-intersection graph has
treewidth exactly \(\tau\), and for which constant-additive approximation of the
scalar optimal value requires

\[
 \Omega(\tau\sqrt{pq})                                    \tag{30a}
\]

quantum fixed-position coefficient queries when \(c\le a\), and
\(\Omega(p\tau)\) randomized queries in the same regime. A
whole-column query can reveal the \(\Theta(\tau)\) coefficients of one original
variable at once, so the corresponding whole-column quantum consequence is only
\(\Omega(\sqrt{pq})\). A whole top row is much stronger and can expose
\(\Theta(ab)\) hidden coefficients, so no analogous row-query bound is claimed.

#### Proof

The oracle in this statement returns the hidden Boolean coefficient \(Z_{ijk}\) at a
specified triple \((i,j,k)\); known coefficients require no query. It is an individual
fixed-position value oracle, not an oracle that lists an entire row or only actual
nonzeros. Use the pre-dual hard LP from Apers and Gribling. For
\(Z^i\in\{0,1\}^{c\times b}\), it is

\[
\begin{aligned}
 \max_{w,v^1,\ldots,v^a}\quad &\sum_{k=1}^c w_k\\
 \text{subject to}\quad
 &w-\sum_{i=1}^aZ^iv^i\le0,\\
 &e^Tv^i\le1\quad(i=1,\ldots,a),\\
 &w,v^i\ge0.
\end{aligned}                                             \tag{30b}
\]

Its value is

\[
 \sum_{i=1}^a\max_{j\in[b]}\sum_{k=1}^c Z_{ijk},          \tag{30c}
\]

and the source's Boolean reduction gives quantum lower bound
\(\Omega(a\sqrt b\,c)\) and randomized lower bound \(\Omega(abc)\).

To force exact rather than upper-bounded treewidth, add for each bottom constraint
\(i\) a nonnegative, zero-objective variable \(z_i\) with coefficient one in all
\(c\) top constraints and in bottom constraint \(i\). Setting \(z=0\) extends every
old feasible solution. Conversely, removing positive \(z\) only relaxes the constraints,
so every augmented feasible solution maps to an old feasible solution with the same
objective. The optimum is unchanged.

Let \(C\) be the set of \(c\) top constraint vertices. Each new column forces
\(C\cup\{i\}\) to be a clique, while no column contains two bottom vertices. The
graph is exactly \(K_c\vee I_a\), with bags \(C\cup\{i\}\), and therefore has
treewidth exactly \(c\).

The augmented dimensions are

\[
 q=c+a,\qquad p=c+a(b+1)=q+ab.                            \tag{30d}
\]

Set \(c=\tau\). Exactly,

\[
 a\sqrt b\,c=\tau\sqrt{(q-\tau)(p-q)},
 \qquad abc=\tau(p-q).                                    \tag{30e}
\]

When \(c\le a\), equivalently \(\tau\le q/2\), the two factors in the first product
are \(\Theta(q)\) and \(\Theta(p)\), respectively. This proves (30a), while the
randomized expression is \(\Theta(p\tau)\). Dummy padding extends the construction to
larger dimensions but does not justify the formula for arbitrary unrelated \((p,q)\).
The graph statement is symbolic: numerical entries of a particular diagonal-weight
normal matrix can cancel, while its constraint-intersection sparsity pattern remains
the stated graph. ∎

This theorem concerns the scalar value, so it has no tomography or dense-output
loophole. It is a structural reinterpretation and small augmentation of an existing
reduction, not a new Boolean adversary method.

### Corollary 3 (bounded-treewidth explicit-output ceiling)

For an SPD Newton system of dimension \(N\) with a supplied width-\(\tau\) elimination
ordering, ordinary scalar sparse Cholesky uses \(O(N\tau^2)\) arithmetic operations and
\(O(N\tau)\) factor storage/solve work. An unrestricted dense classical direction costs
\(\Omega(N)\) just to emit. Thus, against this comparator, no full-output algorithm can
obtain more than an \(O(\tau^2)\) factor in the dimension-only work model. For constant
\(\tau\), no polynomial-in-\(N\) full-output speedup is possible.

This ceiling is reinforced by stronger classical results: Dong, Lee, and Ye give an
end-to-end nearly linear robust IPM for bounded-treewidth LPs, and Gu and Song improve
the width dependence. The statement does not apply to quantum-state output,
objective-only output, or succinct sparse output.

## 6. Projective outlier-corrected reuse of normal matrices

Let \(A=[a_1\ \cdots\ a_n]\in\mathbb R^{m\times n}\) have full row rank and

\[
 H(w)=A\operatorname{Diag}(w)A^T=\sum_{i=1}^n w_i a_i a_i^T,
 \qquad w>0.                                               \tag{31}
\]

### Theorem 5 (projective outlier correction)

Let \(w\) be an old weight vector, \(w^+\) a new vector, \(\gamma>0\),
\(\tau\ge0\), and \(J\subseteq[n]\). Assume

\[
 \left|\log\frac{w_i^+}{\gamma w_i}\right|\le\tau
 \quad(i\notin J).                                        \tag{32}
\]

Define

\[
 p_i=\begin{cases}w_i^+,&i\in J,\\ \gamma w_i,&i\notin J,\end{cases}
 \qquad P=H(p).                                            \tag{33}
\]

Then

\[
 e^{-\tau}P\preceq H(w^+)\preceq e^\tau P,
 \qquad
 \kappa\!\left(P^{-1/2}H(w^+)P^{-1/2}\right)\le e^{2\tau}. \tag{34}
\]

Moreover,

\[
 P-\gamma H(w)
 =A_J\operatorname{Diag}(w_J^+-\gamma w_J)A_J^T,
 \qquad \operatorname{rank}(P-\gamma H(w))\le|J|.         \tag{35}
\]

If a seed preconditioner \(M\succ0\) obeys \(aM\preceq P\preceq bM\) for
\(0<a\le b\), then

\[
 \kappa(M^{-1/2}H(w^+)M^{-1/2})\le(b/a)e^{2\tau}.         \tag{36}
\]

#### Proof

For every coordinate, (32) or equality on \(J\) gives
\(e^{-\tau}p_i\le w_i^+\le e^\tau p_i\). Multiply by the positive semidefinite
matrix \(a_i a_i^T\), sum, and obtain (34). Equation (35) is direct, and (36) follows
by chaining the Loewner inequalities. ∎

This theorem is robust to arbitrary-magnitude changes in the corrected coordinates and
factors out a global scale, which is irrelevant to condition number. Proposition 3
optimizes this coordinate-ratio certificate; dependencies among the columns of \(A\)
can make the actual preconditioned condition number smaller.

### Proposition 3 (optimal correction set for a fixed budget)

Let \(r_i=\log(w_i^+/w_i)\), sorted as
\(r_{(1)}\le\cdots\le r_{(n)}\). With at most \(k\) corrected coordinates, the
smallest feasible \(\tau\) in (32), for \(0\le k<n\), is

\[
 \tau_k={1\over2}\min_{1\le j\le k+1}
 \left[r_{(j+n-k-1)}-r_{(j)}\right].                      \tag{37}
\]

Choose the \(n-k\) ratios in the shortest displayed window, choose \(\log\gamma\) as
its midpoint, and correct the complement. This is optimal because every interval
covering \(n-k\) sorted points contains one of these consecutive windows.

### Theorem 6 (online projective lazy refresh)

Let \(\ell^t=\log w^t\), \(t=0,\ldots,T\), and let \(g_t\) be any supplied scalar
sequence. Initialize \(c_0=0\) and \(q_i^0=\ell_i^0\). At step \(t\), set

\[
 c_t=c_{t-1}+g_t,
 \qquad e_i^t=\ell_i^t-(c_t+q_i^{t-1}).                   \tag{38}
\]

If \(|e_i^t|>\tau\), reset \(q_i^t=\ell_i^t-c_t\); otherwise leave
\(q_i^t=q_i^{t-1}\). Define

\[
 \widehat w_i^t=e^{c_t+q_i^t},\qquad
 \widehat H_t=H(\widehat w^t),
\]

and let \(R\) be the total number of coordinate resets. Then

\[
 e^{-\tau}\widehat H_t\preceq H(w^t)\preceq e^\tau\widehat H_t
 \quad\text{for every }t,                                 \tag{39}
\]

and, for \(\tau>0\),

\[
 R\tau
 \le V(g):=\sum_{t=1}^T\lVert\Delta\ell^t-g_t e\rVert_1. \tag{40}
\]

Choosing \(g_t\) as a median of the coordinate increments minimizes each summand and
gives

\[
 R\le {V_{\rm proj}\over\tau},\qquad
 V_{\rm proj}:=\sum_t\min_g\lVert\Delta\ell^t-ge\rVert_1. \tag{41}
\]

#### Proof

After each step, a reset coordinate has zero log error and a retained coordinate has
absolute log error at most \(\tau\). Exponentiation, multiplication by
\(a_i a_i^T\), and summation prove (39).

For a fixed coordinate, after its previous reset at time \(s\), its provisional error
at a later reset time \(t\) is

\[
 \sum_{r=s+1}^t(\Delta\ell_i^r-g_r).
\]

Its absolute value exceeds \(\tau\), so the sum of the absolute centered increments
over that event interval exceeds \(\tau\). These event intervals are disjoint for each
coordinate. Sum first over reset events and then over coordinates to obtain (40).
The median minimizes scalar \(\ell_1\) deviation, proving (41). ∎

If the trigger is \(|e_i^t|\ge\tau\) and \(\tau>0\), retained coordinates satisfy a
strict spectral bound. At \(\tau=0\), the division bound is inapplicable. The variation
bound is tight up to threshold rounding: take half the log increments equal to \(+h\)
and half equal to \(-h\) at every step.

Computing an exact median in the usual unstructured value/comparison-oracle model costs
\(\Omega(n)\) accesses. Therefore (41) is directly useful when the iterate is already classical, as
in a tomography-based hybrid QIPM, or when a projective scale is structurally known. If
an approximate median \(\widetilde g_t\) satisfies
\(|\widetilde g_t-g_t^*|\le\zeta_t\), then

\[
 V(\widetilde g)\le V_{\rm proj}+n\sum_t\zeta_t.          \tag{42}
\]

The projective variation is an accounting potential for this coordinatewise policy,
not an intrinsic lower bound on operator change. Repeated or dependent columns can
make weight changes cancel in \(H(w)\) even while \(V_{\rm proj}>0\).

### Corollary 4 (short-step variation estimate)

For LP normal weights \(w=x/s\), write

\[
 u^t={\Delta x^t\over x^{t-1}},\qquad
 v^t={\Delta s^t\over s^{t-1}}.
\]

If \(\lVert u^t\rVert_\infty,\lVert v^t\rVert_\infty\le\rho<1\) and
\(\lVert u^t\rVert_2+\lVert v^t\rVert_2\le B\), then

\[
 V_{\rm proj}
 \le\sum_t\lVert\Delta\log w^t\rVert_1
 \le {BT\sqrt n\over1-\rho}.                              \tag{43}
\]

This uses \(|\log(1+z)|\le|z|/(1-\rho)\) and
\(\lVert z\rVert_1\le\sqrt n\lVert z\rVert_2\). For
\(T=O(\sqrt n L)\), the lazy rule gives
\(R=O(BnL/[\tau(1-\rho)])\), versus \(nT=O(n^{3/2}L)\) naive coordinate rewrites.

If column \(i\) of \(A\) has \(d_i\) nonzeros, one reset changes at most
\(d_i(d_i+1)/2\) entries of a materialized symmetric normal matrix. Total touched
entries of the stored scale-free matrix \(H(e^q)\) are at most
\(\sum_{\rm resets}d_i^2\le d_{\max}^2R\). The represented matrix
\(\widehat H=e^cH(e^q)\) globally rescales when \(c\) changes, so materializing that
scale would touch every entry. A factorized
\(A\)-diagonal-\(A^T\) oracle changes one diagonal word instead, but neither bound
controls fill changes in a Cholesky factor.

### Corollary 5 (warm start and energy-state fidelity)

If \(\delta\ge0\), \(b\ne0\), and

\[
 e^{-\delta}\gamma H\preceq H^+\preceq e^\delta\gamma H,
\]

let \(x^+=(H^+)^{-1}b\) and \(x_0=(\gamma H)^{-1}b\). Then

\[
 {\lVert x^+-x_0\rVert_{H^+}\over\lVert x^+\rVert_{H^+}}
 \le e^\delta-1.                                          \tag{44}
\]

Richardson refinement with preconditioner \(\gamma H\) contracts in the
\(\gamma H\)-norm by \(e^\delta-1\) when \(\delta<\log2\). The squared fidelity of
the two normalized solution vectors in the \(\gamma H\) inner product is at least
\(\operatorname{sech}^2\delta\). These follow by diagonalizing
\((\gamma H)^{-1/2}H^+(\gamma H)^{-1/2}\) and applying the Kantorovich angle
inequality.

### Proposition 4 (why this is not an ordinary QLSA warm-state theorem)

Fix \(a\in(0,1/2)\). For \(\varepsilon>0\), define

\[
 A_\varepsilon=
 \begin{bmatrix}1&0&1&1\\0&1&\varepsilon^2&-\varepsilon^2\end{bmatrix},
\]

with weights

\[
 w=(1/2,\varepsilon^4/2,1/4,1/4),
\quad
 w^+=(1/2,\varepsilon^4/2,(1+2a)/4,(1-2a)/4).
\]

Direct calculation gives

\[
 H=\operatorname{Diag}(1,\varepsilon^4),\qquad
 H^+=\begin{bmatrix}1&a\varepsilon^2\\a\varepsilon^2&\varepsilon^4\end{bmatrix}.
\]

Thus \((1-a)H\preceq H^+\preceq(1+a)H\) uniformly in \(\varepsilon\). For
\(b=e_1\), however,

\[
 H^{-1}b=e_1,
 \qquad
 (H^+)^{-1}b={1\over1-a^2}(1,-a/\varepsilon^2),
\]

so the overlap of the ordinary Euclidean normalized solution states tends to zero as
\(\varepsilon\to0\). Relative Loewner closeness alone controls energy geometry, not
the standard QLSA output state; underlying conditioning is necessary.

## 7. Conditional sparse readout: what remains possible

The support barrier concerns the materialized primal/slack update. It does not forbid a
sparse latent QLSA solution with a nonlocal reconstruction map.

The sparse tomography theorem of van Apeldoorn et al. implies the following modular
substitution. If the normalized \(N\)-dimensional solution state at iteration \(t\) is
effectively \(s_t\)-sparse at the required \(\ell_2\) tolerance \(\xi_t\), controlled
preparation-unitary access recovers a classical sparse description, up to global
phase, using

\[
 \widetilde O(s_t/\xi_t)                                  \tag{45}
\]

calls, replacing the dense \(\widetilde O(N/\xi_t)\) factor. To turn that state into a
Newton vector, also assume a relative-\(O(\xi_t)\) estimate of \(\lVert z_t\rVert\)
and a reference that fixes the real global sign; their costs are separate. Normalize
\(\lVert H_t\rVert=1\). For \(H_tz_t=h_t\), if an inexact IPM requires
\(\lVert H_t\widehat z_t-h_t\rVert\le\eta\mu_t\), and
\(\lVert h_t\rVert\le C\mu_t\), relative vector accuracy
\(\xi_t=\Theta(\eta/(C\kappa_t))\) suffices. Readout then costs

\[
 \widetilde O(s_t C\kappa_t/\eta)                         \tag{46}
\]

solution-unitary calls, rather than the same expression with \(N\).

This is a valid conditional improvement to a modular QIPM, but it has four binding
limits:

- Norm estimation and recovery of a consistent real sign must be supplied and charged.
- The effective sparsity promise is required at condition-dependent precision; sparse
  input does not imply it.
- In OSS coordinates, multiplying by \(V\) and \(A^T\) can densify the physical step.
- Theorems 1 and Corollary 1 show that a standard short-step full update cannot have
  latent sparsity times reconstruction locality equal to \(o(n)\); in particular,
  constant-locality reconstruction forces linear latent support.

Accordingly, (46) is most plausible for a compressed output contract, a structured
nonlocal dictionary, or an algorithm that keeps the iterate implicit. It is not an
automatic end-to-end speedup for ordinary hybrid QIPMs.

## 8. Quantum implementation scope of lazy refresh

Theorems 5–6 unconditionally prove algebraic spectral and update-count statements. A
quantum refresh saving additionally requires:

1. a static sparse or block encoding of \(A\);
2. a mutable coherent oracle for the stored log weights \(q_i\), with a declared word
   update cost;
3. a factorized encoding of \(A\operatorname{Diag}(e^q)A^T\) whose circuit topology
   can be reused; and
4. external handling of the global scalar \(e^c\).

Under that model the diagonal memory changes only \(n+R\) times. Rebuilding a separate
inverse or factor every \(K\) threshold events gives at most \(\lfloor R/K\rfloor\)
rebuilds, but its rebuild cost must still be charged.

The reset theorem counts writes, not the accesses needed to discover threshold
violations. Without a maintained event data structure or stronger iterate access,
finding every violation requires a scan, and merely deciding whether any violation
exists is an unstructured-search task. Thus \(R\) alone is not a quantum runtime bound.

Low rank does not make quantum inverse updates free. A Woodbury implementation needs a
stable \(|J|\times|J|\) core, reusable old inverse-state preparation, and overlap
estimation. Even one downdate can make the core arbitrarily ill-conditioned. Likewise,
separately normalized encodings of \(H\) and \(H^{-1}\) can encode their exact product
with a poor normalization: for
\(H=\operatorname{Diag}(1,\varepsilon)\), the natural normalizations are
\(1\) and \(1/\varepsilon\), leaving an effective inverse scale
\(1/\varepsilon\) although \(H^{-1}H=I\). Direct product encoding or a stronger
problem-specific access model is required.

## 9. Novelty search and nearest prior art

The searches were run on 2026-09-02 across the repository literature base, arXiv,
journal full text where open, and web indexes. Exact combinations included “quantum
interior point” with “sparse Newton direction,” “sparse tomography,” “treewidth,”
“chordal,” “separator,” “dynamic diagonal weights,” and “low-rank update.” Negative
search evidence is not proof of priority.

### Complementarity and sparse readout

No source found states Theorem 1, the locality product (4), or Proposition 2. The
closest lines are:

- van Apeldoorn, Cornelissen, Gilyén, and Nannicini,
  [*Quantum tomography using state-preparation unitaries*](https://arxiv.org/abs/2207.08800),
  Section 5.3, which proves sparse-vector tomography but does not connect it to IPM
  complementarity or iterate updates;
- Bellante, Vanerio, and Zanero,
  [*Quantum Sparse Recovery and Quantum Orthogonal Matching Pursuit*](https://arxiv.org/abs/2510.06925),
  which treats sparse recovery in nonorthogonal dictionaries under incoherence and
  conditioning promises, but does not preserve an IPM neighborhood; and
- Zanetti and Gondzio,
  [a sparse-support IPM-inspired optimal-transport method](https://arxiv.org/abs/2206.11009),
  which deliberately restricts supports but is not a QIPM and does not prove the
  complementarity support barrier.

### Perfectly conditioned sparse LP hardness

The closest general LP result is Apers and Gribling,
[*Quantum Speedups for Linear Programming via Interior Point Methods*](https://arxiv.org/abs/2311.03215),
Theorem 8.4, which proves sparse-query LP lower bounds using hardness encoded in the
constraint matrix. No source found gives the fixed-constraint box family (11), its
condition-one central trajectory, or its sparse reduced-variable optimum
specialization. The quantum
parity, adversary, oracle-interrogation, and state-tomography ingredients themselves are
established; the contribution is their sparse-IPM embedding.

### Treewidth

The broad statement that treewidth had not appeared in QLS lower-bound work would be
false: [Khanpour and Talkington (2026)](https://arxiv.org/abs/2607.19263) combine
bounded-treewidth Laplacian conditioning with QLS/readout lower bounds. The narrower
claim here is that no searched source
states the treewidth-two **precision** restriction in Theorem 4. Its main components
and controls are:

- Mori, Kikuchi, Benedetti, and Rosenkranz,
  [*Sparsity-dependent Complexity Lower Bound of Quantum Linear System Solvers*](https://arxiv.org/abs/2601.16697),
  which proves the lower bound transferred in Theorem 3 but does not identify the
  treewidth-two KKT restriction;
- [Wang and Zhang's 2024 QLS lower-bound construction](https://arxiv.org/abs/2407.06012)
  already uses a two-sparse
  Hermitian clock dilation whose support is likewise a union of two matchings. They do
  not state the treewidth/KKT interpretation and do not obtain Mori et al.'s
  \(\log(1/\epsilon)\) precision factor;
- Dong, Lee, and Ye,
  [*A Nearly-Linear Time Algorithm for Linear Programs with Small Treewidth*](https://arxiv.org/abs/2011.05365),
  and Gu and Song,
  [*A Faster Small Treewidth SDP Solver*](https://arxiv.org/abs/2211.06033), which
  establish strong classical baselines; and
- Zhang,
  [*Complexity of Chordal Conversion for Sparse SDPs with Small Treewidth*](https://arxiv.org/abs/2306.15288),
  which shows that ordinary aggregate sparsity is the wrong SDP parameter; extended
  aggregate treewidth is needed.

No source found states Theorem 4A's
\(\Omega(\tau\sqrt{pq})\) coefficient-query lower bound at exact
constraint-intersection treewidth. Because it is obtained by reparameterizing and
slightly augmenting Apers–Gribling's published hard family, its novelty should be
described as a new structural corollary rather than a new lower-bound technique.

### Feasible QIPM lower-bound transfer

No searched source embeds the sparse-QLS lower bounds into a strictly feasible,
standard-neighborhood OSS progress step while preserving sparsity and condition number.
[Mohammadisiahroudi et al.](https://arxiv.org/abs/2307.14445) introduce the feasible
OSS formulation and prove its IPM iteration guarantees, but do not give such a QLS
lower-bound embedding.
Theorem 3 directly fills the QIPM-specific gap identified by the audit of the earlier
repository note. Its ingredients—symmetric dilation, null-space feasible directions,
and Mori et al.'s QLS lower bounds—are known; the balanced LP/OSS construction,
constant-probability hard block, and neighborhood-preserving short-step landing are the
apparently new parts.

Binkowski's 2026
[*Practical lower bounds for hybrid quantum interior point methods in linear
programming*](https://arxiv.org/abs/2604.24362) benchmarks OSS and modified-normal-system
QLSA costs on concrete LP instances. It does not give an oracle reduction of the form
in Theorem 3.

### Dynamic normal-matrix reuse

Low-rank diagonal updates themselves are classical prior art and are not claimed as
new. The closest source is Wang and O'Leary,
[*Adaptive Use of Iterative Methods in Predictor-Corrector Interior Point Methods for
LP*](https://www.cs.umd.edu/users/oleary/reprints/j55.pdf), which writes changing normal
matrices as rank-one weight updates and corrects selected large changes. Bellavia et al.
also study
[diagonally modified sequences](https://epubs.siam.org/doi/10.1137/110860707) and
[KKT low-rank corrections](https://epubs.siam.org/doi/10.1137/130947155).

[Baryamureeba](https://nru.uncst.go.ug/server/api/core/bitstreams/62e718e0-3d99-47ec-a4ed-41ad560f4924/content)
already proves the extremal diagonal-ratio eigenvalue bound and recommends
correcting the largest and smallest ratios to minimize the resulting condition bound;
Bellavia et al. reproduce this low-rank update principle. Proposition 3 is therefore a
log-coordinate restatement of known ratio sorting, not a novelty claim. Lee and
Sidford's [inverse-maintenance framework](https://arxiv.org/abs/1503.01752) also
already lazily refreshes diagonal weights
after multiplicative threshold crossings. The more limited contribution here is the
projective \(\ell_1\)-variation accounting in (40)–(41), together with the explicit
separation between energy-geometry reuse and ordinary QLSA state reuse. Even the
variation accounting should be presented as a refinement of established inverse
maintenance rather than a standalone new preconditioning method.

## 10. What is established and what is not

The internally verified, apparently new results or structural refinements are:

- the complementarity support lower bound, its latent locality tradeoff, and the
  constant-row/column-sparsity incompressible-direction example;
- the fixed-pattern box-LP query lower bound with condition-one central Hessians;
- the query-preserving embedding of sparse-QLS hardness into a legitimate feasible OSS
  progress step;
- the treewidth-two restriction of the QLS condition/precision lower bound;
- the exact-treewidth LP value-query lower bound; and
- the projective-variation refinement of established lazy diagonal maintenance.

None of these proves a universal lower bound for every quantum optimization algorithm.
The support result is specific to standard complementarity-based directions. The box
LP uses a coefficient oracle and classical/value output. The OSS construction uses a
trivial LP; only its dual direction is hard, so it lower-bounds the QLSA short-step
subroutine rather than end-to-end LP optimization. The treewidth-two result
is for an indefinite equality-KKT solve, and Theorem 4A is a structural corollary of an
existing adversary reduction. Finally, the projective ledger needs an explicit event
detector and dynamic quantum access implementation before it gives any runtime saving.

The most promising paper-level package is therefore not “sparsity never helps.” It is a
sharper phase boundary:

> Sparse matrices and sparse optima do not make full short-step QIPM updates sparse,
> and bounded treewidth or perfect conditioning separately do not remove black-box
> hardness. Small projective variation of changing normal weights is a plausible reuse
> parameter, but turning its reset ledger into a quantum runtime improvement remains
> open.
