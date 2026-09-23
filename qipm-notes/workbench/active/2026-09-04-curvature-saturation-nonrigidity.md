# What curvature-budget saturation does—and does not—make rigid

Status: Proved; independently audited  
Started: 2026-09-04  
Paper status: Not incorporated  
Confidence: High

## Question

For an exact \(B_p^N\) lift that attains the minimum number of non-ray
factors under a dimension cap \(d\), can equality in the universal
curvature budget force a \(p\)-order-cone tree, or a \(p\)-dependent barrier
premium for every factor?

The answer to the first question is no.  Saturation has a clean local
linear-algebra consequence, but it does not identify the cones globally.
Even the three-dimensional \(p\)-ball has a saturated, minimum-count lift
with a factor that is not linearly isomorphic to a \(p\)-order cone.  The
counterexample also explains why the local rank proof alone cannot establish
a target-dependent barrier premium.  It does **not** disprove such a premium
by some additional global argument.

## Local equality lemma

Let a \(C^2\) exposed primal/polar contact of a positively curved
\(N\)-body give a mixed-slack matrix

\[
             H=\sum_{i=1}^k M_i,\qquad \operatorname{rank}H=N-1,   \tag{1}
\]

where the tangent-pairing proof gives

\[
             \operatorname{rank}M_i\leq c_i\leq(m_i-2)_+.        \tag{2}
\]

Take primal and dual factor selections on the same contact chart. Each block
slack is nonnegative and vanishes on the diagonal, so the diagonal-kernel
Hessian argument also gives

\[
                         M_i\succeq0.                              \tag{2a}
\]

Suppose the ambient dimension-minus-two budget is saturated:

\[
             \sum_i(m_i-2)_+=N-1.                                \tag{3}
\]

Then every inequality in (2) is an equality:

\[
       \operatorname{rank}M_i=c_i=(m_i-2)_+                      \tag{4}
\]

for every block with positive capacity.  Moreover, the column spaces of the
\(M_i\)'s form an internal direct sum, and so do their row spaces:

\[
 \mathbb R^{N-1}=\bigoplus_i\operatorname{im}M_i,qquad
 \mathbb R^{N-1}=\bigoplus_i\operatorname{im}M_i^T.               \tag{5}
\]

Indeed,

\[
 N-1=\operatorname{rank}\sum_iM_i
 \leq\dim\sum_i\operatorname{im}M_i
 \leq\sum_i\operatorname{rank}M_i
 \leq\sum_i c_i
 \leq\sum_i(m_i-2)_+=N-1,                                       \tag{6}
\]

so equality holds throughout; applying the same argument to transposes
gives the row statement.  Thus each block uses every locally available
curvature channel, and the channels do not cancel or overlap at that
contact.

There is a sharper metric form. Since \(H\) is positive definite, set

\[
                  P_i=H^{-1/2}M_iH^{-1/2}.                         \tag{6a}
\]

Then \(P_i\succeq0\), \(\sum_iP_i=I\), and their ranks sum to \(N-1\).
Factor \(P_i=Z_iZ_i^T\) with \(Z_i\) having \(\operatorname{rank}P_i\)
columns and concatenate the \(Z_i\)'s into the square matrix \(Z\). The
identity \(ZZ^T=I\) makes \(Z\) orthogonal. Consequently

\[
 P_iP_j=0\ (i\ne j),\qquad P_i^2=P_i,                              \tag{6b}
\]

or, equivalently,

\[
 M_iH^{-1}M_j=0\ (i\ne j),\qquad M_iH^{-1}M_i=M_i.                 \tag{6c}
\]

This Parseval-fusion decomposition is the full local consequence under the
\(C^2\) diagonal-slack hypotheses. It remains a statement about first
derivatives at one generic contact and contains no information about unused
regions of a cone, higher jets, global facial structure, or other contacts.

## Minimum factor count versus saturation

Put \(r=N-1\), \(b=d-2\), and

\[
             k_{\min}=\left\lceil r/b\right\rceil.                \tag{7}
\]

Attaining \(k_{\min}\) does not by itself imply (3): the available budget
can exceed \(r\) by as much as \(d-3\).  If (3) is also assumed and all
curvature-carrying factors have dimension at most \(d\), their dimensions
only have to satisfy

\[
             \sum_{i=1}^{k_{\min}}(m_i-2)=r,qquad 3\leq m_i\leq d. \tag{8}
\]

