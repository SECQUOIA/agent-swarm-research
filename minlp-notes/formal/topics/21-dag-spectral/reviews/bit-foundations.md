# Independent review: rational bit bounds and arithmetic traces

Verdict: **PASS for the stated operand bounds, local arithmetic traces, and
root-separation bounds.** No false numerical bound or missing positivity
premise was found. These files do not by themselves establish the complete
producer's Turing running time. The execution and integration limits below
must remain explicit in the final C05 claim.

Reviewed modules in `formal/Formal/DAGSpectral/` are `BitComplexity`,
`DyadicScale`, `DyadicScaleBits`, `FactorBits`, `RationalMatrixArithmetic`,
`MatrixArithmeticTrace`, `NormalizationBits`, `CharpolyBits`,
`EigenCompareSeparation`, and `EigenCompareBits`. I also inspected the reused
rational size and schoolbook cost definitions in
`Formal/ReciprocalAnchor/ManyRationalSize.lean` and `ManyBitCost.lean` to check
the meaning of their bounds. No proof sources were changed.

## Rational size and primitive cost

`RationalBits q B` bounds the actual reduced numerator magnitude and positive
denominator by `2^B`, equivalently their binary digit counts by `B`. Negative
numerators are measured by their absolute values. The reused addition,
subtraction, multiplication, inversion, and division lemmas follow the raw
fraction formulas and prove that reduction cannot increase either component.
Inversion explicitly handles zero; the division theorem consequently uses
Lean's totalized division, including a zero divisor, without a hidden
nonzero premise. Actual PSD elimination only divides by positive nonzero
pivots on its division branches.

The reused `primitiveBitCost` charges signed cross-products, scans, and gcd
normalization using the actual raw numerator and denominator. Their sizes
are bounded before normalization, so a reduced-output size bound is not
being substituted for an intermediate-operand bound. The resulting common
bound is `256*(K+1)^3` for `K`-bit operands. It is a specified schoolbook
arithmetic model, not a measurement or theorem about Lean's compiled `Rat`
backend.

`traceBitWork_le` applies that bound to every event's actual operand pair.
`primitiveResult_bits` also bounds the result for every listed primitive,
including negative values, zero, division, and Boolean-valued comparisons.
`arithmeticWidth d B = 2^d*(B+2)-2` has the proved recurrence
`K -> 2K+2`. Its use is legitimate at fixed arithmetic depth; using it with
an input-dependent path length would not prove polynomial bit growth.

## Dyadic search

`dyadicScale` is a bounded rational computation: it starts at `2^(-B)` and
allows `2B` doublings. A positive rational with `B`-bit components satisfies
`2^(-B)<w<2^B`. These bounds establish the initial upper window and eventual
reachability of one. `dyadicSearch_spec` proves positivity and the exact
window `1<=tau^2*w<4`, including the endpoint where the scan first reaches
one. `dyadicScale_power` proves that the output is a power of two with
integer exponent between `-B` and `B`.

The trace includes construction of the initial power by successive
doubling, its inversion, the two multiplications and comparison per scan
step, and the extra doubling on a continuing branch. Its fuel and branch
condition agree with `dyadicSearch`. The stated bounds are at most `9B+1`
events, operand budget `13B+4`, and output budget `6B+1`. The last two need
no positivity premise, while the scale-window theorem correctly requires
`w>0`. The bounds remain valid when the fuel is zero; no invalid window
claim is made for a zero-bit encoding of a positive rational.

## Elimination and matrix arithmetic

`FactorBits` follows the actual `rationalLDL` recursion. Each Schur entry
uses a multiplication, division, and subtraction, taking its entry budget
from `B` to `4B+1`. Induction bounds every produced weight, column entry,
and traced operand by `4^n*(B+1)`. The trace includes the pivot test,
divisions for the emitted column, all Schur entries, and the recursive
trace. `rationalLDLWithTrace_eq` proves that the instrumented version returns
the original factors and the stated trace. Zero-pivot branches copy a
principal submatrix and do not incur imaginary Schur divisions.

