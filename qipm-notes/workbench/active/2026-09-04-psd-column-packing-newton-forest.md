# PSD column packing has an exact Newton forest after auxiliary centering

Status: Proved; targeted literature screen completed; independently hostile-audited  
Started: 2026-09-04  
Paper status: Not incorporated  
Confidence: High within the stated reduced-direction and access-model scope;
novelty is plausible subject to specialist review

## Result

Consider the column-packed lift of

\[
             C=(B_2^s)^b
\]

from [the PSD column-packing note](2026-09-04-psd-column-packing-product-balls.md).
Every source ball is split into \(h=\lceil s/p\rceil\) coordinate columns,
and up to \(c\) columns are placed in a PSD block

\[
 Z_\ell=\begin{pmatrix}S_\ell&W_\ell^T\\W_\ell&I_p\end{pmatrix}\succ0,
 \qquad D_\ell=S_\ell-W_\ell^TW_\ell\succ0.              \tag{1}
\]

Columns from different source balls may share the same block. Let
\(\Gamma_a\) be the \(h\) columns belonging to ball \(a\), and impose

\[
       \sum_{\gamma\in\Gamma_a}(S_{\ell(\gamma)})_{\gamma\gamma}=1.
                                                                    \tag{2}
\]

The dense-looking sharing in (1) creates **no coupling at all between
source balls in the exactly reduced central-path Newton system**.

### Theorem (packing-invariant marginal barrier and Newton forest)

Partially minimize the restricted standard PSD barrier over all auxiliary
matrices \(S_\ell\), holding the projected point
\(x=(x_1,\ldots,x_b)\in\operatorname{int}C\) fixed. The minimizer is
unique and satisfies

\[
 D_\ell=\operatorname{Diag}(d_\gamma:\gamma\in\ell),
 \qquad
 d_\gamma={1-\|x_a\|^2\over h}\quad(\gamma\in\Gamma_a).   \tag{3}
\]

Consequently the marginal barrier is

\[
 \boxed{
 \bar F(x)=
   -h\sum_{a=1}^b\log(1-\|x_a\|^2)+bh\log h .}            \tag{4}
\]

It is independent of which columns share a PSD block. Its exact
self-concordant parameter is

\[
                         \boxed{\nu(\bar F)=bh.}           \tag{5}
\]

There are two exact sparsity descriptions.

1. The materialized reduced Hessian graph is the disjoint union of \(b\)
   generic \(s\)-cliques, and hence has treewidth exactly \(s-1\).
2. Before eliminating the \(h\) diagonal residuals of each ball, the
   bordered Newton/KKT graph is the disjoint union of \(b\) stars, together
   with isolated off-diagonal residual modes. Its treewidth is exactly
   one (when the graph has an edge).

Every exact reduced Newton solve therefore takes \(O(bs)\) arithmetic and
\(O(bs)\) storage. This remains true for arbitrary cross-source packing,
including the one-factor lift in \(\mathbb S_+^{s+b}\) that packs all \(b\)
balls together.

In the nontrivial balanced-capacity regime
\(p=\lfloor R/2\rfloor\leq s\) and \(H=bh\geq c=R-p\), balanced packing
simultaneously has

\[
 L=O(bs/R^2),\qquad M_{\rm cone}=O(bs),\qquad
 \nu_{\rm ambient}=O(bs/R),\qquad
 \nu_{\rm slice}=O(bs/R),                                \tag{6}
\]

and an exact latent-treewidth-one central Newton system. Dense PSD
packing does not force dense projected Newton algebra on this family.
Outside that regime the exact ceiling formulas below should be used; in
particular, no asymptotic expression is meant to hide one final PSD block.

The statement is additive for heterogeneous products. If
\[
       C=\prod_{a=1}^b B_2^{s_a},\qquad
       h_a=\left\lceil{s_a\over p}\right\rceil,
\]
and all resulting columns are packed arbitrarily, then
\[
 \bar F(x)=
   -\sum_{a=1}^b h_a\log(1-\|x_a\|^2)
     +\sum_{a=1}^b h_a\log h_a,\qquad
 \nu(\bar F)=\sum_a h_a.                                  \tag{6a}
\]
The exact bordered graph remains one star per source body and the
projected solve takes \(O(\sum_a s_a+\sum_a h_a)\) arithmetic. The proof
below applies source by source without change.

