# PSD order caps: exact formulation ledgers and the QIPM boundary

Status: Proved; literature-screened; independently audited  
Started: 2026-09-04  
Paper status: Not incorporated  
Confidence: High on the integer ledgers, Schur lift, and exact-arithmetic replacement theorem

## Conclusion

Let \(N\geq4\).  Consider an exact lift of the Euclidean ball \(B_2^N\)
over a product of real PSD cones

\[
                    K=\prod_{i=1}^k\mathbb S_+^{r_i},
                    \qquad 2\leq r_i\leq R,                \tag{1}
\]

whose full slack has globally labelled \(C^1\) primal and dual contact
factors as in the all-order support--Grassmannian theorem.  Put

\[
 c_r=\left\lfloor{r^2\over4}\right\rfloor,
 \qquad d_r={r(r+1)\over2}.                                \tag{2}
\]

Then the strict curvature theorem gives

\[
                             \sum_i c_{r_i}\geq N.          \tag{3}
\]

Equation (3) has three exact formulation ledgers.  If \(a_r\) counts
order-\(r\) blocks, define

\[
\begin{aligned}
 K_R(N)&=\min\left\{\sum_{r=2}^R a_r:
                  \sum_{r=2}^R c_ra_r\geq N\right\},\\
 V_R(N)&=\min\left\{\sum_{r=2}^R ra_r:
                  \sum_{r=2}^R c_ra_r\geq N\right\},\\
 F_R(N)&=\min\left\{\sum_{r=2}^R d_ra_r:
                  \sum_{r=2}^R c_ra_r\geq N\right\}.
                                                               \tag{4}
\end{aligned}
\]

Every lift in (1) satisfies

\[
       k\geq K_R(N),\qquad
       \nu_{\rm normal}(K)\geq V_R(N),\qquad
       M:=\sum_i d_{r_i}\geq F_R(N).                         \tag{5}
\]

Here the middle identity uses the exact theorem
\(\nu_{\rm normal}(K)=\sum_i r_i\) for a product of PSD cones, even when
the normal barrier is allowed to couple the blocks.  Thus (4), rather than
only a big-\(O\) estimate, is the sharp integer consequence of the curvature
budget.

The ledgers do **not** imply an iteration lower bound.  The explicit
Schur-complement lift below has ambient normal-barrier parameter \(N+k\),
but its restricted log-determinant has exact parameter \(k\) and
its exact Newton system has a tree expansion.  Consequently a QIPM that
materializes its full direction at every round has an \(O(N)\)-work
classical replacement per round under matched access.  Coherent or scalar
output, quantum-only input access, finite precision, and arbitrary external
coupling remain outside this statement.

## 1. Closed lower envelopes and exact recurrences

Since \(c_r\) increases with \(r\),

\[
                         K_R(N)=\left\lceil{N\over c_R}\right\rceil.
                                                               \tag{6}
\]

The dimension ledger is exactly computable in \(O(NR)\) time.  Set
\(F_R(0)=0\) and, for \(n\geq1\),

\[
 F_R(n)=\min_{2\leq r\leq R}
        \left\{d_r+F_R\bigl((n-c_r)_+\bigr)\right\}.           \tag{7}
\]

Choosing the first block in an optimal multiset proves both directions of
(7).  This recurrence retains the sometimes important final-block
overshoot that a capacity-to-cost ratio loses.

The normal-parameter ledger has an exact closed form.  Write

\[
                  N=q c_R+t,\qquad 0\leq t<c_R.              \tag{8}
\]

Then

\[
 \boxed{
 V_R(N)=qR+
 \begin{cases}
 0,&t=0,\\
 \lceil2\sqrt t\rceil,&t>0.
 \end{cases}}                                                \tag{9}
\]

Here is a discrete-majorization proof, including the potentially awkward
one-unit residue.  Extend \(c_r=\lfloor r^2/4\rfloor\) to every integer
\(r\geq0\).  Its increments are

