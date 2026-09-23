# A non-SOCP Schur-block SDP parity family with scalar central Hessian

Date: 2026-09-02

## Main result

The \(3\times3\) block

\[
 X_\tau(t)=
 \begin{pmatrix}
  t+1&0&\tau\\
  0&t&0\\
  \tau&0&1
 \end{pmatrix}
\tag{1}
\]

has an exact higher-rank extension.  The \(3\times3\) version leaves a free
\(\mathbb S_+^2\) Schur complement and is therefore SOCP-representable.
The first genuinely non-SOCP case uses \(4\times4\) PSD blocks and leaves a
free \(\mathbb S_+^3\) Schur complement.

For every fixed \(k\ge2\), there is a linear-size parity family over
\((\mathbb S_+^{k+1})^P\) with the following properties.

1. Its entire primal central path is explicit.
2. In a public Frobenius-orthonormal feasible-tangent basis, the full reduced
   log-det Hessian is a scalar multiple of the identity for every central
   parameter.
3. The two input-dependent central block values do not commute.
4. At \(\mu_0=1/P\), preparing the trace-normalized primal central matrix to
   constant trace distance requires \(\Omega(P)\) raw sparse-coefficient
   queries, and the same bound holds for calls to the canonical
   normalization-two equality-operator block encoding in Section 4.3.
5. On the full late tail \(0<\mu\le\mu_0\), all central coordinates and
   multipliers are bounded, and preparing the amplitude encoding of the
   complete primal--multiplier--slack central triple also requires
   \(\Omega(P)\) raw queries or canonical block-encoding calls.
6. For \(k=2\), every feasible block slice is affinely isomorphic to
   \(\mathbb S_+^2\), hence to a Lorentz cone.  For every \(k\ge3\), it is
   affinely isomorphic to \(\mathbb S_+^k\) and has no finite SOCP lift.

For \(k=3\), the density-state lower bound is robust to arbitrary PSD primal
blocks: it is enough that their equality residual is at most
\(1/(4\sqrt P)\) in Euclidean norm and their objective is no larger than the
\(t=1\) center value.  This \(\Theta(P^{-1/2})\) residual scale is sharp up to
an absolute constant for this decoder: a convex average of single-bit-flipped
exact centers has the same objective and the wrong output parity while its
residual is only \(2\sqrt{2/N}=\Theta(P^{-1/2})\).
The proof, the inverted
\(\Omega(\min\{P,\varepsilon^{-2}\})\) accuracy curve, and exact-size public
padding are given in
[2026-09-02-nonsoc-sdp-accuracy-query-frontier.md](2026-09-02-nonsoc-sdp-accuracy-query-frontier.md).

The strongest clean corollary takes \(k=3\): a product of \(4\times4\) PSD
blocks, with \(\Theta(P)\) scalar variables and equalities, has genuinely
non-SOCP feasible geometry, a unique strictly complementary primal--dual
optimum, an exactly condition-one reduced Hessian along the full central
path, noncommuting local central matrices, and linear lower bounds in both
the raw-query and canonical equality-operator-block-encoding models for
density-state output and full central-triple amplitude output.

This is still an output-interface obstruction, not evidence that optimizing
over the free PSD coordinates is hard.  A public Schur-complement
reparameterization removes all input dependence from the free optimization;
the hidden parity remains in reconstructing the requested matrix state.

## 1. Construction

Let hidden signs be
\(\sigma_1,\ldots,\sigma_N\in\{\pm1\}\).  Put

\[
 K=16N,\qquad P=N+K+1=17N+1,
\]
\[
 a_i=
 \begin{cases}
  \sigma_i,&1\le i\le N,\\
  1,&N<i<P,
 \end{cases}
 \qquad
 \tau_0=1,\qquad \tau_i=\prod_{j=1}^i a_j.
\tag{2}
\]

There are \(P\) primal blocks
\(X_0,\ldots,X_{P-1}\in\mathbb S_+^{k+1}\).  Let
\(e_1,\ldots,e_{k+1}\) be the standard basis and define the
Frobenius-orthonormal last-column matrices

\[
 F_j=\frac1{\sqrt2}(e_je_{k+1}^T+e_{k+1}e_j^T)
 \quad(1\le j\le k),
 \qquad E=e_{k+1}e_{k+1}^T.
\tag{3}
\]

Thus \(\langle F_j,X\rangle=\sqrt2X_{j,k+1}\), exactly the corresponding
off-diagonal coordinate in standard isometric svec.  Put

\[
 d_{j,i}=\langle F_j,X_i\rangle,\qquad
 z_i=\langle E,X_i\rangle.
\]

Use \(k+1\) rooted chains:

\[
 \begin{aligned}
 d_{1,0}&=\sqrt2,&
 d_{1,i}-a_id_{1,i-1}&=0 &&(1\le i<P),\\
 d_{j,0}&=0,&
 d_{j,i}-d_{j,i-1}&=0
        &&(2\le j\le k,\ 1\le i<P),\\
 z_0&=1,&z_i-z_{i-1}&=0 &&(1\le i<P).
 \end{aligned}
\tag{4}
\]

Set \(\mu_0=1/P\) and use the public block cost

\[
 C_0=\mu_0\operatorname{Diag}(I_k,2),
 \qquad
 \min\sum_{i=0}^{P-1}\langle C_0,X_i\rangle.
\tag{5}
\]

The first two row families fix
\((X_i)_{1,k+1}=\tau_i\).  The remaining rows fix the last column, so every
feasible block has the unique form

