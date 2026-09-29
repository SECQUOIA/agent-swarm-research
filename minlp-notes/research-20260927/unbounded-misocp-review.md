# Independent review of the unbounded mixed-integer SOCP extension

Date: 2026-09-27. Status: independent proof reconstruction and comparison
with the complete manuscript completed. No gap was found in the compressed
projection argument, the integer-witness bound, or their stated composition
with the bounded SOCP reduction. This is a mathematical review, not a formal
proof or a priority determination.

The reviewer did not devise the proposed generic-perturbation projection
construction. The reviewed manuscript is
[unbounded-misocp-frontier.md](unbounded-misocp-frontier.md). Its dependencies are
[nonconvex-hessian-span-frontier.md](nonconvex-hessian-span-frontier.md) and
the primary small-integer-point theorem of Khachiyan and Porkolab. The
algorithmic SOCP conclusion additionally depends on the separate
[bounded rational outer-approximation theorem](socp-hessian-span-frontier.md).
Its full statement and the composition of its boxes and parameters were read
for this review; its rational cone construction has a separate independent
audit and was not reconstructed again here.

## Scope and separation of conclusions

Let `z` be `k` integer coordinates and `x` arbitrarily many continuous
coordinates. Consider rational quadratic weak inequalities and affine
equalities, and let `h` be the dimension of the rational linear span of the
`xx` Hessian blocks. No bounds on either group of variables are supplied.

The compressed projection argument applies without convexity: the set of
real parameters `z` with a nonempty continuous fiber admits a first-order
description with polynomial atom degree and coefficient bit length and
quantifier blocks of dimensions `1,1,h+1` (with harmless padding when
needed). Its Boolean part can be large. If this projection is convex, the
description gives a feasible integer vector of bit length
`N^{O((h+1)(k+1)^4)}` whenever one exists.

Convexity of the projection alone does not turn this witness bound into a
polynomial-time algorithm. An NP-hard fixed-span nonconvex feasibility
problem can be made independent of an extra parameter, giving a projection
that is either empty or the whole line. For rational SOCP, a separate
bounded rational outer-lift theorem supplies the algorithmic step after the
integer and continuous radius bounds have been established.

The unbounded reduction initially preserves nonemptiness and permits
returning a feasible integer assignment. It does not preserve every
feasible assignment of the unbounded input. A continuous point returned by
the outer MILP need not be SOC feasible; exact continuous recovery needs its
own argument.

## Independent audit of the projection construction

### Parameter-dependent affine lift and all ranks

A rational basis `B_1,...,B_h` of the continuous Hessian span permits the
lift `y_j = x^T B_j x/2`. Every original quadratic row becomes an affine
inequality in `w=(x,y)` whose coefficients are polynomial in `z`. The
remaining `h` equations are `F_j(w)=x^T B_j x/2-y_j=0`. All original
affine inequalities remain in this parameter-dependent polyhedron.

For each subset of polyhedral rows, consider its affine equality system
`B(z)w=d(z)` together with all original equalities. All possible pivot
ranks and minors must be included. A nonzero pivot determinant, the
particular-solution identity `B(z)a(z)=d(z)`, and the kernel identity
`B(z)V(z)=0` certify a chart `w=a(z)+V(z)u`. Its free-coordinate rows form
an identity matrix, so these guards certify the full affine solution
space, including at parameter values where the rank drops.

For example, `z x=0, x>=1` has continuous projection `{0}` and continuous
Hessian span zero. The generic rank-one chart misses its only feasible
parameter. The rank-zero chart covers it. Thus generic-rank charts alone
would invalidate the claimed theorem.

The number of charts can be exponential. Their individual determinant
degrees and coefficient bit lengths remain polynomial in the input length.
Neither the real value of `z` nor a bound on its magnitude is substituted
into these symbolic coefficient bounds.

### One finite perturbation grid works at every real parameter

This is the central extra issue relative to the convex quadratic proof.
Fix an arbitrary real `z`. It need not be rational or algebraic. For every
valid positive-dimensional affine chart and every oriented subset of the
`h` bands, apply the quantitative genericity lemma to

```
r_epsilon(w) = ||w||^2 + epsilon P_0(w),
sigma (F_j(w) + epsilon^2 P_j(w)) - epsilon = 0.
```

At each fixed nonzero `epsilon`, restricting freely chosen ambient
quadratics `P_j` to that chart is surjective onto all chart quadratics.
Consequently the pulled-back bad polynomial is a nonzero polynomial in
`epsilon` and the perturbation coefficients. At least one coefficient in
its expansion in `epsilon` is a nonzero polynomial in those coefficients.
Multiply one such polynomial for each valid chart and oriented subset.

The resulting polynomial can have real coefficients depending on the fixed
`z`. This causes no problem: grid avoidance requires only that a polynomial
is nonzero and has bounded degree, not that its coefficients have bounded
height. The genericity lemma's degree bound and the number of chart/support
choices give one degree bound `D=2^{poly(N)}` independent of the numerical
value of `z`. A nonzero polynomial of total degree at most `D` cannot vanish
at every point of the integer grid `{0,...,D}^p`.

It follows that one finite grid of integer perturbation tuples suffices for
every real parameter. The successful tuple can depend on `z`. The argument
does not assert that a single tuple works at all real parameters.

Each tuple has polynomial coefficient bit length, and it can be represented
by one disjunct without quantifying its coefficients. This distinction is
essential: existentially quantifying all quadratic perturbation coefficients
would destroy the small bound on quantified dimension. The finite grid and
all chart choices need not be enumerated by the eventual algorithm.

### Bounded perturbed minimizers and few stationarity variables