## 1. Exact partial minimization

Because the bottom-right block of (1) is the public identity,

\[
                         -\log\det Z_\ell=-\log\det D_\ell. \tag{7}
\]

Write \(d_\gamma=(D_{\ell(\gamma)})_{\gamma\gamma}\). Equation (2)
becomes

\[
          \sum_{\gamma\in\Gamma_a}d_\gamma
             =\rho_a,
 \qquad \rho_a:=1-\|x_a\|^2>0.                            \tag{8}
\]

For fixed diagonal, Hadamard's determinant inequality gives

\[
              \det D_\ell\leq\prod_{\gamma\in\ell}d_\gamma,
\]

with equality, for a positive-definite matrix, exactly when \(D_\ell\) is
diagonal. The remaining problem separates by source ball:

\[
 \min\left\{-\sum_{\gamma\in\Gamma_a}\log d_\gamma:
      d_\gamma>0,\ \sum_{\gamma\in\Gamma_a}d_\gamma=\rho_a\right\}.
                                                                    \tag{9}
\]

Strict convexity or AM--GM makes its unique solution
\(d_\gamma=\rho_a/h\). Substitution proves (3)--(4). Notice that neither
Hadamard's step nor (9) remembers the block packing layout.

For one ball, put \(r=\|x\|\) and \(\rho=1-r^2\). The gradient and Hessian
of \(f_h(x)=-h\log\rho\) are

\[
 \nabla f_h={2h\over\rho}x,
 \qquad
 \nabla^2f_h={2h\over\rho}I+{4h\over\rho^2}xx^T.          \tag{10}
\]

The squared local dual norm of the gradient is

\[
 \|\nabla f_h(x)\|_{x,*}^2
       ={2hr^2\over1+r^2}\ \longrightarrow\ h
       \quad(r\uparrow1).                                 \tag{11}
\]

Scaling the standard ball barrier by \(h\geq1\) preserves
self-concordance, so (11) proves that its parameter is exactly \(h\).
Parameters add on Cartesian products, and approaching every ball boundary
simultaneously proves (5).

## 2. Exact Newton congruence in the original lift

The forest is not merely a symbolic representation of (10). It follows
by exact block elimination from the lifted log-determinant Hessian.

Work at an auxiliary-centered point (3). For one packed block write a
direction as \((A,U)=(\delta S,\delta W)\) and define the invertible linear
change of direction coordinates

\[
                    B=A-W^TU-U^TW.                        \tag{12}
\]

At diagonal \(D=\operatorname{Diag}(d_\gamma)\), the second differential is

\[
 d^2(-\log\det D)[A,U]
   =\operatorname{tr}(D^{-1}BD^{-1}B)
       +2\operatorname{tr}(D^{-1}U^TU).                   \tag{13}
\]

Every off-diagonal \(B_{\gamma\delta}\) is an independent positive
quadratic mode and has no linear objective or equality term. It therefore
eliminates without fill. Put \(q_\gamma=B_{\gamma\gamma}\), and write
\(u_\gamma\) for the variation of the coordinates in column \(\gamma\).
The linearization of (2) is exactly

\[
 \sum_{\gamma\in\Gamma_a}
       \bigl(q_\gamma+2x_\gamma^Tu_\gamma\bigr)=0.        \tag{14}
\]

After removing the off-diagonal modes, (13) is diagonal:

\[
 \sum_\gamma {q_\gamma^2\over d_\gamma^2}
       +2\sum_\gamma{\|u_\gamma\|^2\over d_\gamma}.       \tag{15}
\]

Introduce one multiplier \(\lambda_a\) for (14). In scalar coordinates,
the KKT graph has only the edges

\[
     \lambda_a-q_\gamma,\qquad
     \lambda_a-u_{\gamma j}
     \quad(\gamma\in\Gamma_a),                            \tag{16}
\]

