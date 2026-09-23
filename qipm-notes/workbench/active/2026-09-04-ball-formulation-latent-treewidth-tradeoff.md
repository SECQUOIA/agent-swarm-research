# Exact barrier--regularity tradeoff for sparse formulations of the Euclidean ball

Status: Proved; literature-screened; independently audited  
Started: 2026-09-04  
Paper status: Not incorporated  
Confidence: High on the algebra and graph counts; novelty priority uncertain

## Main theorem

Let \(N\geq3\), and represent
\[
 B_2^N=\{x\in\mathbb R^N:\|x\|_2\leq1\}
\]
in conic form.  Measure Newton sparsity on the one-hub expansion of each
Lorentz barrier Hessian, rather than on its materialized dense graph.  The
graphs below are fixed structural supergraphs; a numerical hub coefficient
may vanish at a special iterate and only delete an edge.  For an ambient
product of Lorentz cones, let \(\nu_{\rm amb}\) denote the minimum parameter
of any, possibly coupled, logarithmically homogeneous self-concordant barrier
on that ambient product.

Bi-contact regularity is used in the incidence-sheet sense: the lift is
proper, its affine slice meets the interior of its ambient product cone, and
its primal and normalized-dual contact incidences contain compact nonsingular
global sheets over the sphere.  The regularity lower bound quantifies over
presentations already reduced to this proper incidence-sheet model; it does
not assert that arbitrary free-variable elimination preserves regularity.

The following three statements hold simultaneously.

1. **Direct cone.**  The affine slice \(t=1\) of \(Q_{N+1}\) is
   bi-contact-regular, has
   \[
       \nu_{\rm amb}=2,
   \]
   and its expanded Newton graph is a tree of width one and size \(N+3\).

2. **Minimum granular lift.**  Every exact lift by \(L\) copies of \(Q_3\)
   satisfies
   \[
       L\geq N-1,\qquad \nu_{\rm amb}\geq2N-2.
   \]
   A binary norm tree attains both equalities.  Its expanded Newton graph is
   itself a tree of width one and size \(5(N-1)\).  Every exact
   \(Q_3^{N-1}\)-lift, not only the norm tree, fails bi-contact regularity.

3. **Minimum regular granular lift.**  Every bi-contact-regular exact
   \(Q_3^L\)-lift satisfies
   \[
       L\geq N,\qquad \nu_{\rm amb}\geq2N.
   \]
   The coordinatewise quadratic lift attains both equalities.  Its expanded
   Newton graph has exact treewidth two and size \(5N+1\).

The same standard barriers have a different exact ledger after the displayed
affine equalities are eliminated.  The direct ball barrier has parameter one.
For \(N\geq4\), choose the norm tree with both root children internal; its
exact reduced parameter is \(2N-4\), the minimum over binary norm-tree
shapes.  A root-leaf comb instead has \(2N-3\).  The smooth coordinate lift
has exact reduced parameter \(N\), including after its final sum equality.
Thus

\[
\begin{array}{c|c|c}
\text{formulation}&\nu_{\rm amb}&\nu_{\rm red}
\\ \hline
Q_{N+1}&2&1\\
Q_3^{N-1}\text{ balanced-root norm tree}&2N-2&2N-4\\
Q_3^N\text{ smooth coordinate lift}&2N&N.
\end{array}                                                   \tag{0}
\]

For \(N=3\), both granular reduced parameters are three.  Hence the one extra
cone needed for global contact regularity raises the ambient parameter by
two but, for \(N>4\), nearly halves the parameter of the displayed reduced
barrier.  This is an exact reversal between the ambient and reduced
comparisons, not an intrinsic slice-barrier optimum.  The parameter table
alone is not an iteration lower bound; the bounded-step theorem below
supplies one for these displayed reduced barriers.

Consequently all three displayed formulations have an \(O(N)\)
exact-arithmetic Newton solve from their fixed decompositions.  The direct
high-dimensional cone is no denser in this latent sense than the minimum
three-dimensional norm tree, while its optimal ambient barrier parameter is
smaller by a factor \(N-1\).  Under the block-dimension cap three, removing
the unavoidable global contact singularity costs exactly one further cone
factor and two further units of ambient barrier parameter, but it does not
change the linear Newton-solve exponent.

