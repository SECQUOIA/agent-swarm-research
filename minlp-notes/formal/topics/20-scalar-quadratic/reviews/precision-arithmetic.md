# Independent review: minima and precision arithmetic

Reviewed `CountMinimum.lean` and `PrecisionArithmetic.lean` on 2026-09-20.
The reviewer did not implement these files. No correctness issue was found.

`IsMinimumCount feasible p` includes both feasibility at `p` and a lower
bound against every other feasible natural count. Existence requires an actual
witness supplied to `exists_minimumCount`; the definition does not silently
assign a finite minimum when no lift exists. Uniqueness follows by comparing
the two attained counts. Each error-monotonicity lemma preserves the original
domain, graph or full one-sided containment, and the same lift and dimensions.
The epigraph and hypograph inequalities have the correct monotonic direction.

`precisionDepth A eps` uses the established natural ceiling at normalized
accuracy `eps/A`. Its sufficiency theorem requires `A>0` and `eps>0`, preventing
invalid division or a logarithmic interpretation at zero. For `eps<=A/4`, the
untruncated logarithmic depth is nonnegative, so natural-ceiling estimates
yield the stated lower bound and strict upper bound. The extra one in the
ceiling cancels the minus one in the normalized square precision formula.
Equality at `eps=A/4` is included.

`HasPrecisionRate feasible r` requires one finite nonnegative constant `C` and
one strictly positive threshold `eps0`. For **every** `0<eps<=eps0`, it supplies
an attained minimum `p` and the absolute additive estimate
`abs(p-(r/2)log2(1/eps))<=C`. Thus it asserts the full uniform bounded-additive
error property, not merely a subsequence estimate, a ratio limit, or a
conditional bound on minima that might not exist.

`precisionRate_of_bounds` is correctly an arithmetic assembly lemma with
explicit lower and upper hypotheses. The upper hypothesis supplies actual
feasibility at `r*precisionDepth A eps` and hence supplies existence of a
minimum for every positive accuracy. The lower hypothesis applies to all
feasible counts for every sufficiently small positive accuracy. The proof
uses threshold `A/4` and the fixed nonnegative constant
`abs(c)+abs((r/2)log2 A)`. Both sides of the absolute estimate follow from the
assumed lower bound and the depth upper estimate. The argument also handles
`r=0`; it does not require dividing by rank.

This review certifies these reusable arithmetic and minimum interfaces. It
does **not** discharge R6, I7 or I8 by itself: final quadratic graph,
epigraph and hypograph rate theorems must prove their geometric lower bounds
and actual formulation upper bounds before applying this lemma. In
particular, supplying an arbitrary feasibility predicate or leaving the
`lower`/`upper` hypotheses undischarged is not a source-level rate theorem.

Targeted verification run from `formal/`, with `~/.elan/bin` on `PATH`:

```text
LEAN_NUM_THREADS=1 lake build --wfail Formal.QuadraticPrecision.CountMinimum Formal.QuadraticPrecision.PrecisionArithmetic
```

Result: passed. This was a targeted module build, not a project-wide check or
CI inspection. The final topic audit records kernel replay and axiom checks
separately.

## Final size-bound addition

Also reviewed `precisionDepth_linear_size`. For every
`0<eps<=min(A/4,1)` it bounds the actual construction's common row/variable
upper expression `2n+r(11+10L)+2`, with `L=precisionDepth A eps`, by an
explicit constant independent of accuracy times `1+log2(1/eps)`. The restriction
`eps<=1` ensures the logarithm is nonnegative; `eps<=A/4` permits the established
ceiling bound. The absolute value of `log2 A` makes the coefficient valid for
both small and large positive `A`. Zero rank and zero dimension remain
included. The estimate is a valid uniform size bound; connecting its left-hand
expression to actual constructed systems is supplied separately by the
formulation size theorems.
