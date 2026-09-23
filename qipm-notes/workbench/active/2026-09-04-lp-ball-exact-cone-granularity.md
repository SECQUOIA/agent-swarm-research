# Exact tame-cone granularity of every \(\ell_p\) ball

Status: Proved; literature-screened; independently audited  
Started: 2026-09-04  
Paper status: Not incorporated  
Confidence: High, conditional on the audited universal curvature-capacity theorem

## Result

Fix \(1<p<\infty\), \(N\geq2\), and an integer \(d\geq3\). Work in any
o-minimal expansion of the real field in which the fixed power function
\(t\mapsto t^p\) on \(t>0\) is definable; \(\mathbb R_{\exp}\) suffices.
Consider exact lifts of

\[
 B_p^N=\left\{x\in\mathbb R^N:
 \sum_{j=1}^N|x_j|^p\leq1\right\}                    \tag{1}
\]

over finite products of definable proper cone blocks, each of real ambient
dimension at most \(d\), allowing arbitrary affine slices, projections, and
free variables. Let \(k_+\) count the non-ray factors,
\(k_{\rm all}\) count every factor, and let \(M\) be total cone-space
dimension. The minimum in (2) is over \(k_{\rm all}\); its matching
construction uses no rays. Then

\[
 \boxed{
 k_{\min}=\left\lceil\frac{N-1}{d-2}\right\rceil,
 \qquad
 M_{\min}=N-1+2\left\lceil\frac{N-1}{d-2}\right\rceil.} \tag{2}
\]

For rational \(p\), all cones and sets in the construction are
semialgebraic, so (2) holds already in the semialgebraic category.

The ambient product-cone logarithmically homogeneous self-concordant
(LHSC) barrier lower bound

\[
 \nu\geq2\left\lceil\frac{N-1}{d-2}\right\rceil       \tag{3}
\]

also follows from the universal theorem. Equality in (3) is asserted here
only for \(p=2\), where Lorentz blocks have parameter two. For
\(p\neq2\), the matching \(p\)-order-tree blocks need not have parameter
two, so no barrier upper bound or equality claim is made; (2) is not a
barrier-optimality claim.

## Lower bound from one curved patch

On any orthant where every coordinate is nonzero, the defining function

\[
 f(x)=\sum_j|x_j|^p
\]

is smooth and has Hessian

\[
 \nabla^2f(x)=p(p-1)\operatorname{diag}
 \bigl(|x_1|^{p-2},\ldots,|x_N|^{p-2}\bigr)\succ0.    \tag{4}
\]

Thus \(\partial B_p^N\) has a relatively open smooth patch with strictly
positive second fundamental form, since on its tangent space
\(\mathrm{II}=\nabla^2f/\|\nabla f\|\). The universal dimension-minus-two
curvature theorem gives, for block dimensions \(m_i\),

\[
 N-1\leq\sum_{i:\,K_i\text{ non-ray}}(m_i-2).        \tag{5}
\]

Since \(m_i\leq d\), equation (5) gives
\(k_{\rm all}\geq k_+\geq\lceil(N-1)/(d-2)\rceil\).
Ray factors need not be redundant in an individual formulation; they carry
no curvature and cannot improve this count. Equation (5) also gives

\[
 M\geq\sum_{i:\,K_i\text{ non-ray}}m_i
 \geq N-1+2k_+,
\]

and hence the dimension lower bound in (2). The theorem used here is
[the audited universal cone curvature-capacity
theorem](2026-09-04-universal-cone-curvature-capacity.md).

## Matching \(p\)-norm tree

For \(m\geq2\), define the \(m\)-dimensional \(p\)-order cone

\[
 K_{p,m}=\{(t,u)\in\mathbb R\times\mathbb R^{m-1}:
 t\geq\|u\|_p\}.                                    \tag{6}
\]

