# Integer-sign compilation: local algebraic verification

Date: 2026-09-28. Status: targeted Lean check and axiom audit passed.

This package verifies local algebraic lemmas used in the
[Boolean-closure note](../../../research-20260928/algebra/posslp-boolean-closure-audit.md)
and the
[adaptive-sign note](../../../research-20260928/algebra/adaptive-integer-sign-circuit-compilation.md).
It does not formalize either compiler or either complexity conclusion.

The standalone source is
[verification/SignCompression.lean](verification/SignCompression.lean),
in namespace `IntegerSignCore`. It uses the existing pinned Lean 4.33.1 and
Mathlib installation under `formal/`. No new package or dependency was added.
It is not imported by the canonical `Formal` library or its project-wide
audit. The source ends with its own targeted audit, covering all 53
declarations in the namespace, including generated auxiliary declarations.
Only `propext`, `Classical.choice`, and `Quot.sound` are allowed; dependencies
on `sorryAx` or any other axiom fail the check.

The 26 named theorems cover compressor sign and magnitude, a two-step gate
normalizer, AND/OR ranges and truth conditions, the compressor's rational-pair
identity and denominator positivity, refinement and its iterated signed-error
bound, real threshold margins, and multiplication-error propagation.
The [coverage table](../../../research-20260928/algebra/formal-coverage.md)
states the assumptions and exclusions in detail.

Command actually run from `formal/`:

```sh
lake env lean topics/32-integer-sign-core/verification/SignCompression.lean
```

The final run exited with status 0, without warnings, and printed:

```text
PASS: audited 53 integer-sign core declarations.
```

This runs Lean elaboration and kernel checking of the new proof terms using
the installed dependencies. It is not a fresh replay or rebuild of Mathlib.
An independent reviewer checked the theorem assumptions against the notes,
found no defect, and reran the same targeted command successfully.
No project-wide verification, CI inspection, compiler implementation test, or
runtime benchmark was performed for this package.
