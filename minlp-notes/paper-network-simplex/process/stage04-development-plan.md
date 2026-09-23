# Candidate constructive extension for Stage 4

The earlier bounded-rank result gives separation in `2^{O(r^2)}` times sparse
input length but explicitly leaves an equally direct decomposition algorithm
unproved. The root identified a candidate extension while planning the writing
stage. This is not accepted until the Stage 4 author develops it and the five
reviewers verify it.

Let M be the finite state-normal matrix and R the complete support-direction
library from the bounded-rank theorem. Each suffix Minkowski sum is described
exactly by its supports on R. Once state supports are evaluated, suffix support
arrays cost only parameter-dependent work per state.

At recovery step i, with remaining aggregate t, choose a point of

    Q_i intersect (t - sum_{j>i} Q_j).

Its inequalities have normals from M union (-R), independent of input state
values. Its RHS uses the current state's endpoints and suffix supports. It is
nonempty by the remaining-sum invariant and bounded because Q_i is bounded.
Thus it has a vertex, including when it is lower-dimensional. Enumerate all
nonsingular r-row bases of that fixed normal library, precompute their inverse
matrices, and choose the first resulting candidate satisfying every inequality.
Subtract it and continue; the last suffix is the singleton zero.

Since |M union R| is `2^{O(r^2)}`, the crude complete basis enumeration and
feasibility checks cost `2^{O(r^3)}` per state. This yields exact rational compact
recovery linear in sparse input size at fixed maximum block rank, without an
online LP. It does NOT improve the existing `2^{O(r^2)}` separation bound and
should not be advertised as that same parameter factor. Bit lengths and zero
weights require an explicit check; normalization/refinement then use Stage 1.

The Stage 4 author should investigate and prove this extension if sound. It
closes a stated constructive gap with a simple finite library, even if the
parameter dependence makes it a theoretical option at growing rank. A direct
small-block implementation/check can use the existing support library; do not
claim production speedups without measurements.

## Author development completed; independent reviews pending

The author proved the proposed construction as `thm:rank-recovery` in
`sections/04-bounded-rank.tex`. The proof includes full ambient-rank active
bases at vertices of lower-dimensional intersections, the separate
`2^{O(r^3)}` factor, and denominator growth bounded additively by the
encoding lengths of the successive basis determinants. Zero weights and
compact global-state refinement invoke the accepted earlier conventions.

`verification/stage04-recovery.py` implements the construction using the
existing exact support library and no online LP. It passed 64 exact instances
with 334 state vectors across ranks 1–4, including zero weights, point states,
intermediate dimensions, and 25-state sequences. The K4 inverse library has
nonunimodular bases with determinant magnitudes up to four. Its returned
vectors pass the original state constraints and sum identities exactly.

During this stage the root also proposed a stronger sharpness example with
two explicit simplex variables and five products. The author independently
rederived it, made it the primary K4 example, and retained the prior seven-
product symmetric-reference construction as a remark. The author checked
225 local grid points with exact original-flow witnesses or exact negative
support certificates; the root independently checked a separate 289-point
grid and the full state-flow LP. Both new developments await the prescribed
five independent reviews and are not accepted on these computations alone.
