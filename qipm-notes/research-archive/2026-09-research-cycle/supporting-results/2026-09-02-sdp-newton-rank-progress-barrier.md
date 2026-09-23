# Rank--progress barrier for sparse SDP Newton directions

Date: 2026-09-02

## Main theorem

Low rank of an SDP optimum does not justify low-rank factorization of accurate
primal--dual Newton directions.  In Nesterov--Todd coordinates, complementarity
progress imposes a sharp aggregate-rank lower bound.

Consider one \(n\times n\) positive-semidefinite block at an exact central
point

\[
 XS=\mu I.
\]

Let \(W\) be the Nesterov--Todd scaling, so \(WSW=X\), put
\(P=W^{-1/2}\), and define the scaled directions

\[
 U=P\Delta X P^\top,
 \qquad
 V=P^{-\top}\Delta S P^{-1}.
\]

Write the symmetric scaled complementarity equation operationally as

\[
 \sqrt\mu(U+V)
 =-(1-\sigma)\mu I+\widetilde R.
\tag{1}
\]

This definition avoids ambiguities between residual conventions used in
different SDP-IPM papers.

If, for \(1\leq p<\infty\),

\[
 \|\widetilde R\|_{S_p}
 \leq \theta(1-\sigma)\mu n^{1/p},
 \qquad 0\leq\theta<1,
\tag{2}
\]

then

\[
 \boxed{
 \operatorname{rank}(\Delta X)+
 \operatorname{rank}(\Delta S)
 \geq \left\lceil(1-\theta^p)n\right\rceil.
 }
\tag{3}
\]

For spectral-norm error, the sharper statement is

\[
 \|\widetilde R\|_2<(1-\sigma)\mu
 \quad\Longrightarrow\quad
 \operatorname{rank}(\Delta X)+
 \operatorname{rank}(\Delta S)\geq n.
\tag{4}
\]

The same theorem holds blockwise on a product cone, with \(n\) replaced by
the sum of the PSD block orders.

### Proof

Congruence preserves rank, and

\[
 \operatorname{rank}(U+V)
 \leq\operatorname{rank}(U)+\operatorname{rank}(V)
 =\operatorname{rank}(\Delta X)+\operatorname{rank}(\Delta S)=:k.
\]

Equation (1) says that \(\widetilde R\) is the error of approximating
\((1-\sigma)\mu I\) by a rank-at-most-\(k\) matrix.  The
Eckart--Young--Mirsky theorem gives

\[
 \|\widetilde R\|_{S_p}
 \geq(1-\sigma)\mu(n-k)_+^{1/p}.
\]

Combining this with (2) proves (3).  If \(k<n\), then \(U+V\) has a nonzero
kernel vector, on which the residual in (1) has norm exactly
\((1-\sigma)\mu\), proving (4).

The rank--residual inequality is sharp as a matrix statement: take
\(U=-(1-\sigma)\sqrt\mu\operatorname{Diag}(I_k,0)\) and \(V=0\).  Then the
residual is exactly
\((1-\sigma)\mu\operatorname{Diag}(0,I_{n-k})\).

This statement is invariant under primal congruences
\(X\mapsto QXQ^\top\), \(S\mapsto Q^{-\top}SQ^{-1}\): the resulting scaled
directions differ by a common orthogonal conjugation, which preserves ranks and
all Schatten norms.

## A treewidth-one witness with rank-one optimum

Let \(L\) be the unweighted Laplacian of the connected \(n\)-vertex path, and
consider

\[
 \min\ \langle L,X\rangle
 \quad\text{subject to}\quad
 \operatorname{tr}X=1,
 \quad X\succeq0.
\tag{5}
\]

Its dual slack is \(S=L-yI\).  With

\[
 u=\frac1{\sqrt n}\mathbf1,
\]

the unique optimum is

\[
 X^*=uu^\top,
 \qquad y^*=0,
 \qquad S^*=L,
\]

so the primal optimum has rank one and strict complementarity holds.

For \(t>0\), let

\[
 y(t)=-t,
 \qquad
 S(t)=L+tI,
 \qquad
 Z(t)=\operatorname{tr}(S(t)^{-1}),
\]

\[
 \mu(t)=Z(t)^{-1},
 \qquad
 X(t)=\mu(t)S(t)^{-1}.
\tag{6}
\]

Then \(\operatorname{tr}X(t)=1\) and \(X(t)S(t)=\mu(t)I\), so (6) is the
exact central path.  Put

