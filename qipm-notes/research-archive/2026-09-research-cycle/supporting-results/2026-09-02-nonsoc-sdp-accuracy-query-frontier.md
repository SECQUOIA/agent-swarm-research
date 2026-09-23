# Accuracy--query frontier for the non-SOCP Schur-block SDP family

Date: 2026-09-02

## Result

For the \(k=3\) family of
[2026-09-02-nonsoc-schur-block-sdp-parity.md](2026-09-02-nonsoc-schur-block-sdp-parity.md),
the \(L^{-1/2}\) approximate-feasibility scale can be inverted into the
worst-case raw-query curve

\[
 Q_{\rm abs}(P,\varepsilon)
 =\Omega\!\left(\min\{P,\varepsilon^{-2}\}\right).
\tag{1}
\]

The theorem uses a precise relational output contract.  The output must be
the trace-normalized density matrix of some blockwise PSD primal point whose
Euclidean equality residual is at most \(\varepsilon\) and whose objective is
no larger than the designated exact center's objective.  No centrality,
dual-feasibility, or complementarity promise is needed.

Both the exponent and the query order are sharp for the tuned family.  An
average of single-bit-flipped exact centers has the wrong parity and residual
\(2\sqrt{2/N}\), while reading all \(N\) signs prepares an exact valid output.
Thus this is a robust output-synthesis frontier, not a lower bound on the
public scalar reduced Hessian.

## 1. Active non-SOCP instance

Let \(N\ge2\), \(K=16N\), and \(L=N+K+1=17N+1\).  Use \(L\) blocks
\(X_i\in\mathbb S_+^4\), indexed by \(0\le i<L\).  Put

\[
 a_i=\begin{cases}\sigma_i,&1\le i\le N,\\1,&N<i<L,\end{cases}
 \qquad
 \tau_0=1,
 \qquad
 \tau_i=\prod_{j=1}^ia_j.
\tag{2}
\]

In Frobenius-isometric `svec` coordinates, let

\[
 d_i=\sqrt2(X_i)_{14},
 \qquad
 u_i=\sqrt2(X_i)_{24},
 \qquad
 v_i=\sqrt2(X_i)_{34},
 \qquad
 z_i=(X_i)_{44}.
\]

The four rooted chains are

\[
\begin{aligned}
 d_0&=\sqrt2,&d_i-a_id_{i-1}&=0,\\
 u_0&=0,&u_i-u_{i-1}&=0,\\
 v_0&=0,&v_i-v_{i-1}&=0,\\
 z_0&=1,&z_i-z_{i-1}&=0,
 \qquad 1\le i<L.
\end{aligned}
\tag{3}
\]

They fix the last column to \((\tau_i,0,0,1)^T\).  The free Schur
complement is in \(\mathbb S_+^3\), so each block slice has no finite SOCP
lift.  The rows have at most two nonzeros, the columns have sparsity at most
two, all nonzero magnitudes are one, and exactly one coefficient position
depends on each hidden sign.

For a positive scale \(\lambda\), use block cost

\[
 C_i=\lambda\operatorname{Diag}(I_3,2).
\tag{4}
\]

At \(t=1\), the exact center is

\[
 X_i^{\rm cen}=
 \begin{pmatrix}I_3+e_1e_1^T&\tau_i e_1\\
                 \tau_i e_1^T&1\end{pmatrix},
 \qquad
 \sum_i\langle C_i,X_i^{\rm cen}\rangle=6\lambda L.
\tag{5}
\]

Let \(T=\{N+1,\ldots,N+K\}\).  On this public suffix,
\(\tau_i=p:=\prod_{j=1}^N\sigma_j\).

## 2. Robust residual-to-density theorem

**Theorem 1.**  Let \(X=(X_0,\ldots,X_{L-1})\) be arbitrary matrices
satisfying

\[
 X_i\succeq0,
 \qquad
 \|\mathcal A_\sigma(X)-b\|_2\le\varepsilon,
 \qquad
 \sum_i\langle C_i,X_i\rangle\le6\lambda L.
\tag{6}
\]

If

\[
                         \varepsilon\le\frac1{4\sqrt L},
\tag{7}
\]

then the density matrix

\[
                         \rho_X=\frac{\bigoplus_iX_i}
                                           {\sum_i\operatorname{tr}X_i}
\tag{8}
\]

reveals \(p\) with constant bias under one fixed binary POVM.

### Proof

Let \(r_0=d_0-\sqrt2\) and
\(r_i=d_i-a_id_{i-1}\).  This signed-chain residual is a subvector of the
full residual, so \(\|r\|_2\le\varepsilon\).  Define
\(q_i=\tau_i d_i\) and \(e_i=\tau_i r_i\).  Then

