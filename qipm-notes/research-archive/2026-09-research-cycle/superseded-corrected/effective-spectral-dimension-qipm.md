# Effective spectral dimension for beyond-\(\kappa\) QLS in sparse QIPMs

Date: 2026-09-02

## The phase law

Matrix sparsity and condition number do not determine which of the two 2026
Dalzell--Li--Su (DLS) beyond-\(\kappa\) solvers is preferable. A coordinate-invariant
quantity does: the low-energy spectral dimension seen by the RHS. It yields distinct
critical dimensions, four for effective truncation and eight for filtering.

Let \(H\succ0\), \(\lVert H\rVert=1\), and let \(b\) be normalized. Define
\[
 \nu_b(S)=\langle b,\mathbf1_S(H)b\rangle.
\]
Let \(\lambda_*\) be the smallest eigenvalue visible to \(b\), put
\(\kappa_*=\lambda_*^{-1}\), and assume that for every dyadic
\(t\in[\lambda_*,t_0/2]\),
\[
 c\,t^{D/2}\le\nu_b([t,2t))\le C\,t^{D/2},                \tag{1}
\]
with \(\nu_b([t_0,1])=\Theta(1)\). Call \(D\) the effective spectral dimension of
\((H,b)\). This definition is invariant under \((H,b)\mapsto(VHV^T,Vb)\).

For \(p>0\), put \(Z_p=\langle b,H^{-p}b\rangle\). A shell at scale \(t\) contributes
\(\Theta(t^{D/2-p})\), so dyadic summation gives
\[
 Z_p=
 \begin{cases}
  \Theta(\kappa_*^{p-D/2}),&D<2p,\\
  \Theta(\log\kappa_*),&D=2p,\\
  \Theta(1),&D>2p.
 \end{cases}                                               \tag{2}
\]

Let \(x=H^{-1}b\), and let \(\kappa_{\rm eff}(\epsilon)\) be the smallest DLS cutoff
whose discarded subspace contains at most \(\epsilon^2\) of the normalized solution
mass. Applying the same sum with \(p=2\) gives
\[
 \boxed{
 \kappa_{\rm eff}(\epsilon)=
 \begin{cases}
  \Theta(\kappa_*),&D<4,\\
  \kappa_*^{\,1-\Theta(\epsilon^2)},&D=4,\\
  \Theta\!\left(\min\{\kappa_*,\epsilon^{-4/(D-4)}\}\right),&D>4.
 \end{cases}}                                              \tag{3}
\]
At \(D=4\), the exact exponent is \(1-\epsilon^2+o(1)\) when the logarithmic density
has a definite leading coefficient, as in the torus witness below. Under only (1),
\(1-\Theta(\epsilon^2)\) is sharp. When
\(\epsilon^2\log\kappa_*=O(1)\), the expression saturates at
\(\Theta(\kappa_*)\).

The ideal DLS filtering parameter is
\[
 \rho=\left\lVert H^{-1}\frac{x}{\lVert x\rVert}\right\rVert,
\qquad
 \rho^2=\frac{Z_4}{Z_2}.
\]
Equation (2) yields
\[
 \boxed{
 \rho=
 \begin{cases}
  \Theta(\kappa_*),&D<4,\\
  \Theta(\kappa_*/\sqrt{\log\kappa_*}),&D=4,\\
  \Theta(\kappa_*^{(8-D)/4}),&4<D<8,\\
  \Theta(\sqrt{\log\kappa_*}),&D=8,\\
  \Theta(1),&D>8.
 \end{cases}}                                              \tag{4}
\]
Thus truncation becomes mesh-condition-independent above \(D=4\), while filtering
does so only above \(D=8\). Dimensions five through eight give a strict asymptotic
separation. These are exact instance-parameter laws, not universal QLS lower bounds.

## Constant-degree torus witnesses

Let \(T_L^d\) be the periodic \(d\)-dimensional \(L\)-grid and set
\[
 H_{L,d}
 =\frac{L^{-2}I+\Delta_{T_L^d}}{L^{-2}+4d}.                \tag{5}
\]
This matrix is \(2d+1\)-sparse, has norm one, and
\(\kappa(H_{L,d})=1+4dL^2=\Theta(L^2)\). For a localized source \(b=e_0\), Fourier
overlaps are uniform. At low frequency,
\[
 \lambda_k\asymp L^{-2}(1+\lVert k\rVert^2),
\]
so lattice-shell counting proves (1) with \(D=d\). Equivalently,
\[
 \sum_k\lambda_k^{-p}=
 \begin{cases}
  \Theta(L^{2p}),&d<2p,\\
  \Theta(L^{2p}\log L),&d=2p,\\
  \Theta(L^d),&d>2p.
 \end{cases}
\]

For the dipole source \(b=(e_0-e_{e_1})/\sqrt2\), squared Fourier overlap contributes
one extra factor proportional to \(\lambda\) on each low-frequency shell. Hence
\(D=d+2\). The constant mode has zero overlap, but the first source-visible eigenvalue
remains \(\Theta(L^{-2})\).

For conserved dipole sources:

| physical \(d\) | effective \(D\) | \(\kappa_{\rm eff}\) | \(\rho\) |
|---:|---:|---|---|
| 3 | 5 | \(\Theta(\min\{\kappa,\epsilon^{-4}\})\) | \(\Theta(\kappa^{3/4})\) |
| 4 | 6 | \(\Theta(\min\{\kappa,\epsilon^{-2}\})\) | \(\Theta(\kappa^{1/2})\) |
| 5 | 7 | \(\Theta(\min\{\kappa,\epsilon^{-4/3}\})\) | \(\Theta(\kappa^{1/4})\) |
| 6 | 8 | \(\Theta(\min\{\kappa,\epsilon^{-1}\})\) | \(\Theta(\sqrt{\log\kappa})\) |
| \(\ge7\) | \(>8\) | mesh-independent at fixed \(\epsilon\) | mesh-independent |

