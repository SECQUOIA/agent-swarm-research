# Sparse SDP central mixtures: an operator-Kantorovich phase boundary

Date: 2026-09-02

Verification update (2026-09-20): the current theorem statements are in
`paper/sections/14-structural-tools.tex`, subsection “Central mixtures in
semidefinite programming.” The [Lean report](../../../formal/SDP_MIXTURE.md)
maps the verified matrix, residual, decoder, and soundness results and
records their scope. The current paper makes positivity, nonnegative
thresholds, and the fixed support convention explicit, and includes the
sharper signed KKT constant below. The worst-case Frobenius ratio criterion
in Section 4 is sharp for common-parameter centering and sufficient for
point centering; it is not asserted necessary for point centering.
This note remains an archival derivation, not an independent current
authority for the theorem statements.

## Status and contribution

This note proves an SDP analogue of the LP stationarity-preserving
single-flip mixture theorem. The matrix arithmetic--harmonic mean inequality
and its Kantorovich reverse are classical. The useful apparently new
conjunction is:

1. average exact SDP centers from neighboring coefficient instances;
2. retain positive definiteness and the exact algebraic gap;
3. control simultaneous primal and dual-stationarity residuals by sparse
   coefficient locality; and
4. control the noncommutative complementarity neighborhood by an exact matrix
   variance identity and a sharp spectral-ratio bound.

No commutativity among the neighboring primal matrices is assumed.

## 1. SDP family and sparse access model

Let \(\mathbb S^r\) be the real symmetric \(r\times r\) matrices. For
\(\sigma\in\{-1,+1\}^N\), consider
\[
 \begin{aligned}
  \text{minimize}\quad &\langle C,X\rangle\\
  \text{subject to}\quad
  &{\cal A}_\sigma(X)=b,\qquad X\succeq0,
 \end{aligned}
\tag{1}
\]
with dual
\[
 \begin{aligned}
  \text{maximize}\quad &b^\top y\\
  \text{subject to}\quad
  &{\cal A}_\sigma^*(y)+S=C,\qquad S\succeq0.
 \end{aligned}
\tag{2}
\]
The right-hand side \(b\) and cost matrix \(C\) are common to every input.
Writing
\[
 [{\cal A}_\sigma(X)]_a
 =\langle F^\sigma_a,X\rangle,
\]
fix a Frobenius-isometric symmetric vectorization
\[
 \operatorname{svec}:\mathbb S^r\longrightarrow\mathbb R^d,
 \qquad d=r(r+1)/2.
\]
The vectorized measurement matrix \(A_\sigma\in\mathbb R^{q\times d}\)
has row \(a\) equal to \(\operatorname{svec}(F^\sigma_a)^\top\), so
\[
 {\cal A}_\sigma(X)=A_\sigma\operatorname{svec}(X),
 \qquad
 \operatorname{svec}({\cal A}_\sigma^*(y))=A_\sigma^\top y.
\]

Assume a fixed union support for \(A_\sigma\). Every input-dependent
coordinate position depends on one designated raw bit, its magnitude is at
most \(B\), and there are \(M_{\rm dep}\) such positions. Let
\[
 s_r=\max_a|\operatorname{supp}(A_\sigma)_{a,:}|,
 \qquad
 s_c=\max_j|\operatorname{supp}(A_\sigma)_{:,j}|.
\]
All these quantities are defined after the fixed svec transformation. This is
essential: sparsity of a matrix before vectorization is not by itself a sparse
measurement-oracle statement.