\[
                 c_r-c_{r-1}=\left\lfloor{r\over2}\right\rfloor,
                 \qquad r\geq1,                            \tag{9a}
\]

and are nondecreasing.  If \(0<u\leq v<R\), transferring one unit from
\(u\) to \(v\) changes total capacity by

\[
 (c_{u-1}+c_{v+1})-(c_u+c_v)
 = (c_{v+1}-c_v)-(c_u-c_{u-1})\geq0.                       \tag{9b}
\]

Pad any block-order list by zeros and repeat this exchange.  Therefore, if
its total order is \(S=\ell R+j\), \(0\leq j<R\), then

\[
                         \sum_i c_{r_i}\leq \ell c_R+c_j. \tag{9c}
\]

This is an upper bound in the relaxed problem that permits orders zero and
one.  Consequently it remains valid for the actual orders \(2,\ldots,R\),
and no separate deletion argument is needed when \(j=1\).

If \(t=0\), \(q\) order-\(R\) blocks attain capacity \(N\).  Every list of
total rank at most \(qR-1\) has, by (9c), capacity at most
\((q-1)c_R+c_{R-1}<q c_R=N\).  If \(t>0\), put

\[
             \rho(t)=\min\{r:c_r\geq t\}=\lceil2\sqrt t\rceil. \tag{9d}
\]

The equality follows because \(t\) is integral, so
\(\lfloor r^2/4\rfloor\geq t\) iff \(r^2/4\geq t\).  Also
\(\rho(t)\leq R\).  The \(q\) order-\(R\) blocks and one order-\(\rho(t)\)
block attain capacity at least \(N\).  Conversely, a list of total rank at
most \(qR+\rho(t)-1\) either has rank below \(qR\), in which case the
preceding bound applies, or has rank \(qR+j\) with \(j<\rho(t)\).  In the
latter case (9c) bounds its capacity by
\(q c_R+c_j<q c_R+t=N\).  This proves (9).  Explicitly,
\(c_R=m^2\) for \(R=2m\), while \(c_R=m(m+1)\) for \(R=2m+1\); the same
argument covers both parity classes and also \(R=2\).

There are also useful closed envelopes.  Write \(s=\lfloor R/2\rfloor\).  A
direct calculation gives

\[
 {d_r\over c_r}=
 \begin{cases}
   2+1/j,&r=2j,\\
   2+1/j,&r=2j+1,
 \end{cases}                                                 \tag{10}
\]

and \(c_r/r\) is strictly increasing in \(r\geq2\).  Therefore

\[
\boxed{
\begin{aligned}
 k&\geq\left\lceil{N\over\lfloor R^2/4\rfloor}\right\rceil,\\
 \nu_{\rm normal}
   &\geq\left\lceil {RN\over\lfloor R^2/4\rfloor}\right\rceil,\\
 M&\geq\left\lceil\left(2+{1\over\lfloor R/2\rfloor}\right)N
                \right\rceil.
                                                               \tag{11}
\end{aligned}}
\]

Two cap-independent inequalities strengthen (11) when \(R\) is large.  From

\[
 N\leq\sum_i c_{r_i}\leq{1\over4}\sum_i r_i^2
                    \leq{1\over4}\left(\sum_i r_i\right)^2,
\]

one obtains

\[
                     \nu_{\rm normal}\geq\lceil2\sqrt N\rceil. \tag{12}
\]

Moreover

\[
 d_r=2c_r+\left\lceil{r\over2}\right\rceil,
\]

so (3) and (12) imply

\[
                         M\geq2N+\lceil\sqrt N\rceil.         \tag{13}
\]

In particular, a single globally regular PSD block must have order
\(r\geq\lceil2\sqrt N\rceil\).  Equations (11)--(13) combine as

