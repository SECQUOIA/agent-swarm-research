# Review of the bounded-noise magnitude obstruction

Date: 2026-09-22. Independent adversarial review of
[the supporting note](research-20260922-smoothing-magnitude-obstruction.md).

**Verdict:** the scaling argument and its finite-grid ZPP consequence are
correct, conditional on the reviewed fixed-Hessian SUBSET SUM reduction.
No substantive correction is needed. This is a useful scope restriction on
the positive smoothing result, not a new hardness mechanism.

## Scaling and the gap

I read the supporting note and the fixed-Hessian construction in
[the hardness result](../results/indicator-quadratic-treewidth-two-hardness.md).
The latter gives positive penalties, an attained optimum, and the promise
`v <= Delta/4` in the YES case and `v > Delta` in the NO case.

For `s>0`, the map `(x,z) -> (sx,z)` is a bijection between the old and new
indicator-feasible sets. Substitution into the proposed new objective gives
exactly `F_s(sx,z)=s^2 F(x,z)`. In particular, the matrix and graph are
unchanged. This step must scale the linear term by `s`, the indicator penalties
and constant by `s^2`, and the variables by `s`; the note does all four correctly.

For every binary vector, `|xi'z| <= N sigma`. Taking minima on both sides of
the resulting pointwise objective bounds proves
`s^2 v-N sigma <= v_xi <= s^2 v+N sigma`. Therefore the two displayed
thresholds in the note are correct. Their separation is exactly

```
b-a = 3s^2 Delta/4 - 2N sigma > 0.
```

The strict NO inequality survives this comparison. The midpoint distinguishes
all reduced YES and NO instances for every permitted perturbation, including
grid endpoints. Omitting the objective constant requires subtracting
`s^2 c0` from that midpoint; this is correctly stated.

## Penalties, encoding, and an explicit scale

For the stipulated range of `theta`, `0<Delta<1`. The original state penalty
is `Delta/(4n)`, and every original decision penalty `A_i^2` exceeds one.
Thus the smallest original penalty is the state penalty. The stated second
condition on `s` guarantees strict positivity after any noise in the box.
In fact, since `N=2n`, the first condition already implies the second:
`s^2 Delta > (8/3)N sigma > 4n sigma`. Keeping both conditions is harmless.

The proposed integer

```
s = 1 + ceil(8N(1+sigma)/Delta)
```

is sufficient. For example, its strict lower bound gives
`s^2 Delta > 64N^2(1+sigma)^2/Delta`, which exceeds `(8/3)N sigma`
because `Delta<1`, `N>=1`, and `(1+sigma)^2>=4sigma`.
For fixed rational `theta,sigma`, its magnitude is `O(n)` and its binary
length is `O(log n)`. Exact rational comparisons or the displayed ceiling
compute it in polynomial time. Multiplication by `s` or `s^2` preserves the
polynomial encoding length of the original reduction, including its constant
and threshold.

The argument intentionally permits large encoded penalties as well as large
linear coefficients. It does not prove a corresponding obstruction with
unit or uniformly bounded penalties. The stated uniform algorithm must cover
the arbitrary rational penalty data supplied by this construction; its runtime
may depend polynomially on their encoding lengths.

## Complexity implication

The conclusion is a Turing conclusion when the noise has a prescribed rational
grid and can be sampled with polynomially many random bits. Suppose the proposed
solver always returns an exact optimum and its expected bit time, averaged over
that grid and any internal randomization, is polynomial in the encoded input
length for every allowed base instance. Applying it to the scaled reduction
and comparing its output to the midpoint is then a zero-error randomized
decision algorithm for SUBSET SUM with polynomial expected running time.
Finite expectation also implies almost-sure termination.

There is no promise-problem loophole: every SUBSET SUM input mapped by the
reduction satisfies one of the two separated cases, and the usual trivial
excluded input cases can be decided directly. NP-completeness and composition
with deterministic polynomial reductions give `NP subseteq ZPP`.

The proof does not establish this conclusion from an exact real-arithmetic
oracle alone, from a solver that can return an incorrect answer with positive
probability, or from a runtime guarantee that excludes these large-coefficient
base instances. The supporting note makes the relevant finite-grid and
encoding qualifications and correctly avoids a strong NP-hardness claim.

## Verification and significance

I ran a targeted inline Python `Fraction` check of the explicit scale for
60 combinations: `theta` in `{1/10,1/100,3/100}`, `n` in
`{2,3,10,100,1000}`, and `sigma` in `{10^-12,1/3,1,10^12}`.
All strict threshold and positivity inequalities passed. This finite check
tests the formulas across very different magnitudes; the algebra above proves
the universal statement. No project-wide verification, CI inspection, or Lean
formalization was performed.

The significance assessment is appropriate. The result explains why bounded
penalty noise, excellent conditioning, and small blocks do not alone justify
an exact smoothed algorithm polynomial only in input bit length. It does not
conflict with numerical coefficient dependence in the positive theorem.
No independent novelty claim or new external hardness citation is necessary
for this elementary consequence of the explicitly cited local reduction.
