# Sparse-input obstructions for Hamiltonian quantum interior-point methods

**Research note — 2026-09-02**  
**Status:** apparently new theorem candidates with complete internal proofs and a
targeted open-literature audit. Priority is not guaranteed. In particular, “not
found” below is evidence of novelty, not proof of it.

## Abstract

This note gives three results that are distinct from the support, box-LP, sparse-QLS,
and treewidth results in `notes/research-archive/2026-09-research-cycle/supporting-results/sparse-qipm-structural-results.md`.

1. The complexity proof of the quantum central-path method (QCPM) of Augustino,
   Leng, Nannicini, Terlaky, and Wu does not bound the norm required by its cited
   real-space simulator. The paper replaces a global supremum by a bound valid only
   near the central path. Its own initial center gives an explicit counterexample.
   Moreover, its time dilation treats a time-dependent coefficient as a constant.
   Correcting the clock gives, for the preprint's fixed-domain implementation, a
   simulator norm of order at least
   \(d/(a\eta\epsilon^3\log(1/\epsilon))\) for the paper's schedule, rather than the
   claimed order \(1/(a\eta\epsilon)\).
2. A path-sparse logarithmic barrier has a tridiagonal Hessian at its analytic center,
   but its inverse metric has \(\Theta(n^2)\) nonzero coefficients, with
   \(\Theta(n^2)\) of them of comparable order. This elementary witness shows that
   the condition-independent Laplace--Beltrami QIPM proposed by Gribling, Apers,
   Nieuwboer, and Walter does not inherit an entrywise sparse coefficient
   representation in standard coordinates. It is not a simulation lower bound: this
   particular Green kernel has a fast implicit representation.
3. There is a bounded-coefficient, fixed-pattern, path-sparse LP whose shifted optimal
   value and any classical point with original equality residual below \(1/2\) in
   \(\ell_1\) reveal parity, although its entire primal central path has a fixed
   support-two null basis and scalar reduced Hessian.
   A random-access oracle for one exact central point is parity-complete: it answers
   the optimization problem in one query, but constructing it from the LP oracle
   needs \(\Omega(n)\) queries. This isolates a linear original-form feasible-start
   cost hidden by a free feasible-start oracle.

The first result is a correction to a claimed complexity certificate, not a lower
bound on every implementation of the underlying idea. The second is a
standard-coordinate densification warning, not a computational lower bound. The third
is an end-to-end black-box lower bound for original-form feasible starts and an
oracle-separation theorem.

## 1. A correction to the QCPM simulation certificate

### 1.1 Setup

