# Research log: beyond-condition-number QLS on sparse QIPM systems

Date: 2026-09-02

> Draft log. Its verified results have been cleaned, corrected, and superseded by
> **beyond-kappa-coupling-qipm.md**, **stable-active-subspace-qipm.md**, and
> **effective-spectral-dimension-qipm.md**. Use those three notes for theorem
> statements and citations; this file retains the exploratory record only.

## Scope and exclusion set

This continuation deliberately excludes the results already preserved in the other
notes: the QCPM norm/clock correction, inverse-metric densification, feasible-start and
output/query gadgets, support barriers, OSS/QLS liftings, treewidth bounds, the
spectral-sketch candidate, right-hand-side loading bounds, and the earlier observation
that one small sparse witness defeats a solution-norm shortcut.

The new target is a general structural theorem for the 2026
Dalzell--Li--Su (DLS) beyond-condition-number linear-system algorithms.  The theorem
identifies exactly when strict-complementarity QIPM normal equations do and do not
benefit from those algorithms.  It is currently under independent proof and
literature audit, so this log separates proved statements from claims that remain to
be checked.

## Setup

Consider the primal--dual pair in standard form
\[
 \min\{c^Tx:Ax=b,\ x\geq0\},\qquad A^Ty+s=c,\quad s\geq0,
\]
where (A\in\mathbb R^{m\times n}) has full row rank.  Assume the exact central path
converges to a strictly complementary solution.  Write
\[
 B=\{i:x_i^*>0\},\quad N=\{i:s_i^*>0\},\quad
 U=\operatorname{range}(A_B),\quad K=U^\perp,
\]
and suppose (0<r:=\dim U<m).  The primal normal matrix is
\[
 H_\mu=AXS^{-1}A^T=\mu^{-1}C_\mu+\mu D_\mu,
\]
with
\[
 C_\mu=A_BX_B^2A_B^T\to C_0,
 \qquad D_\mu=A_NS_N^{-2}A_N^T\to D_0.
\]
In the orthogonal decomposition (U\oplus K), write
\[
 D_\mu=\begin{pmatrix}D^U_\mu&F_\mu^T\\F_\mu&E_\mu\end{pmatrix}.
\]
The restrictions (C=C_0|_U\) and (E=E_0|_K\) are positive definite.  Exact feasible
centering at (Xs=\mu e) has right-hand side
\[
 H_\mu\Delta y=(1-\sigma_\mu)b,
\]
where the nonzero scalar (1-\sigma_\mu) cancels from all normalized QLS parameters.

For a block encoding of (H_\mu\) with normalization
\(\alpha_{\rm BE}\geq\lVert H_\mu\rVert\), define
\[
 \nu_\mu=\alpha_{\rm BE}
   \frac{\lVert H_\mu^{-1}b\rVert}{\lVert b\rVert},
 \qquad
 \rho_\mu=\alpha_{\rm BE}
   \frac{\lVert H_\mu^{-2}b\rVert}{\lVert H_\mu^{-1}b\rVert}.
\]
The second quantity, not the first, is the inverse-action parameter in the DLS
filtering solver.  For a spectrally tight encoding,
\(\alpha_{\rm BE}=\Theta(\lVert H_\mu\rVert)=\Theta(\mu^{-1})\).

## Proved candidate theorem: the second-inverse barrier

Define the Schur complement and response vectors
\[
 R_\mu=D^U_\mu-F_\mu^TE_\mu^{-1}F_\mu,
 \qquad
 p_\mu=(C_\mu|_U+\mu^2R_\mu)^{-1}b,
 \qquad
 g_\mu=E_\mu^{-1}F_\mu p_\mu.
\]
Then block elimination gives the exact identity
\[
 H_\mu^{-1}b=\mu\binom{p_\mu}{-g_\mu}.
\]
If
\[
 q_\mu=(C_\mu|_U+\mu^2R_\mu)^{-1}
       (p_\mu+F_\mu^TE_\mu^{-1}g_\mu),
\]
a second elimination gives
\[
 H_\mu^{-2}b=
 \binom{\mu^2q_\mu}
 {-E_\mu^{-1}g_\mu-\mu^2E_\mu^{-1}F_\mu q_\mu}.
\]
These formulas require only (C_\mu=C_0+o(1)) and (D_\mu=D_0+o(1)), not a
power-series expansion of the central path.  Moreover (p_\mu\to p=C^{-1}b\neq0),
and the limit of (q_\mu) is nonzero because
\[
 p^T(p+F^TE^{-2}Fp)=\lVert p\rVert^2+\lVert E^{-1}Fp\rVert^2>0.
\]
Consequently
\[
 \lVert H_\mu^{-1}b\rVert=\Theta(\mu),\qquad
 \lVert H_\mu^{-2}b\rVert=\Theta(\lVert g_\mu\rVert+\mu^2),
\]
and the sharp law is
\[
 \boxed{\rho_\mu=
 \Theta\!\left(1+\frac{\lVert g_\mu\rVert}{\mu^2}\right)}
 \quad\text{for a tight block encoding.}
\]
At the same time, (\nu_\mu=\Theta(1)\).  Thus the bounded first-inverse norm that
looks favorable for exact centering does not control the DLS filtering cost.

