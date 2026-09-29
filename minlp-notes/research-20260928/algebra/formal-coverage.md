# Formal coverage of the integer-sign algebraic core

Date: 2026-09-28. Status: targeted Lean verification passed.

The new
[Lean source](../../formal/topics/32-integer-sign-core/verification/SignCompression.lean)
verifies a substantial local algebraic core of the
[Boolean-closure note](posslp-boolean-closure-audit.md) and
[adaptive-sign note](adaptive-integer-sign-circuit-compilation.md).
It does **not** formally verify circuit compilation, adaptive oracle closure,
or a complexity-class equality. This separate record states precisely the
partial coverage added by the new artifact.

Write
\[
F_M(x)=\frac{2Mx}{M+x^2},\qquad G(x)=\frac{2x}{1+x^2}.
\]
All arithmetic lemmas are statements over the real numbers. The formal
functions use exact field operations, without a floating-point model.

| Mathematical claim | Lean theorem names in `IntegerSignCore` | Scope and assumptions |
|---|---|---|
| Compressor denominator is positive and its positive sign agrees with the input | `denominator_pos`, `compress_pos_iff` | Every real input; \(M>0\). Includes the zero input. |
| Compressor lower and upper magnitude bounds | `compress_abs`, `compress_lower`, `compress_sq_upper`, `compress_range` | From \(1\le\lvert x\rvert\le M\), obtain \(1\le\lvert F_M(x)\rvert\) and \(F_M(x)^2\le M\). The latter is the square-root upper bound in squared form. |
| One square-scale reduction | `compress_square_step` | From \(M\ge1\), \(1\le\lvert x\rvert\le M^2\), obtain \(1\le\lvert F_{M^2}(x)\rvert\le M\). The full dyadic schedule is not defined. |
| Two-step gate normalizer | `normalize_range`, `normalize_pos_iff` | \(F_4(F_{16}(x))\in[-2,-1]\cup[1,2]\) for \(1\le\lvert x\rvert\le16\), with preserved positive sign. |
| AND and OR truth conditions and nonzero margins | `and_gate_ranges`, `or_gate_ranges`, `and_gate_pos_iff`, `or_gate_pos_iff` | Inputs lie in \([-2,-1]\cup[1,2]\). AND lies in \([-11,-1]\cup[1,5]\), OR in \([-5,-1]\cup[1,11]\); positive signs encode the corresponding Boolean operation. |
| Compressor rational-pair update | `pair_denominator_pos`, `pair_compress_identity` | For \(M>0,Q>0\), the pair \((2MPQ,MQ^2+P^2)\) has positive denominator and represents \(F_M(P/Q)\). Both the identity and denominator positivity are checked. |
| Initial refinement range and oddness | `refine_range`, `refine_odd` | \(1\le t\le2\Rightarrow4/5\le G(t)\le1\); oddness covers the negative range. |
| Exact quadratic error identity and bound | `refine_error_identity`, `refine_error_bound`, `refine_signed_error`, `refine_signed_error_bound` | If \(s^2=1\), then \(G(t)-s=-s(t-s)^2/(1+t^2)\) and \(\lvert G(t)-s\rvert\le\lvert t-s\rvert^2\), for every real \(t\). |
| Iterated signed refinement bound | `refine_iter_error` | For every \(r\in\mathbb N\), \(\lvert G^{\circ r}(t)-s\rvert\le\lvert t-s\rvert^{2^r}\) when \(s^2=1\). This checks the induction, including \(r=0\). The notes' selected iteration count and final error budget are not instantiated. |
| Shifted real threshold margins | `positive_threshold_margin`, `nonpositive_threshold_margin` | If \(\lvert w-v\rvert\le1/4\), then \(v\ge1\Rightarrow4w-2\ge1\) and \(v\le0\Rightarrow4w-2\le-1\). The integer dichotomy supplying those hypotheses is not formalized. |
| Multiplication-error propagation | `product_error`, `product_error_linear` | If exact operands have magnitude at most \(B\), input errors are at most \(\delta\ge0\), then product error is at most \(2B\delta+\delta^2\). For \(B\ge1\), \(\delta\le1\), it is at most \(3B\delta\). |

The signed refinement identity slightly strengthens the local statement used
in the notes: the one-step error inequality needs no range assumption on
\(t\). Convergence still requires an initial error below one. The initial
range lemma supplies that condition for the intended application. No new
research contribution is claimed for this algebraic observation.

## What was checked

From `formal/`, the targeted command actually run was:

```sh
lake env lean topics/32-integer-sign-core/verification/SignCompression.lean
```

The final run completed with exit status 0, no warnings, and
`PASS: audited 53 integer-sign core declarations.` There are 26 named
theorems and seven definitions; the audit also covers generated auxiliary
declarations. It allows only the usual Mathlib axioms `propext`,
`Classical.choice`, and `Quot.sound`. No `sorry`-based proof or additional
axiom is accepted by this audit.

This check establishes the universally quantified local statements as
written in Lean, subject to Lean's kernel and the imported formal
foundations. It is stronger than sampling those inequalities, but it does
not independently validate the prose-to-formal correspondence. A separate
adversarial reviewer checked that correspondence, found no incorrect or
vacuous assumptions, and independently reran the targeted command
successfully. The review specifically confirmed the missing schedule,
integer semantics, global error induction, and compiler coverage described
below. The check is not a fresh rebuild or kernel replay of the entire
dependency tree.

Targeted whitespace commands actually run from the repository root were:

```sh
git diff --no-index --check /dev/null formal/topics/32-integer-sign-core/verification/SignCompression.lean
git diff --no-index --check /dev/null formal/topics/32-integer-sign-core/README.md
git diff --no-index --check /dev/null research-20260928/algebra/formal-coverage.md
```

They produced no whitespace diagnostics. Each comparison returned status 1
because the checked file is new relative to `/dev/null`.
After the documentation update, an inline Python check counted the 26 named
theorems and seven definitions and checked trailing whitespace in these same
three files. It exited with status 0 and printed
`PASS: final three-file trailing-whitespace check`.

## What remains unchecked

The artifact has no arithmetic-circuit syntax, threshold-circuit semantics,
integer-pair compiler, sharing model, or bit-complexity model. In particular,
it does not verify:

- the full compressor schedule, gate-height bound, or shared construction of
  the doubly exponential constants;
- Boolean-circuit evaluation induction, negation/constants, or every pair
  update for arithmetic and Boolean gates;
- the chosen global error-budget inequality, the topological circuit-error
  induction, or the final output-threshold test;
- integer separation, a uniform variable-description SLP interpreter,
  malformed-input handling, or an adaptive oracle-machine simulation;
- the size bounds \(O(n+kN+s)\), \(O(S^2)\), polynomial-time uniformity, or
  either claimed PosSLP closure theorem as a complete formal result.

The source is a standalone topic check, not an import of the project's
canonical `Formal` library. No project-wide verification or CI inspection
was performed. Formal verification adds no evidence of originality,
completeness of the literature search, numerical stability in finite
precision, practical solver speed, or application value.
