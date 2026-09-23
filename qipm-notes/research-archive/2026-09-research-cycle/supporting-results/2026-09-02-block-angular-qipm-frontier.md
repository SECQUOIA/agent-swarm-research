# Block-angular QIPM frontier: an optimal border-step speedup, but not yet an end-to-end algorithm

Date: 2026-09-02

## Motivation and scope

Block-angular and arrowhead LPs are a genuinely sparse class arising in
two-stage stochastic programming, multicommodity flow, and energy models.  A
permuted augmented Newton system has the form

\[
 K=
 \begin{bmatrix}
 D_1&&&B_1\\
 &\ddots&&\vdots\\
 &&D_N&B_N\\
 B_1^T&\cdots&B_N^T&-D_0
 \end{bmatrix},
 \qquad
 K\binom{u}{v}=\binom{f}{g},                         \tag{1}
\]

where the scenario blocks have size at most \(p\), the border has size \(k\),
\(D_i\succ0\), and \(D_0\succeq0\).  In an LP augmented system, the \(D_i\)'s
come from the positive diagonal primal--dual scaling after any scenario-local
equalities have been condensed.  Classical structure-exploiting IPMs use this
same decomposition, but must process every scenario contribution.

This note isolates a quantum theorem for the **explicit border component**
\(v\).  It is not a theorem for an explicit full Newton direction.

## Border Schur-complement theorem

Define

\[
 S=D_0+\sum_{i=1}^N B_i^TD_i^{-1}B_i,
 \qquad
 h=\sum_{i=1}^N B_i^TD_i^{-1}f_i-g.                    \tag{2}
\]

Assume \(S\succ0\).  Block elimination gives

\[
 v=S^{-1}h,
 \qquad
 u_i=D_i^{-1}(f_i-B_iv).                               \tag{3}
\]

Suppose a coherent block query returns \((D_i,B_i,f_i)\) and the dimensions
\(p,k\) are small enough that factoring one queried block costs
\(\operatorname{poly}(p,k)\).  Put

\[
 C_i=D_i^{-1/2}B_i,\qquad z_i=D_i^{-1/2}f_i,
\]

and stack the matrices \(C_i\), together with \(D_0^{1/2}\), into a matrix
\(C\in\mathbb R^{(Np+k)\times k}\).  Then \(S=C^TC\), while
\(h=C^T(z_1,\ldots,z_N,0)-g\).

Apply the quantum spectral-approximation and inverse-local-norm mean-estimation
primitives of Apers--Gribling to \(C\).  With high probability they return
explicit \(\widetilde S\) and \(\widetilde h\) such that

\[
 (1-\epsilon)S\preceq\widetilde S\preceq(1+\epsilon)S,
 \qquad
 \|\widetilde h-h\|_{S^{-1}}\leq\eta\|v\|_S.           \tag{4}
\]

The normalization in the matrix--vector primitive is material.  Write

\[
 M=Np+k,\qquad
 \alpha_z=\max_i\|D_i^{-1/2}f_i\|_\infty,\qquad
 \chi_h=\frac{\alpha_z}{\|v\|_S},                       \tag{5a}
\]

and assume \(v\ne0\).  Apers--Gribling's Theorems 3.1 and 5.1 give the
more explicit block-query bound

\[
 \widetilde O\!\left(\sqrt{Mk}\left(
       \frac1\epsilon+\frac{\chi_h}{\eta}\right)\right). \tag{5}
\]

Here \(g\) is added exactly after estimating \(C^Tz\); it does not reduce the
sampling cost.  Thus cancellation between \(C^Tz\) and \(g\) can make
\(\chi_h\), and hence the cost of a relative error guarantee, arbitrarily
large.  A theorem using (5) must either promise \(\chi_h=O(1)\), state an
absolute inverse-energy error \(\delta_h\) (in which case the second term is
\(\alpha_z/\delta_h\)), or pay for adaptive norm estimation.  The gate cost
multiplies the query cost by \(\operatorname{poly}(p,k)\), plus the cost of an
explicit \(k\)-dimensional solve.  Setting
\(\widetilde v=\widetilde S^{-1}\widetilde h\) gives

\[
 \boxed{
 \frac{\|\widetilde v-v\|_S}{\|v\|_S}
 \leq \frac{\epsilon+\eta}{1-\epsilon}.}
                                                               \tag{6}
\]

