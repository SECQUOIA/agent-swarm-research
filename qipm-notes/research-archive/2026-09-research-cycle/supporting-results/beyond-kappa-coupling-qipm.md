# Active/inactive coupling controls beyond-\(\kappa\) QLS on QIPM normal equations

Date: 2026-09-02

**Status: historical derivation; corrected by the current paper.** Use the
exact-center coupling subsection of
[`paper/sections/05-beyond-kappa.tex`](../../../paper/sections/05-beyond-kappa.tex)
and the [Lean verification report](../../../formal/COUPLING.md) for current
statements and verified scope. The discussion below of arbitrary intermediate
powers is obsolete for a fixed strictly complementary LP: its central path is
analytic at zero. The coupled example has a unique primal optimum but an
interval of dual optima. Its slow-eigenspace amplitude tends to `1/sqrt(5)`;
only its normalized coordinate vector is constant. The decoupled formulas
`kappa = 1/(2 mu^2)` and `xi = rho = 1` with norm-tight normalization require
`0 < mu <= 1/sqrt(2)`. The historical derivation is preserved below.

## Main theorem

Consider a standard-form LP with full-row-rank \(A\), and assume its exact central
path converges to a strictly complementary solution.  Let
\[
 B=\{i:x_i^*>0\},\qquad N=\{i:s_i^*>0\},
\]
\[
 U=\operatorname{range}(A_B),\qquad K=U^\perp,
\]
and suppose \(0<r:=\dim U<m\).  This is the primal-degenerate mixed regime; under
primal nondegeneracy \(U=\mathbb R^m\), the normal condition stays bounded after
normalization and the phenomenon below does not occur.

The exact central normal matrix is
\[
 H_\mu=AXS^{-1}A^T
      =\mu^{-1}C_\mu+\mu D_\mu,
\]
\[
 C_\mu=A_BX_B^2A_B^T\longrightarrow C_0,\qquad
 D_\mu=A_NS_N^{-2}A_N^T\longrightarrow D_0.
\]
In the orthogonal decomposition \(U\oplus K\), write
\[
 D_\mu=
 \begin{pmatrix}
 D_\mu^U&F_\mu^T\\
 F_\mu&E_\mu
 \end{pmatrix}.
\]
The restrictions \(C=C_0|_U\) and \(E=E_0|_K\) are positive definite.

At an exact \(\mu\)-center, the feasible short-step RHS for target
\(\sigma_\mu\mu\), with \(\sigma_\mu\ne1\), is
\[
 H_\mu\Delta y=(1-\sigma_\mu)b.
\]
The scalar cancels from normalized QLS quantities, so take the RHS to be \(b\).
Define
\[
 R_\mu=D_\mu^U-F_\mu^TE_\mu^{-1}F_\mu,
\]
\[
 p_\mu=(C_\mu|_U+\mu^2R_\mu)^{-1}b,\qquad
 g_\mu=E_\mu^{-1}F_\mu p_\mu.
\]
Exact block elimination gives
\[
 \boxed{
 H_\mu^{-1}b=\mu
 \begin{pmatrix}p_\mu\\-g_\mu\end{pmatrix}.
 }                                                        \tag{1}
\]
If
\[
 q_\mu=(C_\mu|_U+\mu^2R_\mu)^{-1}
       (p_\mu+F_\mu^TE_\mu^{-1}g_\mu),
\]
a second elimination gives
\[
 \boxed{
 H_\mu^{-2}b=
 \begin{pmatrix}
 \mu^2q_\mu\\
 -E_\mu^{-1}g_\mu-\mu^2E_\mu^{-1}F_\mu q_\mu
 \end{pmatrix}.
 }                                                        \tag{2}
\]
These identities use only central-path convergence, not a power-series expansion.
Since \(p_\mu\to p=C^{-1}b\ne0\), and the limit of \(q_\mu\) is nonzero,
\[
 \lVert H_\mu^{-1}b\rVert=\Theta(\mu),\qquad
 \lVert H_\mu^{-2}b\rVert
 =\Theta(\lVert g_\mu\rVert+\mu^2).                       \tag{3}
\]

Let \(H_\mu/\alpha_{\rm BE}\) be the actual block encoding.  The two inverse-action
quantities are
\[
 \nu_\mu
 =\alpha_{\rm BE}
   \frac{\lVert H_\mu^{-1}b\rVert}{\lVert b\rVert},
\qquad
 \rho_\mu
 =\alpha_{\rm BE}
   \frac{\lVert H_\mu^{-2}b\rVert}
        {\lVert H_\mu^{-1}b\rVert}.                       \tag{4}
\]
The second, not the first, is the DLS filtering parameter.  Under a spectrally tight
encoding,
\(\alpha_{\rm BE}=\Theta(\lVert H_\mu\rVert)=\Theta(\mu^{-1})\),
\[
 \boxed{
 \nu_\mu=\Theta(1),\qquad
 \rho_\mu=\Theta\!\left(
 1+\frac{\lVert g_\mu\rVert}{\mu^2}
 \right).
 }                                                        \tag{5}
\]

