# Algorithm opportunities assessed on 2026-09-12

Status: closed exploratory note. The exact example and repair LP passed the
[independent correctness review](review-20260912-quadratic-conflict-example.md).
No conflict-repair integration or solver benchmark was implemented. The
proposed experiment below is a historical proposal, not an active work queue.

The best secondary algorithmic opportunity from this bounded scout is **using
local infeasibility proofs to select globally useful convex aggregations of
original nonconvex quadratic rows**. Its potential value is broader pruning in
global MIQCQP/GDP search. The elementary aggregation theorem is established
mathematics; a possible contribution is an inexpensive certificate-selection
algorithm and demonstrated improvements over existing solver components.
No performance advantage or publication novelty is established here.

The initial second candidate, numerical certification of inexact OA/Benders
cuts, was rejected as insufficiently distinct from prior work. The root
researcher is pursuing a separate measurement-design direction as the main
project; this note records a bounded secondary candidate and the reasons other
algorithm ideas were not prioritized.

## Relevance and baseline

Bernal Neira's work on GDP, conic reformulations, OA, solver integration, and
process superstructures makes reusable global nonlinear cuts directly relevant.
For nonconvex models, inactive-unit elimination and local NLP incumbent search
do not themselves provide global bounds. A useful extension should preserve
the bound chain while exploiting the active logical structure.

