# Dense-open contact regularity does not imply the global capacity gap

Status: Proved; independently hostile-audited  
Started: 2026-09-04  
Paper status: Not incorporated  
Confidence: High

## Result

The global primal-and-dual \(C^1\) selection hypothesis in the
support-orbit covering theorem cannot be replaced by any of the following
conditions alone:

- an exact semialgebraic affine lift with Slater points;
- unique primal lift points over the whole boundary;
- globally Lipschitz semialgebraic primal and dual contact factors; or
- primal and dual factors that are real analytic on a dense open contact
  stratum whose complement has codimension at least two.

For every \(N\geq2\), the Euclidean ball \(B_2^N\) has an exact affine lift
over \(N-1\) copies of the three-dimensional Lorentz cone \(Q_3\).  Its
universal curvature budget is exactly saturated:

\[
             \sum_{j=1}^{N-1}(\dim Q_3-2)=N-1.
\]

Both primal and dual maps in the induced full-slack factorization have the
regularity listed above.  Consequently, even global Lipschitz regularity,
dense-open stratification, semialgebraic normalization, or generic
smoothness by itself cannot turn the local capacity bound into the strict
global bound.  The defect set is not a technical artifact: normalized
support rays lose properness there, exactly preventing the generic local
diffeomorphism from becoming a covering.  This defect mechanism is needed
in the nontrivial small-block cases \(N\geq3\); for \(N=2\), or for the
direct one-node \(Q_{N+1}\) star, the contact selection is globally analytic
and already has the saturated block profile allowed by the global rigidity
theorem.

This gives a concrete obstruction to an unconditional block-cap lower bound
for affine symmetric-cone lifts.  In particular, with block-dimension cap
\(d=3\), and therefore under any cap \(d\geq3\), an unconditional claim

\[
             \sum_j(\dim K_j-2)_+\geq N
\]

is false: the norm tree attains \(N-1\).

The sharp unconditional theorem therefore remains the local one.  Combining
the definable-lift curvature bound with arbitrary-arity Lorentz norm trees,
the exact simultaneous resource minima under an irreducible symmetric-cone
dimension cap \(d\geq3\) are

\[
\boxed{
 k_\min=\left\lceil\frac{N-1}{d-2}\right\rceil,\qquad
 M_\min=N-1+2k_\min,\qquad
 \nu_\min=2k_\min .}                              \tag{0}
\]

These are the \(N-1\) formulas in the
[symmetric-cone curvature theorem](2026-09-04-symmetric-cone-curvature-capacity.md),
not the conditional \(N\) formulas from global support-orbit regularity.
The construction below explains geometrically why the former cannot be
improved for arbitrary affine lifts.

## Binary-tree lift

Fix a rooted full binary tree \(T\) with \(N\) leaves, labelled by the
coordinates \(x_1,\ldots,x_N\).  For every node \(v\), let \(S_v\) be its
set of descendant leaves.  A leaf \(i\) carries the signed value
\(t_i=x_i\).  Every internal node \(v\) carries a nonnegative auxiliary
\(t_v\), except that the root value is fixed to \(t_\mathrm{root}=1\).
For an internal node with children \(v_0,v_1\), impose

\[
                    (t_v,t_{v_0},t_{v_1})\in Q_3,
 \qquad
 Q_3=\{(a,b,c):a\geq\sqrt{b^2+c^2}\}.             \tag{1}
\]

There are exactly \(N-1\) internal nodes and hence \(N-1\) Lorentz
blocks.  Recursing through (1) gives

\[
                       1=t_\mathrm{root}\geq\|x\|_2.
\]

Conversely, if \(\|x\|_2\leq1\), setting

\[
                       t_v=\|x_{S_v}\|_2                 \tag{2}
\]

at every nonroot internal node satisfies all constraints.  Thus the lift
projects exactly to \(B_2^N\).  It is strictly feasible: at \(x=0\), choose
strictly positive internal values that decrease sufficiently from each
parent to its children.

Boundary fibers are unique.  Indeed, telescoping the squared cone slacks
gives

\[
  1-\|x\|_2^2
   =\sum_{v\ {\rm internal}}
       \bigl(t_v^2-t_{v_0}^2-t_{v_1}^2\bigr),             \tag{3}
\]

where at a leaf \(t_i^2=x_i^2\).  Every summand is nonnegative.
When \(\|x\|_2=1\), all summands vanish, and nonnegativity of the
internal leading coordinates forces exactly (2).

The same construction gives all caps in (0).  Allow an internal node \(v\)
to have \(b_v\geq2\) children and replace (1) by one
\(Q_{b_v+1}\) constraint.  Every rooted tree with \(N\) leaves satisfies

\[
                   \sum_{v\ \mathrm{internal}}(b_v-1)=N-1. \tag{3a}
\]

