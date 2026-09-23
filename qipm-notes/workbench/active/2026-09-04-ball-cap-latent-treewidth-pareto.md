# Exact ball-cap frontier with treewidth-one Newton systems

Status: Proved; algebraically and graph-theoretically hostile-audited  
Started: 2026-09-04  
Paper status: Not incorporated  
Confidence: High in exact arithmetic and generic short-step accounting; finite-precision claims retain the stated regularization qualification

## Result

Let \(B_2^N\), \(N\geq3\), be represented by a product of proper cone
blocks of dimension at most \(d\), with global bi-\(C^1\) primal and polar
slack factors.  Charge a logarithmically homogeneous self-concordant barrier
on the full ambient product.  The saturated-block submersion theorem and
Browder's sphere-fibration theorem give the exact simultaneous structural
frontier

\[
\begin{array}{c|c|c|c}
\text{block cap}&k_{\min}&M_{\min}&\nu_{\min}\\ \hline
3\leq d<N+1&
\displaystyle\left\lceil {N\over d-2}\right\rceil&
\displaystyle N+2\left\lceil {N\over d-2}\right\rceil&
\displaystyle 2\left\lceil {N\over d-2}\right\rceil\\[2mm]
d\geq N+1&1&N+1&2.
\end{array}                                                   \tag{1}
\]

Here \(k\) is the number of positive-capacity blocks,
\(M\) is their total cone-space dimension, and \(\nu\) is the least
possible full-product barrier parameter.  The first row has a strict extra
curvature channel: if every block has dimension below \(N+1\), then

\[
                         \sum_i(\dim K_i-2)_+\geq N,            \tag{2}
\]

not merely \(N-1\).

The grouped Lorentz construction attaining the first row has an even
stronger algorithmic property.  After eliminating its block-local affine
equalities, the fixed structural supergraph of the exact one-hub Newton
matrix is a tree:

\[
 \boxed{\ |V_1|=N+2k+1,\qquad |E_1|=N+2k,\qquad
         \operatorname{tw}(G_1)=1.\ }                          \tag{3}
\]

A positive-diagonal signed two-hub expansion, suitable for the
quasidefinite regularized factorization, has

\[
 \boxed{\ |V_2|=N+3k+1,\qquad |E_2|=2N+3k,\qquad
         \operatorname{tw}(G_2)=2.\ }                          \tag{4}
\]

Thus the dense Lorentz Hessian blocks can be solved in
\(O(N+k)=O(N)\) exact field operations per Newton step.  With

\[
                   k_d=\left\lceil {N\over d-2}\right\rceil
                   \qquad(3\leq d<N+1),                       \tag{5}
\]

the generic ambient-product short-step accounting becomes

\[
 \boxed{\quad
 O\!\left((N+k_d)\sqrt{k_d}\,
          \log{\Delta\over\epsilon}\right)
 =O\!\left(
 N\sqrt{\left\lceil {N\over d-2}\right\rceil}
 \log{\Delta\over\epsilon}\right).\quad}                       \tag{6}
\]

The same construction has an exact reduced separable barrier parameter
\(\nu_{\rm red}=k_d\), half its optimal ambient logarithmically homogeneous
parameter.  This changes only the suppressed constant in (6), but gives an
exact ambient-versus-reduced barrier distinction.

There is also an exact comparison with recursive norm trees under the same
cap.  Let
\(L_0=\lceil(N-1)/(d-2)\rceil\) be their minimum factor count.  The
restricted standard barrier of a count-minimal norm tree has parameter
\(2L_0-1-\chi_{N,d}\), with \(\chi_{N,d}\in\{0,1\}\) determined by whether
all root slots can be internal.  Since
\(k_d\in\{L_0,L_0+1\}\), the present smooth grouped lift always has weakly
smaller reduced parameter and usually improves it by an asymptotic factor
of two, while using at most one additional block.  The exact incidence
criterion and equality cases are proved in
[the capped norm-tree theorem](2026-09-04-norm-tree-reduced-barrier-parameter.md).

For \(d\geq N+1\), the direct \(Q_{N+1}\) lift has a
treewidth-one reduced Newton graph and gives

\[
                         O\!\left(N\log{\Delta\over\epsilon}\right). \tag{7}
\]

Equations (1), (3), and (6) give a cap-dependent Pareto theorem: increasing
the maximum cone dimension reduces the certified short-step count, while
the classical structured Newton solve remains linear throughout.

## The grouped lift

