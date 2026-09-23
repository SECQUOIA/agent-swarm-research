# A constant-barrier sparse LP optimal-value separation

Status: Proved; algebraically cross-checked and independently audited  
Started: 2026-09-04  
Paper status: Not incorporated  
Confidence: High on the reduction; moderate-low on novelty because the affine slice is one-dimensional

## Result

The cyclic Forrelation inverse family admits a particularly direct LP
wrapper. Let \(M,e,a,R,p,\delta,K,q,r,\ell\) be as in
[the parameterized scalar-frontier note](2026-09-04-parameterized-one-cone-scalar-frontier.md),
so

\[
 \|M\|=1,\qquad \sigma_{\min}(M)=K^{-1},\qquad
 \|a\|=R^{-1},\qquad
 a^TM^{-1}e=\sqrt p\,\Phi,
\]

with \(p=\Theta(\delta^2)\),

\[
 R=\sqrt{K\frac{1+\gamma^{3T}}{1-\gamma^{3T}}}=\Theta(\sqrt K),
 \qquad
 \ell=\frac{\log(1/\delta)}{3\alpha_K}+O(1),
 \quad
 \alpha_K=\log\frac{K+1}{K-1}.
\]

Define the unit objective vector \(\bar a=Ra\), and consider the LP

\[
 \boxed{
 \begin{aligned}
  \max_{x,t}\quad &\bar a^Tx\\
  \text{s.t.}\quad&Mx=te,\\
                  &-1\leq t\leq1.
 \end{aligned}}                                           \tag{1}
\]

Equation (1) is the eliminated notation. To make the objective literally
one-sparse, retain a public accumulator chain as in (13) of the companion
note, but multiply its coefficients by \(R\), so that its final coordinate
obeys

\[
 \bar w=(Ra)^Tx=\bar a^Tx.
\]

Maximize the single variable \(\bar w\). This adds only public
three-sparse equality rows, makes the objective coefficient vector a unit
basis vector, and leaves the feasible projection and optimal value
unchanged. Thus the sparsity statement below also holds under conventions
that count objective support, not only constraint-matrix sparsity.

The exact optimal value is

\[
 \boxed{
 \operatorname{OPT}=R\sqrt p\,|\Phi|
 =\Theta(\sqrt K\,\delta)\,|\Phi|.}                       \tag{2}
\]

Consequently, under the 2-Forrelation promise

\[
 |\Phi|\leq\alpha=1/100
 \quad\text{or}\quad
 \Phi\geq\beta=3/5,
\]

additive optimal-value accuracy \(c\sqrt K\,\delta\) decides the promise.
Every bounded-error classical full-SQ algorithm achieving this accuracy
uses

\[
 \boxed{
 Q=\Omega\!\left(\frac{q^{\ell/2}}{r\ell}\right)
 =\exp\!\left(\Omega(K\log s\log(1/\delta))\right)}        \tag{3}
\]

up to the displayed polynomial and rounding factors. Here \(s=\Theta(q)\)
is row/column sparsity. The structured quantum Forrelation algorithm
estimates (2) with \(O(1)\) hidden queries.

For fixed \(k\)-Forrelation, \(T=(k+1)\ell+O(k)\), the value gap is
\(2^{-O(k)}\sqrt K\,\delta\), and the classical lower bound is

\[
 \boxed{
 Q=\Omega_k\!\left[
  \left(\frac{q^\ell}{r\ell}\right)^{1-1/k}
 \right]
 =\widetilde\Omega_k(N^{1-1/k}).}                         \tag{4}
\]

The coherent source algorithm uses \(2^{O(k)}\) hidden queries. Thus, for
each fixed \(k\), (1) gives an ordinary optimal-value separation that is
arbitrarily close to linear in ambient dimension.

## Proof of the value identity

Because \(M\) is invertible, every feasible point of (1) is uniquely
parameterized by

\[
 x=tM^{-1}e,\qquad -1\leq t\leq1.
\]

