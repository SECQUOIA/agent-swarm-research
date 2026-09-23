# Winner-take-all parity SDPs with one global trace budget

## Status

This note records the exact structural properties of the proposed \(G\)-component
construction.  A direct global trace row preserves the condition-one reduced Newton
system and a forest KKT graph, but has \(3G\) nonzeros.  A binary-sum extended
formulation reduces maximum row sparsity to three and maximum column sparsity to two.
It also preserves a forest KKT graph and the same projected SDP.  Its auxiliary
variables are free linear variables, however, so condition one remains exact in the
root-matrix coordinates but not in an orthonormal basis for the full augmented
variable space.  This distinction should not be suppressed.

## 1. Direct formulation and winner-take-all value

Take \(G\) copies of the qutrit signed-triangle path.  Component \(g\) has \(P=33N\)
blocks \(X_{g,i}\in\mathbb S_+^3\), six svec coordinates per block, and copy equations
\[
 X_{g,i}=D_{g,i}X_{g,i-1}D_{g,i}^T,\qquad 1\le i<P.       \tag{1}
\]
The transports are the public identities and the \(N\) private sign transports of
the one-component construction.  Let \(h_g\) be their product and let \(C_{g,i}\) be
the public baseline-\(3I\) costs from that construction.  Impose one budget
\[
                         \sum_{g=1}^G\operatorname{tr}X_{g,0}=1             \tag{2}
\]
and minimize
\[
                         {1\over P}\sum_{g=1}^G\sum_{i=0}^{P-1}
                         \langle C_{g,i},X_{g,i}\rangle.                    \tag{3}
\]

Eliminating the copies gives root matrices \(Z_g\succeq0\) and the exact problem
\[
 \min\left\{\sum_{g=1}^G\langle\overline C_{h_g},Z_g\rangle:
                 \sum_g\operatorname{tr}Z_g=1\right\},                    \tag{4}
\]
where
\[
 \lambda_{\min}(\overline C_{+})={29\over10},\qquad
 \lambda_{\min}(\overline C_{-})={14\over5}.                              \tag{5}
\]
Allocating all trace to a minimum-eigenvalue eigenspace proves
\[
 \operatorname{opt}(4)=\min_g\lambda_{\min}(\overline C_{h_g})
 =\begin{cases}
 29/10,&h_g=+1\text{ for every }g,\\
 14/5,&h_g=-1\text{ for at least one }g.
 \end{cases}                                                               \tag{6}
\]
Thus the scalar value is an OR of \(G\) hidden length-\(N\) parities.  Standard
adversary composition gives quantum raw-query complexity
\(\Theta(N\sqrt G)\) for constant-error value estimation, with a matching Grover
search over exact component-parity subroutines.  This query statement is auxiliary to
the structural audit below.

There are \(6PG\) scalar matrix variables, \(6G(P-1)\) copy rows, and one trace row.
The copy rows are independent by their successive-block identity pivots.  Their
kernel has dimension \(6G\), parametrized by the root matrices.  Row (2) is nonzero
on this kernel and is therefore independent, so the full equality matrix has rank
\[
                              6G(P-1)+1                                    \tag{7}
\]
and nullity \(6G-1\).

Every copy row has two nonzeros, and every matrix-variable column has at most two
nonzeros.  The sole defect is that (2) has \(3G\) nonzeros.  Calling the direct
formulation bounded-row-sparse when \(G\) grows would therefore be false.

## 2. Slater points and non-SOCP geometry

A public strict primal point is
\[
                              X_{g,i}^{0}={I_3\over3G}.                     \tag{8}
\]
Zero equality multipliers and positive-definite slacks \(C_{g,i}/P\) give strict
dual feasibility.  Hence both Slater conditions hold.

The feasible set is not second-order-cone representable.  Its exposed face defined
by \(\operatorname{tr}Z_1=1\) forces \(Z_g=0\) for \(g>1\) and is linearly
isomorphic to
\[
                         \{Z\succeq0:\operatorname{tr}Z=1\}.               \tag{9}
\]
If the full feasible set had a finite SOC lift, the same would hold for this exposed
face.  Compact homogenization of (9) would then give a finite SOC lift of
\(\mathbb S_+^3\), contradicting the known non-SOC-lift theorem.  This argument does
not rely on the optimum being attained in a particular component.

## 3. Public start and scalar root Hessian

For the product log-det barrier use \(\mu=1/(GP)\).  At (8),
\[
 g_{g,i}={1\over P}(C_{g,i}-3I),\qquad
 \mathcal H_{g,i}[Y]={9G\over P}Y.                         \tag{10}
\]
The start, equality residual, gradient, and unreduced Newton right-hand side are all
public.  After copy elimination, the physical root-coordinate Hessian is
\[
                              9G I                                        \tag{11}
\]
on \(\{(Y_g):\sum_g\operatorname{tr}Y_g=0\}\), so its condition number is exactly
one.  The common diagonal part of the gradient is orthogonal to this tangent, and the
root directions are
\[
                         \Delta Z_g=-{u\over9G}A_{h_g}.                    \tag{12}
\]
They preserve (2).  Since \(\|A_{h_g}\|\le2\),
\[
 \lambda_{\min}(I_3/(3G)+\Delta Z_g)
 \ge {1\over3G}-{2u\over9G}={14\over45G}>0,                              \tag{13}
\]
so the undamped primal step is strictly feasible.

