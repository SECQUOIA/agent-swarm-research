# A sparse \(2\times2\) block-SDP parity lower bound—and why it is LP-reducible

Date: 2026-09-02

## Verdict

A proposed block-SDP construction is correct.  It gives a linear raw-query
lower bound for preparing either a normalized primal density matrix or a
Frobenius-amplitude state at an exact SDP center.  The instance has:

- \(P=17N+1\) blocks of size \(2\times2\);
- one input-dependent `svec` coefficient per hidden bit, row and column
  sparsity two, and coefficient magnitude one;
- a public cost matrix and right-hand side;
- primal, slack, and equality-multiplier coordinates bounded by absolute
  constants;
- reduced log-det Hessian condition number exactly one; and
- a fixed output observable with constant parity bias.

The inverse scale remains: the center is at \(\mu=1/P\), its positive slack
eigenvalues are \(\Theta(1/P)\), and constant \(\mu\) would make a path
multiplier grow as \(\Theta(P)\).

This is not a genuinely semidefinite hardness mechanism.  A \(2\times2\) PSD
cone is a three-dimensional Lorentz cone, and the particular fixed-trace,
fixed-off-diagonal slice here is a one-dimensional interval.  Its log-det
barrier is exactly the logarithmic barrier of two nonnegative LP slacks.  The
construction is therefore a clean block-SDP realization of the existing
signed-copy/output-loading obstruction, not a stronger noncommutative result.

## 1. Frobenius-isometric `svec` formulation

Use

\[
 \operatorname{svec}
 \begin{pmatrix}a&b\\b&c\end{pmatrix}
 =(a,\sqrt2b,c),
\tag{1}
\]

so Euclidean inner products of `svec` vectors equal Frobenius inner products.
Let

\[
 I_2=\begin{pmatrix}1&0\\0&1\end{pmatrix},
 \qquad
 G=\frac1{\sqrt2}\begin{pmatrix}0&1\\1&0\end{pmatrix}.
\tag{2}
\]

Then \(\operatorname{svec}(I_2)=(1,0,1)\),
\(\operatorname{svec}(G)=(0,1,0)\), and
\(\langle G,X\rangle=\sqrt2X_{12}\).  These \(\sqrt2\) factors are needed;
using the unscaled off-diagonal entry would not be Frobenius-isometric.

Let \(N\ge2\), \(K=16N\), and \(P=N+K+1=17N+1\).  Define

\[
 a_i=\begin{cases}
       \sigma_i,&1\le i\le N,\\
       1,&N<i<P,
     \end{cases}
 \qquad
 \tau_0=1,
 \qquad
 \tau_i=\prod_{j=1}^ia_j.
\tag{3}
\]

The primal variable is a product of PSD blocks
\(X=(X_0,\ldots,X_{P-1})\in(\mathbb S_+^2)^P\).  Impose

\[
\begin{aligned}
 \langle I_2,X_i\rangle&=4 &&(0\le i<P),\\
 \langle G,X_0\rangle&=\sqrt2,\\
 \langle G,X_i\rangle-a_i\langle G,X_{i-1}\rangle&=0
     &&(1\le i<P).
\end{aligned}
\tag{4}
\]

Use the public block cost \(C_i=I_2\).  In `svec` coordinates, every trace row
is \((1,0,1)\), the root row selects one off-diagonal coordinate, and every
transition row has entries \((1,-a_i)\) in two off-diagonal coordinates.
Thus the measurement matrix has \(2P\) rows, \(3P\) columns, maximum row and
column sparsity two, maximum absolute row and column sums two, and entry
magnitude one.  Exactly one coefficient position depends on each
\(\sigma_i\).  Its right-hand side consists of \(P\) copies of four and one
entry \(\sqrt2\), and is public.

The trace rows are independent on the diagonal coordinates.  The signed
off-diagonal rows form an invertible lower-bidiagonal matrix.  Hence the
complete measurement matrix has full row rank \(2P\).

## 2. Exact center with bounded coordinates

Set \(\mu=1/P\) and define

\[
 X_i^*=\begin{pmatrix}2&\tau_i\\\tau_i&2\end{pmatrix},
 \qquad
 S_i^*=\frac\mu3
 \begin{pmatrix}2&-\tau_i\\-\tau_i&2\end{pmatrix}.
\tag{5}
\]

The eigenvalues of \(X_i^*\) are \(1,3\), and those of \(S_i^*\) are
\(\mu/3,\mu\).  Equations (3)--(4) give primal feasibility, while direct
multiplication gives

\[
                         X_i^*S_i^*=\mu I_2.
\tag{6}
\]

