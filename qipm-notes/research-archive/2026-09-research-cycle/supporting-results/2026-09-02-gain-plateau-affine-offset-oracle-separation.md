# Linear-size affine-offset oracle separation for the gain--plateau LP

## Result and relation to the earlier separation

The gain--plateau family in
`2026-09-02-linear-size-robust-gain-parity-lp.md` gives a stronger, linear-size
version of the nullspace/affine-offset separation.  With \(P=17N+1\) nodes, its
entire reduced barrier problem is public and its late central-path reduced Hessian
has condition number below \(7/6\).  Nevertheless, preparing an original-primal
state for any nonnegative point in a fixed global feasibility-residual tube needs

\[
 \Omega(N)=\Omega(P)
\]

raw local coefficient queries.

This is a formal access-model corollary of the robust gain--plateau state theorem,
not an additional lower-bound exponent.  Compared with the parallel-path
separation, it improves \(\Omega(\sqrt P)\) to \(\Omega(P)\), but gives up two
features: the reduced Hessian is merely uniformly conditioned rather than a scalar
identity, and the bound holds for a late central tail rather than the entire path.
The construction also has primal dynamic range \(\Theta(\sqrt P)\).  These
tradeoffs must accompany the stronger dimension dependence.

## Family and public data

Let \(N\ge2\),

\[
 T=\left\lceil\frac12\log_2N\right\rceil,
 \qquad K=16N,\qquad P=N+K+1=17N+1,
\]

and index nodes by \(i=0,\ldots,N+K\).  Define the public heights and gains

\[
 H_i=2^{\min\{i,T\}},\qquad
 g_i=H_i/H_{i-1}\in\{1,2\},
 \qquad H=2^T\in[\sqrt N,2\sqrt N).
\]

For hidden \(\sigma\in\{-1,1\}^N\), set \(a_i=\sigma_i\) on the first \(N\)
edges and \(a_i=1\) on the following \(K\) edges.  Let

\[
 \tau_0=1,\qquad \tau_i=\prod_{j=1}^i a_j.
\]

At node \(i\), the nonnegative variables are \((u_i,v_i,h_i,t_i)\), with
\(d_i=u_i-v_i\) and \(q_i=u_i+v_i\).  The equalities are

\[
\begin{aligned}
 d_0&=1,&d_i-g_ia_id_{i-1}&=0,\\
 h_0&=1,&h_i-g_ih_{i-1}&=0,\\
 &&q_i+t_i-2h_i&=0,
\end{aligned}                                                   \tag{1}
\]

and the objective is

\[
 \min\sum_i(2u_i+2v_i+h_i+t_i).                              \tag{2}
\]

The tree/path topology, support, \(b,c\), heights, and gains are public.  Only a
coefficient in each of the first \(N\) signed transition rows depends on the
input.  The matrix has full row rank, and \(\|b\|_2=\sqrt2\).

## The hidden coset and its canonical offsets

Define the public orthonormal columns

\[
 W_i=\sqrt{\frac23}
 \left(\frac12e_{u_i}+\frac12e_{v_i}-e_{t_i}\right).          \tag{3}
\]

They lie in \(\ker A_\sigma\): they preserve \(d,h\) and the cap equality.
There are \(P\) such columns, while \(A_\sigma\) has \(4P\) columns and \(3P\)
independent rows.  Hence they form a complete input-independent orthonormal basis
of the nullspace for every \(\sigma\).

Exact feasibility fixes

\[
 h_i=H_i,qquad d_i=H_i\tau_i.                              \tag{4}
\]

Thus every point in the affine equality space is uniquely parameterized by

\[
 x_\sigma(q)_i=
 \left(\frac{q_i+H_i\tau_i}{2},
       \frac{q_i-H_i\tau_i}{2},H_i,2H_i-q_i\right),          \tag{5}
\]

and it is nonnegative exactly when \(H_i\le q_i\le2H_i\).
Taking the optimal boundary value \(q_i=H_i\), define

\[
 (x_\sigma^{\rm off})_i
 =H_i\left(\frac{1+\tau_i}{2},
            \frac{1-\tau_i}{2},1,1\right).                  \tag{6}
\]

Then

\[
 \{x:A_\sigma x=b\}
 =x_\sigma^{\rm off}+\operatorname{range}(W),               \tag{7}
\]

and, for any \(q\),

\[
 x_\sigma(q)=x_\sigma^{\rm off}+W\xi,
 \qquad \xi_i=\sqrt{\frac32}(q_i-H_i).                      \tag{8}
\]

The complete quotient coordinate of the affine feasible set modulo
\(\operatorname{range}(W)\) is therefore the weighted sign vector

\[
 (d_i)_i=(H_i\tau_i)_i.                                    \tag{9}
\]

This, and only this, is hidden from the reduced parameterization.  On the
\(K=16N\) plateau nodes after edge \(N\), it equals \(Hp_N\), where
\(p_N=\prod_{j=1}^N\sigma_j\).  Nullspace motion changes \(u_i,v_i\) equally and
cannot alter or reveal (9).

