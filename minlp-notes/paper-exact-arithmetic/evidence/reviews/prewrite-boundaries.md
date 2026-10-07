# Prewriting review: degeneration, uncertainty, and certificate boundaries

Date: 2026-10-05. This internal review reconstructs the mathematical
boundaries in the coverage map. It introduces no general exact-comparison
upper bound for degenerate convex quartics and no lower bound for the size
of every rational positive semidefinite Gram matrix. No mathematical
experiment, retained computation script, literature search, manuscript
edit, historical-source edit, or CI inspection was performed.

The sources read were the
[coverage map](../coverage-map.md),
[degeneracy frontier](../../../research-20260928/algebra/degeneracy-frontier.md),
[equality frontier](../../../research-20260927/equality-frontier.md),
[succinct root penalties](../../../research-20260927/succinct-root-penalties.md),
[their earlier review](../../../research-20260927/root-penalty-review.md),
[nullvector compression caution](../../../research-20260927/rational-nullvector-compression-caution.md),
[all-PSD Gram frontier](../../../research-20260927/all-psd-gram-size-frontier.md),
and the relevant contracts in the
[all-scale core value theorem](../../../research-20261002/new-direction/all-scale-core-value-oracle.md),
[its earlier review](../../../research-20261002/reviews/all-scale-core-value-oracle-review.md),
and the
[selected-core theorem](../../../research-20261002/new-direction/core-only-noise-core-oracle.md).
The notation \(I\) below means total ordinary binary input length.

The main correction concerns the coverage map's item 12. The succinct
root-penalty theorem assumes explicitly expanded quadratic input and gives
a polynomial-size quadratic lift. It does not assume sparse input of
exponentially large binary degree. Eliminating its auxiliary chain creates
an exponentially large degree; its actual lift retains degree two but is
nonconvex. Either description falls outside the required global-convexity
contract of the strong-convexity exact-comparison theorem. The separate
sparse high-degree objective counterexample limits an extension of the
penalty theorem; it is not that theorem's input model.

The remaining propositions and examples below pass analytic reconstruction.
They distinguish fully vanishing curvature from partial degeneracy,
uncertain function data from exact rational coefficients, a selected
matrix's kernel from the feasible family's common kernel, and interior
Gram size from the size of every feasible positive semidefinite Gram.

**Proposition 1 (a fully zero Hessian gives rational linear recovery).**
Let \(f\in\mathbb Q[X_1,\ldots,X_n]\) have degree at most four
and be globally convex. Suppose a global minimizer \(p\) satisfies
\(\nabla^2f(p)=0\), meaning the whole Hessian matrix is zero.
Then
\[
 \operatorname{argmin}f=\{x:D^3f(x)=0\}.
\]
This is a nonempty rational affine space. A rational minimizer, its exact
minimum value, and a rational affine description of all minimizers can be
computed in polynomial bit time. A unique minimizer is rational with
polynomial coordinate bit length.

**Proof.** For fixed \(u,v\in\mathbb R^n\), global convexity makes
\(u^{\mathsf T}\nabla^2f(p+tv)u\) nonnegative for every real
\(t\). It is a polynomial of degree at most two and vanishes at
\(t=0\), so its linear coefficient is zero. Thus
\(D^3f(p)[u,u,v]=0\). Polarization in \(u\) gives
\(D^3f(p)=0\). Stationarity and exact Taylor expansion give
\[
 f(p+z)=f(p)+Q(z),\qquad
 Q(z)=\frac1{24}T[z,z,z,z],\qquad T=D^4f.
\]
Here \(T\) is a constant rational tensor, and \(Q\) is a convex,
nonnegative homogeneous quartic, possibly identically zero. Put
\[
 V=\{v:T[v,\cdot,\cdot,\cdot]=0\}.
\]
Since \(D^3f\) is affine and vanishes at \(p\), its solution set
is \(p+V\). Every \(v\in V\) has \(Q(v)=0\), so every
point of \(p+V\) is a minimizer.

Conversely, if \(Q(v)=0\), then \(Q(tv)=0\) for every real
\(t\). For \(0<\eta<1\), convexity and homogeneity give
\[
 Q(z+tv)
 \leq (1-\eta)Q\!\left(\frac z{1-\eta}\right)
       +\eta Q\!\left(\frac{tv}{\eta}\right)
 =(1-\eta)^{-3}Q(z).
\]
Let \(\eta\downarrow0\) and apply the resulting inequality in the
opposite direction. It follows that \(Q(z+tv)=Q(z)\) for all
\(z,t\). The directional derivative in \(v\) is zero, hence
\(T[v,z,z,z]=0\) for every \(z\). Polarization gives \(v\in V\).
Thus the zero set of \(Q\) is exactly \(V\), proving the assertion.

