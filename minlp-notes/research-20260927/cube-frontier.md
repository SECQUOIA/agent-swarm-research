# The three-variable quadratic frontier

Date: 2026-09-27. Status: partial structural progress; the full completeness
question remains open in this investigation.

The epigraph-hull question is whether the full disjoint-support affine-SOS cone, augmented
by every cube symmetry of the
[five-parameter family](../research-20260925/three-positive-family-sdp.md),
equals the cone of quadratic polynomials nonnegative on the three-cube with
nonnegative square coefficients. For the compact moment hull, the corresponding
question must additionally include the valid generators \(x_i(1-x_i)\), which
are dual to the diagonal upper bounds. Without this distinction a claim of
completeness for all nonnegative quadratics is already false:
\(x(1-x)\) has a negative square coefficient, whereas every quadratic in
the disjoint cone or the added family has nonnegative square coefficients.
For the disjoint cone, fix the other coordinates: the coefficient of a
coordinate square is a sum of nonnegative weighted squares of affine
coefficients; weights involving that coordinate contribute no square.
The exact six-tetrahedron SDP formulation is already known, so completeness
of this particular certificate system would be a structural result, not a
new tractability theorem for three-variable box quadratic optimization.

## Edge contacts give a small algebraic search space

Write

\[
q(x)=c+\ell^Tx+x^TQx,\qquad Q_{ii}=d_i^2>0,
\]

and suppose every vertex value is positive. For a vertex \(v\), put
\(s_v=\sqrt{q(v)}>0\). On an edge from \(u\) to \(v\), in coordinate
direction \(i\), the restriction is

\[
q((1-t)u+tv)=(1-t)s_u^2+t s_v^2-d_i^2t(1-t).
\]

It is nonnegative on the edge if and only if
\(d_i\leq s_u+s_v\). Indeed, it equals

\[
((1-t)s_u-t s_v)^2+
\bigl((s_u+s_v)^2-d_i^2\bigr)t(1-t).
\]

If the displayed inequality fails, substituting
\(t=s_u/(s_u+s_v)\) gives a negative value. Equality gives one interior
edge zero, at that same parameter; strict inequality gives no edge zero.

The eight vertex values are compatible with a quadratic polynomial exactly
when their alternating sum vanishes:

\[
\sum_{v\in\{0,1\}^3}(-1)^{v_1+v_2+v_3}s_v^2=0.
\]

This follows by multilinear interpolation. Its cubic coefficient is the
alternating sum, up to sign; subtracting
\(\sum_i d_i^2x_i(1-x_i)\) then supplies the prescribed diagonal
coefficients. Thus fixing a set of zero edges imposes linear equations on
the eleven numbers \((s_v,d_i)\), with just one quadratic compatibility
equation left.

If every two-by-two principal minor of \(Q\) is strictly negative, checking
the edges suffices for cube nonnegativity. Any minimum in the relative
interior of a face with at least two free coordinates would require the
corresponding principal Hessian submatrix to be PSD, which is impossible.
These statements are elementary reductions. They are not claimed as new
nonnegativity criteria beyond the established boundary-recursion approach.

## Why a hexagonal contact pattern is not a missing ray

An early possibility was a new extreme ray with edge-contact direction
counts \((2,2,1)\). One surviving pattern forces a sixth contact, making a
hexagonal cycle. Such a pattern is possible even when all the above strict
assumptions hold; it must not be excluded as infeasible.

For example, for \(0<\varepsilon<1\),

\[
p_\varepsilon=(x+y+z-\tfrac32)^2+
\varepsilon\left[\tfrac12-(x-\tfrac12)^2-(y-\tfrac12)^2
 -(z-\tfrac12)^2\right]
\]

vanishes at all permutations of \((0,1/2,1)\). Its diagonal coefficients
are \(1-\varepsilon>0\), its off-diagonal matrix entries are one, and
every two-by-two principal minor is strictly negative. Its vertex values
are also strictly positive. Nevertheless it is not extreme, because

\[
p_\varepsilon=(1-\varepsilon)(x+y+z-\tfrac32)^2+
2\varepsilon\bigl[(1-x)(1-y)(1-z)+xyz\bigr].
\]

Both summands are nonnegative, and the apparent cubic terms cancel in the
second summand. The two summands are not proportional. This example was
derived independently by the lead investigator and the contact-pattern
investigator while auditing the proposed classification.

The [companion classification theorem](cube-strict-extreme-classification.md)
treats this pattern by decomposition, not by an infeasibility claim. It proves
that every extreme ray satisfying the strict hypotheses above is a cube
symmetry of the existing five-parameter family. It received
[independent adversarial review](cube-strict-extreme-review.md), including
an exact enumeration of all 792 five-edge subsets into 24 symmetry orbits.
It does not cover
vertex zeros, zero principal minors, or zeros in the relative interior of
two-dimensional faces. Those remaining cases are essential to the full
completeness question.

## A closure fact for future separation arguments

Let \(\mathcal D_3\) mean its quadratic part, and let \(\mathcal F\) be
the conic hull of all nonnegative-parameter family polynomials and all
their cube symmetries. Then \(\mathcal D_3+\mathcal F\) is closed.