\[
\begin{aligned}
 \nu_{\rm normal}&\geq
 \max\left\{\left\lceil {RN\over c_R}\right\rceil,
             \lceil2\sqrt N\rceil\right\},\\
 M&\geq
 \max\left\{\left\lceil(2+1/s)N\right\rceil,
             2N+\lceil\sqrt N\rceil\right\}.                 \tag{14}
\end{aligned}
\]

The dimension recurrence is not generally equal to the ratio relaxation.
For example, \(F_4(6)=16\), whereas (11) only gives \(15\).  Two small-cap
closed forms, useful for checks, are

\[
 F_4(N)=10\lfloor N/4\rfloor+3(N\bmod4),\qquad
 F_5(N)=\lceil5N/2\rceil \quad(N\geq4).                     \tag{14a}
\]

For \(R=4\), order four supplies four units for cost ten, while orders two
and three cost three per capacity unit; separating the number of order-four
blocks proves the first formula.  For \(R=5\), (10) gives the lower ratio
\(5/2\).  Every even capacity at least four is a nonnegative combination of
four and six, realized by orders four and five at that ratio; for odd \(N\),
add one order-two block to a realization of \(N-1\).  This attains the
ceiling.

For \(R=2\), these give exactly
\((k,M,\nu)=(N,3N,2N)\).  For \(R=3\), they give exactly

\[
       k=\lceil N/2\rceil,\qquad M=3N,
       \qquad\nu=\lceil3N/2\rceil.                           \tag{15}
\]

The constructions in the next section attain (15), including parity.  For
\(R\geq4\), (4) is the exact *capacity-ledger* consequence, but it need not
be the true lift optimum: existence of ball lifts attaining the balanced
PSD contact capacities is open.

## 2. The all-order Schur-complement upper construction

Partition \([N]\) into groups \(G_1,\ldots,G_k\) of sizes
\(g_j\leq R-1\).  Introduce one scalar \(s_j\) per group and impose

\[
 Z_j(s_j,x)=
 \begin{pmatrix}s_j&x_{G_j}^T\\x_{G_j}&I_{g_j}\end{pmatrix}\succeq0,
 \qquad \sum_{j=1}^k s_j=1.                                \tag{16}
\]

Schur complementation makes (16) equivalent to
\(s_j\geq\|x_{G_j}\|_2^2\), so its projection is exactly \(B_2^N\).
Strict feasibility holds at \(x=0\) and any positive \(s\) summing to one.
At a boundary point the fiber is unique:
\(s_j=\|x_{G_j}\|^2\).

The global polynomial contact factors are

\[
 A_j(x)=
 \begin{pmatrix}\|x_{G_j}\|^2&x_{G_j}^T\\x_{G_j}&I_{g_j}\end{pmatrix},
 \qquad
 B_j(y)={1\over2}
 \begin{pmatrix}1\\-y_{G_j}\end{pmatrix}
 \begin{pmatrix}1\\-y_{G_j}\end{pmatrix}^{T},              \tag{17}
\]

and

\[
              \sum_j\operatorname{tr}(A_j(x)B_j(y))
              ={1\over2}\sum_j\|x_{G_j}-y_{G_j}\|^2
              =1-\langle x,y\rangle                         \tag{18}
\]

for \(x,y\in S^{N-1}\).  Thus this is within the regularity scope of (3).

More generally, prescribe any group count

\[
          \left\lceil{N\over R-1}\right\rceil\leq k\leq N.
\]

Among grouped Schur lifts with this \(k\), convexity of
\((g+1)(g+2)/2\) makes balanced group sizes minimize ambient dimension.
Write \(a=\lfloor N/k\rfloor\) and \(b=N-ak\).  The exact Pareto ledger of
the grouped construction is

\[
\boxed{
\begin{aligned}
 k_{\rm Schur}&=k,\\
 \nu_{{\rm normal},\,\rm Schur}&=N+k,\\
 M_{\rm Schur}(k)&=(k-b){(a+1)(a+2)\over2}
                 +b{(a+2)(a+3)\over2}.
                                                               \tag{19}
\end{aligned}}
\]