The principal comparison is Berthold and Witzig, *Conflict Analysis for MINLP*
(2021), DOI [10.1287/ijoc.2020.1050](https://doi.org/10.1287/ijoc.2020.1050),
local package `berthold2021-conflict-analysis-for-minlp`. Their LP method lifts
local proofs toward ancestors where their linearizations remain valid. Their
NLP method aggregates convex nonlinear relaxation rows. The inspected
manuscript explicitly constructs the convex NLP relaxation from recognized
convex original rows and linear underestimators of nonconvex rows; it does not
claim to reconstruct a convex aggregate of original nonconvex rows from an LP
ray. See physical pp.8–14 and p.21 of the retrieved report.

Quadratic aggregation is already a substantial literature. Dey, Muñoz, and
Serrano (2022), DOI
[10.1137/21M1428583](https://doi.org/10.1137/21M1428583), study convex hulls from
aggregations. Blekherman, Dey, and Sun (2024), local package
`blekherman2024-aggregations-of-quadratic-inequalities-and`, provide a further
important comparator. Hongbo Dong's
[2016 manuscript](https://optimization-online.org/wp-content/uploads/2014/03/4274.pdf),
*Relaxing nonconvex quadratic functions by multiple adaptive diagonal
perturbations*, explicitly permits aggregating original quadratic inequalities
or reconstructed lifted rows before generating convex cutting surfaces. It
leaves effective selection of the aggregate outside its scope on physical p.2.
Thus neither aggregation, reconstruction, convexification after aggregation,
nor diagonal perturbation should be claimed new.

## Candidate 1: repair local proof multipliers to recover a global convex row

Consider bounded variables `x` and original quadratic constraints

\[
g_i(x)=x^TQ_i x+a_i^Tx+b_i\le0,\qquad i=1,\ldots,m.
\]

Take every `Q_i` symmetric, replacing it by its symmetric part if necessary.
Some variables may be integer, and some rows may be active only under stated
GDP literals. Initially restrict to globally active rows. At a spatial node
with box `B=[l,u]`, an LP relaxation contains affine estimators

\[
\ell_i(x)=\bar a_i^Tx+\bar b_i\le g_i(x)\quad(x\in B).
\]

Several estimators can come from the same row; their multipliers must be
summed when reconstructing that original row. Linear equalities can be
included with unrestricted multipliers. Every local row needs an explicit
mapping to its original constraint and validity box.

For any `lambda>=0`, define

\[
G_\lambda(x)=\sum_i\lambda_i g_i(x),\qquad
L_\lambda(x)=\sum_i\lambda_i\ell_i(x).
\]

Two elementary facts are the certificate contract:

1. `G_lambda(x)<=0` for every original feasible point, independently of `B`.
2. If `min_B L_lambda>0`, then `G_lambda>0` on `B`, proving that box infeasible.

If `Q_lambda=sum_i lambda_i Q_i` is PSD, `G_lambda` is globally convex, and
every tangent inequality

\[
G_\lambda(\bar x)+\nabla G_\lambda(\bar x)^T(x-\bar x)\le0
\]

is globally valid. For any `bar x in B` it separates that point whenever the
strict proof margin holds. The tangent need not exclude the entire box;
that stronger statement needs a minimizer or a separate affine support check.

The proposed algorithm does not simply accept the first Farkas ray. Starting
with its sparse row support, it searches for nearby nonnegative weights that
retain a positive margin and make `Q_lambda` diagonally dominant with
nonnegative diagonal. This PSD sufficient condition is expressible by an LP:

\[
t_{jk}\ge Q_{\lambda,jk},\quad
t_{jk}\ge-Q_{\lambda,jk},\quad
Q_{\lambda,jj}\ge\sum_{k\ne j}t_{jk}.
\]

The displayed repair LP uses inequality rows only. Use `sum lambda_i=1` to
exclude arbitrary scaling. If linear equality multipliers are also optimized,
split them as `mu=mu_plus-mu_minus` and use
`sum lambda_i+sum mu_plus_j+sum mu_minus_j=1`. Leaving equality multipliers
unrestricted in magnitude can make the maximum margin unbounded. The
inequality-only normalization also excludes certificates using only equalities.
The box support condition
is also linear after lifting. If
`a(lambda)=sum lambda_i bar a_i` and
`b(lambda)=sum lambda_i bar b_i`, introduce `v_j<=0` and
`v_j<=a_j(lambda)` and maximize `delta` subject to

\[
\delta\le b(\lambda)+l^Ta(\lambda)
                 +\sum_j(u_j-l_j)v_j.
\]

At the optimum, the right side can attain `min_B L_lambda`. A positive
certified `delta` therefore supplies a globally valid convex aggregate that
explains the local infeasibility. One could instead enforce PSD through an
SDP or optimize a scaled-DD/SOCP representation, but that is an experimental
comparison, not an immediate implementation requirement.

Rational diagonal dominance gives a simple independent certificate:

\[
x^TQx=\sum_j\left(Q_{jj}-\sum_{k\ne j}|Q_{jk}|\right)x_j^2
 +\sum_{j<k}|Q_{jk}|(x_j+\operatorname{sign}(Q_{jk})x_k)^2.
\]

All coefficients are nonnegative. Approximate LP weights must be rounded and
checked, with the actual margin reported; a floating-point PSD status alone
does not verify validity. Selection can be heuristic while the accepted
certificate is exact.

For conditional GDP rows, the same reasoning proves an aggregate only under
the conjunction of all its supporting activation conditions. It does not justify a global
unconditional cut. The first implementation should avoid this complication
or explicitly retain that condition through a valid GDP/indicator encoding.

## Exact example showing room beyond the termwise root relaxation

Let `0<=x,y<=1` and impose

\[
g_1=x^2+2xy-3/50\le0,\qquad
g_2=2y^2-xy-9/100\le0.
\]

Both quadratic Hessian matrices are indefinite. The complete termwise
relaxation uses square lifts `s_x,s_y`, exact square envelopes
`x^2<=s_x<=x`, `y^2<=s_y<=y`, and the McCormick envelope

\[
\max(0,x+y-1)\le w\le\min(x,y).
\]

It admits

\[
x=y=1/5,\quad s_x=s_y=1/25,\quad w=0.
\]

The lifted rows give `1/25<=3/50` and `2/25<=9/100`. Thus this example is
not caused by omitting useful square tangents.

Now consider the node `B=[1/5,1]^2`. Valid affine estimators there are

\[
\ell_1=4x/5+2y/5-9/50,\qquad
\ell_2=-x+3y/5+3/100.
\]

Their validity follows from exact nonnegative identities on `B`:

\[
g_1-\ell_1=(x-1/5)^2+2(x-1/5)(y-1/5),
\]

\[
g_2-\ell_2=2(y-1/5)^2+(1-y)(x-1/5).
\]

The combination `(lambda_1,lambda_2)=(2,1)` yields

\[
2\ell_1+\ell_2=3x/5+7y/5-33/100\ge7/100>0\quad(x\in B).
\]

The reconstructed original aggregate is

\[
G=2g_1+g_2=2x^2+3xy+2y^2-21/100\le0.
\]

Its matrix has diagonal entries `2`, off-diagonal entries `3/2`, and
determinant `7/4`; it is strictly diagonally dominant and positive definite.
The tangent at `(1/5,1/5)` is

\[
x+y\le7/20.
\]

This globally valid inequality excludes the feasible point of the root
termwise relaxation. In fact `G(1/5,1/5)=7/100`. The origin and both points
`(1/5,0)` and `(0,1/5)` are original feasible, so the example is not a
globally infeasible system. Binary activation constraints `x>=z_x/5` and
`y>=z_y/5` give a small GDP/MINLP interpretation: each activation is feasible,
but their joint activation is infeasible.

The one-row estimator `ell_1` already proves `B` infeasible, so a solver may
return a ray supported on the indefinite first row. Obtaining the convex
aggregate can require enlarging/repairing that support. This is precisely why
the proposed selection step is substantive. It also creates overhead that a
benchmark must justify.

The two-row repair LP can be solved exactly. Normalize
`lambda=(a,1-a)`. Diagonal dominance is equivalent to
`1/5<=a<=5/7`. The affine box margin is

\[
\min_B L_\lambda=
\begin{cases}
(31a-17)/20,&a\le5/9,\\
(11a-5)/100,&a\ge5/9.
\end{cases}
\]

Both pieces increase, so the optimal repair is
`lambda=(5/7,2/7)` with normalized margin `1/35`. The illustrative
combination `(2,1)` above was chosen to make the global tangent simple; its
normalized margin is `7/300`. These computations establish that the proposed
LP has a useful solution on this toy, without suggesting typical solver rays
will have the required support.

Exact arithmetic checks are in
[verify_quadratic_conflict_example.py](../code/research_20260912/verify_quadratic_conflict_example.py).
The algebraic reasoning and LP optimum passed a
[fresh independent correctness review](review-20260912-quadratic-conflict-example.md),
with equality-normalization and conditional-GDP wording corrections applied.
The example demonstrates a relaxation separation, not novel convexification
theory or an improvement over current SCIP/Gurobi as complete systems.

## Experiment, success criterion, and killers

First collect node LP rays and row provenance on a small open MIQCQP subset.
Do offline repairs before modifying a search tree. Count how often DD repair
exists, sparse support size, repair time, exact validation failures, additional
ancestor/root separation, and improvement over the same estimator set.
Only then implement online separation for instances with material opportunity.

The comparison must include unchanged solver conflict analysis, adding the
same number of simple aggregate cuts without conflict guidance, available
SDP/RLT or quadratic aggregate separation, and the full solver with all usual
cuts. Report overhead on unaffected instances. Root-gap or node reduction
alone is insufficient; seek a useful change in time, solved count, or dual-gap
progress on a meaningful process/energy MIQCQP class.

Concrete reasons to stop or narrow this direction:

- Aggregation and diagonal perturbation are known; if conflict guidance does
  not select better cuts more cheaply, the contribution is incremental.
- For a purely bilinear aggregate, the Hessian has zero diagonal. PSD then
  forces the whole Hessian to be zero. This specific DD/PSD mechanism cannot
  create a nontrivial convex quadratic row for a pure pooling formulation.
  It needs existing square terms (possibly in signed quadratic equalities),
  or additional valid quadratic identities containing squares. Changing the
  signs of purely bilinear equalities does not remove the obstruction.
  Adding those identities starts a different RLT
  or SDP-strengthening project.
- The example does not beat a full Shor relaxation. If `X-xx^T` is PSD and
  the original lifted rows hold, then every PSD aggregate is automatically
  valid at `x`, because `trace(Q_lambda(X-xx^T))>=0`. The potential gain is
  obtaining selected SDP-type strength cheaply and locally.
- A standard no-good cut may handle the example's binary infeasibility more
  strongly in binary space. The global quadratic row conveys continuous
  information, but this is not universal dominance over logical conflicts.
- If presolve already finds these convex combinations, if ray supports have
  almost no suitable curvature, or if repair/cut density dominates runtime,
  this should remain a recorded negative result.
- Mapping presolved/lifted rows back to original quadratics is a real software
  boundary. It must be solved soundly rather than assuming all local rows are
  globally active original constraints.

## Rejected candidate 2: residual-certified inexact OA/Benders

At an approximate point `(x_k,z_k)`, nonnegative multipliers `lambda` define
the Lagrangian `L=f+lambda^Tg`. With joint convexity and a bounded continuous
domain `Z`, the affine value-function lower cut

\[
\theta\ge L(x_k,z_k)+\nabla_xL(x_k,z_k)^T(x-x_k)
 +\min_{z\in Z}\nabla_zL(x_k,z_k)^T(z-z_k)
\]

is valid by a supporting inequality and minimization over `Z`. Exact KKT
stationarity and feasibility of the evaluation point are not needed for this
basic validity statement. They matter for cut quality and convergence.

This was initially attractive because Li and Vicente's 2013 perturbed-MINLP
analysis has all-assignment residual assumptions, while Tamm and Kronqvist's
2026 cycling analysis retains exact-oracle/CQ conditions in its finite theorem.
However, Guigues's value-function cut theory already covers inexact lower
cuts from approximate primal-dual solutions; Guigues, Monteiro, and Svaiter
extend that analysis to nonsmooth convex problems. The basic correction is
not a new MINLP theorem. Numerical original-expression checking could still
be useful engineering, but it is not currently the strongest research choice.

The following missing sources were routed to the single literature agent:

1. Vincent Guigues, *Inexact Cuts in Stochastic Dual Dynamic Programming*,
   SIAM Journal on Optimization 30(1):407–438 (2020),
   [arXiv:1809.02007](https://arxiv.org/abs/1809.02007),
   [open PDF](https://arxiv.org/pdf/1809.02007).
2. Vincent Guigues, Renato Monteiro, and Benar Svaiter, *Inexact Cuts in
   Stochastic Dual Dynamic Programming Applied to Multistage Stochastic
   Nondifferentiable Problems* (2021),
   [arXiv:2004.02701](https://arxiv.org/abs/2004.02701),
   [open PDF](https://arxiv.org/pdf/2004.02701), and an
   [author-hosted publisher PDF](https://bpb-us-e1.wpmucdn.com/sites.gatech.edu/dist/0/1467/files/2023/01/SIAM-published-version-inexact-cuts-sddp.pdf).
3. Hongbo Dong, *Relaxing nonconvex quadratic functions by multiple adaptive
   diagonal perturbations*, manuscript dated May 12, 2016,
   [open PDF](https://optimization-online.org/wp-content/uploads/2014/03/4274.pdf).
4. Henrik Alsing Friberg, *Presolving and regularization in mixed-integer
   second-order cone optimization*, DTU Wind Energy PhD thesis (2016),
   [open PDF](https://backend.orbit.dtu.dk/ws/files/125210367/main.pdf).
5. *The Many Faces of Degeneracy in Conic Optimization*,
   [Optimization Online landing page](https://optimization-online.org/2017/05/6007/).
   Bibliographic identity and its lawful attachment were delegated for
   verification; this is a relevant broad source for the conic-degeneracy
   boundary, not a source used to support a new theorem here.

No literature KB files were changed by this scout. The literature agent owns
identity verification, ingestion, full reading, and any retrieval report.

## Other eliminated broad directions

Generic nonconvex Benders using partial global lower bounds is too broad:
logic-based Benders, Li–Grossmann's nonconvex stochastic branch-and-cut, and
joint decomposition already supply substantial frameworks. A new proposal
must identify a specific stronger transferable cut or a material reduction in
the work needed to obtain it.

Facial reduction for degenerate conic on/off states is important but already
has direct mixed-integer precedent. Friberg's 2016 thesis,
*Presolving and regularization in mixed-integer second-order cone optimization*,
available from [DTU](https://backend.orbit.dtu.dk/ws/files/125210367/main.pdf),
explicitly studies facial reduction for strengthening LP approximation bounds.
Only excerpts were inspected here. A broad proposal to add facial reduction
to conic OA is therefore not a clean novelty claim. No detailed new direction
was developed from this source in this scout.
