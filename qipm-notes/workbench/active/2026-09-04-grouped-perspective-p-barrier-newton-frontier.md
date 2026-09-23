# Barrier and Newton frontier for grouped perspective-$p$ cones

Status: Proved parameter bounds, Newton structure, and characteristic-family obstructions; literature-screened; independently audited  
Started: 2026-09-04  
Paper status: Not incorporated  
Confidence: High on all stated mathematics; moderate on publishable novelty after the targeted literature screen

## Cone and executive result

For $1<p<\infty$, $q=p/(p-1)$, and $r\geq1$, let

\[
 \mathcal P_{p,r}
 =\operatorname{cl}\left\{(u,v,w)\in\mathbb R^2\times\mathbb R^r:
 u,v>0,\quad uv^{p-1}>\|w\|_p^p\right\}.                 \tag{1}
\]

Write $\nu_{\rm opt}^{\rm LH}(C)$ for the infimum of the parameters of
logarithmically homogeneous self-concordant barriers on a proper cone $C$,
including barriers which couple the factors when $C$ is a product.  Let
$h(p)$ denote Hildebrand's three-dimensional power-cone lower bound,
as defined in the companion power-cone notes.  Then

\[
 \boxed{h(p)\leq \nu_{\rm opt}^{\rm LH}(\mathcal P_{p,r})\leq r+2.} \tag{2}
\]

At $p=2$, the cone is a rotated Lorentz cone and the exact value is

\[
                    \boxed{\nu_{\rm opt}^{\rm LH}(\mathcal P_{2,r})=2.} \tag{3}
\]

For $p\ne2$, no dimension-dependent lower bound or explicit barrier
attaining the existential upper endpoint in (2) was found.  In particular, the
generalized-power-cone theorem of Roy--Xiao does **not** prove an
$r+2$- or constant-parameter explicit barrier for (1): its vector output
is measured in the Euclidean norm, whereas (1) uses the $\ell_p$ norm.
There is, however, a new dimension-dependent obstruction for the canonical
characteristic-function family: for $p>2$ its parameter is at least
$(r+2)/(3/2+(r-1)/p)$, which tends to $p$ with $r$; see (5d).  This sharpens
the family-specific picture without closing the arbitrary-barrier gap.

For a product with nonempty groups of sizes $r_1,\ldots,r_k$, restriction
to one output coordinate in every factor and the positive-branch product
certificate give the stronger coupled-product statement

\[
 \boxed{
 k h(p)\leq
 \nu_{\rm opt}^{\rm LH}\!\left(\prod_{j=1}^k\mathcal P_{p,r_j}\right)
 \leq\sum_{j=1}^k(r_j+2).
 }                                                               \tag{4}
\]

At $p=2$, the exact product value is $2k$.  Away from $p=2$,
both gaps in (2) and (4) are open.

## Proof of the parameter bounds

### Duality and the scalar section

The dual cone has the exact description

\[
 \mathcal P_{p,r}^*
 =\left\{(a,b,z):a,b\geq0,\quad
 a^{1/p}b^{1/q}\geq p^{-1/p}q^{-1/q}\|z\|_q\right\}.             \tag{5}
\]

Indeed, after writing (w=vs), dual membership is equivalent to

\[
       a\|s\|_p^p+b+z\mathbin\cdot s\geq0\qquad\hbox{for every }s,
\]

and the conjugate of $a\|s\|_p^p$ is

\[
 {\|z\|_q^q\over q(ap)^{q-1}}.
\]

Consequently $\mathcal P_{p,r}^*$ is diagonally linearly isomorphic to
$\mathcal P_{q,r}$ under
$(a,b,z)\mapsto(b,a,p^{-1/p}q^{-1/q}z)$.  This also
checks the expected Hölder-dual symmetry of every bound.

Set all but one coordinate of $w$ to zero.  This linear section meets the
interior of (1) and is the three-dimensional power cone with exponent $1/p$.
Restriction of an LHSC barrier preserves its parameter.  Hildebrand's
three-dimensional lower bound therefore gives the left side of (2).

There is also an exact high-dimensional section that gives a useful comparison.
On the linear subspace $u=v=t$, condition (1) becomes

\[
                         t\geq\|w\|_p.                         \tag{5a}
\]

