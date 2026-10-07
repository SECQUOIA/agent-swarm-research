# Prior-art audit: copositive block elimination, scaling, and the width-three reduction

Date: 2026-10-02. This note compares three reviewed constructions with the
closest primary sources located. The comparisons identify classical
components and delimit the results; they do not infer novelty from a search
that found no exact match.

## Findings

The articulation-block algorithm extends the known exact forest algorithm.
Ikramov gives a linear-operation test for copositivity of matrices whose
interaction graph is a tree, including a strict-copositivity version. Its
leaf reductions delete a coordinate for positive coupling and use a
one-coordinate Schur update for negative coupling. The new
[`articulation-copositive-elimination.md`](../new-direction/articulation-copositive-elimination.md)
processes an entire private block of at most `p` vertices at once. It tests
strict copositivity and solves the orthant recourse problem by enumerating
supports, then passes the resulting homogeneous scalar value through the
cut vertex. Thus the tree result, extended componentwise to forests, is the
`p = 2` baseline. Ikramov states the connected-tree case; the forest
extension is immediate. It does not state the bounded-biconnected-block
result or its rational bit bound.

The Jacobi-scaling formula is a direct normalization identity. Positive
diagonal congruence preserves the copositive cone, and unit-diagonal
normalization is standard. The formula in
[`jacobi-copositive-residual.md`](../new-direction/jacobi-copositive-residual.md)
identifies the minimum of this specific ratio:

`inf_{D diagonal, D>0} 2 max_i (D R D)_ii / g(D R D) = 2/gamma(R)`, where
`gamma(R) = min_{x >= 0, x != 0} x' R x / (x' diag(R) x)`.

After setting `u = diag(R)^(1/2) x`, `gamma(R)` is the smallest
orthant-constrained Rayleigh value of the unit-diagonal Jacobi-scaled
residual. Hiriart-Urruty and Seeger call this the smallest Pareto eigenvalue.
Their support characterization can require checking all nonempty principal
supports, so the identity is a normalization fact, not an efficient
copositivity algorithm.

Clipping an off-diagonal entry above the diagonal scale is also a known
copositivity-preserving step. Bomze and Eichfelder's Lemma 4.4 gives a
one-entry truncation rule for unit-diagonal matrices and transfers a
violating vector. The residual note strengthens this sign-preservation
result by showing that clipping preserves the exact Euclidean orthant-growth
constant. That equality follows from the note's mass-transfer argument; it
is not claimed by Lemma 4.4.

The width-three construction uses standard nonnegative complementarity and
homogenization devices: squared residuals enforce `z_i + w_i = t`,
`z_i w_i = 0`, and running-sum equations. The construction and its zero-set
equivalence are proved in
[`strict-copositive-width3-barrier.md`](../new-direction/strict-copositive-width3-barrier.md).
The explicit quadratic has a supplied SPN decomposition, interaction
treewidth at most three, and Hessian bounded below by `-I`, while strict
copositivity remains co-NP-hard to decide. The reduction does not give a
uniform positive growth bound. Murty and Kabadi supply a general
co-NP-completeness baseline for copositivity, but the accessible abstract
does not establish these width, SPN, or curvature restrictions.

## Source comparisons

### Articulation blocks and recursive copositivity