This is the no-free-lunch statement: decomposing the ball constraint into
small cones can make the materialized Hessian look sparse, but it cannot
improve the already-linear latent Newton solve and necessarily changes the
best generic short-step barrier certificate from constant to
\(\Theta(N)\).  Insisting additionally on globally regular primal and dual
contact sheets imposes the sharp \(2N-2\) to \(2N\) barrier jump.  Among the
displayed structural metrics, the direct cone weakly dominates the granular
formulations in ambient dimension, barrier parameter, regularity, and
asymptotic Newton work; its only worse coordinate is maximum cone-block
dimension.  Other resources not modeled here, such as a local oracle,
parallel depth, or a deliberately materialized Hessian, can differ.

For well-initialized instances, suppressing common initialization and gap
factors, combining the linear solve with the standard
\(O(\sqrt{\nu_{\rm amb}}\log(1/\epsilon))\) short-step theorem gives the
certified upper envelopes
\[
\begin{array}{c|c}
\text{formulation}&\text{structured Newton arithmetic}\\ \hline
Q_{N+1}&O(N\log(1/\epsilon)),\\
Q_3^{N-1}\text{ norm tree}&
 O(N^{3/2}\log(1/\epsilon)),\\
Q_3^N\text{ smooth coordinate lift}&
 O(N^{3/2}\log(1/\epsilon)).
\end{array}
\]
These are generic upper-bound certificates.  The next section supplies
matching bounded-step lower bounds for the displayed reduced barriers.
A custom barrier on the affine slice or an algorithm outside that
feasible-step model can fall outside the comparison.

## Bounded-step iteration tax: the upper envelopes are essentially tight

Subsequent path-independent distance theorems upgrade the preceding
certificate comparison to an actual lower bound for the displayed reduced
standard barriers.  The scope is precise: start at the analytic center,
use at most \(m\) feasible chords per outer round, and bound each chord's
starting-point Dikin norm by \(R<1\).  No central-neighborhood condition is
imposed after initialization.

For the direct ball barrier, every point with
\(1-c^Tx\leq\epsilon\) has
\(1-\|x\|^2\leq2\epsilon\).  Its exact reduced parameter is one, so the
barrier-height argument gives

\[
 T_{\rm direct}\geq
 {\left[\log(1/(2\epsilon))\right]_+
  \over m\log(1/(1-R))}.                                \tag{0a}
\]

Now impose any Lorentz block-dimension cap \(3\leq d<N+1\), and put

\[
 b=\left\lceil{N-1\over d-2}\right\rceil,
 \qquad h=\left\lceil{N\over d-2}\right\rceil,
 \qquad \nu_{\rm tree}=2b-1-\chi_{N,d},                 \tag{0b}
\]

with \(\chi_{N,d}\) given by the exact root-incidence criterion in the
[norm-tree parameter theorem](2026-09-04-norm-tree-reduced-barrier-parameter.md).
The count-minimal norm-tree barrier and the smooth grouped barrier obey

\[
 \begin{aligned}
 T_{\rm tree}
 &\geq {\left[(b/\sqrt{\nu_{\rm tree}})
                 \log(1/(2\epsilon))\right]_+
          \over m\log(1/(1-R))},\\
 T_{\rm grouped}
 &\geq {\left[\sqrt h\log(1/(2\epsilon))\right]_+
          \over m\log(1/(1-R))}.
 \end{aligned}                                           \tag{0c}
\]

The first inequality is the exact-parameter sharpening of the
[norm-tree distance theorem](2026-09-04-norm-tree-short-step-iteration-lower-bound.md);
the second is the
[grouped-ball distance theorem](2026-09-04-grouped-ball-short-step-iteration-lower-bound.md).
Because \(h\in\{b,b+1\}\) and
\(\nu_{\rm tree}\in\{2b-2,2b-1\}\), both granular lower bounds are
\(\Theta(\sqrt h\log(1/\epsilon))\), versus
\(\Theta(\log(1/\epsilon))\) for the direct formulation.  The exact
central paths of all three displayed barriers can be partitioned into
matching-order bounded Dikin chords: the norm-tree path is independent of
tree shape and coincides with the grouped scalar profile after substituting
its block count.  Thus (0a)--(0c) are tight in both the square-root
compilation penalty and accuracy dependence for fixed \(R\).

All three latent Newton systems still solve in \(O(N)\) exact arithmetic.
Thus bounded-size cone compilation provides no asymptotic per-round solve
benefit on this family, while it forces an
\(\Omega(\sqrt{N/(d-2)})\) bounded-step iteration penalty relative to the
direct formulation, with a matching central-path construction.  This is a
genuine negative result for fixed-barrier
feasible-step QIPMs as well as classical IPMs.  It is not an arithmetic
lower bound for implicit iterates, a finite-precision theorem, or a lower
bound against long-step, infeasible, custom-barrier, or output-only
algorithms.

