# Reference sign compiler: targeted verification

Date: 2026-09-28.

This record concerns the construction in
[adaptive integer sign-circuit compilation](adaptive-integer-sign-circuit-compilation.md).
It supplies an executable reference DAG compiler and finite checks. It does
not establish the universal theorem, novelty, an efficient PosSLP evaluator,
or a solver speedup.

## Construction implemented

[sign_compiler_reference.py](sign_compiler_reference.py) accepts a DAG with
constants 0 and 1, Boolean input nodes, binary addition, subtraction and
multiplication, and unary strict threshold `H(v) = int(v > 0)`. Its source
output must be Boolean on Boolean inputs; this promise is the caller's
responsibility. The checks verify the promise for their finite fixtures.

The default compilation schedule is exactly the note's schedule:

- Let `S = max(1, source_gate_count)`, counting arithmetic and threshold gates.
- Construct `M_0 = 2` and `M_j = M_(j-1) * M_(j-1)` as shared target nodes.
- Replace each threshold by the shift `4v - 2`, the compressors with indices
  `S+2, S+1, ..., 1`, `2S+5` refinements, and the conversion `(1+z)/2`.
- Represent each rational by two integer nodes `(P,Q)` using the positive
  denominator formulas in the note. Produce the integer output `2P-Q`.

Every repeated node is shared by identifier. The target contains only
constant/input leaves and binary arithmetic gates. Construction never
evaluates `M_j`, the global magnitude bound, or the error tolerance as a
Python integer. Exact evaluation is a separate operation, guarded by a
500,000-bit limit on each integer; products that must exceed the limit are
rejected before multiplication.

Here `S` excludes constant and input leaves. All decoder, selector and
ordinary Boolean-control gates count toward `S`. With `A` arithmetic source
gates, `H` threshold source gates, `J` compressor steps, and `R` refinement
steps, the template gate bound is

\[
J+1+4A+H(7J+5R+5)+2.
\]

Sharing can reduce the actual count. The full schedule therefore satisfies
the deliberately loose bound `17S² + 49S + 5`. These are arithmetic-gate
counts. Because the implementation retains all source leaves, including
unused inputs, total construction size and time also include the length of
the source description. It would be incorrect to bound that overhead by
`S²` when arbitrarily many unused input leaves are allowed. The usual
total-circuit-size convention absorbs this overhead.

## Checks actually run

The targeted command was:

```text
python research-20260928/algebra/check_sign_compiler_reference.py
```

All ten test methods passed. The suite uses exact Python integers and
`Fraction`; it does not use floating-point comparisons.

| Check | What was examined | Precision |
| --- | --- | --- |
| Rational formulas | 112 exact formula comparisons, including negative and zero numerators and nonunit denominators; denominator positivity | Exact local identities on finite samples |
| Strict signs | `H(x)`, `H(0)`, `H(1)`, `H(-1)`, and `H(x-x)` for both Boolean values of `x`; all source-pair denominators positive; final rational error below `1/4` | Full theorem schedule |
| Shared arithmetic | XOR represented by `x+y-(xy+xy)` on all four inputs; repeated subcircuit identifiers and target fanout | Full theorem schedule; no thresholds |
| Arithmetic after a threshold | `1-H(x)` and `H(x)*H(x)` for both Boolean inputs; full error and denominator checks | Full theorem schedule |
| Adaptive choice | An earlier comparison selects the expression passed to a later threshold, on all four Boolean inputs | Reduced schedule `(J,R)=(1,1)` for exact execution; full schedule checked structurally |
| Variable query instruction | All 16 encodings of one arithmetic instruction with variable opcode and operands, including an invalid opcode | Reduced schedule `(2,2)` for exact execution; full schedule checked structurally |
| Adaptive query description | A first threshold answer selects addition or subtraction in a later query | Reduced schedule `(1,1)` for exact execution; full schedule checked structurally |
| Insufficient precision | An explicit circuit whose reduced compilation gives the wrong answer | Reduced schedule `(1,1)` |
| Construction size | Nested-threshold DAGs with `S=1,2,4,8,16,32,64,128`; backward references, bounded fan-in, target operation set, schedule counts, and gate bound | Full theorem schedule; no integer evaluation |
| Evaluation contracts | Non-Boolean inputs, invalid forward references, and integer-growth budget rejection | Exact targeted rejection checks |

At `S=128`, the full construction has 284,293 arithmetic gates. This is a
structural check: evaluating its expanded integers is deliberately avoided.

The tiny query interpreter reserves registers containing 0 and 1 and one
computed instruction. Two opcode bits select addition, subtraction,
multiplication, or an invalid instruction; the latter returns zero. One-bit
operand addresses select the initial registers. The output slot is fixed.
The implementation includes explicit arithmetic selectors and validity
gating. It does not implement variable-length parsing, multiple instruction
slots, unavailable or future addresses, arbitrary output selection, or the
general polynomial-time machine simulation from the note. These omissions
limit what the interpreter checks establish.

## Why reduced-precision checks are kept separate

The full schedule is expensive to evaluate when rational approximations
feed later thresholds. Even when the represented rational stays small, its
unnormalized numerator and denominator can grow rapidly. Reduced schedules
make a few genuinely adaptive executions small enough to inspect exactly.
Their success is evidence about the implementation on those fixtures only.

The suite demonstrates their limitation using

\[
H\bigl(1-32(1-H(1))\bigr).
\]

The exact answer is one. Under `(J,R)=(1,1)`, the inner approximation is
exactly `9/10`, so the outer approximate input is `-11/5`. Its compiled answer
is zero. Thus reduced-precision testing cannot stand in for the theorem's
global error analysis. The counterexample is expected and passes as a test
of this limitation.

## Review and remaining limits

An independent adversarial reviewer inspected the formulas, schedule,
sharing, interpreter scope and size accounting. The reviewer also performed
separate exact pair checks and construction-size checks, and identified the
input-leaf overhead recorded above. The separate
[review record](sign-compiler-reference-review.md) states the review's scope
and commands.

The targeted checks can detect errors in formulas, operation ordering,
strict-zero semantics, adaptive wiring, shared representation, and schedule
construction. They do not prove the error propagation bound for all circuits,
the universal interpreter claim, or the absence of other implementation
defects. They make no novelty assessment. No Lean proof, project-wide
verification, or CI inspection was performed for this implementation.
