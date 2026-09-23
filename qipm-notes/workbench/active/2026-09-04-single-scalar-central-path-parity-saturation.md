# A single-scalar central-path direct sum, and why it is not an iteration lower bound

Status: Proved; independently audited; targeted literature screen completed  
Started: 2026-09-04  
Paper status: Not incorporated  
Confidence: High on the theorem and oracle accounting; moderate on novelty

## Main result

There is a constant-row-and-column-sparse box LP with a unique optimizer,
\(T\) scale-separated central-path transitions, and \(L\) independent hidden
signs assigned to each transition such that both one scalar coordinate at one
final central point and the corresponding exact optimizer coordinate have
bounded-error quantum query complexity

\[
 \boxed{Q=\Theta(TL).}                                      \tag{1}
\]

The output is one real number, not \(T\) checkpoint values or an explicit
iterate. The same fixed input oracle is used throughout, arbitrary coherent
adaptivity and persistent workspace are allowed, and every full sparse-matrix
query is simulated by at most one query to a hidden sign. Thus (1) removes
the explicit-output loophole from the earlier checkpoint direct sums. The
bounded sign output uses \(O(1)\) classical bits at the stated accuracy.
The formulation has only \(2T\) inequalities, so its ordinary product log
barrier has parameter \(2T\); all parity propagation is carried by sparse
equalities.

The terminal coordinate can be kept in \([-1,1]\), and constant additive
error suffices. It is an affine parity carrier, not an averaged statistic,
so coherent mean estimation does not remove the \(T\) factor. The scope is
nevertheless important. In a static-input oracle model the
path does not reveal fresh data online: a solver required to return only the
terminal scalar may ignore all intermediate checkpoints. Consequently (1)
is a single-output endpoint hardness theorem with a scale-separated path
realization, not an unconditional \(\Omega(L)\)-per-iteration lower bound.

## 1. Sparse equality-chain blocks

For signs

\[
 \sigma_{j,1},\ldots,\sigma_{j,L}\in\{-1,+1\},
 \qquad h_j=\prod_{k=1}^L\sigma_{j,k},                      \tag{2}
\]

introduce one boxed activation \(\alpha_j\) and free equality-chain variables
\(x_{j,0},\ldots,x_{j,L}\):

\[
 -1\leq\alpha_j\leq1,\qquad
 x_{j,0}=\alpha_j,\qquad
 x_{j,k}=\sigma_{j,k}x_{j,k-1}\quad(1\leq k\leq L).
                                                               \tag{3}
\]

The equalities force

\[
 x_{j,L}=h_j\alpha_j.                                     \tag{4}
\]

Append the public diagnostic summation chain

\[
 s_1=x_{1,L},\qquad
 s_j=s_{j-1}+x_{j,L}\quad(2\leq j\leq T),\qquad W=s_T,
                                                               \tag{5}
\]

and order the \(TL\) signs as
\(\tau_1,\ldots,\tau_{TL}\).  The bounded carrier is the sparse affine chain

\[
 r_0=\alpha_T,\qquad
 r_m=\tau_mr_{m-1}\quad(1\leq m\leq TL),\qquad w=r_{TL}.
                                                               \tag{6}
\]

For every fixed input these are linear equalities.  Equations (3), (5), and
(6) have at most three nonzeros per row.  Every column has constant
incidence, and every hidden coefficient has magnitude one.

## 2. The scale-separated LP

Fix \(\Gamma=256\), put \(\theta_j=\Gamma^{-j}\), and consider

\[
 \begin{aligned}
 \max\quad&2\sum_{j=1}^T\theta_j\alpha_j,\\
 \text{subject to}\quad&-1\leq\alpha_j\leq1\quad(j\in[T]),\\
 &\text{the equalities \((3)\), \((5)\), and \((6)\).}
 \end{aligned}                                             \tag{7}
\]

The relative-interior point \(\alpha_j=0\), with all chain variables zero,
is strictly feasible.  After eliminating the equalities, the feasible set is
the cube \([-1,1]^T\).  Since every \(\theta_j>0\), the optimizer is unique:
\(\alpha_j^*=1\), with every free variable then uniquely fixed by the
equalities.  In particular, \(w^*=H:=\prod_jh_j\).  The formulation has
\(\Theta(TL)\) variables, equations, and nonzeros, but only \(2T\) scalar
inequalities.  Its row and column sparsity are bounded by numerical constants.
The objective and right-hand sides are public; only the signs in (3) and (6)
are hidden.

At objective multiplier \(\eta\ge0\), the logarithmic
barrier subproblem is

\[
 -\sum_{j=1}^T\log(1-\alpha_j^2)
 -2\eta\sum_{j=1}^T\theta_j\alpha_j.                       \tag{9}
\]