Even the canonical minimum-norm particular solution is input-dependent.  The
squared norm at node \(i\) is

\[
 \frac{q_i^2+H_i^2}{2}+H_i^2+(2H_i-q_i)^2,
\]

which is uniquely minimized at \(q_i=4H_i/3\).  Consequently,

\[
 A_\sigma^\dagger b
 =x_\sigma\!\left(\frac43(H_i)_i\right).                    \tag{10}
\]

The null projector \(WW^T\) and row-space projector \(I-WW^T\) are public, but
(10) is not.  It has pair difference \(H_i\tau_i\) at every node.  Thus computing
the standard initializer \(A_\sigma^T(A_\sigma A_\sigma^T)^{-1}b\) is part of
the charged input processing, even though its target row subspace is known.

Any exact random-access feasible-offset oracle with absolute error below
\(H/3\) at one known plateau pair reveals \(p_N\) from \(u_i-v_i\).  A
constant-success amplitude-state oracle for (6) also reveals parity with constant
probability: \(\|x_\sigma^{\rm off}\|^2=3\sum_iH_i^2\), while the selected pair
coordinates on the plateau carry squared mass \(KH^2=16NH^2\), a constant
fraction of that norm.  Such an oracle therefore cannot be granted for free in a
raw coefficient-query theorem.

## The full reduced barrier is input-independent

On (5), the local objective is \(q_i+3H_i\), and the product of the four primal
coordinates is

\[
 u_iv_ih_it_i
 =\frac{q_i^2-H_i^2}{4}\,H_i(2H_i-q_i).                    \tag{11}
\]

Both expressions depend on \(H_i\) but not on \(\tau_i\).  Hence the complete
reduced logarithmic-barrier objective is public:

\[
 \Phi_\mu(q)=\sum_i\left[
 q_i+3H_i-
 \mu\log\left(\frac{q_i^2-H_i^2}{4}H_i(2H_i-q_i)\right)
 \right].                                                    \tag{12}
\]

All its values, gradients, Hessians, higher derivatives, feasible boxes, and
central solutions are independent of \(\sigma\).  Write the central coordinate
as \(q_i=H_i+z_i(\mu)\), where \(z_i(\mu)\in(0,H_i)\) is the unique solution of

\[
 \frac1\mu
 =\frac1{2H_i+z_i}+\frac1{z_i}-\frac1{H_i-z_i}.           \tag{13}
\]

Only \(T+1=O(\log N)\) distinct public heights occur, so the full central vector
is specified by a public table of that many scalars.  In the orthonormal
coordinates (3), its reduced Hessian is the public diagonal matrix

\[
 \Lambda_\mu=\operatorname{diag}(\lambda_i(\mu)),             \tag{14}
\]

where

\[
 \lambda_i(\mu)=\frac{2\mu}{3}\left[
 (2H_i+z_i)^{-2}+z_i^{-2}+(H_i-z_i)^{-2}
 \right].                                                     \tag{15}
\]

For \(0<\mu\le1/16\), the audited estimates

\[
 \frac{15}{16}\mu\le z_i(\mu)<\mu
\]

give

\[
 \frac2{3\mu}<\lambda_i(\mu)<\frac7{9\mu},
 \qquad \kappa(\Lambda_\mu)<\frac76.                        \tag{16}
\]

Thus one may grant for free clean circuits or exact oracles for \(W,W^T\), both
orthogonal projectors, the entire function (12) and all its derivatives, the
central scalar table \((z_h(\mu))_h\), the exact reduced central vector, and
\(\Lambda_\mu\), \(\Lambda_\mu^{-1}\), or their block encodings.  One may also
grant arbitrary input-independent preprocessing and state preparation of any
reduced-coordinate vector.  None of these operations implements the affine
translation (6) or the original-coordinate loading map (8).

## Linear-size oracle-separation theorem

**Theorem 1 (public reduced geometry, hard original-coordinate loading).**
Consider the LP family (1)--(2) in the coherent fixed-position sparse row/value
oracle model, or the analogous fixed-position sparse column model.  In addition
to raw access to \(A_\sigma\), grant an algorithm, at zero cost and with unlimited
calls and precision, arbitrary clean quantum oracles, circuits, and advice that
are identical for every \(\sigma\).  In particular, the grant may contain every
public reduced object listed after (16), including exact reduced solves on the
whole path.

Suppose that for every \(\sigma\), the algorithm outputs an unconditional density
operator \(\rho_\sigma\) for which there is a nonzero \(x_\sigma\ge0\) such that

\[
 \frac{\|A_\sigma x_\sigma-b\|_2}{\|b\|_2}\le\frac1{100},
 \qquad
 D_{\rm tr}\left(\rho_\sigma,
 |x_\sigma/\|x_\sigma\|\rangle
 \langle x_\sigma/\|x_\sigma\||\right)\le\frac1{100}.       \tag{17}
\]