\[
 T(t)=\operatorname{tr}(S(t)^{-2}).
\]

Differentiating gives

\[
 \dot S=I,
 \qquad
 \dot\mu=\mu^2T,
 \qquad
 \dot X=\dot\mu S^{-1}-\mu S^{-2}.
\tag{7}
\]

Let \(0=\lambda_0<\lambda_1\leq\cdots\) be the eigenvalues of \(L\).  In the
Laplacian eigenbasis, the eigenvalues of \(\dot X\) are

\[
 \frac{\mu}{(t+\lambda_i)^2}
 \left(\frac{T}{Z}(t+\lambda_i)-1\right).
\tag{8}
\]

The \(i=0\) entry is strictly negative.  For every \(i\geq1\), it is strictly
positive whenever

\[
 t\leq\frac{\lambda_1}{2\sqrt n}.
\tag{9}
\]

Indeed, \(T/Z>1/(t+\lambda_1)\) follows from

\[
 \lambda_1^2+\lambda_1t-(n-1)t^2>0,
\]

which is implied by (9).  Hence both \(\dot X\) and \(\dot S=I\) are full
rank throughout this tail.

The exact Newton direction targeting \(\sigma\mu\) is a scalar multiple of
this tangent:

\[
 (\Delta X,\Delta S,\Delta y)
 =-\frac{(1-\sigma)\mu}{\dot\mu}
   (\dot X,\dot S,\dot y).
\tag{10}
\]

It satisfies the trace-feasibility equation and exact linearized
complementarity.  Thus both primal and dual Newton directions have rank \(n\)
arbitrarily close to a rank-one strictly complementary optimum.

This is not only a raw-rank artifact in the relevant NT metric.  Let
\(d_i=t+\lambda_i\) and \(\beta=\dot\mu/\mu=T/Z\).  At (6),
\(W=\sqrt\mu S^{-1}\), so the eigenvalues of the scaled tangent are

\[
 u_i=\sqrt\mu\left(\beta-\frac1{d_i}\right),
 \qquad
 v_i=\frac{\sqrt\mu}{d_i},
 \qquad
 u_i+v_i=\sqrt\mu\beta.
\tag{11}
\]

Under the slightly stronger tail condition

