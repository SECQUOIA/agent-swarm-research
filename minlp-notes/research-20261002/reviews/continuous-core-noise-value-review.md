# Independent review of the lazy continuous-noise value oracle

Date: 2026-10-02. Status: fresh actual-file review passed. No mathematical
correction is requested.

The reviewed file is
[continuous-core-noise-value-oracle.md](../new-direction/continuous-core-noise-value-oracle.md).
This review covers the complete statement and Sections 1–6, including
the common bound for all precisions and the degenerate cases. The
referenced tangent-certificate argument in
[smoothed-polynomial-box-recourse.md](../new-direction/smoothed-polynomial-box-recourse.md#2-convex-recourse-needs-no-strong-convexity-modulus)
was also checked. The author's separate exact prefix/certificate
diagnostic is not claimed as a test performed by this reviewer.

## Persistent coefficients and finite certificates

The independent infinite fair bitstreams define one product-uniform
coefficient vector. A length-`b` prefix gives the closed interval of
width `2 sigma 2^(-b)` in equation (5). Closed endpoints cover all-zero
and all-one streams, as well as both expansions of a dyadic number.
Every stream therefore defines a valid objective, including the
measure-zero exceptional streams.

At level `j`, equation (7) makes the total coefficient interval width
on the unit core at most `e_j/2`. The residual certificate has width at
most `e_j/2`. Their sum gives equation (10), uniformly over every
completion of the used prefixes. Nonnegative unit-box core coordinates
justify using the lower coefficient endpoints in the lower bound and
the upper endpoints in the upper bound.

The residual solve concerns the fixed rational polynomial
`F_0(v,·)`. The returned feasible residual point is rational, and its
base objective value is evaluated exactly. Its upper bound after adding
noise is a certified rational bound, not an exact value of the generally
irrational sampled objective. The cited convex interface supplies a
checkable tangent lower bound without a strong-convexity assumption.

The representation is explicitly relative to a persistent random tape.
It is not a finite rational or algebraic encoding of the sampled
coefficients. This distinction is stated correctly in the theorem.

## Pruning and the global value interval

Independent coordinate rounding in a cell can be applied with a
residual optimizer held fixed. The diagonal upper curvature bound gives
the correction `e_j`, and the linear perturbation adds no curvature.
Hence `min_corner ell_v-e_j` is a valid lower bound on the whole cell
for each compatible coefficient vector.

The same rational incumbent is an upper bound for every compatible
vector. Pruning with the final incumbent therefore preserves every
optimizer for every completion of the current prefixes. The second
pass in Section 3 ensures that retained cells are tested against this
final incumbent.

The global interval `[U-2e_j,U]` is sound. Every current corner satisfies

```text
ell_v >= u_v-e_j >= U-e_j,
```

so every current cell lower bound is at least `U-2e_j`. A cell discarded
earlier had a lower bound greater than its then-current incumbent. That
incumbent is at least the present `U`, and its coefficient prefix
contains all current completions. Current cells together with previously
discarded regions cover the original core box. This proves the stated
global lower bound uniformly over the whole current coefficient box.

For a retained cell, choose a corner attaining its smallest lower bound.
Its true conditional value, and its returned feasible point's true
objective, are at most `U+2e_j<=f*+4e_j`. Thus the witness used by the
counting proof is a true near-optimal witness for the fixed limiting
objective.

All current corners are queried at the current tolerance. Only older
upper incumbents are retained without refinement. Loose historical lower
bounds are not used to claim a new narrow value interval.

## Counting without conditioning on adaptive history

At a fixed deterministic grid node, comparison with its two coordinate
neighbors confines each interior coordinate's true noise coefficient
to equation (14). Holding an exact residual minimizer at that node
fixed proves the required second-difference inequality for `V_0`,
even if the residual minimizer is nonunique.

The interval length is `(1+k)L h_j`. Its endpoints depend only on
`V_0` and the fixed grid node. Independence of the original continuous
coefficients therefore gives equation (16). The proof does not
condition on revealed prefixes, retained lists, or choices made by
the approximate residual solver.

Each witness belongs to at most `2^k` cells; each retained cell has at
most `2^k` children; each generated cell has `2^k` corners. These give
the stated retained, generated, and query factors. Repeated corner
queries are harmless and keep the implementation linear in the generated
list size, with the corner factor explicitly charged. No unspecified
polynomial in list size is used.

## Bit work and the common all-precision bound

For positive `L` and `k`, the prescribed prefix length is `O(I+j)` and
the stopping level is `J=O(I+q)`. Core corners, substituted polynomial
coefficients, residual tolerances, tangent certificates, and final
rational bounds all have polynomial bit length in `I+j`. Their bit
complexity exponent does not depend on `k`.

The prescribed prefixes and deterministic oracle/list rules define one
canonical infinite refinement. With its generated counts `N_j`, Tonelli
gives

```text
E[sum_(j>=0) N_j/(j+1)^2] <= 2(1+4^k H).
```

Thus `R` in equation (17) is finite almost surely. Equation (18)
correctly keeps the additional `2^k` corner-work factor and proves a
single finite-expected random overhead for all precisions. Neither the
algorithm nor its certificates need to compute `R`.

Every stream still has finitely many cells through any finite stopping
level, including streams with infinite `R`. Correctness and termination
therefore hold for every stream; the polynomial work bound is an
expectation claim. The stage for a requested precision supplies the
claimed polynomial-length point and interval. The evaluator may rerun
that canonical prefix or retain its stage records for later queries.

## Degenerate cases and output scope

For `k=0`, ordinary convex value evaluation proves the output contract
without coefficient bits. For `L=0` and positive `k`, sequential
coordinate endpoint rounding gives an optimum among the core vertices.
Certified intervals of width at most `2^(-q)` at those vertices give a
global interval of that width: take the least lower endpoint and the
least upper endpoint, keeping the feasible point for the latter.
The stated `2^k poly_d(I+q)` deterministic work is valid. If the residual
dimension is zero, all residual evaluations are direct rational
calculations.

The final output guarantees value accuracy and a feasible rational point
with a certified objective upper bound. It does not promise distance to
an optimizer or selection of a common optimizer across precisions. No
growth, uniqueness, finite stationary-set, or strong residual convexity
assumption is hidden in the proof.

## Verification performed for this review

This was an analytical actual-file review, supplemented by a separate
independent derivation and a second actual-file check of the common
work factor, prefix-family certificate, and degenerate cases. No numerical
solver or duplicate prefix diagnostic was run. A targeted document check
verified this review's local links, code fences, trailing whitespace,
and final newline. No external search, main-file edit, index edit,
project-wide verification, or CI inspection was performed.

The author's separate
[diagnostic](../new-direction/check_continuous_core_value.py) has a saved
[passing report](../new-direction/continuous-core-value-results.json).
This reviewer read that report but did not rerun the script. It records
33 levels, 417 generated cells, 63 prefix enclosures, 16,716 corner
completion checks, 2,466 cell lower-bound checks, 1,390 retained-witness
checks, 510 true-noise strip checks, and 144 global prefix-certificate
checks. These exact finite fixtures supplement the proof; they are not
a stochastic work estimate or an implementation of the general convex
value oracle.