Fix a base input \(\sigma\), and let \(\sigma^{(i)}\) flip bit \(i\). Suppose
the \(i\)-th neighboring instance has an exact center at a common barrier
parameter \(\mu>0\):
\[
 {\cal A}_{\sigma^{(i)}}(X_i)=b,
 \qquad
 {\cal A}_{\sigma^{(i)}}^*(y_i)+S_i=C,
 \qquad
 X_iS_i=\mu I.
\tag{3}
\]
Thus
\[
 X_i\succ0,\qquad S_i=\mu X_i^{-1}\succ0.
\tag{4}
\]
Existence of these selected centers is assumed. The theorem does not require
uniqueness of \(y_i\), surjectivity of \({\cal A}_{\sigma^{(i)}}\), or full
row rank.
Assume
\[
 mI\preceq X_i\preceq MI
\quad\text{for every }i,
\qquad R=M/m,
\tag{5}
\]
and that every coordinate of
\(\operatorname{svec}(X_i),y_i,\operatorname{svec}(S_i)\) has magnitude at
most \(H\).
For the standard Frobenius-isometric svec convention, (5) and
\(S_i=\mu X_i^{-1}\) bound the matrix-coordinate parts by
\(\sqrt2 M\) and \(\sqrt2\mu/m\), respectively. Thus one may take
\[
 H=\max\{\sqrt2M,\sqrt2\mu/m,\max_i\|y_i\|_\infty\},
\]
although retaining \(H\) separately makes the oracle-resource accounting
clearer.

Define the uniform averages
\[
 \overline X=\frac1N\sum_iX_i,\qquad
 \overline y=\frac1N\sum_iy_i,\qquad
 \overline S=\frac1N\sum_iS_i.
\tag{6}
\]
Both \(\overline X\) and \(\overline S\) are positive definite.

## 2. Exact noncommutative variance identity

Define the scaled averaged complementarity matrix
\[
 Z=
 \overline X^{1/2}\frac{\overline S}{\mu}\overline X^{1/2}
 =
 \overline X^{1/2}
 \left(\frac1N\sum_iX_i^{-1}\right)
 \overline X^{1/2}.
\tag{7}
\]

**Lemma 1 (matrix multiplicative variance).** One has the exact identity
\[
 \boxed{
 Z-I
 =
 \overline X^{-1/2}
 \left[
 \frac1N\sum_i
 (X_i-\overline X)X_i^{-1}(X_i-\overline X)
 \right]
 \overline X^{-1/2}.}
\tag{8}
\]
In particular,
\[
 Z\succeq I,
\tag{9}
\]
with equality if and only if \(X_i=\overline X\) for every \(i\).

### Proof

Expanding the middle expression in (8) and using
\(\frac1N\sum_iX_i=\overline X\) gives
\[
 \begin{aligned}
 &\frac1N\sum_i
 (X_i-\overline X)X_i^{-1}(X_i-\overline X)\\
 &\qquad
 =\overline X
   \left(\frac1N\sum_iX_i^{-1}\right)\overline X
   -\overline X.
 \end{aligned}
\]
Congruence by \(\overline X^{-1/2}\) yields (8). Each summand before
congruence is positive semidefinite, proving (9). If their positive weighted
sum is zero, every summand is zero, hence every \(X_i=\overline X\).
\(\square\)

This is also a direct proof of the arithmetic--harmonic operator inequality
\[
 \frac1N\sum_iX_i^{-1}\succeq\overline X^{-1}.
\]
It does not reorder any noncommuting factors.

## 3. Sharp operator-Kantorovich centrality bound

**Theorem 2 (noncommutative central sandwich).** Under (5),
\[
 \boxed{
 I\preceq
 \overline X^{1/2}\frac{\overline S}{\mu}\overline X^{1/2}
 \preceq K(R)I,}
\qquad
 K(R)=\frac{(R+1)^2}{4R}.
\tag{10}
\]
Consequently,
\[
 \left\|
 \overline X^{1/2}\frac{\overline S}{\mu}\overline X^{1/2}-I
 \right\|_{\rm op}
 \le K(R)-1
 =\frac{(R-1)^2}{4R},
\tag{11}
\]
and
\[
 \left\|
 \overline X^{1/2}\overline S\overline X^{1/2}-\mu I
 \right\|_F
 \le \sqrt r\,[K(R)-1]\mu.
\tag{12}
\]

### Proof

