# Projective lazy refresh for changing sparse Newton systems

Date: 2026-09-02

Status note, 2026-09-20: this is a superseded research record. The current
pathwise theorem and its exact-test hypotheses are in paper Section 13;
[the Lean verification report](../../../formal/REFRESH.md) records its proof
scope. The phrase below about imperfect tests is not a proved extension:
controlling false rejections requires an explicit additional guarantee.
Other claims in this note remain subject to the corrections listed in
[the archive guide](../../../RESEARCH_NOTES.md).

## Pathwise theorem

Consider the realized sequence of nonsingular Newton systems

\[
 H_tz_t=f_t,
 \qquad q_t=\|z_t\|_2,
 \qquad \psi_t=z_t/q_t.
\]

Normalize the systems projectively:

\[
 M_t=\frac{q_t}{\|f_t\|_2}H_t,
 \qquad
 \delta_t=\|M_{t+1}(\psi_{t+1}-\psi_t)\|_2,
 \qquad
 V_{\rm proj}=\sum_t\delta_t.
\tag{1}
\]

At a refresh iteration \(s\), a QLSA plus tomography returns a classical
\(\widehat z_s\) with relative residual \(\epsilon\).  At a later iteration
\(t\), compute the scalar

\[
 a_t=\arg\min_a\|H_t(a\widehat z_s)-f_t\|_2
\tag{2}
\]

using one current sparse matrix--vector product and inner products.  Reuse
\(a_t\widehat z_s\) if its tested relative residual is at most \(\eta\), and
otherwise perform a new quantum solve/tomography.

Assume that, within every checkpoint interval,

\[
 \|M_tM_j^{-1}\|\leq G.
\tag{3}
\]

Then the number \(R\) of quantum refreshes satisfies

\[
 \boxed{
 R\leq1+\frac{2GV_{\rm proj}}{\eta}
 }
\tag{4}
\]

when \(\epsilon\leq\eta/(2G)\), up to constant factors for imperfect residual
tests.

### Proof

The least-squares scalar in (2) is no worse than the candidate \(a=q_t/q_s\).
Propagating the checkpoint error and telescoping the normalized solution ray
give

\[
 \frac{\|H_t(a\widehat z_s-z_t)\|_2}{\|f_t\|_2}
 \leq
 G\left(\epsilon+
 \sum_{j=s}^{t-1}\delta_j\right).
\tag{5}
\]

Therefore a failed residual test consumes at least \(\eta/(2G)\) projective
variation since the preceding checkpoint.  Those intervals are disjoint, which
proves (4).

The theorem is pathwise and allows the systems to depend adaptively on earlier
inexact steps.  It does not multiply a per-solve cost by the full IPM iteration
count.  Moreover,

\[
 \delta_t\leq\kappa(H_{t+1})
 \|\psi_{t+1}-\psi_t\|_2,
\]

so the parameter is bounded by condition-weighted total curvature but can be
strictly smaller because it measures residual-relevant ray motion.

For \(H_t=AD_tA^\top\), every residual test uses \(A^\top\widehat z_s\), the
current diagonal \(D_t\), and \(A\), costing \(O(\operatorname{nnz}A)\)
without forming \(H_t\).

## Precision-independent stable-tail corollary

Suppose a directly assembled scaled system

\[
 M_\mu y_\mu=f_\mu,
 \qquad 0<\mu\leq\mu_0,
\]

satisfies uniform bounds on

\[
 \|M_\mu\|,
 \quad\|M_\mu^{-1}\|,
 \quad\|M_\mu'\|,
 \quad\|f_\mu'\|,
\]

and \(\inf_\mu\|f_\mu\|>0\).  Then \(y_\mu\) and its normalized ray are
\(C^1\) at zero.  Along a monotone path segment,

\[
 V_{\rm proj}=O(\mu_0),
 \qquad G=O(1),
\]

so only

\[
 R=O(1+\mu_0/\eta)
\tag{6}
\]

quantum solves and tomographies are needed over the entire tail, independent of
the final optimization precision and of the
\(\Theta(\sqrt n\log(\mu_0/\epsilon_{\rm opt}))\) outer iteration count.

If derivative bounds are known, a scheduled version needs no residual test.
A checkpoint vector obeys

\[
 \|M_\mu\widehat y_s-f_\mu\|
 \leq\epsilon+
 |\mu-\mu_s|
 \left[L_MB(F+\epsilon)+L_f\right],
\]

where \(B\geq\sup\|M_\mu^{-1}\|\) and \(F\geq\sup\|f_\mu\|\).  Refreshing on
the corresponding additive \(\mu\)-grid proves (6) constructively.

## Strict-complementarity normal matrices have a finite projective tail

The preceding corollary assumes a uniformly conditioned scaled system.  The
same precision-independent refresh conclusion in fact holds for the original,
ill-conditioned normal equation.  What is needed is not two-sided conditioning,
but only the one-sided gain in the direction in which an IPM traverses the path.

Let \(Q\) be the orthogonal projector onto a fixed subspace \(U\), put
\(R=I-Q\), and suppose

\[
 H_\mu=\mu^{-1}C_\mu+\mu D_\mu,
 \qquad 0<\mu\leq\mu_0,
 \tag{7}
\]

where

\[
 C_\mu=QC_\mu Q,
 \quad c_-Q\preceq C_\mu\preceq c_+Q,
 \quad D_\mu\succeq0,
 \quad \|D_\mu\|\leq d_+,
 \quad RD_\mu R\succeq d_-R.
 \tag{8}
\]

Assume that \(C_\mu,D_\mu\) extend continuously differentiably to
\([0,\mu_0]\), with bounded derivatives.  Fix a nonzero \(f\in U\), and define

\[
 z_\mu=H_\mu^{-1}f,
 \qquad \psi_\mu=z_\mu/\|z_\mu\|,
 \qquad
 N_\mu=\frac{\|z_\mu\|}{\|f\|}H_\mu.
 \tag{9}
\]

Then there are constants \(B,L,G<\infty\), depending only on the bounds in
(8), their derivative bounds, and \(\mu_0\), such that

\[
 \sup_{0<\mu\leq\mu_0}\|N_\mu\|\leq B,
 \qquad
 \sup_{0<\mu\leq\nu\leq\mu_0}
       \|N_\mu N_\nu^{-1}\|\leq G,
 \qquad
 \sup_{0<\mu\leq\mu_0}\|\psi_\mu'\|\leq L.
 \tag{10}
\]

Consequently, for every decreasing sequence
\(\mu_0\geq\mu_1\geq\cdots\geq\mu_T>0\), including one whose endpoint is
arbitrarily small,

\[
 \begin{split}
 V_{\rm proj}
 &=\sum_{t=0}^{T-1}
   \|N_{\mu_{t+1}}(\psi_{\mu_{t+1}}-\psi_{\mu_t})\| \\
 &\leq B\int_0^{\mu_0}\|\psi_\mu'\|\,d\mu
 \leq BL\mu_0.
 \end{split}
 \tag{11}
\]

In particular, the number of lazy quantum solves and full direction readouts at
fixed relative normal-equation tolerance \(\eta\) is

\[
 \boxed{
 R\leq 1+\frac{2GBL\mu_0}{\eta},
 }
 \tag{12}
\]

independent of both \(T\) and the final optimization precision.

### Proof

Put

\[
 K_\mu=C_\mu+\mu^2D_\mu,
 \qquad w_\mu=K_\mu^{-1}f.
\]

Then \(z_\mu=\mu w_\mu\), so \(\psi_\mu=w_\mu/\|w_\mu\|\), and

\[
 N_\mu=a_\mu K_\mu,
 \qquad a_\mu=\|w_\mu\|/\|f\|.
 \tag{13}
\]