\[
 X_i=
 \begin{pmatrix}
  A_i&v_i\\
  v_i^T&1
 \end{pmatrix},
 \qquad
 v_i=\tau_i e_1,\qquad A_i\in\mathbb S^k.
\tag{6}
\]

Its Schur complement is

\[
 Z_i=A_i-v_iv_i^T=A_i-e_1e_1^T.
\tag{7}
\]

Therefore

\[
 X_i\succeq0\quad\Longleftrightarrow\quad Z_i\succeq0,
 \qquad
 \det X_i=\det Z_i,
\tag{8}
\]

and

\[
 \langle C_0,X_i\rangle
 =\mu_0(\operatorname{tr}Z_i+3).
\tag{9}
\]

Notice that both (7) and (9) are independent of \(\tau_i\).

All equality rows are independent.  Each rooted chain has rank \(P\), and
different chains act on disjoint svec coordinates.  Hence there are exactly
\(P(k+1)\) independent equality rows, and the feasible tangent dimension is

\[
 P\left[\frac{(k+1)(k+2)}2-(k+1)\right]
 =P\frac{k(k+1)}2.
\tag{10}
\]

For fixed \(k\), this is a linear-size sparse product SDP.  A row touches at
most two blocks, and a block participates in at most \(2(k+1)\) rows.  In
standard isometric svec coordinates, each equality row has at most two
nonzeros and each scalar coordinate occurs in at most two rows.  The support
pattern is public, every nonzero equality coefficient has magnitude one,
and the only input-dependent coefficient in transition \(i\) is
\(-a_iF_1\).  The full right-hand side has only the two nonzero entries
\(\sqrt2\) and \(1\), so

\[
                         \|b\|_2=\sqrt3.
\tag{10a}
\]

## 2. Optimum, strict feasibility, and exact central path

Equations (8)--(9) reduce the primal problem, up to an additive constant, to

\[
                     \min\ \mu_0\sum_i\operatorname{tr}Z_i,
 \qquad Z_i\succeq0.
\tag{11}
\]

It has the unique optimum \(Z_i=0\).  The corresponding original optimum is
the rank-one block

\[
 X_i^{\mathrm{opt}}
 =
 \begin{pmatrix}v_i\\1\end{pmatrix}
 \begin{pmatrix}v_i\\1\end{pmatrix}^{\!T}.
\tag{12}
\]

Strict primal feasibility holds, for example at every \(Z_i=I_k\).

At central parameter \(\mu>0\), the variable part of the barrier objective is

\[
 \sum_i\left[
   \mu_0\operatorname{tr}Z_i-\mu\log\det Z_i
 \right].
\tag{13}
\]

It is strictly convex and has the unique minimizer

\[
 Z_i=tI_k,\qquad t=\frac{\mu}{\mu_0}.
\tag{14}
\]

Thus the entire primal central path is

\[
 \boxed{
 X_{\tau_i}^{(k)}(t)=
 \begin{pmatrix}
  tI_k+e_1e_1^T&\tau_i e_1\\
  \tau_i e_1^T&1
 \end{pmatrix},
 \qquad t=\frac{\mu}{\mu_0}.}
\tag{15}
\]

For \(k=2\), this is exactly (1).

The inverse is

\[
 (X_\tau^{(k)}(t))^{-1}
 =
 \begin{pmatrix}
  t^{-1}I_k&-t^{-1}\tau e_1\\
  -t^{-1}\tau e_1^T&1+t^{-1}
 \end{pmatrix}.
\tag{16}
\]

Hence the central dual slack is

\[
 S_i(\mu)=\mu(X_{\tau_i}^{(k)}(t))^{-1}
 =
 \begin{pmatrix}
  \mu_0I_k&-\mu_0\tau_i e_1\\
  -\mu_0\tau_i e_1^T&\mu+\mu_0
 \end{pmatrix}\succ0.
\tag{17}
\]

For completeness, use the convention
\(S=C-\mathcal A^*y\).  Let \(\alpha_i\) be the multipliers on the signed
\(d_1\)-chain, and let \(\beta_i\) be those on the bottom \(z\)-chain.
Backward substitution gives

\[
 \boxed{
 \alpha_i=\sqrt2\mu_0(P-i)\tau_i,\qquad
 \beta_i=(\mu_0-\mu)(P-i).}
\tag{18}
\]

Indeed, their chain divergences are respectively
\(\sqrt2\mu_0\tau_i\) and \(\mu_0-\mu\), exactly the isometric-svec
coordinates of \(C_0-S_i(\mu)\).  Set every \(d_j\)-chain multiplier for
\(j\ge2\) to zero.  Equations (16)--(18) give (17) exactly.  Thus strict
dual feasibility holds for every \(\mu>0\), and at the selected
\(\mu=\mu_0\),

\[
 |\alpha_i|\le\sqrt2,\qquad \beta_i=0,
\tag{19}
\]

while every slack entry is \(O(1/P)\).  The center blocks have bounded
entries and eigenvalues bounded above and below by absolute constants.

In fact, all central coordinates and multipliers are uniformly bounded on
the entire late tail

\[
                         0<\mu\le\mu_0,\qquad 0<t\le1.
\tag{19a}
\]

Equations (15), (17), and (18) give

\[
 \max_i\|X_i\|_{\max}\le2,\qquad
 \max_i\|S_i\|_{\max}\le\frac2P,\qquad
 \|\alpha\|_\infty\le\sqrt2,\qquad
 \|\beta\|_\infty\le1.
\tag{19b}
\]

The exact per-block Frobenius norms are

\[
 \|X_i\|_F^2=kt^2+2t+4\le k+6,
 \qquad
 \|S_i\|_F^2
 =\mu_0^2[k+2+(1+t)^2]\le\frac{k+6}{P^2}.
\tag{19c}
\]