The lower bound is Lemma 1. For the upper bound, functional calculus applied
to \(mI\preceq X_i\preceq MI\) gives
\[
 X_i+mM X_i^{-1}\preceq(m+M)I.
\tag{13}
\]
Average (13) and congruence by \(\overline X^{1/2}\):
\[
 Z
 \preceq
 \frac{(m+M)\overline X-\overline X^2}{mM}.
\tag{14}
\]
The spectrum of \(\overline X\) is contained in \([m,M]\). For every
\(\lambda\in[m,M]\),
\[
 \frac{\lambda(m+M-\lambda)}{mM}
 \le\frac{(m+M)^2}{4mM}=K(R).
\]
Applying this scalar bound to the spectral decomposition of
\(\overline X\) proves the upper bound in (10). Equations (11)--(12) follow
from the eigenvalue interval. \(\square\)

The proof does not assume that the \(X_i\) commute with one another or with
\(\overline X\). The only functional-calculus steps apply to one matrix at a
time or to \(\overline X\). The constant is sharp under hypothesis (5):
already for scalar \(X_i\), an equal mixture of \(m\) and \(M\) has
\(Z=((m+M)/2)((m^{-1}+M^{-1})/2)=K(R)\).

### Corollary 3 (instance-specific matrix-variance bounds)

The exact identity gives a stronger alternative when neighboring centers have
small additive matrix variance. Let \(w_i\ge0\), \(\sum_iw_i=1\), and define
\[
 X_w=\sum_iw_iX_i,\qquad
 S_w=\sum_iw_iS_i,\qquad
 D_i=X_i-X_w,
\]
\[
 Z_w=X_w^{1/2}(S_w/\mu)X_w^{1/2}.
\]
Assume only the common lower bound \(X_i\succeq mI\). Then
\[
 \boxed{
 \|Z_w-I\|_F
 \le\frac1{m^2}\sum_iw_i\|D_i\|_F^2,}
\tag{14a}
\]
and
\[
 \boxed{
 \|Z_w-I\|_{\rm op}
 \le\frac1{m^2}\sum_iw_i\|D_i\|_{\rm op}^2.}
\tag{14b}
\]

To prove the Frobenius bound, use the weighted form of (8):
\[
 Z_w-I
 =
 X_w^{-1/2}
 \left[\sum_iw_iD_iX_i^{-1}D_i\right]
 X_w^{-1/2}.
\]
Since \(X_w\succeq mI\) and \(X_i\succeq mI\),
\[
 \begin{aligned}
 \|Z_w-I\|_F
 &\le \|X_w^{-1/2}\|_{\rm op}^2
       \sum_iw_i\|D_iX_i^{-1}D_i\|_F\\
 &\le \frac1m\sum_iw_i
       \|D_i\|_{\rm op}\|X_i^{-1}\|_{\rm op}\|D_i\|_F\\
 &\le \frac1{m^2}\sum_iw_i\|D_i\|_F^2.
 \end{aligned}
\]
Replacing the Frobenius norm by the operator norm proves (14b). Both factors
\(m^{-1}\) are necessary in this proof: one comes from the outer congruence
and one from \(X_i^{-1}\).

The resulting complementarity residuals are
\[
 \|X_w^{1/2}S_wX_w^{1/2}-\mu I\|_F
 \le
 \frac{\mu}{m^2}\sum_iw_i\|X_i-X_w\|_F^2,
\tag{14c}
\]
\[
 \|X_w^{1/2}S_wX_w^{1/2}-\mu I\|_{\rm op}
 \le
 \frac{\mu}{m^2}\sum_iw_i\|X_i-X_w\|_{\rm op}^2.
\tag{14d}
\]
These bounds have no generic \(\sqrt r\) loss.

They also survive the standard recentering. Put
\[
 \mu_w=\frac{\langle X_w,S_w\rangle}{r}
 =\mu\alpha,\qquad
 \alpha=\frac{\operatorname{tr}Z_w}{r}\ge1.
\]
Writing \(E=Z_w-I\succeq0\), one has
\[
 \frac1{\mu_w}X_w^{1/2}S_wX_w^{1/2}-I
 =\frac{E-(\operatorname{tr}E/r)I}{\alpha}.
\]
Subtracting the scalar trace component is an orthogonal projection in
Frobenius norm, and all eigenvalues of \(E\) lie between zero and
\(\|E\|_{\rm op}\). Therefore the left side has Frobenius and operator norms
no larger than \(\|E\|_F\) and \(\|E\|_{\rm op}\), respectively. Equations
(14a)--(14d) thus hold, with the same right-hand sides, for neighborhoods
centered at \(\mu_w\).