The target is the publicly posted
[arXiv:2311.03977v2](https://arxiv.org/html/2311.03977v2), last revised 2024-10-16;
all equation and page references below are frozen to that version. Let
\(d=m+n+2\) be the dimension of its self-dual embedding. In the preprint's notation,

\[
  s(z)=Mz+q,\qquad F(z)=z\odot s(z),\qquad
  f_\mu(z)=\frac12\lVert F(z)-\mu e\rVert_2^2 .          \tag{1}
\]

The central-path Hamiltonian is

\[
  H(\mu)=-\frac{h^2}{2}\nabla^2+f_\mu,
\]

and Algorithm 1 chooses

\[
  h(t)=a\mu(t)^2,\qquad
  a=\frac{\gamma^2}{2R_1 C_{d,\delta}},                 \tag{2}
\]

where \(C_{d,\delta}\) is the displayed concentration factor of order
\(\sqrt d+\log(1/\delta)\). More precisely, Algorithm 1 displays
\(C_{d,\delta}=\sqrt d/2+(3/4)\log(2/\delta)\), up to the paper's dimension
notation. The exact shape of this factor is immaterial below.

[Theorem 4, Section 2.3](https://arxiv.org/html/2311.03977v2#S2.SS3) defines the
simulation parameter using a global operator norm,

\[
  \lVert V\rVert_{\infty,1}
   =\int \sup_{z\in\Omega}|V(z,\tau)|\,d\tau .           \tag{3}
\]

The proof of [Theorem 5, Section 3.3](https://arxiv.org/html/2311.03977v2#S3.SS3)
truncates to a fixed box \(\Omega=[0,D]^d\) containing the central-path neighborhood.
It then says that ground-state concentration permits the assumption

\[
  \sup_{z\in\Omega} f_\mu(z)\le K\gamma^2\mu^2           \tag{4}
\]

for a small constant \(K\). Equation (4) is false.

### Proposition 1 (universal supremum counterexample)

If \(\Omega\) contains the initial center \(e=z(1)\), then for every
\(0<\mu\le1\),

\[
  \sup_{z\in\Omega}f_\mu(z)
  \;\ge\;f_\mu(e)
  \;=\;\frac d2(1-\mu)^2 .                              \tag{5}
\]

Consequently, for \(\mu=\epsilon\le1/2\), (4) requires

\[
  K\ge \frac{d}{8\gamma^2\epsilon^2}.                   \tag{6}
\]

#### Proof

The self-dual embedding is initialized so that \(s(e)=e\). Hence \(F(e)=e\), and
(1) gives

\[
 f_\mu(e)=\tfrac12\lVert(1-\mu)e\rVert_2^2
          =\tfrac d2(1-\mu)^2.
\]

Taking a supremum over a box containing \(e\) proves (5), and (6) follows when
\(\epsilon\le1/2\). ∎

Ground-state concentration is a statement about state-weighted mass. It cannot reduce
the supremum of a multiplication operator on a fixed domain. Subtracting a scalar
phase does not repair the scaling: \(f_\mu(z(\mu))=0\), so the range of the potential
on \(\Omega\) is at least the right side of (5), and the best scalar shift still has
operator norm at least half that range.

### 1.2 The correct time dilation

After dividing the evolution equation by \(h(t)\mu(t)\), the paper obtains

\[
 i\eta\,\partial_t\Psi
 =\left[-\frac{\theta(t)}2\nabla^2
       +\frac{f_{\mu(t)}}{\mu(t)h(t)}\right]\Psi,
 \qquad
 \theta(t)=\frac{h(t)}{\mu(t)}=a\mu(t).                 \tag{7}
\]

It then uses the linear substitution \(t=\eta\tau/\theta\). But \(\theta(t)\) is
not constant. The clock that normalizes the kinetic coefficient is instead

\[
  \tau(t)=\frac1\eta\int_0^t\theta(u)\,du
         =\frac a\eta\int_0^t\mu(u)\,du .               \tag{8}
\]

Indeed, \(dt/d\tau=\eta/\theta(t)\), and (7) becomes

\[
 i\partial_\tau\widetilde\Psi
 =\left[-\frac12\nabla^2
        +\frac{f_{\mu(t(\tau))}}{h(t(\tau))^2}\right]
   \widetilde\Psi .                                     \tag{9}
\]

Combining (2), (3), (8), and (9) gives the exact potential-norm expression

\[
 \boxed{
 \Lambda:=\lVert V\rVert_{\infty,1}
 =\frac1{a\eta}\int_0^1
   \frac{\sup_{z\in\Omega}f_{\mu(t)}(z)}{\mu(t)^3}\,dt .
 }                                                       \tag{10}
\]

This identity is independent of any lower-bound argument.

### 1.3 Consequence for the paper's flat schedule

The schedule is

\[
 g(t)=c_e^{-1}\int_0^t
   \exp\!\left[-\frac1{\tau(1-\tau)}\right]d\tau,
 \qquad
 \mu(t)=\epsilon+(1-\epsilon)(1-g(t)),                  \tag{11}
\]

where \(c_e\) normalizes \(g(1)=1\).

### Lemma 2 (endpoint width)

For all sufficiently small \(\epsilon\), if

\[
 u_\epsilon=\frac1{2\log(1/\epsilon)},
\]

then \(\mu(t)\le2\epsilon\) for every
\(t\in[1-u_\epsilon,1]\).

#### Proof

For \(0<u<1\), substitute \(v=1-\tau\) in the tail of (11). Since
\((1-v)v\le v\),

\[
 1-g(1-u)
 \le \frac1{c_e}\int_0^u e^{-1/v}\,dv
 \le \frac{u}{c_e}e^{-1/u}.                             \tag{12}
\]

At \(u=u_\epsilon\), the last exponential equals \(\epsilon^2\). Thus the tail is
at most \(\epsilon^2/(2c_e\log(1/\epsilon))\), which is at most \(\epsilon\) for
all sufficiently small \(\epsilon\). The tail is monotone in \(u\), proving the
claim. ∎

### Theorem 3 (corrected simulator-norm scale)

For the choices in Algorithm 1 and all sufficiently small \(\epsilon\),

\[
 \boxed{
 \Lambda\ge
 \frac{d}{128a\eta\,\epsilon^3\log(1/\epsilon)} .
 }                                                       \tag{13}
\]

If \(\Omega=[0,D]^d\), a valid global upper certificate is

\[
 \Lambda\le \frac{F_D}{a\eta\epsilon^3},\qquad
 F_D=\frac d2
 \left[D\left(D\lVert M\rVert_\infty+\lVert q\rVert_\infty\right)+1\right]^2,
                                                               \tag{14}
\]

where \(\lVert M\rVert_\infty\) is the maximum absolute row sum.

#### Proof

On the interval from Lemma 2, take \(\epsilon\le1/4\). Proposition 1 gives
\(\sup f_{\mu(t)}\ge d/8\), while \(\mu(t)^{-3}\ge(2\epsilon)^{-3}\). Its length
is \(1/(2\log(1/\epsilon))\). Substitution into (10) proves (13).

For the upper bound, every \(z\in[0,D]^d\) satisfies

\[
 |s_i(z)|\le D\lVert M\rVert_\infty+\lVert q\rVert_\infty,
\]

and hence \(f_\mu(z)\le F_D\) for \(0<\mu\le1\). Also \(\mu(t)\ge\epsilon\).
Equation (10) now gives (14). ∎

Since \(a^{-1}=2R_1C_{d,\delta}/\gamma^2\), the norm parameter required by the
theorem invoked in the QCPM paper cannot have the asserted upper bound: it is at least

\[
 \Omega\!\left(
  \frac{R_1dC_{d,\delta}}
       {\gamma^2\eta\epsilon^3\log(1/\epsilon)}
 \right),                                                \tag{15}
\]

not the claimed scale \(O(R_1C_{d,\delta}/(\eta\epsilon))\). Conditional on satisfying
the simulator's remaining smoothness, periodicity, and boundary hypotheses, inserting
the global norm bound gives the norm-based complexity certificate

\[
 O\!\left(
  \frac{F_DR_1C_{d,\delta}}
       {\gamma^2\eta\epsilon^3}
 \right)                                                 \tag{16}
\]

before polylogarithmic factors and the cost of evaluating the potential. Equation
(15) is a lower bound on the norm parameter supplied to that simulation theorem; it
is not, by itself, an unconditional quantum query lower bound for this particular
evolution.

### Corollary 4 (norm--speed tradeoff)

Let \(\mu:[0,1]\to[\epsilon,1]\) be any monotone differentiable schedule with
\(\mu(0)=1\), \(\mu(1)=\epsilon\), and
\(0<L:=\lVert\dot\mu\rVert_\infty<\infty\), and retain \(h=a\mu^2\). For
\(\epsilon\le1/4\),

\[
  \Lambda\ge \frac{d}{64a\eta L\epsilon^2}.             \tag{17}
\]

#### Proof

Traversing from \(2\epsilon\) to \(\epsilon\) takes at least \(\epsilon/L\) units
of \(t\). On that interval Proposition 1 gives \(\sup f_\mu\ge d/8\), and
\(\mu^{-3}\ge(2\epsilon)^{-3}\). Apply (10). ∎

Thus a bounded-speed fixed-domain proof cannot recover the advertised
\(\epsilon^{-1}\) norm. Taking \(L\) large weakens (17), but \(L\) must then be
included in the time-derivative, smoothness, and adiabatic estimates. Equation (17)
alone does not determine the optimized tradeoff. A different theorem could also
exploit localization in a rigorously state-dependent way.

### 1.4 Other independent correctness obligations

The norm and clock errors suffice to invalidate the stated complexity derivation.
They are not the only unresolved points.

- The schedule in (11) is nonconstant and \(C^\infty\)-flat at both endpoints, but
  is not analytic through either endpoint. The paper's quoted exponential adiabatic
  theorem assumes analytic continuation to a strip containing the closed interval.
  If (11) were analytic at an endpoint, its zero Taylor series there would make it
  locally constant. The hypotheses used in Proposition 2 therefore do not hold.
- The adiabatic theorem must be applied to the actual generator in (7), while the
  derivative discussion analyzes a differently scaled Hamiltonian and does not
  establish uniform derivative constants for the time-dependent \(h(t)\).
- The exact potential in (1) is generally quartic. The displayed Gaussian and exact
  oscillator gap belong to its quadratic harmonic approximation. The transfer to the
  exact ground state and gap is only described as valid for “sufficiently small”
  \(h\), with no threshold uniform in \(d,\mu\), or the input.
- Proposition 1 and Algorithm 1 display different choices of \(h\). The former uses
  \(h=\mu^2/(\sqrt{2d}R_1)\), with no \(\gamma\) or \(\delta\) dependence, while the
  latter uses (2). The first formula cannot by itself deliver arbitrarily prescribed
  neighborhood opening and failure probability.
- The initial exact ground state is assumed, not prepared. Knowing its minimizer
  \(e\) does not prepare the ground state of a quartic Hamiltonian.
- The cited real-space theorem assumes a smooth periodic potential and periodic
  boundary conditions. Restricting (1) to \([0,D]^d\) does not make it periodic and
  does not control boundary or truncation error.
- The box size cannot be an absolute constant without an input-size promise; it must
  at least contain the relevant central path and therefore carries a solution-radius
  dependence.

A plausible repair would require a smooth localized or clipped potential together
with proofs of low leakage, absence of spurious low-energy states, a uniform spectral
gap, correct boundary handling, and a Duhamel-type comparison to the unclipped
dynamics. Ground-state concentration alone supplies none of these statements.

## 2. Standard-coordinate inverse-metric densification

[Gribling et al.](https://arxiv.org/abs/2510.06115) replace the Euclidean Laplacian by
the Hessian-metric Laplace--Beltrami operator. In standard coordinates, if
\(G(x)=\nabla^2\phi(x)\), its principal part is governed by \(G(x)^{-1}\):

\[
 L\psi=\frac1{\sqrt{\det G}}
 \sum_{i,j}\partial_i\!\left(
   (G^{-1})_{ij}\sqrt{\det G}\,\partial_j\psi
 \right).                                                \tag{18}
\]

The following barrier is an exact sparse witness.

### Theorem 5 (path-simplex inverse-metric identity)

Let

\[
 \mathcal D_n=\{x\in\mathbb R^n:0<x_1<x_2<\cdots<x_n<1\}
\]

and use its logarithmic barrier

\[
 \phi(x)=-\log x_1-
 \sum_{i=1}^{n-1}\log(x_{i+1}-x_i)-\log(1-x_n).          \tag{19}
\]

Every inequality contains at most two variables, every variable occurs in at most
two inequalities, and the constraint-intersection graph is a path. At the analytic
center

\[
 \bar x_i=\frac{i}{n+1},
\]

the metric \(G=\nabla^2\phi(\bar x)\) is tridiagonal, but

\[
 (G^{-1})_{ij}
 =\frac{\min(i,j)(n+1-\max(i,j))}{(n+1)^3}>0            \tag{20}
\]

for every \(i,j\). Moreover, for all
\(i,j\in[\lceil(n+1)/4\rceil,\lfloor3(n+1)/4\rfloor]\),

\[
  (G^{-1})_{ij}=\Theta(1/n),                             \tag{21}
\]

so, asymptotically, \(\Theta(n^2)\) inverse-metric coefficients are of comparable
order.

#### Proof

Write the \(n+1\) slacks as

\[
 s_0=x_1,\quad s_i=x_{i+1}-x_i\ (1\le i<n),\quad
 s_n=1-x_n.
\]

At \(\bar x\), every slack is \(1/(n+1)\). If \(B=Ds\) is the signed
path-incidence Jacobian of the affine slack map, then

\[
 G=B^T\operatorname{Diag}(s^{-2})B=(n+1)^2T_n,
\]

where \(T_n\) has diagonal entries two and adjacent off-diagonal entries minus one.
The standard discrete Green's-function identity is

\[
 (T_n^{-1})_{ij}
 =\frac{\min(i,j)(n+1-\max(i,j))}{n+1}.
\]

Scaling gives (20). In the middle half, both numerator factors are bounded below by
a constant multiple of \(n\) and above by \(n\), which proves (21). ∎

Equation (18) therefore has a dense second-order coefficient tensor even at the
analytic center of a path-sparse LP barrier. At a tensor-grid point representing
\(\bar x\), a direct standard-coordinate, nondivergence-form central-difference
stencil for its principal symbol has \(\Omega(n^2)\) distinct mixed-derivative
directions, whereas the input has only \(O(n)\) nonzeros. This is a statement about
that direct stencil, not a discretization lower bound. The middle
\(\Theta(n^2)\) entries in (21) are not negligible entrywise relative to the diagonal
or maximum entry; this says nothing by itself about low-rank, quasiseparable, or
transform-based compression.

This theorem rules out only the direct inference

\[
 \text{sparse LP}\Longrightarrow
 \text{sparse Hessian metric}\Longrightarrow
 \text{entrywise sparse Riemannian coefficient tensor}.
\]

It does **not** show that every representation or simulation is expensive. In fact,
this witness is exceptionally compressible. For an arbitrary interior point, put
\(r_k=s_k^2\), \(R=\sum_{k=0}^n r_k\), and let \(i\le j\). The weighted-path
Green's function is

\[
 (G(x)^{-1})_{ij}
 =\frac{\left(\sum_{k=0}^{i-1}r_k\right)
              \left(\sum_{k=j}^{n}r_k\right)}{R}.       \tag{21a}
\]

Every strict off-diagonal block is therefore rank one, entries are available from
prefix sums, and a matrix-vector product or tridiagonal solve costs \(O(n)\)
classically without materializing the \(\Theta(n^2)\) entries. At \(\bar x\), a
discrete sine transform diagonalizes \(G\), and the ordered eigenvalues of \(G^{-1}\)
decay as \(\Theta(k^{-2})\). Slack or barycentric coordinates give another structured
representation. The explicit classical comparison is thus \(O(n)\) implicit apply
versus \(\Theta(n^2)\) materialization, not a quadratic computational lower bound.

The identity is a warning that the support of \(G\) alone cannot be handed directly
to a sparse-Hamiltonian theorem for (18). A genuine obstruction would need an oracle
lower bound invariant under permitted coordinate changes, or a sparse metric family
without an efficient implicit inverse representation. Gribling et al. do not claim
such sparse inheritance; they explicitly leave the cost of simulating the Riemannian
Schrödinger operator, and its realization in a qubit model, open.

[Abe and Nagai, *Quantum Riemannian Hamiltonian Descent*, arXiv:2603.28624](https://arxiv.org/html/2603.28624v1)
give a separate Riemannian Hamiltonian implementation proposal. Their circuit analysis
assumes sparse access to the discretized kinetic operator and notes that constructing
the required black-box oracles is generally nontrivial. Theorem 5 gives an exact LP
barrier on which standard-coordinate sparsity of that kinetic coefficient cannot be
deduced from the sparse input Hessian. It does not rule out their assumed oracle or an
implicit construction of it.

## 3. A parity-complete central-start oracle

The previous sections concern continuous Hamiltonian realizations. The next theorem
applies to feasible path-following QIPMs in the original formulation and isolates the
cost of their feasible-start assumption. It does not apply to infeasible-start or
homogeneous self-dual methods.

### 3.1 LP family

Let hidden signs \(\sigma_1,\ldots,\sigma_N\in\{-1,+1\}\), fix an absolute
constant \(\alpha\in(0,1)\) independent of \(N\) (for example, \(\alpha=1/2\)), and
define

\[
 d_i=u_i-v_i,\qquad u_i,v_i\ge0\quad(0\le i\le N).
\]

Consider

\[
\begin{aligned}
 \min\quad& \sum_{i=0}^N(u_i+v_i)+\alpha(u_N-v_N),\\
 \text{s.t.}\quad&d_0=1,\\
 &d_i-\sigma_i d_{i-1}=0\quad(1\le i\le N).
\end{aligned}                                             \tag{22}
\]

Only the signs of entries in the constraint matrix depend on the input. The support
pattern, right-hand side, and objective are fixed. Each row has at most four nonzeros,
each column at most two, all nonzero entries of \(A\) have magnitude one, all entries
of \((A,b,c)\) are bounded by two, and the constraint-intersection graph is a path.

We use a standard reversible fixed-location sparse value oracle, or its whole-row or
whole-column value analogue; the locations are fixed and known. Every row response
contains at most one hidden sign and every column response contains at most one hidden
sign. Thus one coherent matrix-oracle query is simulable with one query to the
standard sign oracle. This reduction does not assert a lower bound for arbitrary
input-dependent block encodings whose unused registers might leak additional data.

### Theorem 6 (value and original-form feasible-start separation)

Let \(p_0=1\) and \(p_i=\prod_{j=1}^i\sigma_j\). For (22):

1. It is strictly primal-dual feasible and has a unique optimum with
   \[
      \operatorname{OPT}=N+1+\alpha p_N.                 \tag{23}
   \]
   Subtracting the known constant \(N+1\) gives the shifted optimum \(\alpha p_N\)
   without changing the optimizer or central path.
   Estimating the value to additive error less than \(\alpha\) needs
   \(\Omega(N)\) bounded-error quantum input queries.
2. If a classical nonnegative output \(\widehat x\) has
   \(\lVert A_\sigma\widehat x-b\rVert_1<1/2\), then it determines \(p_N\).
   Producing such a point also needs \(\Omega(N)\) queries.
3. Conditional on a feasible offset, the primal central path separates into
   \(N+1\) identical scalar problems. It has an input-independent support-two
   orthonormal null basis and a scalar reduced primal-barrier Hessian, hence condition
   number one, for every \(\mu>0\).
4. At \(\mu=3/4\), one query to a reusable random-access value oracle for the exact
   primal central point reveals \(p_N\), but preprocessing that oracle from the LP
   input needs \(\Omega(N)\) queries.

#### Proof

Feasibility forces \(d_i=p_i\). Put \(q_i=u_i+v_i\). Nonnegativity is equivalent
to \(q_i\ge1\), and

\[
 u_i=\frac{q_i+p_i}{2},\qquad
 v_i=\frac{q_i-p_i}{2}.                                  \tag{24}
\]

The objective is \(\sum_iq_i+\alpha p_N\). Its unique minimum has every \(q_i=1\),
which proves (23). Taking \(q_i=2\) gives strict primal feasibility. With the usual
dual convention \(A^Ty+s=c\), setting \(y=0\) gives \(s=c>0\), because the final
two objective coefficients are \(1\pm\alpha\). Thus strict dual feasibility also
holds. Equation (23) reveals the parity of the signs. The polynomial method of
[Beals et al.](https://arxiv.org/abs/quant-ph/9802049) gives quantum query complexity
\(\Theta(N)\) for parity, proving the first lower bound under the stated oracle
reduction.

For the original-form feasibility statement, define residuals

\[
 r_0=\widehat d_0-1,\qquad
 r_i=\widehat d_i-\sigma_i\widehat d_{i-1}.
\]

Telescoping gives

\[
 \widehat d_N-p_N
 =\sum_{j=0}^N
   \left(\prod_{k=j+1}^N\sigma_k\right)r_j,              \tag{25}
\]

and therefore
\(|\widehat d_N-p_N|\le\sum_j|r_j|\). If the latter is below \(1/2\), the sign of
\(\widehat d_N\), obtained directly from the classical output coordinates
\(\widehat u_N,\widehat v_N\), is \(p_N\). This proves the second lower bound with
the same success probability. Nonnegativity is not needed for this decoding step.

On the feasible affine space, the primal log-barrier objective is

\[
 \Phi_\mu(q)=\sum_{i=0}^Nq_i+\alpha p_N
 -\mu\sum_{i=0}^N\log\frac{q_i^2-1}{4}.                 \tag{26}
\]

Every central coordinate is the positive solution of
\(q^2-1=2\mu q\):

\[
 q(\mu)=\mu+\sqrt{\mu^2+1}.                             \tag{27}
\]

The Hessian in \(q\)-coordinates is

\[
 \mu\left[(q+1)^{-2}+(q-1)^{-2}\right]I.               \tag{28}
\]

Equivalently, the vectors
\(V_i=(e_{u_i}+e_{v_i})/\sqrt2\) form a fixed orthonormal null basis. To see
completeness, any null direction has \(\delta d_0=0\) and recursively
\(\delta d_i=\sigma_i\delta d_{i-1}=0\), so
\(\delta u_i=\delta v_i\). If
\(H_x=\mu\operatorname{Diag}(u_0^{-2},\ldots,u_N^{-2},v_0^{-2},\ldots,v_N^{-2})\)
is the full-space barrier Hessian, then

\[
 V^TH_xV
 =2\mu\left[(q+1)^{-2}+(q-1)^{-2}\right]I,             \tag{29}
\]

twice (28) because a unit null coordinate changes \(q\) by \(\sqrt2\). This proves
the condition-one statement. It is also the primal-dual central path: defining
\(s_\mu=\mu X_\mu^{-1}e\), the identity \(q^2-1=2\mu q\) gives
\(s_{u_i}+s_{v_i}=2=c_{u_i}+c_{v_i}\). Hence
\(V^T(c-s_\mu)=0\), and full row rank of \(A\), already implied by the null-space
calculation, gives a dual vector \(y_\mu\) with \(A^Ty_\mu+s_\mu=c\).

At \(\mu=3/4\), (27) gives \(q=2\). By (24), the central pair at index \(i\) is
\((3/2,1/2)\) when \(p_i=1\), and its swap when \(p_i=-1\). Define the reusable
value oracle by
\(O_x|i,z\rangle=|i,z\mathbin\oplus\operatorname{enc}(u_i,v_i)\rangle\), either
exactly or with coordinate error below \(1/2\). One lookup at \(i=N\) reveals
\(p_N\). If preprocessing this oracle from \(A\) used \(o(N)\) LP queries, composing
the preprocessing with that lookup would contradict the parity lower bound. ∎

The result is stronger than an output-length observation: it lower-bounds a scalar
value, an \(\ell_1\)-feasibility certificate, and construction of a random-access
central-start oracle. It also identifies exactly where the advice sits. Once the
prefix signs \(p_i\) are supplied as a feasible offset, every reduced primal-barrier
Newton system in the fixed null basis is scalar diagonal; deriving that offset from
the original sparse matrix is parity-hard. This statement is not about every KKT or
normal-equation formulation.

The theorem does not say that every QIPM must be feasible or must use this start
representation. It says that a complexity statement conditional on a free feasible
central-start oracle can hide \(\Theta(N)\) end-to-end input queries even on a
path-sparse family with condition-one reduced primal-barrier Hessians. A homogeneous
self-dual embedding does provide a different universal start: for example, the
embedding used by QCPM constructs an enlarged skew-symmetric system with exact center
\(z=s=e\) at \(\mu=1\), and each embedded data query for this family is computable
from \(O(1)\) sign queries. The theorem does not lower-bound that initialization; the
parity cost then moves into the embedded evolution, recovery, or value readout.

A classical scan computes all prefix signs, the optimum, and the original central
oracle in \(\Theta(N)\) time, matching the quantum lower bound. Classical
bounded-treewidth LP algorithms are also near-linear on this family. The novelty
candidate is therefore the conjunction of the original-form start-oracle separation,
path sparsity, and trivial reduced primal-barrier geometry, not a new parity adversary
method or an unconditional quantum advantage claim.

## 4. Literature and novelty audit

The search was run through 2026-09-02 over the local literature corpus, arXiv, and
general web indices.

### QCPM correction

- [Augustino et al., *A quantum central path algorithm for linear optimization*,
  arXiv:2311.03977v2](https://arxiv.org/abs/2311.03977) is the primary object of
  Proposition 1 and Theorem 3.
- [Chakrabarti et al., arXiv:2503.24332v2, Section 4.4](https://arxiv.org/html/2503.24332v2#S4.SS4)
  identify broader missing error controls in the Childs et al. pseudo-spectral
  analysis used by QCPM.
- [Gribling et al., arXiv:2510.06115v1, Section 1.4](https://arxiv.org/html/2510.06115v1#S1.SS4)
  state that the real-space simulator appears not to control all relevant errors and
  that no suitable directly applicable infinite-dimensional adiabatic theorem is
  known.

Those later criticisms overlap with Section 1.4, so that broad criticism is not
claimed as new. No public revision, correction, or source was found that gives the explicit
\(f_\mu(e)\) counterexample, identifies the variable-clock error, derives (10), proves
the \(\epsilon^{-3}/\log(1/\epsilon)\) consequence, or states the norm--speed
tradeoff (17).

### Inverse metric

- [Gribling, Apers, Nieuwboer, and Walter, *Self-concordant Schrödinger operators:
  spectral gaps and optimization without condition numbers*, arXiv:2510.06115](https://arxiv.org/abs/2510.06115)
  prove the Riemannian spectral-gap result and explicitly leave the simulation and
  computational-model questions open.
- [Abe--Nagai, arXiv:2603.28624](https://arxiv.org/abs/2603.28624) propose a
  Riemannian Hamiltonian simulation under sparse discretized-kinetic-oracle access and
  explicitly note the difficulty of constructing that oracle. This anticipates the
  general access concern, though not the ordered-simplex identity.
- Dense Green's functions of sparse elliptic operators are classical. Novelty is not
  claimed for the inverse formula itself. The candidate contribution is the exact
  path-simplex log-barrier witness and its sparse-QIPM access consequence.

No source was found that specializes the open Riemannian-QIPM implementation problem
to a path-sparse LP and proves the \(\Theta(n^2)\) inverse-metric coefficient statement
in Theorem 5.

### Original-form feasible starts

- Existing feasible QIPMs explicitly take a feasible central-neighborhood point as an
  input; for example, [Wu et al., arXiv:2301.05357](https://arxiv.org/html/2301.05357)
  state this initialization in their algorithm.
- Classical IPM texts treat Phase I as a separate optimization problem. Homogeneous
  self-dual and infeasible-start methods avoid the original-form assumption, so they
  are outside Theorem 6. General LP
  quantum query lower bounds, including the value lower bounds in
  [Apers--Gribling, arXiv:2311.03215](https://arxiv.org/abs/2311.03215), do not give
  the central-start oracle separation above.

The \(\Omega(N)\) value exponent itself is not new: the general row-query lower bound
of Apers--Gribling already specializes to that scale for square constant-sparse LPs.
The candidate contribution is the simultaneous fixed-support path structure,
original-feasible-output decoder, condition-one reduced primal-barrier geometry, and
central-start advice-oracle separation.

No quantum lower bound for constructing an original-form feasible central-start
oracle, or a path-sparse separation with condition-one reduced primal-barrier
Hessians matching Theorem 6, was found. Prefix-product parity gadgets themselves are
classical and also appear in quantum query reductions such as
[Dürr et al., arXiv:quant-ph/0401091](https://arxiv.org/abs/quant-ph/0401091); novelty
is claimed only for the LP central-path and access-model packaging.

## 5. Publication assessment and next proofs

The QCPM correction is the most immediately publishable item: it is short, universal,
and falsifies the exact norm estimate used in a headline complexity theorem of the
arXiv preprint. A
standalone correction should lead with Proposition 1 and (10)--(13), carefully state
that this invalidates the preprint's derivation rather than proving an algorithmic
lower bound, and invite a localized-simulation repair.

The path-simplex theorem is an elementary motivating identity, not by itself a
publishable computational obstruction. A stronger paper would turn it into one of the
following:

1. a lower bound for constructing an inverse-metric block encoding from a sparse
   barrier oracle;
2. a matching special-purpose simulation algorithm using implicit Green's-function
   or electrical-flow access; or
3. a representation theorem characterizing when a sparse coordinate change keeps
   both the metric and the potential efficiently queryable.

The original-form feasible-start theorem is already a complete representation-relative
oracle separation. The next useful extension is a robust infeasible-start or
self-dual-embedding version in an \(\ell_2\) residual neighborhood, or a formal
comparison between forward sparse access to \(A\) and the stronger transpose/location
oracles assumed by QLSA-based implementations.