The nonzero multiplier norm is

\[
 \|y\|_2^2
 =[2+(1-t)^2]P^{-2}\sum_{\ell=1}^P\ell^2
 \le3P.
\tag{19d}
\]

Thus boundedness is not confined to the single point \(\mu=\mu_0\).

The objective gap and limiting optimum are also exact.  Since
\(P\mu_0=1\), \(t=\mu/\mu_0\), and only the two root rows have nonzero
right-hand side,

\[
 \sum_i\langle C_0,X_i(t)\rangle=kt+3,
 \qquad
 b^Ty=\sqrt2\,\alpha_0+\beta_0=3-t.
\tag{19e}
\]

Therefore

\[
 \sum_i\langle C_0,X_i(t)\rangle-b^Ty
 =(k+1)t=P(k+1)\mu,
\tag{19f}
\]

as required by \(X_iS_i=\mu I_{k+1}\).  At \(t=0\), the unique primal
optimum (12) is paired with the limiting dual slack

\[
 S_i^{\rm opt}=\mu_0
 \begin{pmatrix}
  I_k&-\tau_i e_1\\
  -\tau_i e_1^T&1
 \end{pmatrix}.
\tag{19g}
\]

This slack has rank \(k\), annihilates the rank-one matrix (12), and hence

\[
 \operatorname{rank}X_i^{\rm opt}
 +\operatorname{rank}S_i^{\rm opt}=1+k=k+1.
\tag{19h}
\]

Thus the optimum is strictly complementary.  It is unique on both sides.
Primal uniqueness follows from (11).  For any dual optimum, zero gap with
the unique \(X^{\rm opt}\) implies \(S_iX_i^{\rm opt}=0\).  The unconstrained
top-block stationarity coordinates fix
\((S_i)_{1:k,1:k}=\mu_0I_k\); applying \(S_i\) to
\((v_i,1)^T\) then uniquely fixes its last column, giving (19g).  Finally,
full row rank of the equality map makes \(\mathcal A^*\) injective, so (18)
at \(t=0\) is the unique multiplier vector.

## 3. Scalar reduced Hessian on the full path

Every feasible tangent has the form

\[
 \Delta X_i=
 \begin{pmatrix}
  H_i&0\\
  0&0
 \end{pmatrix},
 \qquad H_i\in\mathbb S^k.
\tag{20}
\]

This tangent space is public and input-independent.  The primal log-det
Hessian at parameter \(\mu\) is

\[
 \mathcal H_\mu[\Delta X,\Delta Y]
 =\mu\sum_i\operatorname{tr}
 (X_i^{-1}\Delta X_iX_i^{-1}\Delta Y_i).
\tag{21}
\]

Using (16), or differentiating (13), gives

\[
 \boxed{
 \mathcal H_\mu[\Delta X,\Delta Y]
 =\frac{\mu}{t^2}\sum_i\operatorname{tr}(H_iK_i)
 =\frac{\mu_0^2}{\mu}
   \sum_i\langle H_i,K_i\rangle_F.}
\tag{22}
\]

Consequently, in every Frobenius-orthonormal basis of the complete feasible
tangent space,

\[
 \boxed{
 H_{\mathrm{red}}(\mu)=\frac{\mu_0^2}{\mu}I,
 \qquad
 \kappa_2(H_{\mathrm{red}}(\mu))=1
 \quad\text{for every }\mu>0.}
\tag{23}
\]

This is exact scalarity, not preconditioned scalarity and not a restriction
to a selected active subspace.

The two possible local center matrices are genuinely noncommuting:

\[
 [X_+^{(k)}(t),X_-^{(k)}(t)]
 =2t(e_{k+1}e_1^T-e_1e_{k+1}^T)\ne0.
\tag{24}
\]

Thus they have no common orthogonal diagonalizing basis.  This means the
two input-dependent local matrix values are noncommuting; it does not mean
that every single parity instance necessarily contains both signs.

## 4. Density-state parity lower bound

At a general path parameter,
\(\operatorname{tr}X_{\tau_i}^{(k)}(t)=kt+2\).  Define the block-diagonal
density matrix

\[
 \rho_\sigma(t)=
 \frac{\bigoplus_{i=0}^{P-1}X_{\tau_i}^{(k)}(t)}
      {P(kt+2)}.
\tag{25}
\]

Let the public tail be
\(T=\{N+1,\ldots,N+K\}\), on which
\(\tau_i=\tau_N=\prod_{j=1}^N\sigma_j\).  Define the fixed Hermitian
contraction

\[
 O=\bigoplus_{i=0}^{P-1}O_i,\qquad
 O_i=
 \begin{cases}
  e_1e_{k+1}^T+e_{k+1}e_1^T,&i\in T,\\
  0,&i\notin T.
 \end{cases}
\tag{26}
\]

Then

\[
 \boxed{
 \tau_N\operatorname{tr}(O\rho_\sigma(t))
 =\frac{2K}{P(kt+2)}.}
\tag{27}
\]

At the selected \(\mu=\mu_0\), one has \(t=1\); for every fixed \(k\), the
bias is then a positive constant.  In the minimal non-SOCP case \(k=3\),

\[
 \tau_N\operatorname{tr}(O\rho_\sigma(1))
 =\frac{32N}{5(17N+1)}>\frac13.
\tag{28}
\]

For \(0<t\le1\), the denominator in (27) is no larger than its value at
\(t=1\).  Thus the same density-state bias, and hence the same query lower
bound, holds uniformly throughout the public late-tail range
\(0<\mu\le\mu_0\), although the headline only needs \(\mu=\mu_0\).