\[
 q_i=\sqrt2+\sum_{j=0}^ie_j.
\tag{9}
\]

For \(i\in T\), \(q_i=pd_i\).  Summing (9) over \(T\) gives

\[
 p\sum_{i\in T}d_i
 =K\sqrt2+\sum_{j=0}^{L-1}w_je_j,
\tag{10}
\]

where \(w_j\) is the number of suffix indices \(i\in T\) with \(i\ge j\).
Every \(0\le w_j\le K\), so \(\|w\|_2\le K\sqrt L\).  Cauchy--Schwarz and
(7) imply

\[
 p\sum_{i\in T}d_i
 \ge K(\sqrt2-\sqrt L\,\varepsilon)>K.
\tag{11}
\]

Let \(O\) be zero off \(T\) and equal to
\(e_1e_4^T+e_4e_1^T\) on each suffix block.  It is a Hermitian contraction,
and

\[
 p\operatorname{tr}\!\left(O\bigoplus_iX_i\right)
 =\sqrt2p\sum_{i\in T}d_i>\sqrt2K.
\tag{12}
\]

Positive semidefiniteness makes every diagonal entry nonnegative.  Hence the
objective cap gives

\[
 \sum_i\operatorname{tr}X_i
 \le\sum_i[\operatorname{tr}(X_i)_{1:3,1:3}+2(X_i)_{44}]
 \le6L.
\tag{13}
\]

Combining (8), (12), and (13),

\[
 p\operatorname{tr}(O\rho_X)
 >\frac{\sqrt2K}{6L}>\frac15.
\tag{14}
\]

Thus \((I\pm O)/2\) reports parity with advantage greater than \(1/10\).
An output state within trace distance \(1/100\) of \(\rho_X\) retains
advantage greater than \(9/100\).  \(\square\)

The objective cap in (6) can be replaced by the trace bound in (13).  Some
such normalization assumption is essential: without it one may add an
arbitrarily large positive matrix in the unconstrained top-left blocks and
dilute the density observable while keeping equality residual zero.  The PSD
assumption is also essential both to define the density output and to infer
(13) from the positive cost.

## 3. Sharpness of the residual exponent

Fix a base input \(\sigma\).  For every \(j\in[N]\), flip only \(\sigma_j\)
and let \(X^{(j)}\) be that neighboring input's exact center (5).  Their
average

\[
                         \overline X=\frac1N\sum_{j=1}^NX^{(j)}
\tag{15}
\]

is blockwise PSD and has the same objective as (5).  Every neighbor has
parity \(-p\), so every suffix block of \(\overline X\) is exactly the
opposite-parity center.

Evaluated in the base constraints, neighbor \(j\) violates only signed row
\(j\).  In isometric `svec` units that violation has magnitude \(2\sqrt2\).
The average therefore has \(N\) disjoint residual coordinates of magnitude
\(2\sqrt2/N\), and

\[
                 \|\mathcal A_\sigma(\overline X)-b\|_2
                 =2\sqrt{\frac2N}.
\tag{16}
\]

Its normalized density matrix has constant bias toward \(-p\).  Thus no
theorem based only on PSD, the objective cap, and equality residual can force
the correct density output at a radius asymptotically larger than
\(N^{-1/2}\).  Equations (7) and (16) match in exponent; the constants are not
optimized.

## 4. The two-parameter query curve

Let \(Q_{\rm abs}(P,\varepsilon)\) be the worst-case raw coefficient-query
complexity over this family with at most \(P\) PSD blocks, under the output
contract (6)--(8).  This is a family-level worst-case curve: the hard hidden
length is chosen as a function of the requested accuracy.

The access model is coherent fixed-position sparse value access to the
equality map.  Its support, right-hand side, cost, and block layout are public;
all oracle calls used in preprocessing and output preparation are counted.
One coefficient-value query is simulated with at most one query to the
corresponding raw sign.  No input-dependent block encoding, prefix table, or
target-state oracle is supplied for free.

For \(0<\varepsilon\le1/8\), choose

\[
 N=\left\lfloor
     \min\left\{\frac{P-1}{17},\frac1{2048\varepsilon^2}\right\}
   \right\rfloor,
 \qquad L=17N+1.
\tag{17}
\]

Outside the irrelevant range \(N<2\), this is
\(\Theta(\min\{P,\varepsilon^{-2}\})\), and

\[
 \varepsilon^2L
 \le\frac{17}{2048}+\frac1{64}<\frac1{16}.
\]