Let
\[
 g=E^{-1}FC^{-1}b.
\]
If (g\neq0), then
\[
 \rho_\mu=\Theta(\mu^{-2})=\Theta(\kappa(H_\mu)).
\]
The generic obstruction is therefore the active-to-inactive coupling condition
\[
 \Pi_KD_0(C|_U)^{-1}b\neq0.
\]
The exceptional limiting right-hand sides are exactly (b\in C(\ker F)\).  The
obstruction vanishes for every (b\in U) exactly when (F=0), equivalently when
the inactive metric (D_0) reduces (U\oplus K).

If (g=0), no universal improved power follows from strict complementarity alone:
\[
 \rho_\mu=\Theta\!\left(1+\frac{\lVert g_\mu\rVert}{\mu^2}\right)
             =o(\mu^{-2}).
\]
It is bounded exactly when (g_\mu=O(\mu^2)).  Exact finite-μ decoupling
(F_\mu\equiv0) gives (\rho_\mu=\Theta(1)), whereas intermediate vanishing rates
give every intermediate power.  For a non-tight encoding the right formula is
\[
 \rho_\mu=\Theta\!\left[
 \alpha_{\rm BE}\left(\mu+\frac{\lVert g_\mu\rVert}{\mu}\right)
 \right].
\]

## Spectral form and solver-selection phase diagram

Let (P_s(\mu)) project onto the (m-r) eigenvalues of (H_\mu) of order
\(\Theta(\mu)\), let (z=H_\mu^{-1}f), and set
\[
 p_s=\frac{\lVert P_sz\rVert^2}{\lVert z\rVert^2},\qquad
 \beta_{\rm BE}=\frac{\alpha_{\rm BE}}{\lVert H_\mu\rVert}.
\]
Fixed-instance spectral separation gives
\[
 \rho_{\rm BE}
 =\Theta\!\left(
  \beta_{\rm BE}\sqrt{(1-p_s)+\mu^{-4}p_s}
 \right).
\]
Hence filtering improves on (\mu^{-2}) exactly when (p_s=o(1)), and it has
bounded ideal conditioning only when (p_s=O(\mu^4)) and
\(\beta_{\rm BE}=O(1)\).  In the generic exact-centering case (g\neq0), the
small-cluster mass tends to the positive constant
\[
 \frac{\lVert g\rVert^2}{\lVert p\rVert^2+\lVert g\rVert^2},
\]
so filtering pays the full (\Theta(\beta_{\rm BE}\mu^{-2})\).

If (q_s=\lVert P_sf\rVert/\lVert f\rVert\) and the large-cluster part of (f) is
bounded below, then
\[
 p_s=\Theta\!\left(\frac{q_s^2}{\mu^4+q_s^2}\right).
\]
This yields a three-regime solver-selection rule:

1. (q_s=\Theta(\mu^2)): the solution has constant slow-cluster mass, so both
   fixed-accuracy truncation and filtering retain the full (\mu^{-2}) scale.
2. (q_s=o(\mu^2)): the slow solution mass vanishes, so a fixed-accuracy truncation
   solver can eventually discard the slow cluster, but filtering may still diverge.
3. (q_s=O(\mu^4)): filtering also has bounded ideal conditioning (subject to tight
   block encoding).

For exact centering,
\[
 P_s(\mu)b=-\mu^2D_{0,KU}C^{-1}b+o(\mu^2)
\]
in its leading (K)-component.  Thus generic active/inactive coupling puts exact
centering precisely at the saturated boundary (q_s=\Theta(\mu^2)).  This spectral
claim and its connection to the precise DLS truncation error definition still require
a source-level audit before being promoted to the final theorem.

## Constant-sparse sharpness witnesses