The binary POVM \((I\pm O)/2\) therefore recovers parity with advantage
greater than \(1/6\).  Trace distance \(1/100\) changes either outcome
probability by at most \(1/100\), leaving constant advantage.

Here
\(D_{\mathrm{tr}}(\rho,\omega)=\tfrac12\|\rho-\omega\|_1\).  The
probability of any fixed POVM outcome changes by at most this quantity, which
is the convention used in the preceding robustness statement.

Use coherent fixed-position sparse access to the equality coefficients,
right-hand sides, and cost.  A query to the only input-dependent value
\(-a_iF_1\) is simulated with one query to \(\sigma_i\); all support
positions and all other values are public.  Composing any preparation
algorithm, at any fixed public \(0<t\le1\), for a state
\(\widetilde\rho\) satisfying

\[
 D_{\mathrm{tr}}(\widetilde\rho,\rho_\sigma(t))\le\frac1{100}
\tag{29}
\]

with the fixed POVM contradicts the quantum parity lower bound unless the
algorithm makes \(q\ge N/2=\Omega(P)\) raw coefficient queries.  Since
\(k\) is fixed, this is linear in the Hilbert-space dimension, the scalar
conic dimension, and the number of equality rows.

The statement concerns unconditional output.  Postselection is covered only
when its success probability and amplification cost are charged.

### 4.1 Full central-triple amplitude state on the late tail

The lower bound is not limited to trace normalization of the primal matrix.
Fix the isometric-svec ordering used in (3)--(4), include every equality
multiplier in the row order of (4), and define the complete central vector

\[
 g_\sigma(t)=
 \bigl(\operatorname{svec}X(t),\,y(t),\,
       \operatorname{svec}S(t)\bigr).
\tag{29a}
\]

Equations (19c)--(19d) give the exact normalization

\[
 \|g_\sigma(t)\|_2^2
 =P(kt^2+2t+4)
 +[2+(1-t)^2]\frac{(P+1)(2P+1)}{6P}
 +\frac{k+2+(1+t)^2}{P}.
\tag{29b}
\]

In particular, for \(k=3\) and \(N\ge1\), hence \(P\ge18\),

\[
                         \|g_\sigma(t)\|_2^2<11P,
 \qquad 0<t\le1.
\tag{29c}
\]

Indeed, the three terms in (29b) are at most
\(9P\), \(P+3/2+1/(2P)\), and \(9/P\), respectively.  The vector is always
nonzero; already its primal sector has squared norm at least \(4P\).  The
identically zero multiplier-chain sectors remain part of the fixed public
coordinate space but affect neither normalization nor the observable below.

Let \(\lvert b_i\rangle\) denote the primal-\(X_i\) amplitude coordinate for
\((X_i)_{k+1,k+1}=1\), and let \(\lvert d_i\rangle\) denote its isometric
svec coordinate

\[
 \sqrt2(X_i)_{1,k+1}=\sqrt2\tau_i.
\]

Define the fixed Hermitian contraction on the complete triple-coordinate
space

\[
 W=\sum_{i\in T}
   (\lvert b_i\rangle\langle d_i\rvert+
    \lvert d_i\rangle\langle b_i\rvert),
\tag{29d}
\]

acting as zero on all other primal, multiplier, and slack coordinates.
The two coordinates form disjoint swap pairs, so \(\|W\|_{\rm op}=1\).
For the normalized amplitude state

\[
 \lvert\Psi_\sigma(t)\rangle
 =\frac{\lvert g_\sigma(t)\rangle}{\|g_\sigma(t)\|_2},
\]

each tail block contributes \(2\sqrt2\tau_N\) to the numerator.  Hence

\[
 \boxed{
 \tau_N\langle\Psi_\sigma(t)|W|\Psi_\sigma(t)\rangle
 =\frac{2\sqrt2K}{\|g_\sigma(t)\|_2^2}.}
\tag{29e}
\]

For \(k=3\), (29c), \(K=16N\), and \(P=17N+1\) give the uniform bound

\[
 \tau_N\langle\Psi_\sigma(t)|W|\Psi_\sigma(t)\rangle
 >\frac{32\sqrt2N}{11(17N+1)}
 >\frac15,
 \qquad 0<t\le1.
\tag{29f}
\]

Thus the binary POVM \((I\pm W)/2\) reads parity with constant advantage
greater than \(1/10\) from the full central-triple amplitude state at every
point of the late tail.  Preparing any state to trace distance \(1/100\) from
\(\lvert\Psi_\sigma(t)\rangle\langle\Psi_\sigma(t)\rvert\) still leaves
advantage greater than \(9/100\).  The same raw-oracle reduction therefore
proves \(\Omega(N)=\Omega(P)\) coefficient queries uniformly for every public
\(0<\mu\le\mu_0\).

### 4.2 Robust approximate-primal density theorem

The exact-center requirement can also be weakened.  Specialize to \(k=3\),
and let \(\mathcal A_\sigma\) denote the equality operator in (4).  Consider
arbitrary blocks

\[
 X_i=\begin{pmatrix}A_i&b_i\\b_i^T&z_i\end{pmatrix}\succeq0,
 \qquad A_i\in\mathbb S^3,\quad b_i\in\mathbb R^3,
\tag{29g}
\]

not necessarily on the central path.  Define

\[
 u_i=\sqrt2(X_i)_{1,4}=\langle F_1,X_i\rangle,
 \qquad
 \rho(X)={\bigoplus_iX_i\over\sum_i\operatorname{tr}X_i}.
\tag{29h}
\]

Suppose

