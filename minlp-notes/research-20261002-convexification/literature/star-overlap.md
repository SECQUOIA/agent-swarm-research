**Star quadratic support: targeted literature comparison, October 2, 2026.**

The box-only star support problem is already polynomially solvable as a
special case of the existing forest-QP preprint. Its elementary leaf elimination
is useful for a small exact certificate implementation, but it must not be
presented as a new tractability result. The comparison below concerns

\[
q(y,x)=a y^2+b y+c+
\sum_{i=1}^k[d_i x_i^2+(e_i y+f_i)x_i],
\]

with rational coefficients and finite rational independent bounds, allowing
either sign for every quadratic coefficient. This audit checked four
primary sources; it is not proof of novelty for the extensions.

| Primary source and statement checked | Overlap and boundary |
| --- | --- |
| Alberto Del Pia and Aida Khajavirad, *Treewidth and the complexity of box-constrained quadratic programs*, [arXiv:2609.35595v1](https://arxiv.org/html/2609.35595v1), September 28, 2026. Theorem 1 and Section 2.1, equation (3). [Primary PDF](https://arxiv.org/pdf/2609.35595v1). | Theorem 1 solves arbitrary rational box QP on a forest in `O(n²)` arithmetic operations and comparisons with controlled intermediate encoding. Stars are a direct special case. Equation (3) conditions on a parent coordinate, minimizes child subproblems independently, and sums their value functions. On a star these child problems are scalar quadratics: clipped affine minimizers for positive curvature and endpoint minimizers otherwise. Rational boxes reduce affinely to the unit box; fixed coordinates can be eliminated. Thus the proposed box support algorithm is an attributed specialization with a simpler rational representation. The theorem does not include additional affine constraints coupling the center and leaves. |
| Alberto Bemporad, Manfred Morari, Vivek Dua, and Efstratios N. Pistikopoulos, *The explicit linear quadratic regulator for constrained systems*, Automatica 38 (2002), 3–20, [DOI](https://doi.org/10.1016/S0005-1098(01)00174-1). Theorems 2 and 4, checked in the [author primary PDF](https://cse.lab.imtlucca.it/~bemporad/publications/papers/automatica-mpqp.pdf), available in the local literature cache, and its text extraction. | For strictly convex parametric QP, a fixed independent active set gives affine optimizer and multiplier maps; the optimizer is piecewise affine and the value is piecewise quadratic. These are established foundations for positive-curvature leaves with affine parameter-dependent bounds. They do not establish the all-sign star support theorem or a general linear bound on the number of parametric regions. Eliminating one separable scalar leaf is an elementary specialization of this framework. No new claim should concern piecewise-affine active-set responses themselves. |
| Aida Khajavirad, *Tight semidefinite programming relaxations for sparse box-constrained quadratic programs*, [arXiv:2601.18545v2](https://arxiv.org/html/2601.18545v2), February 12, 2026; latest version listed by arXiv when checked October 2. Introduction, definition of `QP(G)`, and Theorems 5–6. | Theorem 5 gives exact SDP representations of size `O(2^|V|)` for sign-oriented lifted sets when the subgraph of variables with positive square coefficients has no connected component of size three or more. Theorem 6 gives polynomial-size construction under additional logarithmic bounds on treewidth and the degrees of positive-loop vertices. A star with positive square coefficients on its center and two leaves fails the first sufficient condition; a high-degree positive center can fail the size condition. Failure of a sufficient condition is not evidence of impossibility. These sign-oriented hulls, with square inequalities selected by objective signs, must also be distinguished from the complete simultaneous graph of every square and product. The source already establishes substantial sparse quadratic convexification, so a general claim of introducing star-based convexification would be too broad. |
| Marco Locatelli, *Convex Envelopes of Some Quadratic Functions over the n-Dimensional Unit Simplex*, SIAM Journal on Optimization 25 (2015), 589–621, [DOI](https://doi.org/10.1137/140976637). The [author's May 26, 2014 technical report](https://www.ce.unipr.it/~locatell/ConvEnvSimplex-TechRep.pdf), *Computing convex envelopes of quadratic functions over the unit simplex*, Sections 2 and 5, was inspected. | The feasible domain is `x >= 0`, `sum(x)=1`; its star is the graph of simplex edges on which the quadratic is strictly convex after the paper's transformations. Section 5 develops the corresponding envelope. Both the simplex domain and this convexity graph differ from independent boxes and the off-diagonal interaction graph. This is relevant prior star convexification, but its stated theorem is not the box support theorem. Technical-report section numbers should not be attributed to the final journal version. |

For this continuation, the defensible development is an explicit,
replayable support certificate and its use in simultaneous
convexification, together with a carefully delimited constraint extension.
Each affine row in that extension must involve only the center and one
leaf, so conditional leaf feasibility remains separable. General rows
coupling several leaves do not retain that property. The forest box theorem
does not supply the constraint extension, but that scope difference alone
does not prove novelty; the construction still uses classical parametric
optimization.

An exact minimum for a supplied linear functional certifies one support
inequality. It does not by itself prove that an implemented algorithm finds
a separating inequality for every point outside the joint hull. Likewise,
intersecting exact block hulls requires a separate compatibility argument
before claiming the full hull of their union. Certificate validity,
separation completeness, overlap repair, and solver speed are distinct
claims and need distinct evidence.

The primary-source search used combinations of `arrowhead`, `star`,
`box-constrained quadratic`, `forest`, `parametric quadratic`, and `convex
hull`. The existing decomposition source ledger identified the decisive
forest theorem, which was then checked in the primary arXiv text. No
project-wide verification or CI inspection was performed; this was a
literature and scope audit.