Assume \(3\leq d<N+1\), put \(c=d-2\), and partition the \(N\) coordinates
into \(k=k_d\) nonempty groups \(G\), with sizes

\[
                         g_G=|G|\leq c,\qquad \sum_Gg_G=N.
\]

For each group introduce

\[
                     q_G=(u_G,v_G,w_G)\in Q_{g_G+2}
\]

and impose

\[
                  u_G+v_G=1,\qquad
                  \sum_G(u_G-v_G)=1.                           \tag{8}
\]

The projected coordinate is \(x_G=w_G\).  Set
\(s_G=u_G-v_G\).  The first equality in (8) gives

\[
       u_G={1+s_G\over2},\qquad v_G={1-s_G\over2},
\]

and the Lorentz constraint becomes

\[
                     s_G\geq\|w_G\|^2.
\]

Consequently the relative interior of the reduced formulation is

\[
 \sum_Gs_G=1,\qquad s_G>\|w_G\|^2,                             \tag{9}
\]

which projects to \(\sum_G\|w_G\|^2<1\); replacing both strict inequalities
by non-strict ones gives the exact closed lift of \(B_2^N\).  Restricting the
standard Lorentz product barrier to (8) gives

\[
                   F(s,w)=-\sum_G\log q_G,\qquad
                   q_G=s_G-\|w_G\|^2.                          \tag{10}
\]

The reduced barrier in (10) has exact self-concordance parameter \(k\), both
on the product of open paraboloids and after restriction to the final affine
equation \(\sum_Gs_G=1\).  This is the parameter of this particular
separable non-logarithmically-homogeneous barrier.  It is also optimal among
all possibly coupled self-concordant barriers on the affine slice: fixing
positive allocation variables and one coordinate direction per group gives
an affine \(k\)-cube section, whose optimal barrier parameter is \(k\).
The full proof is recorded in
[Coupling cannot lower the barrier parameter of the grouped ball
slice](2026-09-04-coupled-barrier-grouped-ball-slice.md).  By contrast,
the full-product lower bound in (1) proves that \(2k\) is the optimal
**ambient-product logarithmically homogeneous** parameter for this cap.