This section meets the interior, so

\[
 \boxed{
 \nu_{\rm opt}^{\rm LH}(\mathcal P_{p,r})
 \geq \nu_{\rm opt}^{\rm LH}(K_{p,r+1}).
 }                                                               \tag{5b}
\]

The product version follows by taking these sections factor by factor.  Thus a
grouped perspective cone cannot have a lower intrinsic optimal barrier parameter
than the $p$-order cone on the same $r$ norm coordinates.  Equation (5b) is
stronger as a comparison theorem than the numerical lower bound $h(p)$, although
the best presently known numerical lower bound for the right-hand side is still
$h(p)$ when $r\geq2$.

For a product, take the product of these interior-meeting scalar sections.  The
positive-branch cross-ratio product theorem for three-dimensional power cones
applies to an arbitrary, possibly nonseparable barrier on the product and gives
the left side of (4).  This is not merely summing lower bounds of separately
chosen factor barriers.

The canonical-barrier existence theorem gives an LHSC barrier of parameter at
most the ambient cone dimension.  Since $\dim\mathcal P_{p,r}=r+2$, summing
canonical barriers proves the upper endpoints in (2) and (4).  This is an
existence result, not an efficient derivative oracle.

Finally, when $p=2$, $uv\geq\|w\|_2^2$ is linearly isomorphic to the
$(r+2)$-dimensional Lorentz cone.  Its optimal parameter is two.  The
universal product lower bound and the sum of Lorentz barriers give the exact
$2k$ product statement.

## New obstruction for the characteristic-barrier family

The broad interval (2) remains open, but the characteristic-function family can
be separated sharply from its lower endpoint in growing dimension.  Define

\[
 \zeta_{p,r}(x)=\int_{\mathcal P_{p,r}^*}e^{-\langle x,s\rangle}\,ds,
 \qquad \Phi_{p,r,\kappa}(x)=\kappa\log\zeta_{p,r}(x).          \tag{5c}
\]

Since the cone dimension is $r+2$, this function, if self-concordant, is an
LHSC barrier of parameter $\nu=(r+2)\kappa$.  For $r\geq2$ and $p>2$,
self-concordance necessarily implies

\[
 \boxed{
 \nu(\Phi_{p,r,\kappa})
 \geq {r+2\over \frac32+\frac{r-1}{p}}>2.
 }                                                               \tag{5d}
\]

In particular, the right side tends to $p$ as $r\to\infty$.  The bound concerns
scalar multiples of the characteristic barrier only; it is not a lower bound on
all LHSC barriers on $\mathcal P_{p,r}$.

Here is a direct proof.  Put $\alpha=1/p$ and $\beta=1/q$.  Formula (5) gives
the following one-to-one parametrization of the interior of the dual cone, up to
a null boundary set:

\[
 a=s\alpha,\qquad z=-sy,\qquad
 b=s\bigl(\beta\|y\|_q^q+\rho\bigr),qquad
 s>0,\ y\in\mathbb R^r,\ \rho>0.                               \tag{5e}
\]

Its Jacobian is $\alpha s^{r+1}$.  Evaluate at the interior points
$x_\delta=(1+\delta,1,e_1)$ and integrate first in $\rho$ and then in $s$:

\[
 \zeta_{p,r}(x_\delta)
 =\alpha\Gamma(r+1)\int_{\mathbb R^r}
 \left[\alpha\delta+\alpha+\beta\|y\|_q^q-y_1\right]^{-(r+1)}dy. \tag{5f}
\]

Young's inequality says that the bracket at $\delta=0$ is nonnegative and
vanishes uniquely at $y=e_1$.  With $y_1=1+\eta$ and
$y_\perp=(y_2,\ldots,y_r)$, its local expansion is

\[
 \alpha\delta+{q-1\over2}\eta^2
       +\beta\|y_\perp\|_q^q+O(|\eta|^3).                     \tag{5g}
\]

