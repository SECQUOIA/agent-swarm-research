# A sharp normalization--conditioning frontier for plateau Schur factors

Date: 2026-09-02

## Summary

For the signed gain-propagation block inside the linear plateau LP, improving
Schur conditioning forces the norm, and hence the block-encoding
normalization, of the **preconditioning factor** to grow. If the normalized
preconditioned Schur condition is \(K\), then

\[
 \boxed{\alpha_P\sqrt K>\frac{16N}{\pi}.}
\]

The hyperbola is tight across its full range. Approximate whitening or an
approximate inverse factor has normalization \(\Omega(N)\). A stronger
raw-access theorem shows that an \(\alpha\)-normalized approximate inverse
block encoding with setup cost \(s\) and \(q\) raw queries per invocation
obeys

\[
 \boxed{Ns+q\alpha=\Omega(N^2).}
\]

There is an equally important no-go: the already-preconditioned product can be
the identity. Thus no lower bound on its normalization and condition number
alone is possible. The cost can move into factor access, the transformed
right-hand side, or recovery.

## The signed gain block

Let \(M=17N\), with nodes \(0,\ldots,M\), and let

\[
 T=\left\lceil\frac12\log_2N\right\rceil,\qquad
 H_i=2^{\min\{i,T\}},\qquad g_i=H_i/H_{i-1}.
\]

For edge signs \(a_i=\sigma_i\) through \(i=N\) and \(a_i=1\) afterward,
define the pinned lower-bidiagonal matrix

\[
 (B_\sigma d)_0=d_0,\qquad
 (B_\sigma d)_i=d_i-g_ia_id_{i-1}.
\tag{1}
\]

Let \(\tau_0=1\), \(\tau_i=\prod_{j=1}^ia_j\), and
\(D_\tau=\operatorname{Diag}(\tau_i)\). The exact gauge identities are

\[
 B_\sigma=D_\tau B_+D_\tau,\qquad
 S_\sigma:=B_\sigma B_\sigma^T=D_\tau S_+D_\tau.
\tag{2}
\]

Thus all singular values are input-independent, although implementing the
gauge requires prefix parities.

### Lemma 1 (small singular value)

Let \(L=M-T+1\) be the number of height-\(H\), unit-gain nodes. Then

\[
 \sigma_{\min}(B_\sigma)
 \le2\sin\frac{\pi}{2(L+1)}
 \le\frac{\pi}{L+1}
 <\frac{\pi}{16N}.
\tag{3}
\]

To prove this, take a Dirichlet sine vector supported on nodes
\(T,\ldots,M\), with virtual zeros at \(T-1\) and \(M+1\). On this support,
\(B_+\) is the first-difference operator. Adding the omitted final difference
can only increase its energy, and the full Dirichlet path quotient is
\(4\sin^2(\pi/(2(L+1)))\). Equation (2) proves the signed case.

The order is tight. For \(i\ge j\),

\[
 (B_+^{-1})_{ij}=\frac{H_i}{H_j}.
\tag{4}
\]

The plateau column \(B_+^{-1}e_0=(H_i)\) has norm \(\Theta(N)\), while the
inverse Frobenius norm is \(O(N)\). Hence

\[
 \|B_\sigma^{-1}\|_2=\Theta(N).
\tag{5}
\]

## The factor frontier

### Theorem 2 (Schur whitening frontier)

Let \(P_\sigma\) be any square factor for which the preconditioned Schur matrix
is spectrally normalized as

\[
 \frac1K I\preceq
 P_\sigma S_\sigma P_\sigma^*
 \preceq I,\qquad K\ge1.
\tag{6}
\]

Then

\[
 \|P_\sigma\|_2\sqrt K
 \ge\frac1{\sigma_{\min}(B_\sigma)}
 >\frac{16N}{\pi}.
\tag{7}
\]

Consequently every block encoding \(P_\sigma/\alpha_P\) satisfies