Use \(U\oplus U^\perp\) blocks and write \(D_{KK}=RD_\mu R|_{U^\perp}\).
The equations \(K_\mu w_\mu=f\) give the exact formulas

\[
 \begin{split}
 E_\mu
 &=D_{UU,\mu}
   -D_{UK,\mu}D_{KK,\mu}^{-1}D_{KU,\mu}\succeq0,\\
 S_\mu&=C_{UU,\mu}+\mu^2E_\mu,\\
 w_{U,\mu}&=S_\mu^{-1}f,\\
 w_{K,\mu}&=-D_{KK,\mu}^{-1}D_{KU,\mu}w_{U,\mu}.
 \end{split}
 \tag{14}
\]

The uniform lower bounds on \(C_{UU,\mu}\) and \(D_{KK,\mu}\) make every
factor on the right-hand side bounded.  They also bound \(\|w_\mu\|\) above
and away from zero.  Since all these factors are \(C^1\), (14) proves that
\(w_\mu\), and hence its normalized ray, extend \(C^1\) to \(\mu=0\).
This proves the first and third bounds in (10).

It remains to prove the forward cross-gain bound.  At a parameter \(\nu\), the
block inverse is

\[
 K_\nu^{-1}=
 \begin{pmatrix}
 S_\nu^{-1}&
 -S_\nu^{-1}D_{UK,\nu}D_{KK,\nu}^{-1}\\
 -D_{KK,\nu}^{-1}D_{KU,\nu}S_\nu^{-1}&
 \nu^{-2}D_{KK,\nu}^{-1}+F_\nu
 \end{pmatrix},
 \tag{15}
\]

where

\[
 F_\nu=D_{KK,\nu}^{-1}D_{KU,\nu}S_\nu^{-1}
       D_{UK,\nu}D_{KK,\nu}^{-1}
\]

is uniformly bounded.  All blocks of \(K_\nu^{-1}\) are therefore bounded
except the displayed \(\nu^{-2}\) term.  Every block in the bottom row and
right column of

\[
 K_\mu=
 \begin{pmatrix}
 C_{UU,\mu}+\mu^2D_{UU,\mu}&\mu^2D_{UK,\mu}\\
 \mu^2D_{KU,\mu}&\mu^2D_{KK,\mu}
 \end{pmatrix}
\]

that can multiply this term contains \(\mu^2\).  Hence
\(\|K_\mu K_\nu^{-1}\|=O(1)\) whenever \(0<\mu\leq\nu\), because
\(\mu^2/\nu^2\leq1\).  Finally, (14) bounds
\(a_\mu/a_\nu\), so (13) proves the middle bound in (10).  Equation (11)
follows by the fundamental theorem of calculus, and (12) follows from (4).

The order \(\mu\leq\nu\) is essential.  The reverse product can grow as
\((\nu/\mu)^2\).  Thus the result is tailored to path following toward the
optimum and is stronger than a condition-number estimate in precisely the
direction the lazy policy needs.  The two-dimensional example
\(C=\operatorname{diag}(1,0)\),
\(D=\operatorname{diag}(0,1)\), and \(f=e_1\) is sharp: its solution ray is
constant, its forward gain is one, and its reverse gain is
\((\nu/\mu)^2\).

## QIPM interpretation and complexity

For a standard-form LP on its exact central path,

\[
 Ax=b,
 \qquad A^Ty+s=c,
 \qquad Xs=\mu\mathbf1,
\]

differentiation with respect to \(\log\mu\) gives

\[
 H_\mu\dot y=-b,
 \qquad H_\mu=AS^{-1}XA^T.
 \tag{16}
\]

Let \((B,\bar B)\) be the optimal partition, so the central-path limit has
\(x_B^*>0\) and \(s_{\bar B}^*>0\).  Then

\[
 C_\mu=A_B\operatorname{Diag}(x_B(\mu)^2)A_B^T,
 \qquad
 D_\mu=A_{\bar B}\operatorname{Diag}(s_{\bar B}(\mu)^{-2})A_{\bar B}^T,
 \tag{17}
\]

and (7) is exact.  Moreover,
\(U=\operatorname{range}(A_B)\), and
\(b=A_Bx_B^*\in U\).  Thus (12) applies to the normalized multiplier tangent
whenever \(b\ne0\).

For LP this regularity is automatic, rather than an additional nondegeneracy
assumption.  The logarithmic central path has an analytic extension to
\(\mu=0\), including for degenerate optimal faces.  Hence
\(x_B(\mu)\) and \(s_{\bar B}(\mu)\) are analytic, remain bounded away from
zero, and make (8) and the derivative assumptions hold for every fixed
strictly primal-dual feasible LP with full-row-rank \(A\) and an attained
optimum.  At an exactly centered point, the feasible predictor from
\(\mu\) to \(\sigma\mu\) has the same normal equation up to the harmless
scalar \(1-\sigma\), so the theorem controls its direction ray as well.

Combine this with the directly assembled active-subspace operator

\[
 \widetilde H_\mu=C_\mu+RD_\mu+\mu^2QD_\mu.
 \tag{18}
\]

It is uniformly conditioned and
\(\widetilde H_\mu^{-1}b=\mu^{-1}H_\mu^{-1}b\), so it prepares exactly the
same normalized state.  If its block-encoding normalization is \(\Gamma\), a
conventional QLSA costs
\(\widetilde O(\Gamma\log(1/\epsilon_{\rm QLS}))\) queries per state
preparation.  At fixed residual tolerance one can take
\(\epsilon_{\rm QLS}=\Theta(\eta)\).  If a full \(m\)-coordinate direction is
required, basic copy/sample tomography uses
\(\widetilde O(m/\eta^2)\) state preparations.  With controlled access to the
state-preparation unitary and its inverse, coherent pure-state tomography
improves this to the tight \(\widetilde\Theta(m/\eta)\) unitary-query bound.
Hence the quantum solve/readout work over an arbitrarily long
strict-complementarity tail is, respectively,

\[
 \begin{split}
 C_{\rm copy}
 &=\widetilde O\!\left(
   \left(1+\frac{GBL\mu_0}{\eta}\right)
   \frac{m\Gamma}{\eta^2}
   \log\frac1\eta
 \right),\\
 C_{\rm coherent}
 &=\widetilde O\!\left(
   \left(1+\frac{GBL\mu_0}{\eta}\right)
   \frac{m\Gamma}{\eta}
   \log\frac1\eta
 \right),
 \end{split}
 \tag{19}
\]

with no \(\log(1/\epsilon_{\rm opt})\) factor.  The full QIPM still performs
its usual
\(T=O(\sqrt n\log(\mu_0/\epsilon_{\rm opt}))\) sparse classical updates and
residual tests; for \(H_\mu=AD_\mu A^T\), these cost
\(O(T\operatorname{nnz}A)\).  The gain is that the expensive QLSA and
tomography are no longer charged at all \(T\) iterations.

Even without (18), (11) says that after a forced checkpoint at
\(\mu_*=\Theta(\eta/(GBL))\), no later refresh is necessary.  All quantum
solves can therefore be arranged at \(\mu\geq\mu_*\), where
\(\kappa(H_\mu)=O(\mu_*^{-2})\).  This is polynomial in the fixed direction
tolerance but independent of \(\epsilon_{\rm opt}\).

This is a theorem for the exact central trajectory, and a conditional
complexity theorem for a QIPM whose realized systems satisfy the same
bounded-variation and residual contract.  A standard central-neighborhood
condition alone does not imply it: iterates may oscillate inside the
neighborhood.  A complete feasible-QIPM instantiation must either show that
its predictor-corrector sequence inherits (10), or use an OSS/nullspace
reconstruction so that each reused approximate solve preserves feasibility.
Likewise, a normal-equation tolerance that shrinks with \(\mu\) can restore a
precision-dependent refresh count.