The tensor equations \(D^3f(x)=0\) are rational affine equations.
There are at most \(\binom{n+2}{3}=O(n^3)\) distinct rows and
their coefficient bit lengths are polynomial in the explicit input
length. Rational Gaussian elimination gives a rational particular
solution and a rational nullspace basis with polynomial bit length.
Evaluating the degree-at-most-four polynomial at that rational solution
gives the rational minimum value in polynomial bit time. This includes
the case \(T=0\): the assumptions then make \(f\) constant and
the solution space is all of \(\mathbb R^n\). \(\square\)

Within the class of globally convex inputs, the promise is recognizable.
Solve \(D^3f(x)=0\). If it is inconsistent, reject. Otherwise choose
a rational solution \(q\), and check
\(\nabla f(q)=0\) and \(\nabla^2f(q)=0\). Acceptance certifies
the stated situation, because stationarity of a globally convex function
gives a global minimum. If the promise holds, every solution lies in
\(p+V\), and the Taylor expression shows that its gradient and Hessian
are zero. This procedure does not itself recognize global convexity.

The proposition is about an unconstrained minimum and complete Hessian
vanishing. It cannot be applied merely because some Hessian eigenvalues
vanish, nor merely because the Hessian vanishes at a constrained optimum
with nonzero gradient.