Its objective is

\[
 \bar a^Tx
 =tR a^TM^{-1}e
 =tR\sqrt p\,\Phi.
\]

Maximization over the interval chooses the sign of \(t\), proving (2).
The objective is normalized:

\[
 \|\bar a\|=R\|a\|=1.
\]

Thus the gap in (2) is not produced by an arbitrary rescaling of the
objective.

## Sparse full-SQ access and conditioning

Write the equality matrix as

\[
 A_{\rm eq}=[M\; -e].                                    \tag{5}
\]

Every row and column has \(O(q)\) nonzeros. The extra \(t\)-column has one
nonzero, and only the row indexed by \(e\) changes norm. All row and column
norms and mixture weights are public. A sparse-value or location query to
\(A_{\rm eq}\) uses at most one hidden sign query, while the right-hand side
is zero. The unit vector \(\bar a\) has one public coordinate at each hold
clock time and has an exact public SQ interface. Hence full SQ access to
the entire LP input has constant hidden-query overhead.

In the literal-coordinate formulation, the accumulator rows are public and
three-sparse and the objective is one-sparse. Equation (7) concerns the
core equality operator \([M\;-e]\); no condition-number claim is made for
an unreduced augmented KKT matrix containing the free accumulator
equalities.

The equality operator retains the intended conditioning. Since

\[
 A_{\rm eq}A_{\rm eq}^T=MM^T+ee^T,
\]

\[
 K^{-2}I\preceq A_{\rm eq}A_{\rm eq}^T\preceq2I.          \tag{6}
\]

Moreover, the \(K^{-2}\)-eigenspace of \(MM^T\) has data-register
multiplicity \(2^n\). One can choose a vector in that eigenspace orthogonal
to \(e\), on which the rank-one term in (6) vanishes. Therefore

\[
 \sigma_{\min}(A_{\rm eq})=K^{-1},\qquad
 K\leq\kappa(A_{\rm eq})\leq\sqrt2K.                     \tag{7}
\]

The row/column sparsity remains \(s=\Theta(q)\).

## Accuracy parameterization

If the requested additive value accuracy is \(\varepsilon\), choose

\[
 \delta=\Theta(\varepsilon/\sqrt K)
\]

within the small-\(\delta\) regime. Then

\[
 \ell
 =\frac{\log(\sqrt K/\varepsilon)}{3\alpha_K}+O(1),
\]

and the exact lower bound is again (3) with this value of \(\ell\). Up to
the explicit polynomial term, it reads

\[
 Q=\exp\!\left(
  \Omega\!\left(K\log s\log\frac{\sqrt K}{\varepsilon}\right)
 \right).                                                 \tag{8}
\]

The same substitution with denominator \((k+1)\alpha_K\) applies to (4).

An especially clean regime is constant absolute value accuracy. Set

\[
 \delta=\Theta(K^{-1/2}).
\]

Then the promise gap in (2) is a fixed constant, while

\[
 \ell=\Theta(K\log K).
\]

Consequently, for fixed sparsity base \(q>1\),

\[
 \boxed{
 Q=\exp\!\left(\Omega(K\log s\log K)\right)}               \tag{8a}
\]

for constant-error classical LP value approximation. The fixed-\(k\)
version retains \(\widetilde\Omega_k(N^{1-1/k})\) hardness at the same
constant output accuracy, whereas the structured quantum source algorithm
still uses \(2^{O(k)}\) hidden queries.

## Barrier interpretation and limitation

The relative interior of (1) is the interval \(|t|<1\). Its paired
logarithmic barrier

\[
 \phi(t)=-\log(1-t^2)
\]

has self-concordance parameter one. Indeed,