Thus the minimum grouped factor count and normal parameter are

\[
 k_{\rm Schur}^{\min}=\left\lceil{N\over R-1}\right\rceil,
 \qquad
 \nu_{{\rm normal},\,\rm Schur}^{\min}
       =N+\left\lceil{N\over R-1}\right\rceil.               \tag{20}
\]

Coordinatewise minimization of ambient dimension instead uses only groups
of size one or two and gives \(M_{\rm Schur}^{\min}=3N\), because

\[
              {(g+1)(g+2)\over2}-3g={(g-1)(g-2)\over2}\geq0. \tag{21}
\]

These three minima need not occur at the same group count.  Equation (19)
records the exact count--dimension--barrier tradeoff.  In particular,
taking as many maximal groups as possible is generally not
dimension-optimal even at minimum \(k\); balancing the groups is.
More explicitly, if \(N=\ell(R-1)+h\), \(0\leq h<R-1\), the literal
maximal-group partition has

\[
 M_{\rm maximal}=\ell d_R+\mathbf 1_{h>0}d_{h+1},\qquad
 \nu_{\rm maximal}=\ell R+\mathbf 1_{h>0}(h+1).            \tag{21a}
\]

Balancing the same minimum number of groups leaves \(k\) and \(\nu=N+k\)
unchanged and weakly lowers \(M\), giving (19).  On the other hand, the
coordinatewise value \(M=3N\) is feasible under every cap \(R\geq3\) by
using only size-one and size-two groups, but it requires
\(k\geq\lceil N/2\rceil\), generally more than the minimum factor count
when \(R>3\).

For comparison with an unreduced conic encoding, fixing the public
\(I_{g_j}\) blocks uses

\[
 p=1+\sum_j{g_j(g_j+1)\over2}
 \quad\text{affine equations},\qquad
 M-p=N+k-1.                                                 \tag{21b}
\]

Eliminating those fixed coordinates leaves exactly the \(N+k\) variables
\((s,x)\) and the one remaining sum equation used below.

For fixed \(R\), the lower and upper ledgers are all \(\Theta_R(N)\), and
the construction is simultaneous exact at \(R=2,3\).  For a growing cap,
however, the presently proved bounds leave a real formulation gap.  Away
from ceiling regimes, and for \(4\leq R\leq N+1\),

\[
\begin{array}{c|c|c}
 &\text{curvature lower envelope}
 &\text{balanced minimum-factor Schur point}\\ \hline
 k&\gtrsim\max\{1,4N/R^2\}&\sim\max\{1,N/R\}\\
 \nu_{\rm normal}&\gtrsim\max\{4N/R,2\sqrt N\}&\sim N\\
 M&\gtrsim2N+\sqrt N&\sim NR/2.
\end{array}                                                   \tag{22}
\]

Thus this simultaneous minimum-factor point can exceed the capacity ledger
by a factor as large as \(\Theta(\min\{R,\sqrt N\})\) for the normal parameter,
\(\Theta(\min\{R,N/R\})\) for factor count, and \(\Theta(R)\) for ambient
dimension.  Optimizing the grouped construction for dimension instead gives
\(3N\), as in (21), while sacrificing the minimum count and normal parameter.
These are gaps between a lower bound and an upper construction, not
separations and not evidence that the lower ledger is attainable.

## 3. Restriction collapses both barrier and Newton complexity

The ambient normal parameter in (19) is not the relevant intrinsic
parameter after the public identity blocks in (16) are eliminated.  Put

\[
                   \Delta_j=s_j-\|x_{G_j}\|^2.
\]

The restricted product log determinant is exactly

\[
                         F(s,x)=-\sum_j\log\Delta_j.          \tag{23}
\]

