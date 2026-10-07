# Fixed-dimensional polynomial margin away from zeros

Date: 2026-10-02. Status: independent proof review passed, including a
separate cross-check. This review covers the margin lemma below, not the
full flow certificate or its probabilistic composition. No numerical
experiment or general polynomial solver was run.

## Statement and scope

Let `q` be a rational polynomial of fixed degree at most `d` on
`[0,1]^k`. Let `H>=1` bound the binary length of each coefficient, and
let `delta>0` be a rational number in ordinary binary numerator/denominator
encoding. Put

```text
Z = {x in [0,1]^k : q(x)=0},
K = {x in [0,1]^k : dist(x,Z)>=delta}.
```

When `Z` is empty, define `K` to be the whole cube. If `K` is nonempty,
there is an effective uniform bound

```text
min_(x in K) |q(x)| >= 2^(-E_d(k) poly_d(H+bits(delta)+1)),
E_d(k) = (k+1)^(O_d(k^2)).
```

The exponent in the polynomial in coefficient and precision bits is
independent of `k`. The statement concerns distance from the zeros inside
the cube, not from all real zeros of `q`.

## Compactness and the exact scalar formula

Assume first that `k>=1` and `K` is nonempty. The zero set `Z` is compact.
If it is nonempty, its distance function is continuous, so `K` is compact;
if it is empty, compactness is immediate. Because `delta>0`, a zero of
`q` cannot belong to `K`. Thus

```text
m = min_(x in K) |q(x)| > 0.
```

For a free real scalar `t`, use the following formula, where `Box` denotes
the closed unit cube:

```text
exists x in R^k, forall y in R^k:
  Box(x)
  and [not(Box(y) and q(y)=0) or ||x-y||^2>=delta^2]
  and 0<q(x)^2<t.
```

Its satisfying set is exactly `(m^2,infinity)`. The minimum is attained,
so every `t>m^2` has a witness and no `t<=m^2` does. The strict inequality
in `t` therefore causes no endpoint ambiguity. Empty `Z` simply makes
the universal distance condition vacuous.

## Format and coefficient height

The formula has two quantified blocks of size `k`, one free scalar,
`O(k)` atomic occurrences, and degree at most `max(2d,2)`. The squared
polynomial is explicit and still has a number of monomials bounded by a
function of `k,d`.

There are at most `binom(k+d,d)` original coefficients. Clearing their
denominators, squaring `q`, and clearing the denominator of `delta^2`
gives integer coefficient length

```text
L <= f_d(k) (H+bits(delta)+1).
```

All denominator multipliers are positive. In particular, this step does
not raise the coefficient height to an exponent depending on dimension.

The already audited Renegar fixed-block theorem, as recorded in
[the exact polynomial fallback proof](../new-direction/polynomial-exact-fallback.md#4-the-primary-theorem-separates-coefficient-height-from-dimension),
bounds output format and degree by

```text
A_d(k) = (O(k) max(2d,2))^(O(k^2)),
```

and output integer coefficient length by `(L+1) A_d(k)`. Thus a uniform
integer bound `B` on the output coefficient lengths satisfies

```text
B <= E_d(k) poly_d(H+bits(delta)+1).
```

This uses the theorem's separate coefficient-height bound. An arithmetic
operation count alone, or an unrestricted cylindrical-decomposition
bound, would not establish the claimed dependence.

## The positive endpoint gives a dyadic margin

Simplify constant and identically zero polynomial atoms in the scalar
output formula. Its finite boundary `m^2` must be a root of a remaining
nonzero nonconstant atom polynomial `P`. Otherwise all atom signs would
be constant on a neighborhood of `m^2`, contradicting the satisfying
set `(m^2,infinity)`.

Factor any power of `t` out of `P`. This preserves its positive root
`m^2` and leaves a nonzero integer constant coefficient. Every coefficient
has absolute value at most `2^B`, and the constant coefficient has absolute
value at least one. The reciprocal Cauchy root bound therefore gives

```text
m^2 >= 1/(1+2^B) >= 2^(-(B+1)).
```

Consequently the coarser dyadic choice `mu=2^(-(B+1))` is also a lower
bound on `m`: the root bound gives `m>=sqrt(mu)>=mu`. This proves the
stated form without computing the minimizing point or the endpoint.
The uniform format and height bounds alone determine a sufficient `B`.

## Edge cases and use in a precision budget

- If `K` is empty, there is no finite minimum or scalar endpoint to use;
  the assertion about values on `K` is vacuous.
- If `q` is identically zero, positive `delta` forces `K` to be empty.
- A nonzero constant polynomial has empty `Z` and is covered directly
  and by the formula.
- For `k=0`, evaluate the single rational value directly.
- A succinct exponent encoding of `delta` is outside the stated bit
  model; ordinary rational encoding is required.

For fixed `k,d`, the needed dyadic exponent is polynomial in the input
height and the encoding length of `delta`. With `k` as a parameter,
the conclusion supports precision and work budgets of the form
`f_d(k) poly_d(I)`. It does not justify claiming polynomial bit length
in total input size uniformly over varying `k`. Any subsequent sampling
argument must keep its base exponential factor separate from the
polynomial dependence on these added precision bits.

The proof was checked analytically, including the empty-set cases,
strict scalar endpoint, denominator clearing, and reciprocal root bound.
No new literature search, numerical check, project-wide verification,
or CI inspection was performed.
