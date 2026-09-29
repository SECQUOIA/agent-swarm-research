# Independent review of the reference sign compiler

Date: 2026-09-28.

The reviewer inspected [the implementation](sign_compiler_reference.py),
[its targeted tests](check_sign_compiler_reference.py),
[its verification record](sign-compiler-reference-verification.md), and the
[mathematical construction](adaptive-integer-sign-circuit-compilation.md).
No mathematical or implementation defect was found in the inspected
construction. This is evidence from manual inspection and finite tests,
not a formal proof of compiler correctness or an assessment of novelty.

## Formula and construction review

The arithmetic pair formulas implement the indicated rational operations.
The compressor and refinement denominators are positive whenever the incoming
denominator and compressor scale are positive. Negative and zero numerators
require no exceptional case. The strict threshold shift is `4*v - 2`; the
final integer is `2*P - Q`. These conventions correctly distinguish zero from
a positive integer.

The scale list starts at the node for 2, constructs later scales by shared
squaring gates, and applies indices `S+2` down to 1. It does not materialize
the large scale integers during compilation. The default refinement count
is `2*S+5`, with `S` replaced by 1 when there are no source gates.
The arithmetic templates reference earlier node identifiers rather than
copying expression trees. Hash-consing also shares the initial squaring gate
with the node for 4.

For compressor index `j`, refinement count `r`, `A` arithmetic source gates,
and `H` threshold source gates, the recorded bound is

\[
 j+1+4A+H(7j+5r+5)+2.
\]

Each term agrees with the implementation. In particular, one compressor
uses at most seven arithmetic gates and one refinement uses at most five.
Sharing may lower the count.

One size convention needs care. The implementation's `source_size` counts
arithmetic and threshold gates, including the interpreter's decoder and
selector gates. It excludes input leaves. Compilation still scans and
preserves unused input leaves. Therefore its arithmetic-gate count is
`O(S^2)`, while its total node count and construction work also depend on
the source description length. With `I` input leaves, the node bound is
`O(I+S^2)`; polynomial construction time should be measured against the
complete source description. This does not affect the magnitude or error
bounds, since all input leaves are Boolean.

## Targeted verification

The reviewer independently ran:

```text
python research-20260928/algebra/check_sign_compiler_reference.py
```

All ten tests present on the final run passed. They check exact
rational identities, strict zero boundaries, production precision on small
circuits, arithmetic after a threshold, source and target sharing, bounded
evaluation, a complete small query encoding, adaptive dependence, and
structural growth. An explicit
counterexample correctly shows that the reduced precision used in larger
execution experiments has no general correctness guarantee.

Independent inline Python checks also passed:

- 1,400 exact rational identities and positive-denominator checks, using
  200 samples from `random.Random(6101)`, numerators in `[-10,10]`, and
  denominators and compressor scales in `[1,10]`.
- Production-schedule construction of nested threshold chains with
  `S = 1, 2, 8, 32, 128`. Every reference was backward, every target operation
  was allowed, and operation counts met the template bound. The largest
  target had 284,293 arithmetic gates. These chains were not evaluated.
- Exact production-schedule execution of `1-H(x)`, `H(x)*H(x)`, and
  `H(x)-H(x)` for both Boolean inputs. Each has two source gates. Output
  signs, positive denominators, and output error below `1/4` were checked.

The local tests exercise all pair formulas but do not prove them universally.
The large structural tests establish construction properties for the tested
graphs, not correctness of their unevaluated output signs. In particular,
the adaptive execution examples use an explicitly reduced schedule; they
do not numerically verify the production schedule on those same examples.

## Interpreter scope and remaining limits

The interpreter deliberately covers one instruction with two initialized
constant registers, one-bit addresses, and two-bit opcodes. Exhaustive tests
cover every encoding, including its malformed opcode. A second fixture
allows an earlier threshold answer to determine a later opcode. This tests
real dependence of query control on an earlier answer.

The interpreter does not implement the note's general bounded parsing,
multiple instruction slots, unavailable addresses, or output-slot selection.
Those parts of the reduction remain supported by the mathematical argument,
not this small executable interpreter. The compiler also relies on the
caller's promise that the designated exact source output is Boolean.

The targeted whitespace command
`git diff --no-index --check /dev/null research-20260928/algebra/sign-compiler-reference-review.md`
returned no diagnostics; its exit status 1 records the new-file difference.
No project-wide tests or CI inspection were
performed. This review does not
establish a practical solver speedup, an efficient explicit integer evaluator,
or publication priority for the representation theorem.
