# Independent review: rational pseudoinverse and contrast execution

Reviewed [RationalPseudoinverse](../../../Formal/DAGSpectral/RationalPseudoinverse.lean),
[RationalPseudoinverseTrace](../../../Formal/DAGSpectral/RationalPseudoinverseTrace.lean),
and [RationalContrastTrace](../../../Formal/DAGSpectral/RationalContrastTrace.lean).
The reviewer did not implement these modules. Mathematical correctness and the repaired execution coupling passed.

The reciprocal polynomial first removes exactly the zero-root multiplicity of
the characteristic polynomial. Its constant coefficient is nonzero because
the characteristic polynomial is monic, including dimension zero. On each
nonzero eigenvalue its value is the reciprocal. The final formula is `A R R`,
so the value on a zero eigenvalue is zero even if `R` has a nonzero constant
term. Spectral evaluation therefore proves equality to the actual
Moore–Penrose inverse, rather than to a totalized ordinary inverse. The proof
requires symmetry, not positive definiteness. Singular and zero matrices need
no numerical pivot bound.

`zeroRootIndex` is the least nonzero coefficient among the first `n+1`
coefficients and equals the actual trailing degree. Its nonemptiness follows
from the leading coefficient. The finite matrix-power sum evaluates the same
reciprocal polynomial; excess coefficient indices are exactly zero.
`rationalEstimable` checks `A A⁺ c = c`, with a proved equivalence to membership
in the actual real range. `rationalContrastVariance` casts to the spectral
quadratic form. This real value alone is not a finite cost for a non-estimable
contrast; the Boolean test must be used when selecting extended costs.

The expression and event bounds account for repeated coefficient evaluation
inside the deliberately unshared matrix expressions. Operation budgets depend
only on the fixed dimension. The arithmetic-width recurrence is linear in the
input bit bound at fixed dimension, so the listed trace work is polynomial in
that bound. Signed entries, exact zero tests, small nonzero coefficients and
zero contrast are included. These are arithmetic-event bounds, not a claim
that dimensions have polynomial dependence.

The initial review identified a separation between computed values and their
traces. The author repaired it, and the follow-up review checked the actual
data flow. `coefficientIndexRun` evaluates the coefficient list once, executes
the ordered zero comparisons, and selects the first nonzero coefficient from
the returned Boolean flags. The returned index feeds the reciprocal matrix
expression. `matrixArithmeticRun` stores scalar `ArithmeticExpr.run` results
in vectors; the returned matrix and event list read the same stored pairs.
`vectorRun` does the same for matrix-vector products. The returned matrix,
first product and second product feed the variance and `vectorEqualityRun`.
The latter compares the actual returned coordinates. The `*_eq` theorems prove
that these executed stages have the previous semantic values and exactly the
same event lists, so the existing event-length and operand bounds apply. This
closes the reported execution-coupling finding.

The trace work counts rational primitive operations. Fixed-dimensional loop
control and expression construction remain finite overhead; this local review
does not identify the trace bound with the total cover producer's Turing cost.

Targeted checks run from `formal/`, with `~/.elan/bin` on `PATH`:

```text
LEAN_NUM_THREADS=1 lake build --wfail Formal.DAGSpectral.RationalPseudoinverse Formal.DAGSpectral.RationalPseudoinverseTrace Formal.DAGSpectral.RationalContrastTrace
LEAN_NUM_THREADS=1 lake env lean topics/21-dag-spectral/verification/RationalPseudoinverseReview.lean
```

Both commands passed. The preserved audit samples ten correctness
and trace declarations; all report only `propext`, `Classical.choice`, and
`Quot.sound`. No project-wide verification or CI inspection was run.

The repaired execution modules were rechecked with `lake build --wfail
Formal.DAGSpectral.RationalPseudoinverseTrace
Formal.DAGSpectral.RationalContrastTrace` as part of the targeted selector
build recorded in [criterion-selectors.md](criterion-selectors.md). The build
and expanded ten-declaration axiom audit passed.
