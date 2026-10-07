# Independent review of mixed-integer gap cell closure

Date: 2026-10-02. Verdict: the stated theorem passes this independent
mathematical review. No substantive gap remains in the reviewed version.
This is a proof assessment, not a claim of publication priority or a
production implementation.

Reviewed:

- [The complete MIQP theorem](../new-direction/smoothed-miqp-cell-closure.md).
- [The integer-label isolation lemma](../new-direction/integer-label-isolation.md).
- The continuous and ambient cell-closure arguments invoked by the theorem,
  with particular attention to which steps need smoothness.
- The exact convex-MIQP oracle contract in
  [Del Pia, Theorem 3](../../literature/papers/pia2025-convex-quadratic-sets-and-the/fulltext.md).
- The source of the targeted rational diagnostic described below.

The review challenges the actual mixed extension, rather than inferring
its correctness from the continuous result. A separate child review
independently checked the exclusion oracle, gap transport, and isolation
argument and reached the same conclusions.

## The new cell certificate is valid

The union of the \(2p\) exclusion constraints contains exactly the
feasible integer tuples different from the returned winner. Overlap is
harmless. Exact minimization over that union therefore gives the true
best-other-label gap and a competing witness. Infeasible exclusions and
the absence of competitors are handled correctly.

For a fixed integer label, subtracting
\(\alpha\|a\|^2/2\) leaves an infimum of affine functions with slopes
\(-\alpha Tx\). Along \(a-v\), every label's value change lies in the
same scalar interval determined by all feasible \(Tx\). Subtracting two
such changes costs the width of that interval, not twice its width.
Consequently the difference between two label values changes by at most
\(\alpha\operatorname{diam}(T\mathcal P)\|a-v\|\).
The prescribed \(\Lambda=\alpha k C_T\) safely bounds this change over
the cell.

Thus a fixed-label critical region covering the cell and a corner gap
\(\Delta(v)\ge\Lambda h_j\) certify its whole mixed value function.
Equality is safe: another label may tie inside the cell without
invalidating the certified value or feasible witness. Matching corner
labels alone would not suffice; the diagnostic includes a counterexample.

Exact convex-MIQP values and feasible witnesses are essential. The
argument does not justify substituting numerical primal values, local
solutions, or uncertified solver gaps.

## Nonsmooth mixed recourse does not invalidate the rare-event argument

For every attaining mixed witness \(x\) at \(v\), its quadratic
\(Q_x\) bounds the envelope above everywhere and touches it at \(v\).
Because \(\min Q_x\ge\min V_\gamma\), completing the square gives

\[
 \|\alpha(v-Tx)+d\|^2
 \le 2\alpha\bigl(V_\gamma(v)-\min V_\gamma\bigr).
\]

This holds for every active witness, including at an integer tie. There
is no appeal to a mixed-envelope derivative or to a specially chosen
subgradient. Once a label is fixed, the inherited kernel condition
\(\ker P_{cc}\subseteq\ker T_c\) gives the smooth slice needed for
continuous critical-region extraction. Indeed, a zero quadratic form of
\(P_{cc}\) extends to a zero quadratic form of the full positive
semidefinite \(P\), so the full kernel condition applies.

The response Hessians use only fixed matrices. Label values and residual
noise enter their affine offsets. Hence the stated Cramer's-rule bound
is independent of the noise denominator. A failed fixed-label region
test produces one of finitely many fixed ambient hyperplanes. Its normal
is nonzero because the ambient normal \(w\) satisfies \(Tw=u\) for a
nonzero factor normal \(u\). Enlarging the count by all bounded integer
labels changes only a quantity whose logarithm enters the cutoff.

## Isolation controls the adaptive gap failure

The isolation lemma includes missing integer groups, nonproduct feasible
label sets, zero gaps, simultaneous crossings, and noise endpoints.
Conditioning on the other coefficients produces lines with distinct
integer slopes. A near-winning different group forces a lower-envelope
breakpoint within \(\varepsilon\), even if a third line intervenes
before the selected pair crosses. Each envelope has at most its integer
coordinate width many breakpoints.

