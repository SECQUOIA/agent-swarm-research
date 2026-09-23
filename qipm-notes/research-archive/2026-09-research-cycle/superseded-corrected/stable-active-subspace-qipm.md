# Stable active-subspace equilibration for sparse QIPM normal equations

Date: 2026-09-02

## Result in one sentence

The usual strict-complementarity normal matrix can make both the condition number and
the 2026 Dalzell--Li--Su (DLS) filtering parameter diverge as
\(\Theta(\mu^{-2})\).  If the active range is accessible, a directly assembled
left-equilibrated operator is uniformly conditioned, exactly preserves the normalized
Newton state, and needs only \(\mu\)-independent projector accuracy.  Multiplying
separately normalized block encodings does not achieve this.

## Theorem

Let \(Q\) be the orthogonal projector onto a subspace \(U\), let \(R=I-Q\), and suppose
\[
 H_\mu=\mu^{-1}C_\mu+\mu D_\mu,\qquad 0<\mu\le1,
\]
where, for constants independent of \(\mu\),
\[
 C_\mu=QC_\mu Q,\qquad
 c_-Q\preceq C_\mu\preceq c_+Q,
\]
and
\[
 D_\mu\succeq0,\qquad
 \lVert D_\mu\rVert\le d_+,\qquad
 RD_\mu R\succeq d_-R.
\]
These are exactly the fixed-instance asymptotics of a strictly complementary,
primal-degenerate LP normal matrix, with
\(U=\operatorname{range}(A_B)\).

Define
\[
 P_\mu=\mu Q+\mu^{-1}R
\]
and assemble the following operator directly:
\[
 \boxed{
 M_\mu
 :=C_\mu+RD_\mu+\mu^2QD_\mu
 =C_\mu+D_\mu-(1-\mu^2)QD_\mu .
 }                                                        \tag{1}
\]
Then:

1. \(M_\mu=P_\mu H_\mu\) exactly.
2. \(\lVert M_\mu\rVert+\lVert M_\mu^{-1}\rVert=O(1)\), uniformly in \(\mu\).
3. If \(f\in U\) and \(x_\mu=H_\mu^{-1}f\), then
   \[
   M_\mu^{-1}f=\mu^{-1}x_\mu.                              \tag{2}
   \]
   Thus the two solves produce exactly the same normalized state, with no recovery
   transform or postselection.
4. If \(C_\mu,D_\mu,Q\) have block encodings with normalizations
   \(\alpha_C,\alpha_D,1\), direct LCU assembly of (1) has normalization
   \[
   \Gamma_\mu\le\alpha_C+(2-\mu^2)\alpha_D.                \tag{3}
   \]
   When the component normalizations are bounded, a conventional optimal QLS solver
   prepares the Newton state with
   \(\widetilde O(\Gamma_\mu\log(1/\epsilon_{\rm QLS}))\) queries and no polynomial
   dependence on the central parameter.
5. The ideal DLS filtering parameter is also \(O(\Gamma_\mu)\), although filtering's
   \(1/\epsilon_{\rm QLS}\) precision dependence makes the conventional uniformly
   conditioned solver preferable.

### Proof

The identity follows from \(RC_\mu=0\):
\[
 P_\mu H_\mu
 =C_\mu+\mu^2QD_\mu+RD_\mu=M_\mu.
\]
In \(U\oplus U^\perp\) blocks,
\[
 M_\mu=
 \begin{pmatrix}
 C_\mu+\mu^2D_{UU}&\mu^2D_{UK}\\
 D_{KU}&D_{KK}
 \end{pmatrix}.                                           \tag{4}
\]
The Schur complement of \(D_{KK}\) is
\[
 G_\mu
 =C_\mu+\mu^2
  (D_{UU}-D_{UK}D_{KK}^{-1}D_{KU}).                       \tag{5}
\]
The parenthesized term is positive semidefinite because \(D_\mu\succeq0\).
Consequently \(G_\mu\succeq c_-I_U\), while
\(D_{KK}\succeq d_-I_{U^\perp}\).  The block-inverse formula bounds every block of
\(M_\mu^{-1}\) using only \(c_-,d_-,d_+\), and
\(\lVert M_\mu\rVert\le c_++2d_+\).

For (2), \(P_\mu f=\mu f\), so
\[
 M_\mu x_\mu=P_\mu H_\mu x_\mu=P_\mu f=\mu f.
\]

## Direct assembly is essential