\[
 \|\mathcal A_\sigma X-b\|_2\le\varepsilon
       \le {1\over4\sqrt P},
 \qquad
 \sum_i\langle C_0,X_i\rangle
 ={1\over P}\sum_i(\operatorname{tr}A_i+2z_i)\le6.
\tag{29i}
\]

The normalization in (29h) is well-defined.  Indeed, the root residual
implies \(u_0\ne0\), while a PSD matrix with a nonzero off-diagonal entry has
positive trace.

Let \(g_0=u_0-\sqrt2\) and
\(g_i=u_i-a_iu_{i-1}\) for \(1\le i<P\).  These are coordinates of the full
residual in (29i), so \(\|g\|_2\le\varepsilon\).  Inverting the signed
bidiagonal chain gives

\[
 u_i-\sqrt2\tau_i
 =\sum_{j=0}^i\left(\prod_{\ell=j+1}^ia_\ell\right)g_j,
 \qquad
 |u_i-\sqrt2\tau_i|
 \le\sqrt{i+1}\,\|g\|_2\le {1\over4}.
\tag{29j}
\]

On every output-copy block \(i\in T\), one has \(\tau_i=\tau_N\).  Therefore
the observable (26) satisfies the exact per-block lower bound

\[
 \tau_N\operatorname{tr}(O_iX_i)
 =\sqrt2\tau_Nu_i
 \ge 2-\frac{\sqrt2}{4}
 =2-\frac1{2\sqrt2}>\frac{13}{8}.
\tag{29k}
\]

PSD implies \(A_i\succeq0\) and \(z_i\ge0\).  The objective promise thus
controls the trace even though it does not control the individual blocks:

\[
 \sum_i\operatorname{tr}X_i
 =\sum_i(\operatorname{tr}A_i+z_i)
 \le\sum_i(\operatorname{tr}A_i+2z_i)\le6P.
\tag{29l}
\]

Combining (29k)--(29l), using \(K=16N\), \(P=17N+1\), and
\(K/P\ge8/9\), gives the uniform signed bias

\[
 \boxed{
 \tau_N\operatorname{tr}(O\rho(X))
 \ge {K\over6P}\left(2-{1\over2\sqrt2}\right)
 >{13\over54}>{6\over25}.}
\tag{29m}
\]

The POVM \((I\pm O)/2\) consequently recovers parity from \(\rho(X)\) with
advantage greater than \(3/25\).  If a prepared state \(\widetilde\rho\)
satisfies \(D_{\rm tr}(\widetilde\rho,\rho(X))\le1/100\), its advantage is
still greater than \(3/25-1/100>0\).

This proves the following robust query statement.  In the raw sparse oracle
model of Section 4, any algorithm which, for every hidden input \(\sigma\),
prepares a state within trace distance \(1/100\) of the trace normalization of
some PSD block vector \(X\) satisfying (29i) must make
\(\Omega(N)=\Omega(P)\) coefficient queries.  The approximate point may be
chosen adversarially and need not be a central point, a Newton iterate, or
close to the exact center in matrix norm.  Only PSD, the residual bound, and
the objective upper bound are used.

The norms and normalization in this statement are specific.  The residual is
the ordinary Euclidean norm of the equality vector in the exact row scaling
of (4), and the output is the trace normalization of the PSD block-diagonal
matrix.  PSD is used both to make this a density matrix and to infer
\(A_i\succeq0,z_i\ge0\).  The objective upper bound prevents adding
arbitrarily large public diagonal mass that would dilute the parity
observable.  Dropping either assumption, changing the equality-row scaling,
or asking for a different normalization requires a separate theorem.

#### Sharpness of the residual scale

The \(P^{-1/2}\) dependence cannot be replaced by a constant using this
residual-to-parity argument.  Fix a base input \(\sigma\).  For each
\(j\in\{1,\ldots,N\}\), flip only \(\sigma_j\), and let \(X^{(j)}\) be that
neighboring instance's exact \(t=1\) center (15).  The convex average

\[
                         \overline X={1\over N}\sum_{j=1}^NX^{(j)}
\tag{29n}
\]

is blockwise positive definite and has the same objective value six.  Its
first off-diagonal chain, measured in the normalized coordinates \(u_i\), is

\[
 \overline u_i=
 \begin{cases}
  \sqrt2\tau_i(1-2i/N),&0\le i\le N,\\
  -\sqrt2\tau_i,&N<i<P.
 \end{cases}
\tag{29o}
\]

All equality residuals vanish except the \(N\) hidden signed transitions.
For \(1\le i\le N\),

\[
 \overline u_i-\sigma_i\overline u_{i-1}
 =-{2\sqrt2\over N}\tau_i.
\tag{29p}
\]

Consequently,

\[
 \|\mathcal A_\sigma\overline X-b\|_2
 =\sqrt{N\,{8\over N^2}}
 =2\sqrt{2/N}
 =\Theta(P^{-1/2}).                                    \tag{29q}
\]

Yet every output-copy block has off-diagonal sign \(-\tau_N\), so (26)
decodes the wrong parity from \(\rho(\overline X)\), with the same magnitude
as at an exact center.  More explicitly, every averaged block still has trace
five, and

\[
 \tau_N\operatorname{tr}(O\rho(\overline X))
 =-{2K\over5P}<-{1\over3}.                              \tag{29r}
\]

Thus (29i) and (29q) match in asymptotic residual scale, though not in
constants.  The robust theorem is a \(\Theta(P^{-1/2})\)-residual result, not
a constant-residual theorem.

### 4.3 Canonical equality-operator block encoding