For a feasible fixed fiber, any exact lifted feasible anchor remains feasible
for all sufficiently small positive `epsilon`, since the perturbation of
each equation is of order `epsilon^2` while the band has width `epsilon`.
The objective is uniformly coercive for sufficiently small `epsilon`.
Comparing a global minimizer with this anchor bounds a sequence of minimizers
in one compact set. No input bound or quantitative estimate on the unknown
anchor is needed here.

At such a minimizer, restrict all active polyhedral rows to equalities. The
remaining affine rows are strict locally, so the minimizer is a local
minimum in the resulting chart. At most one orientation of each band can
be active. Genericity gives linearly independent active nonlinear gradients
and an invertible stationarity Hessian; ordinary KKT therefore supplies at
most `h` nonlinear multipliers. A zero-dimensional chart supplies its point
directly.

The objective Hessian need not stay positive definite after adding the KKT
terms, because the perturbed nonlinear equations can be indefinite. The
proof needs the explicit generic invertibility assertion; it cannot borrow
the PSD stationarity argument from the earlier convex quadratic note.
Adjugates then give actual rational candidate points
`W(z,epsilon,lambda)`, guarded by the nonzero stationarity determinant.

The argument only needs candidates that approach some feasible limit. It
does not need uniqueness of the perturbed minimizer, bounded multipliers,
or a uniform rate of convergence in `z`. Passing to subsequences is valid
because there are finitely many chart and support choices.

### The common quantifier prefix describes fibers exactly

Place the finite disjunction over perturbations, charts and supports under

```
exists R>0, for every delta>0,
    exists epsilon>0 and at most h multipliers:
        chart and denominator guards hold,
        ||W(z,epsilon,lambda)||^2 <= R,
        W belongs to the full original lifted polyhedron P_z,
        |F_j(W) + epsilon^2 P_j(W)| <= epsilon for every j.
```

Require `epsilon<delta`, as in the manuscript. The selected band equalities
can also be checked, although the reverse implication does not need them.
Zero-dimensional charts can ignore the last block and check their point
exactly. The forward implication follows from a bounded convergent sequence
of perturbed minimizers. The entire lifted polyhedron is retained, including
affine rows omitted only for the local KKT argument.

Conversely, fix a real `z` satisfying this formula. Choose `delta=1/j` and
the candidate point provided by any successful disjunct. These are actual
points, because all rational denominators are guarded. They lie in one ball
chosen before `delta`. Since the perturbations range over a fixed finite
grid, the numbers `P_j(W)` stay uniformly bounded on that ball, even if the
chosen grid point changes. The bands and `epsilon<delta` therefore give
`F_j(W)->0`. A convergent subsequence stays in the closed polyhedron `P_z`
and satisfies every unperturbed lift equation in the limit. Hence the fixed
fiber is feasible. The chart, support, and multipliers may also change;
boundedness and retention of all lifted rows make this harmless.

The radius quantifier is necessary. The SOC-representable quadratic system

```
x^2 <= 0,  1-xy <= 0,  x+y >= 0
```

is empty. Nevertheless `x=1/t, y=t`, for positive integers `t`, satisfies
every row to quadratic violation at most `1/t^2`. The second and third rows
are equivalent to `||(2,x-y)||_2 <= x+y`. Thus even in SOCP a vanishing
residual sequence need not yield a feasible point when its norm is
unbounded. The displayed formula rules this out. Its proof takes limits
only in continuous coordinates at a fixed `z`, so it also does not replace
a nonclosed projection by its closure.

### Atom bounds and the primary integer-point theorem

Rational input denominators, rank-chart denominators, stationarity
determinants, and adjugates involve matrices of polynomial dimensions and
entries of polynomial degree and coefficient bit length. Their resulting
numerators and denominators have degree and coefficient bit length
`N^{O(1)}`. Perturbation coefficients from the common finite grid have
polynomial bit length as well. Multiplying inequality denominators by
positive even powers, while retaining explicit nonzero guards, preserves
their signs at every valid parameter.

The primary text of
[Khachiyan--Porkolab, *Integer Optimization on Convex Semialgebraic Sets*](https://www.math.ucdavis.edu/~deloera/MISC/LA-BIBLIO/trunk/Khachiyan/00230207.pdf),
Theorem 1.1, page 208, was inspected directly. It permits arbitrary Boolean
combinations of polynomial predicates, requires convexity of the solution
set, and gives an integer-coordinate bit bound independent of the number
of predicates. Feasibility is covered by adjoining a coordinate fixed to
zero. Substituting the three quantified block dimensions `1,1,h+1` and the
polynomial atom bounds yields `N^{O((h+1)(k+1)^4)}`. No closedness hypothesis
is imposed on the convex projection.

The large Boolean formula is used only to bound a witness. Applying the
runtime theorem to its potentially exponential length would not prove the
desired polynomial-time algorithm. Instead one computes a conservative
integer box from the witness bound, then a continuous box from the
nonconvex small-point theorem on each bounded integer fiber. For rational
SOCP the separate bounded outer-MILP reduction and fixed-integer-dimension
MILP algorithm can then decide feasibility.

## Verification limits

This audit independently reconstructs the parameter-dependent proof and
checks the precise imported integer-point theorem. The rank-drop and
unbounded-residual examples are exact symbolic counterexamples to tempting
omissions, not a proof of the general theorem. No Lean verification,
implementation of the full algorithm, project-wide test, or CI inspection
was performed. The candidate contribution is the small-quantified-dimension
description; the imported integer-point theorem and generic KKT machinery
are established tools. This review does not establish novelty.

The targeted inline Python check of this review's final newline, trailing
whitespace, control characters, and local Markdown link targets passed.