To verify the reduced parameter, consider one block
\(f(s,w)=-\log(s-\|w\|^2)\).  Along any line, normalize at the point by
\(a=q'/q\) and \(c=2\|\dot w\|^2/q\geq0\).  Then
\[
 f''=a^2+c,\qquad f'''=-2a^3-3ac,
\]
and
\[
 4(a^2+c)^3-(2a^3+3ac)^2=3a^2c^2+4c^3\geq0.              \tag{10b}
\]
Thus the block is standard self-concordant.  Directly solving with the
Hessian (11) gives
\[
 H_G^{-1}\nabla f_G=(-q_G,0),\qquad
 \|\nabla f_G\|_{H_G^{-1}}^2=1,
\]
so its exact barrier parameter is one and the product parameter is exactly
\(k\).  Restriction preserves self-concordance and the gradient bound.  On
the tangent space of \(\sum_Gs_G=1\), the squared dual gradient norm is
\[
 k-{(\sum_Gq_G)^2\over
       \sum_Gq_G(s_G+\|w_G\|^2)}.                          \tag{10c}
\]
Taking \(s_G=1/k\) and
\(\|w_G\|^2=1/k-\varepsilon\) makes (10c) tend to \(k\),
proving exactness even on the final slice.

The construction also attains the regularity hypothesis in (1).  On the
contact sphere its unique primal boundary fiber and a normalized dual factor
are, blockwise,
\[
\begin{aligned}
 A_G(x)&=\left({1+\|x_G\|^2\over2},
               {1-\|x_G\|^2\over2},x_G\right),\\
 B_G(y)&=\left({1+\|y_G\|^2\over2},
              -{1-\|y_G\|^2\over2},-y_G\right).
\end{aligned}                                             \tag{10d}
\]
They are globally polynomial and
\[
 \langle A_G(x),B_G(y)\rangle={1\over2}\|x_G-y_G\|^2.
\]
Summing gives \(1-x^Ty\).  The dual factors arise from the smooth equality
multipliers \(\lambda_G=\|y_G\|^2/2\) and
\(\lambda_0=1/2\), so both contact incidences contain global nonsingular
smooth sheets.

## Exact one-hub graph

For one reduced block write

\[
            \zeta_G=(s_G,w_G),\qquad
            a_G=(1,-2w_G).
\]

Direct differentiation of (10) gives the exact identity

\[
 \nabla^2[-\log(s_G-\|w_G\|^2)]
   =
   \underbrace{\operatorname{diag}
       \left(0,{2\over q_G}I_{g_G}\right)}_{D_G}
   +{1\over q_G^2}a_Ga_G^T.                                  \tag{11}
\]

This can also be obtained by restricting the one-hub Lorentz identity
through the affine map

\[
 T_G:\ (s_G,w_G)\longmapsto
       \left({1+s_G\over2},{1-s_G\over2},w_G\right).
\]

Introduce one hub \(h_G\) for the rank-one term and one row vertex
\(\lambda\) for \(\sum_Gs_G=1\).  The structural edges are exactly

\[
            \lambda-s_G,\qquad s_G-h_G,\qquad
            h_G-w_{Gj}\quad(j\in G).                           \tag{12}
\]

Thus this fixed structural supergraph is the tree obtained by attaching, for
each \(G\), the
two-edge stem

\[
                       \lambda-s_G-h_G
\]

and the \(g_G\) leaves \(w_{Gj}\) at \(h_G\).  It contains

\[
\begin{aligned}
\text{primal vertices}&=N+k,\\
\text{hub vertices}&=k,\\
\text{equality-row vertices}&=1,
\end{aligned}
\]

which proves the vertex and edge counts and treewidth in (3).

The diagonal \(D_G\) has a zero in the \(s_G\) coordinate.  This causes no
problem for the exact-arithmetic low-treewidth linear-system theorem: the
full augmented Newton matrix is nonsingular because the restricted barrier
Hessian is positive definite and the single equality row has full rank.
The theorem tolerates arbitrary pivoting and algebraic cancellations.  It
does mean that (11) alone is not the positive-diagonal quasidefinite
expansion used for the finite-precision branch.

## Positive-diagonal two-hub graph

Use the signed two-hub Lorentz identity before applying the affine
restriction \(T_G\).  Write \(J_G=DT_G\) for its constant full-column
Jacobian.  Then

\[
        H_G=\bar D_G+\bar a_G\bar a_G^T-\bar v_G\bar v_G^T,
 \qquad
        \bar D_G=J_G^T\left({2\over q_G}I\right)J_G
        =\operatorname{diag}
          \left({1\over q_G},{2\over q_G}I_{g_G}\right)\succ0. \tag{13}
\]

The original identity has \(D-vv^T\succ0\), so congruence by the full-column
Jacobian \(J_G\) gives

\[
                         \bar D_G-\bar v_G\bar v_G^T\succ0.     \tag{14}
\]

The corresponding regularized KKT augmentation is therefore symmetric
quasidefinite.  Its fixed structural supergraph has two hubs
\(h_G^+,h_G^-\), each adjacent to \(s_G\) and every coordinate of \(w_G\),
plus the edge \(\lambda-s_G\).

For each \(G\), bags

\[
       \{h_G^+,h_G^-,s_G\},\qquad
       \{h_G^+,h_G^-,w_{Gj}\},\qquad
       \{\lambda,s_G\}
\]

give a width-two decomposition; connect all groups through a singleton
\(\{\lambda\}\) bag.  Conversely, because \(g_G\geq1\),

\[
       h_G^+-s_G-h_G^--w_{Gj}-h_G^+
\]

is a cycle, so the graph is not a forest.  Its treewidth is exactly two.
Counting two hub edges per reduced primal coordinate and the \(k\) equality
edges proves (4).

With the usual small negative regularization on the equality multiplier,
the pivot-free \(LDL^T\) factorization, storage, and subsequent triangular
solves are all \(O(N+k)\).  This is an exact real-arithmetic structural
claim.  Converting the regularized direction into a certified direction
for the unregularized Newton system still requires the inverse-norm,
working-precision, residual, and refinement conditions in the latent
treewidth theorem.

## Direct-cone branch

When \(d\geq N+1\), use

\[
                         (t,x)\in Q_{N+1},\qquad t=1.
\]

After eliminating \(t\), the barrier is

\[
                         -\log(1-\|x\|^2),
\]

with Hessian

\[
 {2\over1-\|x\|^2}I+
 {4\over(1-\|x\|^2)^2}xx^T.                                 \tag{15}
\]

This is already a positive-diagonal one-hub expansion.  Its fixed structural
supergraph is a star with \(N+1\) vertices and \(N\) edges, hence treewidth
one.  Both the exact and quasidefinite branches take \(O(N)\) arithmetic per
step.

## Raw conic structural graph before equality elimination

The reduced graph is the relevant minimal Newton graph, but the
uneliminated equality-form counts are also exact and provide a check on the
reduction.  In the raw formulation (8), \(M=N+2k\) scalar cone coordinates
and \(p=k+1\) equality rows are retained.

With one hub per cone, the fixed structural supergraph has

\[
             |V_1^{\rm raw}|=N+4k+1,\qquad
             |E_1^{\rm raw}|=N+6k,\qquad
             \operatorname{tw}(G_1^{\rm raw})=2.              \tag{16}
\]

For a group, the vertices \(u_G,v_G\) and the three vertices consisting of
the cone hub, local row, and global row induce \(K_{2,3}\), which has
treewidth two.  Bags \(\{u_G,v_G,a\}\), one for each of those three
vertices \(a\), together with leaf bags for \(w_G\), give the matching upper
bound.  Different groups meet only through the global row.

With two hubs per cone, the fixed structural supergraph has

\[
             |V_2^{\rm raw}|=N+5k+1,\qquad
             |E_2^{\rm raw}|=2N+8k,\qquad
             \operatorname{tw}(G_2^{\rm raw})=3.              \tag{17}
\]

A width-three decomposition uses a core
\(\{h_G^+,h_G^-,u_G,v_G\}\), a bag
\(\{\lambda,\lambda_G,u_G,v_G\}\), and size-three leaf bags for the
\(w_G\)'s.  The lower bound follows from a subdivision of \(K_4\) with
branch vertices \(u_G,v_G,h_G^+,h_G^-\): use a row vertex for the
\(u_G-v_G\) path and one \(w_G\) coordinate for the
\(h_G^+-h_G^-\) path.  Eliminating the \(k\) local rows and their paired
affine directions reduces (16)--(17) to (3)--(4).

All exact treewidth lower bounds here concern these fixed structural
supergraphs, equivalently a generic interior point where the displayed hub
coefficients are nonzero.  At a special iterate such as \(w=0\), numerical
zeros can delete hub edges and reduce the actual graph; they never invalidate
the stated decompositions or arithmetic upper bounds.

## Cap-dependent generic arithmetic

The standard ambient Lorentz product barrier has \(\nu=2k\), while the exact
reduced barrier (10) has \(\nu=k\).  Either route therefore gives, with only
the conventional constant differing, a generic short-step bound of

\[
                  O\!\left(\sqrt{k}\log{\Delta\over\epsilon}\right)
                                                                    \tag{18}
\]

Newton steps, with conventional constants suppressed.  Equations (3)--(4)
make each exact or conditionally regularized step \(O(N+k)\), proving (6).
Some representative regimes are

\[
\begin{array}{c|c|c}
d&k_d&\text{generic structured arithmetic}\\ \hline
3&N&O(N^{3/2}\log(\Delta/\epsilon))\\
\Theta(N^\alpha),\ 0<\alpha<1&
\Theta(N^{1-\alpha})&
O(N^{(3-\alpha)/2}\log(\Delta/\epsilon))\\
\Theta(N)&\Theta(1)&O(N\log(\Delta/\epsilon))\\
\geq N+1&1&O(N\log(\Delta/\epsilon)).
\end{array}                                                    \tag{19}
\]

The second-to-last row assumes the cap remains below \(N+1\).

This is optimal in the following precise, limited sense.  For every
bi-\(C^1\) product representation under the same cap, (1)--(2) give the
least possible \(k,M,\nu\) that can be inserted into the standard
ambient-product short-step certificate.  A method that materializes an
\(N\)-coordinate projected Newton direction already performs
\(\Omega(N)\) word writes per iteration.  The grouped construction attains
linear \(O(N)\) structured solve time.  Therefore neither a different
optimal representation nor a quantum linear solver can improve the
per-iteration dependence on \(N\) by a polynomial factor in a
materializing architecture.

This paragraph is **not** an iteration lower bound.  The
\(O(\sqrt{\nu}\log(\Delta/\epsilon))\) theorem is a generic upper guarantee;
a special path-following analysis, a custom barrier on the affine slice, or
a non-materializing algorithm may use fewer iterations or a different cost
model.

## Can an arbitrary optimal representation have smaller latent treewidth?

Three distinct statements must not be conflated.

1. **For the grouped Lorentz formulation**, the exact one-hub treewidth is
   one, the smallest possible value for its connected nontrivial Newton
   graph.  Another Lorentz formulation cannot improve its asymptotic
   \(O(N)\) materializing solve cost, though it may change constants or
   eliminate some auxiliary vertices.

2. **For arbitrary Lorentz formulations**, the one-hub identity always
   supplies a latent graph, but (1) does not constrain how the affine slice
   is wired.  An optimal \(k,M,\nu\) formulation might also have treewidth
   one, or might have larger treewidth.  No uniqueness of the grouped lift
   is proved or needed.

3. **For arbitrary proper cone products**, “one-hub latent treewidth” is not
   an intrinsic invariant.  A non-Lorentz barrier Hessian may have no
   diagonal-plus-one-rank representation at all.  The curvature,
   submersion, and barrier arguments prove (1), but they do not prove a
   treewidth lower bound for those Hessians or their KKT formulations.

Thus it is valid to say that the grouped construction attains the exact
structural frontier with the minimum nonzero latent treewidth and
output-optimal linear per-step arithmetic.  It is not valid to say that all
optimal cone lifts are graph-isomorphic to it or that arbitrary proper-cone
barriers must have the same latent graph.

## QIPM consequence

Consider a hybrid QIPM that uses the standard ambient product barrier,
constructs each Newton system under matched classical/quantum entry access,
and materializes an \(N\)-coordinate direction or iterate before the next
outer step.  Replacing its quantum linear solve by the treewidth-one exact
solver gives the same admissible Newton direction in \(O(N+k_d)=O(N)\)
field operations per round.  Under the regularization and precision
hypotheses above, the width-two quasidefinite solver gives the same
asymptotic replacement.

Hence this entire exact ball-cap Pareto family has no polynomial
linear-solve advantage for a materializing QIPM, even though a naively
materialized Lorentz Hessian contains cliques of size \(g_G+1\) and can have
treewidth \(\Theta(d)\).  The statement does not exclude coherent
non-materializing QIPMs, scalar or sampled output, quantum-only instance
access, custom projected barriers, or improvements in parallel depth.

## Hostile audit

The audit checked the following possible failure modes.

- **Wrong slice barrier.**  Since
  \(u_G^2-v_G^2=(u_G-v_G)(u_G+v_G)=s_G\), restricting the Lorentz
  determinant gives exactly \(q_G=s_G-\|w_G\|^2\).
- **Missing Hessian term.**  For \(q=s-\|w\|^2\),
  \(\nabla q=(1,-2w)\) and
  \(\nabla^2q=\operatorname{diag}(0,-2I)\); hence
  \(\nabla^2(-\log q)=q^{-2}\nabla q\nabla q^T-q^{-1}\nabla^2q\),
  which is (11).
- **Ambient versus reduced parameter.**  The explicit calculation
  (10b)--(10c) shows that the displayed reduced separable barrier has exact
  parameter \(k\), including after the final affine restriction.  This does
  not prove that \(k\) is optimal among all coupled slice barriers.  The exact
  value \(2k\) in (1) is instead the minimum logarithmically homogeneous
  parameter on the full ambient product, as required by the stated ambient
  accounting model.
- **Regularity of the grouped lift.**  The polynomial factors (10d), their
  exact slack identity, and the explicit dual multipliers supply the global
  bi-\(C^1\) contact sheets needed to attain the first row of (1).
- **Singular diagonal base.**  It affects only the convenient
  quasidefinite proof, not the exact augmented system.  Congruencing the
  full Lorentz two-hub identity by the affine map's full-column Jacobian,
  rather than by the affine map itself, supplies the positive diagonal (13)
  and the strict inequality (14).
- **Treewidth underestimated.**  The one-hub edge list is a connected graph
  with \(|E|=|V|-1\) and no cross-group edge except through \(\lambda\), so
  it is a tree.  The two-hub graph has the explicit width-two decomposition
  and an explicit cycle lower bound.
- **Raw/reduced counts mixed.**  Equations (3)--(4) count the
  equality-eliminated Newton systems; (16)--(17) separately count the
  original conic equality form.  All lower bounds are for fixed structural
  supergraphs; special numerical zeros can only delete edges.
- **Overstated optimality.**  Exactness is claimed for \(k,M,\nu\), and the
  construction's graph counts.  No universal treewidth lower bound is
  claimed for arbitrary proper-cone barriers, and no worst-case iteration
  lower bound is inferred from \(\nu\).

No algebraic or graph-theoretic counterexample was found.