Here is a direct finite-dimensional proof. For the full disjoint-support
cone, represent each weighted affine SOS by a PSD Gram matrix \(G_w\) in
its permitted affine basis \(b_w\). The matrix

\[
H_w=\int_{[0,1]^3}w(x)b_w(x)b_w(x)^T\,dx
\]

is positive definite: the weight is positive in the open cube and a
nonzero affine polynomial cannot vanish there. If the sum of the terms
has bounded integral, every
\(\operatorname{tr}(G_wH_w)\) is bounded because these quantities are
nonnegative and add to that integral. Thus every Gram matrix is bounded.
Taking convergent subsequences proves closedness, including after
intersection with the quadratic-polynomial subspace.

For the family, normalize its real parameter \(h\) and its four
nonnegative parameters to have Euclidean norm one. This parameter set is
compact. No parameter on it gives the zero polynomial: its three diagonal
coefficients first force \(d_1=d_2=d_3=0\); the constant coefficient
then forces \(h=0\); the mixed coefficient then forces \(k=0\).
Every such polynomial is nonnegative and nonzero, so its cube integral is
positive. Compactness gives a uniform positive lower bound on this
integral. Normalizing each family polynomial to integral one therefore
gives a compact set, also after taking the finitely many cube symmetries.
Its convex hull is compact, proving that \(\mathcal F\) is closed and
has a compact integral-one base.

Finally, in a convergent sequence of sums from
\(\mathcal D_3+\mathcal F\), the two nonnegative integrals are separately
bounded. A nonnegative polynomial of bounded degree and bounded cube
integral has bounded coefficients: the integral has a positive minimum on
the compact coefficient-norm unit sphere intersected with the nonnegative
cone.
Each summand thus has a convergent subsequence; the limits stay in their
respective closed cones.

The closure argument was also checked in the linked independent review.
Consequently, finding an extreme ray of the full nonnegative-quadratic
cone which belongs neither to \(\mathcal D_3\) nor to an individual
family ray would rigorously disprove completeness. Extremality rules out
a nontrivial conic sum, and the closure fact rules out approximation as
an escape. This is a proof tool, not a construction of such a ray.

## Sources checked and scope of the contribution

On 27 September 2026, the arXiv records still list
[Khajavirad, 2601.18545v2](https://arxiv.org/abs/2601.18545v2), revised
12 February 2026;
[Burer–Natarajan–Willemsen, 2504.03996v3](https://arxiv.org/abs/2504.03996v3),
revised 31 August 2026; and
[Anstreicher–Puges, 2501.09150v1](https://arxiv.org/abs/2501.09150v1).
The inspected Khajavirad HTML still explicitly leaves three-positive-loop
exactness open. The repository's earlier counterexample answers that
source-specific question negatively; this investigation asks whether its
added family repairs the failure completely.

The strongest exact comparator remains
[Anstreicher–Burer, Theorem 7](https://optimization-online.org/wp-content/uploads/2007/02/1586.pdf),
which gives a complete SDP lift by triangulation in dimension at most
three. Boundary recursion and the use of cube-face restrictions were
already developed by Burer–Letchford and Burer–Dong, as documented in the
[earlier priority review](../research-20260925/three-positive-family-priority-review.md).
Searches for extreme nonnegative quadratics on the cube, five-zero box
quadratics, and hypercube quadratic preorderings did not identify a full
matching classification. That limited negative search is not evidence
establishing novelty.

The separate
[four-star note](four-star-bound-bridge-obstruction.md)
rules out one proposed sparse copositive proof route even for an instance
with an exact SDP–RLT certificate. It does not settle unrestricted
four-variable star exactness. Further investigation of a restricted class
produced the [binary-leaf star projection theorem](binary-leaf-star-hull.md):
full SDP–RLT is exact for stars with nonpositive leaf square coefficients,
with no bound on the number of leaves. Its proof and source comparison are
documented separately; it does not resolve the unrestricted four-variable
case.

## Targeted computational record

`python research-20260927/check_cube_strict_extreme_classification.py`
was independently rerun by the lead investigator and passed: 792 subsets,
24 orbits, and all three edge-slack identities. A separate exact SymPy
expansion checked the hexagonal-family decomposition and its six contacts.
These checks do not replace the analytic arguments in the classification
proof or establish novelty.

`OPENBLAS_NUM_THREADS=1 python research-20260927/checks/cube_exact_cone_probe.py`
ran 300 numerical optimizations over the classical exact cone lift, using
PSD–RLT-feasible moment matrices as objective coefficients. The saved JSON
contains five numerically indefinite candidates with positive diagonal
coefficients. Four had principal minors close to zero and no reliable new
structural interpretation; the fifth had all three minors strictly
negative. CLARABEL warned of inaccurate solutions in some trials. None
of these outputs is an exact certificate, a proof of extremality, or
evidence of completeness. The experiment found no certified missing ray.

An earlier 300-probe run with unconstrained random cost matrices produced
no candidate passing the same filter; the retained script uses the more
relevant PSD–RLT cost construction. No project-wide verification or CI
inspection was performed.