It is a closed, pointed, full-dimensional convex cone. It is
\(\mathbb R_{\exp}\)-definable for every fixed real \(p\), and
semialgebraic for rational \(p\). Explicitly, if \(p=a/b\) in lowest terms,
introduce nonnegative \(s_j,z\) satisfying
\(s_j^b=|u_j|^a\), \(z^b=t^a\), and
\(z\geq\sum_js_j\). This avoids any invalid manipulation of fractional
powers and gives a semialgebraic projection even when \(b\) is even.
An internal tree node with \(r\) children
uses one block \(K_{p,r+1}\) to require its scalar to dominate the
\(\ell_p\) norm of the child values.

Let

\[
 k=\left\lceil\frac{N-1}{d-2}\right\rceil
\]

and partition \(N-1=b_1+\cdots+b_k\) with
\(1\leq b_i\leq d-2\). Construct a rooted chain of internal nodes: node
\(i<k\) has \(b_i\) leaf children and the next internal node, while the
last has \(b_k+1\) leaf children. Node \(i\) has arity \(b_i+1\) and uses
one block of dimension

\[
 m_i=b_i+2\leq d.                                    \tag{7}
\]

Fix the root scalar to one. Recursive elimination works because

\[
 \left(\sum_{j\in A}|x_j|^p+
 \left(\sum_{j\in B}|x_j|^p\right)\right)^{1/p}
 =\left(\sum_{j\in A\cup B}|x_j|^p\right)^{1/p}      \tag{8}
\]

for disjoint child subtrees. The projected feasible set is therefore
exactly \(B_p^N\). Moreover,

\[
 \sum_i m_i=\sum_i(b_i+2)=N-1+2k,                   \tag{9}
\]

so the construction attains both lower bounds simultaneously.

The same proof includes ellipsoids at \(p=2\) after an invertible affine
change of coordinates.

## Boundary and literature note

The endpoints \(p=1\) and \(p=\infty\) are excluded: their balls are
polyhedral and have no positively curved boundary patch, so the differential
lower bound does not apply. Equation (2) concerns exact formulations; no
claim is made for approximating lifts.

The upper tree is known. Proposition 1 of
[Krokhmal and Soberanis](https://doi.org/10.1016/j.ejor.2009.03.053)
represents a \((J+1)\)-dimensional \(p\)-order cone by \(J-1\)
three-dimensional \(p\)-order cones.
[Blanco and Martínez-Antón](https://doi.org/10.1137/23M1617205) study
minimal representations of generalized power cones into specified simpler
cone families and repeat the tree construction. These results do not lower
bound the number of blocks against arbitrary definable proper cones.

The apparently new statement is narrow: universal optimality of the known
tree over all tame proper block dictionaries and arbitrary affine lifts,
for every cap \(d\), together with the exact total-dimension optimum.
[Hildebrand](https://doi.org/10.1007/s10107-012-0576-1), Corollary 7.2,
gives a nontrivial \(p\)-dependent lower bound on the LHSC barrier parameter
of the three-dimensional \(p\)-order cone, supporting the barrier caveat
above. Targeted searches found no collision with the lower bound or the
exact statements in (2). Novelty remains subject to specialist review.

## Audit checklist

- Verify strict positive curvature at a point with all coordinates nonzero
  for the full range \(1<p<\infty\).
- Verify definability and semialgebraicity of \(K_{p,m}\), especially for a
  rational exponent with an even denominator.
- Verify the chain-tree arities, exact recursive elimination, and total
  dimension count.
- Check that arbitrary affine lifts and arbitrary definable proper blocks
  are genuinely covered by the universal theorem's final hypotheses.
- Literature-screen exact block-count results for \(\ell_p\) balls.

The independent audit checked the curved patch for the entire range
\(1<p<\infty\), definability and rational semialgebraicity, cone properness,
the forward and converse tree induction, all arity/leaf/dimension counts,
ray accounting, and the barrier qualification. It found the tree prior art
recorded above but no prior lower bound against arbitrary tame cone blocks.
