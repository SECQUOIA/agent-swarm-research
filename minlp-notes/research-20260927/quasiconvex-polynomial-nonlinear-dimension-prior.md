# Prior audit: quasiconvex polynomial optimization with a large linear part

Date: 2026-09-28. This audit concerns the proposed exact algorithm for
globally quasiconvex polynomial rows with few nonlinear continuous
directions. It supplements the [convex feasibility audit](polynomial-nonlinear-dimension-prior.md)
and [convex optimization audit](polynomial-nonlinear-dimension-optimization-prior.md).
It does not certify the proposed proof or establish priority.

The closest algorithmic prior already handles quasiconvex polynomial
integer optimization with fixed-parameter complexity. The candidate
addition is a uniform exact Turing bound with arbitrarily many linear
continuous coordinates, together with exact continuous optimizer output.
The extension from convex to quasiconvex native rows is a useful widening
of a structural result, but the inspected literature does not support
calling it a new general quasiconvex optimization method.

## Model and the proposed difference

The candidate has rational, explicitly encoded data and the form

\[
 \min\{g_0(z,u,v):g_i(z,u,v)\leq0\ (1\leq i\leq m),\quad
 z\in\mathbb Z^k,\ u\in\mathbb R^r,\ v\in\mathbb R^n\},
 \qquad g_i(z,u,v)=C_i v+p_i(z,u).
\]

Each full function `g_i`, including the objective, is globally
quasiconvex on its real ambient space. The `C_i` are constant rational
rows and the polynomial degrees are at most `d`. With total input length
`N`, the proposed bound is `f(k,r,d) N^c` with absolute `c`. Neither `m`
nor `n` is a parameter. Finite output would include the exact algebraic
value and an optimizer represented over one real number field.

Quasiconvexity here means convexity of every sublevel set. It is a promise
about the full real function, not only about its restriction to feasible
points or integer fibers. A supplied affine change of coordinates must
count toward the input. The objective must participate in the common
nonlinear core.

An elementary restriction is central to the scope. If `C_i` is nonzero,
restrict `v` to a line on which `C_i v` ranges over all real numbers. The
zero sublevel becomes `{(y,t):p_i(y)+t<=0}`. Its convexity is equivalent
to convexity of `p_i`. Thus the rows newly admitted by the quasiconvex
extension have `C_i=0`. Every row coupled directly to the large linear
part remains convex. This follows from the usual epigraph characterization;
it should not be promoted as an independent structural discovery.

The zero rows of `C` also explain why the proposed Farkas projection can
retain quasiconvex polynomials. A vertex of
`{lambda>=0:C^T lambda=0, 1^T lambda=1}` that assigns positive mass to a
zero row of `C` is the corresponding unit vector; otherwise it is a
nontrivial convex combination of that unit vector and another feasible
multiplier. Other vertices combine only convex rows. This is an elementary
reduction for this model, not a claim that arbitrary nonnegative sums of
quasiconvex polynomials remain quasiconvex.

## Strongest exact algorithmic predecessors

