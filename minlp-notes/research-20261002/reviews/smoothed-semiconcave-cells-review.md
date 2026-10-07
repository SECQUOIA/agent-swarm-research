# Independent review of the smoothed cell count

Date: 2026-10-02. Scope: the complete
[expected-cell theorem](../new-direction/smoothed-semiconcave-cells.md),
its anisotropic meshes, finite-bit perturbations, and convex quadratic
recourse application. No substantive gap was found in the stated
approximation result. No priority claim is made.

## The probability argument avoids hidden conditioning

At a fixed interior grid coordinate, being \(\delta\)-near-optimal
requires both neighboring comparisons. They force the corresponding
linear noise coefficient into an interval with length at most
\(\alpha h_i+2\delta/h_i\). Its endpoints depend only on the
fixed base function, grid node, and deterministic tolerance. All other
noise coordinates cancel from the comparisons. Independence therefore
applies directly, without conditioning on an adaptively chosen incumbent
or optimizer.

Summing the resulting product bounds over the complete tensor grid
factors by coordinate. Boundary coordinates need no restriction on their
noise coefficient and contribute the two endpoint choices. The argument
works for either global or complete-grid near-optimality. It does not
assume a differentiable value function, convex objective, unique optimizer,
or quadratic growth.

The adaptive algorithm uses this deterministic full-grid count only as
an upper bound. It does not claim that its adaptively chosen queries are
independent of the sampled coefficients. This distinction is correct.

## The mesh and incumbent details are necessary

The equal dyadic subdivisions of each original interval are nested. With
global scale \(h\), every coordinate having interior nodes has mesh
\(h_i\in(h/2,h]\). An unrefined coordinate has only its two
endpoints, so a very short original interval contributes no factor
\(1/h_i\) to the probability count. Substituting
\(\delta=2B\), \(B=\alpha\sum_i h_i^2/8\), gives the
claimed bound \((1+2k)\alpha h_i\).

A clipped last interval would require a different argument: its tiny
terminal gap could introduce a term \(\delta/\text{gap}\) in
the neighboring comparison. The reviewed construction explicitly uses
equal subdivisions and avoids this issue.

Retention uses the completed level's incumbent and keeps cells with
lower bound at most that incumbent. A cell containing an optimizer
therefore always survives, including equality cases. Its corner values
give incumbent error at most \(B\). Every surviving cell has a
\(2B\)-near-optimal corner, and every grid corner belongs to at most
\(2^k\) cells. This proves the deterministic survivor bound and the
expected evaluation bound \(2^k+8^kHJ\).

The global certificate also checks out. Every processed cell lower bound
is at least \(U-B\). Discarded cells had lower bounds above the
incumbent at discard time and hence above every later incumbent. The
smallest surviving lower bound and current incumbent thus form a valid
interval of width at most \(B\), for every realization of the noise.

## The finite-bit limitation is real and is correctly stated

For an \(M_i\)-point uniform noise grid, interval probability is
bounded by length divided by \(2\sigma_i\), plus \(1/M_i\).
After summing grid nodes, the extra term is
\((m_{ij}-1)/M_i\). Requiring \(M_i\ge m_{iJ}\) controls it
through the prescribed terminal level and yields the stated rational
noise bound. Sampling once from that distribution and retaining the same
sample throughout the algorithm is sufficient.

This condition cannot simply be dropped. In one dimension, choose an atom
\(c_0\) of a fixed finite noise law and base function \(f(x)=-c_0x\)
on \([0,1]\). When the sampled noise equals \(c_0\), the
perturbed objective is flat. Every node is globally optimal, so the
expected near-optimal count is at least \((m+1)\Pr(c=c_0)\).
With a supplied positive curvature bound, every cell also survives the
reviewed corrected-corner algorithm on that event. The count grows with
mesh refinement. The note correctly limits its rational result to a
noise resolution chosen for the requested accuracy.

An exact-recovery precision that itself depends on the number of noise
bits cannot automatically be inserted into this prescription. A separate
argument would be needed to close that dependence or analyze the atomic
events. No fixed-law exact-optimization claim is established by this
review.

## The Fenchel application preserves the noise model

For \(F_d(x)=F(x)+d^TTx\), the correct auxiliary objective is
\(W(a)+d^Ta\). Its optimum differs from the original one by
\(-\|d\|^2/(2\alpha)\), and an auxiliary optimizer has the
form \(Tx^*-d/\alpha\). Bounded supports
\(|d_i|\le\sigma_i\) justify the fixed enlarged box
\([\ell_i-\sigma_i/\alpha,u_i+\sigma_i/\alpha]\).
This box is chosen before sampling and keeps the probability argument
valid. A realized-noise-dependent box would not satisfy that argument
without further work.

The recourse witness satisfies the stated shifted original upper bound,
so an auxiliary certificate produces an original feasible certificate
with no increase in gap. The exact rational version uses ordinary exact
convex-QP solves at rational auxiliary nodes. The real-noise version
still assumes exact arithmetic and comparisons; the cell count alone is
not a Turing-model claim for arbitrary real samples.

Finally, independent noise in the factor coordinates produces
\(T^Td\) in the original linear coefficients. Those coefficients
are generally correlated and supported on a lower-dimensional space.
The note makes this restriction explicit. The theorem does not thereby
cover independent perturbations of every original coefficient.

## Targeted verification

The command
`python research-20261002/new-direction/check_smoothed_cells_review.py`
passed exact rational checks on a nonsmooth two-dimensional base function
given by a positive quadratic plus the minimum of two affine functions.
Its coordinate widths were \(1\) and \(3/16\), exercising
unrefined short coordinates and unequal active mesh sizes.

Across six levels and all 81 combinations of two nine-point noise
coordinates, the checker verified 1,425 near-optimal events and 1,287
necessary coefficient-interval conditions. It checked the exact average
near-optimal counts against the finite-noise product bound. It then ran
the adaptive algorithm: 3,979 processed cells and 1,414 surviving cells
passed the objective-interval, mesh-error, and near-optimal-corner count
checks. Exact minima were computed independently by minimizing each of
the two convex quadratic branches over the original box.

The checker also records the elementary growing lower bound from a fixed
noise atom. These are targeted diagnostics, not a proof of asymptotic
runtime. The scoped command
`git diff --check -- research-20261002/reviews/smoothed-semiconcave-cells-review.md research-20261002/new-direction/check_smoothed_cells_review.py`
passed, as did an inline `python - <<'PY'` check of whitespace,
mathematical delimiters, and local references. No project-wide checks,
CI inspection, or external search were performed.