\[
 \phi'(t)=\frac{2t}{1-t^2},\qquad
 \phi''(t)=\frac{2(1+t^2)}{(1-t^2)^2},\qquad
 \phi'''(t)=\frac{4t(3+t^2)}{(1-t^2)^3}.
\]

Thus \((\phi')^2/\phi''=2t^2/(1+t^2)\leq1\), and
\(|\phi'''|\leq2(\phi'')^{3/2}\); after squaring, the latter reduces to
\((1-t^2)^2(t^2+2)\geq0\). Hence parameter one is proved for the restricted
one-dimensional barrier, rather than inferred from the generic additive
parameter two of the separate logarithms. At the analytic center
\(t=0,x=0\),
the tangent space to the equalities is

\[
 \{(dx,dt):Mdx=e\,dt\}
 =\operatorname{span}\{(M^{-1}e,1)\}.                    \tag{9}
\]

Thus the unique null direction itself contains the hard inverse history.
The theorem does not separately lower-bound nullspace-basis construction:
an explicit dense output already has linear output cost, while an SQ basis
would require its own output contract. The construction has constant barrier
parameter and only two scalar inequalities.

The same observation gives an exact Newton-decrement identity. On the
tangent coordinate \(t\), the barrier Hessian at the analytic center is
two, while the projected objective coefficient is

\[
 \bar a^TM^{-1}e=R\sqrt p\,\Phi.
\]

Therefore, for objective multiplier \(\eta\),

\[
 \boxed{
 \Lambda_\eta^2
 =\frac{\eta^2}{2}R^2p\,\Phi^2
 =\frac{\eta^2}{2}\operatorname{OPT}^2.}                 \tag{10}
\]

Estimating this squared decrement to additive accuracy
\(2^{-O(k)}\eta^2K\delta^2\) has lower bounds (3) and (4). In particular,
with \(\delta=\Theta(K^{-1/2})\) and fixed \(\eta\), constant-additive-error
decrement estimation requires
\(\exp(\Omega(K\log s\log K))\) classical full-SQ queries. The structured
quantum source algorithm uses \(2^{O(k)}\) hidden queries.

Unlike the direct reduced-Hessian result in the companion note, this claim
does not hand the projected scalar right-hand side to the algorithm: doing
so would reveal the hard quantity. Its content is that projecting the unit
objective through the sparse equality constraints, a standard
equality-constrained IPM preprocessing step, is classically hard in the SQ
model.

This strength comes with an important boundary. The feasible affine slice
is one-dimensional and has \(N\) equality constraints. If an explicit
nullspace basis for (5), together with its objective projection, is supplied
as extra input, the LP reduces immediately to a scalar interval problem. The
theorem therefore isolates hardness of sparse equality/nullspace
preprocessing in the matched SQ access model; it is not an iteration lower
bound caused by high-dimensional barrier geometry.

The reduction is also close in spirit to
[Montanaro--Shao's sparse matrix-function entry lower
bounds](https://arxiv.org/abs/2311.06999) and to the underlying
Grønlund--Larsen/Forrelation inverse family. Moreover,
[Apers--Gribling, Lemma 8.5](https://arxiv.org/abs/2311.03215) already proves
an \(\Omega(n)\) classical lower bound for constant-error LP optimal-value
approximation even with full SQ access. Therefore this is not the first
full-SQ LP value lower bound. The potentially new content is the simultaneous
explicit \((K,s,\varepsilon)\) frontier, constant-hidden-query structured
quantum side, unit-objective affine-slice wrapper, and barrier parameter one.
Priority has not been established.

The matching classical scalar upper bound is recorded separately in
[the affine-slice SQ upper note](2026-09-04-sparse-sq-affine-lp-value-upper.md).
It uses the public clock norm
\(R=\|M^{-1}e\|=\Theta(\sqrt K)\) and estimates
\(|\bar a^TM^{-1}e|\) in dimension-independent time with exponential part

\[
 \exp\!\left(
 O\!\left(K\log(s+1)\log\frac{\sqrt K}{\varepsilon}\right)
 \right),
\]

matching (8) up to constants in the exponent.  This does not construct the
hard null direction or an explicit optimizer.
