# Independent review of the bilinear core-flow sharpening

Date: 2026-10-02. Result: passed the completed
[bilinear corollary](../new-direction/smoothed-bilinear-core-flow.md).
This review uses the separately reviewed arbitrary-boundary theorem and
checks the sharper margin, computational cost and output claims. No
publication-priority claim is assessed.

The original arc marginals are affine in the core: the core-only objective
cancels, the native scalar cost contributes a rational constant, and the
coupling contributes one linear form. Tree potentials and adjusted marginal
charts remain affine. Their rational coefficient heights have a base
polynomial bound despite large native capacities. Identities are coefficient
checks, and minima over rational boxes are endpoint calculations. Inward
derivative minimization over the optimal-flow intervals has linear arc
costs, so it uses the exact linear-cost flow oracle. No algebraic box solve
is needed for these per-level certificate tests.

The affine margin proof is valid for the zero set restricted to the cube,
including zeros only on its boundary. If the value is positive, a minimizing
vertex has value at most zero. Move only coordinates with nonzero
coefficient monotonically toward that vertex and stop at the first zero.
The decrease in value is at least `b_min` times the path's one-norm length.
Its endpoint is a feasible zero, so the path bounds the Euclidean distance
to the restricted zero set. Negative values use a maximizing vertex; values
already zero are immediate. Skipping zero-coefficient coordinates is needed
for this path-length estimate and is explicit in the note.

If the zero set is empty, continuity gives one strict sign throughout the
cube, and the minimum absolute value occurs at a vertex. Clearing the at
most `q+1` coefficient denominators gives the claimed nonzero rational lower
bound. This includes constant polynomials and zero-dimensional faces. Thus
`mu_0=2^(-(k+1)H_0)*delta/2` is uniform, base-computable, and has polynomial
ordinary binary length. The nonlinear gradient-image elimination bound
remains unchanged; only its logarithm enters the earlier tube and distance
budgets. It therefore does not reintroduce the general theorem's larger
value-margin precision.

The original law and failure budgets now have `J,log M=poly_d(I)`. There
are at most `3^k` face attempts per level, rather than per retained cell.
Their polynomial work is absorbed by `8^k Q`, where
`Q=[3+(1+k/2)L/(2sigma)]^k`. One final fixed-flow box optimization gives the
additive `c_d^k` term. The same-draw fallback cancels its base enumeration
factor in expectation and returns only one winning flow and core
representation. The claimed output and refinement bounds follow.

Finally, every fixed-flow core slice is `phi` plus a rational linear term
and constant. Its core Hessian is exactly that of `phi`; coupling strengths
and native capacities do not increase the curvature parameter in the
expected-count factor. If `phi` is quadratic, stationary-face enumeration
returns rational core optimizers and values even when the native scalar
costs have higher fixed degree. Their evaluations at an integer flow are
still rational. These statements concern the sampled objective.

## Targeted verification

A distinct inline `python3` check using exact `Fraction` arithmetic passed
125 restricted-zero-set distance inequalities and 50 empty-zero-set vertex
checks across seven two-dimensional affine fixtures. Distances were
computed by testing the orthogonal projection when feasible and all line
intersections with cube edges. Cases included boundary-only zeros, a zero
coefficient, strongly unequal coefficients, an 80-bit constant, and a
small rational slope. These checks supplement the geometric proof; they
are not a probability simulation or a general solver implementation.

A separate arithmetic reviewer freshly checked Sections 2--3 and also
approved the restricted-zero-set margin, restored polynomial precision,
additive work accounting and rational quadratic-core output. Scoped local
link and whitespace checks passed. No existing flow-search diagnostic was
rerun. No external search, project-wide verification or CI inspection was
performed.