Finally,
\[
 0\le
 \langle X_w,S_w\rangle-r\mu
 =\mu\operatorname{tr}(Z_w-I)
 \le
 \frac{\mu}{m^2}\sum_iw_i\|D_i\|_F^2.
\tag{14e}
\]
For the last inequality, put
\(Q=\sum_iw_iD_iX_i^{-1}D_i\succeq0\). Cyclicity of trace and the standard
bound \(\operatorname{tr}(AB)\le\|A\|_{\rm op}\operatorname{tr}B\) for
\(A,B\succeq0\) give
\[
 \operatorname{tr}(Z_w-I)
 =\operatorname{tr}(X_w^{-1}Q)
 \le\frac1m\sum_iw_i\operatorname{tr}(X_i^{-1}D_i^2)
 \le\frac1{m^2}\sum_iw_i\|D_i\|_F^2.
\]

## 4. Gap and standard central-neighborhood conventions

Every neighboring center satisfies
\[
 \langle C,X_i\rangle-b^\top y_i
 =\langle S_i,X_i\rangle=r\mu.
\]
Therefore
\[
 \boxed{
 \langle C,\overline X\rangle-b^\top\overline y=r\mu.}
\tag{15}
\]
No common primal or dual objective value is assumed separately.

Let
\[
 \overline\mu
 =\frac{\langle\overline X,\overline S\rangle}{r}
 =\mu\,\frac{\operatorname{tr}Z}{r}.
\]
Theorem 2 gives
\[
 \mu\le\overline\mu\le K(R)\mu.
\tag{16}
\]
If the central neighborhood is centered at \(\overline\mu\), rather than at
the common input-center parameter \(\mu\), then every eigenvalue of
\[
 \overline\mu^{-1}
 \overline X^{1/2}\overline S\overline X^{1/2}
\]
lies in \([1/K(R),K(R)]\). Hence its operator-norm distance from \(I\) is
still at most \(K(R)-1\).

Because the average is generally infeasible for the base instance,
\(\langle C,\overline X\rangle-b^\top\overline y\) need not equal
\(\langle\overline X,\overline S\rangle\). Their discrepancy satisfies
\[
 0\le
 \langle\overline X,\overline S\rangle-
 [\langle C,\overline X\rangle-b^\top\overline y]
 \le r[K(R)-1]\mu.
\tag{17}
\]
Indeed, the left-hand side of (17) equals
\(\mu\operatorname{tr}Z-r\mu\), so (17) is exactly the trace consequence of
\(I\preceq Z\preceq K(R)I\). It is not a weak-duality assertion at the
base-instance-infeasible averaged point.

Many SDP IPMs use the Frobenius narrow neighborhood
\[
 \|X^{1/2}SX^{1/2}-\mu I\|_F\le\eta_F\mu.
\]
The spectral-ratio hypothesis alone guarantees this only when
\[
 \sqrt r\,[K(R)-1]\le\eta_F.
\tag{18}
\]
Thus a constant \(R>1\) gives a dimension-free operator neighborhood, but
not automatically a dimension-free Frobenius narrow neighborhood. The exact
variance identity (8) can give a smaller instance-specific Frobenius defect.

The worst-case common-parameter high-dimensional phase law is explicit:
\[
 K(R)-1
 =\sinh^2\!\left(\frac{\log R}{2}\right).
\]
For fixed narrow-neighborhood width \(\eta_F\), condition (18) is equivalent
to
\[
 \log R
 \le
 2\operatorname{arsinh}\!\left(\sqrt{\eta_F}\,r^{-1/4}\right)
 =O(r^{-1/4}).
\tag{18a}
\]
The equal mixture of \(mI\) and \(MI\) attains \(Z=K(R)I\), so this
criterion is sharp for common-parameter centering. It is sufficient for
point centering, but that same example has zero point-centered width and
does not prove necessity under that convention. Thus the common-parameter
worst-case guarantee requires global spectral-ratio control to tighten
with matrix dimension.
By contrast, Corollary 3 gives the dimension-free sufficient condition
\[
 \frac1{m^2N}\sum_i\|X_i-\overline X\|_F^2\le\eta_F
\tag{18b}
\]
for the uniform mixture. Neighboring centers can therefore have a larger
global spectral ratio while remaining in a fixed Frobenius narrow
neighborhood if their actual matrix variance is small.