The raw-query theorem also transfers to a fully specified block-encoding
interface.  Let \(A_\sigma\) be the matrix of the equality operator in (4)
in the standard isometric-svec coordinates fixed in (3).  Its dimensions are

\[
 m=P(k+1),\qquad
 n_{\rm svec}=P\frac{(k+1)(k+2)}2,
 \qquad A_\sigma\in\mathbb R^{m\times n_{\rm svec}}.
\tag{BE1}
\]

In particular, the genuinely non-SOCP case \(k=3\) has
\(A_\sigma\in\mathbb R^{4P\times10P}\).  The support and magnitudes are
public, every nonzero magnitude is one, and

\[
 \max_r\|(A_\sigma)_{r,*}\|_1
 =\max_c\|(A_\sigma)_{*,c}\|_1=2.
\tag{BE2}
\]

For every potential nonzero \((r,c)\), introduce a distinct public entry
label \(\lvert e_{rc}\rangle\), together with mutually orthogonal row-failure
labels \(\lvert L_r\rangle\) and column-failure labels
\(\lvert R_c\rangle\).  Define

\[
\begin{aligned}
 \lvert\chi_r\rangle
 &=\sum_{c:(r,c)\in\operatorname{supp}A}
   \sqrt{\frac{|A_{rc}|}{2}}\,\lvert e_{rc}\rangle
   +\sqrt{1-\frac{\|(A_\sigma)_{r,*}\|_1}{2}}\,
       \lvert L_r\rangle,\\
 \lvert\phi_c^\sigma\rangle
 &=\sum_{r:(r,c)\in\operatorname{supp}A}
   \operatorname{sgn}(A_{rc}^\sigma)
   \sqrt{\frac{|A_{rc}|}{2}}\,\lvert e_{rc}\rangle
   +\sqrt{1-\frac{\|(A_\sigma)_{*,c}\|_1}{2}}\,
       \lvert R_c\rangle.
\end{aligned}
\tag{BE3}
\]

The row states are orthonormal because distinct rows have disjoint entry and
failure labels.  The column states are orthonormal for the same reason.
Free top-block svec columns have degree zero and lie entirely on their
failure label.  Root rows and terminal chain columns have degree one and
failure amplitude \(1/\sqrt2\); internal chain rows and columns have degree
two and no failure amplitude.  Directly from the shared entry label,

\[
 \langle\chi_r\mid\phi_c^\sigma\rangle
 =\frac{(A_\sigma)_{rc}}2.
\tag{BE4}
\]

Choose public unitary completions

\[
 L\lvert0,r\rangle=\lvert\chi_r\rangle,
 \qquad
 R_0\lvert0,c\rangle=\lvert\phi_c^0\rangle.
\tag{BE5}
\]

Here \(R_0\) contains all public coefficient signs, including the minus sign
on each predecessor coefficient, but omits the hidden factor \(\sigma_i\).
A concrete input-independent completion uses a two-slot register.  For a
degree-two row or column, apply a Hadamard and reversibly map its two slots to
the corresponding entry labels.  For degree one, map the unused slot to the
failure label.  For a degree-zero column, map directly to its failure label.
Padded invalid addresses map bijectively to public invalid labels, and a
fixed lexicographic bijection completes the unused basis.  Thus both the
principal state preparations and their junk actions are public.

On an entry label, reversibly test whether it is the predecessor coefficient
of the signed \(d_1\)-transition row \(i\le N\), and compute that \(i\) when
it is.  Let \(S_\sigma\) multiply precisely such labels by \(\sigma_i\), and
act as the identity on all public-entry, failure, and invalid labels.  With a
standard phase-sign oracle, extended by the public dummy value
\(\sigma_0=1\), this costs exactly one coherent hidden-sign query even on a
superposition.  Then

\[
 R_\sigma=S_\sigma R_0,
 \qquad
 U_A=L^\dagger R_\sigma
\tag{BE6}
\]

is an exact rectangular projected-unitary encoding of \(A_\sigma/2\).  After
padding the row and column address spaces to a common public dimension,

\[
 \langle0,r\rvert U_A\lvert0,c\rangle
 =\frac{(A_\sigma)_{rc}}2,
 \qquad \alpha_A=2.
\tag{BE7}
\]

Each call to \(U_A\), \(U_A^\dagger\), or a controlled version uses one sign
query.  A square Hermitian interface is obtained by applying the same
state-pair construction directly to

\[
 \mathscr A_\sigma=
 \begin{pmatrix}0&A_\sigma\\A_\sigma^T&0\end{pmatrix}
 \in\mathbb R^{D\times D},
 \qquad
 D=m+n_{\rm svec}=P\frac{(k+1)(k+4)}2.
\tag{BE8}
\]

For \(k=3\), this is a \(14P\times14P\) Hermitian dilation.  Its maximum
absolute row and column sums remain two.  Each hidden entry and its transpose
compute the same local input index, so the column-state phase again gives an
exact normalization-two block encoding with one sign query per ordinary,
adjoint, or controlled call.

The right-hand side \(b\), cost \(C_0\), parameter \(t\), block layout, and
both decoding observables are public.  Consider an algorithm with either of
the preceding canonical encodings, its adjoint and controlled versions,
arbitrary input-independent gates, and unlimited public-data preparation.
The resulting **canonical-access theorem** is the following.  For \(k=3\)
and any fixed public \(t\in(0,1]\), if the algorithm outputs either

- a density operator within trace distance \(1/100\) of the central density
  state (25), or
- a state within trace distance \(1/100\) of the full central-triple state
  in Section 4.1,

then the corresponding fixed decoder computes parity with bounded error.
Replacing every encoding call by the one-query implementation above and
using the parity lower bound gives

