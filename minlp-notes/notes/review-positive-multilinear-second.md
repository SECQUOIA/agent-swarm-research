# Second independent audit: positive multilinear gap counterexample

Date: 2026-09-04. Reviewer: `review_scaling_characterization`.
Reviewed: sparse dyadic construction in `results/positive-multilinear-gap.md`.

## Verdict and scope

The sparse construction and the analytic divergent ratio bound are correct.
The proof refutes a universal dimension-independent bound for the term-by-term
relaxation gap divided by the convex-hull gap for positive multilinear polynomials
on nonnegative boxes. It already uses unit coefficients, the unit box, and a number
of monomials linear in the number of variables.

I checked the conjecture wording against both the extracted text and a rendered
image of the original PDF: [[luedtke2012-some-results-on-the-strength]] p.22.
The source imposes positive coefficients and nonnegative lower variable bounds;
it does not restrict polynomial degree, number of monomials, or relative marginal
values. The construction satisfies those assumptions. The statement concerns the
universal constant interpretation of the conjecture; it does not exhibit unbounded
ratio for one fixed polynomial as its evaluation point varies.

The earlier dense complete-subset construction is distinct. Its symmetry-reduced
LP values are not exact hull gaps for the sparse construction. This distinction
is correctly reflected in the revised result. This review does not establish
literature novelty beyond checking that the stated conjecture covers the example.

## Construction checked independently

For `L≥2`, let `m=2^L`, take `m` leaf variables and `L` anchors, and for each level
`j=1,...,L` partition the leaves into `2^j` equal blocks of size `m/2^j`.
Partitions may be nested dyadically, although the upper-bound proof only uses
the partition property at each level. Include the monomial

```
a_j ∏_{i∈B} z_i
```

with coefficient one for each block `B` at level `j`. Evaluate at anchor marginals
`a_j=2^(−j)` and leaf marginals `z_i=1−1/m`.

There are exactly `2m−2` monomials and `Lm+2m−2` variable incidences. No two
monomials coincide: anchors distinguish levels and the blocks distinguish terms
within a level. Each term is multilinear. Maximum monomial degree is `m/2+1`,
so this is not a bounded-degree counterexample.

For a degree-`k+1` positive unit monomial on the unit box, the term envelopes at
these marginals are

```
upper = min(2^(−j),1−1/m) = 2^(−j),
lower = max(0,2^(−j)+k(1−1/m)−k) = 0,
```

because `k=m/2^j`. Thus each level contributes one to the term-by-term gap.
The upper term envelopes are jointly attainable: use a common uniform random
variable and set each binary variable to one below its prescribed marginal.
The probability that all variables of a monomial equal one is its smallest
marginal. Therefore the concave envelope and term-by-term gap both equal `L`.

## Exact hull representation and valid count relaxation

For a multilinear polynomial, its graph over a box lies in the convex hull of its
binary-vertex graph. One direct proof is independent Bernoulli interpolation at
each point: the expected polynomial is its multilinear value and the expected
vertex is that point. Consequently the convex envelope at fixed marginals is the
minimum expected polynomial over joint binary distributions with those marginals.

At a binary outcome, let `F` be the failed-leaf set, `R=|F|`, and let `h_j(F)` be the
number of level-`j` blocks intersected by `F`. Then `ER=1` and

```
f(A,Z) = Σ_j A_j [2^j−h_j(F)],
chgap = max E Σ_j A_j h_j(F).
```

The second identity uses `EA_j=2^(−j)`, so the expected first part is exactly `L`
for every admissible joint distribution. Because a failed leaf can hit only one
block per level,

```
0 ≤ h_j(F) ≤ min(2^j,R).
```

Thus the hull gap is at most the maximum of `EΣ_j A_j min(2^j,R)` with the same
anchor marginals and `ER=1`. Passing to arbitrary joint distributions of the count
and anchors is an upper relaxation; equality with the original sparse hull gap
is neither required nor generally established.