plus diagonal entries. It is therefore exactly a forest of stars; the
discarded off-diagonal \(B\)'s are isolated. This proves treewidth one.
The graph is independent of which columns coexist in a PSD block because
those interactions were absorbed by the free residual coordinates (12).

This is a genuine elimination effect, not sparsity already visible in the
naive lifted coordinates. At a generic \(W_\ell\), the term
\[
 \bigl(A_{\gamma\delta}
       -x_\gamma^Tu_\delta-u_\gamma^Tx_\delta\bigr)^2
\]
in (13) makes all scalar \(U\)-variables in a full \(p\)-by-\(c_\ell\)
block a clique. Thus the naive lifted Hessian graph contains
\(K_{pc_\ell}\), and has treewidth at least \(pc_\ell-1\). In the
one-factor \(p=s,c=b\) construction this lower bound is \(bs-1\), while
the exact reduced bordered graph still has width one.

Eliminating \(q\) and \(\lambda\) in each star yields (10). At a generic
point with every coordinate of \(x_a\) nonzero, its rank-one term has every
off-diagonal entry nonzero, so the materialized Hessian graph on \(x_a\) is
\(K_s\). Hence its generic structural treewidth is exactly \(s-1\), even
though its rank-expanded treewidth is one.

The same calculation can be phrased as the auxiliary-centered residual
manifold

\[
 d_\gamma>0,\qquad
 \sum_{\gamma\in\Gamma_a}d_\gamma+\|x_a\|^2=1,            \tag{17}
\]

with barrier \(-\sum_\gamma\log d_\gamma\). Its bordered Hessian has
diagonal primal blocks and one equality hub per source ball. Formula
(12) shows why this reduced nonlinear description is an exact Newton
Schur complement of the original affine PSD lift at every
auxiliary-centered point.

## 3. Balanced curvature capacity and low treewidth are compatible

Take

\[
       p=\lfloor R/2\rfloor,\qquad c=R-p,\qquad
       h=\left\lceil{s\over p}\right\rceil,\qquad H=bh.    \tag{18}
\]

Pack the \(H\) columns arbitrarily into groups of at most \(c\). Then

\[
 L=\left\lceil{H\over c}\right\rceil,\qquad
 \nu_{\rm slice}=H,\qquad
 \nu_{\rm ambient}=pL+H.                                  \tag{19}
\]

Full blocks carry the maximum PSD mixed-curvature capacity
\(pc=\lfloor R^2/4\rfloor\). Away from ceilings, (19) and the cone
coordinate formula in the construction note give (6). More explicitly,
when \(R=O(s)\) and \(R^2=O(bs)\),
\[
 H=\Theta(bs/R),\quad L=\Theta(bs/R^2),\quad
 \nu_{\rm ambient}=\Theta(bs/R),\quad M_{\rm cone}=\Theta(bs).
\]
Without these size assumptions, (18)--(19) and the exact cone-coordinate
sum are the valid ledger. Equations
(12)--(16) show simultaneously that the reduced KKT treewidth is one and
the exact solve cost is \(O(bs)\). There is no tradeoff between balanced
curvature packing and *latent* Newton treewidth on this construction.

At the extreme setting \(p=s,c=b,R\geq s+b\), all columns fit in one PSD
block. Here

\[
 L=1,\qquad \nu_{\rm slice}=b,\qquad
 \bar F(x)=-\sum_a\log(1-\|x_a\|^2),                      \tag{20}
\]

and the exact reduced KKT graph is still \(b\) disconnected stars. One
dense cone factor can therefore share every slack row without creating a
single cross-ball edge after exact auxiliary elimination.

For projected Newton arithmetic alone, factor sharing is not the right
objective. Under the order cap \(p+c\leq R\), every \(p\) has the same
\(O(bs)\) reduced solve, while its standard certificate uses
\[
        H_p=b\left\lceil{s\over p}\right\rceil.
\]
Therefore the smallest short-step reduced-work certificate within this
construction chooses
\[
        p_*=\min\{s,R-1\},\qquad c=1,                     \tag{21}
\]
and is
\[
 O\!\left(
   bs\sqrt{b\left\lceil{s\over p_*}\right\rceil}
   \log(\Delta/\epsilon)\right).                          \tag{22}
\]
Balanced \(p\approx c\approx R/2\) instead minimizes the PSD
factor/capacity scales while retaining linear work per projected solve.
Thus the construction has a real **factor-count versus iteration-certificate**
tradeoff, but no factor-count versus latent-treewidth tradeoff. Formula
(22) is only an upper certificate, not an actual iteration lower bound.

