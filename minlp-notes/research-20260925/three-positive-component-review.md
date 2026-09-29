# Independent review of the three-positive-component SDP lift

Date: 2026-09-25. Scope: Proposition 1 in
[three-positive-exploration.md](three-positive-exploration.md).
Reviewers: the independent reviewer of the CP obstruction and a fresh
subreviewer assigned to the component construction.

**Verdict.** The proposition is correct, with size interpreted as the number
of scalar variables, affine equations, and bounded-order LMI blocks, plus
the original coordinates. The proof needs no per-component or
per-conditioning-state allocation of diagonal slack. Explicit global
slack formulas would make this particularly clear. No claim relating the
torso width to the original graph width is used or validated by this review.

The following details were checked independently.

**The Bernoulli reduction includes negative loops.** Consider an original
generating point with coordinate \(a_j\in[0,1]\) at a vertex \(j\notin P\).
Independently replace all such coordinates by Bernoulli variables \(B_j\)
of mean \(a_j\). Keep every positive-loop coordinate fixed. Independence
preserves products between two rounded vertices, and fixing the positive
variables preserves every product between a rounded and unrounded vertex.

If \(j\in M\) and its original diagonal coordinate is \(d_j\le a_j^2\), put

\[
 \widehat Y_{jj}(B)=B_j-(a_j-d_j).
\]

Since \(d_j\le a_j^2\le a_j\), the subtracted slack is nonnegative. Therefore
\(\widehat Y_{jj}(B)\le B_j^2\) for every binary outcome, and its expectation
is \(d_j\). This works for arbitrarily negative \(d_j\). Existing positive
diagonal coordinates remain unchanged. The rounding uses finitely many
outcomes, so it proves equality of ordinary convex hulls without a closure
or infinite-measure argument.

**The simplex blocks describe homogeneous finite moment measures exactly.**
For a component \(C\) of size \(k\le3\), each order simplex has a
\(k\times(k+1)\) vertex matrix \(V_\pi\). Complete positivity equals double
nonnegativity at order \(k+1\le4\). Thus a feasible block has a finite
decomposition \(W=\sum_\ell r_\ell r_\ell^\top\) with \(r_\ell\ge0\).
For each nonzero term set

\[
 a_\ell=\mathbf1^\top r_\ell>0,\qquad
 u_\ell=V_\pi r_\ell/a_\ell,\qquad
 \alpha_\ell=a_\ell^2.
\]

Then \(u_\ell\) lies in that simplex and

\[
 \sum_\ell\alpha_\ell=\mathbf1^\top W\mathbf1,\qquad
 \sum_\ell\alpha_\ell u_\ell=VW\mathbf1,\qquad
 \sum_\ell\alpha_\ell u_\ell u_\ell^\top=VWV^\top.
\]

Conversely, the barycentric coordinates of any finite atomic measure on
the simplex construct such a completely positive block. Partitioning a box
measure among its order simplices gives the union construction; overlaps
between simplex boundaries can be assigned arbitrarily to one simplex.
Moments of nonedges inside a component are auxiliary entries, so retaining
the full second moment matrix imposes no additional condition on the
projected hull.

Let \(q_C(b)\) be the required mass for boundary assignment \(b\). The
actual mass constraint is

\[
 \sum_\pi\mathbf1^\top W_{C,b,\pi}\mathbf1=q_C(b).
\]

If \(q_C(b)=0\), entrywise nonnegativity forces every \(W_{C,b,\pi}=0\),
not merely its projected first moment. Hence there are no nonzero
conditional moments at a zero-probability state. For \(q_C(b)>0\), divide
the resulting finite measure by \(q_C(b)\) to obtain a conditional
probability law.

**Consistent bag tables give the needed joint binary distribution.**
Each boundary \(B_C\) is a clique of the torso graph \(T\). It is contained
in a bag of every tree decomposition of \(T\): the bags containing each
vertex form a subtree, these subtrees intersect pairwise for a clique, and
the subtree Helly property gives a common bag.

Root the supplied decomposition. For a child bag \(D\), let \(S\) be its
intersection with its parent. If the agreed separator probability
\(p_S(s)\) is positive, use the conditional kernel