The coupled LP
\[
 \min x_2+x_3\quad\text{s.t.}\quad
 \begin{pmatrix}1&1&0\\0&1&-1\end{pmatrix}x=\binom10,
 \quad x\geq0
\]
has row and column sparsity at most two, unique strictly complementary optimum
(x^*=e_1,s^*=(0,1,1)), and central path (x=(1-t,t,t)), where
\[
 t=\frac{2+3\mu-\sqrt{4-4\mu+9\mu^2}}4=\mu+O(\mu^2).
\]
With (\theta_1=(1-t)^2/\mu\) and (\theta=t^2/\mu\),
\[
 H_\mu=\begin{pmatrix}\theta_1+\theta&\theta\\\theta&2\theta\end{pmatrix},
 \qquad \kappa(H_\mu)\sim\frac1{2\mu^2}.
\]
Here (C=1,E=2,F=1,p=1,g=1/2), and
\[
 H_\mu^{-1}b=\frac{(2,-1)^T}{2\theta_1+\theta},
 \qquad H_\mu^{-2}b\to(0,-1/4)^T.
\]
For (\alpha_{\rm BE}=\lVert H_\mu\rVert),
\[
 \nu_\mu\to\frac{\sqrt5}{2},
 \qquad \mu^2\rho_\mu\to\frac1{2\sqrt5}.
\]

The decoupled LP
\[
 \min x_2+x_3\quad\text{s.t.}\quad
 \begin{pmatrix}1&0&0\\0&1&-1\end{pmatrix}x=\binom10,
 \quad x\geq0
\]
has the same optimum and sparsity, but
\[
 H_\mu=\operatorname{diag}(\mu^{-1},2\mu),
 \qquad \kappa(H_\mu)=\frac1{2\mu^2},
 \qquad \nu_\mu=\rho_\mu=1.
\]
These examples show that condition number and first-inverse norm alone cannot choose
the faster QLS method; active/inactive coupling can.

## Algorithmic caution and possible positive direction

Solving only the active Galerkin block
\(μ H_{UU}=C_{UU}+\mu^2D_{UU}\) is asymptotically well conditioned.  At an exact
center, setting the (K)-multiplier component to zero leaves a normal-equation residual
of order (O(\mu^2)\).  This suggests an inexact-infeasible active-subspace QIPM, but it
is not yet an end-to-end algorithm: one must control residual accumulation and charge
construction of a basis for (U=\operatorname{range}(A_B)\), which may be dense and
ill-conditioned.  Classical active-block CG is also well conditioned.

Any complexity corollary must separately charge the block-normalization overhead
\(\beta_{\rm BE}\), RHS preparation, norm estimation, DLS filtering's
(1/\epsilon_{\rm QLS}\) dependence, tomography or classical iterate materialization,
and the cost of identifying/encoding the active subspace.

## Proved oracle lower bound at an exact center

The preceding fixed (2\times3) LP cannot imply oracle hardness because its complete
matrix is readable in constant time.  The following dimension-dependent family closes
that gap without falling back to the earlier generic OSS lifting.

Fix an integer (K=2^r\ge2), put
\[
 \mu=K^{-2},\qquad N=K^8=\mu^{-4},\qquad
 h=1+(1-\mu)^2,
\]
and hide a unique marked row (j\in[N]).  Define
\(A_j\in\mathbb R^{N\times2N}\) by giving row (i) support only on columns
\((2i-1,2i)\), with values
\[
 (A_{i,2i-1},A_{i,2i})=
 \begin{cases}
   (\mu/2,\mu/2),&i=j,\\
   (1,\mu-1),&i\ne j.
 \end{cases}
\]
Every row sums to (\mu); row sparsity is two, column sparsity is one, all entries
have magnitude at most one, and the disjoint nonzero rows give full row rank.  Let
\[
 b=\mu^{3/2}e_N,\qquad c=\sqrt\mu e_{2N}.
\]
The LP
\[
 \min\{c^Tx:A_jx=b,\ x\ge0\}
\]
is strictly primal--dual feasible and has a finite attained optimum.  Indeed
\[
 x^0=s^0=\sqrt\mu e,\qquad y^0=0
\]
is feasible and obeys (X^0S^0e=\mu e), so it is the exact μ-center.  Its normal
matrix is
\[
 H_j=A_jA_j^T
 =\operatorname{diag}(h,\ldots,h,\underbrace{\mu^2/2}_{j},h,\ldots,h),
\]
and therefore
\[
 \lVert H_j\rVert=h,\qquad
 \kappa(H_j)=\frac{2h}{\mu^2}=\Theta(\mu^{-2}).
\]