There need not be a unique dimension allocation.  The \(p\)-norm aggregation
tree realizes any compatible composition
\(r=\sum_i(m_i-2)\), and different rooted tree shapes realize the same
allocation.  If \(b\mid r\), (8) forces every \(m_i=d\); otherwise multiple
allocations may occur.  None of these elementary equalities identifies a
global cone.

## Explicit saturated minimum-count counterexample

Fix \(1<p<\infty\) and consider \(B_p^3\).  Let

\[
 K_{p,3}=\{(t,u_1,u_2):t\geq(|u_1|^p+|u_2|^p)^{1/p}\}.            \tag{9}
\]

Use one auxiliary scalar \(t\) and the two three-dimensional factors

\[
 K_1=K_{p,3},\qquad
 K_2'=K_{p,3}\cap\{(s,t,x_3):t\geq0\}.                            \tag{10}
\]

The lift is

\[
 (t,x_1,x_2)\in K_1,qquad (1,t,x_3)\in K_2'.                    \tag{11}
\]

The extra halfspace in \(K_2'\) is redundant in (11), because the first
constraint already gives

\[
             t\geq(|x_1|^p+|x_2|^p)^{1/p}\geq0.                  \tag{12}
\]

Eliminating \(t\) therefore shows that (11) projects exactly onto

\[
             |x_1|^p+|x_2|^p+|x_3|^p\leq1.                      \tag{13}
\]

Both factors are proper, definable in \(\mathbb R_{\exp}\) (and
semialgebraic for rational \(p\)), and three-dimensional.  The exact
granularity theorem gives

\[
 k_{\min}=\left\lceil{3-1\over3-2}\right\rceil=2,                \tag{14}
\]

so (11) attains the minimum non-ray count.  It also saturates curvature:

\[
             \sum_{i=1}^2(m_i-2)=2=N-1.                          \tag{15}
\]

No facial reduction is hidden: for \(0<t<1\), the feasible point \(x=0\)
places \((t,0,0)\) in the interior of \(K_1\) and \((1,t,0)\) in the
interior of \(K_2'\). Both reduced factor faces are therefore the full
three-dimensional cones.

Nevertheless, \(K_2'\) is not linearly isomorphic to \(K_{p,3}\).
The cone \(K_{p,3}\) is strictly convex for \(1<p<\infty\), so all of its
proper nonzero faces are rays.  In contrast,

\[
             K_2'\cap\{t=0\}
        =\{(s,0,x_3):s\geq|x_3|\}                                 \tag{16}
\]

is a two-dimensional exposed face of \(K_2'\).  Face dimensions are
preserved by linear cone isomorphisms.  Hence this saturated minimum-count
lift is not a product of \(p\)-order cones up to blockwise linear
isomorphism.  For \(p=2\), it is already a minimum two-block lift of the
three-ball with one non-Lorentz factor.

At a generic all-nonzero contact of (13), the aggregate \(t\) is strictly
positive.  The added facet of \(K_2'\) is then inactive, so the local boundary
germ used by the curvature proof is identical to that of \(K_{p,3}\).  This
is why (4)--(5) cannot detect the global modification.

## Consequence for barrier arguments

The equality lemma does not imply a \(p\)-dependent LHSC barrier premium.
It only forces full use of the tangent pairing at one contact, while an LHSC
barrier parameter is a global invariant of the whole cone.  The cones in
(9)--(10) have identical local boundary germs at the contact but different
global face lattices.

This is a limitation of the curvature-rank proof, not a counterexample to a
target-level premium.  In particular, no claim is made here that \(K_2'\)
admits a barrier with parameter below the known \(p\)-cone lower bound.
A valid premium theorem for arbitrary minimum-count lifts would need extra
global hypotheses—for example, irredundancy/minimality of each factor as a
cone, coverage of its projective boundary by the lift, or a projective
invariant propagated across all contacts.  Local rank saturation alone is
insufficient.

## Novelty boundary

The rank-equality lemma is elementary.  The useful new information is the
explicit half-cone construction (10)--(16), which prevents an unjustified
global classification from being inferred from the new curvature theorem.
No literature claim is made for this construction pending specialist
review. An independent hostile audit verified the exact projection,
full-face property, minimum count, rank saturation, exposed-face
nonisomorphism, and the strengthened Parseval-fusion equality.