The mixed application now explicitly assumes continuity on a compact
mixed feasible set. This corrects the earlier wording: compactness alone
would not ensure attained finite slice minima for an arbitrary objective.
Quadratic objectives satisfy the corrected assumption.

At a near-optimal auxiliary corner, square completion bounds the original
objective of both the winning and competing witnesses by
\(f_\gamma^*+2B_j+\Delta(v)\). If the gap test fails, this is at most
\(f_\gamma^*+C_{\rm gap}h_j\). Two distinct near-optimal feasible
labels imply a small gap between the best two original labels, even if
neither queried label is itself globally best. This is one event about
the original problem. It requires no union over adaptively visited
corners.

The integer widths in the isolation bound may be numerically enormous.
They occur in the refinement and sampling choices through their
logarithms; they have not been silently replaced by encoding lengths
inside the probability inequality.

## Finite sampling and exact work are noncircular

At a fixed query and along one original noise coordinate, each fixed-label
KKT basis supplies a quadratic on an interval. Unlike the continuous
case, values of different labels need not agree where their intervals
overlap. The theorem correctly adds all pairwise quadratic intersection
points. With at most \(R\) candidates there are at most \(2R^2\)
partition points. Identical quadratics need no split; singleton feasible
intervals and isolated event points are covered by the generous component
bound. This bound is uniform in the fixed values of the other
coefficients, as required by the product-measure replacement argument.

The cutoff \(J\), fallback count \(B\), component count, and noise
precision \(N\) depend only on base data. Their logarithms have
polynomial length. The two terms of the failure probability are bounded
by \(1/(2B)\) each. The same-draw fallback costs
\(B\operatorname{poly}(I+\log N)\), including infeasible labels and
singular or lower-dimensional slices, so its expected cost is polynomial.
There is no rejection sampling or assumption excluding ties.

Del Pia's primary statement defines accurate solution to include an
attaining optimizer and optimum value, and Theorem 3 gives fixed-parameter
time in the integer dimension. This supports the required oracle.
Bounded integer coordinates have polynomial height from the original LP
ranges. Fixing the returned label and polishing its continuous slice
gives polynomial-height values and witnesses for subsequent operations.
The proof therefore does not propagate a merely parameter-dependent
oracle output-height bound into later oracle instances.

The expected result remains \(f(p)C^k(1+H_{\rm amb})\operatorname{poly}(I)\).
Its ambient geometric factor has dimension powers depending on \(k\).
It is not a dimension-free FPT theorem in \((p,k)\), and it solves the
sampled objective rather than the unperturbed instance.

## Targeted diagnostic and its limits

The author ran
`python research-20261002/new-direction/check_smoothed_miqp_closure.py`
and reported a pass: 23 rational cases, 134 levels, 463 cells, 90 gap
closures, 152 prunes, 137 gap events, and 84 slice-region events.
This review inspected the diagnostic source rather than repeating that
command.

The diagnostic uses exact fractions and an explicit one-binary,
one-continuous recourse oracle. It analytically checks whole-cell
dominance against every competing slice piece, compares exact solutions
with a separate original-slice minimization, and checks the incumbent,
active-gradient, and two-witness bounds. It includes coupled variables,
positive, zero, and negative original continuous curvature, an exact
finite-grid tie, a corner-label counterexample, and a deliberately
zero-stage cap to exercise same-draw fallback.

Those checks give distinct evidence for the new certificate and failure
events. They do not implement the general fixed-parameter convex-MIQP
oracle, validate asymptotic probability bounds by simulation, or establish
practical performance. The separate isolation diagnostic was run by the
parent researcher and is recorded in its lemma note.

A scoped Python check of this review passed: trailing whitespace,
paired mathematical delimiters, and existence of local link targets.
No project-wide verification, CI inspection, or external literature
search was performed for this review.
