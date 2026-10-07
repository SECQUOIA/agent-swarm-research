# Independent review of the constant-base core-solver transfer

Date: 2026-10-02. Result: passed the scoped algorithmic replacement in
[native integer recourse](../new-direction/smoothed-native-integer-recourse.md)
and [interior core-flow recourse](../new-direction/smoothed-interior-core-flow.md).
Read both complete actual files before and after the transfer. No
mathematical correction was needed.

This review checks the use of the reviewed
[deterministic polynomial box solver](../new-direction/polynomial-component-primitive-limit.md)
for completion, sign decisions, output and fallback comparisons. It does
not replace the separate reviews of the unchanged recourse oracle,
growth-tail theorem or algebraic tube theorem, or claim a new full review
of the interior-flow theorem.

## 1. Native recourse completion and output

The competing-label certificate is unchanged. When it passes, its label
is feasible independently of the core and attains the global optimum at
an original optimal core point. Therefore minimizing its fixed-label
polynomial over the entire closed unit core box is sufficient. No
convexity, uniqueness or stationary-set regularity is needed.

After substituting that native integer label, degree stays fixed and
coefficient bit length is polynomial in `I+log M`. The deterministic box
solver consequently applies with `c_d^k poly_d(I+log M+t)` work. Choosing
the first minimizer in a fixed candidate order gives a deterministic
answer; it does not require the globally lexicographically least
optimizer. The revised theorem makes no such promise.

All coordinates are maps `r_i(alpha)` of the same isolated real root.
For a separate coordinate representation, clear denominators in
`r_i=H_i/q_i` and form

\[
 \operatorname{Res}_T\bigl(P(T),q_i X-H_i(T)\bigr).
\]

This polynomial is nonzero and has degree at most `deg P` in `X`.
Root isolation and matching from the selected `alpha` identify the
correct coordinate, including a rational or repeated value. The same
construction applies to the objective polynomial. With the solver's
conservative fixed base, these optional operations preserve the claimed
constant-base degree, height, output-size and refinement bounds. They
do not select independent coordinate roots and therefore cannot mix
different optimizers.

Clipping rational core approximations to the unit box preserves
feasibility while the exact integer label remains fixed. Its independent
feasibility is essential. Gradient bounds and exact-value refinement
give the stated certified objective gaps without comparing values from
other labels.

## 2. The fallback budget remains valid

The fallback still checks every bounded native label for residual
feasibility and minimizes each feasible fixed-label core polynomial.
A running minimum requires one comparison for each new candidate.
Two univariate value representations can be compared by gcd or
squarefree-product isolation, including ties. There is no quadratic
number of label comparisons or compositum of all examined values.

The component solver's mixed-label bound covers these comparisons after
fixing its base conservatively. Thus an effective budget of the form
`B = R_Z` times a parameter-only factor containing `c_d^k` still has
`log B=poly_d(I)`, and the polynomial exponent in new coefficient bits
stays independent of `k`. Renaming that exponent `e_d` correctly
distinguishes it from the exponential base `c_d`.

Only the winning label and its own common-root witness are returned.
Its defining polynomials depend on the small core and input heights,
not the number of labels examined. Its roots can be isolated afresh in
their own polynomials if temporary comparisons used finer intervals.
Therefore the all-draw output and refinement bounds do not inherit the
fallback enumeration count.

The rare-event budget remains noncircular: choose `B` from the base
instance, then choose `rho`, the growth cutoff, the level cutoff and the
noise-grid size. The fallback's remaining dependence on `log M` is
polynomial. Replacing the completion algorithm does not require a
different growth event, resampling or an additional failure probability.

## 3. Interior reduced-cost tests use ordinary box minima

Each reduced-cost polynomial is of fixed degree and has polynomial
coefficient bit length after its integer flow and tree have been chosen.
Its retained hull is a rational closed box. Substituting fixed hull
coordinates first leaves a box problem of dimension at most `k`.
Minimizing that polynomial exactly and comparing its one algebraic
minimum value with zero decides the non-strict sign condition. A
zero minimum passes, so persistent flow ties remain permitted.

These tests use one univariate value at a time. They do not require
exact comparison of unrelated algebraic sums. A proof record can replay
the exact box calculation to establish the minimum, rather than treating
one feasible minimizing candidate as a certificate by itself.

There is one collection of at most `2r+s` tests per level. Its work is
`c_d^k poly_d(I+j)`, independent of the number of retained cells at that
level. Summing through a cutoff with `J=poly_d(I)` gives an additive
`c_d^k poly_d(I)` term. The one-time whole-core completion and the output
use the same interface as native recourse. No lexicographic selection is
required here either.

## 4. The elimination bound is still analysis-only

The revised interior note correctly retains

\[
 E_d(k)=(k+1)^{O_d(k^2)}
\]

for the multivariate image formula with `k` quantified and `k` free
variables. A fast box optimizer does not imply a smaller formula for
that image. The cross-label degree bound still contains `E_d(k)^3`,
and the algorithm only computes its numerical format bound in binary.
It does not construct the image polynomial or enumerate the chart
collection on each draw.

Because `log E_d(k)` is polynomial in `k`, retaining this quantity is
consistent with polynomial base bit length for the image degree, tube
constant, cutoff level and sampling precision. It introduces no
additional elimination term in the online expected work. The distinction
between the computational constant `c_d` and analysis quantity `E_d(k)`
is explicit in the revised theorem.

The search correction, competing-label stopping inequalities, growth
tail, chart-image construction, tube estimate and same-draw cutoff
formulas retain their previous roles. This transfer changes the exact
small-core operations and their budget, not those probability arguments.

## Verification scope

Ran a targeted inline Python check of the two revised notes and this
review for local link targets, paired code fences and display delimiters,
trailing whitespace, removal of the old algorithmic `A_d(k)` notation,
and retention of the interior `E_d(k)` bound. It passed. No new solver
implementation or diagnostic was added, and no core dynamics tests were
rerun. No further delegation, external search, project-wide verification
or CI inspection was performed.