Kh. D. Ikramov, “A linear-time algorithm for verifying the copositivity of
an acyclic matrix,” *Computational Mathematics and Mathematical Physics*
42(12) (2002), 1701–1703, [Math-Net record and full text](https://www.mathnet.ru/eng/zvmmf1082).
I inspected the Russian primary text in the official Math-Net PDF. It
defines an acyclic matrix by a tree interaction graph. Propositions 3–4 and
the algorithm on pp. 1772–1773 give leaf reductions: for a positive single
leaf coupling, delete that coordinate; for a negative coupling and positive
leaf diagonal, subtract the rank-one Schur update. The article also states
the strict-copositivity version. Its operation count is linear in `n`; it
does not analyze rational bit complexity.

Immanuel M. Bomze, “Linear-time copositivity detection for tridiagonal
matrices and extension to block-tridiagonality,” *SIAM Journal on Matrix
Analysis and Applications* 21(3) (2000), 840–848,
[DOI 10.1137/S0895479898341487](https://doi.org/10.1137/S0895479898341487),
is the earlier path-structured result cited by Ikramov. I checked the
publisher abstract, which describes a tridiagonal algorithm and a
block-tridiagonal generalization. It is a path baseline; Ikramov is the
closer source for branching forests. No stronger claim is based on the
abstract alone.

The bounded-block result uses different local work. In each leaf block the
private principal matrix may be indefinite but must be strictly copositive.
For a boundary value `s >= 0`, homogeneity gives

`min_{y >= 0} (y' B y + 2 s b' y) = s^2 min_{u >= 0} (u' B u + 2 b' u)`.

Support enumeration computes this minimum and a rational minimizer using at
most `2^p` supports. Unlike ordinary Schur elimination, it does not require
`B` to be positive definite. The one-dimensional separator keeps the
message as a scalar diagonal update and creates no fill between remaining
blocks.

Johnson and Reams, “Spectral theory of copositive matrices,” *Linear
Algebra and its Applications* 395 (2005), 275–281,
[DOI 10.1016/j.laa.2004.08.008](https://doi.org/10.1016/j.laa.2004.08.008),
give a copositive Schur-complement criterion requiring a positive-definite
principal block, as stated in the accessible abstract. The exact theorem
hypotheses and equivalence were not verified from the primary text: the
CiteSeerX PDF currently returns 403, and the local KB package is
metadata-only. This remains a narrower comparison than the bounded-block
algorithm's stated recourse over a strictly copositive, possibly indefinite
private block; this audit does not rely on an unverified sign condition or
formula.

Bomze's 2008 paper, “Perron–Frobenius property of copositive matrices, and
a block copositivity criterion,” *Linear Algebra and its Applications*
429(1) (2008), 68–71,
[DOI 10.1016/j.laa.2008.02.003](https://doi.org/10.1016/j.laa.2008.02.003),
announces a Schur-complement block criterion and says it generalizes
Johnson–Reams. Its local source record is metadata-only, so no more precise
hypothesis or conclusion is attributed here.

Hiriart-Urruty and Seeger, “A variational approach to copositive matrices,”
*SIAM Review* 52 (2010), 593–629,
[author-hosted primary PDF](https://www.math.univ-toulouse.fr/~mongeau/JBHU-copositive.pdf),
give the broader terminology. Theorem 4.3 identifies copositivity with
nonnegativity of every Pareto eigenvalue; Proposition 4.4 characterizes
these through positive eigenvectors of principal submatrices and outside
complementarity conditions. They note that the generic support test can
involve all `2^n - 1` nonempty index sets (PDF pp. 8–9). This is the global
analogue of local support enumeration, not an articulation-block dynamic
program.

The 2016 SPN-graph result also uses the block-cut tree, but for a different
purpose: Corollary 4.4 says that a graph is SPN exactly when each of its
blocks is SPN. For known SPN blocks this reduces cone membership to PSD plus
entrywise-nonnegative decomposition, but gives no scalar recourse identity,
rational output guarantee, or exact bit bound for the supplied algorithm.
Lemma 7.1 gives the non-SPN fan `F5`, which has treewidth two; thus this SPN
shortcut cannot cover every width-two pattern. See the readable primary
package
[`monderer2016-spn-graphs-when-copositive-spn`](../../literature/papers/monderer2016-spn-graphs-when-copositive-spn/paper.md),
pp. 11, 16, and the [2017 corrigendum](../../literature/papers/monderer2017-corrigendum-to-spn-graphs-when/paper.md),
pp. 1–4. The corrigendum concerns the general `T_n` claims, not Lemma 7.1's
`F5` example.

### Jacobi normalization and entry truncation

Positive diagonal congruence `R -> D R D` preserves copositivity. The
SPN-graph paper records this standard cone symmetry and customary
normalization of positive diagonal entries to one (Section 2.2). For
strictly copositive `R`, let `J = diag(R)`. The residual note's value is
equivalently

`gamma(R) = max {tau : R - tau J is copositive}`.

This is a direct generalized Rayleigh quotient. The diagonal-normalized
matrix `J^(-1/2) R J^(-1/2)` has unit diagonal and orthant growth
`gamma(R)`. Since its maximum diagonal is one, its curvature-to-growth
ratio is `2/gamma(R)`; the inequality in the note proves no other positive
diagonal congruence improves this particular ratio. Jacobi scaling is
standard unit-diagonal equilibration. Exact optimality for this specific
`L/g` objective is the quotient argument in the note. The Pareto-spectrum
characterization gives a name for the remaining global minimization, not a
tractable method.

Bomze and Eichfelder, “Copositivity detection by difference-of-convex
decomposition and ω-subdivision,” *Mathematical Programming*
138(1–2) (2013), 365–400,
[DOI 10.1007/s10107-012-0543-x](https://doi.org/10.1007/s10107-012-0543-x),
Section 4.2, Lemma 4.4, address truncating positive off-diagonal entries.
For a unit-diagonal matrix with `q_1n > 1`, replacing that entry by `1`
preserves copositivity; the lemma constructs a transferred vector when the
truncated matrix is not copositive. I inspected the full primary manuscript
from [Optimization Online](https://optimization-online.org/wp-content/uploads/2010/01/2523.pdf);
the local package is now readable at
[`bomze2013-copositivity-detection-by-difference-of`](../../literature/papers/bomze2013-copositivity-detection-by-difference-of/paper.md).
Lemma 4.4 and the following paragraph are on physical p. 18. This result
preserves copositivity status. The residual note's growth equality is
stronger: its endpoint-mass
transfer argument preserves the minimum of `x' C x / ||x||^2`, not merely
the sign of the minimum.

### Strict copositivity at width three

Murty and Kabadi, “Some NP-complete problems in quadratic and nonlinear
programming,” *Mathematical Programming* 39(2) (1987), 117–129,
[DOI 10.1007/BF02592948](https://doi.org/10.1007/BF02592948), prove that
deciding noncopositivity of an integer square matrix is NP-complete
(Theorem 3, printed p. 125). The primary author-hosted scan is linked from
[Murty's faculty page](https://public.websites.umich.edu/~murty/) and can be
[opened directly here](https://public.websites.umich.edu/~murty/np.pdf).
The PDF has no usable text layer; the ingestion audit verified the theorem
by OCR checked against the original page images. This supports only the
general hardness baseline; it says nothing about bounded treewidth, strict
copositivity, SPN matrices, or a curvature bound.

The reviewed reduction is self-contained. All terms of the constructed
quadratic are nonnegative on the orthant, so it comes with an explicit
`A = P + N` decomposition, with `P` PSD and `N` entrywise nonnegative. A
nonzero zero must have `t > 0`; after division by `t`, each `z_i/t` is binary
and the final running-sum equation is exactly the input subset-sum target.
The path bags of size four plus attached `{t, z_i, w_i}` bags give treewidth
at most three, and the disjoint `z_i w_i` Hessian blocks give
`lambda_min(nabla^2 q) >= -1`. These are direct properties of the new
construction. They do not follow from general co-NP-completeness and do not
establish hardness when the positive orthant growth margin is bounded below
by a uniform constant.

## Source access and verification status

- Read primary texts: Ikramov 2002 (official Math-Net Russian PDF; local
  package [`ikramov2002-a-linear-time-algorithm-for`](../../literature/papers/ikramov2002-a-linear-time-algorithm-for/paper.md)),
  Hiriart-Urruty–Seeger 2010 (author-hosted PDF), Shaked-Monderer 2016 and
  its 2017 corrigendum (local primary copies), and Bomze–Eichfelder's full
  manuscript (Optimization Online PDF; local readable package linked above).
- Abstract/metadata only: Bomze 2000, Johnson–Reams 2005, and Bomze 2008.
  Johnson–Reams is compared only at the level of the abstract's
  positive-definite-block requirement; no exact formula is used. No precise
  Bomze 2008 theorem is used.
- Murty–Kabadi's scanned author-hosted primary text was checked by OCR
  against the page images; Theorem 3, printed p. 125, is the only claim used.
- The three reviewed project proofs were read to scope these comparisons.
  This work changed only this audit note. No tests, project-wide checks, or
  CI checks were run; this was a focused literature comparison.