Define the limiting active-to-inactive response
\[
 g=E^{-1}FC^{-1}b.                                        \tag{6}
\]
If \(g\ne0\), then
\[
 \rho_\mu=\Theta(\mu^{-2})=\Theta(\kappa(H_\mu)).
\]
Equivalently, the obstruction is
\[
 \Pi_KD_0(C|_U)^{-1}b\ne0.                                \tag{7}
\]
The exceptional limiting RHS space is \(C(\ker F)\).  The obstruction vanishes for
every \(b\in U\) exactly when \(F=0\), meaning \(D_0\) reduces \(U\oplus K\).

If \(g=0\), strict complementarity alone gives only
\[
 \rho_\mu
 =\Theta\!\left(1+\frac{\lVert g_\mu\rVert}{\mu^2}\right)
 =o(\mu^{-2}).                                            \tag{8}
\]
Bounded filtering cost requires \(g_\mu=O(\mu^2)\).  Exact finite-\(\mu\) decoupling
\(F_\mu\equiv0\) gives \(\rho_\mu=\Theta(1)\); intermediate coupling rates produce
every intermediate power.

For a non-tight encoding the exact scale is
\[
 \rho_\mu
 =\Theta\!\left[
 \alpha_{\rm BE}
 \left(\mu+\frac{\lVert g_\mu\rVert}{\mu}\right)
 \right].                                                 \tag{9}
\]

## Truncation phase transition

Let \(P_s(\mu)\) project onto the \(m-r\) eigenvalues of \(H_\mu\) of order
\(\Theta(\mu)\), and put \(z_\mu=H_\mu^{-1}b\).  In the generic case \(g\ne0\),
\[
 \frac{\lVert P_sz_\mu\rVert^2}{\lVert z_\mu\rVert^2}
 \longrightarrow
 \frac{\lVert g\rVert^2}
      {\lVert p\rVert^2+\lVert g\rVert^2}>0.               \tag{10}
\]
After normalizing \(H_\mu\), this slow cluster lies at eigenvalue
\(\Theta(\mu^2)\).  Therefore DLS effective truncation has
\[
 \kappa_{\rm eff}=\Theta(\mu^{-2})
\]
for every fixed error below the limiting slow-cluster mass.  For an error above that
mass it can discard the cluster and have \(O(1)\) effective condition.

More generally, if
\[
 q_s=\frac{\lVert P_sf\rVert}{\lVert f\rVert}
\]
and the large-cluster RHS part is bounded below, then
\[
 p_s:=\frac{\lVert P_sH_\mu^{-1}f\rVert^2}
            {\lVert H_\mu^{-1}f\rVert^2}
 =\Theta\!\left(\frac{q_s^2}{\mu^4+q_s^2}\right).          \tag{11}
\]
This separates the two DLS routes:

- \(q_s=\Theta(\mu^2)\): constant slow solution mass; truncation and filtering both
  retain the full \(\mu^{-2}\) scale.
- \(q_s=o(\mu^2)\): fixed-accuracy truncation can eventually discard the slow cluster,
  while filtering may still diverge.
- \(q_s=O(\mu^4)\): filtering also has bounded ideal condition, assuming a tight
  encoding.

Exact centering generically sits at the critical boundary
\(q_s=\Theta(\mu^2)\), because
\[
 P_s(\mu)b=-\mu^2D_{0,KU}C^{-1}b+o(\mu^2)
\]
in its leading \(K\)-component.

## Two constant-sparse sharpness witnesses

The coupled LP
\[
 \min x_2+x_3
\]
subject to
\[
 \begin{pmatrix}1&1&0\\0&1&-1\end{pmatrix}x
 =\begin{pmatrix}1\\0\end{pmatrix},\qquad x\ge0,
\]
has row and column sparsity at most two and the unique strictly complementary optimum
\(x^*=e_1,\ s^*=(0,1,1)\).  Its central point is
\(x=(1-t,t,t)\), where
\[
 t=\frac{2+3\mu-\sqrt{4-4\mu+9\mu^2}}4=\mu+O(\mu^2).
\]
Writing
\[
 \theta_1=\frac{(1-t)^2}{\mu},\qquad
 \theta=\frac{t^2}{\mu},
\]
gives
\[
 H_\mu=
 \begin{pmatrix}\theta_1+\theta&\theta\\
                 \theta&2\theta\end{pmatrix},
\qquad
 \kappa(H_\mu)\sim\frac1{2\mu^2}.
\]
Here \(C=1,E=2,F=1,p=1,g=1/2\), and
\[
 H_\mu^{-1}b=\frac{(2,-1)^T}{2\theta_1+\theta},
\qquad
 H_\mu^{-2}b\longrightarrow(0,-1/4)^T.
\]
For \(\alpha_{\rm BE}=\lVert H_\mu\rVert\),
\[
 \nu_\mu\longrightarrow\frac{\sqrt5}{2},\qquad
 \mu^2\rho_\mu\longrightarrow\frac1{2\sqrt5}.
\]
The normalized solution ray is exactly \((2,-1)/\sqrt5\), so it retains asymptotic
slow-cluster amplitude \(1/\sqrt5\) even though the discarded RHS amplitude is only
\(\Theta(\mu^2)\).