\[
                         q_{\rm BE}\ge\frac N2=\Omega(P).
\tag{BE9}
\]

This theorem is deliberately relative to the displayed canonical unitary and
its fully specified junk action.  It does not hold automatically for an
arbitrary input-dependent unitary completion supplied for free: nonprincipal
blocks of such a completion could store prefix products or parity while its
encoded principal block remains \(A_\sigma/2\).  Any preprocessing or input
queries used to construct another completion must be charged for this
reduction to apply.

## 5. Exact SOCP boundary

For a fixed sign \(\tau\), the affine map

\[
 Z\longmapsto
 \begin{pmatrix}
  Z+e_1e_1^T&\tau e_1\\
  \tau e_1^T&1
 \end{pmatrix}
\tag{30}
\]

is a bijection from \(\mathbb S_+^k\) onto the feasible single-block slice.
Its inverse is the public affine extraction
\(Z=X_{1:k,1:k}-e_1e_1^T\), which does not depend on \(\tau\).

For \(k=2\), \(\mathbb S_+^2\) is linearly isomorphic to a
three-dimensional Lorentz cone.  Hence the original \(3\times3\) block
construction is exactly SOCP-representable, despite the noncommuting
matrices in (24).

For \(k=3\), the feasible \(4\times4\) block slice is affinely isomorphic to
\(\mathbb S_+^3\).  Fawzi proved that \(\mathbb S_+^3\) admits no lift over
any finite product of second-order cones; see
[*On representing the positive semidefinite cone using the second-order
cone*](https://arxiv.org/abs/1610.04901) (journal
[version](https://doi.org/10.1007/s10107-018-1233-0)).  This is an exact
finite-lift theorem: it rules out a projection of an affine slice of any
finite Cartesian product of Lorentz cones.  It does not, by itself, give a
lower bound for approximate SOCP lifts.
For \(k>3\), the same conclusion follows because
\(\mathbb S_+^3\) is a face of \(\mathbb S_+^k\), and SOCP
representability is preserved under affine slices.  Thus

\[
 \boxed{
 \text{the feasible block slice has a finite SOCP lift exactly when }
 k\le2.}
\tag{31}
\]

The \(k=1\) case is polyhedral after the last row and column are fixed; the
stated construction starts at \(k=2\).  The full product feasible set is
also non-SOCP-representable for \(k\ge3\), because fixing all but one factor
to feasible points recovers one non-SOCP factor as an affine slice.

## 6. What the theorem does and does not show

The following conjunction appears stronger than the earlier
\(2\times2\)-block and \(3\times3\)-block examples:

- linear-size, bounded-incidence coefficient access;
- strict primal and dual feasibility and a unique strictly complementary
  primal--dual optimum;
- noncommuting input-dependent central block values;
- exact condition-one reduced log-det geometry on the entire central path;
- uniformly bounded central triples on the entire late tail;
- native density-state and full-triple amplitude decoders with linear
  raw-query and canonical-block-encoding lower bounds; and
- genuinely non-SOCP feasible geometry in the \(4\times4\)-block case.

The last point is a cone-representation statement, not a claim that the
hidden input makes the free SDP solve difficult.  Equations (7), (11), and
(13) expose the decisive limitation: in the \(Z_i\) coordinates the
optimization problem, central path, and Hessian are identical for every
input and separable across blocks.  The input controls only the fixed
off-diagonal embedding needed to reconstruct \(X_i\).  An algorithm asked
only for the optimum value, the free Schur complements, or an
input-independent representation of the solution needs no parity queries.

The noncommutativity is also removable by an input-dependent sign
congruence.  It cannot be removed by one public simultaneous diagonalizer,
but learning which congruence to apply on the tail is exactly the hidden
parity task.  Thus the theorem is best described as a non-SOCP,
noncommuting **output-interface** lower bound with ideal reduced geometry,
not as a lower bound on abstract SDP optimization or on a supplied
block-encoding of the target density matrix.  Section 4.3 instead encodes
the equality operator, with a specified input-independent completion.

### 6.1 Established ingredients and nearby results

Schur-complement elimination, the determinant identity in (8), the log-det
barrier and its Hessian, and the scalar minimizer of (13) are standard.
Equation (24) is a direct matrix calculation.  The bounded-error quantum
query lower bound for parity is also standard.  The theorem should not claim
novelty for any of these ingredients separately.

Fawzi's theorem has precisely the scope stated above.  Two further classical
lift results are nearby but logically different.  Fawzi and Parrilo prove
exponential extension-complexity lower bounds for the cut polytope over
products of fixed-size PSD cones in
[*Exponential lower bounds on fixed-size psd rank and semidefinite extension
complexity*](https://arxiv.org/abs/1311.2571).  Fawzi, Saunderson, and Parrilo
prove exponential lower bounds for **equivariant** PSD lifts of the parity
and cut polytopes in
[*Equivariant semidefinite lifts and sum-of-squares
hierarchies*](https://arxiv.org/abs/1312.6662).  These are lower bounds on
classical formulation size.  They neither use the coefficient-query model
nor ask for a central-path matrix state, so they do not imply Section 4.

The main quantum SDP lower bounds also use different success contracts.
Brandao and Svore prove an
\(\Omega(\sqrt n+\sqrt m)\) lower bound for approximately solving an SDP in
[*Quantum Speed-ups for Semidefinite
Programming*](https://arxiv.org/abs/1609.05537).  Van Apeldoorn, Gilyen,
Gribling, and de Wolf obtain stronger parameter-dependent lower bounds by
encoding a decision in the approximate optimum of an LP, hence an SDP, in
[*Quantum SDP-Solvers: Better upper and lower
bounds*](https://arxiv.org/abs/1705.01843).  Van Apeldoorn and Gilyen give
additional lower bounds in quantum-state and quantum-operator input models
in [*Improvements in Quantum SDP-Solving with
Applications*](https://arxiv.org/abs/1804.05058).  None of these statements
is a lower bound for preparing the primal central density matrix of a
strictly feasible, condition-one-reduced SDP.

There is also no contradiction with quantum SDP state-generation upper
bounds.  Brandao, Kalev, Li, Lin, Svore, and Wu work in both sparse-matrix
and purified-quantum-state input models and, in one application, output a
circuit for a maximum-entropy density matrix matching prescribed
expectations; see
[*Quantum SDP Solvers: Large Speed-ups, Optimality, and Applications to
Quantum Learning*](https://arxiv.org/abs/1710.02581).  That target is not an
original-coordinate IPM central matrix, and the stronger quantum-state input
model can already contain data-loading work excluded by the raw oracle in
Section 4.

QIPMs of Kerenidis and Prakash
([*A Quantum Interior Point Method for LPs and
SDPs*](https://arxiv.org/abs/1808.09266)) and Augustino, Nannicini, Terlaky,
and Zuluaga
([*Quantum Interior Point Methods for Semidefinite
Optimization*](https://arxiv.org/abs/2112.06025)) use quantum linear solves
followed by tomography to obtain classical search directions and iterates.
The end-to-end analysis of Dalzell et al. explicitly identifies input-to-
output accounting and tomography as major costs; see
[*End-to-end resource analysis for quantum interior point methods and
portfolio optimization*](https://arxiv.org/abs/2211.12489).  These are
algorithmic upper bounds and resource analyses, not a raw-query lower bound
for central-state preparation.

Two later SDP developments do not change that comparison.
Mohammadisiahroudi, Augustino, Sampourmahani, and Terlaky use iterative
refinement to improve the precision dependence of an SDO QIPM in
[*Quantum Computing Inspired Iterative Refinement for Semidefinite
Optimization*](https://arxiv.org/abs/2312.11253).  Nie, An, and Wen give a
quantum ADMM upper bound for approximate SDP solutions in
[*Quantum Alternating Direction Method of Multipliers for Semidefinite
Programming*](https://arxiv.org/abs/2510.10056), revised in June 2026.
Neither paper studies the central-density or full-central-triple state-output
query problem used here.

Finally, generic quantum-linear-system lower bounds do not subsume this
example.  Orsucci and Dunjko treat the state of the solution of a supplied
positive-definite square linear system in
[*On solving classes of positive-definite quantum linear systems with
quadratically improved runtime in the condition
number*](https://arxiv.org/abs/2101.11868).  Mori, Kikuchi, Benedetti, and
Rosenkranz prove an \(\Omega(\kappa\sqrt{s})\) sparse-oracle QLS lower bound
in [*Sparsity-dependent Complexity Lower Bound of Quantum Linear System
Solvers*](https://arxiv.org/abs/2601.16697).  Here the equality-eliminated
barrier Hessian is an input-independent scalar identity and no square QLS
instance is supplied.  The hardness is in applying the input-dependent
affine loading map from the public Schur variables back to the requested
central matrix.

### 6.2 Defensible novelty boundary

A targeted search through September 2, 2026 found no primary source with the
following full conjunction: a fixed-position, bounded-incidence coefficient
oracle for a linear-size product of constant-size PSD cones; strict primal
and dual feasibility; an explicit full central path with a public complete
feasible tangent and scalar reduced log-det Hessian; noncommuting local
central blocks; genuinely non-SOCP exact feasible geometry; and an
\(\Omega(P)\) raw-query and canonical equality-operator-block-encoding lower
bound for constant-trace-distance preparation of both the
original-coordinate primal central density matrix and the fixed amplitude
encoding of the full primal--multiplier--slack central triple.
The robust extension to every PSD block vector obeying the
\(\Theta(P^{-1/2})\) equality-residual and objective promises in (29i), with
the matching neighboring-center obstruction (29n)--(29q), is part of the
same construction.  The candidate novelty should be limited to this explicit
conjunction.  This is a different lower-bound contract, not a uniformly
stronger complexity lower bound than the approximate-value bounds for
general quantum SDP solvers cited above.

In particular, the result is **not** a lower bound for outputting an
approximate optimum value, a free Schur complement, an arbitrary equivalent
representation of an optimizer, a Newton direction, or a classical
primal-dual solution.  It is not a lower bound for an algorithm supplied
with a purification or block-encoding of the target state.  It is also not
a condition-one statement for the unreduced KKT matrix: (23) concerns the
Hessian after exact equality elimination in a public orthonormal tangent
basis, while the rooted-chain constraint operator in (4) can itself be
ill-conditioned.  The full-triple statement in Section 4.1 concerns one
specified svec ordering, concatenation, and Euclidean amplitude
normalization; it does not cover every possible quantum or classical
representation of a primal--dual central point.  The robust statement in
Section 4.2 likewise requires an objective upper bound: small equality
residual alone does not force a useful trace-normalized output.

## Status

The central path, inverse, dual certificate, reduced Hessian, commutator,
density and full-triple amplitude biases, late-tail norm bounds, sparsity
counts, canonical rectangular and Hermitian equality-operator encodings,
robust approximate-primal decoder, matching residual-scale obstruction, and
SOCP boundary have been derived exactly.  The \(k=3\), \(4\times4\)-block
theorem is the recommended headline result.  Its output-interface,
public-Schur-reduction, and arbitrary-completion caveats are essential.