Suppose \(H/\alpha\) and \(P/\beta\) are encoded separately, with
\(\alpha\ge\lVert H\rVert\) and \(\beta\ge\lVert P\rVert\), and their encodings are
composed.  Put \(x=H^{-1}f\).  The DLS parameter of the composed encoding satisfies
\[
\begin{aligned}
 \rho_{\rm prod}
 &=\alpha\beta
   \frac{\lVert P^{-\dagger}H^{-1}x\rVert}{\lVert x\rVert}\\
 &\ge
 \alpha\frac{\lVert H^{-1}x\rVert}{\lVert x\rVert}
 =\rho_H.                                                  \tag{6}
\end{aligned}
\]
Thus separate composition cannot improve even the RHS-sensitive DLS parameter.
The escape comes from normalization compression in a direct encoding of the
algebraically simplified product.  Here
\[
 \alpha=\Theta(\mu^{-1}),\qquad
 \beta=\Theta(\mu^{-1}),\qquad
 \Gamma_\mu=O(1),
\]
so (1) realizes a \(\Theta(\mu^{-2})\) compression.

This is consistent with known general block-encoding normalization obstructions.  The
apparently new point is their RHS-sensitive DLS specialization and the stable QIPM
split (1), not the generic warning that encoded preconditioner products may lose their
classical benefit.

## A \(\mu\)-independent projector-accuracy firewall

If \(\lVert\widehat Q-Q\rVert\le\delta\), assemble
\[
 \widehat M_\mu
 =C_\mu+D_\mu-(1-\mu^2)\widehat QD_\mu.
\]
Then
\[
 \lVert\widehat M_\mu-M_\mu\rVert\le\delta d_+.
\]
For small constant \(\delta\), the perturbed operator remains uniformly invertible and
\[
 \frac{\lVert\widehat M_\mu^{-1}f-M_\mu^{-1}f\rVert}
      {\lVert M_\mu^{-1}f\rVert}=O(\delta).                \tag{7}
\]
Therefore \(\delta=O(\epsilon_{\rm QLS})\), independent of \(\mu\), suffices.

This stability fails if one forms \(\widehat P_\mu H_\mu\) from the original normal
matrix.  For
\[
 H_\mu=\operatorname{diag}(\mu^{-1},\mu)
\]
and a projector rotated by angle \(\theta\), the \((2,1)\) entry of
\(\widehat P_\mu H_\mu\) is
\[
 (1-\mu^{-2})\sin\theta\cos\theta.
\]
Keeping this product uniformly normalized requires
\(\sin\theta=O(\mu^2)\).  Split assembly thus improves the required projector accuracy
from the central-path scale to the ordinary solver-error scale.

Given a block encoding of \(A_B/\alpha_B\), the range projector \(Q\) can be produced
by QSVT in
\[
 O\!\left(
 \frac{\alpha_B}{\sigma_{\min}^+(A_B)}
 \log(1/\epsilon_{\rm QLS})
 \right)                                                   \tag{8}
\]
queries.  This charges active-basis conditioning, but introduces no polynomial
\(\mu\)-dependence.

## Constant-sparse LP witness

The improvement is realized by an explicit family of standard-form LPs.

Let \(G=(L,R,E)\) be a connected balanced \(d\)-regular bipartite expander on \(m\)
vertices, with constant \(d\) and Laplacian gap bounded below.  Orient every edge from
the left part to the right part and let \(B\) be its signed incidence matrix.  Put
\[
 p=\mathbf1_R,\qquad g=2p-\mathbf1,\qquad
 q=m^{-1/2}\mathbf1.
\]
Then
\[
 B^Tp=\mathbf1_E,\qquad B\mathbf1_E=L_Gp=d\,g.
\]
Fix \(0<\delta<1\), set \(w_i=1+\delta g_i\) and
\(a_i=\sqrt{2/w_i}\), and consider
\[
\begin{aligned}
 \min_{x,u,v\ge0}\quad&
   \sum_{i=1}^m a_i(u_i+v_i)\\
 \text{subject to}\quad&
   Bx+u-v=B\mathbf1_E.                                    \tag{9}
\end{aligned}
\]
Its constraint matrix is \([B,I,-I]\), so row and column sparsity are \(O(d)\).

Strict primal feasibility holds at
\(x=\mathbf1_E,\ u=v=t\mathbf1\) for \(t>0\).  Strict dual feasibility follows from
\(y=-\varepsilon p\) for sufficiently small \(\varepsilon>0\).  The optimum has
\[
 x^*=\mathbf1_E,\qquad u^*=v^*=0,\qquad y^*=0,
\]
\[
 s_x^*=0,\qquad s_u^*=s_v^*=a>0.                          \tag{10}
\]
The active optimal face is bounded: a nonnegative recession vector \(h\) with
\(Bh=0\) must vanish by inspecting a left-vertex row.  Moreover
\(\mathbf1_E\) is its analytic center because \(B^Tp=\mathbf1_E\).  Thus (10) is the
strictly complementary analytic-center limit of the central path.