Each summand is a \(1\)-self-concordant barrier on the paraboloid epigraph
\(s>\|x\|^2\).  Here is a direct check.  Along a line with
\(q(t)=\Delta+dt-\|b\|^2t^2\), put
\(u=d/\Delta\) and \(v=2\|b\|^2/\Delta\).  Then

\[
 D^2(-\log q)=u^2+v,
 \qquad D^3(-\log q)=-2u^3-3uv,                              \tag{24}
\]

and

\[
 |2u^3+3uv|\leq2(u^2+v)^{3/2}.
\]

The local squared norm of the gradient is exactly one.  Indeed, for one
block

\[
 \nabla^2(-\log\Delta)=D+ww^T,
 \quad
 D=\operatorname{diag}(0,2\Delta^{-1}I_g),
 \quad
 w={1\over\Delta}\begin{pmatrix}1\\-2x\end{pmatrix}.         \tag{25}
\]

Solving \(Hu=\nabla(-\log\Delta)\) gives
\(u=(-\Delta,0)\), hence
\(\nabla F^TH^{-1}\nabla F=1\).  Products add parameters and affine
restriction cannot increase them.  Therefore (23), restricted to
\(\sum_js_j=1\), has parameter at most

\[
                             \nu_{\rm slice}\leq k.
\]

The parameter remains exactly \(k\) after this restriction.  On the tangent
space of \(\sum_js_j=1\), block inversion and a one-row Schur complement
give

\[
 \|\nabla F\|_{*,\,\mathrm{slice}}^2
 =k-\frac{(\sum_j\Delta_j)^2}
          {\sum_j\Delta_j(s_j+\|x_{G_j}\|^2)}.               \tag{26}
\]

Choose \(s_j=1/k\) and
\(\|x_{G_j}\|^2=1/k-\varepsilon\) in one coordinate of each nonempty
group.  The second term tends to zero with \(\varepsilon\), proving

\[
                              \boxed{\nu_{\rm slice}=k}.      \tag{27}
\]

This proves, without any iteration lower-bound inference, that
\(N+k\) is only the optimal *ambient normal-barrier* parameter;
the same formulation has a much smaller slice certificate.  That
certificate is intrinsic to the fixed grouped slice, not merely exact for
the displayed separable barrier.  Fixing \(s_j=\sigma_j>0\), with
\(\sum_j\sigma_j=1\), and restricting each \(x_{G_j}\) to one coordinate
direction cuts out an affine \(k\)-cube.  The classical cube lower bound
therefore gives
\[
      \vartheta_{\rm opt}(\text{grouped Schur affine slice})=k
\]
even among arbitrary coupled, non-logarithmically-homogeneous
self-concordant barriers.  See
[Coupling cannot lower the barrier parameter of the grouped ball
slice](2026-09-04-coupled-barrier-grouped-ball-slice.md).
The companion
[PSD nullity theorem](2026-09-04-psd-nullity-restricted-barrier.md)
now proves that at the minimum allowed group count this certificate is
optimal across all globally \(C^1\) full-contact selected PSD-product
lifts under the same order cap:
\[
                  \nu_{\rm std,slice}^{\min}
                    =\left\lceil{N\over R-1}\right\rceil.
\]
That across-lift optimality is for the restricted standard sum of log
determinants.  The arbitrary-coupled-barrier conclusion above is for the
fixed grouped slice and is not yet an all-lifts theorem.

Equation (25) also exposes the exact Newton sparsity.  Introduce one hub for
each rank-one term \(w_jw_j^T\), and retain one row vertex for
\(\sum_js_j=1\).  The expanded graph consists of the paths

\[
       \text{global row} - s_j - \text{hub}_j
       - \{x_i:i\in G_j\}.                                  \tag{28}
\]

It is a tree with \(N+2k+1\) vertices and \(N+2k\) edges.  Schur
complementation of the negative identity hub block recovers the exact
primal KKT matrix.  Since
the Hessian is positive definite and the equality row has full rank, both
matrices are nonsingular.  A supplied tree decomposition therefore gives
an exact solve in

