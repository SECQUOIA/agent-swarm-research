# Prior audit: exact feasibility with a small common quadratic range

Date: 2026-09-28. This is a literature comparison, not an independent proof
review of [the developing FPT theorem](common-range-fpt-frontier.md).
The search found strong nearby
results but no inspected statement directly giving the proposed combined
parameterization. That does not establish novelty.

## Proposed scope and the distinction that matters

For rational quadratic constraints with continuous Hessians `Q_i`, let
`r = codim(intersection_i ker Q_i)`. With positive semidefinite matrices,
this is `rank(sum_i Q_i)`. For squared SOC inequalities, the matrices may
be indefinite; the intersection-of-kernels definition still applies.
An invertible rational change of continuous coordinates writes every row
as a quadratic in `u in R^r` plus an affine function of the remaining
continuous coordinates `v`. Individual matrix rank, Hessian matrix-span
dimension, and common range dimension are different parameters.

The developing claim is exact continuous feasibility in `f(r) N^C` time,
and mixed-integer feasibility in `f(k,r) N^C` time, where `k` is the
integer dimension and `C` is absolute. It allows arbitrarily many
continuous coordinates that enter only linearly after the change of
basis. For boxed integer fibers, the parameter uses continuous Hessian
blocks. Without an integer box, the draft instead requires a common
continuous kernel of the full Hessians, so that eliminated coordinates
also avoid integer-continuous bilinear terms. Joint positive
semidefiniteness makes these two kernels agree. No exact optimizer or
common-field recovery claim is being audited here.

Eliminating `v` by Farkas' lemma produces at most exponentially many
quadratic rows with polynomial coefficient lengths. Enumerating these
rows destroys the desired input-size bound. The proposed method instead
uses the implicit description only to derive radius and positive-residual
bounds, then solves a compact rational LP or MILP outer approximation.
This combination should be credited to its established ingredients.

## Primary comparisons