## 5. Sparse primal--dual residual

Under svec, stack the primal and dual linear equations as
\[
 \begin{bmatrix}
 A_\sigma&0&0\\
 0&A_\sigma^\top&I
 \end{bmatrix}
 \begin{bmatrix}
 \operatorname{svec}(X)\\y\\\operatorname{svec}(S)
 \end{bmatrix}
 =
 \begin{bmatrix}
 b\\\operatorname{svec}(C)
 \end{bmatrix}.
\tag{19}
\]
The free vector \(y\) need not be sign-split: the feasible domain
\(\mathbb S_+^r\times\mathbb R^q\times\mathbb S_+^r\) is convex, and the
single-flip residual proof uses only linearity and coordinate bounds.

Put
\[
 s_{\rm KKT}=\max\{s_r,s_c+1\},
 \qquad
 B_{\rm KKT}=\max\{B,1\}.
\tag{20}
\]
Each input-dependent position of \(A_\sigma\) appears once in the primal
block and once in the dual block. The vectorized one-bit mixture theorem
therefore gives the separate estimates
\[
 \|{\cal A}_\sigma(\overline X)-b\|_2^2
 \le \frac{4B^2H^2s_rM_{\rm dep}}{N^2},
 \qquad
 \|\operatorname{svec}({\cal A}_\sigma^*(\overline y)
       +\overline S-C)\|_2^2
 \le \frac{4B^2H^2s_cM_{\rm dep}}{N^2}.
\tag{20a}
\]
Indeed, a changed coefficient differs from its base value by at most \(2B\).
Cauchy--Schwarz is then applied once within each affected primal row and once
within each affected dual column. Consequently,
\[
 \|r_p\|_2^2+\|r_d\|_2^2
 \le \frac{4B^2H^2(s_r+s_c)M_{\rm dep}}{N^2}
 \le \frac{8B_{\rm KKT}^2H^2s_{\rm KKT}M_{\rm dep}}{N^2},
\tag{20b}
\]
which gives
\[
 \boxed{
 \left\|
 \begin{bmatrix}
 {\cal A}_\sigma(\overline X)-b\\
 \operatorname{svec}(
 {\cal A}_\sigma^*(\overline y)+\overline S-C)
 \end{bmatrix}
 \right\|_2
 \le
 \frac{2B_{\rm KKT}H
       \sqrt{2s_{\rm KKT}M_{\rm dep}}}{N}.}
\tag{21}
\]

For arbitrary convex weights \(w_i\), let \(M_i\) count the original
input-dependent measurement positions designated by bit \(i\). Then
\[
 \left\|
 \begin{bmatrix}
 {\cal A}_\sigma(X_w)-b\\
 \operatorname{svec}(
 {\cal A}_\sigma^*(y_w)+S_w-C)
 \end{bmatrix}
 \right\|_2^2
 \le
 8s_{\rm KKT}B_{\rm KKT}^2H^2\sum_iM_iw_i^2.
\tag{22}
\]
The exact variance identity (8) remains true with \(1/N\) replaced by
\(w_i\).

The factor two in the incidence count, rather than the LP split-dual factor
three, is intentional. The svec coordinates of \(X\) and \(S\) may be signed,
but positive semidefiniteness is a convex-cone constraint; coordinatewise
nonnegativity is not required. The identity block on \(S\) accounts for the
\(+1\) in \(s_{\rm KKT}\), but it contains no input-dependent coordinate and
therefore introduces no third occurrence in the incidence count.

## 6. Output hypotheses and the SDP phase boundary

Coefficient locality alone says nothing about an arbitrary nonlinear output
decoder. Two useful mixture-stable contracts are:

1. A fixed real affine score \(\Phi(X,y,S)\) obeys
   \[
   f(\xi)\Phi(X^\xi,y^\xi,S^\xi)\ge\gamma
   \]
   on every exact neighboring center. Because affine maps preserve convex
   averages, if every neighbor flips \(f\), then
   \(-f(\sigma)\Phi(\overline X,\overline y,\overline S)\ge\gamma\).