Moreover, on a sufficiently small fixed neighborhood there are constants
$c_1,c_2>0$ such that the bracket at $\delta=0$ is bounded below and above by
$c_1(\eta^2+\|y_\perp\|_q^q)$ and
$c_2(\eta^2+\|y_\perp\|_q^q)$.  Off that neighborhood it has a positive
lower bound on compact sets, while for sufficiently large $\|y\|$ it is at
least $c_3\|y\|_q^q$.  The anisotropic substitution
$\eta=\delta^{1/2}t$, $y_\perp=\delta^{1/q}z$ in (5f), together
with a fixed-neighborhood/tail split, yields

\[
 \zeta_{p,r}(x_\delta)
 =C_{p,r}\delta^{-B_{p,r}}(1+o(1)),\qquad
 B_{p,r}=r+1-\frac12-\frac{r-1}{q}
        =\frac32+\frac{r-1}{p}.                                \tag{5h}
\]

These bounds also dominate the differentiated integrands of orders
$k=0,1,2,3$; the tail is integrable because $q(r+1+k)>r$.  Thus the same
rescaling argument after differentiating (5f) under the integral gives
$\zeta^{(k)}\sim(-1)^k(B_{p,r})_kC_{p,r}\delta^{-B_{p,r}-k}$ through
order three, where $(B)_k$ is the rising factorial.  Hence, for
$f_\kappa(\delta)=\Phi_{p,r,\kappa}(x_\delta)$,