Along that path the normal matrix is exactly
\[
 H_\mu=\mu^{-1}C_\mu+\mu D_\mu,                            \tag{11}
\]
where
\[
 C_\mu
 =B\operatorname{Diag}(x_e(\mu)^2)B^T\longrightarrow L_G
\]
and
\[
 D_\mu
 =\operatorname{Diag}\!\left(
 \frac1{(a_i-y_i(\mu))^2}
 +\frac1{(a_i+y_i(\mu))^2}
 \right)
 \longrightarrow
 D_0=\operatorname{Diag}(w_i).                            \tag{12}
\]
Here
\[
 U=\operatorname{range}B=\mathbf1^\perp,\qquad
 Q=I-|q\rangle\langle q|.
\]
The expander gap and \(w_i\in[1-\delta,1+\delta]\) verify the theorem's uniform
hypotheses.

For the exact-centering RHS \(f=b=B\mathbf1_E\),
\[
 L_G(Qp)=b,\qquad Qp=g/2.
\]
The limiting active-to-null coupling is nonzero:
\[
 q^TD_0(Qp)=\frac{\delta\sqrt m}{2}
            =\delta\lVert Qp\rVert.                       \tag{13}
\]
The exact block identities then give
\[
 \rho(H_\mu/\lVert H_\mu\rVert,f)=\Theta(\mu^{-2}),        \tag{14}
\]
so the unpreconditioned DLS filtering parameter has the full central-path divergence.

By contrast, the directly assembled operator is
\[
 M_\mu
 =C_\mu+\mu^2D_\mu
 +(1-\mu^2)|q\rangle\langle q|D_\mu.                       \tag{15}
\]
It has uniform singular conditioning and \(O(d)\) block-encoding normalization:
\(C_\mu\) is a bounded-weight degree-\(d\) Laplacian, \(D_\mu\) is diagonal, \(q\) is
the uniform state, and the last term is rank one.  At every \(\mu\),
\[
 M_\mu^{-1}b=\mu^{-1}H_\mu^{-1}b
\]
exactly.

Under coherent access to current central weights and the graph, a conventional QLS
solver therefore prepares the exact normalized Newton state using
\[
 \widetilde O(d\log(1/\epsilon_{\rm QLS}))
\]
queries, independent of \(\mu\).  A classical Krylov solve applies (15) in
\(O(dm)\) time per iteration and produces a full vector in
\(O(dm\log(1/\epsilon_{\rm QLS}))\) time.  The quantum comparison is meaningful only
for state or few-observable output; tomography or classical iterate materialization
restores dimension dependence.

## Scope and novelty

The theorem does not make active-set identification free.  It assumes or charges:

- the active partition and coherent current weights;
- a block encoding of \(A_B\) and its nonzero singular-value condition;
- direct termwise access to \(C_\mu,D_\mu,Q\);
- RHS preparation, norm estimation, and the chosen state/observable output.

Classical active/inactive preconditioners and directly encoded quantum preconditioning
are known. Lapworth--Sünderhauf explicitly show that multiplying separately normalized
block encodings can erase classical preconditioning gains, while Nie--Lai--An show how
algebraic regrouping can restore them for Pauli structure. Searches through 2026-09-02
found no source deriving (1) for QIPM central
normal equations, proving exact normalized-state preservation, obtaining
\(\mu\)-independent projector accuracy through the split, or evaluating the DLS
second-inverse penalty on the expander LP (9).  These narrower claims are apparently
new.

Relevant sources are:

- A. M. Dalzell, J. Li, and Y. Su,
  [Faster quantum linear system solver beyond the condition
  number](https://arxiv.org/abs/2607.07691), 2026.
- L. Lapworth and C. Sünderhauf,
  [Preconditioned block encodings for quantum linear
  systems](https://arxiv.org/abs/2502.20908), 2025.
- H. Nie, Z. Lai, and D. An,
  [Pauli-structured preconditioning for quantum linear system
  solvers](https://arxiv.org/abs/2606.01733), 2026.
- J. Gondzio, S. Pougkakiotis, and J. W. Pearson,
  [General-purpose preconditioning for regularized interior point
  methods](https://link.springer.com/article/10.1007/s10589-022-00424-5),
  Computational Optimization and Applications 83 (2022).