## 4. Classical and quantum linear-solver ledger

Let \(n=bs\), \(H=bh\), and let

\[
       T=O\!\left(\sqrt H\log(\Delta/\epsilon)\right)      \tag{23}
\]

be the usual short-step *upper certificate* for the marginal barrier. It
is not an iteration lower bound.

### Explicit classical reduced solve

For each source ball, (10) is diagonal plus rank one. Sherman--Morrison,
or leaf elimination in (16), applies its inverse in \(O(s)\) arithmetic.
Thus

\[
 \begin{array}{c|c|c}
   &\text{one reduced Newton solve}&\text{short-step ledger}\\ \hline
 \text{classical arithmetic}&O(n)&O(n\sqrt H\log(\Delta/\epsilon))\\
 \text{working storage}&O(n)&O(n)
 \end{array}                                               \tag{24}
\]

This is an upper bound for the explicit family, not a general lower bound
for all algorithms or all SDP instances.

The unpreconditioned eigenvalue ratio within the \(a\)-th block is exactly

\[
          \kappa_a={1+\|x_a\|^2\over1-\|x_a\|^2}.          \tag{25}
\]

It is independent of \(h\) and of the packing. A diagonal-plus-radial
rank-one solve removes this conditioning exactly; treating only the
diagonal part as a blockwise scalar preconditioner leaves ratio (25).
For clarity, if the radii differ across balls, the unpreconditioned
condition number of the whole block-diagonal Hessian need not equal
\(\max_a\kappa_a\): its exact value is
\[
 {\displaystyle\max_a{1+\|x_a\|^2\over(1-\|x_a\|^2)^2}
  \over
  \displaystyle\min_a{1\over1-\|x_a\|^2}}.
                                                                    \tag{25a}
\]
After symmetric scaling of block \(a\) by
\(\sqrt{(1-\|x_a\|^2)/(2h)}\), the eigenvalues are \(1\) in its
tangential space and \(\kappa_a\) in its radial direction, so the
preconditioned global condition number is \(\kappa_{\max}:=\max_a\kappa_a\).

For a linear objective with block \(c_a\) and central multiplier \(\eta\),
stationarity gives the more explicit path identity

\[
 \kappa_a(\eta)
   =\sqrt{1+\left({\eta\|c_a\|\over h}\right)^2}.          \tag{26}
\]

This particular uncoupled optimization family even has a closed-form
central path, so its purpose is to expose formulation and Newton-algebra
effects, not to manufacture an algorithmic speedup. The companion
[dynamic scale-access theorem](2026-09-04-dynamic-psd-fiber-scale-maintenance-lower-bound.md)
records the resulting positive caching corollary: all fiber-center scales
along this exact path are compiled from the fixed objective-block norms,
so those norms are computed once rather than maintained after every path
step.

### Added sparse affine constraints

If one adds sparse affine constraints \(Ax=d\), the packing still
disappears. In the direction coordinates above, add one constraint hub
\(y_j\) adjacent to \(u_i\) exactly when \(A_{ji}\ne0\). Let
\(G_{\rm aug}\) be the bipartite scalar-variable/hub graph containing
these constraint hubs and the \(b\) ball hubs from (16), but not the
\(q_\gamma\) or off-diagonal \(B\) vertices. The generic rank-expanded
KKT graph is obtained from \(G_{\rm aug}\) by attaching every
\(q_\gamma\) as a leaf and adding the off-diagonal \(B\)'s as isolated
vertices. Therefore

\[
 \operatorname{tw}(K_{\rm rank})
   =\max\{1,\operatorname{tw}(G_{\rm aug})\}.              \tag{27}
\]

