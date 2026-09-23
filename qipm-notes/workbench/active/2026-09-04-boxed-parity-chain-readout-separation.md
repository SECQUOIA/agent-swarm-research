# A one-barrier sparse parity chain separates normalized Newton states from readout

Status: Proved candidate; independently hostile-audited  
Started: 2026-09-04  
Paper status: Not incorporated  
Confidence: High on the algebra, query reduction, and conditioning; moderate-low
on novelty pending a specialist literature review

## Main result

Let \(N\geq 1\), let hidden signs
\(\sigma_1,\ldots,\sigma_N\in\{-1,+1\}\), and put

\[
 s_0=1,\qquad s_m=\prod_{j=1}^m\sigma_j,\qquad s=s_N.
\]

Consider the equality-constrained convex program

\[
 \boxed{
 \begin{aligned}
  \operatorname*{maximize}_{r_0,\ldots,r_N}\quad&r_0+2r_N,\\
  \text{subject to}\quad&r_m-\sigma_m r_{m-1}=0
       &&(m=1,\ldots,N),\\
  &-1\leq r_0\leq1.
 \end{aligned}}                                                   \tag{1}
\]

The intermediate variables are **free**: only \(r_0\) is boxed.  The
equalities imply \(r_m=s_m\alpha\), where \(\alpha=r_0\), so the feasible
set is a compact line segment and

\[
             (r_0+2r_N)=(1+2s)\alpha.
\]

Consequently

\[
 \boxed{\operatorname{OPT}_\sigma=
 \begin{cases}3,&s=+1,\\1,&s=-1,
 \end{cases}\qquad
 \alpha^*=\begin{cases}+1,&s=+1,\\-1,&s=-1.
 \end{cases}}                                                     \tag{2}
\]

Thus a multiplicative estimate \(\widehat V\) satisfying

\[
       |\widehat V-\operatorname{OPT}_\sigma|
          \leq\gamma\operatorname{OPT}_\sigma,
          \qquad \gamma<\tfrac12,                                \tag{3}
\]

determines the parity \(s\).  The optimum is positive in both cases, so
(3) is an unambiguous relative-error convention.  In the raw-sign,
sparse-coefficient, coherent sparse-row, or full sample-and-query input
models specified below, bounded-error quantum and randomized algorithms
therefore require

\[
                              \boxed{\Theta(N)}                    \tag{4}
\]

input queries.  The quantum lower bound is the ordinary approximate-degree
lower bound for parity (a \(T\)-query acceptance probability has degree at
most \(2T\)); the upper bound reads all signs.

Yet the feasible slice is one dimensional, its displayed barrier has exact
self-concordance parameter one, and every normalized **reduced-coordinate**
optimizer, central point, and predictor is the same one-dimensional quantum
state.  Preparing that state requires no input query.  What is hard is its
discarded classical sign or scale, equivalently the effective reduced
objective coefficient \(1+2s\).  This is a clean state/readout separation,
not a claim that the equality elimination itself is free.

The original-variable KKT graph is an alternating path of treewidth one.
At any fixed central parameter bounded away from the boundary its condition
number is \(\Theta(N)\), and classical forward elimination costs \(O(N)\).
The query, movement, and solve statements are simultaneous statements and
must not be multiplied.

## 1. Exact parameter-one barrier

The relative interior of the feasible affine line is \(|\alpha|<1\).  Pull
back the paired logarithmic barrier to that line:

\[
                         \phi(\alpha)=-\log(1-\alpha^2).           \tag{5}
\]

Its derivatives are

\[
 \phi'(\alpha)={2\alpha\over1-\alpha^2},\qquad
 \phi''(\alpha)={2(1+\alpha^2)\over(1-\alpha^2)^2},\qquad
 \phi'''(\alpha)={4\alpha(3+\alpha^2)\over(1-\alpha^2)^3}.
\]

The usual one-dimensional self-concordance inequality holds because

\[
 {\phi'''(\alpha)^2\over4\phi''(\alpha)^3}
 = {\alpha^2(3+\alpha^2)^2\over2(1+\alpha^2)^3}\leq1.
\]

Indeed, after putting \(x=\alpha^2\), the nonnegative difference is
\(2(1+x)^3-x(3+x)^2=(1-x)^2(x+2)\).  Moreover,