For any (0\le\sigma<1), eliminating the exact feasible
centering equations at this center gives
\[
 H_j\Delta y=f,\qquad
 f=(1-\sigma)\mu A_j(S^0)^{-1}e
   =(1-\sigma)\mu^{3/2}e_N.
\]
Thus both the center and the normalized RHS — the uniform state — are independent of
the marked row.  The exact multiplier direction is
\[
 \Delta y_i=
 \begin{cases}
  (1-\sigma)\mu^{3/2}/h,&i\ne j,\\
  2(1-\sigma)\mu^{-1/2},&i=j.
 \end{cases}
\]
Its marked-coordinate probability is
\[
 p_j=\frac4{4+(1-\mu^4)/h^2}\ge\frac45.
\]

In the standard sparse-entry oracle model, each query to (A_j), (H_j), or the
canonical diagonal block encoding of (H_j/h) is simulated with (O(1)) queries to a
unique-search oracle for (j).  The positions of all nonzeros are fixed, and one mark
query selects between two known coefficient pairs.  Conversely, measuring any output
state within trace distance (1/10) of the normalized multiplier direction finds
(j) with probability at least (7/10).  Grover's lower bound therefore proves
\[
 \boxed{Q=\Omega(\sqrt N)=\Omega(\mu^{-2})=\Omega(\kappa(H_j))}
\]
queries for constant-error preparation of this exact-centering multiplier state, even
when the exact center and uniform RHS preparation are free.

This can be made an ordinary short step rather than merely a formal centering solve.
Choose
\[
 \gamma:=1-\sigma=\mu^2/4=\Theta(N^{-1/2}).
\]
For the reconstructed direction
\(Delta s=-A_j^T\Delta y\) and
\(Delta x=-\gamma\sqrt\mu e+A_j^T\Delta y\), primal and dual feasibility remain
exact.  On the marked row, (\Delta x=0\) and
\(Delta s=-\gamma\sqrt\mu,-\gamma\sqrt\mu)\).  On an unmarked coordinate with
coefficient (q\in\{1,\mu-1\}\),
\[
 \Delta x=\gamma\sqrt\mu(-1+q\mu/h),\qquad
 \Delta s=-\gamma q\mu^{3/2}/h.
\]
For \(\mu\le1/4\) the endpoint is positive, and each second-order product error is at
most \((1+\mu)\gamma^2\mu^2\).  Hence
\[
 \frac{\lVert X^+S^+e-\sigma\mu e\rVert_2}{\sigma\mu}
 \le \frac{\sqrt2(1+\mu)\gamma^2}{\sigma\mu}=O(\mu^3).
\]
The exact-center query lower bound therefore occurs in a feasible, positivity-
preserving short step whose endpoint lies deep in every fixed Euclidean central
neighborhood.

This is a QIPM-native specialization rather than a new generic QLS lower bound.
Orsucci--Dunjko (2021, Proposition 7) already prove the marked-diagonal QLS lower-bound
core.  The new conjunction here is its realization as ordinary normal equations at an
exact QIPM center, with a fixed/free RHS and center, bounded row-two/column-one original
data, a valid feasible short step, and a misleadingly bounded first-inverse measure.
Indeed, for \(\bar H=H_j/h\) and normalized \(f\),
\[
 \nu^2=\lVert\bar H^{-1}|f\rangle\rVert^2
       =4h^2+1-\mu^4=\Theta(1),
\]
whereas
\[
 \rho_{\rm DLS}
 =\lVert\bar H^{-1}|\Delta y\rangle\rVert
 =\Theta(\mu^{-2}).
\]
The solution places at least \(4/5\) probability on the smallest eigenspace, so for
any fixed DLS truncation accuracy below that mass threshold,
\[
 \kappa_{\rm eff}=\kappa(H_j)=\Theta(\mu^{-2}).
\]
The lower bound is for the normalized multiplier state in the original, unscaled dual
coordinates and in the stated source-oracle model.  It is not a lower bound for the LP
objective, the primal/slack direction, or every equivalent constraint formulation.
Indeed row equilibration \(R=\operatorname{diag}(1/\lVert A_i\rVert)\) turns
\(RH_jR\) into the identity; the scaled multiplier state no longer reveals the mark,
while reconstructing the original multiplier state reintroduces the search cost.
A free preconditioner, QRAM, or affine oracle that already identifies \(j\) is a
strictly stronger input.  Li's sparse affine construction does not contradict the
bound because adjoining the uniform RHS creates a dense \(N\)-sparse column and restores
the \(\Theta(\sqrt N)\) cost.