The decrement and the standard self-concordant full-step bound are
\[
 \lambda^2
 =\sum_{g=1}^G\left\langle uA_{h_g},(9GI)^{-1}uA_{h_g}\right\rangle
 ={2u^2\over3}={1\over150},
 \qquad
 \lambda_{\rm next}\le {1\over(\sqrt{150}-1)^2}<{1\over126}.             \tag{13a}
\]
Here \(\|A_h\|_F^2=6\).  This scaling gives central-path duality-gap scale
\(\mu(3PG)=3\), independent of \(G,N\).  The displayed start has nonzero
decrement, so that number is not an exact primal--dual gap certificate at
the start itself.

Ignoring diagonal Hessian loops, the direct symmetric scalar KKT graph is already a
forest.  Each of the \(6G\) copy-coordinate systems is a subdivided path.  The global
trace multiplier joins the \(3G\) distinct diagonal-root paths through one star
vertex, creating one tree and no cycle; all \(3G\) off-diagonal paths remain separate.
Thus unbounded row degree, not treewidth, is the only graph-sparsity defect of (2).

## 4. A row-three binary trace-sum extension

Take any full binary tree with the \(3G\) root diagonal entries
\[
                         \xi_{g,a}=(X_{g,0})_{aa},qquad
                         1\le g\le G,\ 1\le a\le3                         \tag{14}
\]
as its leaves.  For each of its \(3G-1\) internal vertices \(v\), introduce one free
scalar \(s_v\).  If the two children of \(v\) carry scalars \(z_{v,L}\) and
\(z_{v,R}\) (a leaf \(\xi_{g,a}\) or a child variable \(s_w\)), impose
\[
                         s_v-z_{v,L}-z_{v,R}=0.                            \tag{15}
\]
For the root vertex \(r\), add \(s_r=1\).  Eliminating the tree variables gives
exactly (2).

The extended formulation has
\[
 \begin{array}{c|c}
 \text{scalar variables}&6PG+3G-1\\
 \text{equality rows}&6G(P-1)+3G\\
 \text{equality rank}&6G(P-1)+3G\\
 \text{nullity}&6G-1.
 \end{array}                                                               \tag{16}
\]
For rank, first pivot on successive matrix blocks in the copy rows.  The binary-tree
rows can then be pivoted bottom-up on their distinct output variables \(s_v\); after
those rows, the terminal equation is independent because it imposes the nonzero
functional \(\sum_{g,a}(Z_g)_{aa}\) on the root-matrix kernel.

Every binary-tree row has three nonzeros and the terminal row has one.  Maximum column
sparsity is two.  A root diagonal entry occurs in one outgoing copy row and its unique
parent sum row; every other matrix coordinate occurs in at most two copy rows; and
every internal \(s_v\) occurs in its defining row and either its parent's row or the
terminal row.  Every hidden input bit still changes only its two signed copy
coefficients.  Thus the entire displayed equality matrix has row sparsity at most
three and column sparsity at most two, independently of \(G\).

At the public point (8), set
\[
                         s_v^0={\#\{\text{leaves below }v\}\over3G}.       \tag{17}
\]
This satisfies all tree equations.  The \(s_v\)'s are free variables and carry no
barrier or objective term, so primal and dual Slater statements for the PSD blocks are
unchanged.  Eliminating both copies and tree variables gives exactly (4), (11), and
(12).

The symmetric scalar KKT sparsity graph remains a forest.  The bipartite
variable--multiplier graph of (15), together with the terminal multiplier, is a
subdivision of the chosen binary tree.  Each leaf is the root vertex of one previously
disjoint diagonal-coordinate path, so attaching those paths cannot create a cycle.
All off-diagonal coordinate paths remain separate.  Hence the graph has treewidth one
while every row and column has constant degree.

There is one important conditioning caveat.  In the root matrices alone, (11) is a
scalar identity.  In the full augmented Euclidean variable space, a feasible tangent
also contains
\[
                         \delta s_v=\sum_{(g,a)\text{ below }v}(Y_g)_{aa}. \tag{18}
\]
The map \((Y_g)\mapsto(Y_g,(\delta s_v)_v)\) is not an isometry, while the free
accumulators have zero barrier Hessian.  Therefore an orthonormal nullspace basis for
the full extended KKT formulation need not see a condition-one reduced Hessian.  The
bounded-degree gadget preserves the projected optimization problem, public start,
root-coordinate scalar Hessian, and forest graph, but not the stronger
representation-dependent claim of condition one in the full augmented Euclidean
metric.  The direct row (2) retains that stronger claim at the price of row degree
\(3G\).

## 5. Exact scope

The binary-sum gadget is a mixed SDP with free linear auxiliaries.  If a formulation
requires every scalar auxiliary to lie in a cone and includes its standard logarithmic
barrier, those extra barrier terms alter (11); a separate conditioning analysis is
then required.  Encoding each free scalar as a difference of two nonnegative variables
also introduces nonunique lifts and does not preserve the clean condition-one claim.
Thus (15) is the bounded-incidence winner for sparse KKT access, while (2) is the
winner for an exactly isometric, condition-one reduced primal barrier system.