2. For an SDP-native quantum output, a fixed binary-POVM difference
   \(O=E_+-E_-\), equivalently a symmetric contraction
   \(\|O\|_{\rm op}\le1\), obeys
   \[
   f(\xi)\langle O,X^\xi\rangle
   \ge\gamma\,\operatorname{tr}X^\xi
   \tag{23}
   \]
   for every selected input \(\xi\), where \(0<\gamma\le1\) and
   \(f(\xi)\in\{-1,+1\}\) is the desired Boolean output.

If every single-bit neighbor flips \(f\), averaging (23) gives
\[
 -f(\sigma)
 \operatorname{tr}\left(
 O\,\frac{\overline X}{\operatorname{tr}\overline X}
 \right)\ge\gamma.
\tag{24}
\]
Thus the normalized density matrix
\(\overline X/\operatorname{tr}\overline X\) has a constant bias toward the
wrong output: the POVM outcome has success probability at least
\((1+\gamma)/2\) for the wrong sign. This is a statement about a robust output
contract, not an algorithm for preparing the density matrix. Explicitly,
every symmetric contraction defines the binary POVM
\(E_\pm=(I\pm O)/2\); no equality of the neighboring traces is needed because
both numerator and denominator in (24) average with the same weights.
This trace-scaled hypothesis is essential: it is exactly the statement that
each normalized density matrix \(X^\xi/\operatorname{tr}X^\xi\) has bias at
least \(\gamma\), and trace weighting preserves a common signed bias.  It says
nothing about the different vector-amplitude encoding
\(\lvert\operatorname{svec}(X)\rangle/\|X\|_F\), whose normalization is
nonlinear under convex averaging.

For clarity, the two operator widths used below are
\[
 \Theta_{\mu}^{\rm op}(X,S)
 =\left\|X^{1/2}\frac S\mu X^{1/2}-I\right\|_{\rm op},
 \qquad
 \Theta_{\rm pt}^{\rm op}(X,S)
 =\left\|X^{1/2}\frac S{\mu_{X,S}}X^{1/2}-I\right\|_{\rm op},
\]
where \(\mu_{X,S}=\langle X,S\rangle/r\).  Theorem 2 and Section 4 show that
both widths of \((\overline X,\overline S)\) are at most \(K(R)-1\).

For a precise phase-boundary statement, assume that all \(N\) single-bit
neighbors are sensitive, that one of the two fixed decoders above has its
stated margin on every neighboring exact center, and that a claimed
base-instance contract requires the correct output from **every**
positive-definite triple with:

- absolute Euclidean combined primal and dual residual at most
  \(\varepsilon\);
- algebraic objective difference \(r\mu\); and
- one specified width
  \(\Theta\in\{\Theta_\mu^{\rm op},\Theta_{\rm pt}^{\rm op}\}\) at most
  \(\theta\).

Then soundness requires
\[
 \boxed{
 \frac{8s_{\rm KKT}B_{\rm KKT}^2H^2M_{\rm dep}}{N^2}
 >\varepsilon^2
 \quad\text{or}\quad
 \frac{(R-1)^2}{4R}>\theta.}
\tag{25}
\]
Otherwise the averaged neighboring center satisfies the complete certificate
and reports the wrong output. Thus (25) is a necessary condition for this
quantified robust-output contract; the inequalities are strict because a
contract stated with “at most” accepts equality at either threshold.  It is
not a universal limitation on SDP algorithms.

For the point-centered convention, the algebraic objective condition remains
\(r\mu\), while the central parameter is
\(\overline\mu=\langle\overline X,\overline S\rangle/r\).  These quantities
need not agree at the base-infeasible mixture.  Therefore (25) does not cover
a different contract that additionally requires the algebraic objective
difference to equal \(r\overline\mu\).

Equation (25) uses no implicit residual normalization.  For a relative
contract \(\|r\|_2/D(X,y,S)\le\varepsilon_{\rm rel}\), its first alternative
must instead compare the left side with
\(\varepsilon_{\rm rel}^2D(\overline X,\overline y,\overline S)^2\).  A
denominator-free corollary requires an independently proved positive lower
bound on \(D\).