**Basu--Roy: the quantitative ingredient is established.** In
[*Bounding the radii of balls meeting every connected component of
semi-algebraic sets*, final author manuscript, 5 June
2010](https://www.math.purdue.edu/~sbasu/jsc_final-06-05-10.pdf),
Theorem 3 bounds all bounded components of a weak-sign realization;
Theorem 4 gives a ball meeting every component, including unbounded
ones. Reading the displayed formulas at degree two gives
`log R <= (tau + log(s+1) + 1) 2^{O(d)}` in ambient dimension `d`.
Thus exponentially many implicit Farkas rows do not ruin the bit bound.
The source itself says that asymptotic bounds of this form were already
known. The new work must not claim a new general algebraic radius theorem.
The local final-source text was inspected at Theorems 3--4 and Remark 1.

**Khachiyan--Porkolab: distinguish witness bounds from algorithms.**
[*Integer Optimization on Convex Semialgebraic
Sets*](https://www.math.ucdavis.edu/~deloera/MISC/LA-BIBLIO/trunk/Khachiyan/00230207.pdf),
Theorem 1.1, p. 208, gives an optimal integer point of coordinate bit
length `L D^{O(k^4) product_j O(n_j)}` for a convex set described by a
first-order formula. This bound does not depend on the number of atomic
predicates. The preceding paragraph reduces feasibility to optimization
by adding a zero coordinate. However, Theorem 1.2 has running time
`L^{O(1)} (m D)^{O(k^4) product_j O(n_j)}`. Applying its algorithm to an
exponentially long Farkas formula does not prove FPT. Its witness theorem
can still supply the integer box used by a different algorithm. Both
statements and the formula conventions on pp. 207--208 were read directly.

**Heinz and Hildebrand--Köppe: genuine FPT with explicit rows.**
[*A new Lenstra-type Algorithm for Quasiconvex Polynomial Integer
Minimization with Complexity 2^{O(n log n)}*, v3](https://arxiv.org/pdf/1006.4661),
Theorem 1.1, treats sparsely encoded quasiconvex polynomial inequalities
in `n` integer variables. Its general-case bound is
`s l^{O(1)} d^{O(n)} 2^{2n log_2 n + O(n)}`. At fixed degree this is true
FPT in the total variable dimension, with linear dependence on the
explicit constraint count `s`. The primary introduction also states
Heinz's earlier `s l^{O(1)} d^{O(n)} 2^{O(n^3)}` bound. These are stronger
than generic fixed-dimensional QE, and they cover the pure-integer
special case. They do not directly handle an exponential collection of
projected rows or an unbounded number of existential linear coordinates.
Heinz's full article was not retrieved here; its bound is reported through
the inspected primary Hildebrand--Köppe text.

**Toledo: an important implicit-description precedent, with a stronger parallel application.**
[*Maximizing Non-Linear Concave Functions in Fixed
Dimension*](https://www.tau.ac.il/~stoledo/Bib/Pubs/concave.pdf),
Theorem 4.4, allows a bounded-degree polynomial comparison algorithm that
evaluates a concave objective or returns a violated concave polynomial
valid for a convex set. The paper's sequential analysis gives
`T_0^{2^d}`; the theorem's parallel form is
`O(T_0 (T_p log P)^{2^d-1})`, with dimension-dependent constants.
The generic sequential bound has a dimension-dependent exponent. However,
Section 5, p. 16, applies the parallel theorem to explicit convex
polynomial rows in arithmetic time
`O(m (log m log log m)^{2^d-1})`. The logarithmic powers can be absorbed
into a parameter factor times a fixed power of `m`, so that application
is compatible with FPT arithmetic complexity. This remains an
arithmetic/RAM analysis, not the proposed uniform Turing bit bound.
A generic polynomial-time separation oracle does not automatically
supply the needed parallel comparison algorithm. The definition of an
admissible algorithm, p. 4, also
restricts dependence on the query point; polynomial-time LP cannot be
substituted without checking those restrictions. Definition, complexity
recurrence, Theorem 4.4, and its Section 5 application were inspected.
The last was independently reread during the
[polynomial optimization prior audit](polynomial-nonlinear-dimension-optimization-prior.md).
This is closer prior than
ordinary low-rank objective optimization because the feasible set may
have a superpolynomial implicit description.

**Amenta and the LP-type framework: few-dimensional explicit convex
optimization is old.**
[*Helly-type Theorems and Generalized Linear
Programming*](https://web.cs.ucdavis.edu/~amenta/pubs/helly.pdf),
author manuscript pp. 1--2, explicitly describes expected linear numbers
of calls to a subroutine optimizing over `d+1` convex sets in fixed
dimension. Sections 2 and 5 make the explicit family, well-defined
objective, and unique-minimum conditions clear. Exact fixed-size
algebraic subproblems can supply such primitives for bounded polynomial
data. This does not remove the exponential size of an implicitly
projected family. One must not identify a separation oracle for that
family with the sampling and basis primitives of an LP-type algorithm.
The scanned primary manuscript was inspected through OCR of pp. 1, 2,
4, 5, and 6; the OCR is marked as such in the saved source.

**Del Pia: a stronger one-quadratic comparator and a direct FPT MILP
ingredient.**
[*Convex quadratic sets and the complexity of mixed integer convex
quadratic programming*, v2, 2 February 2024](https://arxiv.org/pdf/2311.00099v2),
Proposition 4, pp. 18--20, handles one convex quadratic inequality plus an arbitrary
rational polyhedron in FPT time parameterized only by the integer
dimension. The continuous dimension and quadratic rank are unrestricted.
The proposed common
range result therefore does not improve this one-row case. Its additional
scope is an arbitrary number of native quadratic constraints sharing a
small continuous curvature subspace. The exact rational optimization
result in Theorem 3 concerns a convex quadratic objective over a
polyhedron, not an arbitrary QCQP. Setting its quadratic to zero gives
the exact `f(k) poly(L)` MILP subroutine required by the candidate theorem,
with arbitrarily many continuous variables. Thus the argument need not
infer a uniform polynomial exponent from Lenstra's original
fixed-dimension wording. Proposition 4 bounds the branching count by a
function of `p`; the final discussion, p. 23, explicitly distinguishes
worst-case FPT from expected FPT and polynomial fixed-dimensional
algorithms. The statement, complete Proposition 4 proof, and that
discussion were read. The existing local filename `delpia-2025` contains
this 2024 v2 manuscript.

## Adjacent terminology and remaining audit limits

Searches included common range, common kernel, fixed rank, nonlinear
variables, implicit convex programming, fixed-dimensional separation,
FPT quasiconvex optimization, and exact SOC feasibility. Low-rank
objective algorithms, numerical low-rank cone factorizations, and
constant-rank constraint qualifications are not matching complexity
theorems.

Pirani's recent
[*Effective curvature dimension in smooth DC
optimization*](https://arxiv.org/html/2609.28319v1), Sections 1 and 3,
explicitly uses Hessian-range subspaces. Its stated algorithmic bound
counts globally solved lower-model subproblems, and expressly makes no
general polynomial-time claim. Thus the common-curvature-subspace idea
itself is not new. Zhao--Fan's *On subspace properties of the quadratically
constrained quadratic program* was located, but the full article was not
successfully retrieved in this audit. Its abstract alone cannot settle
overlap with the exact FPT statement.

The strongest defensible current assessment is that the proposed theorem
would combine classical quantitative algebraic bounds, Farkas projection,
and rational lifted approximation into an exact FPT result with a useful
parameter. The search did not establish that this assembly or an
equivalent formulation is unpublished. The proof and the practical
significance need separate review. An enormous parameter factor may limit
direct implementation even when the result distinguishes FPT from XP.

## Source and verification record

New primary PDFs and extracted text are stored in
`common-range-prior-sources/`: Toledo, Hildebrand--Köppe, and Amenta.
Basu--Roy was read from the existing
`research-20260925/publication-sources/basu-roy-2010-final.txt`.
Del Pia was read from `sources-hessian-span-prior/delpia-2025.txt`.
The Khachiyan--Porkolab primary PDF was read through the linked source.
Search snippets were used for discovery, not as proof of the displayed
theorem comparisons.

No mathematical implementation or project-wide tests were run for this
audit. A targeted inline `python3` check verified the final newline, absence of
trailing whitespace and control characters, and the new local source
files. It returned `PASS` for this note, its one local Markdown link, and
six saved source files. These checks do not establish mathematical
correctness or novelty.
