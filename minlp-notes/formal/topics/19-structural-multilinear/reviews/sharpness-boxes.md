# Independent review of unit sharpness and original-box transfers

Reviewed 2026-09-20 against F06, Q06, C04 and C05 in
[CLAIMS.md](../CLAIMS.md), the frequency-two and treewidth-two result notes,
and `notes/multilinear-frequency-two-positive-box-obstruction.md`.
The reviewer did not author or edit the reviewed proof modules. The review
excludes `StructuralPositiveFlower`, which this reviewer implemented and which
requires a different independent reviewer.

**The exact gap formulas, explicit witness laws, original-box interpretation,
and stated transfer identities pass review. No mathematical defect was found.
The modules reviewed here do not alone complete F06, Q06 or C04: their graph
membership and bound-instantiation obligations remain separate.** The working
coverage map already describes those integrations as incomplete.

The reviewed modules are `StructuralSharpness`, `StructuralFrequencyCycle`,
`StructuralFrequencySharpness`, `StructuralFrequencySharpnessBox`,
`StructuralFrequencyBox`, and `StructuralCommonAspect`. Supporting uses of
`BilinearGraph` and the baseline-subtracted hull representation in
`StructuralFrequency` were inspected as well.

For the unit flower, `supportPolynomial_eq` identifies the actual polynomial
`a * sum_i x_i + product_i x_i` with a finite original support family and unit
coefficients. Pair supports are injective and never equal the leaf support,
so its term count is not silently reduced. At the specified means, every
bilinear gap is `1/n`, the large-product gap is `1-1/n`, and their sum is
`2-1/n`. The upper endpoint of the polynomial is `2-1/n`, using the common
positive-monomial upper-envelope law. The lower endpoint is `1-1/n`, proved
by a bound valid on every binary vertex and a law attaining its expectation.
The resulting actual hull gap is one, including `n=2`.

The lower law puts mass `1/n` on each state with exactly one failed leaf.
Its anchor is one on one selected atom. It therefore has all required means,
although the anchor is not independent of the failed leaf. Independence is
unnecessary: the number of failed leaves is identically one. This is a valid,
smaller-support alternative to the independent-anchor construction in the
source proof. `ratio_tendsto` and `universal_constant_ge_two` establish the
supremum interpretation; no finite-family ratio is incorrectly asserted to
equal two. The irrelevant `n=0,1` terms of the sequence do not enter the
limit argument.

For each odd length `L=2k+3`, the frequency example uses genuine, distinct
adjacent-pair supports and proves `FrequencyTwo`. Its rounding law chooses a
uniform missing vertex and a fair matching/complement bit. Each coordinate
has mean one half; each factor has coverage `1-1/(2L)`. The universal
pointwise inequality `coveredCount <= selectedCount+k+1`, followed by the
prescribed means, proves that no competing law gives greater total coverage.
The proof of the full hull gap retains the baseline `L/2`; it does not use
raw coverage as a surrogate for the hull width. Consequently the actual
termwise gap is `L/2`, the actual hull gap is `(L-1)/2`, and their ratio is
`L/(L-1)`. The denominator is positive for every parameter. The triangle
specialization is exactly `3/2`.

`StructuralFrequencySharpnessBox` applies proved bilinear affine invariance.
On `[1,rho]`, both original termwise and full hull gaps receive the same
factor `(rho-1)^2`. The gap equalities include `rho=1`, where both gaps are
zero. The ratio theorem requires `rho>1`, so cancellation is valid and its
denominator is positive. The normalization point is the physical midpoint
of every coordinate. No expanded-support structural hypothesis is used.
This establishes the physical witness part of C05; the odd-girth class
membership is the same separate obligation as for Q06.

The unequal-aspect obstruction matches the original source exactly:
`xy+xyz` on `[1,2] x [1,2] x [1,3]`, evaluated at
`(5/4,5/4,5/2)`. Its normalized means are `(1/4,1/4,3/4)`.
The individually certified envelope intervals are `[3/2,7/4]` for `xy` and
`[13/4,19/4]` for `xyz`; the joint interval is `[5,13/2]`. Every endpoint has
an attaining finite law with all three prescribed means. Every endpoint
bound is checked on all eight binary vertices and passed through the actual
multiaffine graph-hull interface. The original termwise gap is therefore
`7/4`, the original hull gap is `3/2`, and the ratio is `7/6`.