Define the uniform instance-specific variances
\[
 V_{\rm op}=\frac1N\sum_i\|X_i-\overline X\|_{\rm op}^2,
 \qquad
 V_F=\frac1N\sum_i\|X_i-\overline X\|_F^2.
\]
Corollary 3 strengthens the operator phase boundary (25) to
\[
 \frac{8s_{\rm KKT}B_{\rm KKT}^2H^2M_{\rm dep}}{N^2}
 >\varepsilon^2
 \quad\text{or}\quad
 \min\left\{
 \frac{(R-1)^2}{4R},\frac{V_{\rm op}}{m^2}
 \right\}>\theta.
\tag{25a}
\]

For a Frobenius neighborhood of width \(\eta_F\), the second alternative in
(25) is replaced by
\[
 \sqrt r\,\frac{(R-1)^2}{4R}>\eta_F,
\tag{26}
\]
unless the exact variance identity gives a sharper instance-specific norm.
This sufficient alternative is valid whether the Frobenius width is centered
at \(\mu\) or at the point-centered \(\overline\mu\): in the latter case,
divide \(\|Z-(\operatorname{tr}Z/r)I\|_F\) by
\(\operatorname{tr}Z/r\), which is at least one.
Including the instance-specific bound, the strongest stated necessary
dichotomy is
\[
 \boxed{
 \frac{8s_{\rm KKT}B_{\rm KKT}^2H^2M_{\rm dep}}{N^2}
 >\varepsilon^2
 \quad\text{or}\quad
 \min\left\{
 \sqrt r\,\frac{(R-1)^2}{4R},\frac{V_F}{m^2}
 \right\}>\eta_F.}
\tag{26a}
\]
The \(V_F/m^2\) alternative can avoid the generic \(\sqrt r\) loss when the
neighboring centers are tightly clustered in Frobenius norm.

For a Boolean function with only \(k\) sensitive bits at the base input,
average those \(k\) neighbors and restrict \(M_{\rm dep}\) to positions
designated by sensitive bits. The denominator \(N\) in (21) becomes \(k\).
This is a routine local-sensitivity extension, not a quantum query lower
bound.

## 7. Caveats

1. **Global spectral stability is strong.** Bounds
   \(mI\preceq X_i\preceq MI\) must hold in one common matrix basis. Upper
   coordinate bounds alone do not provide a lower eigenvalue or a bounded
   ratio \(R\).
2. **Operator versus Frobenius centrality.** A constant operator width becomes
   a \(\sqrt r\)-larger Frobenius bound. Claiming a standard narrow
   neighborhood from global ratio control requires (18), not merely constant
   \(R\).  The instance-specific bound (14a) has no *explicit* \(\sqrt r\)
   factor, but \(V_F\) itself may scale with \(r\); “dimension-free” here means
   that no further norm-conversion loss is imposed.
3. **A lower spectral bound is essential for the variance estimate.** The
   factors \(m^{-2}\) in (14a)--(14e) cannot be dropped under the stated
   assumptions.  Additive closeness of nearly singular centers does not by
   itself control their inverse-average Jensen gap.
4. **Fixed vectorization.** All sparsity, incidence, coefficient, and
   coordinate parameters in (21) are representation-dependent and must be
   measured after one fixed Frobenius-isometric svec map.
5. **Output stability is separate.** Vectorizing a PSD matrix does not make
   its coordinates nonnegative, and convex averaging need not preserve an
   arbitrary amplitude-state decoder. Condition (23) is a sufficient
   density-matrix output hypothesis.
6. **No query lower bound by itself.** The averaged point is existential. A
   separate query reduction is needed to turn a valid robust embedding into
   an oracle lower bound.
7. **The gap is algebraic at an infeasible point.** Equation (15) is exact,
   but weak duality does not apply to the base instance until the residuals
   vanish.

## 8. Literature and novelty calibration