The decoupled LP
\[
 \min x_2+x_3
\]
subject to
\[
 \begin{pmatrix}1&0&0\\0&1&-1\end{pmatrix}x
 =\begin{pmatrix}1\\0\end{pmatrix},\qquad x\ge0,
\]
has the same optimum and sparsity, but
\[
 H_\mu=\operatorname{diag}(\mu^{-1},2\mu),\qquad
 \kappa(H_\mu)=\frac1{2\mu^2},
\qquad
 \nu_\mu=\rho_\mu=1.
\]
Condition number and first-inverse norm therefore cannot distinguish the two cases;
active/inactive coupling can.

## Exact-center oracle specialization

There is also a dimension-dependent exact-center realization of the marked-diagonal
QLS lower bound.  It is useful, but its generic search core is already known from
Orsucci--Dunjko (2021, Proposition 7).

For \(N=\mu^{-4}\), hide \(j\in[N]\).  Let row \(i\) of
\(A_j\in\mathbb R^{N\times2N}\) have fixed support \((2i-1,2i)\) and values
\[
 (\mu/2,\mu/2)\quad(i=j),\qquad
 (1,\mu-1)\quad(i\ne j).
\]
All entries are magnitude at most one and have \(O(\log N)\)-bit rational
descriptions; row sparsity is two and column sparsity one.  With
\[
 b=\mu^{3/2}e_N,\qquad c=\sqrt\mu e_{2N},
\]
\[
 x^0=s^0=\sqrt\mu e,\qquad y^0=0
\]
is the exact \(\mu\)-center.  The normal matrix and exact short-step RHS are
\[
 H_j=A_jA_j^T
 =\operatorname{diag}(h,\ldots,\mu^2/2,\ldots,h),
\qquad h=1+(1-\mu)^2,
\]
\[
 f=(1-\sigma)\mu^{3/2}e_N.
\]
The normalized RHS is free and uniform, while the exact multiplier direction yields
the mark with probability at least \(4/5\).  Under the stated sparse-value oracle, or
the canonical diagonal block encoding reducible to it,
\[
 \Omega(\sqrt N)=\Omega(\mu^{-2})=\Omega(\kappa(H_j))
\]
queries are required to prepare the original normalized multiplier state to constant
trace error.  Yet \(\nu=\Theta(1)\), while
\(\rho_{\rm DLS}=\kappa_{\rm eff}=\Theta(\mu^{-2})\).

Choosing \(1-\sigma=\mu^2/4=\Theta(N^{-1/2})\) gives a positive feasible short step
whose endpoint is deep in a fixed \(2\)-norm neighborhood.  This makes the occurrence
QIPM-native, but not representation invariant:

- row equilibration turns the normal matrix into the identity and makes the scaled
  multiplier state easy;
- the primal/slack direction is invariant under that scaling;
- omitting the marked component gives relative normal residual only
  \(\Theta(\mu^2)\), small enough for ordinary residual-based inexact IPM progress;
- the hardness is therefore for the conventional exact normalized multiplier-state
  contract, not for every QIPM or every equivalent LP representation;
- the hard scale occurs at one point of each fixed instance's central path and does
  not persist as its barrier parameter tends to zero.

## Novelty and prior-art boundary

Classical papers already establish active/inactive spectral splitting, effective
conditioning, structured RHS stability, and active-set preconditioning.  DLS already
define effective condition by solution spectral mass.  The apparently new content is
the exact QIPM specialization: formulas (1)--(9), the coupling cancellation criterion,
the filtering/truncation separation, and the coupled/decoupled sparse witnesses.

Searches through 2026-09-02 found no paper applying the DLS beyond-\(\kappa\) solvers
to an IPM Newton system or deriving this coupling law.  Relevant sources are:

- A. M. Dalzell, J. Li, and Y. Su,
  [Faster quantum linear system solver beyond the condition
  number](https://arxiv.org/abs/2607.07691), 2026.
- D. Orsucci and V. Dunjko,
  [On solving classes of positive-definite quantum linear systems with quadratically
  improved runtime in the condition
  number](https://quantum-journal.org/papers/q-2021-11-08-573/),
  Quantum 5, 573 (2021).
- T. F. Chan and D. E. Foulser,
  [Effectively well-conditioned linear
  systems](https://ww3.math.ucla.edu/camreport/cam87-03.pdf), 1988.
- M. H. Wright,
  [Ill-conditioning and computational error in interior
  methods](https://doi.org/10.1137/S1052623497322279), 1998.

The claims should be described as apparently new rather than as unconditional priority
claims.