## One-hub Newton graph

For \(q=(t,z)\in\operatorname{int}Q_m\), put
\(\Delta=t^2-\|z\|_2^2\) and \(J=\operatorname{diag}(1,-I)\).  The standard
Lorentz barrier has Hessian
\[
 H(q)=-{2J\over\Delta}
       +{4(Jq)(Jq)^T\over\Delta^2}
      =D_q+w_qw_q^T,                                    \tag{1}
\]
where \(D_q=-2J/\Delta\) is diagonal and \(w_q=2Jq/\Delta\).
Introducing one scalar hub replaces \(H\) in the primal KKT system by
\[
 \begin{bmatrix}
 D&W&A^T\\
 W^T&-I&0\\
 A&0&0
 \end{bmatrix}.                                         \tag{2}
\]
Schur complementation of the hub block recovers the exact Newton system.
The low-treewidth Gaussian-elimination theorem therefore solves (2) in
\(O(V(\tau+1)^2)\) field operations when its graph has \(V\) vertices and a
fixed width-\(\tau\) decomposition is supplied.  No regularization,
no-cancellation hypothesis, or materialized dense Hessian is needed in exact
arithmetic.

## Proof of the three graph counts

### Direct cone

Use \(q=(t,x)\in Q_{N+1}\) and the equality row \(t=1\).  In (2), the hub is
adjacent to all \(N+1\) scalar cone coordinates, and the equality row is
adjacent only to \(t\).  This graph is a star with one extra leaf: it has
\(N+3\) vertices and is a tree, so its treewidth is one.  The boundary
primal fiber \(q=(1,x)\) and normalized dual contact \(q^*=(1,-y)\) are
globally smooth for \(x,y\in S^{N-1}\), proving bi-contact regularity.

The standard Lorentz logarithmic barrier has parameter two.  Conversely,
restrict any barrier on this cone to a two-dimensional linear section
\(Q_2\cong\mathbb R_+^2\).  Restriction preserves self-concordance and
logarithmic homogeneity with the same parameter, while every such barrier on
\(\mathbb R_+^2\) has parameter at least two.  Hence the optimum is exactly
two even when the barrier class is not restricted to normal barriers.

### Binary norm tree

Take a full rooted binary tree with \(N\) leaves and \(L=N-1\) internal
nodes.  Give every internal node \(v\) a block
\[
 q_v=(t_v,a_v,b_v)\in Q_3.
\]
If a child is internal, equate its axial coordinate to the corresponding
parent slot.  If it is a leaf, that parent slot is the projected coordinate
\(x_i\).  Fix the root axial coordinate to one.  Recursive elimination gives
exactly \(\|x\|_2\leq1\).

There are \(3L\) scalar cone-coordinate vertices, \(L\) hub vertices,
\(L-1\) two-coordinate link rows, and one root row, hence \(5L\) vertices.
Each hub is adjacent to its three cone coordinates; each link row subdivides the
unique edge between a parent slot and a child axial coordinate; and the root
row is a leaf.  The graph is connected and has
\[
 3L+2(L-1)+1=5L-1
\]
edges, so it is a tree and has treewidth one.

The equality matrix has full row rank: every link or root row has support
disjoint from every other such row.  Since the barrier Hessian is positive
definite, the KKT matrix and its one-hub expansion are nonsingular.

The Lorentz curvature-capacity theorem gives \(L\geq N-1\) for every exact
\(Q_3^L\)-lift of the ball.  The product \(Q_3^L\) has optimal ambient
barrier parameter \(2L\), even among coupled barriers, by restriction to
its orthant section.  Thus the norm tree simultaneously minimizes the
unrestricted \(Q_3\)-factor count and ambient barrier parameter.

The sharp phase-lift obstruction says that every bi-contact-regular exact
\(Q_3^L\)-lift of \(B_2^N\) has \(L\geq N\).  Therefore every count-optimal
\(L=N-1\) lift has a primal or dual contact-incidence defect: a global
nonsingular compact contact sheet is impossible.  For the norm tree this is
visible in the partial norms
\[
 t_v(x)=\left(\sum_{i\text{ below }v}x_i^2\right)^{1/2},
\]
which are nonsmooth wherever a proper subtree vanishes.

### Smooth coordinatewise lift