Let \(\beta_i\) be the trace-row multiplier and \(\alpha_i\) the signed
off-diagonal-row multiplier.  In the convention

\[
                 \mathcal A_\sigma^*y+S=C,
\tag{7}
\]

take

\[
 \beta_i=1-\frac{2\mu}{3},
 \qquad
 \alpha_j=\frac{\sqrt2\mu}{3}\tau_j(P-j).
\tag{8}
\]

Indeed, the diagonal stationarity equation is
\(\beta_i+2\mu/3=1\).  The off-diagonal `svec` equation is

\[
       (B_\sigma^T\alpha)_i
       +\sqrt2(S_i^*)_{12}=0,
 \qquad
       B_\sigma^T\alpha=\frac{\sqrt2\mu}{3}\tau,
\tag{9}
\]

whose backward recurrence is exactly (8).  Therefore (5),(8) satisfy all
central KKT equations.  Full row rank makes the multiplier unique.

At \(\mu=1/P\),

\[
 \|X^*\|_{\max}=2,
 \qquad
 \|S^*\|_{\max}\le\frac{2}{3P},
 \qquad
 \|\alpha\|_\infty\le\frac{\sqrt2}{3},
 \qquad
 \|\beta\|_\infty\le1.
\tag{10}
\]

Thus every primal, slack, and multiplier coordinate is bounded.  Conversely,
(8) shows directly that constant \(\mu\) gives
\(\|\alpha\|_\infty=\Theta(P)\).  The construction avoids that accumulation
by using inverse complementarity.

## 3. Reduced log-det geometry

The equality constraints fix the trace and off-diagonal entry of every block.
An orthonormal basis of the feasible tangent space is

\[
 H_i=\frac1{\sqrt2}
 \begin{pmatrix}1&0\\0&-1\end{pmatrix}
\tag{11}
\]

in block \(i\), with zero in every other block.  For the barrier
\(-\mu\sum_i\log\det X_i\), its reduced Hessian has diagonal entries

\[
 \mu\operatorname{Tr}
 \left[(X_i^*)^{-1}H_i(X_i^*)^{-1}H_i\right]
 =\frac\mu3.
\tag{12}
\]

Different blocks have zero cross terms.  Hence

\[
                       H_{\rm red}=\frac\mu3I_P,
 \qquad \kappa(H_{\rm red})=1.
\tag{13}
\]

The condition number is exactly one, although the absolute eigenvalue scale
is \(1/(3P)\).

## 4. Two constant-bias output interfaces

Let \(O=\{N+1,\ldots,N+K\}\) be the public copy suffix.  Every
\(i\in O\) has \(\tau_i=p_N:=\prod_{j=1}^N\sigma_j\).

### Density-matrix output

Regard the block direct sum as one positive matrix and normalize its trace:

\[
 \rho_\sigma
 =\frac{\bigoplus_{i=0}^{P-1}X_i^*}{4P}.
\tag{14}
\]

Define the fixed contraction

\[
 \mathcal O_{\rm den}
 =\bigoplus_{i=0}^{P-1}O_i,
 \qquad
 O_i=\begin{cases}
       \begin{pmatrix}0&1\\1&0\end{pmatrix},&i\in O,\\
       0,&i\notin O.
      \end{cases}
\tag{15}
\]

Then \(\|\mathcal O_{\rm den}\|=1\) and

\[
 \operatorname{Tr}(\mathcal O_{\rm den}\rho_\sigma)
 =p_N\frac{K}{2P},
 \qquad
 \frac{K}{2P}\ge\frac{16}{35}.
\tag{16}
\]

The binary POVM \((I\pm\mathcal O_{\rm den})/2\), with a fair sign on its
zero-observable sector, therefore reports parity with constant bias.

### Frobenius-amplitude output

The `svec` block of \(X_i^*\) is

\[
                         (2,\sqrt2\tau_i,2),
 \qquad \|X_i^*\|_F^2=10.
\tag{17}
\]

Apply the fixed orthogonal change from the two diagonal coordinates to their
normalized sum and difference.  On the suffix, swap the diagonal-sum
coordinate with the off-diagonal coordinate.  This fixed norm-one observable
has expectation in the normalized amplitude state

\[
 \left|X_\sigma^*\right\rangle_F
 :=\frac{\operatorname{svec}(X^*)}{\sqrt{10P}}
\tag{18}
\]

equal to

\[
 p_N\frac{4K}{5P},
 \qquad
 \frac{4K}{5P}\ge\frac{128}{175}.
\tag{19}
\]

Both decoders use one copy and no input-dependent operation.

## 5. Raw-query lower bound