\[
 f_\kappa''(\delta)={\kappa B_{p,r}\over\delta^2}(1+o(1)),
 \qquad
 f_\kappa'''(\delta)=-{2\kappa B_{p,r}\over\delta^3}(1+o(1)).  \tag{5i}
\]

Restriction to a line preserves self-concordance, so
$|f'''|\leq2(f'')^{3/2}$ forces $\kappa B_{p,r}\geq1$.  Multiplying
by the homogeneity degree $r+2$ proves (5d).  Strictness above two is
equivalent to $(r-1)(1-2/p)>0$.

For $1<p<2$, apply the same result to the characteristic barrier of the dual
cone, which is linearly isomorphic to $\mathcal P_{q,r}$ with $q>2$, and then
take the Legendre dual barrier back to $\mathcal P_{p,r}$.  Thus the corresponding
dual-characteristic family necessarily has

\[
 \nu\geq {r+2\over \frac32+\frac{r-1}{q}}>2.                  \tag{5j}
\]

Combined with the universal lower bound, the characteristic-family obstruction
is $\max\{h(p),(r+2)/B_{p,r}\}$ for $p>2$; for sufficiently large $r$ it is
strictly stronger than the known arbitrary-barrier bound $h(p)$.

### Comparator: the high-dimensional $p$-order characteristic barrier

The same calculation gives a useful new comparator and extends the previously
recorded three-dimensional obstruction.  For
$K_{p,r+1}=\{(t,w):t\geq\|w\|_p\}$, parameterize its dual as
$(s,sy)$ with $s>0$ and $y\in B_q^r$.  At
$\widehat x_\delta=(1+\delta,e_1)$,

\[
 \widehat\zeta_{p,r}(\widehat x_\delta)
 =\Gamma(r+1)\int_{B_q^r}(1+\delta+y_1)^{-(r+1)}dy.             \tag{5k}
\]

Near the unique contact $y=-e_1$, put $a=1+y_1$.  The transverse
$(r-1)$-dimensional section has volume
$C a^{(r-1)/q}(1+O(a))$.  The same rescaling and differentiated-tail argument
therefore gives exponent

\[
 \widehat B_{p,r}=r-\frac{r-1}{q}=1+\frac{r-1}{p}.             \tag{5l}
\]

Consequently, for $p>2$, any self-concordant scalar multiple of the
characteristic barrier on $K_{p,r+1}$ has

\[
 \boxed{
 \nu\geq {r+1\over 1+\frac{r-1}{p}}>2.
 }                                                               \tag{5m}
\]

At $r=2$, this is $3p/(p+1)$, exactly the earlier three-dimensional
characteristic-family obstruction.  For $1<p<2$, the Hölder-dual statement
again applies to the dual-characteristic family.  Both (5d) and (5m) tend to
$p$ as $r\to\infty$, but for $p>2$ the grouped obstruction is strictly smaller:

\[
 {r+2\over \frac32+\frac{r-1}{p}}
 <{r+1\over 1+\frac{r-1}{p}},                                  \tag{5n}
\]

because the sign of the cross-multiplied difference is
$(r-1)(1/p-1/2)<0$.  Thus the necessary obstruction is slightly weaker for
the grouped characteristic family, while it still fails to keep the necessary
parameter near two as $r$ grows.  The comparison alone does not determine the
actual self-concordance threshold of either family.

## A computable $3r$-barrier and its Newton oracle

Put $\alpha=1/p$, $\beta=1-\alpha$, and use Chares's rigorous
parameter-three barrier for the scalar power cone,

\[
 \phi_\alpha(a,v,z)
 =-\log(a^{2\alpha}v^{2\beta}-z^2)
  -\beta\log a-\alpha\log v.                                  \tag{6}
\]

The grouped cone has the exact scalar-power representation

\[
 (u,v,w)\in\mathcal P_{p,r}
 \quad\Longleftrightarrow\quad
 \exists a\in\mathbb R^r:
 \sum_i a_i=u,\quad (a_i,v,w_i)\in\mathcal P_{p,1}\quad\forall i. \tag{7}
\]

Restrict the sum of (6) to the shared-$v$ subspace and partially minimize
the artificial $a_i$'s:

\[
 \Psi_{p,r}(u,v,w)
 =\min_{\sum_i a_i=u}\sum_{i=1}^r\phi_\alpha(a_i,v,w_i).        \tag{8}
\]

The fibers are bounded, the objective diverges at every fiber boundary, and its
Hessian is positive definite.  The exact partial-minimization theorem therefore
makes (8) a nondegenerate $3r$-LHSC barrier on
$\mathcal P_{p,r}$.  Logarithmic homogeneity can also be checked directly:
the minimizer scales as $a\mapsto\tau a$, and the sum in (8) changes by
$-3r\log\tau$.

This upper bound is computational but is weaker than the existential
$r+2$ bound for $r\geq2$.  Its advantage is an essentially linear-time
local Newton oracle.  If $\lambda$ is the multiplier of $\sum_i a_i=u$,
the minimizing variables are characterized by

\[
       \phi_{a}(a_i,v,w_i)+\lambda=0,\qquad \sum_i a_i=u.       \tag{9}
\]

Because $\phi_{aa}>0$, each $a_i$ is a monotone scalar function of
$\lambda$; hence (9) reduces to one scalar root.  Once it is found, the
value and gradient cost $O(r)$ scalar operations.

There is also an exact $O(r)$ Hessian-vector product.  At the minimizer set

\[
 A_i=\phi_{aa}(a_i,v,w_i)>0,qquad
 g_i=\phi_{av}(a_i,v,w_i)\,\dot v+
     \phi_{aw}(a_i,v,w_i)\,\dot w_i,qquad
 S=\sum_iA_i^{-1}.                                             \tag{10}
\]

Differentiating (9) in a direction ($\dot u,\dot v,\dot w$) gives

\[
 \dot\lambda=-{\dot u+\sum_i g_i/A_i\over S},
 \qquad
 \dot a_i=-{g_i+\dot\lambda\over A_i}.                        \tag{11}
\]

Since

\[
 \Psi_u=-\lambda,qquad
 \Psi_v=\sum_i\phi_v(a_i,v,w_i),qquad
 \Psi_{w_i}=\phi_w(a_i,v,w_i),                                \tag{12}
\]

substitution of (11) into the differential of (12) evaluates
$\nabla^2\Psi\,\dot x$ in one pass.  Equivalently, the Hessian is a sparse
arrowhead matrix (the shared $v$ couples to every $w_i$) plus one
rank-one correction caused by $\sum_i a_i=u$.  Thus partial minimization
removes $r-1$ cone coordinates without turning the local Newton operation
into generic dense linear algebra.

The defining-function ansatz does not provide a shortcut.  A barrier based only
on $-\log(uv^{p-1}-\sum_i|w_i|^p)$ is not $C^2$ on interior
coordinate axes for $1<p<2$, and for $p>2$ has zero transverse Hessian
there.  Additional singular corrections would be essential.

## Exact representation comparison under a block cap

Consider an exact lift of $B_p^N$ with cone-block dimension cap $d\geq3$, and
write $b=d-2$.  Three natural ambient products have the following rigorous
parameter ledgers.

\[
\begin{array}{c|c|c|c}
\text{representation}&\text{factor count}&\text{rigorous LH optimum interval}
&\text{standard scalar-power barrier}\\ \hline
\text{coordinate power cones}&N&[Nh(p),\,3N]&3N\\
\text{grouped perspective cones}&
k_g=\lceil N/b\rceil&[k_gh(p),\,N+2k_g]&3N\\
p\text{-order tree}&
k_t=\lceil(N-1)/b\rceil&[k_th(p),\,N-1+2k_t]&3(N-1+k_t)
\end{array}                                                     \tag{13}
\]

The last entry accounts for every norm coordinate in every tree block:
$\sum_j(m_j-1)=N-1+k_t$.  At $p=2$, the exact ambient optima in the three
rows are respectively $(2N,2k_g,2k_t)$, because all relevant grouped or tree
blocks are Lorentz.  The last column records the direct guarantee obtained from
Chares's parameter-three scalar power barrier and partial minimization; it is not
a lower bound on all efficiently evaluable barriers.

Several conclusions are immediate.

1. Grouping can lower the *existential* product-barrier upper bound from $3N$
   to $N+2k_g$, but the currently explicit partial-minimized barrier still
   has parameter $3N$.  Thus no improved worst-case iteration count follows
   from the known efficient oracle.
2. The $p$-order tree weakly dominates the grouped construction in the
   *existential* parameter/dimension ledger: $k_t\leq k_g$, and its canonical
   upper endpoint is smaller by one when the counts agree and by three when
   $k_g=k_t+1$.  For the standard computable barriers, however, grouping uses
   only $N$ scalar power atoms and has parameter $3N$, whereas the tree uses
   $N-1+k_t$ atoms and has parameter $3(N-1+k_t)$.  Grouping therefore gives
   a genuine explicit-barrier saving whenever $k_t>1$, besides the globally
   bi-$C^1$ contact sheets proved in the companion theorem.
3. The direct cones exhibit the unresolved core gaps
   $h(p)\leq\nu_{\rm opt}(K_{p,N+1})\leq N+1$ and
   $h(p)\leq\nu_{\rm opt}(\mathcal P_{p,N})\leq N+2$.
   Consequently it is unknown whether a single large non-Euclidean norm or
   perspective cone admits an $O_p(1)$-parameter LHSC barrier.  Resolving this
   is necessary before claiming a dimension-independent QIPM iteration advantage
   from grouping.
4. The characteristic-family bounds (5d) and (5m) are a separate frontier:
   they grow to $p$ for fixed $p>2$ and increasing block size, but constrain
   only scaled characteristic barriers (or, after duality, the explicitly named
   dual-characteristic family).  They do not tighten the arbitrary-barrier
   intervals in (13) and must not be inserted as general QIPM iteration lower
   bounds.

The Hessian ledger points in the opposite direction from the existential
parameter ledger.  Coordinatewise power cones give $3\times3$ block-diagonal
barrier Hessians.  The grouped partially minimized barrier gives sparse-arrowhead
plus rank-one blocks and an $O(N)$ aggregate Hessian-vector oracle, but retains
parameter $3N$.  Thus the standard short-step bounds are
$O(\sqrt{3N}\log(1/\epsilon))$ for both the coordinate and grouped barriers,
and $O(\sqrt{3(N-1+k_t)}\log(1/\epsilon))$ for the standard tree barrier.
The canonical $N+2k_g$-parameter barrier is not supplied
with an efficient gradient, Hessian, conjugate-gradient, sparse-access, or
block-encoding oracle.  A QIPM complexity statement must not combine the
canonical parameter with the sparse oracle of the different $3N$-barrier.
For $k_g$ groups, the implicit Hessian is a sparse matrix plus at most $k_g$
rank-one corrections.  This is compatible with sparse-plus-low-rank quantum
linear algebra only under separate state-preparation and conditioning promises;
the structural identity alone is not an end-to-end QIPM speedup.

## Literature boundary

- [Glineur and Terlaky](https://doi.org/10.1023/B:JOTA.0000042522.65261.51),
  *Conic Formulation for $l_p$-Norm Optimization*,
  Journal of Optimization Theory and Applications 122 (2004), introduce and
  analyze the $L_p$ cone corresponding to (1), including its duality and an
  earlier self-concordant-barrier construction.  The grouped cone itself is
  therefore established prior art.
- [Chares](http://hdl.handle.net/2078.1/28538), *Cones and Interior-Point Algorithms for Structured Convex
  Optimization Involving Powers and Exponentials* (2009), Theorem 3.1.1,
  proves (6) with parameter three.  Section 4.1 identifies the general
  $\ell_p$-perspective cone (called an $l_p$-cone there), gives its scalar
  power-cone representation, and records parameter $3r$.  Chapter 5 proves
  exact partial minimization preserves the barrier parameter and develops the
  associated implicit Newton method.  Thus neither (7), (8), nor scalar-root
  elimination is claimed as a new construction.
- [Roy and Xiao](https://doi.org/10.1007/s11590-021-01748-7),
  *On Self-Concordant Barriers for Generalized Power Cones*,
  Optimization Letters 16 (2022), prove parameter $m+1$ for
  $\{(x,z):\prod_i x_i^{\alpha_i}\geq\|z\|_2\}$.  This specializes to a
  rigorous parameter-three barrier for the scalar power cone, but not to (1)
  unless $p=2$.  It does not prove Chares's separate numerical
  $3-2\min\{\alpha,1-\alpha\}$ conjecture for the scalar power cone.
- [Hildebrand](https://doi.org/10.1007/s10107-012-0576-1),
  *A Lower Bound on the Barrier Parameter of Barriers for Convex
  Cones*, Mathematical Programming 142 (2013), Corollaries 7.1--7.2, supplies
  $h(p)$.  The coupled-product amplification used in (4) is proved in the
  companion product-premium note.
- Chares and subsequent nonsymmetric-cone implementations emphasize that
  partial minimization can reduce artificial variables while keeping polynomial
  complexity.  Chares also gives the generic Schur-complement derivative formulas
  and explicitly observes arrow-shaped Hessians in a partially minimized example,
  so the arrowhead structure here should be viewed as a useful specialization, not
  by itself as a novelty claim.  Modern generalized-power-cone sparse-Hessian
  results concern the Euclidean-output cone and should not be silently transferred
  to (1).  The sources screened for this audit did not reveal an explicit
  sublinear-in-$r$ parameter barrier for the specific $\ell_p$-output cone (1);
  nor did they reveal the high-dimensional characteristic-barrier asymptotic
  (5d).  These are negative literature searches, not exhaustive nonexistence or
  novelty guarantees.

The surviving candidate new contributions are the high-dimensional
characteristic-family obstructions (5d) and (5m), and the combination of the
exact comparison (13) with the coupled group-product lower bound (4).  The
formulas (10)--(12) are a useful explicit specialization of the established
partial-minimization machinery.  Publishable novelty remains subject to
specialist review.

## Audit record

An independent hostile audit passed the dual scaling, the scalar-section and
coupled-product lower bounds, the canonical upper bound, the exact Lorentz case,
the bounded-simplex hypotheses of exact partial minimization, the multiplier and
Hessian-vector signs, the arrowhead-plus-rank-one decomposition, and every cap
and scalar-atom count in (13).  A follow-up audit separately passed the
high-dimensional section comparison (5b), including its product version for
arbitrary coupled barriers.  The audit caught and corrected the initial tree
count $3N$: the correct standard scalar-power parameter is
$3(N-1+k_t)$.  It also located Chares's prior generic arrow-Hessian discussion,
which is why the Newton specialization is not presented as a standalone novelty.
A second hostile audit checked the characteristic-family theorem independently:
the dual parametrization and Jacobian, exact integral, anisotropic exponent,
differentiated asymptotics, self-concordance inequality, strictness calculation,
and dual-characteristic transfer all passed.  It requested the explicit local,
compact-away, and coercive tail bounds now included before (5h).
The same audit passed the $p$-order comparator (5k)--(5m): the dual-ball
Jacobian, boundary-cap exponent, differentiated asymptotics, and the $r=2$
specialization are exact.  It also checked (5n) and narrowed its interpretation
to a comparison of necessary obstructions, not of the unknown actual
self-concordance thresholds.