For \(i=1,\ldots,N\), introduce
\[
 q_i=(u_i,v_i,w_i)\in Q_3
\]
and impose
\[
 u_i+v_i=1,\qquad
 \sum_{i=1}^N(u_i-v_i)=1.                               \tag{3}
\]
Project by \(x_i=w_i\).  Writing \(s_i=u_i-v_i\), the Lorentz constraint and
the first equality are equivalent to \(s_i\geq x_i^2\).  Hence (3) projects
exactly to the ball.
At a boundary point, all inequalities are tight, so the primal fiber is
unique and polynomial:
\[
 q_i(x)=\left({1+x_i^2\over2},
              {1-x_i^2\over2},x_i\right).               \tag{4}
\]
The normalized dual contact factors
\[
 q_i^*(y)=\left({1+y_i^2\over2},
               -{1-y_i^2\over2},-y_i\right)             \tag{5}
\]
are also globally smooth.  Equations (4)--(5) give
\[
 \sum_i\langle q_i(x),q_i^*(y)\rangle=1-\langle x,y\rangle,
\]
and they come from actual normalized conic-dual certificates.  Namely, give
the local row \(u_i+v_i=1\) multiplier
\(\lambda_i(y)=y_i^2/2\) and the global row multiplier
\(\lambda_0(y)=1/2\).  Subtracting the lifted objective \(y_iw_i\) gives
exactly \(q_i^*(y)\), while the multiplier objective is
\(\sum_i\lambda_i+\lambda_0=1\).  The graph of these multipliers is a compact
smooth normalized-dual contact sheet.  Thus the lift is bi-contact-regular
and attains the sharp \(L=N\) count.
The same orthant-section argument makes its exact optimal ambient barrier
parameter \(2N\).

Let \(h_i\) be the one-hub vertex for block \(i\), \(r_i\) the row
\(u_i+v_i=1\), and \(g\) the global sum row.  The expanded graph has
\(3N+N+(N+1)=5N+1\) vertices.  A width-two decomposition consists of
\[
 \{g,u_i,v_i\},\quad
 \{u_i,v_i,h_i\},\quad
 \{u_i,v_i,r_i\},\quad
 \{h_i,w_i\}                                             \tag{6}
\]
for each \(i\).  Attach \(\{u_i,v_i,h_i\}\) and
\(\{u_i,v_i,r_i\}\) to \(\{g,u_i,v_i\}\), attach
\(\{h_i,w_i\}\) to \(\{u_i,v_i,h_i\}\), and connect the
\(\{g,u_i,v_i\}\) bags in a chain.  Conversely
\(\{g,h_i,r_i\}\) and \(\{u_i,v_i\}\) induce a \(K_{3,2}\), so the
treewidth is at least two.  Thus it is exactly two.

The \(N+1\) equality rows are independent.  Indeed, a dependence
\(\sum_i\alpha_i(u_i+v_i)+\beta\sum_i(u_i-v_i)=0\) has coefficients
\(\alpha_i+\beta=0\) on \(u_i\) and \(\alpha_i-\beta=0\) on \(v_i\), forcing
\(\alpha_i=\beta=0\).  Thus the KKT and one-hub systems are nonsingular.

This completes the theorem.

## Sparse-QIPM consequence

For a QIPM architecture that materializes the Newton direction or updated
iterate at every outer iteration, assume matched classical access to the
current cone coordinates and right-hand side and an outer theorem accepting
the same exact or certified-residual direction.  Replacing its quantum
linear solve by the fixed decompositions above costs \(O(N)\) arithmetic per
round and \(O(N)\) output writes for each formulation.  Consequently none of
the three ball representations yields a polynomial full-output quantum
advantage from its Newton solve alone.

The bounded-step theorem makes this total-work statement tight on the
fully active objective.  Under the explicit contract that every round
materializes its \(\Theta(N)\)-coordinate updated iterate, (0c) forces

\[
 \Omega\!\left(
   N\sqrt{\left\lceil{N\over d-2}\right\rceil}
   \log{1\over\epsilon}\right)                            \tag{7}
\]

word writes across a capped norm-tree or grouped run, for fixed \(R,m\) in
the nonvacuous accuracy regime.  The linear latent solve and matching
central-path chord construction attain the same order in exact arithmetic.
The direct formulation instead has matching
\(\Theta(N\log(1/\epsilon))\) full-output work.  Thus, under matched access
and mandatory per-round materialization, small-cone compilation has no
polynomial quantum advantage and pays the same square-root iteration tax in
total work.