Nor is constant multiplier-state accuracy necessary for every inexact IPM.  Dropping
the marked component creates only relative normal-equation residual \(\Theta(\mu^2)\);
with the short-step choice \(1-\sigma=\Theta(\mu^2)\), the induced complementarity
residual is far inside a fixed \(O(\mu)\) neighborhood tolerance.  The theorem therefore
lower-bounds the conventional QLS normalized-state output contract, not the weakest
residual contract sufficient for IPM convergence.  Each \(N\)-instance has a genuine
fixed central path and the displayed point lies on it, but the conditioning becomes
constant farther down that path.  No persistent or sum-over-iterations hardness is
claimed.

## Conditional positive result: stable active-subspace equilibration

There is a matching structural escape from the second-inverse barrier.  Let
\(Q=\Pi_U\), \(R=I-Q\), and
\[
 P_\mu=\mu Q+\mu^{-1}R.
\]
Naively composing encodings of \(P_\mu\) and \(H_\mu\) retains a bad normalization.
Instead assemble their product term by term:
\[
 B_\mu:=P_\mu H_\mu
 =C_\mu+RD_\mu+\mu^2QD_\mu
 =C_\mu+D_\mu-(1-\mu^2)QD_\mu.
\]
In \(U\oplus K\) blocks,
\[
 B_\mu=
 \begin{pmatrix}
 C_\mu|_U+\mu^2D^U_\mu&\mu^2D^{UK}_\mu\\
 D^{KU}_\mu&E_\mu
 \end{pmatrix}.
\]
Its Schur complement is
\[
 C_\mu|_U+\mu^2
 (D^U_\mu-D^{UK}_\mu E_\mu^{-1}D^{KU}_\mu)\succeq cI,
\]
while \(E_\mu\succeq dI\).  Hence
\[
 \lVert B_\mu\rVert+\lVert B_\mu^{-1}\rVert=O(1)
\]
for a fixed strictly complementary instance.  If \(H_\mu x=f\) with \(f\in U\), then
\[
 B_\mu(x/\mu)=f,
\]
so the equilibrated solve has exactly the same normalized solution state.  A direct
LCU block encoding from separate encodings of \(C_\mu,D_\mu,Q\) has normalization
\(\Gamma\le\alpha_C+(2-\mu^2)\alpha_D\), independent of the central parameter when
those component normalizations are bounded.  A conventional optimal QLS solver then
removes the μ-dependent condition factor entirely.

This assembly is also stable to an approximate projector.  If
\(\lVert\widehat Q-Q\rVert\le\delta\), then
\[
 \lVert\widehat B_\mu-B_\mu\rVert\le\delta\lVert D_\mu\rVert,
\]
so \(\delta=O(\epsilon_{\rm lin})\) suffices for \(O(\epsilon_{\rm lin})\) state error;
no μ-dependent projector precision is needed.  By contrast, forming
\(\widehat P_\mu H_\mu\) as an encoded product can amplify projector error by
\(\Theta(\mu^{-2})\).

The result is conditional rather than a blanket sparse-QIPM speedup.  It assumes the
active partition and an efficient encoding of \(Q\).  Constructing
\(Q=A_B(A_B^TA_B)^\dagger A_B^T\) can be dense and costs the nonzero singular-value
condition of \(A_B\); identifying \(B\), forming the split operators, RHS preparation,
and output remain chargeable.  Classical active-set/preconditioning methods are the
essential comparator.  The useful new point is the stable split assembly and exact
normalized-state preservation, not the general idea of active-set preconditioning.

## Novelty status

The algebraic theorem, exact-center short-step construction, and stable equilibration
have survived independent hostile proof audits.  Searches through 2026-09-02 found no
paper applying either 2026 DLS solver to IPM Newton systems or deriving the coupling
law, exceptional subspace, critical truncation transition, or stable split operator.
Classical work already contains active/inactive spectral splitting, RHS-sensitive
conditioning, and active-set preconditioners; the novelty claim is specifically their
translation to the DLS parameters and the directly assembled quantum operator.

The generic marked-diagonal QLS lower-bound core is not new:

- D. Orsucci and V. Dunjko, [On solving classes of positive-definite quantum linear
  systems with quadratically improved runtime in the condition
  number](https://quantum-journal.org/papers/q-2021-11-08-573/), Quantum 5, 573
  (2021), Proposition 7.

The relevant new QLS source is:

- A. M. Dalzell, J. Li, and Y. Su, [Faster quantum linear system solver beyond the
  condition number](https://arxiv.org/abs/2607.07691), 2026.

The final results should therefore be described as apparently new, with the exact
access, output, degeneracy, and one-step qualifications above, rather than as absolute
priority or universal-QIPM claims.