Both matrix-mean ingredients are classical.  The arithmetic--harmonic
operator inequality belongs to the theory of positive-operator means; see
Kubo--Ando,
[*Means of positive linear
operators*](https://doi.org/10.1007/BF01371042), and Ando,
[*On the arithmetic-geometric-harmonic-mean inequalities for positive
definite matrices*](https://doi.org/10.1016/0024-3795(83)80005-6).  The
matrix Kantorovich reverse goes back at least to Marshall--Olkin,
[*Matrix versions of the Cauchy and Kantorovich
inequalities*](https://doi.org/10.1007/BF02112284).  In its positive-map
form, the operator inequality
\[
 \Phi(A^{-1})\preceq
 \frac{(M+m)^2}{4Mm}\Phi(A)^{-1}
\]
for a unital positive map is classical.  Theorem 2 is a direct specialization:
take \(A=\operatorname{diag}(X_1,\ldots,X_N)\) and let the unital positive
map average its diagonal blocks.  Congruence by
\(\overline X^{1/2}\) gives (10).  See also Lin,
[On an operator Kantorovich inequality for positive linear
maps](https://arxiv.org/abs/1212.5690), and Moradi, Gümüş, and Heydarbeygi,
[A glimpse at the operator Kantorovich
inequality](https://arxiv.org/abs/1708.04547). Matrix
arithmetic--harmonic-mean differences are also studied by Liao and Wu,
[Matrix inequalities for the difference between arithmetic mean and harmonic
mean](https://arxiv.org/abs/1501.04823). Therefore Theorem 2, standing alone,
is not new.  Identity (8) is an elementary exact expansion of the same
arithmetic--harmonic defect.  The note uses it because it exposes an
instance-specific Frobenius defect; it does not claim the algebraic identity
as a new matrix inequality.

The SDP central equations and the operator/Frobenius neighborhoods used here
are also standard.  See Vandenberghe--Boyd,
[*Semidefinite programming*](https://web.stanford.edu/~boyd/papers/sdp.html),
Monteiro,
[*Primal--dual path-following algorithms for semidefinite
programming*](https://doi.org/10.1137/S1052623495293056), and, for a current
computational treatment, Mohammadisiahroudi et al.,
[Quantum computing inspired iterative refinement for semidefinite
optimization](https://link.springer.com/article/10.1007/s10107-024-02183-z).
Infeasible-start SDP methods already track primal and dual residuals while
maintaining a central neighborhood; for example, Potra--Sheng,
[*A superlinearly convergent primal-dual infeasible-interior-point algorithm
for semidefinite programming*](https://doi.org/10.1137/S1052623495294955).
Those analyses concern iterates of one algorithm for one instance, not a
cross-instance average.

The nearest reoptimization comparison found is Chen--Goulart--Jones,
[*A warmstarting technique for general conic optimization in interior point
methods*](https://arxiv.org/abs/2512.00693).  Their smoothing operator turns
one previous optimum into a centered primal--dual warm start for a new conic
problem and proves \(O(\mu)\)-scale linear residuals, including for the PSD
cone.  This is a genuine collision with the broad slogan “centrality plus
small residual under data perturbation.”  It does not average the exact
centers of many single-bit neighboring instances, does not derive residuals
from a fixed sparse coefficient-incidence budget, and has no wrong-output or
Kantorovich-ratio phase boundary.  Classical warm-start and sensitivity
results should therefore be cited as context, but they do not imply
(21)--(26).

A targeted search on 2026-09-02 found no source combining these matrix-mean
facts with a single-flip sparse coefficient mixture, simultaneous primal and
dual-stationarity residual (21), exact algebraic gap (15), and a
mixture-stable wrong-output contract. The defensible apparent novelty is this
combined sparse-SDP **cross-instance obstruction**: coefficient locality gives
the \(N^{-1}\) residual scale, while spectral spread gives the independent
Kantorovich centrality width.  Neither the averaging principle, identity (8),
the operator Kantorovich inequality, standard SDP central neighborhoods, nor
warm starting is new in isolation.  Equation (25) is conditional on the
mixture-stable output hypotheses in Section 6 and is not a general SDP phase
transition or a quantum query lower bound.  No exact prior theorem with this
conjunction was found; that is evidence of apparent novelty, not proof of
priority.