Indeed,

\[
 \widetilde v-v
 =\widetilde S^{-1}\bigl[(\widetilde h-h)
                         +(S-\widetilde S)v\bigr],
\]

\(\|S^{1/2}\widetilde S^{-1}S^{1/2}\|\leq(1-\epsilon)^{-1}\),
and
\(\|(S-\widetilde S)v\|_{S^{-1}}\leq\epsilon\|v\|_S\).

Once \(\widetilde v\) is explicit, one additional block query implements a
coherent local-direction oracle

\[
 |i\rangle|0\rangle\longmapsto
 |i\rangle\left|D_i^{-1}(f_i-B_i\widetilde v)\right\rangle. \tag{7}
\]

Thus the theorem avoids tomography of all \(Np\) local coordinates and avoids a
condition-number factor in the border solve.  It is not merely a QLSA applied to
the full arrowhead matrix: the output is an explicit classical border vector,
and the error is in the Schur energy norm.

## Sharp dependence on the number of blocks

The square-root dependence on \(N\) is optimal even for scalar, uniformly
conditioned blocks.  Let \(z_1,\ldots,z_N\in\{0,1\}\) have Hamming weight zero
or one.  Add a known base block \(i=0\), and choose

\[
 D_i=1,\quad B_0=1,\quad B_i=z_i\ (i\geq1),\quad
 f_0=1,\quad f_i=0\ (i\geq1),\quad D_0=g=0.            \tag{8}
\]

Then

\[
 S=1+\sum_i z_i,qquad h=1,qquad
 v=\begin{cases}1,&|z|=0,\\1/2,&|z|=1.\end{cases}       \tag{9}
\]

The augmented KKT matrix in (1) has condition number bounded by an absolute
constant in both cases: its nontrivial eigenvalues come from a fixed
two-dimensional subspace and the remaining eigenvalues equal one.  Therefore an
additive-\(1/6\) estimate of the scalar border direction distinguishes OR.  It
needs \(\Omega(\sqrt N)\) quantum block queries and \(\Omega(N)\) randomized
block queries.  The construction is the KKT system of an equality-constrained
strictly convex separable quadratic problem, and the same augmented matrix form
occurs in regularized or condensed IPM Newton equations.

This lower bound is elementary search, but it certifies that (5) has the optimal
\(N\)-exponent for fixed \(p,k\).  It is not a full-LP lower bound.

### Exact LP realization, and why it is not simultaneously row sparse

There is an exact standard-form LP realization at a known exact central point,
but it exposes the hidden blocks through one dense row.  Let
\(\delta=1/(2N)\), use variables \(x_0,x_{i,1},x_{i,2}\), and let the only row
of \(A_z\) contain coefficient \(1\) on \(x_0\) and the following pair for
block \(i\):

\[
 (a_{i,1},a_{i,2})=
 \begin{cases}
  (\delta,\delta),&z_i=0,\\
  (1,2\delta-1),&z_i=1.
 \end{cases}                                             \tag{10}
\]

Every pair has sum \(2\delta\).  Hence the LP

\[
 \min \mathbf1^Tx\quad\text{subject to}\quad A_zx=2,
 \qquad x\geq0                                             \tag{11}
\]

has the hidden-bit-independent strictly feasible exact center
\(x=s=\mathbf1,y=0\) at \(\mu=1\); its \(b,c,x,s\) and exact-centering
right-hand side are all known and independent of \(z\).  A centering step with
target \(\sigma\mu\) satisfies

\[
 \frac{\Delta y}{1-\sigma}
 =\frac{A_z\mathbf1}{A_zA_z^T}
 =\frac{2}{A_zA_z^T}.                                    \tag{12}
\]

Under the zero-or-one-mark promise, \(A_zA_z^T=1+1/(2N)\) with no mark and
\(A_zA_z^T=1+1/(2N)-2\delta^2+1+(2\delta-1)^2\) with one
mark.  The two values of (12) approach \(2\) and \(2/3\), respectively, so
constant additive accuracy decides OR.  All coefficients are bounded rational
numbers with \(O(\log N)\) bits, every column is 1-sparse, and the scalar normal
matrix has condition number one.  However, the single equality row has
\(2N+1\) nonzeros.  Thus this proves a coefficient-query or column-query LP
lower bound.  It is not a row-query lower bound--one query returning the whole
dense row reveals the instance--and it is not a lower bound for matrices having
both constant row and column sparsity.