Give an algorithm coherent sparse position/value access to the `svec`
measurement matrix of (4), with all public data free.  Count every query made
during preprocessing, advice construction, or state preparation.  One matrix
value query is simulated with at most one query to the corresponding sign
\(\sigma_i\).

Suppose the algorithm outputs either a density operator within trace distance
\(1/100\) of (14), or a state within trace distance \(1/100\) of (18).  The
fixed measurements in Section 4 then compute parity with bounded error.
The polynomial method gives a lower bound of \(N/2\) quantum sign queries for
parity.  Consequently either output task needs

\[
                         q\ge\frac N2=\Omega(P)
\tag{20}
\]

raw coefficient queries.  Querying all \(N\) signs and preparing the target
shows tightness up to a factor two.

This is an input-oracle theorem.  A supplied input-dependent block encoding,
prefix table, or target-state oracle can already contain the parity and is not
free in this model.

## 6. Exact reduction to an LP interval

Every feasible block has the form

\[
 X_i(r_i)=
 \begin{pmatrix}2+r_i&\tau_i\\\tau_i&2-r_i\end{pmatrix}.
\tag{21}
\]

Since \(\sqrt3<2\), positive semidefiniteness is equivalent to

\[
                         |r_i|\le\sqrt3.
\tag{22}
\]

Set

\[
                   \ell_i=\sqrt3+r_i,
             \qquad u_i=\sqrt3-r_i.
\tag{23}
\]

Then \(\ell_i,u_i\ge0\), \(\ell_i+u_i=2\sqrt3\), and

\[
                  \det X_i(r_i)=3-r_i^2=\ell_iu_i.
\tag{24}
\]

Therefore the SDP log-det barrier restricts exactly to

\[
                 -\log\det X_i=-\log\ell_i-\log u_i,
\tag{25}
\]

the standard logarithmic barrier for two nonnegative LP variables with one
sum equality.  The center \(r_i=0\) is simply \(\ell_i=u_i=\sqrt3\).

More generally, \(\mathbb S_+^2\) is linearly isomorphic to the
three-dimensional Lorentz cone; see Fawzi,
[*On representing the positive semidefinite cone using the second-order
cone*](https://doi.org/10.1007/s10107-018-1233-0).  The extra equalities here
reduce even that second-order cone to the interval (22).

At the selected center all blocks are also diagonal in the same public
Hadamard basis:

\[
 H X_i^*H^T=\operatorname{Diag}(2+\tau_i,2-\tau_i).
\tag{26}
\]

Thus the density decoder reads a classical eigenvalue swap in a public basis;
it does not witness noncommuting SDP geometry.

## 7. Scope and novelty calibration

The construction is a valid sparse product-cone SDP and a useful consistency
check for SDP output models.  It shows that condition-one reduced log-det
geometry and bounded center coordinates do not make exact density-state or
amplitude-state preparation query-efficient.  It also makes all `svec`
normalizations and the native density observable explicit.

It has four important limitations.

1. The cone is the product \((\mathbb S_+^2)^P\).  Embedding it as one
   unrestricted \(2P\times2P\) PSD block while explicitly forcing every
   off-block entry to zero would add quadratically many constraints.  The
   linear sparsity statement relies on the standard block-SDP/product-cone
   representation.
2. The feasible slice and its barrier are exactly LP-reducible by
   (21)--(25).  This is not a noncommutative SDP lower bound.
3. The public objective is constant on the feasible set because every trace
   is fixed.  The theorem concerns exact central-state preparation, not
   finding a unique or nontrivial optimum.
4. The lower bound is driven by signed affine propagation into the requested
   output, not by solving an ill-conditioned reduced Hessian.  The inverse
   slack scale \(\mu=1/P\) remains visible despite reduced condition one.

No exact local note or targeted open-literature result was found for this
particular density-output formulation.  Nevertheless, because of the exact
LP interval reduction, it should be presented only as an SDP corollary or
output-interface example.  A genuinely stronger block-SDP result would need
higher-dimensional blocks or constraints whose feasible tangent directions
do not reduce to independent intervals, ideally with noncommuting central
blocks or Newton directions.

As an independent arithmetic check, dense `svec` systems for
\(N=2,5,17\) had exact primal residual zero, maximum dual residual below
\(4.5\times10^{-17}\), and complementarity residual below
\(3.5\times10^{-18}\).  The reduced Hessian eigenvalues were all exactly
\(\mu/3\) to floating-point precision.  The observed density biases were
\(0.4571,0.4651,0.4690\), and the amplitude biases were
\(0.7314,0.7442,0.7503\), matching (16) and (19).