Partition \(N-1\) into
\(k=\lceil(N-1)/(d-2)\rceil\) positive parts at most \(d-2\), and choose
a tree whose internal arities minus one are those parts.  Then all cone
dimensions are at most \(d\), while

\[
 \sum_v\dim Q_{b_v+1}=N-1+2k,
 \qquad \sum_v\nu(Q_{b_v+1})=2k.                         \tag{3b}
\]

The uniqueness, telescoping, and codimension-two analysis below extends
word for word, with the two child terms replaced by a sum over all
children.  We retain the binary notation because it displays the defect
mechanism most transparently.

## Telescoping full-slack factorization

For \(x,y\in S^{N-1}\), define node values

\[
 t_i=x_i,\quad s_i=y_i \quad(i\ {\rm a\ leaf}),
 \qquad
 t_v=\|x_{S_v}\|_2,\quad s_v=\|y_{S_v}\|_2
 \quad(v\ {\rm internal}).                            \tag{4}
\]

At the root, \(t_v=s_v=1\).  For every internal node set

\[
 A_v(x)=(t_v,t_{v_0},t_{v_1}),\qquad
 B_v(y)=(s_v,-s_{v_0},-s_{v_1}).                            \tag{5}
\]

Both vectors lie on \(\partial Q_3\).  Their pairings telescope:

\[
\begin{aligned}
 \sum_{v\ {\rm internal}}\langle A_v(x),B_v(y)\rangle
 &=\sum_{v\ {\rm internal}}
       \bigl(t_vs_v-t_{v_0}s_{v_0}-t_{v_1}s_{v_1}\bigr)\\
 &=t_\mathrm{root}s_\mathrm{root}-\sum_{i=1}^Nx_iy_i
  =1-\langle x,y\rangle .                              \tag{6}
\end{aligned}
\]

The cancellation in (6) is an identity in all affine lift variables.
Therefore the \(B_v(y)\) are also feasible conic dual certificates for
the affine lift, not merely an abstract slack factorization.

The maps in (4)--(5) are globally Lipschitz in the ambient Euclidean
metrics and semialgebraic.  Indeed, a leaf coordinate is linear and every map
\(x\mapsto\|x_{S_v}\|_2\) is \(1\)-Lipschitz.  Since the child subtrees
partition \(S_v\),

\[
 \|A_v(x)-A_v(x')\|_2,\ \|B_v(x)-B_v(x')\|_2
 \leq\sqrt2\,\|x_{S_v}-x'_{S_v}\|_2.                    \tag{6a}
\]

Thus the concatenated maps for the \(N-1\) binary-tree nodes are globally
\(\sqrt{2(N-1)}\)-Lipschitz.  For an arbitrary-arity tree with \(k\)
internal nodes, the same argument gives \(\sqrt{2k}\).  Let

\[
 U_T=S^{N-1}\setminus
 \bigcup_{\substack{v\ {\rm internal}\\v\neq\mathrm{root}}}
       \{x:x_{S_v}=0\}.                                  \tag{7}
\]

Every proper internal subtree has at least two leaves.  Hence each deleted
set has codimension \(|S_v|\geq2\) in the sphere.  The set \(U_T\) is
dense and open, and all factors in (5) are real analytic on \(U_T\).
The same statement holds independently on the polar sphere for the dual
factors.  Thus both primal and dual maps are analytic on dense open strata,
with singular locus of codimension at least two.

At a contact \(x=y\), every summand in (6) vanishes separately.  On
\(U_T\), mixed differentiation therefore produces \(N-1\) rank-one
Lorentz channels whose sum is the rank-\(N-1\) tangent metric.  Generic
capacity is genuinely saturated; the example does not evade the local
theorem by wasting a channel on the regular stratum.  The usual
common-kernel argument therefore makes the joint normalized support map
from \(U_T\) to \((S^1)^{N-1}\) a local diffeomorphism.  What fails is its
global proper completion, not its generic differential.

## The two-block three-dimensional witness

The mechanism is already complete for \(N=3\).  Put

\[
 u=\sqrt{x_1^2+x_2^2},\qquad v=\sqrt{y_1^2+y_2^2}.
\]

The affine lift is

\[
       (u,x_1,x_2)\in Q_3,\qquad (1,u,x_3)\in Q_3.    \tag{8}
\]

On the two boundary spheres its full slack factors as

\[
\begin{aligned}
 A_1(x)&=(u,x_1,x_2),&B_1(y)&=(v,-y_1,-y_2),\\
 A_2(x)&=(1,u,x_3),&B_2(y)&=(1,-v,-y_3),                       \tag{9}\\
 \langle A_1,B_1\rangle+\langle A_2,B_2\rangle
   &=1-\langle x,y\rangle .
\end{aligned}
\]