\[
                                  O(N+k)=O(N)                \tag{29}
\]

field operations.  This is a latent graph statement: materializing every
entry of the PSD blocks would conceal the tree and cost much more.

For a well-initialized short-step method based directly on (23), the generic
certificate is consequently

\[
 O\!\left(\sqrt{k}\log{1\over\varepsilon}\right)
 \quad\text{iterations and}\quad
 O\!\left(N\sqrt{k}\log{1\over\varepsilon}\right)
 \quad\text{exact field operations}.                        \tag{30}
\]

This is an upper envelope.  It is not a lower bound for this or any other
IPM, and it suppresses initialization and bit-growth costs.

## 4. Matched full-output QIPM replacement theorem

Consider a hybrid QIPM applied to (16) that, at every outer round,
materializes a classical Newton direction or updated iterate in the
\(N+k\) free coordinates.  Assume:

1. matched classical entry access to the current \(s,x\) and Newton
   right-hand side at the precision charged to the quantum data oracle;
2. the outer convergence theorem accepts any direction satisfying the same
   residual contract;
3. the fixed tree structure (28) is public; and
4. either exact arithmetic is the comparison model or a separate stable
   finite-precision factorization guarantee is supplied.

Then every quantum Newton solve can be replaced by (29), preserving the
outer theorem, at \(O(N)\) classical work per round.  Materializing the
same dense classical direction already takes \(\Omega(N+k)=\Omega(N)\)
word writes.  Thus this architecture has no polynomial per-round or total
Newton-solve advantage on the isolated Schur ball lift.  If it runs for
\(T\) rounds, the replacement costs \(O(TN)\), plus common setup and data
evaluation costs.

The statement is stronger than comparing the dense textbook SDP costs:
the relevant classical baseline is the reduced tree system actually
present in the same formulation.  It does not cover a normalized solution
state, a scalar observable, a sample, or a coherent iterate; nor does it
cover quantum-only access, dense external coupling, or claim that \(T\)
itself must be large.

## 5. Relation to published SDP QIPMs and literature boundary