**Heinz and Hildebrand–Köppe already give the integer algorithm.** Heinz,
[*Complexity of integer quasiconvex polynomial optimization*](https://www.damtp.cam.ac.uk/user/na/FoCM/FoCM05/Posters/heinz.pdf),
2005, gives the pure-integer formulation and complexity
`s l^O(1) d^O(a) 2^O(a^3)` in the author poster. The full original article
was not obtained; its internal theorem assumptions are not asserted here.

Hildebrand–Köppe,
[*A new Lenstra-type Algorithm for Quasiconvex Polynomial Integer Minimization with Complexity 2^O(n log n)*](https://arxiv.org/pdf/1006.4661),
Theorem 1.1, improves the unbounded-input bound to
`s l^O(1) d^O(a) 2^O(a log a)` for explicitly listed quasiconvex
polynomials in `a` integer variables. It returns an optimal integer point
or reports that none exists; its output-size bound is `l d^O(a)`,
independent of the row count. Objective bisection is already in its proof.
Sections 5.2–5.3 handle stationary gradients by probing the selected
polynomial at additional points. Theorem 5.7 needs membership tests and
one violated polynomial, so an implicit-row implementation is a deduction
from this proof. Uniform coefficient bounds and the integer recursion
still need justification. These passages and the theorem were reread.
The original theorem has no continuous algebraic optimizer output.

In particular, the convex shortcut that a violated row with zero gradient
certifies emptiness fails here: `x^3<0` is feasible although its gradient
vanishes at the rejected query `x=0`. Using the established quasiconvex
shallow-cut construction is a substantive proof obligation, not a new
separation principle.

**The mixed-integer extension has already been described as folklore.**
The later published version of Gavenčiak–Koutecký–Knop,
[*Integer Programming in Parameterized Complexity: Five Miniatures*](https://iuuk.mff.cuni.cz/~koucky/EPAC/papers/disopt.pdf),
2020, Appendix A.1, pp. 24–25, retains the statement from its earlier
*Three Miniatures* version that the cited convex integer algorithms have
a folklore FPT mixed-integer extension. The passage immediately follows
mixed linear programming with many continuous variables, but it does not
state a formal mixed polynomial theorem specifying its continuous
dimension parameter, exact oracle implementation, or algebraic output.
Theorem 26 itself is pure integer. The published passage is therefore
material priority pressure. It is not sufficient evidence either that
the displayed candidate is already proved there or that its unrestricted
linear continuous part is absent from the intended folklore. The final
version and surrounding definitions were inspected.

**Khachiyan–Porkolab already supply broad first-order size bounds.**
[*Integer Optimization on Convex Semialgebraic Sets*](https://www.math.ucdavis.edu/~deloera/MISC/LA-BIBLIO/trunk/Khachiyan/00230207.pdf),
Theorem 1.1 and Corollary 2.3, provide integer bounds and real algebraic
sample encodings whose degree and height bounds do not depend on predicate
count. Quantified dimensions do enter the bounds, and the algorithm
charges for the explicit formula. The candidate must remove the large
linear block before applying those size bounds and avoid enumerating an
exponential projection. This comparison reuses the directly inspected
primary statements documented in the convex optimization audit.

## Implicit optimization and affine directions

Toledo,
[*Maximizing Non-Linear Concave Functions in Fixed Dimension*](https://www.tau.ac.il/~stoledo/Pubs/concave.pdf),
Theorem 4.4, allows a restricted polynomial-comparison evaluator and
concave polynomial separators. It treats a concave objective, rather than
arbitrary quasiconcave objectives, in an arithmetic model. Its Section 5
explicit convex-polynomial application has bound
`O(m (log m log log m)^(2^a-1))`; logarithmic powers can be absorbed into
a parameter factor times a fixed power of `m`. This application is
compatible with FPT arithmetic complexity. It is not an exact Turing
bound for a general LP-based evaluator. The definition, theorem, and
application were reread in the saved primary text.

Norton–Plotkin–Tardos,
[*Using separation algorithms in fixed dimension*](https://ecommons.cornell.edu/server/api/core/bitstreams/36e75f7f-421a-43aa-b069-052b4c6850d7/content),
Theorems 2.3–2.4 and 3.1, already optimize from suitable affine-comparison
separation algorithms and avoid enumerating projected LP facets through
dual certificates. Their comparison model differs from the polynomial
one here. This comparison is carried forward from the independently
checked convex feasibility audit.

Slot–Steurer–Wiedmer,
[*Hesse's Redemption: Efficient Convex Polynomial Programming*](https://arxiv.org/abs/2511.03440),
Theorem 1.3, gives an effective affine-direction decomposition for convex
polynomials. Its continuous objective-over-polyhedron algorithm is
stronger in ambient dimension for that special setting, but does not
cover arbitrary quasiconvex polynomial constraints. The primary statements
and encoding were inspected in the preceding audits. A full Hessian
annihilator still gives an elementary affine-direction test for arbitrary
polynomials. The positive-semidefinite argument for using only continuous
Hessian blocks belongs specifically to the convex case. The candidate
extension now supplies a separately reviewed affine-direction argument
that proves the same block-kernel equality under global quasiconvexity;
see its [Section 6](quasiconvex-polynomial-nonlinear-dimension-frontier.md#6-intrinsic-directions).
The limited prior search did not identify this precise lemma, which does
not establish its novelty.

There are older general links between convexity and linear perturbations.
Aussel–Corvellec–Lassonde,
[*Subdifferential Characterization of Quasiconvexity and Convexity*](https://www.heldermann-verlag.de/jca/jca01/jca01014.pdf),
Proposition 2.1(i), says that a function is convex exactly when all linear
perturbations are quasiconvex. The proposition and proof were read.
Pham Duy Khanh–Lassonde,
[*Linear Perturbations of Quasiconvex Functions and Convexity*](https://arxiv.org/pdf/1502.03897),
the theorem on p. 1, weakens the family to all scalar multiples of one
nonconstant linear form under a boundary regularity hypothesis; that
hypothesis is vacuous on a full vector space. Its proof and limitations
were read. These support treating the elementary nonzero-`C_i` observation
as part of established convexity theory. They are not polynomial
mixed-integer complexity theorems.

## Structural restrictions on the claimed enlargement

Ahmadi–Olshevsky–Parrilo–Tsitsiklis,
[*NP-hardness of deciding convexity of quartic polynomials and related problems*](https://www.mit.edu/~jnt/Papers/J143-13-convex-poly-complexity.pdf),
Proposition 4.6, proves that every odd-degree globally quasiconvex
polynomial is `h(a^T x)` for a monotone univariate polynomial `h`.
Its sublevels are halfspaces. Theorem 4.11 proves that even homogeneous
quasiconvex polynomials are convex. Both statements and proofs were read.
Consequently, additional curved native sublevels require nonhomogeneous
even-degree rows. The paper gives `x^4-8x^3+18x^2` as a quasiconvex,
nonconvex example. That univariate example shows strict inclusion of
function classes; it does not show new geometric modeling power, since
its sublevels are intervals. Corollary 4.13 establishes hardness of
recognition in variable dimension. This does not obstruct algorithms
parameterized by the number of nonlinear variables, but reinforces the
need to distinguish a promise from a recognition algorithm.

A related search result must be excluded: Heinz,
[*Quasiconvex functions can be approximated by quasiconvex polynomials*](https://www.esaim-cocv.org/articles/cocv/pdf/2008/04/cocv0668.pdf),
uses quasiconvexity in the calculus of variations, as its abstract and
introduction explicitly state. It does not concern convex sublevel sets.
Searches for affine directions and quasiconvex polynomials frequently
returned this different terminology.

## Attainment and significance

Bank–Mandel's 1987 result already applies to rational globally
quasiconvex polynomial mixed-integer systems. Theorem 3(iii) and Theorem
7(ii) in the
[primary publisher preview](https://api.pageplace.de/preview/DT0400.9783112720936_A50662169/preview-9783112720936_A50662169.pdf)
give the relevant closed right-hand-side feasibility domain, as recorded
in the [attainment audit](mixed-integer-attainment-prior.md). Appending
the objective as a row gives finite attainment. This comparison reuses
the independently checked primary statements from the preceding audits;
the preview omits the proof of Theorem 7. The quasiconvex extension must
not claim a new existence theorem or include nonattainment as an actual
status under these assumptions.

The plausible useful contribution is the same uniform exact complexity
and output theorem as in the convex case, under the wider row promise.
It could permit exact certification for quasiconvex response constraints
on a small aggregate vector coupled to a large linear model. This is a
possible capability, not demonstrated solver acceleration. Important
remaining work includes identifying application families whose advantage
does not disappear under elementary monotone reformulation, obtaining
usable parameter bounds, and implementing the exact oracles.

The primitive-row reduction is especially simple once the convex result
and the older quasiconvex integer machinery are available. It is more
credible to present it as a corollary or extension than as a separate
major breakthrough. No inspected source explicitly states the entire
candidate theorem with this parameterization and output representation.
That search outcome does not establish novelty, particularly in light
of the published mixed-integer folklore statement.

## Search and verification record

Searches included exact mixed-integer quasiconvex polynomial optimization,
few nonlinear variables, partially linear quasiconvex programming, linear
continuous variables, affine directions, odd-degree representations, and
convexification. The primary sources and precise passages inspected in
this audit are identified above. Previously inspected comparisons are
explicitly marked as reused. The original Heinz 2005 full article was
not obtained; the primary author poster was available. No stronger
statement is inferred from inaccessible text or from a secondary abstract.

Local primary texts reread were
`common-range-prior-sources/hildebrand-koppe.txt`,
`common-range-prior-sources/toledo.txt`, and
`polynomial-dimension-prior-sources/gavenciak-knop-koutecky-1711.02032.txt`.
The final *Five Miniatures* paper, both perturbation papers, and the
Ahmadi et al. paper were read through the web PDF tool. The subsequent
[full theorem review](quasiconvex-polynomial-nonlinear-dimension-review.md)
independently inspected the material *Five Miniatures*, Ahmadi et al.,
Hildebrand--Koppe, and Bank--Mandel comparisons. The parent researcher
also independently reopened Appendix A.1 of the final *Five Miniatures*
paper and Proposition 4.6 and Theorem 4.11 of Ahmadi et al. and confirmed
their stated scope. These are focused checks of important comparisons,
not an exhaustive independent novelty search.

Targeted checks for this file covered local Markdown links, final newline,
trailing whitespace, control characters, and `git diff --check`. No
project-wide verification, CI inspection, numerical experiment, or Lean
formalization was performed for this literature audit.