The event kind `compare` records the cost of a signed rational comparison;
the LDL branch itself tests equality to zero. This is a valid use of the
same raw cross-difference cost. It should not be described as a theorem
that replaying the Boolean `primitiveResult .compare` reconstructs every
LDL branch on arbitrary non-PSD input: that Boolean specifically tests
`<=`. On the intended PSD input and recursive PSD residuals, a pivot is
nonnegative, so the equality and `<=0` tests also agree.

`RationalMatrixArithmetic` proves size bounds for actual matrix products,
Leibniz determinants, adjugates, and the explicit inverse. Small nonzero
determinants and ill-conditioned bases do not invalidate them: inversion
exchanges numerator and denominator budgets. A singular inverse is the
totalized zero-determinant formula, not silently assumed invertible.

`MatrixArithmeticTrace` provides stronger execution evidence than an
operation count alone. `ArithmeticExpr.run` evaluates its children and
records their actual returned operands; `run_eq` identifies its result
and trace with the specifications. The determinant, inverse-entry, and
matrix-product expressions are proved equal to the corresponding actual
matrix entries. Their operation counts are derived from the expressions.
The inverse-entry expression deliberately recomputes its determinant for
each entry, and this recomputation is counted. Permutation order is
deterministic; the finite permutation-list length is `n!`.

All leaves and intermediate event operands are bounded. In particular, the
inverse trace bound includes both determinant computations and the
inversion/multiplication, rather than bounding only the final inverse.

## Normalization assembly and its precise cost meaning

`NormalizationBits` bounds the actual Gram matrix, inverse, left inverse,
projector, scales, normalizer, reconstructor, and transformed atom. The
weight-size function is the actual maximum numerator/denominator digit
count; its specification and domination by an input budget are proved.
The dyadic traces use these actual sizes rather than a supplied scale
certificate.

`normalizationTrace` lists a coherent eager evaluation order: compute the
Gram matrix and its inverse, then the left inverse, projector, normalizer,
inverse scales, reconstructor, and the two products for the transformed
atom. Every derived matrix used as an input is obtained from preceding
stages. The individual scalar expression results are proved equal to those
matrix formulas. No missing arithmetic stage was found in this schedule.

The common operand budget bounds inputs to each matrix stage. A
dimension-dependent arithmetic-width bound then covers all internal scalar
operations. The affine budget scaling lemmas yield the explicit degree-four
bound `normalizationCostCoefficient p r * (B+1)^4` for the combined dyadic
and normalization arithmetic trace. Its coefficients can grow rapidly
with `p` and `r`; this proves a polynomial in input bits at fixed dimension,
not a polynomial uniformly in dimension or a dimension-independent FPT
claim. The LDL budget has the same fixed-dimension interpretation.

The formal object here is an eager arithmetic schedule, not a global
interpreter that materializes and caches all intermediate finite matrices.
Function-valued matrix expressions can be recomputed by Lean's evaluator;
no bound for that implementation is asserted. A final algorithmic cost
claim must connect an eager finite representation to the overall producer
and account for reading/copying entries, constructing expressions, computing
digit counts, enumerating/sorting indices, and control and storage work.
Those obligations are not discharged solely by the arithmetic trace length.

## Characteristic coefficients and root separation

`rationalCharpolyCoeff` computes the actual coefficient as a signed sum of
principal minors, with zero returned above the matrix dimension. Its
equality with the characteristic polynomial is proved. The coefficient
budget `1+2^n*(determinantBits n B+1)` includes singular matrices, repeated
eigenvalues, zero coefficients, and the zero-dimensional characteristic
polynomial. It is linear in `B` at fixed dimension.

The root-separation proof uses the first nonzero coefficient, not the
constant coefficient. For `0<|alpha|<=1`, it cancels the power at the
trailing degree and bounds the remaining terms by coefficient height times
`|alpha|`. Integer nonzero coefficients have magnitude at least one;
rational coefficients use the product of their denominators. The case
`|alpha|>1` is handled separately. Thus zero constant coefficients and
repeated roots do not create a missing case. The root theorem correctly
requires a nonzero polynomial and a nonzero root; it makes no separation
claim for equal eigenvalues by pretending their zero difference is nonzero.