There is also a structural reason the same constant-gap construction cannot
simply be replaced by a bounded-degree wiring gadget while retaining all of
its promises.  Normalize a symmetric Newton matrix so \(\|K\|\leq1\), assume
\(\|K^{-1}\|\leq\kappa=O(1)\), and let its sparsity graph have maximum degree
\(\Delta=O(1)\).  Polynomial approximation of \(1/x\) on
\([-1,-1/\kappa]\cup[1/\kappa,1]\) implies inverse decay

\[
 |(K^{-1})_{uv}|\leq C_\kappa
       \exp[-c_\kappa\operatorname{dist}(u,v)].           \tag{13}
\]

For completeness, if \(p_t\) is a degree-\(t\) polynomial uniformly
approximating \(1/x\) on the two spectral intervals, then
\((p_t(K))_{uv}=0\) whenever \(t<\operatorname{dist}(u,v)\).  Therefore
\(|(K^{-1})_{uv}|\leq\|K^{-1}-p_t(K)\|\), and the geometric convergence of
the polynomial approximation gives (13).  The same argument bounds a
constant-size off-diagonal block of \(K^{-1}\), changing only the constant.

For a perturbation \(E_i\) supported on a constant-size candidate gadget, the
resolvent identity

\[
 K_i^{-1}-K_0^{-1}=-K_i^{-1}E_iK_0^{-1}                 \tag{14}
\]

then gives, for border and gadget coordinate projectors \(P_B,P_i\),

\[
 \|P_B(K_i^{-1}-K_0^{-1})r\|
 \leq C_\kappa e^{-c_\kappa\operatorname{dist}(B,i)}
       \|E_i\|\,\kappa\|r\|.                            \tag{14a}
\]

Thus the effect on a fixed constant-size border output, for a unit-norm fixed
right-hand side and bounded \(\|E_i\|\), decays exponentially with the
gadget's distance from the border.  Among \(N\) disjoint constant-size
candidate gadgets in a bounded-degree graph some are at distance
\(\Omega(\log N)\), so they cannot all change that border output by a
constant.  This is a qualified obstruction,
not an unconditional sparse-LP lower bound: it can be evaded by growing
\(\kappa\), using an unnormalized growing right-hand side, requesting a
nonlocal output, or allowing a high-degree row/oracle.  An exact row-and-column
\(O(1)\)-sparse LP realization with all the promises in (10)--(12) is therefore
not claimed.

## What partial minimization does to the barrier parameter

Let \(F(x,y)\) be a \(\nu\)-self-concordant barrier, suppose the minimizer
\(y(x)\) exists in the interior, and assume \(F_{yy}\succ0\).  The standard
partial-minimization theorem makes

\[
 \phi(x)=\inf_y F(x,y),\qquad
 \nabla^2\phi=F_{xx}-F_{xy}F_{yy}^{-1}F_{yx},            \tag{15}
\]

a self-concordant barrier for the projection, with the inherited certificate
\(\nu_\phi\leq\nu\).  Crucially, the theorem does not replace \(\nu\) by the
dimension of \(x\).  For a separable scenario barrier
\(F_0(x)+\sum_iF_i(x,y_i)\), the usual certificate is additive and hence is
\(\nu_0+\sum_i\nu_i=\Theta(Np)\).

The failure of automatic parameter reduction is exact even in one projected
dimension.  On \(x>0\), \(|y_i|<1\), take the ordinary product log barrier

\[
 F(x,y)=\sum_{i=1}^N
   \bigl[-\log x-\log(1-y_i)-\log(1+y_i)\bigr].          \tag{16}
\]

Minimizing over all \(y_i\) gives \(\phi(x)=-N\log x\) up to a constant, whose
barrier parameter is exactly \(N\).  The projected set itself admits the
one-parameter barrier \(-\log x\), so this is not an information-theoretic
lower bound on every barrier for a projection.  It proves the narrower point
needed here: partial minimization of the standard block product barrier does
not by itself remove the scenario count.