Given a width-\(\tau\) decomposition, symbolic scalar sparse elimination
uses \(O(N_{\rm KKT}\tau^2)\) factorization work and
\(O(N_{\rm KKT}\tau)\) factor storage, followed by
\(O(N_{\rm KKT}\tau)\) triangular solves in exact arithmetic, assuming a
nonsingular system and an admissible pivot ordering. The relevant width is
that of the original sparse constraints augmented by one hub per ball, not
the PSD packing layout.

### Quantum state-only solve

Under coherent row/block access to the current \(x_a\), their norms, the
Newton right-hand side, and the blockwise scalar preconditioner described
after (25a), a generic block-encoding linear solver applied to the
preconditioned version of (10) has the conditional state-generation cost

\[
       \widetilde O\!\left(
          T\,\kappa_{\max}
          \log(1/\epsilon_{\rm lin})\operatorname{polylog}n\right), \tag{28}
\]

up to the chosen block-encoding normalization and success amplitude.
The explicit radial eigenspaces permit a direct coherent transform if the
access model supplies the block norms and supports blockwise projections,
but normalization and postselection can reintroduce
\(\kappa_{\max}\). Thus no unconditional removal of condition dependence
is claimed.

Any final output that materializes all \(n\) projected coordinates costs
\(\Omega(n)\) writes or measurements. Materializing a full centered PSD
lift also requires the Gram entries

\[
                  S_\ell=W_\ell^TW_\ell+\operatorname{Diag}d, \tag{29}
\]

whose explicit formation must be charged; ordinary dense multiplication
costs \(O(\sum_\ell p c_\ell^2)\), although factored or query access can
avoid forming (29). Therefore (28) is a state-only conditional ledger,
not an end-to-end quantum speedup. Conversely, the \(O(n)\) classical
solve and output bound do not exclude advantages for a specified compressed
scalar task under a matched oracle model.

Likewise, reconstructing the full lifted Newton direction requires
\[
      A_{\rm off}= (W^TU+U^TW)_{\rm off}
\]
after the zero off-diagonal \(B\)-modes are eliminated. Explicit
reconstruction has the same ordinary
\(O(\sum_\ell p c_\ell^2)\) Gram-product ledger. The \(O(n)\) result in
(24) is therefore exactly a **projected/reduced-direction** bound, not a
claim that all dense lifted auxiliary coordinates can be output in linear
time.

The key QIPM conclusion is narrower and robust: reducing the number of PSD
factors to the curvature-capacity scale does not increase the exact
central Newton solve beyond linear classical work, and materialized dense
Hessian treewidth would badly mismeasure this algebra.

The companion
[PSD--Lorentz reduced-oracle equivalence theorem](2026-09-04-psd-lorentz-reduced-oracle-equivalence.md)
strengthens this observation to an exact two-way quantum query reduction:
under matched complete-unitary access and projected Newton-state output,
the packed PSD and grouped Lorentz systems have identical normalization,
conditioning, right-hand side, and output state.

## 5. Scope and literature boundary

The result concerns the standard product PSD log-determinant restricted to
this particular affine lift and then exactly minimized over its auxiliary
fiber. It does not prove:

- that arbitrary SDP iterates automatically remain auxiliary-centered;
- a finite-precision stability theorem for recentering;
- an iteration or input-query lower bound;
- a quantum advantage for scalar or state output; or
- the same forest structure for arbitrary PSD lifts with the same resource
  counts.

Exact central-path points are auxiliary-centered because the objective is
independent of \(S\). An implementation may maintain the reduced system
directly or explicitly recenter (29); the latter's arithmetic and precision
costs must be included.

A targeted search found the standard literature on chordal SDP conversion,
log-determinant Schur-complement systems, and low-treewidth SDP complexity,
including Zhang,
[*Complexity of Chordal Conversion for Sparse Semidefinite Programs with
Small Treewidth*](https://arxiv.org/abs/2306.15288), and Zheng et al.,
[*Chordal decomposition in operator-splitting methods for sparse
semidefinite programs*](https://arxiv.org/abs/1707.05058). It did not find
the packing-invariant marginal identity (4), the exact congruence
(12)--(16), or the coexistence of balanced PSD curvature packing and an
exact Newton forest. Novelty is plausible, but this is not a comprehensive
or specialist literature review.