Hence (7) holds.  Composing any valid output procedure with the fixed POVM
computes parity, which has quantum query complexity at least \(N/2\).
Therefore (1) follows.

The right-hand side of the active instance has norm \(\sqrt3\).  For
\(0<\eta\le1/8\), a
relative promise

\[
 \frac{\|\mathcal A_\sigma(X)-b\|_2}{\|b\|_2}\le\eta,
\]

choose
\[
 N=\left\lfloor
     \min\left\{\frac{P-1}{17},\frac1{6144\eta^2}\right\}
   \right\rfloor.
\]
The same proof gives

\[
 Q_{\rm rel}(P,\eta)
 =\Omega\!\left(\min\{P,\eta^{-2}\}\right)
\tag{18}
\]

in the corresponding nontrivial range.

For the tuned instance, reading all \(N\) signs, forming their prefixes, and
preparing the exact center gives a matching \(O(N)\) raw-query upper bound.
This is query tightness for this explicit family, not a universal upper bound
for arbitrary SDPs.

## 5. Exact-\(P\) public padding without density dilution

The at-most-\(P\) convention is the cleanest theorem.  An exact block count is
also possible.  Let \(M=P-L\), set the common cost scale and selected central
parameter to

\[
                         \lambda=\mu=\frac1P,
\tag{19}
\]

and retain the \(L\) active blocks above.  Add \(M\) public dummy blocks
\(Y_h\in\mathbb S_+^4\).  For each dummy, use ten one-coordinate equality
rows fixing its complete isometric-svec vector to that of

\[
                              Y_h=P^{-1}I_4.
\tag{20}
\]

Give it the same cost \(P^{-1}\operatorname{Diag}(I_3,2)\).  The exact
objective cap becomes

\[
 B_{P,L}=\frac{6L}{P}+\frac{5M}{P^2}.
\tag{21}
\]

For every blockwise PSD approximate output obeying this cap,

\[
 \operatorname{tr}\!\left(\bigoplus_iX_i\oplus\bigoplus_hY_h\right)
 \le PB_{P,L}=6L+\frac{5M}{P}\le6L+5.
\tag{22}
\]

The recurrence proof uses only active residual rows, so (11)--(12) are
unchanged.  Equation (14) is replaced by

\[
 p\operatorname{tr}(O\rho)>\frac{\sqrt2K}{6L+5}>\frac15
 \qquad(N\ge2).
\tag{23}
\]

Thus exact padding does not dilute any valid density output, even when
\(P\gg L\).

The padded formulation remains sparse and regular.  The ten dummy rows form
an identity matrix on the ten svec coordinates, so they are independent and
introduce no tangent modes.  At (19), the dummy central slack is
\(\mu Y_h^{-1}=I_4\); equality multipliers make dual stationarity exact and
have magnitude at most one.  Along \(0<\mu\le1/P\), all dummy primal, slack,
and multiplier coordinates remain bounded.  At the optimum the fixed dummy
has rank four and may be paired with zero slack, so it is strictly
complementary.  The active reduced Hessian remains a scalar identity, while
the dummy sector has no reduced coordinates.  Since at least one active slice
is affinely isomorphic to \(\mathbb S_+^3\), the complete feasible set still
has no finite SOCP lift.

The padded right-hand side satisfies

\[
                         \|b_{\rm pad}\|_2^2
                         =3+\frac{4M}{P^2}<4
\tag{24}
\]

for \(P>4\).  Hence replacing the constant \(6144\) in the relative choice
by \(8192\) proves (18) for exactly \(P\) blocks as well.

The single-flip mixture (15), with the same public dummy blocks on every
neighbor, still has residual (16), the exact objective (21), and wrong
constant density bias.  This proves sharp-order residual tightness after
padding too.

## 6. Scope

1. The output is the trace-normalized primal density matrix.  A robust
   Frobenius-amplitude or complete primal--dual-state theorem would need
   stronger per-block norm control; a trace cap alone allows Frobenius mass to
   concentrate.
2. The result assumes an unconditional output state.  Heralded preparation
   is covered only when its success amplification is charged.
3. The exact-\(P\) statement uses the product cone
   \((\mathbb S_+^4)^P\).  Encoding it as one unrestricted \(4P\times4P\)
   PSD matrix and explicitly killing all off-block entries costs quadratically
   many scalar equalities.
4. In Schur-complement coordinates the active conic optimization and reduced
   Hessian are public and input-independent.  The query lower bound is for
   reconstructing affine-fixed original matrix entries.
5. Equation (1) is a reparameterized worst-case family bound.  It does not
   say that one fixed instance reveals more hidden bits as the requested
   residual tolerance decreases.