The constant-sparse expander LP in
`stable-active-subspace-qipm.md` realizes (7)--(8).  It therefore separates
the two notions sharply: its unpreconditioned DLS filtering parameter is
\(\Theta(\mu^{-2})\), while its normalized Newton ray has finite projective
tail variation and its active-subspace encoding has uniform per-refresh cost.

Analyticity is an instance-wise statement.  Its derivative constants, and
therefore \(B,L,G\), can be large as functions of dimension and input bit
length; row and column sparsity alone does not bound them.  Thus (19) is a
genuine improvement in final-precision dependence, not by itself a
strongly-polynomial sparse-LP bound.  A separate structural estimate of
\(B,L,G\) is needed for a uniform family-level speedup.

Classical work proves central-path analyticity, limiting tangents, and curvature
bounds; it also reuses factorizations, inverse data structures, preconditioners,
and Krylov subspaces across changing Newton systems.  Those are established
inputs and neighboring techniques, not novelty claims here.  Searches through
2026-09-02 found neither the directed one-sided cross-gain theorem (10), the
residual-weighted projective-tail bound (11), nor their use to bound the number of
QLSA and full classical-readout calls as in (19).

Relevant classical regularity references are:

- M. Halická, [Two simple proofs for analyticity of the central path in
  linear programming](https://doi.org/10.1016/S0167-6377(00)00065-1),
  *Operations Research Letters* 28(1):9--19, 2001.
- R. D. C. Monteiro and T. Tsuchiya,
  [Limiting behavior of the derivatives of certain trajectories associated
  with a monotone horizontal linear complementarity
  problem](https://doi.org/10.1287/moor.21.4.793), *Mathematics of Operations
  Research* 21(4):793--814, 1996.
- P. Armand and J. Benoist,
  [A local convergence property of primal-dual methods for nonlinear
  programming](https://doi.org/10.1007/s10107-007-0136-2), *Mathematical
  Programming* 115:199--222, 2008.  Under their local assumptions, exact-Newton
  iterates become asymptotically tangent to the central trajectory when the
  perturbation parameters do not converge quadratically; later work extends the
  property to inexact solves.  This tracks iterates relative to the central path,
  but does not reuse an old linear-system solution or count residual-certified
  refreshes.
- R. D. C. Monteiro and T. Tsuchiya,
  [A strong bound on the integral of the central path curvature and its
  relationship with the iteration complexity of primal-dual path-following LP
  algorithms](https://optimization-online.org/2005/09/1221/), *Mathematical
  Programming* 115:105--149, 2008.  This gives a scaling-invariant bound on an
  improper curvature integral and geometrically justifies long nearly straight
  path portions.  Its curvature is not the destination-operator-weighted
  multiplier-ray variation in (1), and it has no checkpoint residual or quantum
  readout count.
- J. A. De Loera, B. Sturmfels, and C. Vinzant,
  [The central curve in linear
  programming](https://arxiv.org/abs/1012.3978), 2010.  This work gives
  instance-specific total-curvature bounds, but does not study normalized
  Newton-solution rays, one-sided residual gain, or quantum refresh counts.

The closest algorithmic comparators are:

- M. Parks, E. de Sturler, G. Mackey, D. Johnson, and S. Maiti,
  [Recycling Krylov subspaces for sequences of linear
  systems](https://doi.org/10.1137/040607277), *SIAM Journal on Scientific
  Computing* 28(5):1651--1674, 2006.  GCRO-DR recycles selected subspaces when
  both matrix and right-hand side change, and minimizes the current residual over
  an augmented Krylov space.  It does not skip solves until a residual failure or
  bound refreshes by total solution-ray variation.
- Y. T. Lee and A. Sidford,
  [Efficient inverse maintenance and faster algorithms for linear
  programming](https://arxiv.org/abs/1503.01752), and S. Jiang et al.,
  [Faster dynamic matrix inverse for faster
  LPs](https://arxiv.org/abs/2004.07470).  These maintain inverse information
  under stable diagonal or low-rank changes and still perform maintenance/query
  work each IPM round; their amortization parameter is update stability or rank,
  not normalized solution-ray variation.
- S. Karim and E. Solomonik,
  [Efficient preconditioners for interior point methods via a new Schur
  complement-based strategy](https://arxiv.org/abs/2104.12916).  Their reduced
  formulation reuses a fixed KKT factorization across all IPM iterations and
  improves CG spectra.  It still solves the changing reduced system each round
  and does not imply (4) or (10).
- J. Gondzio and F. Sobral,
  [Polynomial worst-case iteration complexity of quasi-Newton primal-dual
  interior point algorithms for linear
  programming](https://arxiv.org/abs/2208.08771).  Low-rank quasi-Newton updates
  reduce refactorizations but compute a direction each iteration.  Classical LP
  reoptimization/warm-start results instead concern a sequence of perturbed
  problem instances.
- E. Yildirim and S. Wright,
  [Warm-start strategies in interior-point methods for linear
  programming](https://doi.org/10.1137/S1052623400369235), and J. Gondzio and
  A. Grothey,
  [Reoptimization with the primal-dual interior point
  method](https://doi.org/10.1137/S1052623401393141).  They construct starts for
  perturbed LPs and, under suitable perturbations, can absorb the change in one
  Newton step.  Their object is cross-instance reoptimization, not reuse of a
  scalar-rescaled direction along one fixed instance's central tail.
- S. Boixo, E. Knill, and R. Somma,
  [Fast quantum algorithms for traversing paths of
  eigenstates](https://arxiv.org/abs/1005.3034).  Its complexity depends on an
  eigenpath's angular length and spectral gap.  It coherently transports one
  state along a gapped Hamiltonian path, rather than caching a classical vector,
  screening it by the current linear-system residual, and amortizing full
  tomography.
- J. Kim, N.-H. Chia, and A. Kyrillidis,
  [A catalyst framework for the quantum linear system problem via the proximal
  point algorithm](https://doi.org/10.1609/aaai.v40i27.39418), AAAI 2026.  This is a
  theorem-level QLS warm start: a classical approximation accelerates one SPD
  solve through a regularized auxiliary system.  It does not analyze an external
  sequence of changing systems or give a residual-certified refresh count.
- C. Sanavio et al.,
  [Variational-adiabatic quantum solver for systems of linear equations with
  warm starts](https://arxiv.org/abs/2505.24285).  It warm-starts variational
  parameters along an interpolation and is numerical, not a query-complexity or
  tomography-amortization theorem.
- R. Somma and Y. Subasi,
  [Complexity of quantum state verification in the quantum linear systems
  problem](https://arxiv.org/abs/2007.15698).  Quantum-only verification of a
  candidate solution state needs \(\Omega(\kappa)\) right-hand-side-oracle calls
  in the worst case, or \(\Omega(\kappa^2)\) copies for prepare-and-measure
  verification.  The policy here does not evade that bound quantumly: tomography
  first produces a classical vector, after which the current sparse residual is
  evaluated classically.
- J. van Apeldoorn, A. Cornelissen, A. Gilyen, and G. Nannicini,
  [Quantum tomography using state-preparation
  unitaries](https://arxiv.org/abs/2207.08800), for the tight
  \(\widetilde\Theta(m/\eta)\) coherent-unitary and
  \(\widetilde\Theta(m/\eta^2)\) copy-based \(\ell_2\) tomography scalings used
  in (19).

Existing QLSA-based QIPMs reconstruct a Newton direction at each IPM iteration,
and quantum iterative refinement uses a logarithmic number of fixed-precision
QLSA/tomography corrections to solve one system accurately.  The statement here
is narrower: for a hybrid QLSA plus classical-direction-readout pipeline, the
**number of expensive refreshes** on the exact LP central tail is independent of
final optimization precision at fixed direction tolerance.  It is not a claim
about the Hamiltonian quantum central-path method or quantum LP methods that do not
use this per-iteration QLSA/readout architecture.

## Feasible OSS transfer: exact-path theorem and neighborhood obstruction

The normal-equation result does transfer to the standard orthogonal-subspaces
system (OSS) on the exact LP central path.  More importantly, every approximate
OSS coefficient vector reconstructs an exactly primal-dual feasible direction.
What fails is the final step from the exact central path to every trajectory
allowed by the usual inexact short-step neighborhood.

Let \(V\in\mathbb R^{n\times(n-m)}\) have full column rank and
\(\operatorname{range}V=\ker A\).  At a feasible point, the OSS is

\[
 \mathcal M(x,s)
 \binom{\Delta y}{\lambda}
 :=[-XA^T\ \ SV]
 \binom{\Delta y}{\lambda}
 =\beta\mu e-Xs,
 \tag{20}
\]

with reconstructed direction

\[
 \Delta x=V\lambda,
 \qquad \Delta s=-A^T\Delta y.
 \tag{21}
\]

Equations (21) imply \(A\Delta x=0\) and
\(A^T\Delta y+\Delta s=0\) for every coefficient vector, exact or
approximate.  Thus reuse never sacrifices primal or dual feasibility.

### Theorem: finite projective tail for the exact central OSS

Consider a fixed strictly primal-dual feasible LP with full-row-rank \(A\), an
attained optimum, and nonzero central predictor.  Let
\((x(\mu),y(\mu),s(\mu))\) be its central path, fix
\(\tau=1-\beta>0\), and put

\[
 \mathcal M_\mu=[-X_\mu A^T\ \ S_\mu V],
 \qquad f_\mu=-\tau\mu e,
 \qquad z_\mu=\mathcal M_\mu^{-1}f_\mu.
 \tag{22}
\]

Define \(q_\mu=\|z_\mu\|\),
\(\psi_\mu=z_\mu/q_\mu\), and

\[
 \mathcal N_\mu={q_\mu\over\|f_\mu\|}\mathcal M_\mu.
\]

Then, on a sufficiently small fixed tail \(0<\mu\leq\mu_0\),

\[
 \sup_\mu\|\mathcal N_\mu\|<\infty,
 \qquad
 \sup_{0<\mu\leq\nu\leq\mu_0}
 \|\mathcal N_\mu\mathcal N_\nu^{-1}\|<\infty,
 \qquad
 \int_0^{\mu_0}\|\psi_\mu'\|\,d\mu<\infty.
 \tag{23}
\]

Therefore the lazy-refresh theorem gives a number of exact-central OSS solves
and readouts independent of the final \(\mu\).  Every reused checkpoint
coefficient vector remains exactly feasible through (21).

#### Proof

At the center, \(X_\mu S_\mu=\mu I\), and \(AV=0\).  Consequently the two
OSS column blocks are exactly orthogonal:

\[
 \mathcal M_\mu^T\mathcal M_\mu
 =\begin{pmatrix}
 A X_\mu^2 A^T&0\\
 0&V^T S_\mu^2V
 \end{pmatrix}.
 \tag{24}
\]

Analyticity and strict complementarity imply, for a constant \(c>0\),

\[
 \min_i x_i(\mu)\geq c\mu,
 \qquad
 \min_i s_i(\mu)\geq c\mu.
\]

Since \(A\) has full row rank and \(V\) has full column rank, (24) gives

\[
 \|\mathcal M_\mu^{-1}\|\leq C/\mu.
 \tag{25}
\]

The central path and hence \(\mathcal M_\mu\) are analytic at zero, so
\(\|\mathcal M_\mu-\mathcal M_\nu\|\leq L|\mu-\nu|\).  For
\(0<\mu\leq\nu\),

\[
 \begin{split}
 \|\mathcal M_\mu\mathcal M_\nu^{-1}\|
 &\leq1+
 \|\mathcal M_\mu-\mathcal M_\nu\|
 \|\mathcal M_\nu^{-1}\|\\
 &\leq1+LC{\nu-\mu\over\nu}
 \leq1+LC.
 \end{split}
 \tag{26}
\]

This short one-sided estimate is the OSS analogue of the active-subspace block
argument in (15).

Write the central derivative as
\(x'(\mu)=V\lambda'(\mu)\).  Differentiating centrality gives

\[
 \mathcal M_\mu
 \binom{y'(\mu)}{\lambda'(\mu)}=e.
\]

Thus

\[
 z_\mu=-\tau\mu
 \binom{y'(\mu)}{\lambda'(\mu)}.
 \tag{27}
\]

The vector in (27) is analytic and bounded away from zero at \(\mu=0\): if
its limit vanished, the differentiated equation
\(Sx'+Xs'=e\) would give \(0=e\).  Hence
\(q_\mu=\Theta(\mu)\), the scalar
\(q_\mu/\|f_\mu\|\) is bounded above and below, and \(\psi_\mu\) is an
analytic normalized ray.  Equations (26)--(27) prove (23).

The proof also explains why the OSS condition estimate
\(\kappa(\mathcal M_\mu)=O(1/\mu)\) does not force logarithmically many
refreshes: only the forward product in (26), not the two-sided condition
number, enters the checkpoint analysis.

### A row-3-sparse obstruction for the standard inexact trajectory

The exact-path theorem is not, by itself, a complete feasible-QIPM theorem.
For every \(n\geq4\), consider the row-3-sparse LP

\[
 \min\sum_{j=4}^n x_j
 \quad\text{subject to}\quad
 x_1+x_2+x_3=1,
 \qquad x\geq0.
 \tag{28}
\]

Its optimal face is the two-dimensional simplex in the first three
coordinates.  Fix a short-step factor

\[
 \beta=1-\tau,
 \qquad \tau={a_0\over\sqrt n},
\]

and the three unit, sum-zero vectors

\[
 u_0={1\over\sqrt2}(1,-1,0),\quad
 u_1={1\over\sqrt2}(0,1,-1),\quad
 u_2={1\over\sqrt2}(-1,0,1).
\]

Let \(\mu_t=\beta^t\mu_0\), let \(j=t\bmod3\), and define the feasible
points

\[
 \begin{array}{lll}
 x_{1:3}^{(t)}={1\over3}e+d u_j,&
 x_{4:n}^{(t)}=\mu_t e,&
 y^{(t)}=-3\mu_t,\\
 s_{1:3}^{(t)}=3\mu_t e,&
 s_{4:n}^{(t)}=e.&
 \end{array}
 \tag{29}
\]

Their complementarity average is exactly \(\mu_t\), and

\[
 \|X_ts_t-\mu_t e\|_2=3d\mu_t.
 \tag{30}
\]

Thus all points lie in the standard \(N_2(\theta)\) neighborhood when
\(3d\leq\theta\).

The full feasible step from point \(t\) to point \(t+1\) is

\[
 \begin{split}
 \Delta x_{1:3}&=d(u_{j+1}-u_j),&
 \Delta x_{4:n}&=-\tau\mu_t e,\\
 \Delta y&=3\tau\mu_t,&
 \Delta s_{1:3}&=-3\tau\mu_t e,
 \qquad \Delta s_{4:n}=0,
 \end{split}
 \tag{31}
\]

where the subscript on \(u\) is modulo three.  It preserves both feasibility
equations exactly.  Its OSS/complementarity residual is supported on the first
three coordinates and equals

\[
 r_t=3d\mu_t(u_{j+1}-\tau u_j),
 \qquad
 \|r_t\|_2\leq3d(1+\tau)\mu_t\leq6d\mu_t.
 \tag{32}
\]

Choose

\[
 \eta_n={c_0\over\sqrt n},
 \qquad d={\eta_n\over6},
 \tag{33}
\]

with \(c_0\) a sufficiently small constant.  Then (31) satisfies the
stronger-than-standard contract

\[
 \|r_t\|_2\leq\eta_n\mu_t.
 \tag{34}
\]

Moreover, the OSS right-hand side has the exact norm

\[
 \|\beta\mu_t e-X_ts_t\|_2
 =\mu_t\sqrt{n\tau^2+9d^2}=\Theta(\mu_t),
\]

so (34) is also relative OSS residual \(\Theta(1/\sqrt n)\), independent of
\(\mu_t\).  It is stricter than the published feasible IF-IPM choice
\(\|r_t\|\leq0.1\mu_t\), while the usual
\(\beta=1-0.11/\sqrt n\), \(\theta=0.2\) choices remain valid.

Now choose the fixed sparse nullspace basis

\[
 V=[e_1-e_3,\ e_2-e_3,\ e_4,\ldots,e_n].
\]

At point (29), even the exact OSS centering solution has

\[
 \Delta y_{\rm ex}=3\tau\mu_t,
 \qquad
 (\Delta x_{\rm ex})_{1:3}=-\beta d u_j,
 \qquad
 (\Delta x_{\rm ex})_{4:n}=-\tau\mu_t e.
 \tag{35}
\]

Therefore its normalized coefficient ray converges, according to
\(t\bmod3\), to the three distinct projective lines represented in the first
two \(V\)-coordinates by

\[
 (1,-1),\qquad(0,1),\qquad(-1,0).
 \tag{36}
\]

No choice of sign or scalar identifies these three lines.  The normalized OSS
operator scales as \(\Theta(d/\mu_t)\), while its action on differences of
the limiting rays through the \(SV\) block scales as \(\Theta(\mu_t)\).
For completeness, let \(\ell_j=-(u_{j,1},u_{j,2})\), let \(V_F\) be the
first two columns of \(V\), and put

\[
 h_j=(-\tau e-3d u_j,\,-\tau e_{n-3}).
\]

Along a transition from phase \(j\) to phase \(j+1\), direct substitution in
the definition of \(\delta_t\) gives

\[
 \lim_{\mu_t\downarrow0}{\delta_t\over d}
 ={3\beta\|\ell_{j+1}\|\over\|h_{j+1}\|}
 \left\|V_F\left(
 {\ell_{j+1}\over\|\ell_{j+1}\|}
 -{\ell_j\over\|\ell_j\|}
 \right)\right\|>0.
 \tag{37}
\]

The three positive limits are bounded below uniformly in \(n\) for fixed
\(a_0,c_0\).  Consequently there is a constant \(c>0\) such that, for all
sufficiently large \(t\),

\[
 \delta_t\geq c d,
 \qquad
 \sum_{t<T}\delta_t=\Omega(dT).
 \tag{38}
\]

With \(d=\Theta(1/\sqrt n)\) and the standard
\(T=\Theta(\sqrt n\log(\mu_0/\epsilon_{\rm opt}))\) short-step horizon,
(38) is \(\Omega(\log(\mu_0/\epsilon_{\rm opt}))\).

This is an exact obstruction to deriving a precision-independent refresh count
from feasibility, \(N_2(\theta)\), and a fixed
\(\Theta(1/\sqrt n)\) relative OSS residual alone.  Complementarity residual
of order \(\mu\) can create order-one motion along an optimal face because
the corresponding active slacks are themselves order \(\mu\).  A complete
positive theorem needs an additional rule that suppresses or coherently selects
the face-tangent error.  For example, requiring the active-face tangent
component of the complementarity residual to be \(O(\mu^2)\) makes the induced
face motion \(O(\mu)\) and summable, but this is a stronger, structured
accuracy contract and is not implied by standard IF-IPM analysis.

## Proximal or ray-locked OSS selection: exact tradeoff and no-go theorem

A natural response to the cycling obstruction is to select, among approximate
OSS directions, one close to an old checkpoint. The most direct rule is

\[
 z_\lambda
 =\arg\min_z
 \left\{\|Mz-f\|^2+\lambda\|z-c\|^2\right\},
 \qquad \lambda>0,                                       \tag{39}
\]

where \(c\) is a checkpoint, possibly rescaled for the current iteration.
This section proves two facts.

1. Rule (39) inherits the usual feasible-IPM progress theorem whenever its
   **unregularized OSS residual** passes the usual test.
2. No choice of \(\lambda\) derives face-tangent suppression and a
   precision-independent refresh count from the standard neighborhood and
   residual assumptions alone. The row-three-sparse family (28) remains a
   counterexample.

Thus proximal selection is a useful implementation rule under an additional
ray-admissibility or structured face-tangent assumption, but it does not close
the logical gap identified after (38).

### Exact ridge identities

Let \(M\) be nonsingular, \(z_*=M^{-1}f\), and \(e=c-z_*\). The unique
minimizer of (39) satisfies

\[
 (M^TM+\lambda I)z_\lambda=M^Tf+\lambda c,                \tag{40}
\]

and hence

\[
 z_\lambda-z_*
 =\lambda(M^TM+\lambda I)^{-1}e,                          \tag{41}
\]

\[
 z_\lambda-c
 =-(M^TM+\lambda I)^{-1}M^TM e.                           \tag{42}
\]

If \(v\) is a right singular vector of \(M\) with singular value \(\sigma\),
then, componentwise,

\[
 \langle v,z_\lambda-c\rangle
 =-\frac{\sigma^2}{\sigma^2+\lambda}\langle v,e\rangle,   \tag{43}
\]

while the corresponding residual magnitude is

\[
 \left|\left\langle Mv,{Mz_\lambda-f\over\sigma}\right\rangle\right|
 =\frac{\lambda\sigma}{\sigma^2+\lambda}
  |\langle v,e\rangle|.                                   \tag{44}
\]

Equations (43)--(44) are the exact lock--residual frontier. On a weak OSS
face mode, \(\sigma=\Theta(\mu)\). Making the movement fraction in (43)
\(O(\mu)\), which is needed to turn order-one phase changes into summable
normalized changes when the remaining coefficient vector is \(O(\mu)\),
requires

\[
 \lambda=\Omega(\mu).                                    \tag{45}
\]

But under (45), (44) becomes

\[
 \Theta(\mu|\langle v,e\rangle|).                         \tag{46}
\]

Thus strong ray locking leaves essentially the whole face-tangent
complementarity mismatch in the OSS residual.

Two elementary objective comparisons are also useful:

\[
 \|Mz_\lambda-f\|^2+\lambda\|z_\lambda-c\|^2
 \leq \|Mc-f\|^2,                                        \tag{47}
\]

\[
 \|Mz_\lambda-f\|^2+\lambda\|z_\lambda-c\|^2
 \leq \lambda\|z_*-c\|^2.                                \tag{48}
\]

In particular, if \(c\) already passes the OSS residual test, then
\(z_\lambda\) passes it too. Conversely, (48) only guarantees a target
residual \(\eta\|f\|\) when

\[
 \lambda\leq
 {\eta^2\|f\|^2\over\|z_*-c\|^2}.                        \tag{49}
\]

On a face mode with \(\|f\|=\Theta(\mu)\) and
\(\|z_*-c\|=\Theta(1)\), (49) requires
\(\lambda=O(\eta^2\mu^2)\), the opposite of (45). Objective comparison alone
therefore cannot prove both progress and ray locking.

### What remains valid for a feasible IPM

At a feasible iterate, reconstruct

\[
 \Delta x=V\lambda_z,\qquad \Delta s=-A^T\Delta y
\]

from any coefficient vector \(z=(\Delta y,\lambda_z)\), including
\(z_\lambda\). Primal and dual feasibility are exact. If

\[
 r=Mz_\lambda-f,\qquad \|r\|\leq\eta\mu,                  \tag{50}
\]

then

\[
 S\Delta x+X\Delta s=\beta\mu e-Xs+r.                    \tag{51}
\]

After a full step,

\[
 X^+s^+=\beta\mu e+r+\Delta x\circ\Delta s.               \tag{52}
\]

Consequently every established feasible inexact-IPM neighborhood lemma whose
hypotheses are (50), a bound on the scaled direction, and positivity applies
without change. Proximal regularization neither damages nor improves that
lemma: the residual in (50), not the regularized normal-equation residual in
(40), must be tested. This test remains a sparse multiplication by the
current OSS matrix.

### Sparse no-go theorem

There exist fixed constants \(0<\eta<\theta<1\), within the usual feasible
short-step ranges, for which the following obstruction holds. In the LP (28),
choose a constant
\(d>0\) with

\[
 3d\leq\theta                                             \tag{53}
\]

and sufficiently large relative to \(\eta\). Keep the same three-phase
feasible sequence (29), with \(\tau=a_0/\sqrt n\). It remains in
\(N_2(\theta)\), and its exact OSS face-tangent targets are the three
noncollinear vectors in (35)--(36), of norm \(\Theta(d)\).

On their two-dimensional span, the \(SV\) block has singular values
\(\Theta(\mu_t)\). The rest of the exact OSS coefficient vector has norm
\(O(\mu_t)\). Consider any ridge rule (39), with a checkpoint ray that has
finite total projective variation over the tail and bounded reconstructed
steps, as required by the usual neighborhood proof.

Finite total projective variation makes the checkpoint ray Cauchy. Since the
three exact target rays have a fixed positive separation, on at least one of
every three phases the current checkpoint ray remains a fixed distance from
the exact face target. If the movement fraction in (43) is bounded below on
infinitely many such phases, the ridge output makes a fixed positive
projective move infinitely often, contradicting finite variation. The
movement fraction must therefore tend to zero along an infinite separated
subsequence. Equation (44) then leaves asymptotically the whole face mismatch,
so

\[
 \|M_tz_{\lambda_t}-f_t\|\geq c_1d\mu_t                 \tag{54}
\]

on at least one of every three phases. Here \(c_1>0\) is an absolute constant
coming from the positive projective separation of the three lines in (36).
Meanwhile

\[
 \|f_t\|=\mu_t\sqrt{a_0^2+9d^2}.                         \tag{55}
\]

Choose \(d\) satisfying (53) and

\[
 {c_1d\over\sqrt{a_0^2+9d^2}}>\eta.                      \tag{56}
\]

Such fixed constants exist whenever the residual tolerance is chosen below
the fixed geometric separation allowed by the neighborhood. Equations
(54)--(56) contradict the required relative form of (50).

**No-go conclusion.** Feasibility, membership in a fixed
\(N_2(\theta)\) neighborhood, and the standard fixed relative OSS residual
contract do not imply that any Tikhonov- or ray-locked OSS selector
simultaneously has bounded projective tail variation and produces an
admissible inexact Newton direction.

The argument is independent of how \(\lambda_t\) is selected. Allowing a best
scalar multiple of the checkpoint only quotients out one projective degree of
freedom; the three separated lines remain. The stronger scale
\(\lambda_t=\Omega(\mu_t)\) in (45) is a convenient sufficient choice for
summable geometric-tail movement, but is not needed for this dichotomy.

This no-go theorem concerns what follows from the standard trajectory
contract. A particular proximal algorithm may generate a better trajectory,
but that requires a new dynamical centrality proof. It cannot be inferred from
the existing feasible-IF-IPM analysis.

### The maximal positive condition is an additional residual tube

There is a precise conditional positive statement. Suppose a checkpoint ray
\([c]\) has current best scalar representatives

\[
 a_t=\arg\min_a\|M_t(ac)-f_t\|                            \tag{57}
\]

and, throughout a tail,

\[
 \|M_t(a_tc)-f_t\|\leq\eta_0\|f_t\|,
 \qquad \eta_0<\eta.                                     \tag{58}
\]

Then direct reuse of \(a_tc\) already gives exact primal-dual feasibility and
the standard progress contract. It has zero projective refreshes. By (47),
the proximal solution anchored at \(a_tc\) also satisfies (58), but it cannot
improve the refresh count below zero.

A more structural sufficient condition for (58) is that the strong OSS
component of the rescaled checkpoint differs from the current exact direction
by \(O(\eta\mu)\), while its face-tangent mismatch \(e_F\) obeys

\[
 \|M_t e_F\|=O(\eta\mu).                                  \tag{59}
\]

Since \(M_t|_F=\Theta(\mu)\), condition (59) permits an \(O(\eta)\)
coefficient mismatch but forbids the larger rotating mismatch used in
(54). Requiring \(\|M_te_F\|=O(\mu^2)\) is the summable structured-accuracy
contract already identified after (38). Neither (58) nor (59) follows from
\(N_2(\theta)\) alone.

Hence the largest clean positive theorem is conditional: **once the old ray
stays inside the current OSS residual tube, residual-certified lazy reuse
works and no proximal solve is needed**. A proximal term can select a preferred
point within that tube, but it does not establish that the tube contains a
fixed ray.

### Honest conditioning and access cost

Rule (39) is best represented as the rectangular least-squares system

\[
 B_\lambda=
 \begin{pmatrix}M\\ \sqrt\lambda I\end{pmatrix},
 \qquad
 h_\lambda=
 \binom f{\sqrt\lambda c}.                                \tag{60}
\]

It has

\[
 \kappa_2(B_\lambda)
 =\sqrt{{\sigma_{\max}(M)^2+\lambda\over
              \sigma_{\min}(M)^2+\lambda}},              \tag{61}
\]

whereas explicitly forming the normal matrix in (40) squares this condition
number. On a strict-complementarity OSS tail, the general bounds are
\(\sigma_{\max}(M)=O(1)\) and
\(\sigma_{\min}(M)=\Omega(\mu)\). In the face-tangent setting relevant to the
obstruction, including (28), these are attained:
\(\sigma_{\max}(M)=\Theta(1)\) and
\(\sigma_{\min}(M)=\Theta(\mu)\). Thus, in that worst-case regime:

- \(\lambda=\Theta(\mu)\), the smallest generic scale giving summable weak-mode
  movement, has \(\kappa(B_\lambda)=\Theta(\mu^{-1/2})\);
- \(\lambda=\Theta(1)\) makes the augmented system uniformly conditioned but
  leaves nearly all inadmissible face mismatch in the OSS residual; and
- \(\lambda=O(\eta^2\mu^2)\), the unconditional residual-safe scale from
  (49), retains \(\kappa(B_\lambda)=\Theta(1/\mu)\), up to constants depending
  on \(\eta\), and gives essentially no face locking.

If \(M\) has a sparse or block encoding with normalization \(\alpha_M\), then
\(B_\lambda\) can be encoded using that access plus one identity entry per
row, with normalization \(O(\alpha_M+\sqrt\lambda)\). Its row and column
sparsities increase by at most one in the direct sparse-access model. These
facts do not make the checkpoint term free:

- a state proportional to \(h_\lambda\) must load both the changing \(f\) and
  the classical checkpoint \(c\);
- their norms and the LCU/postselection ratio must be charged;
- a projective penalty
  \(\min_{z,a}\|Mz-f\|^2+\lambda\|z-ac\|^2\) eliminates to a dense rank-one
  projector \(I-cc^T/\|c\|^2\), unless reflection about the checkpoint state
  is supplied; and
- that projective formulation leaves the checkpoint ray unregularized, so its
  worst-case condition number can remain \(\Theta(1/\mu)\).

Finally, solving (60) every IPM iteration would itself restore the full
\(\Theta(\sqrt n\log(1/\epsilon_{\rm opt}))\) solve count. Proximal
regularization is compatible with the residual-certified lazy policy only as
a rule used at a refresh, not as an uncharged per-iteration operation.

### Verdict

The proposed proximal idea does not yield an unconditional feasible-QIPM
finite-refresh theorem. The exact identities (43)--(44) expose the reason:
face-tangent locking and OSS residual accuracy consume the same weak singular
mode in opposite ways. A positive result needs the additional residual-tube
condition (58), the structured face accuracy (59), or a new proof that the
algorithm's own trajectory contracts to such a regime. Under (58), direct
ray reuse is already sufficient.

The residual and neighborhood contract used here is the one analyzed by
Mohammadisiahroudi, Fakhimi, Wu, and Terlaky,
[An Inexact Feasible Interior Point Method for Linear Optimization with High
Adaptability to Quantum Computers](https://doi.org/10.1137/23M1589414),
*SIAM Journal on Optimization* 35 (2025), 2203--2235.  Searches through
2026-09-02 found no prior finite-projective-tail theorem for its OSS and no
optimal-face cycling obstruction of the form (28)--(38).

## Sharp face-leakage geometry and an exact residual repair

The cycling example is governed by two precise residual projections.  This
section isolates them and gives a checkable replacement for a raw residual
norm.

Fix the optimal partition \((B,N)\).  Let \(Z\) have orthonormal columns
spanning \(\ker A_B\), and let \(Y\) have orthonormal columns spanning
\(\ker A_B^T\).  Empty matrices are allowed when the corresponding optimal
face is a point.  Suppose a feasible tail point satisfies

\[
 \underline x\leq x_i\leq\overline x\quad(i\in B),
 \qquad
 \underline s\leq s_i\leq\overline s\quad(i\in N),
 \tag{63}
\]

and

\[
 (1-\theta)\mu\leq x_is_i\leq(1+\theta)\mu
 \quad(1\leq i\leq n).
 \tag{64}
\]

Let \((\Delta x,\Delta y,\Delta s)\) be the exact feasible Newton direction
and let hats denote any inexact feasible OSS direction.  Their error obeys

\[
 A e_x=0,
 \qquad e_s=-A^Te_y,
 \qquad Se_x-XA^Te_y=r,
 \tag{65}
\]

where \(r\) is exactly the OSS residual.  Define

\[
 \begin{split}
 G_p&=Z^TX_B^{-1}S_BZ,&
 g_p(r)&=Z^TX_B^{-1}r_B,\\
 G_d&=Y^TA_NS_N^{-1}X_NA_N^TY,&
 g_d(r)&=Y^TA_NS_N^{-1}r_N.
 \end{split}
 \tag{66}
\]

The dangerous primal and dual face errors are

\[
 p_F(r)=ZG_p^{-1}g_p(r),
 \qquad
 q_F(r)=-YG_d^{-1}g_d(r).
 \tag{67}
\]

More precisely, \(p_F\) is the
\(X_B^{-1}S_B\)-orthogonal projection of \((e_x)_B\) onto
\(\ker A_B\), and \(q_F\) is the
\(A_NS_N^{-1}X_NA_N^T\)-orthogonal projection of \(e_y\) onto
\(\ker A_B^T\).

### Proof of the projection identities

Multiply the \(B\) rows of (65) by \(Z^TX_B^{-1}\).  The dual-error term
vanishes because \(A_BZ=0\), and hence

\[
 Z^TX_B^{-1}S_B(e_x)_B=g_p(r).
\]

This is exactly the normal equation for the first weighted projection in
(67).  For the dual identity, eliminate \(e_x\) from (65) and use
\(Ae_x=0\):

\[
 AS^{-1}XA^Te_y=-AS^{-1}r.
\]

Multiplication by \(Y^T\) annihilates all \(B\)-terms because
\(A_B^TY=0\), leaving, with \(H=AS^{-1}XA^T\),

\[
 Y^THe_y=-g_d(r).
\]

The \(H\)-orthogonal projection onto \(\operatorname{range}Y\) is therefore
\(YG_d^{-1}Y^THe_y=-YG_d^{-1}g_d(r)\).  This proves (67).

The amplification is exactly of order \(1/\mu\).  When the dual-face
subspace is nonempty, put

\[
 \sigma_*:=\sigma_{\min}(A_N^TY)>0,
 \qquad \Sigma_*:=\|A_N^TY\|.
\]

Full row rank of \(A\) makes \(\sigma_*>0\) on
\(\ker A_B^T\).  Equations (63)--(64) give

\[
 {1-\theta\over\overline x^2}\mu I
 \preceq G_p\preceq
 {1+\theta\over\underline x^2}\mu I,
 \tag{68}
\]

and

\[
 {(1-\theta)\sigma_*^2\over\overline s^2}\mu I
 \preceq G_d\preceq
 {(1+\theta)\Sigma_*^2\over\underline s^2}\mu I.
 \tag{69}
\]

Thus, with

\[
 c_p={1-\theta\over\overline x^2},\quad
 C_p={1+\theta\over\underline x^2},\quad
 c_d={(1-\theta)\sigma_*^2\over\overline s^2},\quad
 C_d={(1+\theta)\Sigma_*^2\over\underline s^2},
\]

the following two-sided bounds hold:

\[
 {\|g_p(r)\|\over C_p\mu}
 \leq\|p_F(r)\|\leq
 {\|g_p(r)\|\over c_p\mu},
 \qquad
 {\|g_d(r)\|\over C_d\mu}
 \leq\|q_F(r)\|\leq
 {\|g_d(r)\|\over c_d\mu}.
 \tag{70}
\]

Equation (70) is the sharp local geometry hidden by the usual condition
\(\|r\|=O(\mu)\).

### The face-leakage ledger

Define the directly checkable leakage of step \(t\) by

\[
 \ell_t:=\|p_F(r_t)\|+\|q_F(r_t)\|,
 \qquad
 \Lambda_T:=\sum_{t<T}\ell_t.
 \tag{71}
\]

The residual-induced total variation inside the primal and dual optimal faces
is at most \(\Lambda_T\).  Conversely, (70) shows that an adversary can align
successive errors so that this variation is a constant fraction of
\(\Lambda_T\).  Therefore

\[
 \boxed{
 \sum_t\left(
 {\|g_p(r_t)\|\over\mu_t}
 +{\|g_d(r_t)\|\over\mu_t}
 \right)<\infty
 }
 \tag{72}
\]

is the sharp worst-case amortized residual condition, up to the fixed
constants in (70).  A convenient pointwise sufficient rule is

\[
 \ell_t\leq K(\mu_t-\mu_{t+1}).
 \tag{73}
\]

It gives both

\[
 \sum_{k\geq t}\ell_k\leq K\mu_t
 \quad\text{and}\quad
 \Lambda_\infty\leq K\mu_0.
 \tag{74}
\]

For a geometric short-step schedule, (73) follows from the raw projected
moment bounds

\[
 \|g_p(r_t)\|+\|g_d(r_t)\|
 =O\!\left(\mu_t(\mu_t-\mu_{t+1})\right)
 =O(\tau\mu_t^2).
 \tag{75}
\]

This explains the earlier \(O(\mu^2)\) suggestion.  It is a simple
pointwise sufficient condition, but it is not necessary: for
\(\mu_t=\beta^t\mu_0\), any projected residual
\(O(\mu_t^{1+\gamma})\) with \(\gamma>0\) is summable in (72).  The true
threshold is the ledger, not the exponent two.

For a realized-tail projective theorem, one must also prevent the harmless
complement of the residual from changing its normalized profile arbitrarily.
A checkable sufficient pair of ledgers is

\[
 \Lambda_\infty<\infty,
 \qquad
 W_r:=\sum_t
 \left\|{r_{t+1}\over\mu_{t+1}}-{r_t\over\mu_t}\right\|<\infty,
 \tag{76}
\]

together with the tail version (74).  When repair (78) is used, \(r_t\) in
\(W_r\) means the corrected and retested residual \(r_t^+\).  In any fixed
strict-complementarity
chart in which the exact transverse short-step map is uniformly stable, the
OSS matrix, normalized right-hand side, and solution ray are locally
Lipschitz functions of \(\mu\), the face coordinates, and \(r/\mu\).
Consequently there are chart constants \(K_0,K_1\) such that

\[
 V_{\rm proj}^{\rm realized}
 \leq K_0+K_1(\Lambda_\infty+W_r),
 \tag{77}
\]

and the tail condition (74) keeps the forward cross-gain bounded.  Equation
(77) is deliberately a local stable-chart corollary: (72) controls the
singular face modes exactly, while \(W_r\) rules out ordinary transverse
forcing oscillation.  A norm bound on each \(r_t\) alone controls neither.

### Exact face-leakage repair

The leakage certificate can be enforced after tomography without changing
feasibility.  Given an approximate feasible direction and its residual \(r\),
apply

\[
 \begin{split}
 \widehat{\Delta x}^{+}_B
 &=\widehat{\Delta x}_B-ZG_p^{-1}g_p(r),\\
 \widehat{\Delta y}^{+}
 &=\widehat{\Delta y}+YG_d^{-1}g_d(r),\\
 \widehat{\Delta s}^{+}
 &=\widehat{\Delta s}-A^TYG_d^{-1}g_d(r),
 \end{split}
 \tag{78}
\]

leaving the other primal coordinates unchanged.  The primal correction is
supported on \(B\) and lies in \(\ker A_B\); the dual correction lies in
\(\ker A_B^T\).  Hence (78) preserves primal and dual feasibility.  Direct
substitution shows that the corrected residual \(r^+\) satisfies

\[
 g_p(r^+)=0,
 \qquad g_d(r^+)=0.
 \tag{79}
\]

The two corrections do not interfere: the primal correction changes only the
\(B\) residual, while \(A_B^TY=0\) makes the dual correction change only the
\(N\) residual.  Thus (78) exactly removes the two \(1/\mu\)-amplified modes;
it is not an asymptotic cancellation.

The raw residual remains controlled, although it must be retested after the
repair.  Equations (63)--(70) give a tail constant \(C_{\rm rep}\) such that

\[
 \|r^+\|
 \leq\|r\|+\|S_Bp_F(r)\|
       +\|X_NA_N^Tq_F(r)\|
 \leq C_{\rm rep}\|r\|.
 \tag{80}
\]

Thus one can solve initially with a fixed constant safety margin
\(\eta/C_{\rm rep}\), apply (78), and certify the ordinary
\(\|r^+\|\leq\eta\mu\) progress condition by one current sparse residual
test.

There is a corresponding restricted-inverse bound.  On every fixed tail
satisfying (63)--(64), there is a constant \(C_{\rm reg}\), independent of
\(\mu\), such that an OSS error whose residual satisfies (79) obeys

\[
 \|e_y\|+\|e_\lambda\|
 \leq C_{\rm reg}\|r\|,
 \qquad
 \|e_x\|+\|e_s\|
 \leq C_{\rm reg}(\|V\|+\|A\|)\|r\|.
 \tag{81}
\]

To see this, take \(\mu\downarrow0\).  The kernel of the limiting OSS matrix
consists exactly of two types of vectors: dual coefficients in
\(\ker A_B^T\), and primal nullspace coefficients whose physical vector is
supported on \(B\) and lies in \(\ker A_B\).  Conditions (79), through the
positive limiting matrices \(G_p/\mu\) and \(G_d/\mu\), remove exactly these
two kernel components.  The limiting matrix is injective on the remaining
complement.  Compactness of the unit sphere and continuity in \(\mu\) then
give a uniform smallest singular value on that restricted subspace, proving
(81).  Thus an ordinary \(O(\mu)\) residual causes only \(O(\mu)\) direction
error after leakage repair, instead of an order-one face error.

Algorithmically, (71) can be tested after the ordinary sparse OSS residual is
formed.  It requires solves in \(G_p\) and \(G_d\), whose dimensions are the
primal and dual optimal-face dimensions.  This is attractive when those faces
are low-dimensional or have sparse bases, but it is not free in general:
identifying \((B,N)\), constructing \(Z,Y\), and applying the projected solves
can be dense.  Once strict-complementarity separation is certified, the
partition is fixed for the entire tail.

If the implementation stores \(\lambda\) rather than the physical primal
direction, the first correction in (78) is converted back with the fixed left
inverse of \(V\).  This does not affect feasibility because the embedded
vector supported on \(B\) already lies in \(\ker A=\operatorname{range}V\).

### Sparse sharpness family for the whole ledger

The row-3-sparse LP (28) proves more than failure at constant \(d\).  Replace
the fixed radius in (29) by any sequence \(d_t>0\).  The feasible step from
radius \(d_t\) and phase \(u_j\) to radius \(d_{t+1}\) and phase
\(u_{j+1}\) has the exact residual

\[
 r_t=3\mu_t(d_{t+1}u_{j+1}-\tau d_tu_j).
 \tag{82}
\]

For adjacent radii within a fixed constant factor,

\[
 \ell_t=\Theta(d_t+d_{t+1}).
 \tag{83}
\]

When \(d_t\gg\mu_t\), the exact OSS solution ray is still dominated by the
three distinct face directions, and the direct calculation behind (37) gives

\[
 \delta_t=\Theta(d_t+d_{t+1}).
 \tag{84}
\]

Thus this constant-row-sparse family realizes the ledger threshold itself:
constant \(d_t\) gives logarithmically divergent variation, whereas
\(d_t=\Theta(\mu_t^\gamma)\) gives finite variation for every
\(\gamma>0\).  This proves that replacing (72) by the blanket condition
\(r=O(\mu^2)\) would lose the sharp boundary in (72).

## Scope

- The finite-refresh conclusion needs a fixed relative residual tolerance in
  the scaled equation.  A tolerance shrinking as \(\mu\) generally restores a
  precision-dependent number of refreshes.
- Smoothness must hold for the realized system sequence.  A fixed-radius
  central neighborhood alone permits oscillatory errors.
- An approximate normal-equation direction can violate primal feasibility.
  OSS reconstruction fixes this exactly, but the standard OSS residual
  contract does not control face-tangent oscillation; a complete lazy QIPM
  needs the face-leakage and normalized-forcing controls (72) and (76), or an
  equivalent coherent selection rule.  Repair (78) removes the singular face
  leakage exactly once the optimal partition is available.  The proximal
  identities (43)--(44) show that an ordinary Tikhonov checkpoint penalty does
  not enforce those controls.
- Sparse residual tests are classical work; (4) reduces QLSA and tomography
  calls, not all per-iteration work.

Closest literature includes classical Krylov/subspace recycling, dynamic inverse
maintenance, central-curve curvature, QLS warm starts, inexact feasible IPMs, and
generic quantum eigenpath traversal.  No searched source gives the projective
residual-length refresh bound (4), either ordered one-sided gain theorem (10) or
(23), the fixed-\(\eta\), final-optimization-precision-independent quantum refresh
complexity (19), the sparse cycling obstruction (28)--(38), the exact
face-leakage identities (67)--(70), or repair (78).  Finite smooth
central-path tail variation by itself is not claimed as new; it follows from
established analyticity and limiting-tangent theory.

Status: **proved pathwise amortization, exact-LP normal-tail, and exact-central
feasible-OSS theorems; characterized the sharp \(1/\mu\)-amplified face
residual geometry and an exact leakage repair; proved that neither the
standard fixed-accuracy feasible IF-IPM contract nor an ordinary proximal
checkpoint penalty alone yields a complete precision-independent lazy-QIPM
bound.**