The unique primal boundary selection is continuous everywhere and analytic
away from the north and south poles.  On that punctured sphere, the first
normalized boundary-ray map records the azimuthal angle, while the second
records the polar angle.  Their joint map is a local diffeomorphism from a
cylinder onto an open cylinder in \(S^1\times S^1\), not a covering of the
torus.  As a pole is approached, the first block tends to the cone vertex
and its azimuthal support becomes undefined.  Equivalently, the generic
support map is not proper: sequences escaping an end of the punctured
sphere have convergent images.

This codimension-two collapse is precisely what a dense-open argument
cannot repair.  Taking a graph closure or a semialgebraic normalization
does not restore a single support value at the pole: the limiting support
circle depends on azimuth.

## Consequences for possible upgrades

The construction rules out an unconditional strict capacity gap for exact
affine lifts over products of symmetric cones.  It also shows that the
following proposed bridges are insufficient:

1. **Definable choice.** Semialgebraic choice supplies piecewise analytic
   contact factors, but (5) already has that property and still saturates.
2. **Discarding lower-dimensional strata.** The bad set here has
   codimension two, yet it carries the entire obstruction to completing the
   support map.
3. **Normalization or monodromy of the generic graph.** The normalized
   support graph acquires noncompact ends over the defect points; there is
   no proper same-dimensional map to which the covering argument applies.
4. **Unique primal boundary fibers.** Equation (3) proves uniqueness, but
   the unique section is not differentiable where an internal subtree
   vanishes.
5. **Global Lipschitz factor selections.** Inequality (6a) gives them
   explicitly on both sides of the full slack, but Lipschitz regularity does
   not supply a differentiable phase at a collapsed subtree.

A valid lift-level strengthening must impose a genuinely global condition,
for example a proper contact sheet with nonsingular projection as in
bi-contact regularity, or an equivalent extension/properness condition on
all normalized support-orbit maps.  Generic smoothness, even with tame
codimension-two singularities, is not enough.

## Literature boundary

Binary Lorentz norm trees and their Schur-complement formulations are
standard SOCP constructions.  The point recorded here is not the lift
itself, but its role as a sharp counterexample to a tempting regularity
upgrade of the saturated support-orbit theorem.  The explicit telescoping
dual factors, unique-boundary-fiber identity (3), codimension-two analytic
stratification, and failure-of-properness diagnosis make the obstruction
checkable without appealing to a selection theorem.

For general convex projections, continuous right inverses are known to
require additional hypotheses.  Akemann--Shell--Weaver, *Locally
nonconical convexity*, arXiv:math/0005194, prove that locally nonconical
compact convex sets have open linear projections and hence continuous
sections, while also exhibiting the limitations without that condition.
That selection literature is consistent with, but not needed for, the
explicit norm-tree obstruction above.

## Independent hostile audit

The audit checked the construction at the affine-lift level, not only as a
formal slack identity.  For a node of arbitrary arity \(b_v\), the constraint
\[
       (t_v,(t_c)_{c\text{ child of }v})\in Q_{b_v+1}
\]
has squared slack \(t_v^2-\sum_ct_c^2\).  Summing these slacks cancels every
nonroot internal square and leaves \(1-\|x\|^2\).  Thus a boundary point
forces every node constraint to equality; induction from the leaves and the
nonnegative leading coordinates gives the unique fiber
\(t_v=\|x_{S_v}\|\).  Choosing geometrically decreasing positive internal
values at \(x=0\) gives strict feasibility.

The dual factors
\[
       (s_v,(-s_c)_{c\text{ child of }v})\in Q_{b_v+1}
\]
cancel every nonroot auxiliary coefficient in the affine pairing and leave
exactly \(1-x^Ty\).  They are therefore genuine dual certificates for the
displayed lift.  Every list of integers
\(1\leq b_v-1\leq d-2\) summing to \(N-1\) is realized by successively
replacing a leaf by \(b_v\) children.  Hence the factor, ambient-dimension,
and product-barrier counts in (0) are attained simultaneously, including a
smaller final arity.

For regularity, a proper internal subtree contains at least two leaves, so
\(x_{S_v}=0\) has codimension \(|S_v|\geq2\) on the sphere.  Off the finite
union of these sets, every subtree norm and every primal and dual factor is
real analytic.  Globally, every node map is \(\sqrt2\)-Lipschitz and the
finite concatenations are Lipschitz with the constants stated after (6a).
At a zero subtree the corresponding Lorentz factor is the cone vertex.
Approaching it along different normalized subtree directions produces
different limiting boundary-base points although the primal point
converges.  The normalized support graph therefore has noncompact ends and
the generic local diffeomorphism is not proper; neither graph closure nor
uniqueness of the unnormalized boundary fiber repairs this loss of phase.
The \(N=3\) formulas (8)--(9) exhibit the same failure explicitly at the two
poles.  Thus global Lipschitz regularity on both factor maps is verified and
still does not imply the global \(C^1\) capacity gap.