\[
 t\leq\frac{\lambda_1}{4\sqrt n},
\tag{9'}
\]

one has \(\beta d_i\geq3\) for every \(i\geq1\).  Indeed,
\(T\geq t^{-2}\), \(Z\leq t^{-1}+(n-1)\lambda_1^{-1}\), and therefore

\[
 \beta\lambda_1
 \geq \frac{\lambda_1/t}{1+(n-1)t/\lambda_1}
 \geq \frac{4\sqrt n}{1+(n-1)/(4\sqrt n)}>3.
\]

Consequently,

\[
 \frac23\sqrt\mu\beta<u_i<\sqrt\mu\beta
 \qquad(i\geq1).
\tag{12}
\]

Thus \(n-1\) singular values of the NT-scaled primal tangent lie within a
constant factor.  Every rank-\(k\) approximation with \(k<n-1\) satisfies

\[
 \|U-U_k\|_F
 \geq\frac23\sqrt\mu\beta\sqrt{n-1-k}.
\tag{13}
\]

For the path, \(\operatorname{tr}L^+=(n^2-1)/6\) and (9') also makes the
exceptional zero-mode contribution only \(O(n^{-1/2})\) relative to
\(\sqrt\mu\beta\).  Consequently a fixed relative Frobenius approximation of
the scaled primal tangent itself, with relative error bounded by any fixed
constant below \(2/3\), requires rank \(\Omega(n)\).  More generally, for any
fixed target relative error below one, decreasing the constant in (9') makes
all \(n-1\) nonexceptional singular values an arbitrarily large fixed fraction
of \(\sqrt\mu\beta\), and again forces rank \(\Omega(n)\).  Transforming
back to the unscaled coordinates can be ill conditioned, so this corollary is
properly interpreted in the NT local metric used by the progress equation.

The path Laplacian has \(O(n)\) nonzeros and ordinary sparsity graph a path.
The global trace constraint can make an extended aggregate graph appear dense
under some chordal-conversion definitions.  An equivalent local formulation
avoids this artifact: introduce cumulative scalars \(z_i\) and replace
\(\operatorname{tr}X=1\) by

\[
 X_{11}-z_1=0,
\]

\[
 X_{ii}+z_{i-1}-z_i=0
 \quad(2\leq i\leq n-1),
\]

\[
 X_{nn}+z_{n-1}=1.
\]

Stationarity in \(z\) forces all dual multipliers equal and recovers
\(S=L-yI\), while each matrix constraint touches one diagonal entry.  Both
matrix data and the constraint chain are therefore local and linear size.

## Consequence and limitations

For SDP-QIPMs that replace full symmetric-vector tomography by low-rank factor
tomography, low rank of \(X^*\) alone gives no valid direction-rank budget.
Constant relative contraction of the NT-scaled complementarity residual forces
aggregate factor rank \(\Omega(n)\), even for a linearly sparse path instance
with a rank-one optimum.

This is a structural rank obstruction, not an unconditional runtime lower
bound:

- full-rank matrices such as \(I\) can have compact implicit descriptions;
- the witness becomes very late-path and ill conditioned, since for a path
  \(\lambda_1=\Theta(n^{-2})\) and (9) asks for
  \(t=O(n^{-5/2})\);
- raw full algebraic rank does not imply large approximate rank in every norm;
  the robust claim is specifically (3), where truncation must still contract
  the NT-scaled complementarity residual.

Low-rank SDP-IPM papers commonly relax exact KKT equations or use low-rank
solutions for preconditioning, so the qualitative observation that interior
iterates are full rank is not new.  Targeted searches found no prior sharp
Schatten residual-versus-primal/dual-rank law of the form (3), nor its use as a
QIPM tomography obstruction.

### Theorem-level literature boundary

- Bellavia, Gondzio, and Porcelli, *A relaxed interior point method for
  low-rank semidefinite programming problems*, arXiv:1909.06099, Section 2
  explicitly calls the usual primal--dual KKT triple restrictive for low-rank
  iterates.  Their remedy removes the explicit dual slack, imposes a nearly
  low-rank primal form, and solves relaxed least-squares optimality equations.
  It does not retain (1), prove a rank--residual lower bound, or analyze ranks
  of accurate standard Newton directions:
  https://arxiv.org/abs/1909.06099
- Chiu and Zhang, *Well-conditioned Primal-Dual Interior-point Method for
  Accurate Low-rank Semidefinite Programming*, arXiv:2407.14013, equations
  (2a)--(2c) and Theorems 3.3 and 3.5 use the low-rank endpoint to reformulate
  and precondition the full NT Newton subproblem.  They compute a numerically
  exact, generally dense direction; low rank belongs to the spectral
  correction/preconditioner, not to \(\Delta X\) or \(\Delta S\).  This is
  compatible with (3) and is an important implicit-representation escape:
  https://arxiv.org/abs/2407.14013
- Ding, Yurtsever, Cevher, Tropp, and Udell, *An Optimal-Storage Approach to
  Semidefinite Programming Using Approximate Complementarity*,
  arXiv:1902.03373, compress a final primal-recovery problem to the small
  eigenvalue space of an approximate dual slack.  They do not compress the
  Newton direction at every iteration, and their result prevents reading (3)
  as a general low-storage impossibility:
  https://arxiv.org/abs/1902.03373
- Kelbel, Dolgov, Kalise, and Russo, *An Inexact Tensor-Train Primal-Dual
  Interior-Point Method for Semidefinite Programs*, arXiv:2509.11890, prove
  convergence with inexact tensor-train computations and report moderate
  tensor-train ranks empirically.  Tensor-train rank is not ordinary matrix
  rank, and the paper gives no worst-case truncation theorem contradicting
  (3):
  https://arxiv.org/abs/2509.11890
- Halicka, *Analyticity of the central path at the boundary point in
  semidefinite programming* (2001), proves that strict complementarity makes
  the central path and all of its derivatives have finite endpoint limits.
  This supplies classical context for (7)--(10), but gives no direction-rank
  or Schatten approximation result:
  https://optimization-online.org/2001/04/318/
- Augustino, Nannicini, Terlaky, and Zuluaga, *Quantum Interior Point Methods
  for Semidefinite Optimization*, arXiv:2112.06025, use tomography of inexact
  SDP Newton directions but do not use low-rank direction tomography and do
  not prove a rank obstruction:
  https://arxiv.org/abs/2112.06025

No primary source found in searches through 2026-09-02 states the sharp
Schatten residual-versus-aggregate-direction-rank law (3), the full-rank path
Laplacian Newton witness (5)--(13), or their QIPM-tomography consequence.

Status: **proof complete; apparently new quantitative structural theorem, with
the stated non-runtime scope.**

## Chordal escape: the rank barrier is formulation dependent

The same path family rules out a formulation-independent dense-memory lower
bound.  It has an exact product-cone formulation in which every PSD block is
only \(2\times2\).

For edge \(i=1,\ldots,n-1\), introduce

\[
 Y_i=
 \begin{pmatrix}
  x_{ii}&x_{i,i+1}\\
  x_{i,i+1}&x_{i+1,i+1}
 \end{pmatrix}\succeq0.
\]

Impose the overlap equations

\[
 (Y_i)_{22}=(Y_{i+1})_{11}
 \quad(1\leq i\leq n-2)
\tag{14}
\]

and count every diagonal entry once in

\[
 (Y_1)_{11}+\sum_{i=1}^{n-1}(Y_i)_{22}=1.
\tag{15}
\]

Then (5) is equivalent, with the same optimal value, to

\[
 \min\ \sum_{i=1}^{n-1}
 \left\langle
 \begin{pmatrix}1&-1\\-1&1\end{pmatrix},Y_i
 \right\rangle
 \quad\text{subject to (14), (15), and }Y_i\succeq0.
\tag{16}
\]

### Exactness

Restriction of a feasible \(X\succeq0\) to its edge principal submatrices
gives feasible \(Y_i\).  Conversely, consistent PSD edge matrices admit a PSD
completion because a path is chordal.  This can also be seen directly.  Given
a Gram vector for vertex \(i\), the \(2\times2\) PSD condition permits choosing
a Gram vector for vertex \(i+1\) with the prescribed norm and inner product;
one new orthogonal coordinate suffices at each step.  The objective and trace
depend only on these specified entries, proving equivalence.

Every term in (16) is nonnegative.  A zero objective forces

\[
 Y_i= a_i\mathbf1_2\mathbf1_2^\top.
\]

The overlap equations force all \(a_i\) equal, and (15) gives \(a_i=1/n\).
Thus the converted optimum has rank one in each size-two block and completes
to the original unique optimum \(uu^\top\).

### Linear memory and a linear-time classical Newton solve

The logarithmic barrier for (16) is

\[
 -\sum_{i=1}^{n-1}\log\det Y_i
\]

and has parameter \(2(n-1)\).  It stores \(3(n-1)\) primal matrix entries, and
every primal or dual matrix direction is a list of \(2\times2\) blocks.  Hence
even a full-rank direction in every block takes only \(O(n)\) memory.

The barrier Hessian is block diagonal with constant-size blocks.  After these
blocks are eliminated, two overlap constraints interact only when their path
indices differ by at most one.  The trace constraint interacts with all of
them.  The normal matrix is therefore a tridiagonal matrix with one dense
border.  Factoring the tridiagonal part, solving once against the border, and
forming its scalar Schur complement costs \(O(n)\) arithmetic and \(O(n)\)
memory.  Initialization is explicit: the analytic center at zero objective has
zero off-diagonals and vertex diagonals
\(d_1=d_n=1/[2(n-1)]\) and
\(d_i=1/(n-1)\) for \(2\leq i\leq n-1\).  A standard short-step
product-cone IPM consequently gives the
conservative end-to-end bound

\[
 O\!\left(n^{3/2}\log\frac{n}{\epsilon}\right)
 \quad\text{arithmetic},
 \qquad O(n)\quad\text{memory},
\tag{17}
\]

apart from bit-precision costs.  This agrees with the broader lesson of the
chordal-conversion literature: the constraint-support or extended graph, not
the aggregate matrix sparsity graph alone, controls a generic sparse-IPM
factorization; see Zhang, *Complexity of Chordal Conversion for Sparse
Semidefinite Programs with Small Treewidth*, arXiv:2306.15288,
https://arxiv.org/abs/2306.15288.  The
explicit bordered-path calculation above is needed because the single global
trace equation makes some generic extended-graph bounds pessimistic.

Equations (3) and (13) therefore cannot imply an unconditional
\(\Omega(n^2)\) memory or output lower bound for sparse SDP algorithms.  They
apply to the one-block formulation and to algorithms that rank-truncate its NT
directions.  An algorithm may instead change the cone representation, retain
small clique blocks, or store resolvents implicitly.  For this witness, both
the chordal formulation and the identity

\[
 \dot X=\dot\mu(L+tI)^{-1}-\mu(L+tI)^{-2}
\]

give explicit escapes.  A genuine end-to-end lower bound would have to fix an
output representation or prove hardness against all such implicit and
extended formulations; rank alone cannot do this.

## Audited path asymptotics

For the \(n\)-vertex path,

\[
 \lambda_k=4\sin^2\frac{\pi k}{2n},
 \qquad
 \lambda_1=\frac{\pi^2}{n^2}+O(n^{-4}),
\]

\[
 H:=\operatorname{tr}L^+=\frac{n^2-1}{6},
 \qquad
 Q:=\operatorname{tr}(L^+)^2
   =\frac{2n^4+5n^2-7}{180}.
\tag{18}
\]

At the endpoint \(t=\lambda_1/(2\sqrt n)\),

\[
 t=\frac{\pi^2}{2n^{5/2}}(1+o(1)),
 \qquad
 \kappa(L+tI)=\frac{8}{\pi^2}n^{5/2}(1+o(1)).
\tag{19}
\]

For smaller \(t\), (9) gives only the lower bound
\(\kappa(L+tI)=\Omega(n^{5/2})\), not a uniform
\(\Theta(n^{5/2})\) statement.  Moreover,

\[
 \mu=t\left(1-tH+O(n^{-1})\right),
 \qquad
 \beta=\frac1t-H+O\!\left(t(H^2+Q)\right).
\tag{20}
\]

As \(t\downarrow0\), the raw tangent spectrum converges to

\[
 \left\{-H,\frac1{\lambda_1},\ldots,
              \frac1{\lambda_{n-1}}\right\}.
\tag{21}
\]

Its stable rank tends to

\[
 \frac{H^2+Q}{H^2}\longrightarrow\frac75,
\]

and its best rank-one relative Frobenius error tends to

\[
 \sqrt{\frac{Q}{H^2+Q}}\longrightarrow\sqrt{\frac27}.
\tag{22}
\]

Thus raw full rank is not dimensional approximate-rank hardness.  In contrast,
at \(t=\lambda_1/(2\sqrt n)\), (20) gives uniformly for \(i\geq1\)

\[
 \frac{u_i}{\sqrt\mu\beta}=1-O(n^{-1/2}),
 \qquad
 \frac{|u_0|}{\sqrt\mu\beta}=O(n^{-1/2}).
\tag{23}
\]

The NT-scaled primal tangent therefore has \(n-1\) asymptotically flat
singular values even though the raw tangent has stable rank bounded by a
constant.  This sharp contrast is why every norm and coordinate system must be
stated explicitly.

There is a further quantum-output caveat.  Let
\(a=\sqrt\mu\beta\).  The same estimates imply

\[
 \left\|\frac{U}{a}-(I-uu^\top)\right\|_2=O(n^{-1/2})
 \quad\text{and}\quad
 \left\|\frac{U}{a}-(I-uu^\top)\right\|_F=O(1).
\tag{24}
\]

Write \(|A\rangle=\operatorname{vec}(A)\).  Since
\(\|I-uu^\top\|_F=\sqrt{n-1}\), the normalized vectorization of \(U\)
is \(O(n^{-1/2})\)-close in Euclidean norm to

\[
 \frac{|I\rangle-|uu^\top\rangle}{\sqrt{n-1}}.
\tag{25}
\]

For the path, \(u=\mathbf1/\sqrt n\).  The state
\(|I\rangle/\sqrt n\) is a maximally entangled index state and
\(|uu^\top\rangle=|u\rangle|u\rangle\) is the product of two uniform states.
Combining them with coefficients \(\sqrt n\) and \(-1\) prepares (25) by
LCU with constant success probability and a polylogarithmic-size circuit.
For \(n=2^m\), the two component states use \(O(m)\) Hadamard and CNOT gates;
 the coefficient rotation and a constant number of amplitude-amplification
 steps add
\(O(1)\) state-oracle calls.  For general \(n\), standard approximate uniform
state preparation gives the same \(\widetilde O(\log n)\) gate bound.
Thus this witness has maximal approximate matrix rank in the NT metric but an
easy approximate quantum state.  The rank-progress theorem obstructs
low-rank factor tomography; it does not by itself lower-bound amplitude-state
preparation.