Then the algorithm makes \(\Omega(N)=\Omega(P)\) queries to the raw local
coefficient oracle.  The conclusion remains true under any additional primal
centrality-neighborhood or two-sided objective-accuracy condition.  It also holds
for a constant-success heralded output when the repetitions used to obtain
successful copies are charged.

For every prescribed \(\mu>0\), preparing a state within trace distance \(1/10\)
of the exact original-primal central state requires \(\Omega(P)\) raw queries.
When \(0<\mu\le1/16\), this holds while the reduced Hessian at that point and
throughout the remaining central tail has condition number below \(7/6\).

### Proof

All freely granted oracles and advice are, by hypothesis, the same channel or
state for every hidden string; in particular they have no input-dependent phase
or garbage register.  They can be hardwired as free operations in a quantum query
algorithm for parity.

A raw sparse row or column query exposes at most one \(\sigma_i\).  The queried
position and corresponding sign index are determined by the public path.  Such a
query, including a coherent superposition query, is therefore simulated
reversibly with at most one standard sign-oracle query.  Free reduced-oracle calls
need no sign queries.

For the first claim, the robust decoder proved in the gain--plateau state theorem
applies to every nonnegative vector satisfying (17), without using centrality or
objective accuracy.  A fixed measurement of a constant number of independently
prepared output states recovers \(p_N\) with bounded error.  Thus \(Q\) raw
coefficient queries would give a bounded-error parity algorithm using \(O(Q)\)
sign queries.  Bounded-error quantum parity requires \(\Omega(N)\) queries, and
\(P=17N+1\).

For the stronger exact-central-state error constant, let

\[
 S=\{N+1,\ldots,N+K\},\qquad
 O_S=\sum_{i\in S}
 (|u_i\rangle\langle u_i|-|v_i\rangle\langle v_i|).
\]

For every exact central point, \(q_i\in(H_i,2H_i)\).  Its local squared norm is

\[
 \frac{q_i^2+H_i^2}{2}+H_i^2+(2H_i-q_i)^2
 \le\frac72H_i^2.                                          \tag{18}
\]

The audited height sum satisfies

\[
 \sum_iH_i^2<\frac{53}{3}NH^2.                             \tag{19}
\]

On every plateau node, \(d_i=p_NH\), so

\[
 p_N\langle O_S\rangle
 =\frac{\sum_{i\in S}p_Nd_iq_i}{\|x_{\sigma,\mu}\|^2}
 \ge\frac{16NH^2}{(7/2)(53/3)NH^2}
 =\frac{96}{371}.                                          \tag{20}
\]

Trace distance \(1/10\) changes the expectation of the norm-one observable
\(O_S\) by at most \(1/5\), leaving bias at least
\(96/371-1/5>0\).  A constant number of measurements therefore computes parity.
The same oracle simulation proves \(\Omega(N)=\Omega(P)\) raw queries.  Equation
(16) supplies the late-tail condition statement. \(\square\)

## Access boundary and caveats

This is the strongest natural coefficient-query formulation because arbitrary
input-independent reduced computation has already been made free.  It excludes
the following input-dependent resources:

1. a particular feasible point such as (6) or (10), in random-access or
   constant-success amplitude-state form;
2. a QRAM table of \(\tau_i\), or a loading isometry implementing
   \(\xi\mapsto x_\sigma^{\rm off}+W\xi\);
3. a global or batch oracle that aggregates the hidden coefficients in a way not
   simulable by a constant number of raw sign queries.

Each excluded resource can already contain the endpoint parity.  A complexity
analysis that assumes one as free input has moved the hard work outside the
counted reduced solve.

The theorem is a sharper **linear-size interface separation** than the
parallel-path corollary, but it is not a new lower bound independent of the robust
gain--plateau theorem.  Nor is it a universal statement about all nullspace or OSS
QIPMs.  The original signed propagation block has condition \(\Theta(N)\), even
though the late reduced barrier Hessian is well conditioned.  The result does not
show that every KKT formulation is well conditioned or that every feasible-offset
construction takes linear time.

The primal dynamic range is \(H=\Theta(\sqrt P)\), the optimum is
\(\Theta(P^{3/2})\), and the optimal vector norm is \(\Theta(P)\).  These scales
are the mechanism that permits a linear-size residual-robust amplifier with
constant raw coefficients.  The result uses the global right-hand-side-relative
residual in (17), with \(\|b\|_2=\sqrt2\); it does not cover a row-normalized RMS
residual, scale-invariant backward error, stronger batch access, scalar objective
output, or a reduced Newton-direction output.  The unconditional-versus-heralded
qualification in Theorem 1 is also essential.

In QIPM terms, the family makes the accounting boundary explicit.  The public
reduced central solve has a known right-hand side, public diagonal matrix, and
condition below \(7/6\) on the tail.  Its coefficient-query cost can be zero.
The \(\Omega(P)\) cost lies in producing a feasible affine offset or realizing the
reduced answer as an original-variable amplitude state.