The same matrix can therefore occupy a different phase when the Newton residual
changes from localized to conserved.

## A positive full-step feasible-QIPM occurrence

Let \(B\) be an oriented incidence matrix of \(T_L^d\), and define
\[
 \mathcal A=[B,I],\qquad
 W=\operatorname{Diag}(I_E,L^{-2}I_V).
\]
Then
\[
 \mathcal A W\mathcal A^T
 =\Delta_{T_L^d}+L^{-2}I.                                 \tag{6}
\]
The original constraint matrix has row sparsity \(2d+1\) and column sparsity at most
two.

For \(d\ge2\), choose two perpendicular torus edges \(f,g\) meeting at a vertex. Fix
\(\tau>0\) and \(0<\delta<1\), retain \(x_i/s_i=w_i\), and choose
\[
 p_i=x_is_i=
 \begin{cases}
  \tau(1+\delta),&i=f,\\
  \tau(1-\delta),&i=g,\\
  \tau,&\text{otherwise}.
 \end{cases}                                               \tag{7}
\]
Set \(x_i=\sqrt{p_iw_i}\), \(s_i=\sqrt{p_i/w_i}\),
\(b_{\rm LP}=\mathcal A x\), \(c=s\), and \(y=0\). This point is exactly primal and
dual feasible, has average complementarity \(\tau\), and satisfies
\[
 \frac{\lVert XSe-\tau e\rVert_2}{\tau}=\sqrt2\,\delta.
\]

For a \(\sigma=1\) feasible centering corrector,
\[
 \mathcal A\Delta x=0,\qquad
 \mathcal A^T\Delta y+\Delta s=0,\qquad
 S\Delta x+X\Delta s=\tau e-XSe.
\]
Elimination gives
\[
 (\mathcal A W\mathcal A^T)\Delta y
 =-\mathcal A S^{-1}(\tau e-XSe),                         \tag{8}
\]
whose normalized RHS is proportional to
\[
 \frac{\mathcal A_f}{\sqrt{1+\delta}}
 -\frac{\mathcal A_g}{\sqrt{1-\delta}}.                   \tag{9}
\]
Its low-frequency Fourier symbol vanishes linearly and has nonzero gradient. Its shell
weight is therefore \(\Theta(t^{(d+2)/2})\), realizing \(D=d+2\).

The complete Newton step is safe. Put
\[
 u=X^{-1}\Delta x,\qquad v=S^{-1}\Delta s,\qquad
 P=\operatorname{Diag}(p).
\]
The equations imply
\[
 P(u+v)=\tau e-p,\qquad
 u^TPv=\Delta x^T\Delta s=0.
\]
Thus \(P^{1/2}u\) and \(P^{1/2}v\) are orthogonal and sum to
\(P^{-1/2}(\tau e-p)\), whose squared norm is
\[
 \frac{2\tau\delta^2}{1-\delta^2}.
\]
For \(\delta\le1/4\), every relative step has magnitude below one, so positivity is
preserved. The new average complementarity remains \(\tau\), and
\[
 \boxed{
 \frac{\lVert X^+S^+e-\tau e\rVert_2}{\tau}
 \le\frac{\delta^2}{1-\delta^2}.
 }                                                        \tag{10}
\]
The full feasible corrector quadratically improves centrality while realizing the
\(D=d+2\) law. It centers but does not reduce the duality gap.

## Localized RHS through an infeasible corrector

The \(D=d\) branch also occurs in a sparse QIPM normal equation. At a chosen
complementarity \(\tau\), set
\[
 x_i=\sqrt{\tau w_i},\qquad
 s_i=\sqrt{\tau/w_i},\qquad
 b_{\rm LP}=\mathcal A x.
\]
Give this exactly complementary, primal-feasible point a one-coordinate dual residual
\(r_d=\eta e_f\), and take a \(\sigma=1\) infeasible feasibility corrector. Elimination
gives
\[
 (\mathcal A W\mathcal A^T)\Delta y=\eta\,\mathcal AWe_f. \tag{11}
\]
If \(f\) is a ground variable at vertex zero, the normalized RHS is \(e_0\), so
\(D=d\). If \(f\) is a torus edge, the RHS is a dipole, so \(D=d+2\).

## Interpretation and novelty boundary

DLS define their parameters abstractly and derive moment bounds, but do not discuss
IPMs, Newton systems, Laplacians, Weyl laws, or spectral dimension. Classical
Green-function moment thresholds are old. The apparently new contribution is their
basis-invariant translation into (3)--(4), including the distinct critical dimensions
four and eight, and the positive full-step sparse-QIPM realization.

This does not prove an end-to-end quantum LP speedup. The torus has FFT and multigrid
structure; block encoding, norm estimation, state/observable output, and classical
iterate recovery remain chargeable. The construction is a single centering corrector,
not a complete progress trajectory.

Targeted searches through 2026-09-02 found no prior derivation of these phase laws or
their QIPM realization. The relevant source is A. M. Dalzell, J. Li, and Y. Su,
[Faster quantum linear system solver beyond the condition
number](https://arxiv.org/abs/2607.07691), 2026.