\[
 {\phi'(\alpha)^2\over\phi''(\alpha)}
       ={2\alpha^2\over1+\alpha^2}<1,
 \qquad
 \sup_{|\alpha|<1}{\phi'(\alpha)^2\over\phi''(\alpha)}=1.         \tag{6}
\]

Hence the smallest barrier parameter of (5) is exactly

\[
                              \boxed{\nu=1}.                      \tag{7}
\]

This claim is relative to the equality-defined affine hull, as is standard
for equality-constrained Newton steps.  The function (5), viewed on
\((-1,1)\times\mathbb R^N\) before imposing the equalities, has a singular
Hessian and is not asserted to be a full-dimensional barrier there.

It is essential that (1) boxes only \(r_0\).  If every \(r_m\) were given
its own copy of \([-1,1]\), the restricted barrier would be
\(-(N+1)\log(1-\alpha^2)\), with exact parameter \(N+1\); the corresponding
diagonal-Hessian saddle system has condition number \(\Theta(N^2)\) at a
fixed center.  That is a different construction.

## 2. Exact central path and a constant fixed-center gap

Let

\[
                 c_s=1+2s\in\{3,-1\},\qquad
 \rho(z)={z\over1+\sqrt{1+z^2}}.
\]

At objective multiplier \(\eta\geq0\), the reduced centering problem is

\[
             \min_{|\alpha|<1}\;\phi(\alpha)-\eta c_s\alpha.
\]

Stationarity gives

\[
 {2\alpha\over1-\alpha^2}=\eta c_s,
 \qquad
 \boxed{\alpha_s(\eta)=\rho(\eta c_s)},
 \qquad
 r_m(\eta)=s_m\alpha_s(\eta).                                   \tag{8}
\]

Already at the public fixed multiplier \(\eta=1\), the primal objective
at the exact center has the two constant values

\[
 J_+=3\rho(3)=\sqrt{10}-1,
 \qquad
 J_-=(-1)\rho(-1)=\rho(1)=\sqrt2-1.                              \tag{9}
\]

Their additive gap is \(\sqrt{10}-\sqrt2\).  A relative-error estimate
with \(\gamma<1/2\) also distinguishes them, since

\[
                 (1+\gamma)J_-<(1-\gamma)J_+
                 \quad(\gamma<1/2).                              \tag{10}
\]

This is a lower bound from the original problem-data oracle.  If an exact
fixed-center Hessian or assembled KKT oracle is handed to the algorithm for
free, its endpoint diagonal \(\phi''(\alpha_s(1))\) already differs between
the two parity cases.  Such an oracle has performed the hard preprocessing
and is not the input model of (4).

## 3. What normalization erases

Let

\[
                 p_\sigma=(s_0,s_1,\ldots,s_N)^T,
                 \qquad L=N+1.                                  \tag{11}
\]

The reduced problem has the single coordinate \(\alpha\).  For
\(\eta>0\), its optimizer, central point, and central predictor are nonzero
scalars.  Differentiating (8), with

\[
 d(\alpha)=\phi''(\alpha),
\]

gives

\[
                       d(\alpha_s(\eta))\dot\alpha_s=c_s.         \tag{12}
\]

The reduced Hessian is the positive \(1\times1\) matrix \([d(\alpha)]\),
so its spectral condition number is exactly one at every interior point.
This conditioning statement does not include the work needed to construct
the hidden reduction map or its effective objective coefficient.

Amplitude normalization maps every nonzero one-coordinate real vector to
the same physical state \(|0\rangle\), because its sign is a global phase.
Thus

\[
 |\alpha^*\rangle=|\alpha_s(\eta)\rangle
     =|\dot\alpha_s(\eta)\rangle=|0\rangle                       \tag{13}
\]

as normalized reduced-coordinate states.  Equation (13) does **not** give
the sign, norm, objective value, a signed reference amplitude, or a
reusable classical coordinate oracle.  At a center, even supplying the norm
would distinguish the two cases because \(|\rho(3)|\ne|\rho(1)|\).

In the original coordinates,

\[
 r(\eta)=\alpha_s(\eta)p_\sigma,qquad
 \dot r(\eta)=\dot\alpha_s(\eta)p_\sigma.
\]

Their normalized primal states, and the normalized optimizer direction,
are all the prefix-parity state

\[
             |p_\sigma\rangle={1\over\sqrt L}
                    \sum_{m=0}^N s_m|m\rangle,                   \tag{14}
\]

up to a global phase.  Unlike (13), (14) is not claimed to be cheap to
prepare from raw sign access.  Constructing the hidden nullspace basis
\(p_\sigma\), or the effective reduced coefficient \(c_s\), is exactly
where equality elimination can spend \(\Theta(N)\) work.

The same qualification applies to the full augmented Newton state.  Its
primal block is proportional to (14), but its equality-multiplier block is
nonzero and its relative weight changes with \(d(\alpha)\); it is not
identified with the trivial scalar state (13).

## 4. Exact sparse-oracle reduction

Write the equality matrix as \(A_\sigma\in\mathbb R^{N\times(N+1)}\), with
row \(m\)

\[
                 (A_\sigma)_{m,m-1}=-\sigma_m,qquad
                 (A_\sigma)_{m,m}=1.                             \tag{15}
\]

Every row has two nonzeros and every column has at most two.  The locations,
row norms \(\sqrt2\), column norms, and Frobenius norm \(\sqrt{2N}\) are
public and independent of the signs.  The objective is the public
two-sparse vector \(e_0+2e_N\), and the right-hand side is zero.

One sparse-value query to (15) uses at most one raw query to \(\sigma_m\).
Sparse-location queries are public.  A coherent normalized-row state or a
classical SQ row sample is implemented with one sign query, while all
squared-magnitude sampling distributions are public.  Conversely, querying
the first coefficient in row \(m\) returns \(-\sigma_m\).  Thus raw sign
access and full sparse/SQ access to the original input simulate one another
with constant query overhead, including coherently.

This equivalence excludes stronger interfaces that return an exact norm of
a hidden central point, query access to its signed coordinates, or a
preassembled exact-center KKT matrix.  Any of those can leak the answer that
the original input oracle is meant to hide.

## 5. Relative solutions and full chain output

The value-estimation lower bound (4) does not require a large output.  A
feasible relative-approximate **solution** is also parity-hard.  If

\[
       (e_0+2e_N)^Tr\geq(1-\gamma)\operatorname{OPT}_\sigma,
       \qquad \gamma<1,
\]

then

\[
        \alpha\geq1-\gamma\quad(s=+1),\qquad
        \alpha\leq-(1-\gamma)\quad(s=-1).                        \tag{16}
\]

Thus even the signed readout of \(r_0\), to error less than
\(1-\gamma\), determines total parity.

A full classical primal vector contains still more information.  The exact
optimizer satisfies

\[
                   r_m^*=\alpha^*s_m,qquad
                   \sigma_m=\operatorname{sgn}(r_m^*r_{m-1}^*).  \tag{17}
\]

Therefore coordinatewise error below \(1/2\) recovers every hidden sign.
More generally, a feasible relative solution obeying (16), output with
coordinatewise error below \((1-\gamma)/2\), recovers the entire chain by
adjacent sign products.  Outputting all \(N\) signs has quantum and
randomized query complexity \(\Theta(N)\), matching the cost of reading the
input and the output length.  For a normalized version of (14), the
corresponding sufficient coordinatewise accuracy is
\(1/(2\sqrt L)\).

State preparation, one destructive copy of a state, SQ coordinate access,
full classical output, and a reusable preparation unitary are different
output contracts.  Equation (17) is a full-output statement and is not
silently inferred from one copy of (14).

## 6. The literal KKT system has treewidth one and condition \(\Theta(N)\)

At a central point let \(d=\phi''(\alpha)>0\).  The equality-embedded
Newton matrix is

\[
       K_{\sigma,d}=
       \begin{pmatrix}
          d e_0e_0^T&A_\sigma^T\\
          A_\sigma&0
       \end{pmatrix}.                                            \tag{18}
\]

Ordering the vertices as
\(r_0,\lambda_1,r_1,\lambda_2,\ldots,\lambda_N,r_N\) makes (18) a signed
tridiagonal path with one endpoint diagonal \(d\).  Its sparsity graph is a
tree and has treewidth one.

The signs do not affect its singular values.  With
\(P=\operatorname{diag}(s_0,\ldots,s_N)\) and
\(R=\operatorname{diag}(s_1,\ldots,s_N)\),

\[
                    R A_\sigma P=A_0,                            \tag{19}
\]

where \((A_0x)_m=x_m-x_{m-1}\).  Conjugating (18) by
\(\operatorname{diag}(P,R)\) therefore gives the unsigned matrix.

For completeness, solve the unsigned system
\(K_{0,d}(x,y)=(f,g)\).  A particular solution of \(A_0x=g\) with
\(x_0=0\) is

\[
                         x_m=\sum_{j=1}^m g_j.                    \tag{20}
\]

The remaining nullspace component is \(t\mathbf1\).  Multiplying the first
block equation by \(\mathbf1^T\) gives

\[
                         t=x_0={\mathbf1^Tf\over d}.              \tag{21}
\]

Equations (20)--(21), followed by the explicit backward-cumulative solution
\(y_m=\sum_{j=m}^N f_j\), show \(\|K_{0,d}^{-1}\|=O_d(N)\): both cumulative
operators have norm \(O(N)\), and the nullspace term in (21) has norm at
most \(L\|f\|/d\).  Conversely, take
\(f=\mathbf1/\sqrt L\) and \(g=0\).  Then (21) gives
\(x=(\sqrt L/d)\mathbf1\), so \(\|x\|=L/d\) for a unit right-hand side.
Hence

\[
              \|K_{\sigma,d}^{-1}\|=\Theta_d(N),\qquad
              \|K_{\sigma,d}\|=\Theta_d(1),\qquad
              \boxed{\kappa_2(K_{\sigma,d})=\Theta_d(N)}.       \tag{22}
\]

At \(\eta=1\), both possible values of \(d\) are positive absolute
constants, so (22) is uniform over the promise.  The equality operator
itself also has \(\kappa_2(A_\sigma)=\Theta(N)\).  This must not be confused
with the alternative construction that boxes every chain coordinate: its
KKT matrix is \(\bigl(\begin{smallmatrix}dI&A^T\\A&0\end{smallmatrix}\bigr)\),
whose smallest absolute eigenvalue is \(\Theta(\sigma_{\min}(A)^2)\) and
whose condition number is \(\Theta(N^2)\).

Forward/back substitution in (20)--(21) solves (18) in \(O(N)\) arithmetic
and no fill.  Equivalently, one scan computes all prefix signs, after which
the exact central path is only the public scalar formula (8).

## 7. Movement does not multiply query hardness

The barrier parameter is one, so the usual short-step iteration scale has
no \(\sqrt N\) factor.  Directly, the barrier-metric length from the analytic
center to \(|\alpha|=1-\epsilon\) is

\[
 \int_0^{1-\epsilon}\sqrt{\phi''(t)}\,dt
 =\sqrt2\int_0^{1-\epsilon}{\sqrt{1+t^2}\over1-t^2}\,dt
 =\Theta(1+\log(1/\epsilon)).                                   \tag{23}
\]

Thus bounded-local-move schedules can require
\(\Theta(\log(1/\epsilon))\) checkpoints while discovering the hidden parity
requires \(\Theta(N)\) input queries.  These facts do not imply
\(\Omega(N\log(1/\epsilon))\).  The input is static: after one \(O(N)\)
scan, an algorithm caches the prefix gauge and parity, and every later
center is obtained by scalar rescaling.  The natural combined scale is

\[
               O\bigl(N+\log(1/\epsilon)\bigr)
               =O\bigl(\max\{N,\log(1/\epsilon)\}\bigr),         \tag{24}
\]

up to constant factors, plus whatever output-writing contract is required.
Likewise, a one-shot KKT condition or solve cost is not multiplied by the
movement count without a temporal direct-product theorem.

## 8. Interpretation and limits

The useful theorem is a sharp negative statement about normalized quantum
linear-solver output.  A sparse, treewidth-one program with exact barrier
parameter one has a zero-query reduced normalized Newton state, while its
positive optimal value, a fixed-center primal objective, and even the sign
of a useful reduced coordinate require parity and hence \(\Theta(N)\) raw
input queries.  Normalization and global-phase equivalence can erase exactly
the scalar information optimization needs.

The construction does not show a quantum advantage over classical solution:
both quantum and classical parity query complexities are linear, and a
classical path solve is linear.  It also does not prove that the
original-coordinate state (14) is cheap, that a free exact KKT oracle is a
legitimate original-input oracle, or that per-checkpoint costs compose.
Its potentially novel contribution is the same-instance synthesis of
constant exact barrier parameter, bounded treewidth, linear conditioning,
trivial reduced normalized states, and linear scalar readout hardness.