## Upper-tail step checked independently

Fix any distribution of `R`. For each anchor, the maximal expected value of
`A_j min(2^j,R)` with selection probability `2^(−j)` is attained by selecting the
largest values of `R`, splitting a probability atom if necessary. This follows by
moving selected mass from a smaller count to a larger unselected count.

Let `r(t)` be the nonincreasing quantile of `R` on `(0,1)`. All these upper-tail
choices are simultaneously feasible by setting `A_j=1[t≤2^(−j)]`; anchor marginals
are the only constraints on anchors in the relaxed problem. Hence

```
chgap ≤ sup_r ∫_0^1 Σ_{j:t≤2^(−j)} min(2^j,r(t)) dt,
```

where `r≥0` and `∫r=1`. The original quantile has additional monotonicity and
boundedness, and dropping those constraints only enlarges the upper bound.

## Entropy estimate checked independently

Put `δ=2^(−L)`. The interval `(0,δ]` contributes less than two because the sum of
all caps is `2^(L+1)−2`. The interval `(1/2,1)` contributes zero.

For `δ<t≤1/2`, let `l` be the largest integer with `t≤2^(−l)`. Then
`2^l≤1/t`, and splitting the geometric sum at `floor(log₂ r)` gives

```
Σ_{j=1}^l min(2^j,r) ≤ r [3+log₂⁺(1/(tr))].
```

For `r≥2^l` the left side is less than `2r`. For `0<r<2`, it is `lr`, which
satisfies the bound since `log₂(2^l/r)>l−1`. For `2≤r<2^l`, the saturated terms
sum to less than `2r` and there are at most `1+log₂(2^l/r)` unsaturated terms.
At `r=0` use the limiting value zero.

Let `D=(δ,1/2)` and `M=∫_D r≤1`. Using explicitly
`log₂⁺s≤ln(1+s)/ln2` and applying Jensen to the probability measure `r(t)dt/M`
when `M>0` gives

```
∫_D r ln(1+1/(tr)) dt
 ≤ M ln(1+(1/M)∫_{D∩{r>0}}dt/t)
 ≤ M ln(1+(L−1)ln2/M)
 ≤ ln(1+(L−1)ln2).
```

The final inequality follows because `M ln(1+B/M)` is increasing for `M>0` and
`B≥0`: its derivative is `ln(1+B/M)−B/(M+B)≥0`. The case `M=0` contributes zero.
Therefore

```
chgap ≤ 5+log₂(1+(L−1)ln2).
```

The hull gap is strictly positive. Under independent Bernoulli variables, each
level's expected polynomial value is `(1−1/m)^(m/2^j)<1`; its sum is below `L`,
so the convex envelope is below the concave envelope.

It is therefore legitimate to divide and conclude

```
tbtgap/chgap ≥ L / [5+log₂(1+(L−1)ln2)] → ∞.
```

Since `n=2^L+L`, this is `Ω(log n/log log n)`. No numerical calculation enters
the proof. The remaining limitations are mathematical scope: degrees grow with
`n`, anchor marginals reach `1/m`, and the result does not by itself address
strengthened formulations that share auxiliary products across terms.

## Further independent audit: exact sparse dyadic hull gap

The author subsequently proposed, and this reviewer independently verified, the
stronger exact formula

```
H_L = s+(L−s)/2^s,
B_q = (L−q+2)/2^q,
B_(s+1) ≤ 1 ≤ B_s.
```

For `L≥2`, such an integer `s` exists in `{1,...,L−1}` because `B_1=(L+1)/2>1`
and `B_L=2^(1−L)<1`. If equality permits either of two adjacent choices, they
give the same formula: subtracting the values at `s` and `s+1` gives
`1−(L−s+1)/2^(s+1)=1−B_(s+1)`, which vanishes at the shared breakpoint.

The exact result assumes nested dyadic partitions. The earlier upper bound
needed only a partition at each level.