The obstruction proves frequency at most two and an explicit factor
coloring. Mathematically its two shared variables are parallel edges between
the two opposite-colored factor vertices; the private third variable has a
leaf dummy vertex. It is bipartite. The file does not separately instantiate
the general dual-multigraph constructor and its bipartite predicate. That
formal bridge is distinct from the checked exact-gap certificate. The
counterexample refutes arbitrary-positive-box bipartite equality, not the
unresolved universal `3/2` bound for such boxes.

The zero-lower transfer rescales each original coefficient by the product
of its coordinate upper bounds and retains exactly the same supports. Its
full-hull identity allows arbitrary coefficients; its termwise identity
uses nonnegative coordinate scale products. Coordinates with zero upper
bounds, empty supports, empty families and boundary means are covered by
the surjective box normalization and do not require division by side lengths.
`zeroLower_gap_bound_transfer` correctly requires the cube bound as an
input. This is a reusable transfer theorem, not a standalone proof of the
frequency-two bound.

The common-aspect transfer keeps a separate indexed original factor for
every `j`, including repeated scopes. It removes fixed coordinates only
from the cardinality count. Their physical lower-bound factors remain in
`product_i l_i`; a fixed zero coordinate correctly annihilates the factor.
The proved vertex table is
`a_j * product_{i in support_j} l_i * rho_j^count`, with nonnegative second
difference proportional to `(rho_j-1)^2`. Its continuous factor is the
original normalized multiaffine monomial, not an exponential of the mean
count. Ratios may differ by original scope. Fixed coordinates, ratio one,
zero weights, unused coordinates and empty factors all remain covered.
Nonnegative lower bounds are a sound generalization of the strictly positive
source case under the stated multiplicative-ratio premise.

The following integrations were still absent from the reviewed modules and
must not be inferred from the arithmetic results:

- F06 needs actual one-variable feedback membership and treewidth exactly
  two for `StructuralSharpness.supports`. Another implementation agent is
  addressing those graph statements.
- Q06 needs a certificate that the actual dual graph of the odd-cycle
  family has odd girth `2k+3`, connecting the witness to the class in the
  sharp odd-girth theorem. Frequency at most two alone does not supply this.
  The frequency integration agent was notified and assigned the bridge.
- C04 needs an application of `commonAspect_original_box_transfer` to the
  proved structural cardinality bound, including preservation of the
  relevant graph hypothesis after removing fixed coordinates. Its `hbound`
  premise is explicit and was not discharged by this reviewed module.
- The full zero-lower frequency result likewise needs its cube-bound
  instantiation. These are integration obligations, not defects in the
  transfer identities.

The following targeted command passed from `formal/`:

```sh
PATH=$HOME/.elan/bin:$PATH LEAN_NUM_THREADS=1 lake build Formal.MultilinearGap.StructuralSharpness Formal.MultilinearGap.StructuralFrequencySharpnessBox Formal.MultilinearGap.StructuralCommonAspect
```

The second targeted command also passed:

```sh
PATH=$HOME/.elan/bin:$PATH LEAN_NUM_THREADS=1 lake env lean /tmp/topic19-sharpness-box-review.lean
```

The temporary file printed axioms for the unit gap and ratio-limit theorems,
odd-cycle gap and positive-box ratio theorems, obstruction gap and ratio
certificates, and both transfer interfaces. All depend only on `propext`,
`Classical.choice` and `Quot.sound`; none use `sorryAx`. No proof edits,
project-wide verification or CI inspection were performed for this review.

Reviewed SHA-256 values:

```text
f1ec795debcf4b63f10e1820490570f327c50eae5228f8239b78977b89bed1e5  StructuralSharpness.lean
f8b036afbeb78e7113b40612e8eb279ff359a5ff13940210076924ab928098d1  StructuralFrequencyCycle.lean
1f73efe087e6e8dfaffa2e03a6f8752c45f98761ac426ebb9afa47bce879631e  StructuralFrequencySharpness.lean
9a94c10a8f99e5b20e0a415e392e7ef3bad3eab744847c459b8569563beebb73  StructuralFrequencySharpnessBox.lean
36c3da02363259b34ed5be27bd021907754e4a2f3a7933702c835ea668a2e829  StructuralFrequencyBox.lean
1c366d716e166b9bc3ecafe4da988d6ddaef424118e86d71f3542a900ce2da6b  StructuralCommonAspect.lean
```