The conclusion is deliberately limited to the isolated ball-lift graph, or
to larger models whose external coupling preserves the stated bounded-width
supergraph.  Dense external rows can dominate the graph.  The theorem does
not exclude coherent iterates, compressed or scalar output, quantum-only
data access, parallel-depth improvements, or finite-precision effects.
Equation (7) is an output-contract lower bound, not a quantum query lower
bound.

## Novelty and scope

The individual ingredients have precedents.  Binary norm trees and the
coordinatewise rotated-SOC inequalities \(s_i\geq x_i^2\) are standard
modeling devices.  Güler and Tunçel identify the optimal barrier parameter
of a homogeneous cone with its rank.  Fürer, Hoppen, and Trevisan give the
sharp exact low-treewidth elimination theorem.  The local notes
[exact Lorentz curvature](2026-09-04-exact-lorentz-curvature-budget.md),
[contact-regular lift topology](2026-09-04-contact-regular-lift-topology.md),
[smooth \(Q_3^N\) ball factorization](2026-09-04-smooth-q3n-ball-factorization.md),
and [latent Lorentz treewidth](2026-09-04-latent-treewidth-lorentz-newton-systems.md)
prove and audit the constituent lower bounds and constructions.
The exact root-leverage calculation for the reduced norm-tree column is in
[the norm-tree reduced-barrier theorem](2026-09-04-norm-tree-reduced-barrier-parameter.md);
the coordinate column follows from the exact paraboloid calculation in the
[ball-cap theorem](2026-09-04-ball-cap-latent-treewidth-pareto.md).

The new statement is their precise Pareto consequence: after rank expansion,
the high-dimensional direct cone and the smallest granular lift both have a
tree Newton graph, so granularity buys no asymptotic Newton sparsity but
forces an exact linear ambient-barrier penalty; within granular lifts, global
bi-contact regularity has an additional sharp one-factor penalty.  A
targeted search for this combined barrier--regularity--latent-treewidth
tradeoff found no direct match.  The later bounded-step corollary further
turns the reduced-barrier gap into an actual square-root iteration tax,
rather than inferring one from barrier parameters alone.  Riemannian
distance as a generic lower bound for short-step methods is classical
(Nesterov--Todd 2002; Nesterov--Nemirovski 2008); the candidate novelty is
the explicit distance-to-accurate-set comparison across these sparse ball
formulations.  Priority cannot be guaranteed by the targeted search.

Finite-precision factorization is not asserted.  Equation (2) is indefinite;
the exact low-treewidth theorem permits arbitrary pivots, but numerical
stability needs a quasidefinite two-hub regularization or separate pivot,
growth, precision, and refinement bounds.  In particular, the width-one
claims do not automatically transfer to the two-hub finite-precision branch.
The ambient barrier optima concern the cone product.  The reduced values in
(0) are exact for the displayed restricted standard barriers, not for the
best arbitrary barrier intrinsic to either affine slice.

## Audit record

An independent hostile audit verified all three exact lifts and
bi-contact-regularity claims; the lower bounds for arbitrary coupled ambient
barriers; all vertex, edge, and treewidth counts; full row rank and KKT
nonsingularity; the norm-tree connectivity and acyclicity argument; and the
\(K_{3,2}\) lower bound and explicit decomposition (6).  The audit required
the fixed-structural-supergraph convention, the proper incidence-sheet scope,
the explicit coordinate-lift dual multipliers, and the separation between
generic short-step upper envelopes and iteration lower bounds.  Those
corrections are incorporated above.  No mathematical defect remains.

A further independent audit verified the reduced ledger (0): the
logarithmic-homogeneity projection identity, Dikin axial-leverage bounds,
the exact two-internal-child root Schur inequality and both sharpness limits
for the norm tree, and the exact affine-slice dual norm for the coordinate
paraboloid barrier.  It confirmed the scope as a comparison of the displayed
barriers, not arbitrary intrinsic slice barriers.

A third hostile audit verified the path-independent iteration corollary
(0a)--(0c), including the direct barrier-height constant, the exact
norm-tree parameter coefficient, the grouped coefficient, all ceiling and
near-threshold cases, and the matching exact-central-path construction.
It confirmed that the square-root tax is for fixed reduced barriers and
bounded feasible Dikin chords, with no claim against the excluded
algorithmic models.

The same audit verified the matched full-output consequence (7): under the
stated per-round materialization contract, the iteration lower bound may be
multiplied by the \(\Theta(N)\) word-write cost, while the explicit central
path and precomputed subtree weights give the matching exact-real
\(O(N)\)-per-round construction.  It confirmed that this is neither bit
complexity nor a quantum query lower bound.