With

\[
 \rho(z)=\frac{\sqrt{1+4z^2}-1}{2z}
 =\frac{2z}{1+\sqrt{1+4z^2}},\qquad \rho(0)=0,             \tag{10}
\]

so that \(\rho/(1-\rho^2)=z\), strict convexity and separability give

\[
 \alpha_j(\eta)=\rho(\eta\theta_j),\qquad
 \boxed{W(\eta)=\sum_{j=1}^Th_j\rho(\eta\theta_j),\qquad
 w(\eta)=H\rho(\eta\theta_T),\quad H=\prod_{j=1}^Th_j.}    \tag{11}
\]

## 3. Every selected transition isolates one block

Set

\[
 \eta_t=\Gamma^{t+1/2}\quad(0\le t\le T),\qquad
 D_t=W(\eta_t)-W(\eta_{t-1})\quad(1\le t\le T).            \tag{12}
\]

Then

\[
 D_t=\sum_{j=1}^Th_jd_{t-j},\qquad
 d_m=\rho(\Gamma^{m+1/2})-\rho(\Gamma^{m-1/2}).             \tag{13}
\]

The \(d_m\) are nonnegative and telescope over \(m\in\mathbb Z\) to one.
The elementary bounds

\[
 \rho(z)\le z,\qquad 1-\rho(z)\le\frac1{2z}                \tag{14}
\]

imply

\[
 d_0\ge1-\frac{3}{2\sqrt\Gamma}=\frac{29}{32},\qquad
 \sum_{m\ne0}d_m\le\frac3{32}.                             \tag{15}
\]

Truncation to the actual \(T\) blocks only decreases off-diagonal mass, so

\[
 |D_t-d_0h_t|\le1-d_0\le\frac3{32},\qquad
 h_tD_t\ge2d_0-1\ge\frac{13}{16}.                          \tag{16}
\]

Thus transition \(t\) contains exactly block parity \(h_t\), with a constant
margin independent of \(T\). This is a structural property of the path; the
algorithm below need not output any \(D_t\).

## 4. One bounded final scalar saturates the direct sum

At the last selected multiplier \(\eta_T=\Gamma^{T+1/2}\), equation (11)
and (14) give

\[
 |w(\eta_T)-H|
 =1-\rho(\sqrt\Gamma)\le\frac1{2\sqrt\Gamma}=\frac1{32}.
                                                               \tag{17}
\]

Suppose an algorithm returns one number \(\widehat w\) such that

\[
 |\widehat w-w(\eta_T)|\le\frac14                           \tag{18}
\]

with probability at least \(2/3\) on every input. Its sign is \(H\), because
the total error from \(H\) is at most \(9/32<1\). Since

\[
 H=\prod_{j=1}^Th_j
 =\prod_{j=1}^T\prod_{k=1}^L\sigma_{j,k},                  \tag{19}
\]

the estimate computes parity of all \(TL\) hidden input bits. Bounded-error
quantum parity needs \(\Omega(TL)\) queries. Reading every sign and evaluating
(11) gives the matching \(O(TL)\) upper bound. Randomized classical query
complexity is also \(\Theta(TL)\).

The same conclusion holds for the exact optimizer coordinate because
\(w^*=H\).  More quantitatively, every feasible point of objective gap
\(\tau\) obeys

\[
 1-\alpha_T\leq {\tau\over2\theta_T},\qquad
 |w-H|=1-\alpha_T.                                        \tag{19a}
\]

Thus the scale-separated choice transfers the lower bound to feasible
approximate optimizers when \(\tau<\theta_T/2\).  Since
\(\theta_T=\Gamma^{-T}\), this is exponentially fine additive objective
accuracy.  Taking all \(\theta_j=1\) instead gives the same unique-optimizer
coordinate lower bound at constant objective gap, but removes the separated
path scales.

The public diagnostic accumulator also yields a separate additive-statistic
version. At \(\eta_{\mathrm f}=16T\Gamma^T\),

\[
 \left|W(\eta_{\mathrm f})-\sum_{j=1}^Th_j\right|\le\frac1{32}. \tag{20}
\]

Thus estimating \(W(\eta_{\mathrm f})\) to error \(1/4\) also costs
\(\Theta(TL)\), because rounding recovers \(\sum_jh_j\) and hence \(H\).
After normalization by \(T\), however, this asks for \(O(1/T)\) accuracy.
The bounded carrier \(w\) avoids that accuracy qualification by realizing
outer parity inside the sparse affine slice.

## 5. Same-instance full-SQ accounting

Use the reversible sign oracle

\[
 O_\sigma|j,k,z\rangle
 =|j,k,z\mathbin\oplus(1-\sigma_{j,k})/2\rangle.            \tag{21}
\]