\[
 \boxed{\alpha_P\sqrt K>\frac{16N}{\pi}.}
\tag{8}
\]

This inequality should not be presented as a new general obstruction to
quantum preconditioning.  Theorem 3 of Nie, Lai, and An,
[*Pauli-structured preconditioning for quantum linear system
solvers*](https://arxiv.org/abs/2606.01733), already proves, for an arbitrary
separately block-encoded preconditioner, the corresponding oracle-level
lower bound on the effective QLS condition parameter.  Equation (10) below
is their left-preconditioning inequality specialized to the plateau factor
(up to the harmless normalization of \(B_\sigma\)); (7) is the congruence,
square-root form for \(S_\sigma=B_\sigma B_\sigma^T\).  What is specific here
is the explicit constant, the matching plateau family, and the later
raw-sign access theorem.

Indeed, (6) gives
\(\sigma_{\min}(P_\sigma B_\sigma)\ge1/\sqrt K\). On a right singular vector
of \(B_\sigma\) for its least singular value,

\[
 \sigma_{\min}(P_\sigma B_\sigma)
 \le\|P_\sigma\|_2\sigma_{\min}(B_\sigma),
\]

which proves (7). A block-encoding normalization is at least the encoded
operator norm.

The scale-invariant form is useful. If
\(\beta=\|P_\sigma S_\sigma P_\sigma^*\|_2\) and the condition number is at
most \(K\), then

\[
 \|P_\sigma\|_2\sqrt{\frac K\beta}
 \ge\frac1{\sigma_{\min}(B_\sigma)}.
\tag{9}
\]

For a left factor used directly on \(B_\sigma\), normalized by

\[
 \sigma(P_\sigma B_\sigma)\subseteq[1/K,1],
\]

the analogous bound is

\[
 \alpha_PK\ge\|P_\sigma\|_2K
 >\frac{16N}{\pi}.
\tag{10}
\]

Two approximate forms follow immediately:

\[
\begin{aligned}
 \|P_\sigma S_\sigma P_\sigma^*-I\|_2\le\delta<1
 &\Longrightarrow
 \alpha_P\ge
 \frac{\sqrt{1-\delta}}{\sigma_{\min}(B_\sigma)},\\
 \|P_\sigma B_\sigma-I\|_2\le\delta<1
 &\Longrightarrow
 \alpha_P\ge
 \frac{1-\delta}{\sigma_{\min}(B_\sigma)}.
\end{aligned}
\tag{11}
\]

Thus constant-error approximate whitening and approximate inversion both have
\(\alpha_P=\Omega(N)\).

### Tightness throughout the tradeoff

For \(1\le a\le\Theta(N)\), define

\[
 P_\sigma^{(a)}
 =D_\tau(S_++a^{-2}I)^{-1/2}D_\tau.
\tag{12}
\]

Its norm is \(\Theta(a)\). The eigenvalues of its preconditioned Schur matrix
are

\[
 \frac{\lambda}{\lambda+a^{-2}},
 \qquad \lambda\in\sigma(S_+).
\tag{13}
\]

After an input-independent constant normalization of the largest eigenvalue,

\[
 K=\Theta((N/a)^2),\qquad
 \|P_\sigma^{(a)}\|\sqrt K=\Theta(N).
\tag{14}
\]

The endpoint \(a=1\) leaves condition \(\Theta(N^2)\) with constant factor
norm; \(a=\Theta(N)\) whitens to constant condition with factor norm
\(\Theta(N)\). This proves that (7) is sharp in order along the complete
frontier, not only at its endpoints.

## Raw-query cost of an approximate inverse block encoding

Define

\[
 F_\sigma=\operatorname{Diag}(B_\sigma^{-1},B_+^{-1}),\qquad
 G_\sigma=\operatorname{Diag}(B_\sigma,B_+),
\tag{15}
\]

and use the public input state

\[
 |r\rangle=\frac{|0,e_0\rangle+|1,e_0\rangle}{\sqrt2}.
\tag{16}
\]

By (4),

\[
 F_\sigma|r\rangle
 =\frac1{\sqrt2}
 \left((H_i\tau_i)_i\oplus(H_i)_i\right),
\qquad
 \|F_\sigma r\|_2=\left(\sum_iH_i^2\right)^{1/2}=\Theta(N).
\tag{17}
\]

Pair corresponding coordinates of the signed and unsigned blocks and measure
the side qubit in the \(X\) basis on the \(K=16N\) copy nodes. The resulting
parity-signed expectation is

\[
 \frac{KH^2}{\sum_iH_i^2}
 >\frac{16N}{17N+4/3}>\frac9{10}.
\tag{18}
\]

### Theorem 3 (inverse access--normalization tradeoff)

Suppose an offline stage makes \(s\) raw sign queries and produces a reusable
implementation of an exact \((\alpha,a,0)\) block encoding of
\(\widetilde F_\sigma\). Suppose one call to that implementation, its inverse,
or a controlled version uses at most \(q\) additional raw sign queries, and

\[
 \|\widetilde F_\sigma G_\sigma-I\|_2\le\delta
\tag{19}
\]

for a fixed \(\delta\le1/20\). Then

\[
 \boxed{\;s+O(q\alpha/N)=\Omega(N),\;}
\qquad
 \boxed{\;Ns+q\alpha=\Omega(N^2).\;}
\tag{20}
\]

The hidden constants are absolute.

From (19),

\[
 \|(\widetilde F_\sigma-F_\sigma)r\|_2
 \le\delta\|F_\sigma r\|_2.
\tag{21}
\]

Thus the normalized approximate-inverse state retains constant parity bias.
Also \(\|\widetilde F_\sigma r\|\ge(1-\delta)\Theta(N)\). Fixed-point
amplitude amplification applied to the block encoding prepares that state
with constant success using \(O(\alpha/N)\) calls. Composing with the decoder
solves parity with \(s+O(q\alpha/N)\) raw queries. Quantum parity needs
\(N/2\) queries, proving (20).

The normalization lower bound in (11) ensures \(\alpha=\Omega(N)\), so the
amplification count is never below a constant. At the optimal
\(\alpha=\Theta(N)\), (20) says that either setup or each reusable invocation
costs \(\Omega(N)\) raw queries.

The public RHS preparation and fixed output measurement use no sign queries.
If setup produces consumable quantum advice rather than a reusable unitary,
each fresh preparation must be charged to the online term.

## Exact obstructions and scope

Theorem 2 concerns the block encoding of the **factor** \(P_\sigma\), with the
preconditioned spectrum normalized as in (6). It is not a theorem about a
block encoding of the already-preconditioned product. Taking

\[
 P_\sigma=B_\sigma^{-1}
\]

makes \(P_\sigma B_\sigma=I\), whose normalization and condition number are
both one. Similarly, exact Schur whitening makes
\(P_\sigma S_\sigma P_\sigma^*=I\). Therefore no unconditional lower bound on
\(\alpha_C\kappa(C)\) for the product \(C\) can hold.

Scalar rescaling also defeats statements about
\(\alpha_PK\) unless the output spectrum is normalized; this is why (6) or
the scale-invariant expression (9) is necessary.

Nor can factor application be declared free. Any operator-norm-\(<1/3\)
implementation of \(D_\tau\) needs \(\Omega(N)\) raw sign queries: apply it to

\[
 \frac{|0\rangle+|M\rangle}{\sqrt2}
\]

and measure in the \(\{|0\rangle\pm|M\rangle\}\) basis. Since
\(\tau_0=1\) and \(\tau_M=p_N\), this computes parity with bounded error.

For a general end-to-end preconditioned solve, if setup, transformed-RHS
preparation, and recovery cost \(q_{\rm set},q_{\rm rhs},q_{\rm rec}\), and
the solver makes \(m\) block-encoding calls of raw cost \(q_{\rm BE}\), the
plateau state decoder gives the factor-independent conservation law

\[
 q_{\rm set}+q_{\rm rhs}+q_{\rm rec}+m q_{\rm BE}=\Omega(N).
\tag{22}
\]

This is the strongest unrestricted statement: an orthogonal factor rotation
can make the preconditioned matrix or its RHS public while moving the same
parity into another stage.

The analysis is for the pinned signed-gain propagation block embedded in the
plateau LP. It does not assert that every arbitrary full-KKT preconditioner
must preserve this block; unrestricted mixing can relocate the hard
subspace. The full-system invariant is the end-to-end bound (22), not the
factor norm bound (8).

The singular-value inequalities and the regularized spectral filter in
(12)--(14) are standard preconditioning tools.  In particular, neither the
general separate-factor obstruction nor spectral clipping is claimed as new.
The apparently new content is the exact sharp curve for this plateau parity
block and, more importantly, the preprocessing-aware raw-query product
\(Ns+q\alpha=\Omega(N^2)\) for a reusable approximate-inverse block encoding.

A targeted search found the following close results and one genuine
conceptual collision.
Nie, Lai, and An,
[*Pauli-structured preconditioning for quantum linear system
solvers*](https://arxiv.org/abs/2606.01733), Theorem 3 and Corollary 4, prove
the general separate-block-encoding limitation just described.  Their result
does not give a raw-coefficient setup/per-call tradeoff, nor the tight
plateau interpolation (12)--(14).
Lapworth--Sünderhauf,
[*Preconditioned Block Encodings for Quantum Linear
Systems*](https://arxiv.org/abs/2502.20908), compare normalization and
conditioning for separate-factor and precomputed-product encodings, mainly
through concrete CFD instances. Nie, Lai, and An,
in the same paper, also show how directly regrouping a Pauli representation
can evade the separate-factor limitation; this agrees with the no-go caveat
for the already-preconditioned product above.
Tong, An, Wiebe, and Lin,
[*Fast inversion, preconditioned quantum linear system solvers, and fast
evaluation of matrix functions*](https://arxiv.org/abs/2008.13295), assume
an efficiently available inverse block encoding as the positive resource;
they do not lower-bound the raw cost of compiling that resource.
Orsucci--Dunjko,
[*On solving classes of positive-definite quantum linear systems with
quadratically improved runtime in the condition
number*](https://arxiv.org/abs/2101.11868), explicitly use efficiently
block-encoded inverse or factor access as a positive resource assumption.
Low--Su,
[*Quantum linear system algorithm with optimal queries to initial state
preparation*](https://arxiv.org/abs/2410.18178), and Dalzell--Li--Su,
[*Faster quantum linear system solver beyond the condition
number*](https://arxiv.org/abs/2607.07691), sharpen solver costs once the
matrix/factor and right-hand-side or affine-dilation oracles are supplied;
they do not charge compilation of a parity-dependent inverse oracle.
Clader et al.,
[*Quantum resources required to block-encode a matrix of classical
data*](https://doi.org/10.1109/TQE.2022.3231194), give detailed circuit and
QRAM resource counts, but expressly do not prove a query lower bound of this
kind.  Finally, Arihara--Murao,
[*Sample-Query Interconversion of Block Encoding of Unknown Quantum
States*](https://arxiv.org/abs/2608.22470), prove sample/query conversion
lower bounds for unknown density operators; their input object and error
parameter are different from a reusable inverse compiled from raw LP signs.

Thus the general normalization warning collides with prior work.  No source
in this search proved the plateau-specific sharp curve together with the
preprocessing-aware product \(Ns+q\alpha=\Omega(N^2)\).  This is evidence of
apparent novelty, not proof of priority.

Status: **proof complete for the stated factor, normalization, approximation,
and reusable-oracle models.**