**Example 2 (ordinary Newton can require too many refinement steps).**
For \(f(x)=x^4\), at every nonzero point,
\[
 N(x)=x-\frac{f'(x)}{f''(x)}=\frac23x.
\]
Starting from \(x_0=1\), achieving error at most \(2^{-2^s}\)
requires at least \(2^s/\log_2(3/2)\) iterations. Thus the ordinary
Newton iteration does not provide a polynomial number of steps for the
doubly exponential accuracy used in the exact-comparison circuit proof.
This is an iteration-count counterexample, not an arithmetic-circuit
lower bound: the exact minimizer is the trivial rational number zero.

**Example 3 (a partially degenerate optimizer has a discontinuous Newton
map).** Define the rational quartic
\[
 f(x,y)=(x^2+y^2)^2+xy^2+y^2
       =x^4+y^4+(2x^2+x+1)y^2.
\]
Since \(2x^2+x+1>0\), its unique zero and minimum is \((0,0)\).
Its Hessian is
\[
 H=
 \begin{pmatrix}
 12x^2+4y^2 &(8x+2)y\\
 (8x+2)y &4x^2+12y^2+2x+2
 \end{pmatrix},
\]
with determinant
\[
 24x^2(2x^2+x+1)
 +4y^2(24x^2-6x+1)+48y^4.
\]
Both quadratic factors are strictly positive: their discriminants are
\(-7\) and \(-60\). Away from the origin the leading diagonal
entry and determinant are positive, so \(H\succ0\). At the
origin \(H=\operatorname{diag}(0,2)\). Therefore \(f\) is
globally convex despite its partial degeneracy.

Inverting the displayed matrix at \((0,t)\), for \(t\ne0\), gives
\[
 N(0,t)=
 \left(\frac{1-2t^2}{2(1+12t^2)},
       \frac{t(16t^2-1)}{2(1+12t^2)}\right).
\]
This tends to \((1/2,0)\), rather than the minimizer, as \(t\to0\).
In particular, no sufficiently small ordinary Newton neighborhood is
invariant. Positive definiteness at every nearby nonoptimal point is
insufficient for the refinement argument.

The proposed correction \(T=3N\circ N-2N\) also fails quadratic
convergence. For a homogeneous quartic with invertible Hessian, Euler's
identity gives \(N(z)=2z/3\), and this correction would cancel that
linear error. In the present example the first Newton iterate has
\[
 x_1=\frac12-7t^2+O(t^4),\qquad
 y_1=-\frac12t+14t^3+O(t^5).
\]
At \((x,y)\) near \((1/2,0)\), direct rational expansion of the
Newton formulas gives
\[
 N_x(x,y)=\frac23x+\frac{13}{18}y^2
                   +O\!\left(|x-\tfrac12|y^2+y^4\right),
\]
and
\[
 N_y(x,y)=h(x)y+\frac16y^3
                   +O\!\left(|x-\tfrac12||y|^3+|y|^5\right),
 \quad
 h(x)=\frac{x(8x+2)}{6(2x^2+x+1)},
 \quad h(\tfrac12)=\frac14,\quad h'(\tfrac12)=\frac{11}{24}.
\]
Substitution gives
\[
 T(0,t)=
 \left(\frac{13}{24}t^2+O(t^4),
       \frac58t-\frac{51}{4}t^3+O(t^5)\right).
\]
Its norm is not \(O(t^2)\). The differentiability premise needed for
the proposed cancellation was absent. These calculations do not rule out
regularized, deflated, or higher-order methods.

**Example 4 (the Hessian kernel need not admit rational coordinates).**
Let
\[
 F(t,u,v)=t^4+2t^2-4t+(u-tv)^2+(u^2+v^2)^2.
\]
Let \(a\) be the unique real root of \(a^3+a-1=0\). The
univariate part has derivative \(4(t^3+t-1)\) and second derivative
\(12t^2+4>0\). The remaining terms are nonnegative, and the last
term vanishes only at \((u,v)=(0,0)\). Hence the unique minimizer
is \(p=(a,0,0)\).

Global convexity needs its own proof, since \((u-tv)^2\) is not
assumed convex. Set \(y=(u,v)\), \(r=\|y\|\), and \(b=(1,-t)\).
The Hessian blocks are
\[
 H_{tt}=12t^2+4+2v^2,
 \qquad H_{ty}=(-2v,-2u+4tv),
 \qquad H_{yy}=2bb^{\mathsf T}+4r^2I+8yy^{\mathsf T}.
\]
If \(r>0\), then \(H_{yy}\succeq4r^2I\succ0\) and
\(\|H_{ty}\|\leq(2+4|t|)r\). Therefore the Schur-complement
correction is at most
\[
 H_{ty}H_{yy}^{-1}H_{yt}
 \leq\frac{(2+4|t|)^2}{4}
 \leq2+8t^2.
\]
The Schur complement is at least \(4t^2+2+2v^2>0\), so the
Hessian is positive definite there. At \(r=0\), the cross block
is zero and both diagonal blocks are positive semidefinite. This proves
global convexity.

At the minimizer,
\[
 \ker\nabla^2F(p)=\operatorname{span}_{\mathbb R}\{(0,a,1)\}.
\]
The cubic has no rational root, so \(a\) is irrational. A nonzero
rational vector on this line would have rational nonzero third coordinate
\(c\) and rational second coordinate \(ca\), which would make
\(a\) rational. Thus the kernel has no nonzero rational vector. An
invertible rational change of variables cannot convert it into a
coordinate axis, because its inverse would then produce such a vector.
Approximate or algebraic coordinates are not excluded.

Quadratic regularization gives a valid value estimate but does not close
the exact-comparison frontier. If \(m=\min f\) is attained at
\(p\) with \(\|p\|\leq R\), set
\(f_\varepsilon(x)=f(x)+\varepsilon\|x\|^2\) and
\(m_\varepsilon=\min f_\varepsilon\), for \(\varepsilon>0\).
Then
\[
 0\leq m_\varepsilon-m\leq\varepsilon R^2.
\]
The lower bound follows from \(f_\varepsilon\geq f\); the upper
bound follows by evaluating at \(p\). The regularized objective is
coercive and strongly convex when \(f\) is globally convex and has a
finite attained minimum.

Even with a valid nonzero algebraic-gap bound
\(g=2^{-2^{a(I)}}\), choosing
\(\varepsilon\leq g/(8\max\{1,R^2\})\) need not be a
polynomial-size reduction to an explicit rational-coefficient theorem.
The printed denominator of such an \(\varepsilon\) can require
exponentially many bits. A repeated-squaring circuit for it changes the
input model. Moreover, the original warm-start and Newton-neighborhood
bounds depend on \(\log(1/\mu)\), with \(\mu=2\varepsilon\),
which can be exponential in the original input length. A short symbolic
coefficient alone supplies no new initialization argument.

Formal infinitesimals do not make ordinary Newton initialization
automatic. For \((x-1)^4+\varepsilon x^2\), ordinary Newton from
zero has, at every finite iteration, a rational-function expansion with
constant term
\[
 x_j(0)=1-(2/3)^j.
\]
This follows by setting \(\varepsilon=0\) in the recurrence; each
finite iterate remains different from one, so its Hessian denominator
has nonzero constant term. The true minimizer tends to one, for example
from \((p_\varepsilon-1)^4\leq\varepsilon\). Thus no finite
iterate has positive-order infinitesimal error relative to that minimizer.
This easy example is already covered by Proposition 1; it is a failure
of a proof route, not a hardness result. Equality also needs a gap shift:
the regularized minimum is positive for every \(\varepsilon>0\),
whereas the original minimum is zero.

The general exact-comparison upper bound for globally convex quartics
with partially degenerate minimizers remains open in these sources.
Failure of ordinary Newton, of the displayed acceleration, or of rational
kernel coordinates does not establish that such an upper bound is
impossible.

For uncertain equality data, the output contract is different. On a
compact domain \(K\), define
\[
 v(h)=\min\{f(x):x\in K,\ h(x)=0\}.
\]
If available information permits every equality map in a family
\(\mathcal H\), a uniformly justified upper bound must satisfy
\(U\geq\sup_{g\in\mathcal H}v(g)\). Every permitted map must
have a good feasible point, but those points may depend on the map. A
single point feasible for all maps is not required. This is a statement
about information uncertainty, not the complexity of exactly specified
rational input.

**Proposition 5 (a fixed uncertainty gap).** Let \(K=[-1,2]\),
\(f(x)=x\), \(h(x)=x^2(x-1)\), and
\(\mathcal H_\delta=\{g\in C(K):\|g-h\|_\infty\leq\delta\}\).
For \(0<\delta<2\), let \(r_\delta\in(1,2)\) solve
\(r_\delta^2(r_\delta-1)=\delta\). Every permitted map has a
root and
\[
 v(h)=0,\qquad
 \sup_{g\in\mathcal H_\delta}v(g)=r_\delta,
 \qquad r_\delta\longrightarrow1.
\]

**Proof.** The original roots are zero and one. The function \(h\)
is strictly increasing from zero to four on \([1,2]\), giving the
stated \(r_\delta\) and its limit. Every permitted \(g\) satisfies
\(g(-1)\leq-2+\delta<0\) and \(g(r_\delta)\geq0\).
The intermediate value theorem gives a root no greater than
\(r_\delta\). Conversely, \(g=h-\delta\) is negative on
\([-1,1]\) and has precisely the one root \(r_\delta\) on
\((1,2]\). It attains the supremum. \(\square\)

No positive-width uniform enclosure about this map justifies an upper
bound below one. Exact factorization immediately supplies the original
feasible point zero, so the example does not obstruct an exact symbolic
or mixed symbolic/numerical certificate. The lower obstruction persists
even if permitted perturbations are restricted to cubic polynomials with
the same positive-order derivatives: changing only the constant suffices.

**Proposition 6 (exponential uncertainty precision at a robust root).**
For \(k\geq1\), on \([-1,1]^{k+1}\) with variables ordered as
\((y_1,\ldots,y_k,x)\), set \(y_0=x\) and impose
\[
 y_i-y_{i-1}^2=0\quad(1\leq i\leq k),\qquad xy_k=a.
\]
Minimize \(x^2\). Write \(D=2^k+1\). For every \(|a|\leq1\)
there is exactly one real feasible point, and its value is
\[
 x=\operatorname{sgn}(a)|a|^{1/D},\qquad
 y_i=|a|^{2^i/D},\qquad v_k(a)=|a|^{2/D}.
\]
At \(a=0\), the isolated root has Jacobian rank \(k\) and local
Brouwer degree \(+1\). Every equation is quadratic with at most two
variables, and the interaction graph has treewidth at most two. If the
last constant is known only to lie in \([-\delta,\delta]\), with
\(0\leq\delta\leq1\), the least real-valued uniformly valid upper
bound is \(\delta^{2/D}\). At the actual input \(a=0\), achieving
upper-bound error at most \(\varepsilon\in(0,1)\) requires
\[
 \delta\leq\varepsilon^{D/2}.
\]
For an absolute uncertainty radius \(\delta=2^{-b}\), this is
\(b\geq(D/2)\log_2(1/\varepsilon)\).

**Proof.** The chain gives \(y_i=x^{2^i}\), and its last equation
is \(x^D=a\). Since \(D\) is odd, the real solution is unique
and has the stated coordinates, all within the box. At zero the first
\(k\) Jacobian rows have the identity in the \(y\) columns and
the last row is zero, giving rank \(k\).

Let \(G\) denote the equality map at \(a=0\). Its only real zero
is the origin. A small nonzero target \((0,\ldots,0,a)\) has the
one preimage above. The first \(k\) derivative rows have a triangular
\(y\)-block of determinant one. Eliminating that block leaves the
derivative of \(x^D\), so at the preimage
\[
 \det DG=D x^{D-1}>0.
\]
On the boundary of a small closed ball about zero, the norm of \(G\)
has a positive minimum. Small target translations preserve the degree,
and the regular-value formula gives \(+1\). The same boundary margin
and homotopy invariance show that every sufficiently small continuous
perturbation of all equality components has a zero in that ball. No
dimension-independent robustness margin or uniqueness under arbitrary
perturbation is claimed.

The graph is the path \(x-y_1-\cdots-y_k\) with closing edge
\(y_k-x\). For \(k\geq2\), the bags
\(\{x,y_i,y_{i+1}\}\), \(1\leq i<k\), give a width-two tree
decomposition. For \(k=1\), its one edge has width one. Taking the
supremum of \(|a|^{2/D}\) over the permitted interval gives
\(\delta^{2/D}\), attained at its endpoints. Comparing that value
with \(\varepsilon\) gives the precision formulas. \(\square\)

The exponential dependence is on chain length, or number of variables;
ordinary indexed sparse input also includes variable-index bits. The
bound measures a specified absolute uncertainty radius. It is not a
universal mantissa-length or running-time lower bound. If the checker
requires rational bounds, \(\delta^{2/D}\) is their infimum and is
attained exactly when it is rational. For two-sided estimation, the
minimax absolute error is half the value range; a certified upper bound
has the full-range requirement at the central actual input.

All positive-order derivatives are independent of \(a\), so exact
derivative data do not resolve the uncertain constant. Exact knowledge
that \(a=0\) does: the origin is an immediate rational certificate.
Robust existence also does not imply robust uniqueness. Replacing the
first equality by \(y_1-x^2=-\eta\), with \(0<\eta<1\), gives
three solutions with \(x=0,\sqrt\eta,-\sqrt\eta\); they approach
zero as \(\eta\downarrow0\). The corresponding first coordinates
are \(-\eta,0,0\), respectively, with later coordinates obtained
by squaring. This does not contradict the degree argument.

The succinct fractional penalty is a representation result with a
different input contract. Its algebra and encoding reconstruct as follows.
Let \(X\) be a compact native domain described by explicitly expanded
rational quadratic equalities, weak inequalities, and finite variable
bounds, with bounded integer coordinates allowed. Let \(f\) be an
explicit rational quadratic, and let a nonempty subset \(S\) be
defined by additional quadratic equalities and weak inequalities. Define
\(V\) as the maximum of zero, the positive inequality residuals, and
the absolute equality residuals. Termwise box estimates give positive
integers \(H,B\), of polynomial bit length, with
\(V\leq H\) and \(|f|\leq B\). Put \(R=V/H\in[0,1]\).

The imported effective facts are coefficient-sensitive one-block real
quantifier elimination and the effective semialgebraic inequality:
continuous nonnegative functions on a compact rational semialgebraic set,
with \(h=0\Rightarrow g=0\), admit \(g^q\leq Ch\). For
description degree \(d\), coefficient bit bound \(\tau\), and
ambient dimension \(r\), the bounds used here are
\(q\leq(8d)^{2(r+7)}\) and
\(\log_2\max\{1,C\}\leq\tau d^{O(r^2)}\). The earlier
root-penalty review records the precise primary-source contracts. This
review does not retrieve or newly verify those external sources; the
manuscript's literature audit must provide their vetted citations.

For each bounded integer coordinate, encode its finite interval by
\(z=\ell+\sum_j2^jb_j\), \(b_j(1-b_j)=0\), and
\(0\leq b_j\leq1\), retaining its upper bound to exclude surplus
codes. Integral ceiling and floor of the original bounds give \(\ell\)
and the upper endpoint. Polynomially many bits suffice; a singleton
interval needs none. The resulting real quadratic lift \(X'\) is
compact, has polynomial input length, and projects exactly onto \(X\).
Write \(S'\) for the corresponding feasible lift.

Let \(v=\min_S f\). Avoid using this unknown algebraic value as a
coefficient by defining
\[
 T=\{t\in[-B,B]:\neg\exists y\in S'\text{ with }f(y)<t\}
   =[-B,v].
\]
One-block elimination supplies a quantifier-free rational description
of \(T\) whose degrees and coefficient bit lengths are at most
\(2^{\operatorname{poly}(I)}\). The potentially long description
is used only to prove bounds, not printed as part of the final lift.
On \(A=X'\times T\), define
\(g(w,t)=\max\{0,t-f(w)\}\) and \(h(w,t)=R(w)\).
Their graphs have rational semialgebraic descriptions with the same
parameter bounds, and \(h=0\Rightarrow g=0\). The effective
inequality therefore gives
\[
 g^q\leq Ch,\qquad q\leq2^{a(I)},\qquad
 \log_2\max\{1,C\}\leq2^{a(I)}
\]
for a universal polynomial \(a\). Increase \(C\) to at least one.
Choose an integer-valued polynomial \(p\) large enough that
\(\alpha=2^{-p(I)}\) satisfies \(\alpha q\leq1\) and
\(\alpha\log_2C\leq1\). Since \(g\leq2B\), interpolation
between its two upper bounds gives
\[
 g\leq\min\{2B,C^{1/q}h^{1/q}\}
 \leq(2B)^{1-\alpha q}C^\alpha h^\alpha
 \leq4B h^\alpha.
\]
The assertion at \(h=0\) follows from the zero-set implication.
Taking \(t=v\) yields
\[
 f(x)+(4B+1)R(x)^\alpha\geq v+R(x)^\alpha.
\]
Every infeasible point is strictly worse than \(v\), and every
original feasible minimizer attains it. Thus the value and minimizer
set agree exactly.

The rational exponent \(\alpha=1/2^{p(I)}\) has polynomial binary
length. Introduce \(s_0,\ldots,s_{p(I)}\in[0,1]\), impose
\[
 s_{j+1}=s_j^2\quad(0\leq j<p(I)),\qquad
 Hs_{p(I)}\geq V(x),
\]
and minimize \(f(x)+(4B+1)s_0\). The last inequality means one
quadratic inequality for each signed residual; no maximum variable is
needed. For fixed \(x\), the smallest feasible \(s_0\) is exactly
\(R(x)^{1/2^{p(I)}}\). The lift has polynomially many variables
and quadratic constraints of polynomial coefficient bit length. Its
constants are effective but have not been evaluated for numerical use
in the sources. No efficient optimization algorithm follows.

The nonconvex equalities are essential. Replacing them by
\(s_{j+1}\geq s_j^2\) permits
\(s_0=\cdots=s_{p(I)-1}=0\), \(s_{p(I)}=R(x)\), and hence
zero penalty at an infeasible point. Eliminating the exact chain instead
produces \(s_0^{2^{p(I)}}\geq R(x)\), with exponentially large
numerical degree. The original theorem has small explicit input degree;
the eliminated formulation has a different degree model.

Three elementary boundaries support this distinction. First, on the
native quadratic curve \(x_{i+1}=x_i^2\), \(0\leq x_i\leq1\),
with objective \(-x_0\) and additional equality \(x_k=0\), a
penalty \(\rho|x_k|^\alpha\) becomes
\(-s+\rho s^{\alpha2^k}\). If \(\alpha2^k>1\), it is negative
for small positive \(s\), for every finite \(\rho\). Hence
exactness requires \(0<\alpha\leq2^{-k}\); with \(\rho>1\)
this condition also suffices. At \(\alpha=2^{-k}\), \(\rho=1\)
preserves value but makes every point tie, losing minimizer-set exactness.

Second, take native \(z\in\{0,1\}\), \(y_0=1/2\), and
\(y_{i+1}=y_i^2\), minimizing \(-z\), with additional equality
\(zy_k=0\). The infeasible point has residual \(2^{-2^k}\),
so minimizer-set exactness is precisely
\(\rho>2^{\alpha2^k}\). A fixed positive exponent requires many
printed coefficient bits; an exponent of order \(2^{-k}\) makes
a constant coefficient possible. All native equations remain quadratic.

Third, in the first curve at \(x_0=1/2\), the residual is
\(r=2^{-2^k}\). In a root lift of depth at least \(k\), set
all auxiliaries except the last to zero and set the last to \(r\).
Only the last lift equality fails, by absolute error \(r\); the
residual inequality holds. A tolerance at least \(r\) accepts zero
penalty and objective \(-1/2\), despite the exact augmented minimum
zero. A short exact lift can therefore be badly conditioned for approximate
feasibility tests.

The separate sparse high-degree counterexample uses objective
\(x^{2^k}\) on \([1,2]\), with additional constraint \(x\geq2\).
At \(x=1\), the unscaled violation \([2-x]_+\) is one for
every exponent, while the objective deficit is \(2^{2^k}-1\).
The coefficient must therefore be at least this deficit for value
exactness, and strictly larger to exclude a tie there. This shows why
the penalty theorem needs its explicit quadratic objective-range bound.
It does not show that the theorem itself allows exponentially large
binary input degree.

**Proposition 7 (one selected nullvector does not justify rational
feasibility preservation).** There is a rational affine semidefinite
family with a rational positive definite feasible matrix such that
restriction to a rational nullvector of another feasible matrix leaves
real feasibility but destroys all rational feasible matrices.

**Proof.** Define the rational affine pencil
\[
 A(x)=
 \begin{pmatrix}2&x\\x&1\end{pmatrix}
 \oplus
 \begin{pmatrix}x&1&0\\1&x&1\\0&1&x\end{pmatrix}.
\]
The first block is positive semidefinite exactly for \(|x|\leq\sqrt2\).
The second block has eigenvalues \(x-\sqrt2,x,x+\sqrt2\), so it
is positive semidefinite exactly for \(x\geq\sqrt2\). Therefore
\(A(x)\succeq0\) exactly when \(x=\sqrt2\).

Now take the rational affine six-by-six family
\[
 X(t,x)=\operatorname{diag}(t,A(x)+tI_5).
\]
The matrix \(X(2,0)\) has rational entries and positive eigenvalues
\(2,4,3,2-\sqrt2,2,2+\sqrt2\). In contrast,
\(X(0,\sqrt2)\) is feasible and kills the rational vector \(e_1\).
Restricting the affine family to matrices that kill \(e_1\) forces
\(t=0\). The remaining feasibility condition then forces
\(x=\sqrt2\), so every restricted feasible matrix has irrational
entries. Real feasibility survives; rational feasibility does not.
\(\square\)

Here compression means a face restriction imposing \(Xe_1=0\),
with the original affine equations retained. Merely deleting the first
principal row and column while allowing \(t\) to remain free is a
different operation and is not the counterexample's restricted problem.
The original feasible matrix was not of maximum feasible rank.

A common rational nullvector does justify preservation. If every
feasible \(X\) kills a rational nonzero vector \(v\), choose a
rational full-column-rank matrix \(U\) spanning \(v^\perp\) and
a rational left inverse \(C\). Every such symmetric \(X\) has
\[
 X=UYU^{\mathsf T},\qquad Y=CXC^{\mathsf T}.
\]
Positive semidefiniteness and rationality pass in both directions. Thus
this rational change of coordinates preserves the full feasible family
and its rational points.

A nullvector of a maximum-rank feasible matrix is common. For positive
semidefinite \(G_0,G\),
\(\ker(G_0+G)=\ker G_0\cap\ker G\), since a zero sum of their
nonnegative quadratic forms makes each matrix kill the vector. If a
feasible \(G\) failed to kill a vector in \(\ker G_0\), their
feasible midpoint would have larger rank than \(G_0\). Consequently
a maximum-rank feasible matrix has exactly the common kernel. A rational
vector in that kernel can be used for rational compression. Maximum
rank alone does not produce a rational basis of an irrational kernel
or an algorithm for finding it.

This is a counterexample to an overly broad restriction principle. This
review has not independently examined the external book version cited
in the historical note, so the manuscript should present the mathematical
safeguard without a new claim about that source's wording. It does not
invalidate facial reduction procedures that establish a common kernel.

The all-PSD Gram-size frontier remains unresolved in the stated strict
quartic class. A tiny positive minimum can force long entries in every
interior rational polynomial Gram while a short singular rational Gram
still exists. In the recorded family, the displayed identity
\(f_k=\lambda\sum_jq_j^2+u^2\) supplies a short rational Gram
directly. Interior determinant arguments require a positive determinant;
a singular Gram has determinant zero and escapes that rational separation
step. Small eigenvalues therefore do not by themselves lower-bound the
encoding of every positive semidefinite Gram.

One direct penalty transfer also fails analytically. Let
\(q_i(y)=y_i^2-y_{i+1}\) for \(i<m\), \(q_m(y)=y_m^2\),
and \(g(y)=\epsilon-y_1\), where \(0<\epsilon<1/2\).
At the rational point \(a_i=(2\epsilon)^{2^{i-1}}\), all chain
residuals except the last vanish, and
\[
 \left(\lambda\sum_iq_i^2+g\right)(a)
   =\lambda(2\epsilon)^{2^{m+1}}-\epsilon.
\]
Even nonnegativity requires
\(\lambda\geq\epsilon(2\epsilon)^{-2^{m+1}}\). At
\(\epsilon=1/4\), this is \(2^{2^{m+1}-2}\). The coefficient
of \(y_m^4\) in the expanded quartic is exactly \(\lambda\),
so this proposed transfer already has exponentially many input coefficient
bits in chain length. It cannot prove a large-output theorem for short
explicit quartic input. Taking a short circuit for \(\lambda\) again
changes the input model. This does not exclude other embeddings.

Restrictions to interior Grams, maximal-rank Grams, exposing matrices,
separated-block certificates, or algebraic coefficient fields are
different output contracts. Their proved obstructions do not settle
the existence of a short unrestricted singular rational Gram. The open
question here is a lower bound for every expanded rational positive
semidefinite polynomial Gram of a short strictly positive quartic under
the given strict Hessian-certificate assumptions.

The coverage map's item 9 does not restore the older two-dimensional cap.
The all-scale core-value theorem uses a weak \(1/T\) tail for a single
scale-uniform count proxy in every core dimension, rather than a product
of directional growth constants. Its ball-covering estimate is independent
of absolute continuity of the auxiliary measure: disjoint balls with
\(\mu(B(c,r))>Tr^k/C\), followed by their fivefold enlargements,
give \(\operatorname{Leb}\{A>T\}\leq C'/T\) on a bounded
noise box. Truncation at a base-computable cap makes the logarithmic
integral of this weak tail finite, and the finite-noise transfer and exact
fallback control every accuracy query under the same draw. There is no
\(k\leq2\) restriction in that source's final theorem.

This paragraph checks the relevant boundary and the source contract;
it is not a fresh proof audit of the full finite-grid value theorem.
That theorem returns feasible rational value intervals, with no distance
guarantee for residual coordinates. The selected-core continuation adds
distance to one fixed lexicographically selected optimal core, while
residual witnesses still carry only objective-gap accuracy. Neither
contract supplies a general full-optimizer completion theorem in degree
four. Any full-point claim needs the separate globally convex or cubic
recourse arguments and their stated selector, face, and margin hypotheses.

The results appropriate for a supporting appendix are Proposition 1,
the three explicit Newton/kernel examples, Propositions 5 and 6 with
their information model, and Proposition 7 with the common-kernel repair.
The penalty discussion is a concise representation-model comparison,
conditional on the vetted effective semialgebraic theorems. The general
partially degenerate exact-comparison upper bound, unrestricted all-PSD
Gram size, and general degree-four full-point completion are not resolved
by these examples. The full-point frontier should retain any additional
restricted positive cases proved elsewhere in the manuscript.

Verification was analytical: matrix determinants, Newton expansions,
Schur-complement estimates, power-chain elimination, and penalty inequalities
were rederived without executing mathematical code. A document-only Python
check of this owned review's final newline, whitespace, control characters,
paired math delimiters outside fenced code, and relative local links was
run successfully. No project-wide check or CI result is claimed.

The targeted command, run from the repository root, was:

```text
python - <<'PY'
from pathlib import Path
import re
p = Path('paper-exact-arithmetic/evidence/reviews/prewrite-boundaries.md')
s = p.read_text()
assert s.endswith('\n')
assert not any(line.rstrip() != line for line in s.splitlines())
assert all(ord(c) >= 32 or c in '\n\t' for c in s)
prose = re.sub(r'```.*?```', '', s, flags=re.S)
assert prose.count(r'\(') == prose.count(r'\)')
assert prose.count(r'\[') == prose.count(r'\]')
links = re.findall(r'\]\(([^)]+)\)', prose)
for target in links:
    assert (p.parent / target).resolve().is_file(), target
print(f'Boundary review text checks passed; {len(links)} local links resolve.')
PY
```