The support pattern, every row and column norm, and every nonzero magnitude
of the LP matrix are public. A hidden sign appears once in its local equality
in (3) and once in its carrier equality in (6).  Every row contains at most
one hidden sign, and every column is incident to at most one hidden-sign
coefficient.  Hence an indexed sparse-entry query or normalized row/column
state preparation is simulated by at most one sign query; norm and support-
sampling queries need none. Querying either duplicate still queries the same
raw input bit once. Therefore a \(q\)-query full-SQ algorithm for (18) yields
an \(O(q)\)-query parity algorithm on the same fixed oracle.

The scales \(\theta_j=256^{-j}\) and multiplier \(\eta_T\) have \(O(T)\)-bit
descriptions. Hidden coefficients have one-bit signs and constant magnitude.
There is no fresh LP sample per checkpoint and no hidden high-precision
input-dependent number.

## 6. Static-oracle temporal collapse

The construction exposes a general obstruction.

> **Lemma (static-oracle temporal collapse).** Let one fixed oracle \(O_x\)
> define an optimization instance and a public sequence of \(T\) path
> parameters. If correctness asks only for a final relation \(R(x,y)\), with
> no online output or memory restriction, intermediate path parameters impose
> no query obligation. Every query algorithm for \(R\) is valid even if it
> never constructs an intermediate iterate. Therefore the fact that
> checkpoint \(t\) contains an independent answer does not by itself justify
> summing \(T\) one-checkpoint lower bounds.

This is a model statement. Static query complexity charges total access to
\(O_x\), not when the analytic path makes a datum geometrically salient. A
genuine per-iteration lower bound needs an online-answer contract,
sequentially revealed input, a persistent-memory cap, or a proof that the
required final function itself has a direct-product lower bound.

Here the last alternative applies: \(w(\eta_T)\) determines the
outer parity of all block parities. A solver may nevertheless compute that
parity directly and skip the path. The theorem lower-bounds total
same-instance endpoint cost, not when the cost must be paid.

For comparison, there is a quantitative obstruction for additive
statistics. If one block bit has an exact
coherent evaluator costing \(q_0\) raw queries, amplitude estimation
approximates

\[
 \frac1T\sum_{j=1}^T\frac{1+h_j}{2}                        \tag{22}
\]

to additive error \(\epsilon\) using
\(O(q_0\min\{T,1/\epsilon\})\) queries. A direct sum cannot survive at
constant normalized accuracy for an averaged scalar. It saturates only at
\(\epsilon=O(1/T)\), as in (20). This does not apply to the parity carrier:
parity is not an expectation and has quantum query complexity \(T\) even
when its output is one bounded bit.

## 7. Literature and novelty

The parity lower bound is the polynomial method of Beals et al.,
[*Quantum lower bounds by polynomials*](https://arxiv.org/abs/quant-ph/9802049).
The mean-estimation obstruction is the standard algorithm of Brassard,
Høyer, Mosca, and Tapp,
[*Quantum amplitude amplification and estimation*](https://arxiv.org/abs/quant-ph/0005055).
Perfect adversary composition is prior art; see Belovs and Lee,
[*The quantum query complexity of composition with a relation*](https://arxiv.org/abs/2004.06439).

Optimization scalar-output composition is also prior art. Apers and Gribling,
[*Quantum speedups for linear programming via interior point
methods*](https://arxiv.org/abs/2311.03215), embed Boolean composition in an
LP optimum. The local batched-holonomy note already proves the exact
\(q_0\min\{T,1/\epsilon\}\) law for an averaged sparse-SDP scalar. The local
multiplexed-LP note proves a \(T\)-fold lower bound for returning all
scale-separated increments, while the lazy-central-oracle note explains why
static trajectory data can be cached.

A targeted search found no prior theorem combining one fixed
constant-row-and-column-sparse LP, \(T\) isolated constant-margin central-path
transitions, one final central-point scalar, matched full-SQ
\(\Theta(TL)\) quantum complexity, and the explicit separation between total
endpoint hardness and unavoidable cost at each iteration. The lower-bound
ingredient and normalized-accuracy frontier are known; the defensible novelty
is this central-path realization, the bounded affine parity carrier, and the
scope theorem.

## 8. Assessment

Explicit checkpoint output is not necessary for a linear-total-input lower
bound: one succinct scalar can retain all \(T\) hidden blocks. But without
an online or memory contract, this does not imply an intrinsic
\(\Omega(L)\) charge at each of \(T\) QIPM iterations. Static-oracle query
complexity sees the terminal function, not central-path chronology. Nor is
this a normalized-state lower bound: the amplitude of one designated
coordinate can shrink with the total dimension, and the free
accumulator/carrier coordinates can change the normalization further.