More generally, a polytope in \(\mathbb R^k\) can have \(N\) projected facets
yet admit universal or Lewis-weight barriers with parameter depending only
linearly, or nearly linearly, on \(k\).  The unresolved issue is computational:
evaluating their gradient and Hessian for an implicitly projected recourse set
may itself require processing all scenarios.  An \(N\)-independent parameter
is immediate only when the projection has a compact explicitly evaluable
description (or the scenario terms decouple from the border); in that regime,
classical preprocessing may also erase the proposed quantum advantage.

## Collision map and classical comparator

- Classical block-angular IPMs have used Schur-complement decomposition for
  decades.  Relevant antecedents include Birge--Qi (1988),
  Grigoriadis--Khachiyan (1996), Schultz--Meyer (1989), PIPS-IPM, and the recent
  PIPS-IPM++ arrowhead solver of Kempke--Rehfeldt--Koch.  They process and sum
  all scenario Schur contributions, giving \(\Theta(N)\) block work in the
  adversarial block-oracle model.  Parallel wall-clock depth is a different
  comparator and can be small with \(N\) processors.
- Apers--Gribling already prove the spectral and gradient primitives used above.
  Their tall-LP theorem covers the special case with no genuine local degrees of
  freedom, because dualization then leaves only the \(k\) border variables.  It
  does not directly cover a block-angular LP whose dual contains
  \(\Theta(N)\) scenario-local variables.
- Generic QLS-based QIPMs can prepare a state proportional to the full arrowhead
  solution, subject to conditioning and loading assumptions.  They do not give
  the explicit \(k\)-vector guarantee (6); extracting a small border can incur an
  inverse border-amplitude cost.
- The 2025 almost-exact QIPM and the 2025--26 Hamiltonian QIPMs do not state a
  block-angular Schur aggregation theorem.  No searched source gives (5)--(7)
  as a QIPM border-output result.

## Why this is not yet the desired publishable QIPM speedup

The per-step theorem survives review, but three end-to-end obstacles remain.

1. A logarithmic-barrier method on all scenario variables has
   \(\Theta(\sqrt{Np})\) iterations.  Multiplying this by a
   \(\widetilde O(\sqrt N)\) scenario aggregation cost can reach \(\widetilde
   O(N)\), so it is not automatically a sublinear total-query algorithm.
2. A classical algorithm can read and cache all \(N\) static blocks once.
   Therefore a total static-input query claim above \(N\) is not a meaningful
   advantage.  Any end-to-end theorem must be a gate/arithmetic result for
   changing diagonal weights, or must use a barrier whose iteration count
   depends on the border dimension rather than the total local dimension.
3. Continuing the IPM requires access to the updated local iterates.  Naively
   composing (7) recursively through \(T\) iterations creates depth \(T\), while
   materializing every local update costs \(\Omega(Np)\) per iteration.

The concrete open target is therefore:

> Construct a projected or decomposed self-concordant barrier for block-angular
> LPs with complexity \(\widetilde O(k+\operatorname{poly}(p))\), whose local
> center and derivative data can be recomputed from one scenario block and the
> current explicit border point.  Combining such a barrier with (5)--(7) would
> give a genuine \(\widetilde O(\sqrt N\,\operatorname{poly}(p,k))\) QIPM for a
> first-stage/border-output contract, versus the \(\Omega(N)\) classical
> block-query lower bound.

Without that barrier or an equivalent nonrecursive local-state representation,
the result should be advertised only as an optimal quantum Newton-border module,
not as an end-to-end QIPM speedup.

## Sources checked

- Apers and Gribling, *Quantum speedups for linear programming via interior
  point methods*, arXiv:2311.03215.
- Grigoriadis and Khachiyan, *An Interior Point Method for Bordered
  Block-Diagonal Linear Programs*, SIAM Journal on Optimization.
- Schultz and Meyer, *An Interior Point Method for Block Angular
  Optimization*, SIAM Journal on Optimization.
- Kempke, Rehfeldt, and Koch, *A Massively Parallel Interior-Point-Method for
  Arrowhead Linear Programs*, arXiv:2412.07731 and SIAM J. Sci. Comput. (2026).
- Kang, Cao, Word, and Laird, *An interior-point method for efficient solution
  of block-structured NLP problems using an implicit Schur-complement
  decomposition*, Computers & Chemical Engineering 71 (2014).

Status: **new and proved as a per-Newton-step border-output theorem; the missing
projected-barrier/local-state theorem prevents an honest end-to-end QIPM claim.**