Augustino--Nannicini--Terlaky--Zuluaga's convergent SDP QIPMs use a quantum
linear-system routine for each Newton system and tomography to obtain the
classical update.  Their bounds depend polynomially on the SDP matrix order,
the Newton-system condition bound, and tomography precision, and their
standard outer count is \(O(\sqrt n\log(1/\varepsilon))\); see
[*Quantum Interior Point Methods for Semidefinite
Optimization*](https://doi.org/10.22331/q-2023-09-11-1110).  Those generic
dimension bounds do not exploit the public identity compressions and
tree expansion (25)--(28).  Applying them to a block-diagonal embedding of
(16) therefore cannot establish an advantage over the \(O(N)\) same-instance
classical Newton solve.

In that embedding, the single matrix order is
\(\sum_jr_j=N+k\), not the maximum block order \(R\).  There is no justified
substitution \(n\mapsto R\) in the published SDP-QIPM bounds.  Exploiting
the product incidence, the \(M\)-coordinate ledger, or the latent tree
requires a separate algorithmic analysis; (25)--(29) supply that analysis
for the classical comparator on this particular family.

Huang--Jiang--Song--Tao--Zhang give a robust quantum SDP IPM with headline
time \((mn^{3/2}+n^3)\operatorname{poly}(\kappa,\log(mn/\varepsilon))\)
under its QRAM/oracle and condition assumptions, and with classical
primal--dual output; see
[*A Faster Quantum Algorithm for Semidefinite Programming via Robust IPM
Framework*](https://arxiv.org/abs/2207.11154).  This is again a generic
matrix-order/constraint-count bound, not a theorem that the maximum product
block order controls the cost.

On the classical side, Zhang's sparse chordal-SDP theorem gives
\(O(\omega^4N_c)\) time per round when the *extended* aggregate graph,
which makes every constraint support a clique, has frontsize \(\omega\);
see [*Complexity of Chordal Conversion for Sparse Semidefinite Programs with
Small Treewidth*](https://doi.org/10.1007/s10107-024-02137-5).  Applied
mechanically here, the global row \(\sum_js_j=1\) creates a \(k\)-vertex
constraint clique, so that generic theorem does not certify (29).  The
explicit rank-one KKT augmentation proves the stronger linear result for
this special formulation.  This also illustrates why raw SDP sparsity,
extended-graph width, and latent Newton treewidth are different resources.

The end-to-end SOCP analysis of Dalzell et al. separately emphasizes the
cost of condition numbers, data loading, and repeated tomography:
[*End-To-End Resource Analysis for Quantum Interior-Point Methods and
Portfolio Optimization*](https://doi.org/10.1103/PRXQuantum.4.040325).
The replacement theorem above is exact-arithmetic and structural; it does
not infer favorable conditioning from treewidth and does not hide those
costs.

Gouveia--Parrilo--Thomas give the general equivalence between cone lifts and
slack factorizations in
[*Lifts of convex sets and cone
factorizations*](https://arxiv.org/abs/1111.3164).  Fawzi--Parrilo study
products of fixed-size PSD cones, chiefly for combinatorial polytopes and
through support-pattern arguments, in
[*Exponential lower bounds on fixed-size psd rank and semidefinite extension
complexity*](https://arxiv.org/abs/1311.2571).  These do not give the smooth
ball capacity ledger (4).  The Schur-complement ball LMI and grouped
quadratic epigraph modeling are standard; no novelty is claimed for (16).

The exact normal-barrier identity uses Güler--Tunçel,
[*Characterization of the barrier parameter of homogeneous convex
cones*](https://doi.org/10.1007/BF01584844).  The tree solve uses
Fürer--Hoppen--Trevisan,
[*Fast Gaussian Elimination for Low Treewidth
Matrices*](https://doi.org/10.4230/LIPIcs.ESA.2025.116).  A targeted search
over PSD extension complexity, small-block PSD approximations, smooth ball
lifts, SDP-QIPM tomography, and structured SDP Newton systems found no
source combining the all-order strict curvature capacity with (4), the
cap-independent floors (12)--(13), and the slice-barrier/tree collapse.
Apparent novelty remains subject to specialist review.

## Scope checklist

- The lower ledgers require the global primal/dual \(C^1\) contact-factor
  hypothesis of the all-order Grassmannian theorem; they are not claimed for
  arbitrary PSD lifts.
- The values in (4) are exact consequences of the capacity inequality, not
  claims that a lift attains them for \(R\geq4\).
- The normal-barrier lower bound concerns the ambient homogeneous product.
  Equation (27) explicitly prevents its use as an intrinsic iteration lower
  bound for the affine slice.
- Treewidth controls exact arithmetic, not numerical stability or bit
  complexity.  No uniform condition-number bound is asserted.
- The QIPM conclusion uses matched access and explicit full-vector output.
  It is not an oracle lower bound for compressed output and not an
  iteration lower bound.

## Independent audit

A hostile audit independently verified the majorization proof and exact
\(V_R\) formula, including residual cases, and exhaustively compared it with
the dynamic program for \(2\leq R\leq14\), \(N\leq500\).  It also checked
the \(F_4,F_5\) formulas, balanced grouped-Schur Pareto curve, unreduced
equation counts, exact slice dual-norm formula, one-hub graph and
nonsingularity, matched-output replacement scope, equation tags, and
internal references.  It identified and corrected two presentation issues:
the rank-one-residue step in the original majorization sketch was too terse,
and the asymptotic Schur table needed to specify its minimum-factor Pareto
point.  With those corrections incorporated, the final verdict was
**PASS**.
