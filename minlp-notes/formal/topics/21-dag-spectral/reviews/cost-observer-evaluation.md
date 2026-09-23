# Independent review: executable primitive-cost observer

Verdict: **PASS for the `BitComplexity.lean` compiler-equality repair.**
This review covers only `primitiveBitCostClosed` and
`@[csimp] primitiveBitCost_closed`; the whole-cover runtime regression is
checked separately.

The original cost observer computed constant finite sums over every digit
position up to the supplied uniform width. A loose width budget could be
numerically enormous even for a small positive-rank input. Evaluating the
observer therefore attempted to construct a list whose length was that
budget, independently of the actual rational computation's size.

The replacement uses the already proved closed formulas for multiplication
and division charges. With `L=2*K+2`, it retains exactly three multiplication
charges and three addition/comparison charges. Normalization still uses the
actual raw numerator and denominator, their actual maximum digit count, and
the actual `countedEuclid` iteration count plus two final divisions. It does
not substitute a worst-case normalization budget, omit work, or change any
constant.

`primitiveBitCost_closed` proves equality of the entire original and new
functions by the existing cost identities. Its compiler simplification
attribute changes evaluation using this kernel-checked equality. No operand
bit-bound premise is required, so the identity also covers `K=0`, signed
inputs, zero operands, and totalized division/inversion at zero. The
mathematical definition of `traceBitWork` and its bound remain unchanged.
There is no unsafe override, admitted equation, or new axiom.

Targeted verification:

- `lake build --wfail Formal.DAGSpectral.BitComplexity` passed.
- `topics/21-dag-spectral/verification/CostObserverReview.lean`, run with
  `lake env lean -DwarningAsError=true`, passed 84 comparisons against an
  independently written original finite-sum observer: all seven operations,
  four signed/zero operand pairs, and widths 0, 1, and 5. That comparison
  explicitly calls the original multiplication/division loop definitions,
  so it is not merely the same compiler replacement on both sides.
- The client successfully evaluated actual `traceBitWork` at `K=2^100` on
  three events, including division and inversion at zero, and matched the
  closed-form sum. This directly checks that the compiler rule applies to
  the observer and avoids the former width-sized allocation.
- Axiom inspection of `primitiveBitCost_closed` and `traceBitWork_le`
  returned only `propext`, `Classical.choice`, and `Quot.sound`. No
  project-wide or CI checks were run.

Reviewed SHA-256:
`253cf753fa06b688986c966052ed11c57d35d2c69dd65c36cd1c493275084f5c`.