\[
 K_D(t\mid s)=p_D(s,t)/p_S(s),
 \qquad t\in\{0,1\}^{D\setminus S}.
\]

If \(p_S(s)=0\), choose any probability distribution for that kernel.
Nonnegativity of the child table implies \(p_D(s,t)=0\) for every \(t\)
in this case. The separator state is reached with probability zero, so the
chosen kernel has no effect. The running-intersection condition guarantees
that the vertices introduced at a child bag are new to the part already
processed. Induction therefore glues the bags without changing previous
bag marginals and produces the correct new child marginal. The resulting
law is finite because \(R\) is finite.

The marginal of \(B_C\) obtained from a containing bag is well defined
across different containing bags: every bag on the connecting path also
contains \(B_C\), and separator consistency propagates its marginal.
If \(R\) or a boundary is empty, use the unique empty assignment of mass
one. An empty bag can be added when a concrete table is desired.

Given this joint law of the binary vector \(B\), sample each positive
component independently using its finite conditional law indexed by
\(B|_{B_C}\). The construction recovers component first and second
moments and every boundary edge moment. Independence between distinct
positive components loses no required coordinate, because there is no
edge between them. Correlations of a component with binary coordinates
outside its boundary are likewise absent from the recorded coordinates.
Binary edge moments are read directly from bag tables.

**Global diagonal slack suffices.** Let \(Z_{C,b,\pi}\) denote the
unnormalized second moment output of a simplex block. The exact diagonal
projection can be written

\[
 Y_{ii}=\sum_{b,\pi}(Z_{C,b,\pi})_{ii}+s_i
       \quad(i\in P,\ i\in C),\qquad
 Y_{jj}=x_j-s_j\quad(j\in M),\qquad s\ge0.
\]

Once a finite probability law realizing the compact moment coordinates
has been constructed, add the same \(s_i\) to the positive diagonal
coordinate of every atom, and subtract the same \(s_j\) at every negative
diagonal coordinate. Each resulting atom satisfies its required square
inequality, and the desired total diagonal coordinates are recovered.
Thus slack need not be distributed across boundary states or simplex
blocks. Keeping it global also makes zero-mass blocks unambiguous.

**The displayed counting bound is sound in its stated torso parameters.**
A bag has at most \(2^{\tau+1}\) probability entries. A tree with
\(|\mathcal B|\) bags has \(|\mathcal B|-1\) adjacent separators, each
requiring at most \(2^{\tau+1}\) marginal equations. Thus the bag variables,
nonnegativity conditions, normalization equations, and consistency
equations have total count \(O(|\mathcal B|2^{\tau+1})\).

Each component and boundary state has \(k!\le6\) matrix blocks of
order \(k+1\le4\), with a bounded number of scalar entries and
nonnegativity constraints per block. Its mass equation adds one equation
per boundary state. The component count is therefore

\[
 O\left(\sum_C |C|!\,2^{|B_C|}\right).
\]

Reading original moments and adding global slacks introduces only the
original output coordinates and their affine projection equations.
This proves the claimed formulation count. If “size” instead means
total nonzero coefficient encoding length, the output maps must also be
counted: the boundary-edge readouts can use an additional factor
\(|B_C|\) per component table, and sparse encodings of bag consistency
have their own incidence count. The current count should therefore be
identified with numbers of variables and constraints, rather than a
literal bound on all encoded nonzero coefficients.

The argument assumes the torso decomposition is supplied. It gives no
bound on its width from the original graph decomposition, and provides
no algorithm for computing an optimal decomposition.

**Verification scope.** Both reviewers independently checked the
Bernoulli/slack and simplex arguments; this reviewer additionally checked
the explicit bag gluing construction, conditional moments, finite
support, and formulation count above. No new numerical experiment,
project-wide verification, CI inspection, or Lean verification was
performed for Proposition 1. The theorem uses the established
order-at-most-four CP=DNN identity as an external mathematical input,
not as something independently reproved here. The result remains a
combination of classical constructions, without an asserted new
representability mechanism.