### Exact scalar upper bound

Partition the quantile parameter into levels `l=0,...,L`, with weights

```
w_0=1/2,
w_l=2^(−l−1) for 1≤l<L,
w_L=2^(−L).
```

Exactly the anchors `j≤l` are selected on level `l`. Put
`S_l(r)=Σ_{j=1}^l min(2^j,r)`. For any nonnegative `r` and integer `s≥1`,

```
S_l(r) ≤ s r + F_l(s),
F_l(s) = 0                           if l≤s,
F_l(s) = 2^(l−s+1)−2                 if l>s.
```

For `l≤s`, use `S_l(r)≤lr≤sr`. For `l>s`, cap the first `l−s` terms by their
geometric caps and bound each of the remaining `s` terms by `r`. This proves the
bound directly, without a differentiability or relaxation-optimality assumption.

A finite geometric sum gives

```
Σ_l w_l F_l(s) = (L−s)/2^s.
```

Integrating the majorant and using `ER=1` yields
`H_L≤s+(L−s)/2^s`.

### Scalar equality construction

For `q=1,...,L`, on level `l` define

```
R_l^(q) = 0                    if l<q,
R_l^(q) = 2^(l−q+1)           if l≥q.
```

These are admissible integer counts in `[0,m]`. Their mean is

```
Σ_l w_l R_l^(q)
 = (L−q)2^(−q)+2^(1−q)
 = B_q.
```

Mix the `q=s` and `q=s+1` constructions with mixing probability
`η=(1−B_(s+1))/(B_s−B_(s+1))` for the first construction. Since the budgets straddle
one, `0≤η≤1`, and the resulting expected count is one. Sample the quantile level
with probabilities `w_l`, and set `A_j=1[j≤l]`. The anchor marginals are then
`Σ_{l≥j}w_l=2^(−j)` in either construction and their mixture.

Both constructions attain the scalar majorant at every level. If `l<s`, the
count is zero. At `l=s`, the two counts are two and zero; the majorant is tight
throughout `[0,2]`. For `l>s`, the two counts are the endpoints
`2^(l−s)` and `2^(l−s+1)`. On this interval the first `l−s` terms are saturated
and the remaining `s` terms are linear, so equality holds. Hence the mixture
attains `s+(L−s)/2^s` in the relaxed count problem.

### Realizing every count by actual leaf failures

Index leaves by `L`-bit binary strings. A level-`j` dyadic block fixes the first
`j` bits. For an integer `R`, take the bit reversals of the indices
`0,1,...,R−1` as the failed-leaf set. The first `j` bits of these reversed strings
are reversals of the original indices' last `j` bits. Those last bits run through
exactly `min(2^j,R)` residue classes. Thus this failed set hits exactly
`min(2^j,R)` blocks at every level simultaneously.

Randomize this set by a uniform bitwise XOR shift over all `L`-bit strings. Such
a shift permutes the blocks at each level and preserves all block-hit counts.
For any fixed leaf and any failed set of cardinality `R`, exactly `R` shifts
place that leaf in the shifted failed set. Therefore every leaf fails with
conditional probability `R/m`, and unconditional probability `ER/m=1/m`.

This constructs the required joint binary distribution with the correct leaf
and anchor marginals and realizes the relaxed count objective exactly. No
unproved assumption about simultaneously spreading failures across dyadic levels
is needed. It proves equality in the exact formula for the original sparse
polynomial.

### Consequences

The exact term-by-term to hull ratio is

```
L / [s+(L−s)/2^s].
```

The budget inequalities imply `s=log₂ L+O(1)` and `(L−s)/2^s=O(1)`, so
`H_L=log₂ L+O(1)`. The ratio is asymptotic to `L/log₂ L`, equivalently to
`ln n/ln ln n` with `n=2^L+L`. This confirms and sharpens the earlier entropy
bound; the entropy estimate remains a valid upper bound for arbitrary equal-size
level partitions.