`separationFromCoefficients` is executable and agrees with the polynomial
formula when the list includes every coefficient. Zero padding contributes
denominator one and height zero. Its positivity holds even for an empty
list; using it as a root bound still requires the polynomial premises.

`EigenCompareBits` proves denominator-product, coefficient-height, and gap
budgets for actual rational values. The gap budget is at most
`(2d+4)*(B+1)`. The numerator digit count of `4R/gap` is bounded by the sum
of the radius and gap budgets plus three. This provides an actual
fixed-degree bisection-depth bound, not a complete comparator bit-work
theorem. Execution costs of coefficient construction, threshold tests,
midpoint updates, and their repeated use remain to be connected in the
comparator's own cost proof.

## Targeted checks

The following targeted build passed from `formal`, with
`PATH="$HOME/.elan/bin:$PATH" LEAN_NUM_THREADS=1`:

```
lake build --wfail Formal.DAGSpectral.BitComplexity Formal.DAGSpectral.DyadicScale Formal.DAGSpectral.DyadicScaleBits Formal.DAGSpectral.FactorBits Formal.DAGSpectral.RationalMatrixArithmetic Formal.DAGSpectral.MatrixArithmeticTrace Formal.DAGSpectral.NormalizationBits Formal.DAGSpectral.CharpolyBits Formal.DAGSpectral.EigenCompareSeparation Formal.DAGSpectral.EigenCompareBits
lake env lean -DwarningAsError=true topics/21-dag-spectral/verification/BitFoundationReview.lean
```

The client imports all reviewed branches together. It also checks native
execution of scales for weights `1/64`, `64`, and `1`; the full signed
Schur trace for `[[1,-2],[-2,4]]`; a zero-pivot trace; expression evaluation
with a negative operand and zero divisor; empty and singular determinants;
the totalized singular inverse; characteristic coefficients with zero and
repeated eigenvalues; and a separation formula with a zero constant and
extra zero padding. These native checks are regression tests, not
production proof axioms. The final client passed with warnings treated as
errors. Its first draft needed `RationalBits` unfolded for the zero-division
native check; no reviewed source was changed.

Selected production axiom checks covered the instrumented LDL equality and
cost, expression runner and operand bounds, determinant/inverse expression
correctness, normalization polynomial bound, characteristic coefficient
correctness and size, nonzero-root separation, and coefficient-list
bisection size. All reported only `propext`, `Classical.choice`, and
`Quot.sound`. This is not the separate final declaration audit. No
project-wide check or CI inspection was run.

There are matching declarations named `DAGSpectral.rationalBits_finset_prod`
in `RationalMatrixArithmetic` and `EigenCompareBits`. The combined-import
client passed, so this is not a current compilation or mathematical
failure. It is duplicated ownership of the same bound and was reported to
the integrator.

Reviewed SHA-256 digests:

```
0b5467bde516c53f252712ca2a0e8fdf4ffb58dcf67d845b8458a5adbdadef6a  BitComplexity.lean
782f3ec04e64e88b31be024f1e762e24649a6942d12c59ec4336a5db3028b029  DyadicScale.lean
0c7e6bffccc40436e79154499c28ba4cf621823c3c22b7becd0896cef9e06457  DyadicScaleBits.lean
01be102148f58a62fa58b5876de265fd2baff911195288179572fa005ba7eaec  FactorBits.lean
3a335a68ccd2d20075c0769daa07d518d6a5b6fd0568dd810d157ea0f19fb6da  RationalMatrixArithmetic.lean
7abe3c9998c5443f639a623706cbf61c2c9f22cb50b43c4e7505df210b2230be  MatrixArithmeticTrace.lean
272d81a6e64b9c360b0ceb1cb11976c8e4cd073a4b8dddd36d3ca43bae7c5b20  NormalizationBits.lean
826dccc8e842d00cfc0988f0d6a6f37056e3103fe123446db40e0983c65a5840  CharpolyBits.lean
3eee51a9a118525b73c75700895ed9fc959b84ec61fd0c9a99acdc8a9c51ec21  EigenCompareSeparation.lean
3d33cc056e27e5d9499919240284915840e3f20ce50e56b528f1b7f7c0298481  EigenCompareBits.lean
```
